# ==========================================================
# MTSE Marketing Engine v13 - Main Application Entry
# Digital Sovereignty Hub - Next-Gen AI Marketing Platform
# ==========================================================

import streamlit as st
import base64

# Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="MTSE v13 — AI Marketing Platform",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# IMPORTS
# ==============================

from config import (
    PREMIUM_CSS, APP_NAME_AR, APP_NAME_EN, BORDER_GLOW,
    APP_VERSION, PRIMARY, ACCENT, PRIMARY_LIGHT, NEON_GREEN
)
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
from views import social_command_page
from views import campaign_builder_view
from views import owner_panel_page
from views import ai_engine_page
from views import ai_secrets_page
from views import brand_voice_page

# v13 New Modules
try:
    from views import image_generator_page
    HAS_IMAGE_GEN = True
except ImportError:
    HAS_IMAGE_GEN = False

try:
    from views import competitor_intel_page
    HAS_COMPETITOR = True
except ImportError:
    HAS_COMPETITOR = False

try:
    from views import trend_forecaster_page
    HAS_TRENDS = True
except ImportError:
    HAS_TRENDS = False

try:
    from views import email_campaign_page
    HAS_EMAIL = True
except ImportError:
    HAS_EMAIL = False

# AI Router
try:
    from ai_engine.router import router
except ImportError:
    router = None

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

# ==============================
# LOGIN SCREEN
# ==============================

if not st.session_state.logged_in:
    # ─── v13 PREMIUM LANDING PAGE ───

    # Language toggle (pre-login)
    lang_col1, lang_col2, lang_space = st.columns([0.5, 0.5, 9])
    with lang_col1:
        if st.button("🇪🇬 عربي", key="pre_ar", use_container_width=True):
            st.session_state.lang = "AR"
            st.rerun()
    with lang_col2:
        if st.button("🇺🇸 EN", key="pre_en", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()

    # Hero Section
    st.markdown(f"""
    <div class="hero-v13 animate-in">
        <div class="hero-badge">🌌 {t("الجيل القادم من الذكاء التسويقي", "Next-Gen AI Marketing Intelligence")}</div>
        <h1 class="hero-title">MTSE AI Platform v13</h1>
        <p class="hero-subtitle">
            {t("نظام السيادة الرقمية المتكامل — أقوى منصة تسويق ذكي في منطقة الشرق الأوسط وأفريقيا",
               "The Unified Digital Sovereignty System — The most powerful AI marketing platform in MENA & Africa")}
        </p>
        <div style="display:flex; gap:12px; justify-content:center; position:relative; z-index:2; flex-wrap:wrap;">
            <span class="hero-cta">🚀 {t("ابدأ الآن مجاناً", "Start Free Today")}</span>
            <span style="display:inline-block; padding:16px 32px; border:1px solid rgba(124,58,237,0.4); border-radius:16px; color:#94a3b8; font-weight:600; cursor:pointer;">
                ▶ {t("شاهد العرض", "Watch Demo")}
            </span>
        </div>
        <div class="stats-row">
            <div class="stat-item">
                <div class="stat-value">500+</div>
                <div class="stat-label">{t("علامة تجارية", "Brands")}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">50M+</div>
                <div class="stat-label">{t("وصول", "Reach")}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">99.9%</div>
                <div class="stat-label">{t("وقت التشغيل", "Uptime")}</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">6</div>
                <div class="stat-label">{t("نماذج AI", "AI Models")}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Features Grid
    st.markdown(f"<div style='margin:32px 0 20px; text-align:center;'><h2 style='color:{PRIMARY_LIGHT}; font-weight:800;'>⚡ {t('أدوات الذكاء الاصطناعي', 'AI-Powered Tools')}</h2></div>", unsafe_allow_html=True)

    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🚀", t("بناء الحملات", "Campaign Builder"), t("بناء حملات متكاملة عبر كل المنصات في ثوانٍ", "Build complete multi-platform campaigns in seconds")),
        ("🎨", t("استوديو الإبداع", "Creative Studio"), t("توليد صور ونصوص احترافية بقوة DALL-E 3", "Generate pro images & copy with DALL-E 3")),
        ("📊", t("تحليلات لحظية", "Live Analytics"), t("رؤى تنبؤية فورية وتتبع ذكي للأداء", "Real-time predictive insights & smart tracking")),
        ("🧠", t("استراتيجية AI", "AI Strategy"), t("تحليل المنافسين وتوقع الاتجاهات بالذكاء الاصطناعي", "Competitor analysis & trend forecasting with AI")),
    ]
    for col, (icon, title, desc) in zip([f1, f2, f3, f4], features):
        with col:
            st.markdown(f"""
            <div class="feature-card animate-in">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    f5, f6, f7, f8 = st.columns(4)
    features2 = [
        ("🎬", t("محرك الفيديو", "Video Engine"), t("نصوص فيديو احترافية لـ TikTok و YouTube و Reels", "Pro video scripts for TikTok, YouTube & Reels")),
        ("📧", t("حملات البريد", "Email Campaigns"), t("سلاسل بريدية كاملة ومخصصة بالذكاء الاصطناعي", "Full personalized email sequences with AI")),
        ("🔮", t("توقع الاتجاهات", "Trend Forecaster"), t("توقعات للاتجاهات لـ 30/60/90 يوم", "30/60/90-day market trend predictions")),
        ("🌐", t("قيادة السوشيال", "Social Command"), t("إدارة مركزية لكل منصاتك الاجتماعية", "Centralized management for all social profiles")),
    ]
    for col, (icon, title, desc) in zip([f5, f6, f7, f8], features2):
        with col:
            st.markdown(f"""
            <div class="feature-card animate-in">
                <span class="feature-icon">{icon}</span>
                <div class="feature-title">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Pricing Section (1 Free + 2 Paid)
    st.markdown(f"<div style='text-align:center; margin:32px 0 20px;'><h2 style='color:{PRIMARY_LIGHT}; font-weight:800;'>💎 {t('خطط الاشتراك', 'Subscription Plans')}</h2></div>", unsafe_allow_html=True)

    p1, p2, p3 = st.columns(3)
    plans = [
        ("Starter", "🆓", "0", False, [
            "AI Campaign Builder (5/mo)", 
            "Analytics Dashboard", 
            "1 Social Profile"
        ]),
        ("Pro", "⚡", "299", True, [
            "AI Image Studio (DALL-E 3)", 
            "Video Script Engine", 
            "Email Campaigns",
            "5 Social Profiles"
        ]),
        ("Command", "👑", "799", False, [
            "Trend Forecaster (90-day)", 
            "Strategy Deep Dive", 
            "White-label Reports",
            "Unlimited Profiles"
        ]),
    ]
    
    for col, (name, icon, price, popular, feats) in zip([p1, p2, p3], plans):
        with col:
            popular_html = f'<div class="popular-badge">{t("الأكثر طلباً", "POPULAR")}</div>' if popular else ''
            currency_symbol = t("ج.م", "EGP")
            feats_html = "".join([f"<div style='margin:8px 0; font-size:0.85rem; color:#94a3b8;'>✅ {f}</div>" for f in feats])
            popular_class = 'popular' if popular else ''
            month_text = t('شهر', 'month')
            
            # COMPLETELY STATIC HTML TEMPLATE TO AVOID F-STRING/FORMAT CONFLICTS
            html_template = """
            <div class="pricing-card [POPULAR_CLASS]" style="min-height:420px; display: flex; flex-direction: column; align-items: center; justify-content: flex-start; padding: 32px 20px;">
                [POPULAR_HTML]
                <div style="font-size:2.5rem; margin-bottom:8px;">[ICON]</div>
                <div style="font-size:1.2rem; font-weight:700; color:var(--text-primary); margin-bottom: 8px;">[NAME]</div>
                <div class="price-amount" style="direction:ltr; font-size: 2.8rem; font-weight: 800; margin-bottom: 4px;">[PRICE] <span style="font-size:1.2rem;">[CURRENCY]</span></div>
                <div style="color:#64748b; font-size:0.8rem; margin-bottom:16px;">/[MONTH]</div>
                <div style="width: 100%; text-align: left; padding-left: 10px;">
                    [FEATS]
                </div>
            </div>
            """
            
            final_html = html_template.replace("[POPULAR_CLASS]", popular_class)\
                                     .replace("[POPULAR_HTML]", popular_html)\
                                     .replace("[ICON]", icon)\
                                     .replace("[NAME]", name)\
                                     .replace("[PRICE]", str(price))\
                                     .replace("[CURRENCY]", currency_symbol)\
                                     .replace("[MONTH]", month_text)\
                                     .replace("[FEATS]", feats_html)
            
            st.markdown(final_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)


    # Login Form
    st.markdown(f"<div id='login'></div>", unsafe_allow_html=True)
    _, login_col, _ = st.columns([1, 1.5, 1])

    with login_col:
        st.markdown(f"""
        <div class="login-card animate-in">
            <div style="text-align:center; margin-bottom:24px;">
                <div style="font-size:2.5rem; filter:drop-shadow(0 0 12px {PRIMARY}88);">🌌</div>
                <h3 style="margin:8px 0; background: linear-gradient(135deg, #fff, {PRIMARY_LIGHT}); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">
                    {t("الولوج للمنصة الذكية", "Secure Intelligence Access")}
                </h3>
                <div style="color:#64748b; font-size:0.85rem;">MTSE v{APP_VERSION}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab_login, tab_signup = st.tabs([t("🔐 تسجيل الدخول", "🔐 Sign In"), t("✨ إنشاء حساب", "✨ Create Account")])

        with tab_login:
            with st.form("login_form_v13"):
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
                    t("🔐 دخول إلى المنصة", "🔐 Enter Platform"),
                    use_container_width=True,
                    type="primary"
                )
                if submitted:
                    success, message = login_user(username, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)

        with tab_signup:
            with st.form("signup_form_v13"):
                new_username = st.text_input(
                    t("اختر اسم مستخدم", "Choose a Username"),
                    placeholder=t("حروف إنجليزية وأرقام فقط", "Letters and numbers only")
                )
                new_password = st.text_input(
                    t("كلمة المرور", "Password"),
                    type="password",
                    placeholder=t("6 أحرف على الأقل", "At least 6 characters")
                )
                new_email = st.text_input(
                    t("البريد الإلكتروني", "Email"),
                    placeholder=t("example@domain.com", "example@domain.com")
                )
                signup_submitted = st.form_submit_button(
                    t("🚀 إنشاء حساب مجاني", "🚀 Create Free Account"),
                    use_container_width=True,
                    type="primary"
                )
                if signup_submitted:
                    if not new_username or not new_password:
                        st.error(t("يرجى إدخال جميع البيانات", "Please fill in all fields"))
                    elif len(new_password) < 6:
                        st.error(t("كلمة المرور يجب أن تكون 6 أحرف على الأقل", "Password must be at least 6 characters"))
                    else:
                        from auth import hash_password
                        from database import create_user
                        success = create_user(
                            new_username,
                            hash_password(new_password),
                            "Viewer",
                            "Starter"
                        )
                        if success:
                            st.success(t("✅ تم إنشاء الحساب! يرجى تسجيل الدخول.", "✅ Account created! Please sign in."))
                        else:
                            st.error(t("❌ اسم المستخدم مسجل مسبقاً.", "❌ Username already exists."))

    # Footer
    st.markdown(f"""
    <div style="text-align:center; color:#475569; margin-top:48px; padding:24px; border-top:1px solid rgba(124,58,237,0.1);">
        <div style="margin-bottom:8px;">
            <span style="background:linear-gradient(135deg,{PRIMARY_LIGHT},{ACCENT}); -webkit-background-clip:text; -webkit-text-fill-color:transparent; font-weight:700;">
                MTSE AI v{APP_VERSION}
            </span>
        </div>
        <div style="font-size:0.8rem;">
            {t("جميع الحقوق محفوظة", "All Rights Reserved")} © 2026 MTSE Digital Sovereignty
        </div>
        <div style="margin-top:12px; display:flex; gap:16px; justify-content:center; font-size:0.8rem;">
            <span>🧠 GPT-4o</span>
            <span>✨ Gemini 1.5 Pro</span>
            <span>🦙 Llama 3.3</span>
            <span>🌀 Mixtral</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.stop()

# ==============================
# MAIN APP (After Login)
# ==============================

page = st.session_state.get("page", "Dashboard")
username = st.session_state.get("username", "")
role = st.session_state.get("role", "")
plan = st.session_state.get("plan", "Starter")

# ─── SIDEBAR v13 ───
with st.sidebar:
    # Logo
    st.markdown(f"""
    <div class="sidebar-logo">
        <span class="sidebar-logo-icon float">🌌</span>
        <div class="sidebar-logo-title">MTSE Platform</div>
        <div class="sidebar-version">v{APP_VERSION} · Digital Sovereignty</div>
    </div>
    """, unsafe_allow_html=True)

    # User info badge
    plan_colors = {"Starter": "#38bdf8", "Pro": "#a78bfa", "Command": "#f0abfc"}
    plan_color = plan_colors.get(plan, PRIMARY_LIGHT)
    st.markdown(f"""
    <div class="sidebar-user">
        <div style="font-size:1.4rem;">👤</div>
        <div style="font-weight:600; font-size:0.9rem; margin:4px 0;">{username}</div>
        <div style="display:flex; gap:6px; justify-content:center; flex-wrap:wrap;">
            <span style="background:rgba(124,58,237,0.15); color:{PRIMARY_LIGHT}; padding:2px 10px; border-radius:20px; font-size:0.75rem;">{role}</span>
            <span style="background:rgba(56,189,248,0.12); color:{plan_color}; padding:2px 10px; border-radius:20px; font-size:0.75rem;">✦ {plan}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # ─── Navigation ───
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    # Navigation Sections Array (List of Tuples: (ExpanderLabel, ItemsList))
    nav_structure = [
        (f'🏠 {t("الرئيسية", "CORE")}', [
            ("Dashboard", "🏠", t("لوحة التحكم", "Dashboard")),
            ("Workspace", "🏢", t("مساحة العمل", "Workspace"))
        ]),
        (f'🧠 {t("الاستراتيجية والذكاء", "STRATEGY & INTEL")}', [
            ("Strategy Hub", "🔮", t("مركز الاستراتيجية", "Strategy Hub")),
            ("Brand Voice", "🎭", t("بصمة العلامة", "Brand Voice")),
            ("Competitor Intel", "🕵️", t("استخبارات المنافسين", "Competitor Intel")),
            ("Trend Forecaster", "📈", t("توقع الاتجاهات", "Trend Forecaster"))
        ]),
        (f'🚀 {t("الحملات والإبداع", "CAMPAIGNS & CREATIVE")}', [
            ("Campaign Hub", "🚀", t("مركز الحملات", "Campaign Hub")),
            ("AI Engines", "🤖", t("محركات الذكاء الاصطناعي", "AI Engines")),
            ("Creative Studio", "🎨", t("استوديو الإبداع", "Creative Studio")),
            ("Image Studio", "🖼️", t("استوديو الصور", "Image Studio")),
            ("Video Scripts", "🎬", t("نصوص الفيديو", "Video Scripts")),
            ("Email Campaigns", "📧", t("حملات البريد", "Email Campaigns"))
        ]),
        (f'📊 {t("التحليلات", "ANALYTICS")}', [
            ("Real-time Analytics", "📊", t("التحليلات اللحظية", "Live Analytics")),
            ("Social Command", "🌐", t("قيادة السوشيال", "Social Command"))
        ]),
        (f'⚙️ {t("الإعدادات", "SETTINGS")}', [
            ("AI Secrets", "🔑", t("مفاتيح الذكاء الاصطناعي", "AI Secrets")),
            ("Reports", "📄", t("التقارير", "Reports")),
            ("Billing", "💳", t("الاشتراك والفواتير", "Billing")),
            ("Settings", "⚙️", t("الإعدادات", "Settings"))
        ])
    ]

    from config import ADMIN_DEFAULT_USERNAME
    if username == ADMIN_DEFAULT_USERNAME or role == "admin":
        nav_structure.append(
            (f'👑 {t("المالك", "OWNER")}', [
                ("Owner Panel", "👑", t("لوحة المالك", "Owner Panel")),
                ("Users", "👥", t("إدارة المستخدمين", "User Management"))
            ])
        )

    # Render Nav Structure in Collapsible Expanders
    for section_label, section_items in nav_structure:
        # Keep expander open if the current page is inside it
        is_expanded = any(st.session_state.page == item[0] for item in section_items)
        with st.expander(section_label, expanded=is_expanded):
            for page_id, icon, label in section_items:
                is_active = st.session_state.page == page_id
                btn_style = "primary" if is_active else "secondary"
                if st.button(f"{icon}  {label}", use_container_width=True, key=f"nav_{page_id}", type=btn_style):
                    st.session_state.page = page_id
                    st.rerun()

    st.markdown("---")

    # Language & Theme Controls
    lang_c1, lang_c2 = st.columns(2)
    with lang_c1:
        if st.button("🇪🇬 عربي", key="side_ar", use_container_width=True):
            st.session_state.lang = "AR"
            st.rerun()
    with lang_c2:
        if st.button("🇺🇸 EN", key="side_en", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()

    current_mode = st.session_state.get("theme_mode", "Quantum Dark")
    new_mode = "Solar Light" if current_mode == "Quantum Dark" else "Quantum Dark"
    icon_mode = "☀️" if current_mode == "Quantum Dark" else "🌙"
    if st.button(f"{icon_mode} {t('تبديل الوضع', 'Toggle Theme')}", use_container_width=True):
        st.session_state.theme_mode = new_mode
        st.rerun()

    st.markdown("---")

    if st.button(f"🔴 {t('تسجيل الخروج', 'Logout')}", use_container_width=True):
        logout_user()
        st.rerun()

    # AI Assistant Toggle
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"🤖 {t('المساعد الذكي', 'AI Assistant')}", use_container_width=True, type="primary"):
        st.session_state.show_assistant = not st.session_state.get("show_assistant", False)
        st.rerun()

    # Floating AI Assistant Widget
    if st.session_state.get("show_assistant", False):
        st.markdown(f"""
        <div class="glass-card" style="margin-top:12px; padding:16px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:12px;">
                <span style="font-size:1.5rem; filter:drop-shadow(0 0 8px {PRIMARY}88);">🤖</span>
                <div>
                    <div style="font-weight:700; font-size:0.9rem;">{t('المساعد الذكي v13', 'Smart Assistant v13')}</div>
                    <span class="badge badge-success">● Online</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        user_q = st.chat_input(t("اسأل المساعد...", "Ask the Assistant..."), key="sidebar_chat")
        if user_q:
            st.info(f"🤖: {t('سأساعدك الآن! جاري التحليل...', 'On it! Analyzing your request...')}")

# ==============================
# PAGE ROUTING v13
# ==============================

page = st.session_state.get("page", "Dashboard")

page_map = {
    "Owner Panel": owner_panel_page,
    "Dashboard": dashboard_page,
    "Strategy Hub": intel_hub_page,
    "AI Engines": ai_engine_page,
    "Creative Studio": creative_hub_page,
    "Real-time Analytics": analytics_page,
    "Social Command": social_command_page,
    "Campaign Hub": campaign_builder_view,
    "Video Scripts": video_intel_page,
    "Workspace": workspace_page,
    "AI Secrets": ai_secrets_page,
    "Brand Voice": brand_voice_page,
    "Reports": reports_page,
    "Billing": billing_page,
    "Settings": settings_page,
    "Users": users_page,
}

# Add optional v13 modules if available
if HAS_IMAGE_GEN:
    page_map["Image Studio"] = image_generator_page
if HAS_COMPETITOR:
    page_map["Competitor Intel"] = competitor_intel_page
if HAS_TRENDS:
    page_map["Trend Forecaster"] = trend_forecaster_page
if HAS_EMAIL:
    page_map["Email Campaigns"] = email_campaign_page

# Render the selected page
if page in page_map:
    page_map[page].render()
else:
    dashboard_page.render()
