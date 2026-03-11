# ==========================================================
# MTSE Marketing Engine - SaaS Edition v2.0
# Main Application Entry Point
# ==========================================================

import streamlit as st

# Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="MTSE Marketing Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# IMPORTS
# ==============================

from config import PREMIUM_CSS, APP_NAME_AR, APP_NAME_EN, BORDER_GLOW
from database import init_database
from auth import init_session, login_user, create_default_admin, logout_user
from utils import t

from views import dashboard_page
from views import analytics_page
from views import ai_engine_page
from views import reports_page
from views import users_page
from views import billing_page
from views import settings_page
from views import workspace_page
from views import video_intel_page
from views import intel_hub_page
from views import creative_hub_page
from views import industrial_hub_page
from views import social_command_page
from views import owner_panel_page

# ==============================
# INIT
# ==============================

# Apply premium CSS theme
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)

# Initialize database and default admin
init_database()
create_default_admin()

# Initialize session
init_session()

# Load Logo Base64
import base64
try:
    with open("mtse_logo.png", "rb") as f:
        st.session_state.logo_base64 = base64.b64encode(f.read()).decode()
except:
    st.session_state.logo_base64 = ""

# ==============================
# LOGIN SCREEN
# ==============================

if not st.session_state.logged_in:

    # Language switcher on login page
    col_spacer, col_ar, col_en = st.columns([6, 1, 1])
    with col_ar:
        if st.button("🇪🇬 عربي", key="login_ar"):
            st.session_state.lang = "AR"
            st.rerun()
    with col_en:
        if st.button("🇺🇸 EN", key="login_en"):
            st.session_state.lang = "EN"
            st.rerun()

    # Logo
    st.markdown(f"""
    <div class="logo-container" style="background: linear-gradient(135deg, #6d28d9 0%, #06b6d4 100%);">
        <div style="font-size: 5rem; margin-bottom: 20px; filter: drop-shadow(0 0 15px rgba(255,255,255,0.4));">🌌</div>
        <h1 style="background: linear-gradient(to right, #fff, #c4b5fd); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">MTSE v11</h1>
        <p>{t("نظام السيادة الرقمية الفائق", "Hyper Digital Sovereignty OS")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Login form
    st.markdown("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
        <div class="glass-card" style="padding:16px; margin-bottom:16px;">
            <h3 style="text-align:center; margin-bottom:0;">{t("مرحباً بك في المنصة الذكية", "Welcome to the Smart Platform")}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        tab_login, tab_signup = st.tabs([t("تسجيل الدخول", "Sign In"), t("إنشاء حساب جديد", "Create Account")])

        with tab_login:
            with st.form("login_form"):
                username = st.text_input(
                    t("اسم المستخدم", "Username"),
                    placeholder=t("أدخل اسم المستخدم", "Enter your username")
                )
                password = st.text_input(
                    t("كلمة المرور", "Password"),
                    type="password",
                    placeholder=t("أدخل كلمة المرور", "Enter your password")
                )

                submitted = st.form_submit_button(
                    t("🔐 دخول", "🔐 Sign In"),
                    use_container_width=True
                )

                if submitted:
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        with tab_signup:
            with st.form("signup_form"):
                new_username = st.text_input(
                    t("اختر اسم مستخدم", "Choose a Username"),
                    placeholder=t("حروف إنجليزية وأرقام فقط", "English letters and numbers only")
                )
                new_password = st.text_input(
                    t("كلمة المرور", "Password"),
                    type="password",
                    placeholder=t("اختر كلمة مرور قوية", "Choose a strong password")
                )
                new_email = st.text_input(
                    t("البريد الإلكتروني", "Email"),
                    placeholder=t("أدخل بريدك الإلكتروني", "Enter your email")
                )
                
                signup_submitted = st.form_submit_button(
                    t("🚀 إنشاء حساب جديد", "🚀 Create Account"),
                    use_container_width=True
                )
                
                if signup_submitted:
                    if not new_username or not new_password:
                        st.error(t("يرجى إدخال اسم المستخدم وكلمة المرور", "Please enter username and password"))
                    elif len(new_password) < 6:
                        st.error(t("كلمة المرور يجب أن تكون 6 أحرف على الأقل", "Password must be at least 6 characters"))
                    else:
                        from auth import hash_password
                        from database import create_user
                        success = create_user(
                            new_username,
                            hash_password(new_password),
                            "Viewer",  # Default role
                            "Explorer" # Default free/base plan
                        )
                        if success:
                            st.success(t("✅ تم إنشاء الحساب بنجاح! نرجو تسجيل الدخول الآن.", "✅ Account created! Please sign in now."))
                        else:
                            st.error(t("❌ اسم المستخدم هذا مسجل مسبقاً، اختر غيره.", "❌ Username already exists, choose another one."))

        # Footer
        st.markdown(f"""
        <div style="text-align:center; color:#94a3b8; margin-top:24px; font-size:0.85rem;">
            MTSE Digital Sovereignty v11.0 — {t("جميع الحقوق محفوظة", "All Rights Reserved")} © 2026
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ==============================
# MAIN APP (After Login)
# ==============================

# Sidebar Navigation
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div style="text-align:center; padding:16px 0; background: linear-gradient(to bottom, {BORDER_GLOW}, transparent); border-radius: 20px;">
        <div style="font-size:2.5rem; filter: drop-shadow(0 0 10px var(--primary));">🌌</div>
        <h3 style="margin:4px 0; color:var(--primary-light);">MTSE v11</h3>
        <p style="color:var(--accent); font-size:0.8rem; margin:0; font-weight:bold; letter-spacing:1px;">{t("السيادة الرقمية", "DIGITAL SOVEREIGNTY")}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # User info
    st.markdown(f"""
    <div style="text-align:center; padding:8px; margin-bottom:12px;">
        <div style="font-size:1.2rem;">👤 {st.session_state.username}</div>
        <div style="color:#94a3b8; font-size:0.8rem;">{st.session_state.role} • {st.session_state.plan}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    nav_items = [
        ("Dashboard", "🏠", t("لوحة التحكم", "Dashboard")),
        ("Intel Hub", "🌐", t("مركز الاستخبارات", "Intelligence Hub")),
        ("Creative War Room", "🎭", t("غرفة الحرب الإبداعية", "Creative War Room")),
        ("Industrial Hub", "⚙️", t("المركز الصناعي", "Industrial Hub")),
        ("Analytics", "📊", t("التحليلات المتكاملة", "Unified Analytics")),
        ("Social Command", "🚀", t("التنفيذ التلقائي", "Social Command")),
        ("Video Intelligence", "📹", t("ذكاء الفيديو", "Video Intelligence")),
        ("Workspace", "🏢", t("مساحة العمل", "Workspace Hub")),
        ("Users", "👥", t("المستخدمين", "Users")),
        ("Billing", "💳", t("الفوترة", "Billing")),
        ("Settings", "⚙️", t("الإعدادات", "Settings")),
    ]

    from config import ADMIN_DEFAULT_USERNAME
    if st.session_state.username == ADMIN_DEFAULT_USERNAME:
        nav_items.insert(0, ("Owner Panel", "👑", t("لوحة المالك (Owner)", "Owner Panel")))

    for page_id, icon, label in nav_items:
        is_active = st.session_state.page == page_id
        if st.button(
            f"{icon}  {label}",
            use_container_width=True,
            key=f"nav_{page_id}",
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = page_id
            st.rerun()

    st.markdown("---")

    # Language toggle in sidebar
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇪🇬 AR", key="sidebar_ar", use_container_width=True):
            st.session_state.lang = "AR"
            st.rerun()
    with col2:
        if st.button("🇺🇸 EN", key="sidebar_en", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()

    st.markdown("---")
    # v11 Dual-Core Toggle
    current_mode = st.session_state.get("theme_mode", "Quantum Dark")
    new_mode = "Solar Light" if current_mode == "Quantum Dark" else "Quantum Dark"
    if st.button(f"{'☀️' if current_mode == 'Quantum Dark' else '🌙'} {t('الوضع ' + ('المضيء' if current_mode == 'Quantum Dark' else 'المظلم'), 'Switch to ' + new_mode)}", use_container_width=True):
        st.session_state.theme_mode = new_mode
        st.rerun()

# ==============================
# PAGE ROUTING
# ==============================

page = st.session_state.page

page_map = {
    "Owner Panel": owner_panel_page,
    "Dashboard": dashboard_page,
    "Intel Hub": intel_hub_page,
    "Creative War Room": creative_hub_page,
    "Industrial Hub": industrial_hub_page,
    "Analytics": analytics_page,
    "Social Command": social_command_page,
    "Video Intelligence": video_intel_page,
    "Workspace": workspace_page,
    "Users": users_page,
    "Billing": billing_page,
    "Settings": settings_page,
}

if page in page_map:
    page_map[page].render()
else:
    dashboard_page.render()
