"""src/dashboard/app.py — KRA-LIP Litigation Dashboard with Auth."""
import sys
from pathlib import Path
from datetime import datetime, timezone

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from src.dashboard.theme import (inject_theme, stat_card, kpi_pill, bar_row,
                                status_badge, risk_badge, top_bar, page_header)
from src.dashboard import case_store
from src.dashboard.auth import login, sign_up, seed_admin, get_all_users, delete_user

st.set_page_config(page_title="KRA Legal — Litigation Intelligence",
                page_icon="⚖️", layout="wide", initial_sidebar_state="expanded")
inject_theme()

st.markdown("""
<style>
.auth-box {
    background: #FFFFFF;
    border: 1px solid #E3E1DC;
    border-radius: 0;
    padding: 40px 40px 32px 40px;
    max-width: 440px;
    margin: 60px auto 0 auto;
    box-shadow: 0 4px 24px rgba(0,0,0,0.06);
}
.auth-logo-icon {
    background: #C0392B;
    border-radius: 6px;
    width: 52px;
    height: 52px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    margin-bottom: 8px;
}
.auth-title {
    text-align: center;
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #0A0A0A;
    margin-bottom: 4px;
}
.auth-subtitle {
    text-align: center;
    color: #9A9A93;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin-bottom: 24px;
}
.auth-divider {
    border: none;
    border-top: 1px solid #E3E1DC;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

CASE_TYPES     = ["VAT","Income Tax","Customs Duty","Excise Duty","PAYE","Withholding Tax"]
COURT_LEVELS   = ["Tax Appeals Tribunal","High Court","Court of Appeal"]
TAXPAYER_CATS  = ["Individual","SME","Large Corporation","Multinational"]
LEGAL_GROUNDS  = ["Incorrect Assessment","Procedural Error","Statute of Limitations",
                "Double Taxation","Transfer Pricing Dispute","Exemption Claim",
                "Valuation Dispute","Input Tax Credit"]
REPRESENTATION = ["Self-Represented","Legal Counsel","Tax Consultant"]
STATUSES       = ["Open","Pending","Closed","Appealed"]

# ── Initialize session state defaults ─────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = {}
if "show_signup" not in st.session_state:
    st.session_state["show_signup"] = False
if "selected_case_id" not in st.session_state:
    st.session_state["selected_case_id"] = None
seed_admin()
case_store.seed_demo_cases()

# AUTH PAGES
def show_login():
    st.markdown("""
        <div class="auth-box">
            <div style="text-align:center;margin-bottom:8px;">
                <div class="auth-logo-icon">⚖️</div>
                <div class="auth-title">KRA Legal</div>
                <div class="auth-subtitle">Litigation Intelligence Platform</div>
            </div>
    """, unsafe_allow_html=True)

    username = st.text_input("Username", placeholder="Enter your username")
    password = st.text_input("Password", placeholder="Enter your password", type="password")

    if st.button("Login", use_container_width=True):
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            success, user = login(username, password)
            if success:
                st.session_state["user"]      = user
                st.session_state["logged_in"] = True
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.markdown("<hr class='auth-divider'>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;color:#9A9A93;font-size:0.85rem;'>"
                "Don't have an account?</div>", unsafe_allow_html=True)

    if st.button("Create Account", use_container_width=True):
        st.session_state["show_signup"] = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center;color:#AAA;font-size:0.75rem;margin-top:16px;'>"
                "Default admin — username: <b>admin</b> &nbsp;/&nbsp; password: <b>admin123</b>"
                "</div>", unsafe_allow_html=True)


def show_signup():
    st.markdown("""
        <div class="auth-box">
            <div style="text-align:center;margin-bottom:8px;">
                <div class="auth-logo-icon">⚖️</div>
                <div class="auth-title">Create Account</div>
                <div class="auth-subtitle">KRA Legal Intelligence Platform</div>
            </div>
    """, unsafe_allow_html=True)

    full_name = st.text_input("Official Full Name",
                            placeholder="e.g. John Omondi Kariuki",
                            key="signup_fullname")
    username  = st.text_input("Username",
                            placeholder="No spaces — e.g. JohnOmondi",
                            key="signup_username")
    password  = st.text_input("Password",
                            placeholder="At least 6 characters",
                            type="password",
                            key="signup_password")
    confirm   = st.text_input("Confirm Password",
                            placeholder="Repeat your password",
                            type="password",
                            key="signup_confirm")
    role      = st.selectbox("Role", ["Legal Officer", "Admin"], key="signup_role")

    if st.button("Create Account", use_container_width=True):
        fn = st.session_state.get("signup_fullname", "").strip()
        un = st.session_state.get("signup_username", "").strip()
        pw = st.session_state.get("signup_password", "").strip()
        cf = st.session_state.get("signup_confirm", "").strip()
        rl = st.session_state.get("signup_role", "Legal Officer")

        if not fn or not un or not pw or not cf:
            st.error("All fields are required.")
        elif pw != cf:
            st.error("Passwords do not match.")
        else:
            success, msg = sign_up(fn, un, pw, rl)
            if success:
                st.success(f"{msg} You can now log in.")
                st.session_state["show_signup"] = False
                st.rerun()
            else:
                st.error(msg)

    st.markdown("<hr class='auth-divider'>", unsafe_allow_html=True)
    if st.button("Back to Login", use_container_width=True):
        st.session_state["show_signup"] = False
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ── AUTH CHECK — must be here ──────────────────────────────────────────────────
if not st.session_state["logged_in"]:
    if st.session_state["show_signup"]:
        show_signup()
    else:
        show_login()
    st.stop()

# MAIN APP
user      = st.session_state.get("user", {})
username  = user.get("username", "")
full_name = user.get("full_name", username)
role      = user.get("role", "")
is_admin  = role == "Admin"


def get_cases_for_user():
    all_c = case_store.get_all_cases()
    if is_admin:
        return all_c
    return [c for c in all_c if c.get("assigned_to") in (username, None, "")]


# Sidebar
with st.sidebar:
    st.markdown("""
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">⚖️</div>
            <div>
                <div class="sidebar-brand-title">KRA <span>LEGAL</span></div>
                <div class="sidebar-brand-sub">Intelligence Platform</div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown(f"""
        <div class="sidebar-status-label" style="margin-top:12px;">LOGGED IN AS</div>
        <div class="sidebar-dossier-box">
            <div class="sidebar-dossier-name">{full_name}</div>
            <div class="sidebar-dossier-pin">{username} &nbsp;|&nbsp; {role}
                <span class="sidebar-dossier-tag">{'ALL ACCESS' if is_admin else 'LIMITED'}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section-label" style="margin-top:16px;">NAVIGATION</div>',
                unsafe_allow_html=True)

    visible_cases = get_cases_for_user()
    nav_options  = ["Dashboard", "Upload Case", "View Cases"]
    nav_captions = ["Overview", "Register a new dispute", "Case records"]
    if is_admin:
        nav_options.append("Admin Panel")
        nav_captions.append("User management")

    try:
        page = st.radio("nav", nav_options, captions=nav_captions, label_visibility="collapsed")
    except TypeError:
        # older Streamlit versions without the `captions` kwarg
        page = st.radio("nav", nav_options, label_visibility="collapsed")

    st.markdown(f"<div style='color:#666;font-size:0.72rem;margin-top:4px;'>"
                f"Cases visible: {len(visible_cases)}</div>", unsafe_allow_html=True)

    sel_id   = st.session_state.get("selected_case_id")
    sel_case = case_store.get_case(sel_id) if sel_id else (visible_cases[0] if visible_cases else None)
    if sel_case:
        wp = sel_case.get("win_probability", 0)
        st.markdown(f"""
            <div class="sidebar-section-label" style="margin-top:20px;">SELECTED DOSSIER</div>
            <div class="sidebar-dossier-box">
                <div class="sidebar-dossier-name">{sel_case.get('taxpayer_name', '-')}</div>
                <div class="sidebar-dossier-pin">PIN: {sel_case.get('pin', '-')}
                    <span class="sidebar-dossier-tag">{wp:.0f}% KRA</span>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# Helpers
def metrics(cases):
    df = pd.DataFrame(cases) if cases else pd.DataFrame()
    n  = len(df)
    def cnt(col, val): return int((df[col] == val).sum()) if n else 0
    def wp_cnt(op, thresh): return int(op(df["win_probability"].fillna(100), thresh).sum()) if n else 0
    return {
        "total":       n,
        "open":        cnt("status", "Open"),
        "pending":     cnt("status", "Pending"),
        "closed":      cnt("status", "Closed"),
        "appealed":    cnt("status", "Appealed"),
        "high_risk":   wp_cnt(lambda a, b: a < b, 50),
        "medium_risk": wp_cnt(lambda a, b: (a >= 50) & (a < 70), 70),
        "low_risk":    wp_cnt(lambda a, b: a >= b, 70),
        "portfolio":   df["disputed_amount"].sum() if n and "disputed_amount" in df else 0,
        "win_rate":    df["win_probability"].mean() if n and "win_probability" in df else 0,
    }


def run_prediction(case_data):
    try:
        from src.case_predictor.predictor import predict_case
        r  = predict_case(case_data)
        wp = round(100 - r["probability"] * 100, 1)
        return {"prediction": r["prediction"], "win_probability": wp,
                "risk_level": "High" if wp < 50 else ("Medium" if wp < 70 else "Low"),
                "recommendation": r["recommendation"], "shap_values": r.get("shap_values")}
    except Exception:
        score = 70
        if case_data.get("legal_grounds") == "Procedural Error": score -= 20
        if case_data.get("representation") == "Legal Counsel":   score -= 12
        if case_data.get("court_level") == "Court of Appeal":    score -= 15
        if case_data.get("disputed_amount", 0) > 5_000_000:      score -= 8
        score = max(5, min(95, score))
        return {"prediction": "KRA Wins" if score >= 50 else "KRA Loses",
                "win_probability": score,
                "risk_level": "High" if score < 50 else ("Medium" if score < 70 else "Low"),
                "recommendation": "Using heuristic estimate — train the model for real predictions.",
                "shap_values": None}

# PAGE: DASHBOARD
if page == "Dashboard":
    top_bar("OVERVIEW", "DASHBOARD")
    cases = get_cases_for_user()
    m = metrics(cases)

    col_title, col_k1, col_k2 = st.columns([3, 1, 1])
    with col_title:
        page_header("OVERVIEW — LITIGATION", "Legal Intelligence", "Dashboard",
                    "Real-time overview of active tax disputes, ML predictions, and risk levels.")
    with col_k1: kpi_pill("Portfolio Sum:", f"Ksh {m['portfolio']:,.0f}")
    with col_k2: kpi_pill("KRA Win:", f"{m['win_rate']:.0f}%")

    st.write("")
    c1, c2, c3, c4 = st.columns(4)
    with c1: stat_card("TOTAL CASES",     m["total"],     "Total cases in the system.")
    with c2: stat_card("OPEN CASES",      m["open"],      "Cases currently being handled.")
    with c3: stat_card("HIGH RISK CASES", m["high_risk"], "Cases KRA is likely to lose.", "red")
    with c4: stat_card("CLOSED CASES",   m["closed"],    "Concluded cases.", "green")

    st.write("")
    col_l, col_r = st.columns(2)
    total = max(m["total"], 1)

    with col_l:
        st.markdown('<div class="panel-card"><div class="panel-title">Cases by Risk Level</div>'
                    '<div class="panel-subtitle">Distribution by risk exposure rating.</div>',
                    unsafe_allow_html=True)
        bar_row("High Risk",   m["high_risk"],   m["high_risk"] / total * 100,   "#C0392B")
        bar_row("Medium Risk", m["medium_risk"], m["medium_risk"] / total * 100, "#B9770E")
        bar_row("Low Risk",    m["low_risk"],    m["low_risk"] / total * 100,    "#1E8449")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="panel-card"><div class="panel-title">Cases by Status</div>'
                    '<div class="panel-subtitle">Distribution by legal proceedings status.</div>',
                    unsafe_allow_html=True)
        bar_row("Open",     m["open"],     m["open"] / total * 100,     "#0A0A0A")
        bar_row("Pending",  m["pending"],  m["pending"] / total * 100,  "#B9770E")
        bar_row("Closed",   m["closed"],   m["closed"] / total * 100,   "#1E8449")
        bar_row("Appealed", m["appealed"], m["appealed"] / total * 100, "#7D3C98")
        st.markdown("</div>", unsafe_allow_html=True)

    if cases:
        df = pd.DataFrame(cases)
        if "case_type" in df.columns and "disputed_amount" in df.columns:
            st.markdown('<div class="panel-card"><div class="panel-title">Disputed Amount by '
                        'Case Type</div><div class="panel-subtitle">Where financial exposure '
                        'is concentrated.</div>', unsafe_allow_html=True)
            grp = df.groupby("case_type")["disputed_amount"].sum().reset_index().sort_values(
                "disputed_amount", ascending=True)
            fig = px.bar(grp, x="disputed_amount", y="case_type", orientation="h",
                        color_discrete_sequence=["#C0392B"])
            fig.update_layout(height=300, margin=dict(l=10, r=10, t=10, b=10),
                            xaxis_title="Disputed Amount (KES)", yaxis_title="",
                            plot_bgcolor="white", paper_bgcolor="white",
                            font=dict(family="Inter"))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

# PAGE: UPLOAD CASE
elif page == "Upload Case":
    top_bar("MODULE 01", "UPLOAD CASE")
    page_header("REGISTER — NEW DISPUTE", "Upload New", "Case",
                "Register a new tax dispute and get an instant outcome forecast.")
    st.write("")

    tab1, tab2 = st.tabs(["Manual Entry", "Upload Document"])

    with tab1:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        with st.form("upload_case_form"):
            c1, c2 = st.columns(2)
            with c1:
                taxpayer_name   = st.text_input("Taxpayer / Company Name",
                                                placeholder="e.g. Kipchoge Tea Exporters Ltd")
                pin             = st.text_input("Taxpayer PIN",
                                                placeholder="e.g. A012345678B")
                plaintiff       = st.text_input("Plaintiff",
                                                placeholder="Who is suing")
                defendant       = st.text_input("Defendant",
                                                placeholder="Who is being sued")
                case_type       = st.selectbox("Case Type", CASE_TYPES)
                disputed_amount = st.number_input("Disputed Amount (KES)",
                                                min_value=0.0,
                                                value=2_000_000.0,
                                                step=50_000.0,
                                                format="%.2f")

            with c2:
                court_level    = st.selectbox("Court Level", COURT_LEVELS)
                legal_grounds  = st.selectbox("Legal Grounds", LEGAL_GROUNDS)
                representation = st.selectbox("Taxpayer Representation", REPRESENTATION)
                taxpayer_cat   = st.selectbox("Taxpayer Category", TAXPAYER_CATS)
                status         = st.selectbox("Case Status", STATUSES)
                if is_admin:
                    all_users    = get_all_users()
                    officer_list = [u["username"] for u in all_users
                                    if u["role"] == "Legal Officer"]
                    assigned_to  = st.selectbox("Assign to Legal Officer",
                                                ["Unassigned"] + officer_list)
                else:
                    assigned_to = username

            submitted = st.form_submit_button("Submit Case and Run Forecast",
                                            use_container_width=True)

        if submitted:
            if not taxpayer_name or not pin:
                st.error("Please provide Taxpayer Name and PIN.")
            elif not plaintiff or not defendant:
                st.error("Please provide both Plaintiff and Defendant.")
            else:
                try:
                    case_data = {
                        "taxpayer_name":          taxpayer_name,
                        "pin":                    pin,
                        "plaintiff":              plaintiff,
                        "defendant":              defendant,
                        "case_type":              case_type,
                        "disputed_amount":        disputed_amount,
                        "court_level":            court_level,
                        "legal_grounds":          legal_grounds,
                        "representation":         representation,
                        "taxpayer_category":      taxpayer_cat,
                        "status":                 status,
                        "assigned_to":            assigned_to if assigned_to != "Unassigned" else "",
                        "created_by":             full_name,
                        "case_duration_days":     365,
                        "prior_compliance_score": 50,
                        "num_prior_disputes":     0,
                        "taxpayer_risk_score":    20,
                    }

                    pred = run_prediction(case_data)
                    case_data.update({
                        "prediction":      pred["prediction"],
                        "win_probability": pred["win_probability"],
                        "risk_level":      pred["risk_level"],
                    })

                    new_id = case_store.add_case(case_data)

                    if new_id:
                        st.success(f"Case {new_id} successfully registered for {taxpayer_name}.")
                        st.info(
                            f"{pred['risk_level'].upper()} RISK | "
                            f"{pred['prediction']} | "
                            f"KRA Win Probability: {pred['win_probability']:.0f}%\n\n"
                            f"{pred['recommendation']}"
                        )
                        st.session_state["selected_case_id"] = new_id
                        st.balloons()
                    else:
                        st.error("Case was not saved. Please try again.")

                except Exception as e:
                    import traceback
                    st.error(f"Failed to save case: {e}")
                    st.code(traceback.format_exc())
        st.markdown("</div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="panel-card">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title">Classify a Legal Document</div>',
                    unsafe_allow_html=True)
        st.markdown('<div class="panel-subtitle">Auto-classify incoming documents and extract '
                    'key fields.</div>', unsafe_allow_html=True)
        doc_text = st.text_area("Paste document text here", height=180,
                                placeholder="Paste a demand notice, court summons, "
                                            "tribunal ruling, etc.")
        uploaded = st.file_uploader("Or upload a .txt file", type=["txt"])
        if uploaded:
            doc_text = uploaded.read().decode("utf-8")
            st.text_area("Preview",
                        doc_text[:400] + ("..." if len(doc_text) > 400 else ""),
                        height=100)
        if st.button("Classify Document", use_container_width=True):
            if not doc_text:
                st.error("Please paste or upload a document first.")
            else:
                try:
                    from src.document_intelligence.classifier import classify_document
                    r   = classify_document(doc_text)
                    ent = r.get("entities", {})
                    st.success(f"Document Type: {r['doc_type']}  |  "
                            f"Confidence: {r['confidence']}%")
                    e1, e2, e3 = st.columns(3)
                    e1.write(f"PIN: {ent.get('pin', 'Not found')}")
                    e2.write(f"Case No: {ent.get('case_number', 'Not found')}")
                    e3.write(f"Amounts: {', '.join(ent.get('amounts', [])[:2]) or 'Not found'}")
                    if ent.get("dates"):
                        st.write(f"Dates: {', '.join(ent['dates'][:2])}")
                    st.info(f"Summary: {r.get('summary', '')}")
                    scores_df = pd.DataFrame(list(r["all_scores"].items()),
                                            columns=["Type", "Score%"]).sort_values("Score%")
                    fig = px.bar(scores_df, x="Score%", y="Type", orientation="h",
                                color="Score%", color_continuous_scale=["#F5D6D1", "#C0392B"],
                                title="Confidence by Document Type")
                    fig.update_layout(height=280, margin=dict(l=0, r=10, t=30, b=0),
                                    font=dict(family="Inter"))
                    st.plotly_chart(fig, use_container_width=True)
                except FileNotFoundError:
                    st.error("Document model not trained yet.")
                except Exception as e:
                    st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

# PAGE: VIEW CASES
elif page == "View Cases":
    top_bar("RECORDS", "VIEW CASES")
    cases = get_cases_for_user()

    sel_id = st.session_state.get("selected_case_id")

    if sel_id and cases:
        case = case_store.get_case(sel_id)
        if case:
            if st.button("Back to Case List"):
                st.session_state["selected_case_id"] = None
                st.rerun()

            st.write("")
            st.markdown(f'<div class="page-eyebrow">CASE FILE</div>'
                        f'<div class="page-title">{case.get("taxpayer_name", "Case Details")}</div>',
                        unsafe_allow_html=True)
            st.markdown(f'<div class="page-subtitle">'
                        f'Case ID: {case.get("case_id")} &nbsp;·&nbsp; '
                        f'PIN: {case.get("pin", "-")} &nbsp;·&nbsp; '
                        f'Plaintiff: {case.get("plaintiff", "-")} &nbsp;·&nbsp; '
                        f'Defendant: {case.get("defendant", "-")} &nbsp;·&nbsp; '
                        f'Assigned to: {case.get("assigned_to", "Unassigned")}</div>',
                        unsafe_allow_html=True)
            st.write("")

            wp = case.get("win_probability", 0)
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                stat_card("DISPUTED AMOUNT",
                          f"KES {case.get('disputed_amount', 0):,.0f}",
                          case.get("case_type", "-"))
            with c2:
                stat_card("KRA WIN PROBABILITY", f"{wp:.0f}%",
                          case.get("prediction", "-"),
                          "red" if wp < 50 else ("orange" if wp < 70 else "green"))
            with c3:
                stat_card("CASE DURATION",
                          f"{case.get('case_duration_days', '-')} days",
                          case.get("court_level", "-"))
            with c4:
                stat_card("STATUS",
                          case.get("status", "Open"),
                          case.get("legal_grounds", "-"))

            st.write("")
            col_l, col_r = st.columns([2, 1])

            with col_l:
                st.markdown('<div class="panel-card"><div class="panel-title">'
                            'Case Profile</div>', unsafe_allow_html=True)
                for k, v in {
                    "Plaintiff":              case.get("plaintiff", "-"),
                    "Defendant":              case.get("defendant", "-"),
                    "Taxpayer Category":      case.get("taxpayer_category", "-"),
                    "Representation":         case.get("representation", "-"),
                    "Legal Grounds":          case.get("legal_grounds", "-"),
                    "Court Level":            case.get("court_level", "-"),
                    "Prior Compliance Score": case.get("prior_compliance_score", "-"),
                    "Prior Disputes":         case.get("num_prior_disputes", "-"),
                    "Taxpayer Risk Score":    case.get("taxpayer_risk_score", "-"),
                    "Assigned To":            case.get("assigned_to", "Unassigned"),
                    "Created By":             case.get("created_by", "-"),
                }.items():
                    st.markdown(
                        f"<div style='display:flex;justify-content:space-between;"
                        f"padding:6px 0;border-bottom:1px solid #F0EEE9;'>"
                        f"<span style='color:#9A9A93;font-size:0.85rem;'>{k}</span>"
                        f"<span style='font-weight:700;color:#0A0A0A;font-size:0.85rem;'>"
                        f"{v}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                st.markdown('<div class="panel-card"><div class="panel-title">'
                            'Update Case Status</div>', unsafe_allow_html=True)
                new_status = st.selectbox("New Status", STATUSES,
                                          index=STATUSES.index(case.get("status", "Open")))
                if st.button("Save Status", use_container_width=True):
                    try:
                        result = case_store.update_case(case["case_id"], {"status": new_status})
                        if result:
                            st.success(f"Status successfully updated to {new_status}.")
                            st.balloons()
                            st.rerun()
                        else:
                            st.error("Could not update status. Case not found in the system.")
                    except Exception as e:
                        st.error(f"Something went wrong while saving: {e}")
                st.markdown("</div>", unsafe_allow_html=True)

            with col_r:
                st.markdown('<div class="panel-card"><div class="panel-title">'
                            'Outcome Forecast</div>', unsafe_allow_html=True)
                fig = go.Figure(go.Indicator(
                    mode="gauge+number", value=wp,
                    title={"text": "KRA Win Probability"},
                    gauge={"axis": {"range": [0, 100]},
                           "bar": {"color": "#1E8449" if wp >= 50 else "#C0392B"},
                           "steps": [{"range": [0,  50], "color": "#FCEBE9"},
                                     {"range": [50, 70], "color": "#FDF3DC"},
                                     {"range": [70,100], "color": "#EAF6EF"}]}))
                fig.update_layout(height=260, margin=dict(t=40, b=10, l=10, r=10),
                                  font=dict(family="Inter"))
                st.plotly_chart(fig, use_container_width=True)
                st.markdown(risk_badge(case.get("risk_level", "Low")),
                            unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

                if is_admin:
                    st.write("")
                    if st.button("Delete This Case", use_container_width=True):
                        case_store.delete_case(case["case_id"])
                        st.session_state["selected_case_id"] = None
                        st.success("Case deleted.")
                        st.rerun()

            st.stop()

    # ── Case list ──────────────────────────────────────────────────────────
    page_header("CASE RECORDS", "View", "Cases", "Cases visible to your account.")
    st.write("")

    if not cases:
        st.info("No cases assigned to you yet. Ask an Admin to assign cases to your account.")
    else:
        df = pd.DataFrame(cases)
        f1, f2, f3 = st.columns(3)
        with f1:
            sf = st.multiselect("Status", STATUSES, default=STATUSES)
        with f2:
            rf = st.multiselect("Risk", ["High","Medium","Low"],
                                default=["High","Medium","Low"])
        with f3:
            tf = st.multiselect("Case Type",
                                sorted(df["case_type"].dropna().unique().tolist()),
                                default=sorted(df["case_type"].dropna().unique().tolist()))

        filtered = df[
            df["status"].isin(sf) &
            df["risk_level"].isin(rf) &
            df["case_type"].isin(tf)
        ]

        st.markdown(f'<div class="panel-card"><div class="panel-title">'
                    f'{len(filtered)} Case(s) — Click Open to view details</div>',
                    unsafe_allow_html=True)
        h1, h2, h3, h4, h5 = st.columns([3, 2, 2, 2, 1])
        h1.markdown("**Taxpayer**")
        h2.markdown("**Type / Amount**")
        h3.markdown("**Status**")
        h4.markdown("**Risk**")
        h5.markdown("")
        st.markdown("<hr style='margin:4px 0 8px 0;border-color:#E3E1DC;'>",
                    unsafe_allow_html=True)

        for _, row in filtered.iterrows():
            c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 1])
            c1.markdown(f"**{row.get('taxpayer_name', '-')}**  \n"
                        f"`{row.get('case_id', '-')}`")
            c2.markdown(f"{row.get('case_type', '-')}  \n"
                        f"KES {row.get('disputed_amount', 0):,.0f}")
            c3.markdown(status_badge(row.get('status', 'Open')), unsafe_allow_html=True)
            c4.markdown(risk_badge(row.get('risk_level', 'Low')), unsafe_allow_html=True)
            if c5.button("Open", key=f"open_{row.get('case_id')}"):
                st.session_state["selected_case_id"] = row.get("case_id")
                st.rerun()
            st.markdown("<hr style='margin:6px 0;border-color:#F0EEE9;'>",
                        unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# PAGE: ADMIN PANEL
elif page == "Admin Panel":
    top_bar("SYSTEM", "ADMIN PANEL")
    page_header("SYSTEM — USERS", "Admin", "Panel",
                "Manage user accounts and system access.")
    st.write("")

    st.markdown('<div class="panel-card"><div class="panel-title">Registered Users</div>',
                unsafe_allow_html=True)
    users = get_all_users()
    if users:
        h1, h2, h3, h4 = st.columns([3, 3, 2, 2])
        h1.markdown("**Full Name**")
        h2.markdown("**Username**")
        h3.markdown("**Role**")
        h4.markdown("**Action**")
        st.markdown("<hr style='margin:4px 0 8px 0;border-color:#E3E1DC;'>",
                    unsafe_allow_html=True)
        for u in users:
            c1, c2, c3, c4 = st.columns([3, 3, 2, 2])
            c1.write(u.get("full_name", "-"))
            c2.write(u["username"])
            c3.write(u["role"])
            if u["username"] != username:
                if c4.button("Remove", key=f"del_{u['username']}"):
                    delete_user(u["username"])
                    st.success(f"User {u['username']} removed.")
                    st.rerun()
            else:
                c4.write("(you)")
    st.markdown("</div>", unsafe_allow_html=True)