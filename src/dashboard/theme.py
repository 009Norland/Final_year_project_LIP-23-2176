"""src/dashboard/theme.py — Custom CSS for KRA Litigation Dashboard."""
import streamlit as st

CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --ink:#0A0A0A; --paper:#FAFAF8; --white:#FFFFFF;
        --red:#C0392B; --red-dark:#A93226;
        --line:#E3E1DC; --gray:#6B6B6B; --muted:#9A9A93;
    }

    .stApp { background-color: var(--paper); font-family:'Inter',sans-serif; }
    #MainMenu, footer, header {visibility: hidden;}

    /* ── Sidebar ─────────────────────────────────────────────── */
    section[data-testid="stSidebar"] { background-color: var(--ink); border-right: 1px solid #1E1E1E; }
    section[data-testid="stSidebar"] * { color: #E5E5E5; font-family:'Inter',sans-serif; }
    section[data-testid="stSidebar"] hr { border-color: #222; }

    .sidebar-brand { display:flex; align-items:center; gap:10px; padding:4px 0 18px 0; }
    .sidebar-brand-icon { background:var(--red); border-radius:6px; width:38px; height:38px; display:flex; align-items:center; justify-content:center; font-size:20px; }
    .sidebar-brand-title { font-weight:800; font-size:1.1rem; color:#FFFFFF; line-height:1.1; }
    .sidebar-brand-title span { color:var(--red); font-weight:700; font-size:0.62rem; letter-spacing:1.5px; margin-left:6px; font-family:'JetBrains Mono',monospace; }
    .sidebar-brand-sub { color:#8A8A8A; font-size:0.68rem; letter-spacing:0.5px; font-family:'JetBrains Mono',monospace; text-transform:uppercase; }

    .sidebar-status-box { background:#141414; border-radius:4px; padding:10px 12px; margin-bottom:18px; border:1px solid #232323; }
    .sidebar-status-label { color:#777; font-size:0.62rem; letter-spacing:1.2px; text-transform:uppercase; margin-bottom:4px; font-family:'JetBrains Mono',monospace; }
    .sidebar-status-value { color:#2ECC71; font-size:0.78rem; font-weight:600; }
    .sidebar-status-time { color:#666; font-size:0.68rem; margin-top:4px; font-family:'JetBrains Mono',monospace; }
    .sidebar-section-label { color:#666; font-size:0.64rem; letter-spacing:1.5px; text-transform:uppercase; margin:14px 0 8px 2px; font-weight:700; font-family:'JetBrains Mono',monospace; }
    .sidebar-dossier-box { background:#141414; border-radius:4px; padding:12px; border:1px solid #232323; margin-top:8px; }
    .sidebar-dossier-name { color:#FFFFFF; font-weight:700; font-size:0.86rem; }
    .sidebar-dossier-pin { color:#888; font-size:0.7rem; margin-top:2px; font-family:'JetBrains Mono',monospace; }
    .sidebar-dossier-tag { float:right; color:var(--red); font-weight:700; font-size:0.72rem; font-family:'JetBrains Mono',monospace; }

    /* Sidebar nav radio → looks like a module list */
    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        border-left: 2px solid transparent; padding:8px 0 8px 10px; margin-bottom:2px; border-radius:0;
    }
    section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
        border-left: 2px solid var(--red); background:#141414;
    }

    /* ── Top eyebrow / breadcrumb ────────────────────────────── */
    .top-eyebrow { display:flex; justify-content:space-between; align-items:center; margin-bottom:22px; padding-bottom:14px; border-bottom:1px solid var(--line); }
    .top-eyebrow-left { font-family:'JetBrains Mono',monospace; font-size:0.72rem; letter-spacing:1.5px; color:var(--muted); text-transform:uppercase; }
    .top-eyebrow-right { display:flex; align-items:center; gap:14px; font-family:'JetBrains Mono',monospace; font-size:0.75rem; color:var(--gray); }
    .status-pill { border:1px solid #2ECC71; color:#1E8449; border-radius:20px; padding:3px 12px; font-size:0.72rem; font-family:'JetBrains Mono',monospace; }
    .status-pill::before { content:"● "; }

    /* ── Titles ──────────────────────────────────────────────── */
    .page-eyebrow { font-family:'JetBrains Mono',monospace; font-size:0.72rem; letter-spacing:1.5px; color:var(--muted); text-transform:uppercase; margin-bottom:6px; }
    .page-title { font-family:'Playfair Display',serif; font-size:2.4rem; font-weight:800; color:var(--ink); margin-bottom:2px; line-height:1.15; }
    .page-title span { color:var(--red); display:block; }
    .page-subtitle { color:var(--gray); font-size:0.95rem; margin-bottom:24px; max-width:640px; }

    /* ── KPI pill ────────────────────────────────────────────── */
    .kpi-pill { background:var(--white); border:1px solid var(--line); border-radius:0; padding:10px 16px; display:flex; align-items:center; gap:10px; }
    .kpi-pill-label { color:var(--muted); font-size:0.68rem; font-weight:600; font-family:'JetBrains Mono',monospace; text-transform:uppercase; }
    .kpi-pill-value { color:var(--ink); font-size:1.05rem; font-weight:800; }

    /* ── Stat cards ──────────────────────────────────────────── */
    .stat-card { background:var(--white); border:1px solid var(--line); border-radius:0; padding:18px 18px 14px 18px; height:100%; }
    .stat-card-label { color:var(--muted); font-size:0.68rem; font-weight:700; letter-spacing:1px; text-transform:uppercase; font-family:'JetBrains Mono',monospace; }
    .stat-card-value { font-family:'Playfair Display',serif; font-size:2.1rem; font-weight:800; color:var(--ink); margin:6px 0 6px 0; }
    .stat-card-desc { color:var(--muted); font-size:0.78rem; line-height:1.3; }
    .stat-card-value.red { color:var(--red); }
    .stat-card-value.green { color:#1E8449; }
    .stat-card-value.orange { color:#B9770E; }

    /* ── Panel cards ─────────────────────────────────────────── */
    .panel-card { background:var(--white); border:1px solid var(--line); border-radius:0; padding:20px 22px; margin-bottom:18px; }
    .panel-title { font-family:'Playfair Display',serif; font-weight:700; font-size:1.15rem; color:var(--ink); margin-bottom:2px; }
    .panel-subtitle { color:var(--muted); font-size:0.78rem; margin-bottom:16px; }

    .bar-row { margin-bottom:14px; }
    .bar-row-top { display:flex; justify-content:space-between; font-weight:700; font-size:0.86rem; color:var(--ink); margin-bottom:6px; }
    .bar-track { background:#F0EEE9; border-radius:2px; height:8px; width:100%; overflow:hidden; }
    .bar-fill { height:100%; border-radius:0; }

    /* ── Badges ──────────────────────────────────────────────── */
    .badge { display:inline-block; padding:3px 10px; border-radius:2px; font-size:0.7rem; font-weight:700; font-family:'JetBrains Mono',monospace; border:1px solid transparent; }
    .badge-open { background:#F5F5F5; color:#333; border-color:#DDD; }
    .badge-pending { background:#FDF3DC; color:#B9770E; border-color:#F0DBAE; }
    .badge-closed { background:#EAF6EF; color:#1E8449; border-color:#C9E9D6; }
    .badge-appealed { background:#F4E3FB; color:#7D3C98; border-color:#E4C7F0; }
    .badge-high { background:#FCEBE9; color:var(--red); border-color:#F4C6C0; }
    .badge-medium { background:#FDF3DC; color:#B9770E; border-color:#F0DBAE; }
    .badge-low { background:#EAF6EF; color:#1E8449; border-color:#C9E9D6; }

    /* ── Buttons ─────────────────────────────────────────────── */
    .stButton > button { background-color:var(--red); color:white; border-radius:2px; border:none; font-weight:700; }
    .stButton > button:hover { background-color:var(--red-dark); color:white; }
    .stFormSubmitButton > button { background-color:var(--red); color:white; font-weight:700; border-radius:2px; width:100%; }
    .stFormSubmitButton > button:hover { background-color:var(--red-dark); }
</style>
"""


def inject_theme():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def top_bar(section, page_name, status="Models Online"):
    """Breadcrumb + status pill row, shown at the top of every page."""
    from datetime import datetime
    today = datetime.now().strftime("%d %b %Y")
    st.markdown(f"""
        <div class="top-eyebrow">
            <div class="top-eyebrow-left">{section} &nbsp;·&nbsp; {page_name}</div>
            <div class="top-eyebrow-right">
                <span class="status-pill">{status}</span>
                <span>{today}</span>
            </div>
        </div>""", unsafe_allow_html=True)


def page_header(eyebrow, title_line1, title_line2, subtitle):
    """Eyebrow + two-line serif headline (2nd line in red) + subtitle."""
    st.markdown(f"""
        <div class="page-eyebrow">{eyebrow}</div>
        <div class="page-title">{title_line1}<span>{title_line2}</span></div>
        <div class="page-subtitle">{subtitle}</div>""", unsafe_allow_html=True)


def stat_card(label, value, desc, color=""):
    color_class = f" {color}" if color else ""
    st.markdown(f"""
        <div class="stat-card">
            <div class="stat-card-label">{label}</div>
            <div class="stat-card-value{color_class}">{value}</div>
            <div class="stat-card-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)


def kpi_pill(label, value):
    st.markdown(f"""
        <div class="kpi-pill">
            <div>
                <div class="kpi-pill-label">{label}</div>
                <div class="kpi-pill-value">{value}</div>
            </div>
        </div>""", unsafe_allow_html=True)


def bar_row(label, count, pct, color):
    st.markdown(f"""
        <div class="bar-row">
            <div class="bar-row-top"><span>{label}</span><span>{count} ({pct:.0f}%)</span></div>
            <div class="bar-track"><div class="bar-fill" style="width:{pct}%; background:{color};"></div></div>
        </div>""", unsafe_allow_html=True)


def status_badge(status):
    cls = {"Open":"badge-open","Pending":"badge-pending","Closed":"badge-closed","Appealed":"badge-appealed"}.get(status,"badge-open")
    return f'<span class="badge {cls}">{status}</span>'


def risk_badge(level):
    cls = {"High":"badge-high","Medium":"badge-medium","Low":"badge-low"}.get(level,"badge-low")
    return f'<span class="badge {cls}">{level} Risk</span>'