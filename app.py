# ==========================================================
# MTSE Marketing Engine - SaaS Edition v2.0
# Main Application Entry Point
# ==========================================================

import streamlit as st
import base64

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
from views import reports_page
from views import users_page
from views import billing_page
from views import settings_page
from views import workspace_page
from views import video_intel_page
from views import intel_hub_page
from views import creative_hub_page
from views import campaign_builder_view
from views import owner_panel_page

# v12.0 New Infrastructure
from ai_engine.router import router
from services.social_connector import social_hub

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

# Load Assets
try:
    with open("assets/v12_hero.png", "rb") as f:
        st.session_state.hero_base64 = base64.b64encode(f.read()).decode()
    with open("assets/v12_assistant.png", "rb") as f:
        st.session_state.asst_base64 = base64.b64encode(f.read()).decode()
except:
    st.session_state.hero_base64 = ""
    st.session_state.asst_base64 = ""

# ==============================
# LOGIN SCREEN
# ==============================

if not st.session_state.logged_in:
    # --- V12 PREMIUM LANDING PAGE ---
    hero_img = f"data:image/png;base64,{st.session_state.hero_base64}" if st.session_state.get("hero_base64") else ""
    st.markdown(f"""
    <div class="hero-container" style="background: url('{hero_img}') center/cover;">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 style="font-size: 3.5rem; margin-bottom: 10px;">MTSE AI Platform v12</h1>
            <p style="font-size: 1.2rem; color: #cbd5e1; max-width: 600px; margin: 0 auto 30px;">
                {t("نظام السيادة الرقمية المتكامل - الجيل القادم من إدارة الحملات والذكاء التسويقي", "The Unified Digital Sovereignty System - Next-Gen Campaign Management & Marketing Intelligence")}
            </p>
            <div style="display: flex; gap: 15px; justify-content: center;">
                <a href="#login" style="text-decoration: none;">
                    <div style="background: var(--primary); color: white; padding: 12px 30px; border-radius: 12px; font-weight: bold; cursor: pointer;">
                        {t("ابدأ الآن", "Get Started")}
                    </div>
                </a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:
        st.markdown('<div id="login"></div>', unsafe_allow_html=True)
        # Custom login card
        st.markdown(f"""
        <div class="glass-card" style="margin-top: -50px; position: relative; z-index: 100;">
            <h3 style="text-align:center; margin-bottom:20px;">{t("الولوج للمنصة الذكية", "Secure Intelligence Access")}</h3>
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

    # Navigation Hubs v12.0
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    st.markdown(f"### {t('استكشاف المحاور', 'Explore Hubs')}")
    
    nav_items = [
        ("Dashboard", "🏠", t("نظرة عامة", "Control Center")),
        ("Strategy Hub", "🧠", t("محور الاستراتيجية", "Strategy Hub")),
        ("Campaign Hub", "🚀", t("مركز الحملات", "Campaign Hub")),
        ("Creative Studio", "🎥", t("استوديو الإبداع", "Creative Studio")),
        ("Real-time Analytics", "📊", t("التحليلات اللحظية", "Live Analytics")),
        ("Workspace", "🏢", t("مساحة العمل", "Workspace")),
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

    # Utility Section
    st.markdown("---")
    
    c_about, c_asst = st.columns(2)
    with c_about:
        if st.button("ℹ️ " + t("عن المنصة", "About"), use_container_width=True):
            st.session_state.show_about = not st.session_state.get("show_about", False)
    with c_asst:
        if st.button("🤖 " + t("المساعد", "AI"), use_container_width=True):
            st.session_state.show_assistant = not st.session_state.get("show_assistant", False)

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
    # v12 Dual-Core Toggle
    current_mode = st.session_state.get("theme_mode", "Quantum Dark")
    new_mode = "Solar Light" if current_mode == "Quantum Dark" else "Quantum Dark"
    if st.button(f"{'☀️' if current_mode == 'Quantum Dark' else '🌙'} {t('الوضع ' + ('المضيء' if current_mode == 'Quantum Dark' else 'المظلم'), 'Switch to ' + new_mode)}", use_container_width=True):
        st.session_state.theme_mode = new_mode
        st.rerun()

    if st.button("🔴 " + t("خروج", "Logout"), use_container_width=True):
        logout_user()
        st.rerun()

# ==============================
# PAGE ROUTING
# ==============================

page = st.session_state.page

page_map = {
    "Owner Panel": owner_panel_page,
    "Dashboard": dashboard_page,
    "Strategy Hub": intel_hub_page,
    "Creative Studio": creative_hub_page,
    "Real-time Analytics": analytics_page,
    "Social Command": social_command_page,
    "Campaign Hub": campaign_builder_view,
    "Workspace": workspace_page,
}

if page in page_map:
    # Handle Overlays first
    if st.session_state.get("show_about"):
        st.markdown(f"""
        <div class="glass-card animate-in" style="border-left: 5px solid var(--primary);">
            <h2>{t("عن منصة MTSE AI v12", "About MTSE AI v12")}</h2>
            <p>{t("المنصة الرائدة في الشرق الأوسط لإدارة الحملات التسويقية والذكاء الاصطناعي السيادي.", "The leading MENA platform for marketing campaign management and sovereign AI intelligence.")}</p>
            <ul>
                <li>{t("أتمتة المحتوى عبر TikTok و Instagram", "Content automation for TikTok & Instagram")}</li>
                <li>{t("تحليلات لحظية وتنبؤات ذكية", "Real-time analytics & smart predictions")}</li>
                <li>{t("محرك إبداعي لإنتاج الفيديوهات والمقالات", "Creative engine for video & article production")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.get("show_assistant"):
        with st.sidebar:
            asst_avatar = f"data:image/png;base64,{st.session_state.asst_base64}" if st.session_state.get("asst_base64") else ""
            st.markdown(f"""
            <div style="text-align:center; padding:10px;">
                <img src="{asst_avatar}" width="80" style="border-radius:50%; border: 2px solid var(--primary); box-shadow: var(--neon-glow);">
                <h3 style="margin-top:10px;">🤖 {t('المساعد الذكي v12', 'Smart Assistant v12')}</h3>
            </div>
            """, unsafe_allow_html=True)
            st.info(t("كيف يمكنني مساعدتك في استراتيجيتك التسويقية اليوم؟", "How can I help with your marketing strategy today?"))
            st.chat_input(t("اسأل المساعد...", "Ask the Assistant..."))

    page_map[page].render()
else:
    dashboard_page.render()
