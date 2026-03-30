"""
ui/styles.py
Complete dark-theme CSS injected once at app startup.
"""

GLOBAL_CSS: str = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&family=Source+Sans+3:wght@300;400;600;700&display=swap');

:root {
    --bg:#0d0d14;--surface:#12121c;--s0:#17172a;--s1:#1e1e32;--s2:#252540;
    --b0:#2a2a45;--b1:#343458;
    --blue:#4f9cf9;--blue-lt:#7ab8ff;--blue-dk:#2563eb;
    --blue-g:rgba(79,156,249,0.08);--blue-mid:rgba(79,156,249,0.15);
    --green:#34d399;--green-lt:#6ee7b7;--green-g:rgba(52,211,153,0.08);
    --yellow:#f5c842;--yellow-lt:#fde68a;--yellow-g:rgba(245,200,66,0.08);
    --red:#f87171;--red-lt:#fca5a5;--red-g:rgba(248,113,113,0.08);
    --purple:#a78bfa;--purple-g:rgba(167,139,250,0.08);
    --t0:#ffffff;--t1:#f0efff;--t2:#e8e7ff;--t3:#c8c7f0;--t4:#a0a0c8;
    --font-head:'Segoe UI','Helvetica Neue',Arial,sans-serif;
    --font:'Source Sans 3','Source Sans Pro','Segoe UI',system-ui,sans-serif;
    --mono:'JetBrains Mono','Cascadia Code','Consolas',monospace;
    --sz-xl:16px;--sz-lg:15px;--sz-body:14px;--sz-sm:13px;--sz-xs:12px;
    --shadow-sm:0 1px 6px rgba(0,0,0,.5),0 0 1px rgba(79,156,249,.08);
    --shadow:0 4px 20px rgba(0,0,0,.6),0 0 2px rgba(79,156,249,.10);
    --shadow-lg:0 8px 40px rgba(0,0,0,.7),0 0 4px rgba(79,156,249,.12);
    --radius-sm:4px;--radius:7px;--radius-lg:11px;--radius-xl:16px;
}
*,*::before,*::after{box-sizing:border-box}
.stApp{background:var(--bg)!important;color:var(--t1);font-family:var(--font);font-size:var(--sz-body);line-height:1.6;-webkit-font-smoothing:antialiased}
.stApp::before{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.03) 2px,rgba(0,0,0,.03) 4px);pointer-events:none;z-index:0}
h1,h2,h3,h4{font-family:var(--font-head)!important;color:var(--t0)!important}
h1{font-size:var(--sz-xl)!important;font-weight:700!important}
h2{font-size:var(--sz-lg)!important;font-weight:700!important}
h3{font-size:var(--sz-body)!important;font-weight:600!important}
p,li{font-size:var(--sz-body)!important;color:var(--t0);font-family:var(--font)!important}
code{background:var(--s1)!important;border:1px solid var(--b0)!important;border-radius:var(--radius-sm)!important;padding:2px 6px!important;font-family:var(--mono)!important;font-size:var(--sz-xs)!important;color:var(--blue)!important}
#MainMenu{visibility:hidden}
header[data-testid="stHeader"]{display:none!important}
div[data-testid="stToolbar"]{display:none!important}
div[data-testid="stDecoration"]{display:none!important}
footer{display:none!important}
.block-container{padding-top:0!important;padding-left:1.5rem!important;padding-right:1.5rem!important;max-width:100%!important}
.section-lbl{font-size:var(--sz-xs);font-weight:600;color:var(--t2);text-transform:uppercase;letter-spacing:2px;font-family:var(--mono);margin-bottom:10px;margin-top:2px}
.navbar-title{font-size:15px;font-weight:700;color:var(--t0);font-family:var(--font-head);letter-spacing:-.2px;white-space:nowrap;line-height:1.2}
.navbar-subtitle{font-size:10px;font-weight:400;color:var(--t3);font-family:var(--mono);letter-spacing:.4px;white-space:nowrap}
.navbar-schema-badge{display:inline-flex;align-items:center;gap:6px;border-radius:6px;padding:5px 13px;font-size:12px;font-weight:700;font-family:var(--mono);border:1px solid;white-space:nowrap;letter-spacing:.2px}
.file-card{background:var(--surface);border:1px solid var(--b0);border-top:2px solid var(--blue);border-radius:var(--radius-xl);margin-bottom:18px;overflow:hidden;box-shadow:var(--shadow)}
.file-card-header{background:var(--s0);border-bottom:1px solid var(--b0);padding:13px 20px;display:flex;align-items:center;justify-content:space-between}
.file-card-title{font-size:var(--sz-body);font-weight:700;color:var(--t0);display:flex;align-items:center;gap:10px;font-family:var(--font-head)}
.file-badge{font-family:var(--mono);font-size:10px;font-weight:600;padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:1px}
.badge-unique{background:var(--green-g);color:var(--green);border:1px solid rgba(52,211,153,.3)}
.badge-duplicate{background:var(--yellow-g);color:var(--yellow);border:1px solid rgba(245,200,66,.3)}
.file-card-body{display:grid;grid-template-columns:repeat(4,1fr);padding:18px 24px;gap:0;background:var(--surface)}
.file-stat{display:flex;flex-direction:column;gap:5px}
.file-stat-lbl{font-size:var(--sz-xs);font-weight:600;color:var(--t3);text-transform:uppercase;letter-spacing:1.8px;font-family:var(--mono);margin-bottom:6px}
.file-stat-val{font-size:var(--sz-lg);font-weight:700;color:var(--t0);font-family:var(--font)}
.file-stat-val.accent{color:var(--blue);font-weight:700}
.file-stat-val.mono-sm{font-size:var(--sz-xs);color:var(--t2);letter-spacing:.3px;word-break:break-all;font-weight:400;font-family:var(--mono)}
.file-card-sheets{padding:10px 20px 14px;border-top:1px solid var(--b0);background:var(--s0)}
.sheet-pill-sm{display:inline-block;background:var(--s1);border:1px solid var(--b0);border-radius:4px;padding:3px 10px;font-family:var(--mono);font-size:var(--sz-xs);color:var(--t1);margin:3px 4px 3px 0}
.sheet-card{background:var(--surface);border:1px solid var(--b0);border-left:3px solid var(--blue);border-radius:var(--radius-lg);margin-bottom:16px;overflow:hidden;box-shadow:var(--shadow-sm)}
.sheet-card-hdr{padding:12px 18px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--b0);background:var(--s0)}
.sheet-card-name{font-size:var(--sz-body);font-weight:700;color:var(--t0);display:flex;align-items:center;gap:10px;font-family:var(--font-head)}
.sheet-type-tag{font-family:var(--mono);font-size:10px;padding:3px 10px;border-radius:20px;text-transform:uppercase;letter-spacing:.8px;font-weight:600;background:var(--blue-g);border:1px solid rgba(79,156,249,.2);color:var(--blue)}
.sheet-type-tag.unk{background:var(--s1);border-color:var(--b0);color:var(--t3)}
.sheet-stats-grid{display:grid;grid-template-columns:repeat(6,1fr);padding:14px 18px;gap:12px;background:var(--surface)}
.sh-stat{display:flex;flex-direction:column;gap:5px}
.sh-stat-lbl{font-size:var(--sz-xs);font-weight:600;color:var(--t2);text-transform:uppercase;letter-spacing:1.4px;font-family:var(--mono)}
.sh-stat-val{font-size:var(--sz-body);font-weight:600;color:var(--t0);font-family:var(--font)}
.sh-stat-val.hi{color:var(--green);font-weight:700}
.sh-stat-val.mid{color:var(--yellow);font-weight:700}
.sh-stat-val.hash-sm{font-size:10px;color:var(--t3);letter-spacing:.3px;word-break:break-all;font-weight:400;font-family:var(--mono)}
.claim-card{background:var(--surface);border:1px solid var(--b0);border-radius:var(--radius);padding:12px 14px;margin-bottom:6px;cursor:pointer;transition:border-color .15s,box-shadow .15s,background .15s}
.claim-card:hover{border-color:var(--blue);background:var(--blue-g);box-shadow:var(--shadow-sm)}
.selected-card{border-left:3px solid var(--blue)!important;background:var(--blue-g)!important;box-shadow:0 0 12px rgba(79,156,249,.15)!important}
.status-text{font-size:var(--sz-xs);color:var(--green);margin-top:4px;font-family:var(--mono);font-weight:600;text-transform:uppercase;letter-spacing:.8px}
.status-progress{font-size:var(--sz-xs);color:var(--yellow);margin-top:4px;font-family:var(--mono);font-weight:600;text-transform:uppercase;letter-spacing:.8px}
.sheet-title-banner{background:var(--blue-g);border:1px solid rgba(79,156,249,.2);border-left:3px solid var(--blue);border-radius:var(--radius);padding:11px 16px;margin-bottom:12px}
.sheet-title-label{font-size:var(--sz-xs);color:var(--t2);text-transform:uppercase;font-weight:600;letter-spacing:1.4px;margin-bottom:4px;font-family:var(--mono)}
.sheet-title-value{font-size:var(--sz-body);color:var(--t0);font-weight:700;font-family:var(--font-head)}
.mid-header-title{font-size:var(--sz-lg);font-weight:700;color:var(--t0);margin-bottom:2px;letter-spacing:-.2px;font-family:var(--font-head)}
.mid-header-sub{font-size:var(--sz-body);color:var(--t1);margin-top:2px;margin-bottom:3px;font-family:var(--font)}
.mid-header-status{font-size:var(--sz-xs);color:var(--green);margin-bottom:12px;font-family:var(--mono);font-weight:600;letter-spacing:.8px;text-transform:uppercase}
.incurred-label{font-size:var(--sz-xs);color:var(--t2);margin-bottom:2px;text-transform:uppercase;letter-spacing:1.4px;font-weight:600;font-family:var(--mono)}
.incurred-amount{font-size:var(--sz-lg);font-weight:700;color:var(--green);margin-top:2px;margin-bottom:14px;font-family:var(--font-head);text-shadow:0 0 20px rgba(52,211,153,.3)}
.mandatory-asterisk{display:inline-block;font-size:var(--sz-body);color:var(--blue);font-weight:700;margin-left:3px;vertical-align:middle}
.optional-badge{display:inline-block;background:var(--s1);border:1px solid var(--b0);border-radius:3px;font-size:var(--sz-xs);color:var(--t1);padding:0 5px;margin-left:4px;vertical-align:middle;font-family:var(--mono)}
.custom-field-badge{display:inline-block;background:var(--purple-g);border:1px solid rgba(167,139,250,.3);border-radius:3px;font-size:10px;color:var(--purple);padding:0 5px;margin-left:4px;vertical-align:middle;font-family:var(--mono)}
.llm-mapped-badge{display:inline-block;background:rgba(245,200,66,.1);border:1px solid rgba(245,200,66,.3);border-radius:3px;font-size:10px;color:var(--yellow);padding:0 5px;margin-left:4px;vertical-align:middle;font-family:var(--mono)}
.dup-field-badge{display:inline-block;background:rgba(248,113,113,.1);border:1px solid rgba(248,113,113,.3);border-radius:3px;font-size:10px;color:var(--red);padding:0 5px;margin-left:4px;vertical-align:middle;font-family:var(--mono)}
.add-field-panel{background:var(--s0);border:1px dashed var(--b1);border-radius:var(--radius-lg);padding:14px 16px;margin-top:16px}
.add-field-panel:hover{border-color:var(--purple)}
div[data-baseweb="input"],div[data-baseweb="base-input"],div[data-baseweb="select"]{background-color:var(--s1)!important;border:1px solid var(--b1)!important;border-radius:var(--radius)!important}
div[data-baseweb="input"]:focus-within,div[data-baseweb="base-input"]:focus-within{border-color:var(--blue)!important;box-shadow:0 0 0 3px rgba(79,156,249,.12)!important}
div[data-baseweb="input"] input{color:var(--t0)!important;-webkit-text-fill-color:var(--t0)!important;background-color:transparent!important;font-size:var(--sz-body)!important;padding:8px 12px!important;font-family:var(--font)!important}
div[data-baseweb="input"]:has(input:disabled),div[data-baseweb="base-input"]:has(input:disabled){background-color:transparent!important;border:none!important}
div[data-baseweb="input"] input:disabled{color:var(--t0)!important;-webkit-text-fill-color:var(--t0)!important;cursor:default!important;padding-left:0!important;font-size:var(--sz-body)!important}

/* ── Buttons: base state ── */
div[data-testid="stButton"] button{
    background-color:var(--s1)!important;
    color:var(--t0)!important;
    border:1px solid var(--b1)!important;
    border-radius:var(--radius)!important;
    padding:7px 14px!important;
    transition:all .15s ease!important;
    font-family:var(--font)!important;
    font-size:var(--sz-body)!important;
    font-weight:600!important;
}
/* ── Buttons: hover — keep text WHITE, only border/glow turns blue ── */
div[data-testid="stButton"] button:hover{
    border-color:var(--blue)!important;
    color:var(--t0)!important;
    background-color:var(--blue-g)!important;
    box-shadow:0 0 12px rgba(79,156,249,.15)!important;
}
/* ensure any <p> or <span> inside button stays white on hover */
div[data-testid="stButton"] button:hover p,
div[data-testid="stButton"] button:hover span,
div[data-testid="stButton"] button:hover div{
    color:var(--t0)!important;
    -webkit-text-fill-color:var(--t0)!important;
}
/* ensure SVG icons inside buttons stay visible */
div[data-testid="stButton"] button svg,
div[data-testid="stButton"] button:hover svg{
    fill:var(--t0)!important;
    stroke:var(--t0)!important;
    color:var(--t0)!important;
}

/* ── Primary buttons ── */
div[data-testid="stButton"] button[kind="primary"]{
    background:linear-gradient(135deg,var(--blue-dk) 0%,var(--blue) 100%)!important;
    color:#fff!important;
    border-color:transparent!important;
    font-weight:700!important;
    box-shadow:0 2px 12px rgba(79,156,249,.35)!important;
}
div[data-testid="stButton"] button[kind="primary"]:hover{
    box-shadow:0 4px 20px rgba(79,156,249,.50)!important;
    transform:translateY(-1px);
    color:#fff!important;
}
div[data-testid="stButton"] button:disabled{opacity:.3!important}

/* ── File uploader "Browse files" button ── */
div[data-testid="stFileUploader"] button,
div[data-testid="stFileUploaderDropzone"] button{
    background-color:var(--s1)!important;
    color:var(--t0)!important;
    border:1px solid var(--b1)!important;
    border-radius:var(--radius)!important;
    font-family:var(--font)!important;
    font-size:var(--sz-body)!important;
    font-weight:600!important;
    transition:all .15s ease!important;
}
div[data-testid="stFileUploader"] button:hover,
div[data-testid="stFileUploaderDropzone"] button:hover{
    border-color:var(--blue)!important;
    color:var(--t0)!important;
    background-color:var(--blue-g)!important;
    box-shadow:0 0 12px rgba(79,156,249,.15)!important;
}
/* force text inside Browse Files button to stay white */
div[data-testid="stFileUploader"] button span,
div[data-testid="stFileUploader"] button p,
div[data-testid="stFileUploaderDropzone"] button span,
div[data-testid="stFileUploaderDropzone"] button p{
    color:var(--t0)!important;
    -webkit-text-fill-color:var(--t0)!important;
}

div[role="dialog"]{background-color:var(--surface)!important;border:1px solid var(--b0)!important;border-radius:var(--radius-xl)!important;box-shadow:var(--shadow-lg)!important}
div[role="dialog"] *{color:var(--t1)!important}
div[role="dialog"] h1,div[role="dialog"] h2,div[role="dialog"] h3{color:var(--t0)!important}
div[role="dialog"] button{background:var(--s1)!important;border:1px solid var(--b1)!important;color:var(--t0)!important;border-radius:var(--radius)!important;font-size:var(--sz-body)!important;font-family:var(--font)!important}
div[role="dialog"] button:hover{border-color:var(--blue)!important;color:var(--t0)!important}
.conf-bar-wrap{background:var(--s1);border-radius:4px;height:5px;width:100%;margin-top:4px;overflow:hidden}
.conf-bar-fill{height:100%;border-radius:4px;transition:width .4s ease}
.field-pill{display:inline-block;background:var(--s1);border:1px solid var(--b0);border-radius:4px;padding:4px 12px;font-size:var(--sz-sm);color:var(--t1);margin:3px 4px;font-family:var(--font)}
.field-pill-required{border-color:rgba(79,156,249,.35)!important;color:var(--blue)!important;background:var(--blue-g)!important}
.field-pill-custom{border-color:rgba(52,211,153,.35)!important;color:var(--green)!important;background:var(--green-g)!important}
div[data-baseweb="tab-list"]{background:var(--s0)!important;border-radius:var(--radius) var(--radius) 0 0!important;border-bottom:2px solid var(--b0)!important;padding:0 6px!important}
div[data-baseweb="tab"]{color:var(--t3)!important;font-family:var(--mono)!important;font-weight:600!important;font-size:var(--sz-sm)!important;padding:11px 18px!important;border-bottom:2px solid transparent!important;transition:all .15s!important;margin-bottom:-2px!important}
div[data-baseweb="tab"]:hover{color:var(--t1)!important}
div[data-baseweb="tab"][aria-selected="true"]{color:var(--blue)!important;border-bottom-color:var(--blue)!important;font-weight:700!important}
div[data-baseweb="tab-panel"]{background:var(--surface)!important;border:1px solid var(--b0)!important;border-top:none!important;border-radius:0 0 var(--radius) var(--radius)!important;padding:18px!important}
.stDataFrame thead th{background:var(--s0)!important;color:var(--blue)!important;font-family:var(--mono)!important;font-size:var(--sz-xs)!important;text-transform:uppercase!important;letter-spacing:.9px!important;border-color:var(--b0)!important;font-weight:600!important}
.stDataFrame tbody td{color:var(--t1)!important;font-family:var(--font)!important;font-size:var(--sz-body)!important;border-color:var(--b0)!important}
div[data-testid="stFileUploader"]{background:var(--s0)!important;border:2px dashed var(--b1)!important;border-radius:var(--radius-lg)!important}
div[data-testid="stFileUploader"]:hover{border-color:var(--blue)!important}
::-webkit-scrollbar{width:5px;height:5px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--b1);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--blue)}
hr{border-color:var(--b0)!important;margin:16px 0!important}
div[data-testid="stForm"] div[data-testid="stFormSubmitButton"]{display:none!important}
div[data-testid="stForm"]{border:none!important;padding:0!important}
details{background:var(--s0)!important;border:1px solid var(--b0)!important;border-radius:var(--radius)!important;margin-bottom:8px!important}
details summary{color:var(--t2)!important;font-family:var(--font)!important;font-weight:600!important;font-size:var(--sz-body)!important;padding:10px 14px!important}
div[data-testid="stAlert"]{font-family:var(--font)!important;font-size:var(--sz-body)!important;border-radius:var(--radius)!important}
div[data-testid="stMarkdownContainer"] p,div[data-testid="stMarkdownContainer"] li{font-family:var(--font)!important;font-size:var(--sz-body)!important;color:var(--t0)!important}
div[data-baseweb="select"] span,div[data-baseweb="select"] div{font-family:var(--font)!important;font-size:var(--sz-body)!important}
div[data-testid="stWidgetLabel"] p,div[data-testid="stWidgetLabel"] label{font-family:var(--font)!important;font-size:var(--sz-sm)!important;font-weight:600!important;color:var(--t1)!important}
div[data-testid="stCheckbox"] label{font-family:var(--font)!important;font-size:var(--sz-body)!important;color:var(--t0)!important}
.json-live-panel{background:var(--s0);border:1px solid var(--b0);border-radius:var(--radius-lg);padding:0;overflow:hidden;margin-top:12px}
.json-live-header{background:var(--s1);border-bottom:1px solid var(--b0);padding:8px 14px;display:flex;align-items:center;justify-content:space-between}
.json-live-dot{width:8px;height:8px;background:var(--green);border-radius:50%;animation:pulse-dot 2s infinite;display:inline-block;margin-right:6px}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:.3}}
.json-live-body{padding:12px 14px;font-family:var(--mono);font-size:var(--sz-xs);color:var(--t2);max-height:320px;overflow-y:auto;white-space:pre-wrap;word-break:break-all;line-height:1.7}
.col-summary-panel{background:var(--s0);border:1px solid var(--b1);border-left:3px solid var(--green);border-radius:var(--radius);padding:7px 12px;margin-top:4px;margin-bottom:6px}
.col-summary-text{font-size:var(--sz-xs);color:var(--t2);font-family:var(--font);line-height:1.5}
.llm-map-banner{background:rgba(245,200,66,.07);border:1px solid rgba(245,200,66,.25);border-left:3px solid var(--yellow);border-radius:var(--radius);padding:10px 14px;margin-bottom:12px}

/* ── Tooltip nuclear fix ── */
div[role="tooltip"],
div[role="tooltip"] *,
div[role="tooltip"] p,
div[role="tooltip"] span,
div[role="tooltip"] div{
    background:#1e1e32!important;
    color:#ffffff!important;
    -webkit-text-fill-color:#ffffff!important;
    font-family:var(--font)!important;
    font-size:12px!important;
}

/* ── Selectbox / Dropdown dark theme fix ── */
div[data-baseweb="select"] > div{
    background-color:var(--s1)!important;
    border:1px solid var(--b1)!important;
    border-radius:var(--radius)!important;
    color:var(--t0)!important;
}
div[data-baseweb="select"] > div:focus-within{
    border-color:var(--blue)!important;
    box-shadow:0 0 0 3px rgba(79,156,249,.12)!important;
}
/* Dropdown menu list (the white popup) */
ul[data-baseweb="menu"]{
    background-color:var(--s1)!important;
    border:1px solid var(--b1)!important;
    border-radius:var(--radius)!important;
}
li[role="option"]{
    background-color:var(--s1)!important;
    color:var(--t0)!important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"]{
    background-color:var(--blue-g)!important;
    color:var(--t0)!important;
}
li[role="option"] span,
li[role="option"] div{
    color:var(--t0)!important;
    -webkit-text-fill-color:var(--t0)!important;
}
/* Popover/listbox container */
div[data-baseweb="popover"] div,
div[data-baseweb="popover"] ul{
    background-color:var(--s1)!important;
    border-color:var(--b1)!important;
}

</style>
"""