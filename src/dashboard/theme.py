"""src/dashboard/theme.py — Custom CSS for KRA Litigation Dashboard."""
import streamlit as st

CUSTOM_CSS = """
<style>
    .stApp { background-color: #F4F6F8; }
    #MainMenu, footer, header {visibility: hidden;}

    section[data-testid="stSidebar"] { background-color: #111315; border-right: 1px solid #232323; }
    section[data-testid="stSidebar"] * { color: #E5E5E5; }
    section[data-testid="stSidebar"] hr { border-color: #2A2A2A; }

    .sidebar-brand { display:flex; align-items:center; gap:10px; padding:4px 0 18px 0; }
    .sidebar-brand-icon { background:#C0392B; border-radius:8px; width:38px; height:38px; display:flex; align-items:center; justify-content:center; font-size:20px; }
    .sidebar-brand-title { font-weight:800; font-size:1.15rem; color:#FFFFFF; line-height:1.1; }
    .sidebar-brand-title span { color:#E67E22; font-weight:700; font-size:0.65rem; letter-spacing:1px; margin-left:6px; }
    .sidebar-brand-sub { color:#9A9A9A; font-size:0.75rem; }
    .sidebar-status-box { background:#1A1C1E; border-radius:8px; padding:10px 12px; margin-bottom:18px; border:1px solid #262626; }
    .sidebar-status-label { color:#8A8A8A; font-size:0.65rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:4px; }
    .sidebar-status-value { color:#2ECC71; font-size:0.8rem; font-weight:600; }
    .sidebar-status-time { color:#777; font-size:0.7rem; margin-top:4px; }
    .sidebar-section-label { color:#707070; font-size:0.68rem; letter-spacing:1.2px; text-transform:uppercase; margin:14px 0 8px 2px; font-weight:700; }
    .sidebar-dossier-box { background:#1A1C1E; border-radius:8px; padding:12px; border:1px solid #262626; margin-top:8px; }
    .sidebar-dossier-name { color:#FFFFFF; font-weight:700; font-size:0.88rem; }
    .sidebar-dossier-pin { color:#999; font-size:0.72rem; margin-top:2px; }
    .sidebar-dossier-tag { float:right; color:#E67E22; font-weight:700; font-size:0.75rem; }

    .page-title { font-size:1.7rem; font-weight:800; color:#1A1A1A; margin-bottom:2px; }
    .page-subtitle { color:#7C8896; font-size:0.92rem; margin-bottom:18px; }

    .kpi-pill { background:#FFFFFF; border:1px solid #E6E9EC; border-radius:10px; padding:10px 16px; display:flex; align-items:center; gap:10px; }
    .kpi-pill-label { color:#8A93A0; font-size:0.72rem; font-weight:600; }
    .kpi-pill-value { color:#111; font-size:1.05rem; font-weight:800; }

    .stat-card { background:#FFFFFF; border:1px solid #E9ECEF; border-radius:12px; padding:18px 18px 14px 18px; height:100%; }
    .stat-card-label { color:#8A93A0; font-size:0.72rem; font-weight:700; letter-spacing:0.5px; text-transform:uppercase; }
    .stat-card-value { font-size:2.1rem; font-weight:800; color:#1A1A1A; margin:4px 0 6px 0; }
    .stat-card-desc { color:#9AA3AE; font-size:0.78rem; line-height:1.3; }
    .stat-card-value.red { color:#E74C3C; }
    .stat-card-value.green { color:#27AE60; }
    .stat-card-value.orange { color:#E67E22; }

    .panel-card { background:#FFFFFF; border:1px solid #E9ECEF; border-radius:12px; padding:20px 22px; margin-bottom:18px; }
    .panel-title { font-weight:800; font-size:1.02rem; color:#1A1A1A; margin-bottom:2px; }
    .panel-subtitle { color:#9AA3AE; font-size:0.78rem; margin-bottom:16px; }

    .bar-row { margin-bottom:14px; }
    .bar-row-top { display:flex; justify-content:space-between; font-weight:700; font-size:0.88rem; color:#222; margin-bottom:6px; }
    .bar-track { background:#EEF1F4; border-radius:6px; height:9px; width:100%; overflow:hidden; }
    .bar-fill { height:100%; border-radius:6px; }

    .badge { display:inline-block; padding:3px 10px; border-radius:20px; font-size:0.72rem; font-weight:700; }
    .badge-open { background:#E8F1FE; color:#2E75B6; }
    .badge-pending { background:#FDF3DC; color:#B9770E; }
    .badge-closed { background:#E3F8EC; color:#1E8449; }
    .badge-appealed { background:#F4E3FB; color:#7D3C98; }
    .badge-high { background:#FCE4E2; color:#C0392B; }
    .badge-medium { background:#FDF3DC; color:#B9770E; }
    .badge-low { background:#E3F8EC; color:#1E8449; }

    .stButton > button { background-color:#C0392B; color:white; border-radius:8px; border:none; font-weight:700; }
    .stButton > button:hover { background-color:#A93226; color:white; }
    .stFormSubmitButton > button { background-color:#C0392B; color:white; font-weight:700; border-radius:8px; width:100%; }
    .stFormSubmitButton > button:hover { background-color:#A93226; }
</style>
"""


def inject_theme():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


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
