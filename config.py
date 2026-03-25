import streamlit as st
# ==========================================================
# MTSE Marketing Engine - Configuration
# ==========================================================

# ==============================
# PLAN LIMITS & PRICING
# ==============================

PLAN_LIMITS = {
    "Explorer": {"reports": 10, "uploads": 10},
    "Strategist": {"reports": 100, "uploads": 100},
    "Command": {"reports": 9999, "uploads": 9999}
}

PLAN_PRICING = {
    "Explorer": 19,
    "Strategist": 69,
    "Command": 199
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
APP_NAME_AR = "منصة MTSE v12 - السيادة الرقمية "
APP_NAME_EN = "MTSE v12 - Digital Sovereignty Hub"

# --- v11 DUAL-CORE AESTHETICS ---
if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Quantum Dark"

IS_DARK = st.session_state.theme_mode == "Quantum Dark"

# Dynamic Colors
PRIMARY = "#8b5cf6"
ACCENT = "#06b6d4"
BG_MAIN = "#030712" if IS_DARK else "#f8fafc"
TEXT_MAIN = "#f8fafc" if IS_DARK else "#0f172a"
CARD_BG = "rgba(17, 24, 39, 0.7)" if IS_DARK else "rgba(255, 255, 255, 0.8)"
BORDER_GLOW = "rgba(139, 92, 246, 0.3)" if IS_DARK else "rgba(139, 92, 246, 0.2)"

# ==============================
# PREMIUM CSS THEME
# ==============================

PREMIUM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Quantum Glass UI v12.0 */
    :root {{
        --primary: {PRIMARY};
        --primary-light: #c4b5fd;
        --primary-dark: #6d28d9;
        --accent: {ACCENT};
        --success: #10b981;
        --warning: #fbbf24;
        --danger: #f43f5e;
        --bg-main: {BG_MAIN};
        --bg-card: {CARD_BG};
        --text-primary: {TEXT_MAIN};
        --text-secondary: {"#9ca3af" if IS_DARK else "#475569"};
        --glass-border: rgba(255, 255, 255, 0.1);
        --neon-glow: 0 0 15px {PRIMARY}44;
        --haptic-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.3);
    }}

    .stApp {{
        font-family: 'Inter', sans-serif;
        background: {BG_MAIN};
        background-image: {
            "radial-gradient(circle at 0% 0%, #1e1b4b 0%, transparent 50%), radial-gradient(circle at 100% 100%, #111827 0%, #030712 100%)" if IS_DARK else
            "radial-gradient(circle at 0% 0%, #e2e8f0 0%, transparent 50%), radial-gradient(circle at 100% 100%, #f1f5f9 0%, #f8fafc 100%)"
        };
        background-attachment: fixed;
    }}

    .glass-card {{
        background: var(--bg-card);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 30px;
        box-shadow: var(--haptic-shadow);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }}

    .glass-card:hover {{
        transform: translateY(-8px) scale(1.01);
        border-color: var(--primary);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), var(--neon-glow);
    }}

    /* Global Professional Buttons */
    .stButton > button {{
        width: 100%;
        border-radius: 16px !important;
        background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        font-weight: 700 !important;
        padding: 14px 28px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3) !important;
    }}

    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(109, 40, 217, 0.5), var(--neon-glow) !important;
        filter: brightness(1.1);
    }}

    .stButton > button:active {{
        transform: scale(0.96) !important;
    }}

    /* Secondary/Sidebar Buttons */
    div[data-testid="stSidebar"] .stButton > button {{
        background: rgba(255,255,255,0.03) !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        text-transform: none;
        letter-spacing: 0;
        text-align: right !important;
        box-shadow: none !important;
    }}

    div[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(139, 92, 246, 0.15) !important;
        border-color: var(--primary) !important;
        color: var(--primary-light) !important;
    }}

    /* Landing Page Hero */
    .hero-container {{
        background: url('https://raw.githubusercontent.com/marsa-mtse/engidraft-assets/main/v12_hero.jpg') center/cover;
        padding: 80px 40px;
        border-radius: 32px;
        text-align: center;
        margin-bottom: 40px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }}

    .hero-overlay {{
        position: absolute;
        top:0; left:0; width:100%; height:100%;
        background: linear-gradient(180deg, rgba(3, 7, 18, 0.2) 0%, rgba(3, 7, 18, 0.8) 100%);
    }}

    .hero-content {{
        position: relative;
        z-index: 10;
    }}

    /* KPI Metric Cards */
    .kpi-card {{
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }}

    .kpi-value {{
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #818cf8, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }}

    .kpi-label {{
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid var(--border);
    }}

    section[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        text-align: right !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(99, 102, 241, 0.1) !important;
        color: var(--primary-light) !important;
    }}

    /* Status Badges */
    .status-badge {{
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    .badge-active {{
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }}

    .badge-warning {{
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }}

    .badge-danger {{
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}

    /* Tables */
    .stDataFrame {{
        border-radius: 12px !important;
        overflow: hidden;
    }}

    /* Progress Bars */
    .usage-bar {{
        background: var(--bg-card);
        border-radius: 10px;
        overflow: hidden;
        height: 10px;
        margin: 8px 0;
    }}

    .usage-bar-fill {{
        height: 100%;
        border-radius: 10px;
        transition: width 0.6s ease;
    }}

    /* Animations */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .animate-in {{
        animation: fadeInUp 0.5s ease-out;
    }}

    @keyframes pulse {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.7; }}
    }}

    .pulse {{
        animation: pulse 2s infinite;
    }}

    /* Buttons (Global Override) */
    .stButton > button {{
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.3px;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }}

    /* Download Buttons */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, var(--success), #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
    }}

    /* Section Dividers */
    .section-header {{
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        border-bottom: 2px solid var(--primary);
        padding-bottom: 8px;
        margin: 24px 0 16px;
    }}
</style>
"""
