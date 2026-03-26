import streamlit as st
# ==========================================================
# MTSE Marketing Engine v13 - Configuration & Premium Theme
# ==========================================================

# ==============================
# PLAN LIMITS & PRICING
# ==============================

PLAN_LIMITS = {
    "Starter": {"reports": 5,    "uploads": 5,    "ai_calls": 20},    # Free
    "Pro":     {"reports": 200,  "uploads": 200,  "ai_calls": 2000},  # Paid
    "Command": {"reports": 9999, "uploads": 9999, "ai_calls": 99999}  # Paid Enterprise
}

PLAN_PRICING = {
    "Starter": 0,     # مجاني
    "Pro":     299,   # EGP / month
    "Command": 799    # EGP / month
}

PLAN_FEATURES = {
    "Starter": [
        "AI Campaign Builder (5 campaigns/month)",
        "Analytics Dashboard",
        "1 Social Profile",
        "Community Support"
    ],
    "Pro": [
        "كل مميزات Starter",
        "AI Image Studio (DALL-E 3)",
        "Competitor Intel",
        "Video Script Engine",
        "Email Campaigns",
        "5 Social Profiles",
        "Priority Support"
    ],
    "Command": [
        "كل مميزات Pro",
        "Trend Forecaster (AI 90-day)",
        "Strategy Deep Dive",
        "Unlimited Social Profiles",
        "White-label PDF Reports",
        "API Access",
        "Dedicated Account Manager"
    ]
}

AVAILABLE_ROLES = ["Analyst", "Viewer", "Marketing Manager", "Creative Director"]


# ==============================
# AI MODELS CONFIGURATION
# ==============================

FALLBACK_API_KEYS = {
    "google": "",
    "groq": "",
    "openai": "",
    "anthropic": ""
}

AI_MODELS = {
    "GPT-4o": {"provider": "openai", "model_id": "gpt-4o", "icon": "🧠", "speed": "Fast", "context": "128K"},
    "GPT-4o Mini": {"provider": "openai", "model_id": "gpt-4o-mini", "icon": "⚡", "speed": "Ultra Fast", "context": "128K"},
    "Gemini 1.5 Pro": {"provider": "google", "model_id": "gemini-1.5-pro", "icon": "✨", "speed": "Fast", "context": "1M"},
    "Gemini 1.5 Flash": {"provider": "google", "model_id": "gemini-1.5-flash", "icon": "💫", "speed": "Ultra Fast", "context": "1M"},
    "Llama 3.3 70B": {"provider": "groq", "model_id": "llama-3.3-70b-versatile", "icon": "🦙", "speed": "Fastest", "context": "128K"},
    "Mixtral 8x7B": {"provider": "groq", "model_id": "mixtral-8x7b-32768", "icon": "🌀", "speed": "Fast", "context": "32K"},
}

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

APP_VERSION = "13.5.0"
APP_NAME_AR = "منصة MTSE v13 - السيادة الرقمية"
APP_NAME_EN = "MTSE v13 - Digital Sovereignty Hub"

# ==============================
# THEME ENGINE
# ==============================

if "theme_mode" not in st.session_state:
    st.session_state.theme_mode = "Quantum Dark"

IS_DARK = st.session_state.theme_mode == "Quantum Dark"

# Color Palette - v13 Nebula
PRIMARY = "#7c3aed"
PRIMARY_LIGHT = "#a78bfa"
ACCENT = "#38bdf8"
NEON_PINK = "#f0abfc"
NEON_GREEN = "#34d399"
BG_MAIN = "#05061a" if IS_DARK else "#f0f4ff"
TEXT_MAIN = "#f1f5f9" if IS_DARK else "#0f172a"
CARD_BG = "rgba(15, 20, 50, 0.75)" if IS_DARK else "rgba(255, 255, 255, 0.85)"
BORDER_GLOW = "rgba(124, 58, 237, 0.35)" if IS_DARK else "rgba(124, 58, 237, 0.2)"

# ==============================
# PREMIUM CSS THEME v13 NEBULA
# ==============================

PREMIUM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@400;500;600;700&display=swap');

    /* ─── v13 Nebula Design System ─── */
    :root {{
        --primary: {PRIMARY};
        --primary-light: {PRIMARY_LIGHT};
        --primary-dark: #5b21b6;
        --accent: {ACCENT};
        --neon-pink: {NEON_PINK};
        --neon-green: {NEON_GREEN};
        --success: #10b981;
        --warning: #fbbf24;
        --danger: #f43f5e;
        --bg-main: {BG_MAIN};
        --bg-card: {CARD_BG};
        --text-primary: {TEXT_MAIN};
        --text-secondary: {"#94a3b8" if IS_DARK else "#475569"};
        --glass-border: {"rgba(255, 255, 255, 0.08)" if IS_DARK else "rgba(0, 0, 0, 0.06)"};
        --neon-glow: 0 0 20px {PRIMARY}55, 0 0 40px {PRIMARY}22;
        --card-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
        --border-subtle: {"rgba(255, 255, 255, 0.06)" if IS_DARK else "rgba(0,0,0,0.08)"};
    }}

    /* ─── Base App ─── */
    .stApp {{
        font-family: 'Inter', 'Space Grotesk', sans-serif;
        background: {BG_MAIN};
        background-image: {"radial-gradient(ellipse at 10% 10%, rgba(124,58,237,0.15) 0%, transparent 55%), radial-gradient(ellipse at 90% 90%, rgba(56,189,248,0.08) 0%, transparent 55%), radial-gradient(ellipse at 50% 50%, rgba(240,171,252,0.04) 0%, transparent 70%)" if IS_DARK else "radial-gradient(ellipse at 10% 10%, rgba(124,58,237,0.06) 0%, transparent 55%), radial-gradient(ellipse at 90% 90%, rgba(56,189,248,0.04) 0%, transparent 55%)"};
        background-attachment: fixed;
        min-height: 100vh;
    }}

    /* ─── Hide Default Streamlit Elements ─── */
    #MainMenu, footer, header, .stDeployButton {{ display: none !important; }}
    .block-container {{ padding: 1.5rem 2rem !important; max-width: 1400px; }}
    
    /* ─── Glass Cards ─── */
    .glass-card {{
        background: var(--bg-card);
        backdrop-filter: blur(24px) saturate(200%);
        -webkit-backdrop-filter: blur(24px) saturate(200%);
        border: 1px solid var(--glass-border);
        border-radius: 28px;
        padding: 32px;
        box-shadow: var(--card-shadow);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }}

    .glass-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, var(--primary-light), transparent);
        opacity: 0.5;
    }}

    .glass-card:hover {{
        transform: translateY(-6px);
        border-color: rgba(124, 58, 237, 0.4);
        box-shadow: 0 30px 60px -12px rgba(0,0,0,0.7), var(--neon-glow);
    }}

    /* ─── Premium Sidebar Navigation v13 ─── */
    [data-testid="stSidebar"] .stButton > button {{
        background: rgba(124, 58, 237, 0.03) !important;
        border: 1px solid rgba(124, 58, 237, 0.1) !important;
        border-radius: 12px !important;
        color: var(--text-secondary) !important;
        justify-content: flex-start !important;
        text-align: right !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: none !important;
        margin-bottom: 2px !important;
        width: 100% !important;
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(124, 58, 237, 0.15) !important;
        border-color: rgba(124, 58, 237, 0.4) !important;
        color: var(--text-primary) !important;
        transform: translateX(-6px) !important; /* Translate left for RTL Arabic */
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.1) !important;
    }}

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: linear-gradient(270deg, rgba(124, 58, 237, 0.25), rgba(124, 58, 237, 0.02)) !important;
        border-right: 3px solid var(--accent) !important; /* Right border for RTL */
        border-left: 1px solid rgba(124, 58, 237, 0.1) !important;
        border-radius: 12px 4px 4px 12px !important;
        color: var(--text-primary) !important;
        text-shadow: 0 0 8px rgba(255, 255, 255, 0.4) !important;
    }}

    /* ─── Premium Sidebar Expanders (Collapsible Menus) v13 ─── */
    [data-testid="stSidebar"] [data-testid="stExpander"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 4px !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary {{
        background: rgba(124, 58, 237, 0.05) !important;
        border: 1px solid rgba(124, 58, 237, 0.15) !important;
        border-radius: 12px !important;
        color: #cbd5e1 !important;
        font-weight: 700 !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stExpander"] summary:hover {{
        background: rgba(124, 58, 237, 0.15) !important;
        border-color: rgba(124, 58, 237, 0.4) !important;
        color: var(--text-primary) !important;
    }}
    
    [data-testid="stSidebar"] [data-testid="stExpanderDetails"] {{
        border: none !important;
        padding: 8px 12px 0 12px !important;
        background: transparent !important;
    }}

    /* ─── Feature Cards ─── */
    .feature-card {{
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        transition: all 0.35s ease;
        text-align: center;
        cursor: pointer;
    }}

    .feature-card:hover {{
        transform: translateY(-4px);
        border-color: var(--primary);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4), 0 0 20px {PRIMARY}33;
    }}

    .feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 12px;
        display: block;
        filter: drop-shadow(0 0 8px {PRIMARY}66);
    }}

    .feature-title {{
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 8px;
    }}

    .feature-desc {{
        font-size: 0.85rem;
        color: var(--text-secondary);
        line-height: 1.5;
    }}

    /* ─── Hero Section ─── */
    .hero-v13 {{
        background: linear-gradient(135deg, #0d0628 0%, #130a3e 40%, #0a1628 100%);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 32px;
        padding: 80px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 40px;
    }}

    .hero-v13::before {{
        content: '';
        position: absolute;
        top: -50%; left: -50%;
        width: 200%; height: 200%;
        background: radial-gradient(circle at center, rgba(124,58,237,0.12) 0%, transparent 60%);
        animation: rotateBg 20s linear infinite;
    }}

    .hero-v13::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0;
        right: 0; height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), var(--accent), var(--neon-pink), transparent);
    }}

    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: clamp(2.5rem, 6vw, 4.5rem);
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #ffffff 0%, {PRIMARY_LIGHT} 40%, {ACCENT} 80%, {NEON_PINK} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 2;
    }}

    .hero-subtitle {{
        font-size: 1.15rem;
        color: #94a3b8;
        max-width: 620px;
        margin: 0 auto 36px;
        line-height: 1.7;
        position: relative;
        z-index: 2;
    }}

    .hero-badge {{
        display: inline-block;
        padding: 6px 18px;
        background: rgba(124, 58, 237, 0.2);
        border: 1px solid rgba(124, 58, 237, 0.4);
        border-radius: 50px;
        font-size: 0.8rem;
        font-weight: 600;
        color: {PRIMARY_LIGHT};
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 24px;
        position: relative;
        z-index: 2;
    }}

    .hero-cta {{
        display: inline-block;
        padding: 16px 40px;
        background: linear-gradient(135deg, {PRIMARY} 0%, #5b21b6 100%);
        color: white;
        font-weight: 700;
        font-size: 1rem;
        border-radius: 16px;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 8px 32px rgba(124, 58, 237, 0.4);
        letter-spacing: 0.5px;
        position: relative;
        z-index: 2;
        text-decoration: none;
    }}

    .hero-cta:hover {{
        transform: translateY(-3px);
        box-shadow: 0 16px 48px rgba(124, 58, 237, 0.6), var(--neon-glow);
    }}

    /* ─── Stats Counter ─── */
    .stats-row {{
        display: flex;
        justify-content: center;
        gap: 48px;
        margin-top: 40px;
        position: relative;
        z-index: 2;
        flex-wrap: wrap;
    }}

    .stat-item {{
        text-align: center;
    }}

    .stat-value {{
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .stat-label {{
        font-size: 0.8rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 4px;
    }}

    /* ─── Sidebar v13 ─── */
    section[data-testid="stSidebar"] {{
        background: {"linear-gradient(180deg, #07091f 0%, #0d1028 50%, #090d24 100%)" if IS_DARK else "linear-gradient(180deg, #f8f9ff 0%, #eef2ff 100%)"};
        border-right: 1px solid var(--border-subtle);
    }}

    .sidebar-logo {{
        text-align: center;
        padding: 20px 12px;
    }}

    .sidebar-logo-icon {{
        font-size: 2.8rem;
        display: block;
        filter: drop-shadow(0 0 12px {PRIMARY}88);
        margin-bottom: 8px;
    }}

    .sidebar-logo-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }}

    .sidebar-version {{
        font-size: 0.7rem;
        color: #64748b;
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }}

    .sidebar-user {{
        background: rgba(124, 58, 237, 0.08);
        border: 1px solid rgba(124, 58, 237, 0.15);
        border-radius: 14px;
        padding: 12px 16px;
        margin: 8px 0;
        text-align: center;
    }}

    .nav-section-label {{
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #64748b;
        padding: 12px 8px 4px;
    }}

    /* Sidebar Buttons Override */
    section[data-testid="stSidebar"] .stButton > button {{
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: 1px solid transparent !important;
        border-radius: 12px !important;
        padding: 10px 14px !important;
        text-align: right !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        margin-bottom: 2px;
    }}

    section[data-testid="stSidebar"] .stButton > button:hover {{
        background: rgba(124, 58, 237, 0.12) !important;
        border-color: rgba(124, 58, 237, 0.3) !important;
        color: {PRIMARY_LIGHT} !important;
        transform: translateX(-2px) !important;
    }}

    /* ─── Main Buttons ─── */
    .stButton > button {{
        border-radius: 14px !important;
        font-weight: 600 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.3px;
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, {PRIMARY} 0%, #5b21b6 100%) !important;
        border: none !important;
        color: white !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.35) !important;
    }}

    .stButton > button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 28px rgba(124, 58, 237, 0.55), var(--neon-glow) !important;
    }}

    /* ─── Login Card ─── */
    .login-card {{
        background: {"rgba(10, 15, 40, 0.9)" if IS_DARK else "rgba(255,255,255,0.95)"};
        backdrop-filter: blur(30px);
        border: 1px solid rgba(124, 58, 237, 0.2);
        border-radius: 28px;
        padding: 40px;
        box-shadow: 0 40px 80px rgba(0,0,0,0.5), var(--neon-glow);
        position: relative;
        overflow: hidden;
    }}

    .login-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 20%;
        right: 20%; height: 1px;
        background: linear-gradient(90deg, transparent, {PRIMARY}, transparent);
    }}

    /* ─── KPI Cards ─── */
    .kpi-card {{
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px 20px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}

    .kpi-card::after {{
        content: '';
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
        border-radius: 0 0 20px 20px;
    }}

    .kpi-value {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 8px 0;
    }}

    .kpi-label {{
        color: var(--text-secondary);
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }}

    .kpi-trend {{
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 6px;
    }}

    .trend-up {{ color: var(--neon-green); }}
    .trend-down {{ color: var(--danger); }}

    /* ─── Section Headers ─── */
    .section-header {{
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 28px 0 16px;
        display: flex;
        align-items: center;
        gap: 12px;
    }}

    .section-header::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, var(--primary), transparent);
        margin-right: auto;
    }}

    /* ─── Tool Header ─── */
    .tool-header {{
        background: linear-gradient(135deg, rgba(124,58,237,0.15) 0%, rgba(56,189,248,0.05) 100%);
        border: 1px solid rgba(124,58,237,0.2);
        border-radius: 24px;
        padding: 28px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }}

    .tool-header-icon {{
        font-size: 2.5rem;
        margin-bottom: 8px;
        filter: drop-shadow(0 0 10px {PRIMARY}88);
    }}

    .tool-header h1, .tool-header h2 {{
        background: linear-gradient(135deg, {TEXT_MAIN}, {PRIMARY_LIGHT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }}

    /* ─── Input Styling ─── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {{
        background: {"rgba(15, 23, 42, 0.6)" if IS_DARK else "rgba(248, 250, 252, 0.9)"} !important;
        border: 1px solid rgba(124, 58, 237, 0.2) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        transition: border-color 0.2s ease !important;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: {PRIMARY} !important;
        box-shadow: 0 0 0 3px {PRIMARY}22 !important;
    }}

    /* ─── Status Badges ─── */
    .badge {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 14px;
        border-radius: 30px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }}

    .badge-success {{
        background: rgba(52, 211, 153, 0.12);
        color: {NEON_GREEN};
        border: 1px solid rgba(52, 211, 153, 0.25);
    }}

    .badge-primary {{
        background: rgba(124, 58, 237, 0.12);
        color: {PRIMARY_LIGHT};
        border: 1px solid rgba(124, 58, 237, 0.25);
    }}

    .badge-warning {{
        background: rgba(251, 191, 36, 0.12);
        color: #fbbf24;
        border: 1px solid rgba(251, 191, 36, 0.25);
    }}

    .badge-danger {{
        background: rgba(244, 63, 94, 0.12);
        color: #f43f5e;
        border: 1px solid rgba(244, 63, 94, 0.25);
    }}

    /* ─── Tables ─── */
    .stDataFrame {{
        border-radius: 16px !important;
        overflow: hidden;
        border: 1px solid var(--glass-border) !important;
    }}

    /* ─── Tabs ─── */
    .stTabs [data-baseweb="tab-list"] {{
        background: {"rgba(15, 20, 50, 0.5)" if IS_DARK else "rgba(240, 244, 255, 0.8)"};
        border-radius: 14px;
        padding: 4px;
        border: 1px solid var(--glass-border);
    }}

    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        transition: all 0.2s ease !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: {PRIMARY} !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(124,58,237,0.35) !important;
    }}

    /* ─── Chat Input ─── */
    .stChatInput {{
        border-radius: 16px !important;
    }}

    /* ─── Divider ─── */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
        margin: 16px 0;
    }}

    /* ─── Pricing Cards ─── */
    .pricing-card {{
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 32px 24px;
        text-align: center;
        transition: all 0.35s ease;
        position: relative;
        overflow: hidden;
    }}

    .pricing-card.popular {{
        border-color: {PRIMARY};
        box-shadow: 0 20px 40px rgba(124,58,237,0.3), var(--neon-glow);
    }}

    .popular-badge {{
        position: absolute;
        top: 16px; right: -28px;
        background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
        color: white;
        padding: 4px 40px;
        font-size: 0.7rem;
        font-weight: 700;
        transform: rotate(35deg);
        letter-spacing: 1px;
    }}

    .price-amount {{
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    /* ─── AI Output Box ─── */
    .ai-output {{
        background: {"rgba(10, 15, 40, 0.8)" if IS_DARK else "rgba(248, 250, 252, 0.95)"};
        border: 1px solid rgba(124, 58, 237, 0.25);
        border-radius: 16px;
        padding: 24px;
        margin-top: 16px;
        position: relative;
        white-space: pre-wrap;
        line-height: 1.8;
        font-size: 0.95rem;
    }}

    .ai-output::before {{
        content: '🤖 AI Response';
        position: absolute;
        top: -10px;
        left: 20px;
        background: linear-gradient(135deg, {PRIMARY}, {ACCENT});
        color: white;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 1px;
    }}

    /* ─── Download Button ─── */
    .stDownloadButton > button {{
        background: linear-gradient(135deg, {NEON_GREEN}, #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
    }}

    /* ─── Progress Bars ─── */
    .usage-bar {{
        background: rgba(255,255,255,0.06);
        border-radius: 8px;
        overflow: hidden;
        height: 8px;
        margin: 6px 0;
    }}

    .usage-fill {{
        height: 100%;
        border-radius: 8px;
        background: linear-gradient(90deg, {PRIMARY}, {ACCENT});
        transition: width 0.8s ease;
    }}

    /* ─── Animations ─── */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(24px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    @keyframes glow {{
        0%, 100% {{ box-shadow: 0 0 20px {PRIMARY}44; }}
        50% {{ box-shadow: 0 0 40px {PRIMARY}88, 0 0 60px {ACCENT}33; }}
    }}

    @keyframes rotateBg {{
        from {{ transform: rotate(0deg); }}
        to {{ transform: rotate(360deg); }}
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-10px); }}
    }}

    @keyframes shimmer {{
        0% {{ background-position: -200% center; }}
        100% {{ background-position: 200% center; }}
    }}

    .animate-in {{ animation: fadeInUp 0.5s ease-out; }}
    .glow-pulse {{ animation: glow 3s infinite; }}
    .float {{ animation: float 4s ease-in-out infinite; }}

    /* ─── Scrollbar ─── */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: {"#0a0f28" if IS_DARK else "#f1f5f9"}; }}
    ::-webkit-scrollbar-thumb {{
        background: {PRIMARY};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{ background: {PRIMARY_LIGHT}; }}

</style>
"""
