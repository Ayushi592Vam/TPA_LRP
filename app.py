"""
TPA Loss Run Parser — Main Entry Point
Orchestrates all modules and renders the Streamlit UI.
"""

import os
from dotenv import load_dotenv, find_dotenv

# Load .env before anything else so API keys are available to all modules
_app_dir  = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_app_dir, ".env")
if os.path.exists(_env_path):
    load_dotenv(_env_path, override=True)
else:
    _found = find_dotenv(usecwd=True)
    if _found:
        load_dotenv(_found, override=True)

import streamlit as st

from config.settings import SESSION_DEFAULTS
from config.schemas import SCHEMAS, _CONFIG_LOAD_STATUS
from modules.audit import _append_audit
from modules.storage import (
    _load_hash_store, _save_hash_store,
    _compute_file_sha256, _compute_sheet_sha256,
    _load_from_feature_store, _save_to_feature_store,
)
from modules.file_utils import (
    get_sheet_names, get_sheet_dimensions,
    extract_merged_cell_metadata, extract_totals_row,
)
from modules.parsing import extract_from_excel
from modules.normalization import (
    auto_normalize_on_schema_activate,
    normalize_str,
    rename_columns_to_standard,
)
from modules.schema_mapping import (
    map_claim_to_schema, extract_title_fields,
    _has_unknown_fields, llm_map_unknown_fields,
    detect_claim_id,
)
from modules.enrichment import enrich_claim_cause_of_loss
from modules.dup_detection import _build_field_value_index
from modules.claim_dup_store import check_and_register_claims, get_claim_dup_result
from modules.export import (
    build_mapped_records_for_export,
    to_standard_json, to_guidewire_json, to_duck_creek_json,
    clean_duplicate_fields, _sanitize_for_json,
)
from modules.json_export_table import _append_json_export
from ui.styles import GLOBAL_CSS
from ui.topbar import render_topbar
from ui.file_card import render_file_card
from ui.sheet_card import render_sheet_card
from ui.nav_panel import render_nav_panel
from ui.claim_panel import render_claim_panel
from ui.export_panel import render_export_panel
from ui.claim_dup_panel import render_claim_dup_panel
from ui.dialogs import (
    show_settings_dialog,
    show_schema_fields_dialog,
    show_field_history_dialog,
    show_eye_popup,
    show_cache_manager_dialog,
)

import os
import tempfile
import datetime

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(layout="wide", page_title="TPA Loss Run Parser", page_icon="🛡️")

# ── Global CSS ───────────────────────────────────────────────────────────────
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# ── Session state defaults ───────────────────────────────────────────────────
for _k, _v in SESSION_DEFAULTS.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

# ── One-time migration: clear stale claim dup snapshots with empty fields ─────
if "claim_dup_migrated_v2" not in st.session_state:
    try:
        from modules.claim_dup_store import _load_claim_dup_store, _save_claim_dup_store
        _dup_store = _load_claim_dup_store()
        _cleaned   = {
            cid: snap for cid, snap in _dup_store.items()
            if snap.get("fields") and
            sum(1 for v in snap["fields"].values() if str(v).strip()) /
            max(len(snap["fields"]), 1) >= 0.3
        }
        if len(_cleaned) != len(_dup_store):
            _save_claim_dup_store(_cleaned)
    except Exception:
        pass
    st.session_state["claim_dup_migrated_v2"] = True

if "focus_field" not in st.session_state:
    st.session_state.focus_field = None

# ── Top bar ──────────────────────────────────────────────────────────────────
_settings_clicked = render_topbar(SCHEMAS, _CONFIG_LOAD_STATUS)
if _settings_clicked:
    show_settings_dialog(SCHEMAS, _CONFIG_LOAD_STATUS)

# ── Schema popup ─────────────────────────────────────────────────────────────
if st.session_state.get("schema_popup_target"):
    _target = st.session_state["schema_popup_target"]
    st.session_state["schema_popup_target"] = None
    show_schema_fields_dialog(_target, SCHEMAS)

if st.session_state.get("_open_cache_manager"):
    st.session_state["_open_cache_manager"] = False
    show_cache_manager_dialog()

_, col_sheet_dropdown = st.columns([6.8, 1.2])

# ── File upload ──────────────────────────────────────────────────────────────
uploaded = st.file_uploader("Upload Loss Run Excel/CSV", type=["xlsx", "csv"])

if not uploaded:
    st.stop()

# ── Temp file management ─────────────────────────────────────────────────────
if "tmpdir" not in st.session_state:
    st.session_state.tmpdir = tempfile.mkdtemp()

file_ext   = os.path.splitext(uploaded.name)[1]
excel_path = os.path.join(st.session_state.tmpdir, f"input{file_ext}")

# AFTER
_upload_fingerprint = f"{uploaded.name}_{uploaded.file_id}"
if st.session_state.get("last_uploaded") != _upload_fingerprint:
    with open(excel_path, "wb") as f:
        f.write(uploaded.read())
    st.session_state.last_uploaded = _upload_fingerprint
    st.session_state.sheet_names   = get_sheet_names(excel_path)
    st.session_state.sheet_cache   = {}
    st.session_state.selected_idx  = 0
    st.session_state.focus_field   = None
    # Clear all field-level session state so Modified == Extracted on fresh upload
    for key in list(st.session_state.keys()):
        if (
            key.startswith("_rendered_")
            or key.startswith("_llm_fieldmap_")
            or key.startswith("_claim_dup_results_")
            or key.startswith("mod_")       # modified field values
            or key.startswith("edit_")      # edit mode flags
            or key.startswith("_fv_")       # form version counters
            or key.startswith("_v_")        # version counters
            or key.startswith("err_")       # field error messages
            or key.startswith("disp_")      # display widget keys
            or key.startswith("_frozen_")   # frozen claim IDs
            or key.startswith("chk_")       # checkbox states
            or key.startswith("_chk_")      # checkbox snapshots
            or key.startswith("_col_")      # cause of loss cache
            or key.startswith("show_live_") # JSON preview toggle
            or key.startswith("_std_json")  # export cache
            or key.startswith("_schema_export") # schema export cache
            or key.startswith("user_added_") # custom fields
            or key.startswith("_claim_id_edit_warn_") # claim ID warnings
        ):
            del st.session_state[key]

    file_hash  = _compute_file_sha256(excel_path)
    st.session_state["current_file_hash"] = file_hash

    sheet_hashes = {sn: _compute_sheet_sha256(excel_path, sn) for sn in st.session_state.sheet_names}
    st.session_state["sheet_hashes"] = sheet_hashes

    hash_store = _load_hash_store()
    if file_hash in hash_store:
        st.session_state["is_duplicate_file"]    = True
        st.session_state["duplicate_first_seen"] = hash_store[file_hash]["first_seen"]
        st.session_state["duplicate_orig_name"]  = hash_store[file_hash]["filename"]
    else:
        st.session_state["is_duplicate_file"]    = False
        st.session_state["duplicate_first_seen"] = None
        hash_store[file_hash] = {
            "filename":     uploaded.name,
            "first_seen":   datetime.datetime.now().isoformat(),
            "sheet_hashes": sheet_hashes,
        }
        _save_hash_store(hash_store)
        _append_audit({
            "event": "FILE_INGESTED",
            "timestamp": datetime.datetime.now().isoformat(),
            "filename": uploaded.name,
            "file_hash": file_hash,
            "sheets": st.session_state.sheet_names,
        })

    _sheet_hash_index = {}
    for _fh, _fdata in hash_store.items():
        if _fh == file_hash or not isinstance(_fdata, dict):
            continue
        for _sn, _sh in _fdata.get("sheet_hashes", {}).items():
            _sheet_hash_index[_sh] = {
                "filename":   _fdata.get("filename", "unknown"),
                "sheet_name": _sn,
                "first_seen": _fdata.get("first_seen", "unknown"),
                "file_hash":  _fh,
            }
    st.session_state["sheet_dup_info"] = {
        sn: _sheet_hash_index.get(sh) for sn, sh in sheet_hashes.items()
    }
else:
    file_hash    = st.session_state.get("current_file_hash", "")
    sheet_hashes = st.session_state.get("sheet_hashes", {})

is_dup         = st.session_state.get("is_duplicate_file", False)
sheet_dup_info = st.session_state.get("sheet_dup_info", {})

# ── File card ─────────────────────────────────────────────────────────────────
render_file_card(uploaded, excel_path, file_hash, is_dup, sheet_dup_info, st.session_state.sheet_names)

with col_sheet_dropdown:
    st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
    selected_sheet = st.selectbox(
        "Sheet", st.session_state.sheet_names, index=0, label_visibility="collapsed"
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ── Sheet cache / parse ───────────────────────────────────────────────────────
sh_hash = sheet_hashes.get(selected_sheet, "")

if selected_sheet not in st.session_state.sheet_cache:
    _cached = _load_from_feature_store(sh_hash)

    if _cached:
        _records = _cached.get("records", {})
        _data = []
        for cid, rec in _records.items():
            row = {}
            for fld, fd in rec.items():
                if isinstance(fd, dict) and "value" in fd:
                    row[fld] = {
                        "value":    fd["value"],
                        "modified": fd["value"],   # always reset to raw on load
                        "excel_row": fd.get("excel_row"),
                        "excel_col": fd.get("excel_col"),
                        "original": fd.get("original", fd["value"]),
                    }
            if row:
                _data.append(row)
        if not _data:
            _cached = None

    if not _cached:
        with st.spinner(f"Reading '{selected_sheet}'..."):
            data, sheet_type = extract_from_excel(excel_path, selected_sheet)
            merged_meta      = extract_merged_cell_metadata(excel_path, selected_sheet)
            totals_data      = extract_totals_row(excel_path, selected_sheet)
            total_rows, total_cols = get_sheet_dimensions(excel_path, selected_sheet)
            if not data:
                st.warning(f"No data found in sheet '{selected_sheet}'.")
                st.stop()
            for row in data:
                for fld, inf in row.items():
                    # Normalise only the raw "value" — never auto-change "modified"
                    if "value" in inf and isinstance(inf["value"], str):
                        inf["value"] = normalize_str(inf["value"])
                    # Keep modified in sync with value on fresh parse
                    inf["modified"] = inf.get("value", "")
            _title_flds = extract_title_fields(merged_meta)
            data, _col_rename_log = rename_columns_to_standard(data)

            st.session_state.sheet_cache[selected_sheet] = {
                "data": data, "merged_meta": merged_meta, "totals": totals_data,
                "title_fields": _title_flds, "sheet_type": sheet_type,
                "total_rows": total_rows, "total_cols": total_cols,
                "sheet_hash": sh_hash, "col_rename_log": _col_rename_log,
            }
            st.session_state.selected_idx = 0
            st.session_state.focus_field  = None
            _append_audit({
                "event": "SHEET_PARSED",
                "timestamp": datetime.datetime.now().isoformat(),
                "filename": uploaded.name, "sheet": selected_sheet,
                "sheet_hash": sh_hash, "claim_rows": len(data),
                "sheet_type": sheet_type, "total_rows": total_rows,
                "total_cols": total_cols, "col_renames": _col_rename_log,
            })
            _std_for_store = {}
            for i, row in enumerate(data):
                cid = detect_claim_id(row, i)
                _std_for_store[cid] = {
                    fld: {**inf, "modified": inf.get("modified", inf["value"])}
                    for fld, inf in row.items()
                }
            _save_to_feature_store(sh_hash, selected_sheet, {
                "records": _std_for_store, "sheet_type": sheet_type,
                "total_rows": total_rows, "total_cols": total_cols,
                "sheet_name": selected_sheet, "col_rename_log": _col_rename_log,
            })
    else:
        data        = _data
        sheet_type  = _cached.get("sheet_type", "UNKNOWN")
        total_rows  = _cached.get("total_rows", 0)
        total_cols  = _cached.get("total_cols", 0)
        merged_meta = {}
        totals_data = {}
        _title_flds = {}
        try:
            merged_meta = extract_merged_cell_metadata(excel_path, selected_sheet)
            totals_data = extract_totals_row(excel_path, selected_sheet)
            _title_flds = extract_title_fields(merged_meta)
        except Exception:
            pass
        st.session_state.sheet_cache[selected_sheet] = {
            "data": data, "merged_meta": merged_meta, "totals": totals_data,
            "title_fields": _title_flds, "sheet_type": sheet_type,
            "total_rows": total_rows, "total_cols": total_cols,
            "sheet_hash": sh_hash, "_from_cache": True,
        }
        st.session_state.selected_idx = 0
        st.session_state.focus_field  = None
        _append_audit({
            "event": "SHEET_LOADED_FROM_CACHE",
            "timestamp": datetime.datetime.now().isoformat(),
            "filename": uploaded.name, "sheet": selected_sheet, "sheet_hash": sh_hash,
        })

    _cur_schema = st.session_state.get("active_schema")
    if _cur_schema and _cur_schema in SCHEMAS:
        auto_normalize_on_schema_activate(
            st.session_state.sheet_cache[selected_sheet]["data"], _cur_schema, selected_sheet
        )
        st.session_state.sheet_cache[selected_sheet]["_normalized_for"] = _cur_schema

# ── Active sheet context ──────────────────────────────────────────────────────
active       = st.session_state.sheet_cache[selected_sheet]
data         = active["data"]
merged_meta  = active.get("merged_meta", {})
totals_data  = active.get("totals", {})
title_fields = active.get("title_fields", {})
sheet_type   = active.get("sheet_type", "UNKNOWN")
total_rows   = active.get("total_rows", 0)
total_cols   = active.get("total_cols", 0)
sh_hash      = active.get("sheet_hash", "")
_from_cache  = active.get("_from_cache", False)

# Auto-normalize on schema switch
_active_schema_now = st.session_state.get("active_schema")
_normalized_for    = active.get("_normalized_for")
if _active_schema_now and _active_schema_now in SCHEMAS and _normalized_for != _active_schema_now:
    auto_normalize_on_schema_activate(data, _active_schema_now, selected_sheet)
    active["_normalized_for"] = _active_schema_now

# ── LLM field-map ─────────────────────────────────────────────────────────
# Fires whenever columns look non-standard (schema active OR plain mode).
# Uses Guidewire as the broadest reference schema for plain-mode mapping.
_llm_map_result = {}
_llm_map_ran    = False
_llm_map_count  = 0

if data:
    _sample_keys   = list(data[0].keys()) if data else []
    _ref_schema    = _active_schema_now if (_active_schema_now and _active_schema_now in SCHEMAS) else "Guidewire"
    _needs_llm_map = _has_unknown_fields(_sample_keys, _ref_schema)

    if _needs_llm_map:
        _llm_map_result = llm_map_unknown_fields(data[:5], _ref_schema, selected_sheet)
        _llm_map_count  = len(_llm_map_result.get("mappings", {}))
        _llm_map_ran    = _llm_map_count > 0
        if _llm_map_ran:
            active["_llm_field_map"] = _llm_map_result
            # Apply LLM mappings to rename column keys in data in-place
            # so detect_claim_id and nav panel work correctly
            _llm_mappings = _llm_map_result.get("mappings", {})
            _already_renamed = active.get("_llm_renamed", False)
            if _llm_mappings and not _already_renamed:
                from modules.normalization import rename_columns_to_standard
                active["data"], _extra_renames = rename_columns_to_standard(
                    active["data"], llm_map=_llm_map_result
                )
                data = active["data"]
                active["_llm_renamed"] = True
    else:
        active.pop("_llm_field_map", None)

_llm_map_result = active.get("_llm_field_map", {})

# Field-value dup index
_field_dup_index_key = f"_fdi_{selected_sheet}"
if _field_dup_index_key not in st.session_state:
    st.session_state[_field_dup_index_key] = _build_field_value_index(data, selected_sheet)
_field_dup_index = st.session_state[_field_dup_index_key]

# ── Claim-level duplicate detection (cross-upload) ────────────────────────────
_claim_dup_key = f"_claim_dup_results_{selected_sheet}"
if _claim_dup_key not in st.session_state:
    st.session_state[_claim_dup_key] = check_and_register_claims(
        data=data,
        sheet_name=selected_sheet,
        filename=uploaded.name,
        detect_claim_id_fn=detect_claim_id,
    )
_claim_dup_results = st.session_state[_claim_dup_key]

# ── Sheet card ────────────────────────────────────────────────────────────────
render_sheet_card(
    selected_sheet, sheet_type, sh_hash, len(data), total_rows, total_cols,
    len(merged_meta), totals_data, len(title_fields), _from_cache, sheet_dup_info,
)

# LLM map banner
if _llm_map_ran:
    from ui.sheet_card import render_llm_map_banner
    render_llm_map_banner(_llm_map_result, _llm_map_count)

# ── Three-column layout ───────────────────────────────────────────────────────
curr_claim    = data[st.session_state.selected_idx]

# Freeze claim ID in session state so editing the Claim Number field
# doesn't change the mk/ek/xk keys mid-session and lose edited values.
# The frozen ID is reset only when the user navigates to a different claim.
_frozen_id_key = f"_frozen_claim_id_{selected_sheet}_{st.session_state.selected_idx}"
if _frozen_id_key not in st.session_state:
    st.session_state[_frozen_id_key] = detect_claim_id(curr_claim)
curr_claim_id = st.session_state[_frozen_id_key]

# Enrich Cause of Loss silently
if enrich_claim_cause_of_loss(curr_claim, curr_claim_id, selected_sheet):
    st.rerun()

col_nav, col_main, col_fmt = st.columns([1.2, 3.2, 1.4], gap="large")

with col_nav:
    new_idx = render_nav_panel(data, selected_sheet)
    if new_idx is not None and new_idx != st.session_state.selected_idx:
        # Clear frozen claim ID for the new index so it re-derives from fresh data
        _old_frozen = f"_frozen_claim_id_{selected_sheet}_{new_idx}"
        if _old_frozen in st.session_state:
            del st.session_state[_old_frozen]
        st.session_state.selected_idx = new_idx
        st.session_state.focus_field  = None
        st.rerun()

with col_main:
    render_claim_panel(
        curr_claim=curr_claim,
        curr_claim_id=curr_claim_id,
        active=active,
        selected_sheet=selected_sheet,
        excel_path=excel_path,
        merged_meta=merged_meta,
        totals_data=totals_data,
        title_fields=title_fields,
        uploaded_name=uploaded.name,
        SCHEMAS=SCHEMAS,
        _llm_map_result=_llm_map_result,
        _field_dup_index=_field_dup_index,
        _claim_dup_results=_claim_dup_results,
    )

with col_fmt:
    render_export_panel(
        data=data,
        curr_claim=curr_claim,
        curr_claim_id=curr_claim_id,
        selected_sheet=selected_sheet,
        sh_hash=sh_hash,
        uploaded_name=uploaded.name,
        SCHEMAS=SCHEMAS,
        merged_meta=merged_meta,
        totals_data=totals_data,
        title_fields=title_fields,
        _llm_map_result=_llm_map_result,
    )
