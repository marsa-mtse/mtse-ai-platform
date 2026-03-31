import streamlit as st
# ==========================================================
# MTSE Marketing Engine v12 - Configuration
# ==========================================================

# ==============================
# PLAN LIMITS & PRICING
# ==============================

PLAN_LIMITS = {
    "Explorer": {"reports": 3,    "uploads": 3},      # FREE
    "Starter":  {"reports": 30,   "uploads": 30},     # $19
    "Strategist":{"reports": 200,  "uploads": 200},   # $69
    "Command":  {"reports": 9999, "uploads": 9999},   # $199
}

PLAN_PRICING = {
    "Explorer":  0,
    "Starter":   19,
    "Strategist": 69,
    "Command":   199
}

PLAN_BADGES = {
    "Explorer":  ("🆓", "Free",       "#10b981"),
    "Starter":   ("⚡", "Starter",    "#f59e0b"),
    "Strategist":("🚀", "Strategist", "#8b5cf6"),
    "Command":   ("👑", "Command",    "#ef4444"),
}

AVAILABLE_ROLES = ["Analyst", "Viewer", "Marketing Manager"]

# ==============================
# ADMIN DEFAULTS
# ==============================

ADMIN_DEFAULT_USERNAME = "admin"
ADMIN_DEFAULT_PASSWORD = "admin@2026"

# ==============================
# LOGIN SECURITY
# ==============================

MAX_LOGIN_ATTEMPTS = 5
LOGIN_LOCKOUT_MINUTES = 15

# ==============================
# APP METADATA
# ==============================

APP_VERSION = "12.0.0"
APP_NAME_AR = "منصة MTSE v12 — السيادة الرقمية"
APP_NAME_EN = "MTSE v12 — Digital Sovereignty Hub"

# --- DUAL-CORE THEME ENGINE ---
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Quantum Dark"

IS_DARK = st.session_state.theme_mode == "Quantum Dark"

# Dynamic Colors
PRIMARY       = "#8b5cf6"
PRIMARY_LIGHT = "#c4b5fd"
PRIMARY_DARK  = "#6d28d9"
ACCENT        = "#06b6d4"
SUCCESS       = "#10b981"
WARNING       = "#fbbf24"
DANGER        = "#f43f5e"

BG_MAIN   = "#030712"    if IS_DARK else "#f8fafc"
BG_CARD   = "rgba(17,24,39,0.75)"  if IS_DARK else "rgba(255,255,255,0.85)"
TEXT_MAIN = "#f8fafc"    if IS_DARK else "#0f172a"
TEXT_SEC  = "#9ca3af"    if IS_DARK else "#475569"
BORDER_GLOW = "rgba(139,92,246,0.3)" if IS_DARK else "rgba(139,92,246,0.15)"

# ==============================
# WORLD-CLASS CSS THEME v12
# ==============================

PREMIUM_CSS = f"""
<style>
    /* ─── FONTS ─────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Tajawal:wght@300;400;500;700;800&display=swap');

    /* ─── ROOT VARIABLES ─────────────────────────── */
    :root {{
        --primary:       {PRIMARY};
        --primary-light: {PRIMARY_LIGHT};
        --primary-dark:  {PRIMARY_DARK};
        --accent:        {ACCENT};
        --success:       {SUCCESS};
        --warning:       {WARNING};
        --danger:        {DANGER};
        --bg-main:       {BG_MAIN};
        --bg-card:       {BG_CARD};
        --text-primary:  {TEXT_MAIN};
        --text-secondary:{TEXT_SEC};
        --glass-border:  rgba(255,255,255,0.08);
        --neon-glow:     0 0 20px {PRIMARY}55;
        --haptic-shadow: 0 8px 32px rgba(0,0,0,0.35);
        --border:        rgba(255,255,255,0.06);
        --radius-lg:     20px;
        --radius-xl:     28px;
        --transition:    0.3s cubic-bezier(0.4,0,0.2,1);
    }}

    /* ─── GLOBAL RESET ────────────────────────────── */
    * {{ box-sizing: border-box; }}

    body, .stApp {{
        font-family: 'Tajawal','Inter',sans-serif;
        background: {BG_MAIN};
        background-image: {
            "radial-gradient(ellipse at 0% 0%, #1e1b4b 0%, transparent 55%), radial-gradient(ellipse at 100% 100%, #111827 0%, #030712 100%)" if IS_DARK else
            "radial-gradient(ellipse at 0% 0%, #ede9fe 0%, transparent 55%), radial-gradient(ellipse at 100% 100%, #f1f5f9 0%, #f8fafc 100%)"
        };
        background-attachment: fixed;
        color: {TEXT_MAIN};
    }}

    /* ─── HIDE STREAMLIT CHROME ───────────────────── */
    header[data-testid="stHeader"]  {{ visibility: hidden !important; height: 0 !important; }}
    footer                          {{ display: none !important; }}
    #MainMenu                       {{ display: none !important; }}
    .block-container                {{ padding-top: 1.25rem !important; max-width: 1400px; }}

    /* ─── GLASS CARD ──────────────────────────────── */
    .glass-card {{
        background: var(--bg-card);
        backdrop-filter: blur(24px) saturate(180%);
        -webkit-backdrop-filter: blur(24px) saturate(180%);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 28px 32px;
        box-shadow: var(--haptic-shadow);
        transition: transform var(--transition), box-shadow var(--transition), border-color var(--transition);
    }}
    .glass-card:hover {{
        transform: translateY(-6px) scale(1.005);
        border-color: var(--primary);
        box-shadow: 0 24px 48px -10px rgba(0,0,0,0.5), var(--neon-glow);
    }}

    /* ─── KPI CARDS ───────────────────────────────── */
    .kpi-card {{
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 22px 18px;
        text-align: center;
        transition: transform var(--transition);
    }}
    .kpi-card:hover {{
        transform: translateY(-4px);
        border-color: var(--primary);
    }}
    .kpi-value {{
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0 4px;
        line-height: 1;
    }}
    .kpi-label {{
        color: var(--text-secondary);
        font-size: 0.82rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 600;
    }}
    .kpi-icon {{
        font-size: 1.8rem;
        margin-bottom: 4px;
    }}

    /* ─── MAIN BUTTONS ────────────────────────────── */
    .stButton > button {{
        border-radius: 14px !important;
        background: linear-gradient(135deg, {PRIMARY} 0%, {PRIMARY_DARK} 100%) !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        color: white !important;
        font-weight: 700 !important;
        font-family: 'Tajawal','Inter',sans-serif !important;
        padding: 13px 26px !important;
        letter-spacing: 0.5px;
        transition: all var(--transition) !important;
        box-shadow: 0 4px 16px rgba(109,40,217,0.3) !important;
    }}
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 28px rgba(109,40,217,0.5), var(--neon-glow) !important;
        filter: brightness(1.08);
    }}
    .stButton > button:active {{
        transform: scale(0.97) !important;
    }}

    /* ─── SIDEBAR ─────────────────────────────────── */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0a0f1e 0%, #0f172a 60%, #1e293b 100%) !important;
        border-right: 1px solid var(--border) !important;
    }}
    section[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        border: none !important;
        color: {TEXT_SEC} !important;
        border-radius: 12px !important;
        padding: 11px 16px !important;
        text-align: right !important;
        font-weight: 500 !important;
        box-shadow: none !important;
        letter-spacing: 0;
        text-transform: none;
        width: 100%;
    }}
    section[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, rgba(139,92,246,0.25), rgba(109,40,217,0.15)) !important;
        border: 1px solid rgba(139,92,246,0.4) !important;
        color: {PRIMARY_LIGHT} !important;
    }}
    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(139,92,246,0.12) !important;
        color: {PRIMARY_LIGHT} !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    /* ─── STATUS BADGES ────────────────────────────── */
    .status-badge {{
        display: inline-block;
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }}
    .badge-active  {{ background: rgba(16,185,129,0.15); color: {SUCCESS}; border: 1px solid rgba(16,185,129,0.3); }}
    .badge-warning {{ background: rgba(251,191,36,0.15);  color: {WARNING}; border: 1px solid rgba(251,191,36,0.3); }}
    .badge-danger  {{ background: rgba(244,63,94,0.15);   color: {DANGER};  border: 1px solid rgba(244,63,94,0.3); }}
    .badge-free    {{ background: rgba(16,185,129,0.15); color: {SUCCESS}; border: 1px solid rgba(16,185,129,0.4); }}

    /* ─── SECTION HEADER ──────────────────────────── */
    .section-header {{
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text-primary);
        border-bottom: 2px solid var(--primary);
        padding-bottom: 8px;
        margin: 28px 0 18px;
        letter-spacing: 0.3px;
    }}

    /* ─── USAGE BAR ────────────────────────────────── */
    .usage-bar {{
        background: rgba(255,255,255,0.06);
        border-radius: 10px;
        overflow: hidden;
        height: 9px;
        margin: 8px 0;
    }}
    .usage-bar-fill {{
        height: 100%;
        border-radius: 10px;
        transition: width 0.7s cubic-bezier(0.4,0,0.2,1);
    }}

    /* ─── INPUTS ──────────────────────────────────── */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {{
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 12px !important;
        color: {TEXT_MAIN} !important;
        font-family: 'Tajawal','Inter',sans-serif !important;
        transition: border-color var(--transition) !important;
    }}
    .stTextInput input:focus, .stTextArea textarea:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px rgba(139,92,246,0.18) !important;
    }}

    /* ─── TABS ─────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {{
        background: rgba(255,255,255,0.03);
        border-radius: 14px;
        padding: 6px;
        gap: 4px;
        border: 1px solid var(--border);
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px !important;
        padding: 8px 18px !important;
        color: var(--text-secondary) !important;
        font-weight: 600 !important;
        font-family: 'Tajawal','Inter',sans-serif !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, {PRIMARY}, {PRIMARY_DARK}) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(109,40,217,0.35) !important;
    }}

    /* ─── DOWNLOAD BUTTON ──────────────────────────── */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {SUCCESS}, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
    }}

    /* ─── DATAFRAMES / TABLES ──────────────────────── */
    .stDataFrame {{ border-radius: 14px !important; overflow: hidden; }}

    /* ─── METRICS ──────────────────────────────────── */
    [data-testid="metric-container"] {{
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 18px 20px;
        backdrop-filter: blur(12px);
    }}
    [data-testid="metric-container"] [data-testid="stMetricValue"] {{
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }}

    /* ─── ANIMATIONS ──────────────────────────────── */
    @keyframes fadeInUp {{
        from {{ opacity:0; transform:translateY(22px); }}
        to   {{ opacity:1; transform:translateY(0);     }}
    }}
    .animate-in {{ animation: fadeInUp 0.45s ease-out; }}

    @keyframes pulse {{
        0%,100% {{ opacity:1; }}
        50%      {{ opacity:0.65; }}
    }}
    .pulse {{ animation: pulse 2.2s ease-in-out infinite; }}

    @keyframes shimmer {{
        0%   {{ background-position: -1000px 0; }}
        100% {{ background-position:  1000px 0; }}
    }}
    .shimmer {{
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.06), transparent);
        background-size: 1000px 100%;
        animation: shimmer 2s infinite;
    }}

    /* ─── HERO / LANDING ──────────────────────────── */
    .hero-container {{
        border-radius: 32px;
        padding: 80px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
        margin-bottom: 40px;
    }}

    /* ─── PRICING CARDS ─────────────────────────────── */
    .pricing-card {{
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-xl);
        padding: 32px 28px;
        text-align: center;
        transition: transform var(--transition), box-shadow var(--transition);
        position: relative;
        overflow: hidden;
    }}
    .pricing-card.featured {{
        border-color: {PRIMARY};
        box-shadow: 0 0 0 2px {PRIMARY}44, var(--neon-glow);
    }}
    .pricing-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 24px 48px rgba(0,0,0,0.4);
    }}
    .pricing-price {{
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1;
    }}

    /* ─── PLAN BADGE COLORS ────────────────────────── */
    .plan-explorer   {{ color: {SUCCESS}; }}
    .plan-starter    {{ color: {WARNING}; }}
    .plan-strategist {{ color: {PRIMARY}; }}
    .plan-command    {{ color: {DANGER};  }}

    /* ─── NOTIFICATION / ALERT ─────────────────────── */
    .stAlert {{ border-radius: 14px !important; }}
    .stInfo   {{ border-left: 4px solid {ACCENT} !important; }}
    .stSuccess{{ border-left: 4px solid {SUCCESS} !important; }}
    .stWarning{{ border-left: 4px solid {WARNING} !important; }}
    .stError  {{ border-left: 4px solid {DANGER}  !important; }}

    /* ─── EXPANDER ──────────────────────────────────── */
    .streamlit-expanderHeader {{
        background: rgba(255,255,255,0.03) !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-family: 'Tajawal','Inter',sans-serif !important;
    }}

    /* ─── SCROLLBAR ──────────────────────────────────── */
    ::-webkit-scrollbar       {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: rgba(255,255,255,0.02); }}
    ::-webkit-scrollbar-thumb {{ background: {PRIMARY}66; border-radius: 6px; }}
    ::-webkit-scrollbar-thumb:hover {{ background: {PRIMARY}aa; }}
</style>
"""
