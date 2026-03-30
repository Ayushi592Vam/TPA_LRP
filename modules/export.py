"""
modules/export.py
JSON export formatters: Standard, Guidewire, Duck Creek.
"""

import datetime
import json
import re

import streamlit as st

from modules.schema_mapping import map_claim_to_schema, detect_claim_id


# ── Sanitize for JSON ─────────────────────────────────────────────────────────

def _sanitize_for_json(obj):
    from modules.normalization import normalize_str
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_json(i) for i in obj]
    if isinstance(obj, str):
        return normalize_str(obj)
    return obj


def clean_duplicate_fields(record: dict) -> dict:
    seen: set  = set()
    out:  dict = {}
    for k, v in record.items():
        if k.strip() not in seen:
            seen.add(k.strip())
            out[k.strip()] = v
    return out


# ── Standard JSON ─────────────────────────────────────────────────────────────

def to_standard_json(export_data: dict, sheet_meta: dict, totals: dict, merged_meta: dict) -> dict:
    titles_section = []
    for _, m in sorted(
        [(k, v) for k, v in merged_meta.items() if v.get("value")],
        key=lambda x: (x[1]["row_start"], x[1]["col_start"]),
    ):
        titles_section.append({
            "type": m["type"], "value": m["value"],
            "excel_row": m["excel_row"], "excel_col": m["excel_col"],
            "span_cols": m["span_cols"], "span_rows": m["span_rows"],
        })
    totals_section = {}
    if totals:
        totals_section = {
            "excel_row":  totals.get("excel_row"),
            "rows":       totals.get("rows", []),
            "aggregated": totals.get("aggregated", {}),
        }
    return {
        "exportDate": datetime.datetime.now().isoformat(),
        "sheetMeta":  {"sheet_name": sheet_meta.get("sheet_name"), "record_count": sheet_meta.get("record_count")},
        "titleRows":  titles_section,
        "records":    export_data,
        "totals":     totals_section,
        "recordCount": len(export_data),
    }


# ── Guidewire JSON ────────────────────────────────────────────────────────────

_GW_KEY_MAP: dict[str, str] = {
    "Claim Number":        "claimNumber",
    "Claimant Name":       "claimantName",
    "Loss Date":           "lossDate",
    "Date Reported":       "reportedDate",
    "Total Incurred":      "totalIncurredAmount",
    "Total Paid":          "totalPaidAmount",
    "Reserve":             "reserveAmount",
    "Status":              "status",
    "Line of Business":    "lineOfBusinessCode",
    "Policy Number":       "policyNumber",
    "Insured Name":        "insuredName",
    "Description of Loss": "lossDescription",
    "Cause of Loss":       "causeOfLoss",
}


def to_guidewire_json(mapped_records: list, sheet_meta: dict) -> dict:
    claims = []
    for rec in mapped_records:
        claim_obj  = {"_type": "cc.Claim"}
        financials = {}
        for sf, fd in rec.items():
            if sf.startswith("_"):
                continue
            gw_key = _GW_KEY_MAP.get(sf, sf[0].lower() + sf[1:].replace(" ", ""))
            val    = fd.get("value", "")
            if any(x in sf.lower() for x in ["paid", "reserve", "incurred", "deductible", "recovery", "subrogation"]):
                financials[gw_key] = {"amount": val, "currency": "USD"}
                if fd.get("edited"):
                    financials[gw_key]["originalValue"] = fd.get("original", "")
            else:
                claim_obj[gw_key] = {"value": val}
                if fd.get("edited"):
                    claim_obj[gw_key]["originalValue"] = fd.get("original", "")
        if financials:
            claim_obj["financials"] = financials
        claims.append(claim_obj)
    return {
        "schema":      "Guidewire.ClaimCenter.REST.v1",
        "exportDate":  datetime.datetime.now().isoformat(),
        "source":      "TPA_Loss_Run_Parser",
        "sheetName":   sheet_meta.get("sheet_name", ""),
        "recordCount": len(claims),
        "data":        {"claims": claims},
    }


# ── Duck Creek JSON ───────────────────────────────────────────────────────────

def to_duck_creek_json(mapped_records: list, sheet_meta: dict) -> dict:
    transactions = []
    for rec in mapped_records:
        claim_obj = {}
        for sf, fd in rec.items():
            if sf.startswith("_"):
                continue
            claim_obj[sf] = {
                "value":   fd.get("value", ""),
                "edited":  fd.get("edited", False),
            }
            if fd.get("edited"):
                claim_obj[sf]["originalValue"] = fd.get("original", "")
        transactions.append({
            "transactionType": "UPDATE",
            "claim":           claim_obj,
        })
    return {
        "schema":      "DuckCreek.Claims.Transaction.v6",
        "exportDate":  datetime.datetime.now().isoformat(),
        "source":      "TPA_Loss_Run_Parser",
        "sheetName":   sheet_meta.get("sheet_name", ""),
        "recordCount": len(transactions),
        "transactions": transactions,
    }


# ── Build mapped records for export ──────────────────────────────────────────

def build_mapped_records_for_export(data: list, schema_name: str, selected_sheet: str) -> list:
    from config.schemas import SCHEMAS
    schema      = SCHEMAS[schema_name]
    custom_flds = st.session_state.get(f"custom_fields_{schema_name}", [])
    export_flds = list(schema["required_fields"]) + [
        f for f in custom_flds if f not in schema["required_fields"]
    ]
    title_fields = st.session_state.get("sheet_cache", {}).get(selected_sheet, {}).get("title_fields", {})
    records      = []
    for i, row in enumerate(data):
        c_id   = detect_claim_id(row, i)
        mapped = map_claim_to_schema(row, schema_name, title_fields)
        rec    = {}
        confs  = []
        for sf in export_flds:
            if sf not in mapped:
                rec[sf] = {"value": "", "confidence": 0, "edited": False, "original": ""}
                confs.append(0)
                continue
            m       = mapped[sf]
            mk_key  = f"mod_{selected_sheet}_{c_id}_schema_{sf}"
            live_val = st.session_state.get(mk_key, None)
            orig    = m["info"].get("value", "")
            final   = live_val if live_val is not None else m["value"]
            rec[sf] = {
                "value":      final,
                "original":   orig,
                "edited":     final != orig,
                "confidence": m["confidence"],
                "excel_row":  m["info"].get("excel_row"),
                "excel_col":  m["info"].get("excel_col"),
            }
            confs.append(m["confidence"])
        rec["_avg_confidence"] = round(sum(confs) / len(confs)) if confs else 0
        rec["_claim_id"]       = c_id
        records.append(rec)
    return records
