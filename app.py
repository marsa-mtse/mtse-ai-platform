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

from config import PREMIUM_CSS, APP_NAME_AR, APP_NAME_EN
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
from views import expert_tools_page
from views import cost_engine_page
from views import social_analysis_page
from views import technical_intel_page

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
    <div class="logo-container">
        <img src="data:image/png;base64,{st.session_state.get('logo_base64', '')}" class="logo-img">
        <h1>MTSE Marketing Engine</h1>
        <p>{t("منصة التسويق الذكية العالمية", "Global Smart Marketing Platform")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Login form
    st.markdown("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown(f"""
        <div class="glass-card" style="padding:32px;">
            <h3 style="text-align:center; margin-bottom:24px;">{t("تسجيل الدخول", "Sign In")}</h3>
        </div>
        """, unsafe_allow_html=True)

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

        # Footer
        st.markdown(f"""
        <div style="text-align:center; color:#94a3b8; margin-top:24px; font-size:0.85rem;">
            MTSE Marketing Engine v2.0 — {t("جميع الحقوق محفوظة", "All Rights Reserved")} © 2026
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
    <div style="text-align:center; padding:16px 0;">
        <div style="font-size:2rem;">📊</div>
        <h3 style="margin:4px 0;">MTSE</h3>
        <p style="color:#94a3b8; font-size:0.8rem; margin:0;">{t("منصة التسويق", "Marketing Engine")}</p>
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
        ("Analytics", "📊", t("التحليلات", "Analytics")),
        ("Expert Tools", "🛠️", t("أدوات النخبة", "Expert Tools")),
        ("AI Engine", "🤖", t("محرك AI", "AI Engine")),
        ("Reports", "📁", t("التقارير", "Reports")),
        ("Cost Engine", "💰", t("محرك التكاليف", "Cost Engine")),
        ("Social Sniper", "🎯", t("قناص السوشيال", "Social Sniper")),
        ("Technical Intel", "📐", t("استخبارات المخططات", "Technical Intel")),
        ("Users", "👥", t("المستخدمين", "Users")),
        ("Billing", "💳", t("الفوترة", "Billing")),
        ("Settings", "⚙️", t("الإعدادات", "Settings")),
    ]

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

# ==============================
# PAGE ROUTING
# ==============================

page = st.session_state.page

page_map = {
    "Dashboard": dashboard_page,
    "Analytics": analytics_page,
    "Expert Tools": expert_tools_page,
    "AI Engine": ai_engine_page,
    "Reports": reports_page,
    "Cost Engine": cost_engine_page,
    "Social Sniper": social_analysis_page,
    "Technical Intel": technical_intel_page,
    "Users": users_page,
    "Billing": billing_page,
    "Settings": settings_page,
}

if page in page_map:
    page_map[page].render()
else:
    dashboard_page.render()
