# ==========================================================
# MTSE Marketing Engine - Configuration
# ==========================================================

# ==============================
# PLAN LIMITS & PRICING
# ==============================

PLAN_LIMITS = {
    "Starter": {"reports": 5, "uploads": 5},
    "Pro": {"reports": 25, "uploads": 25},
    "Business": {"reports": 9999, "uploads": 9999}
}

PLAN_PRICING = {
    "Starter": 29,
    "Pro": 99,
    "Business": 299
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

APP_VERSION = "2.0.0"
APP_NAME_AR = "منصة MTSE للتسويق"
APP_NAME_EN = "MTSE Marketing Engine"

# ==============================
# PREMIUM CSS THEME
# ==============================

PREMIUM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Main Theme */
    :root {
        --primary: #6366f1;
        --primary-light: #818cf8;
        --primary-dark: #4f46e5;
        --accent: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: #1e293b;
        --bg-card-hover: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --border: #334155;
        --glass-bg: rgba(30, 41, 59, 0.7);
        --glass-border: rgba(99, 102, 241, 0.2);
    }

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* RTL Support */
    [data-lang="AR"] {
        direction: rtl;
        text-align: right;
    }

    .stTextInput > div > div > input,
    .stTextArea textarea {
        text-align: right;
        border-radius: 12px !important;
        border: 1px solid var(--border) !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid var(--glass-border);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }

    /* Logo Header */
    .logo-container {
        background: linear-gradient(135deg, var(--primary-dark), var(--accent));
        padding: 28px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 24px;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.3);
    }

    .logo-container h1 {
        color: white !important;
        font-weight: 700;
        font-size: 2rem;
        margin: 0;
        letter-spacing: -0.5px;
    }

    .logo-container p {
        color: rgba(255,255,255,0.75);
        font-size: 0.95rem;
        margin-top: 4px;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: linear-gradient(135deg, var(--bg-card), var(--bg-card-hover));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: transform 0.2s ease;
    }

    .kpi-card:hover {
        transform: translateY(-3px);
    }

    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .kpi-label {
        color: var(--text-secondary);
        font-size: 0.85rem;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: var(--text-secondary) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        text-align: right !important;
        transition: all 0.2s ease !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(99, 102, 241, 0.1) !important;
        color: var(--primary-light) !important;
    }

    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .badge-active {
        background: rgba(16, 185, 129, 0.15);
        color: var(--success);
        border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .badge-warning {
        background: rgba(245, 158, 11, 0.15);
        color: var(--warning);
        border: 1px solid rgba(245, 158, 11, 0.3);
    }

    .badge-danger {
        background: rgba(239, 68, 68, 0.15);
        color: var(--danger);
        border: 1px solid rgba(239, 68, 68, 0.3);
    }

    /* Tables */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden;
    }

    /* Progress Bars */
    .usage-bar {
        background: var(--bg-card);
        border-radius: 10px;
        overflow: hidden;
        height: 10px;
        margin: 8px 0;
    }

    .usage-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 0.6s ease;
    }

    /* Animations */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-in {
        animation: fadeInUp 0.5s ease-out;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }

    .pulse {
        animation: pulse 2s infinite;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        letter-spacing: 0.3px;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }

    /* Download Buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, var(--success), #059669) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
    }

    /* Section Dividers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-primary);
        border-bottom: 2px solid var(--primary);
        padding-bottom: 8px;
        margin: 24px 0 16px;
    }
</style>
"""
