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
        --primary-light: #a5b4fc;
        --primary-dark: #4338ca;
        --accent: #0ea5e9;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --bg-dark: #0f172a;
        --bg-card: rgba(30, 41, 59, 0.7);
        --bg-card-hover: rgba(51, 65, 85, 0.8);
        --text-primary: #f8fafc;
        --text-secondary: #94a3b8;
        --border: rgba(148, 163, 184, 0.1);
        --glass-bg: rgba(15, 23, 42, 0.8);
        --glass-border: rgba(255, 255, 255, 0.05);
    }

    /* Global Styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: var(--bg-card);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }

    .glass-card:hover {
        transform: translateY(-4px);
        background: var(--bg-card-hover);
        border-color: rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }

    /* Logo Header */
    .logo-container {
        background: linear-gradient(135deg, var(--primary-dark) 0%, var(--accent) 100%);
        padding: 40px;
        border-radius: 28px;
        text-align: center;
        margin-bottom: 35px;
        box-shadow: 0 15px 30px rgba(99, 102, 241, 0.4);
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .logo-img {
        width: 100px;
        margin-bottom: 15px;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
    }

    .logo-container::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        pointer-events: none;
    }

    .logo-container h1 {
        color: white !important;
        font-weight: 800;
        font-size: 2.4rem;
        margin: 0;
        letter-spacing: -1px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }

    /* Buttons */
    .stButton > button {
        border-radius: 14px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        transition: all 0.2s ease !important;
        background: var(--primary) !important;
        border: none !important;
        color: white !important;
    }

    .stButton > button:hover {
        background: var(--primary-dark) !important;
        transform: scale(1.02) !important;
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4) !important;
    }

    /* KPI Metric Cards */
    .kpi-card {
        background: var(--bg-card);
        border: 1px solid var(--glass-border);
        border-radius: 20px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .kpi-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #818cf8, #0ea5e9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
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
