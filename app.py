# ==========================================================
# MTSE Marketing Engine - SaaS Edition v12.0
# Main Application Entry Point
# ==========================================================

import streamlit as st
import base64

# Page config MUST be the first Streamlit command
st.set_page_config(
    page_title="MTSE Digital Sovereignty v12",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# IMPORTS
# ==============================

from config import (
    PREMIUM_CSS, APP_NAME_AR, APP_NAME_EN, BORDER_GLOW,
    PLAN_BADGES, PRIMARY, PRIMARY_LIGHT, ACCENT, SUCCESS, WARNING
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
from views import campaign_builder_view
from views import owner_panel_page
from views import social_command_page

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
# LOGIN SCREEN  — WORLD-CLASS UI
# ==============================

if not st.session_state.logged_in:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none;}
        header[data-testid="stHeader"]   {display: none;}
        .block-container {padding-top: 0 !important; max-width: 100vw !important; padding-left: 0 !important; padding-right: 0 !important;}
    </style>
    """, unsafe_allow_html=True)

    hero_img = (
        f"data:image/png;base64,{st.session_state.hero_base64}"
        if st.session_state.get("hero_base64")
        else "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=1200&q=80"
    )

    left_col, right_col = st.columns([1.3, 1], gap="small")

    # ── LEFT PANEL (HERO) ─────────────────────────────────────────
    with left_col:
        st.markdown(f"""
        <div style="
            height:100vh;
            background: linear-gradient(rgba(3,7,18,0.55), rgba(3,7,18,0.92)),
                        url('{hero_img}') center/cover no-repeat;
            border-radius: 0 48px 48px 0;
            display: flex; flex-direction: column; justify-content: center;
            padding: 70px 60px;
            box-shadow: 12px 0 40px rgba(0,0,0,0.6);
            position: relative; overflow: hidden;
        ">
            <!-- Animated particles overlay -->
            <div style="
                position:absolute; inset:0; opacity:0.15;
                background:
                    radial-gradient(circle at 20% 30%, {PRIMARY} 0%, transparent 40%),
                    radial-gradient(circle at 80% 70%, {ACCENT} 0%, transparent 40%);
                border-radius: 0 48px 48px 0;
            "></div>

            <!-- Badge -->
            <div style="
                background: rgba(255,255,255,0.08);
                padding: 8px 22px;
                border-radius: 30px;
                display: inline-block;
                width: fit-content;
                margin-bottom: 28px;
                border: 1px solid rgba(255,255,255,0.18);
                backdrop-filter: blur(12px);
            ">
                <span style="color:{PRIMARY_LIGHT}; font-weight:700; font-size:0.88rem; letter-spacing:1.5px;">
                    🌌 MTSE DIGITAL SOVEREIGNTY v12
                </span>
            </div>

            <!-- Headline -->
            <h1 style="
                font-size:3.8rem; color:white; margin-bottom:22px;
                line-height:1.08; font-weight:900;
                text-shadow: 0 4px 24px rgba(0,0,0,0.6);
            ">
                {t("نظام إدارة", "Sovereign Campaign")} <br>
                <span style="
                    background: linear-gradient(90deg, {PRIMARY_LIGHT}, {ACCENT});
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    filter: drop-shadow(0 0 12px rgba(139,92,246,0.4));
                ">{t("الحملات الذكية", "Intelligence Platform")}</span>
            </h1>

            <p style="font-size:1.15rem; color:#cbd5e1; max-width:88%; line-height:1.75; margin-bottom:36px;">
                {t(
                    "أقوى محرك لتحليل البيانات وإدارة الحملات السيادية. تحكم بالمحتوى، تصدر التريند، واصنع التأثير في الشرق الأوسط وخارجه.",
                    "The most powerful AI-driven engine for data analysis and sovereign campaign management. Dominate trends and shape outcomes."
                )}
            </p>

            <!-- Features list -->
            <div style="display:flex; flex-direction:column; gap:12px;">
                {''.join([f"""
                <div style="display:flex; align-items:center; gap:12px; color:#e2e8f0;">
                    <div style="width:36px;height:36px;border-radius:10px;background:rgba(139,92,246,0.2);display:flex;align-items:center;justify-content:center;font-size:1.1rem;border:1px solid rgba(139,92,246,0.3);">{icon}</div>
                    <span style="font-size:0.95rem;">{txt}</span>
                </div>""" for icon, txt in [
                    ("🤖", t("تحليل ذكي بـ Gemini 2.0 + Groq + GPT-4o", "Smart Analysis: Gemini 2.0 + Groq + GPT-4o")),
                    ("📊", t("تحليلات لحظية وتنبؤات بالذكاء الاصطناعي", "Real-time analytics & AI predictions")),
                    ("🎬", t("إنتاج محتوى لـ TikTok & Instagram & YouTube", "Content for TikTok, Instagram & YouTube")),
                    ("🆓", t("خطة مجانية متاحة — لا حاجة لبطاقة ائتمان", "Free plan available — no credit card needed")),
                ]])}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── RIGHT PANEL (AUTH FORMS) ─────────────────────────────────
    with right_col:
        st.markdown("""<div style="height:6vh;"></div>""", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:28px;">
            <div style="font-size:2.8rem; margin-bottom:10px; filter:drop-shadow(0 0 12px {PRIMARY}88);">🔐</div>
            <h2 style="font-size:2rem; color:{PRIMARY_LIGHT}; margin-bottom:6px; font-weight:900;">
                {t("مرحباً بك مجدداً", "Welcome Back")}
            </h2>
            <p style="color:#9ca3af; font-size:1rem;">
                {t("الولوج للمنظومة الذكية (Secure Access)", "Sign in to the sovereign system")}
            </p>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns([0.08, 1, 0.08])
        with c2:
            tab_login, tab_signup = st.tabs([
                t("🔑  تسجيل الدخول", "🔑  Sign In"),
                t("🆕  إنشاء حساب جديد", "🆕  Create Account")
            ])

            # ── TAB: LOGIN ─────────────────────────────────────────
            with tab_login:
                st.markdown('<div class="glass-card animate-in" style="padding:32px; margin-top:12px;">', unsafe_allow_html=True)
                with st.form("login_form"):
                    username = st.text_input(
                        t("📛  اسم المستخدم", "📛  Username"),
                        placeholder="admin"
                    )
                    password = st.text_input(
                        t("🔒  كلمة المرور", "🔒  Password"),
                        type="password",
                        placeholder="••••••••"
                    )
                    st.markdown("")
                    submitted = st.form_submit_button(
                        "➔  " + t("تسجيل الدخول والدخول للمنظومة", "Sign In & Enter"),
                        use_container_width=True
                    )
                    if submitted:
                        if not username or not password:
                            st.error(t("⚠️ يرجى إدخال بيانات الدخول", "⚠️ Please enter your credentials"))
                        else:
                            success, message = login_user(username, password)
                            if success:
                                st.rerun()
                            else:
                                st.error(t("❌ بيانات الدخول غير صحيحة أو الحساب مقفل", "❌ Invalid credentials or account locked"))

                st.markdown("</div>", unsafe_allow_html=True)

                # Free plan callout
                st.markdown(f"""
                <div style="text-align:center; margin-top:16px;">
                    <span style="color:#64748b; font-size:0.85rem;">
                        {t("ليس لديك حساب؟", "No account yet?")}
                        <span style="color:{PRIMARY_LIGHT}; font-weight:700; margin-right:6px;">
                            {t("سجّل مجاناً ←", "← Create one free")}
                        </span>
                    </span>
                </div>
                <div style="
                    background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(6,182,212,0.1));
                    border: 1px solid rgba(16,185,129,0.25);
                    border-radius:14px; padding:12px 18px; text-align:center;
                    margin-top:14px;
                ">
                    <span style="color:{SUCCESS}; font-size:0.88rem; font-weight:700;">
                        🆓 {t("الخطة المجانية متاحة الآن — 3 تقارير شهرياً بدون بطاقة ائتمان!", "Free plan now available — 3 reports/month, no credit card!")}
                    </span>
                </div>
                """, unsafe_allow_html=True)

            # ── TAB: SIGNUP ───────────────────────────────────────
            with tab_signup:
                st.markdown('<div class="glass-card animate-in" style="padding:32px; margin-top:12px;">', unsafe_allow_html=True)

                # Free plan highlight
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, rgba(16,185,129,0.12), rgba(6,182,212,0.08));
                    border: 1px solid rgba(16,185,129,0.3);
                    border-radius: 12px; padding: 12px 16px; margin-bottom: 20px;
                    text-align: center;
                ">
                    <b style="color:{SUCCESS};">🆓 {t("الخطة المجانية (Explorer)", "Free Plan (Explorer)")}</b>
                    <span style="color:#94a3b8; font-size:0.88rem; margin-right:8px;">
                        — {t("3 تقارير + 3 رفع شهرياً، مجاناً تماماً", "3 reports + 3 uploads/month, completely free")}
                    </span>
                </div>
                """, unsafe_allow_html=True)

                with st.form("signup_form"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        full_name = st.text_input(
                            t("👤  الاسم الكامل", "👤  Full Name"),
                            placeholder=t("محمد أحمد", "John Doe")
                        )
                    with col_b:
                        new_user = st.text_input(
                            t("📛  اسم المستخدم", "📛  Username"),
                            placeholder="user_001"
                        )

                    new_email = st.text_input(
                        t("📧  البريد الإلكتروني", "📧  Email Address"),
                        placeholder="example@email.com"
                    )

                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        new_pass = st.text_input(
                            t("🔒  كلمة المرور", "🔒  Password"),
                            type="password",
                            placeholder="••••••••"
                        )
                    with col_p2:
                        confirm_pass = st.text_input(
                            t("🔒  تأكيد كلمة المرور", "🔒  Confirm Password"),
                            type="password",
                            placeholder="••••••••"
                        )

                    # Password strength indicator
                    if new_pass:
                        strength = 0
                        if len(new_pass) >= 8:  strength += 1
                        if any(c.isupper() for c in new_pass):  strength += 1
                        if any(c.isdigit() for c in new_pass):  strength += 1
                        if any(c in "!@#$%^&*" for c in new_pass): strength += 1
                        colors  = ["#ef4444", "#f59e0b", "#eab308", "#10b981"]
                        labels  = [
                            t("ضعيف جداً",   "Very Weak"),
                            t("ضعيف",        "Weak"),
                            t("متوسط",       "Medium"),
                            t("قوي",         "Strong"),
                        ]
                        st.markdown(f"""
                        <div style="margin:6px 0 12px;">
                            <div style="display:flex; gap:4px; margin-bottom:4px;">
                                {''.join([f'<div style="flex:1;height:5px;border-radius:4px;background:{"' + colors[strength-1] + '" if i < strength else "rgba(255,255,255,0.08)"};"></div>' for i in range(4)])}
                            </div>
                            <small style="color:{colors[strength-1]}; font-weight:700;">
                                {labels[strength-1]}
                            </small>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("")
                    terms = st.checkbox(t(
                        "أوافق على شروط الاستخدام وسياسة الخصوصية",
                        "I agree to the Terms of Service and Privacy Policy"
                    ))
                    signup_sub = st.form_submit_button(
                        "🚀  " + t("إنشاء الحساب مجاناً", "Create Free Account"),
                        use_container_width=True
                    )

                    if signup_sub:
                        errors = []
                        if not full_name.strip():
                            errors.append(t("الاسم الكامل مطلوب", "Full name is required"))
                        if not new_user.strip():
                            errors.append(t("اسم المستخدم مطلوب", "Username is required"))
                        if "@" not in new_email:
                            errors.append(t("البريد الإلكتروني غير صحيح", "Invalid email address"))
                        if len(new_pass) < 6:
                            errors.append(t("كلمة المرور ضعيفة جداً (6 أحرف على الأقل)", "Password too short (min 6 chars)"))
                        if new_pass != confirm_pass:
                            errors.append(t("كلمتا المرور غير متطابقتين", "Passwords do not match"))
                        if not terms:
                            errors.append(t("يجب الموافقة على الشروط", "You must agree to the terms"))

                        if errors:
                            for err in errors:
                                st.error(f"❌ {err}")
                        else:
                            from auth import hash_password
                            from database import create_user
                            if create_user(new_user.strip(), hash_password(new_pass), "Viewer", "Explorer"):
                                st.success(t(
                                    "✅ مرحباً بك! تم إنشاء حسابك المجاني. سجّل دخولك الآن.",
                                    "✅ Welcome! Your free account is ready. Sign in now."
                                ))
                            else:
                                st.error(t("❌ اسم المستخدم مسجل مسبقاً", "❌ Username already taken"))

                st.markdown("</div>", unsafe_allow_html=True)

        # Footer
        st.markdown(f"""
        <div style="text-align:center; color:#374151; margin-top:40px; font-size:0.82rem; letter-spacing:0.4px;">
            MTSE Digital Sovereignty Engine v12.0
            <br><br>
            {t("جميع الحقوق السيادية محفوظة", "All Sovereign Rights Reserved")} © 2026
        </div>
        """, unsafe_allow_html=True)

    st.stop()

# ==============================
# MAIN APP (After Login)
# ==============================

# Sidebar Navigation
with st.sidebar:
    badge_icon, badge_label, badge_color = PLAN_BADGES.get(
        st.session_state.plan, ("💎", st.session_state.plan, PRIMARY)
    )

    # Logo & Branding
    st.markdown(f"""
    <div style="text-align:center; padding:18px 0 12px; position:relative;">
        <div style="
            font-size: 2.8rem;
            filter: drop-shadow(0 0 14px {PRIMARY}88);
            margin-bottom: 6px;
        ">🌌</div>
        <h3 style="margin:2px 0 1px; color:{PRIMARY_LIGHT}; font-weight:900; letter-spacing:0.5px;">
            MTSE v12
        </h3>
        <p style="color:{ACCENT}; font-size:0.75rem; margin:0; font-weight:700; letter-spacing:2px; text-transform:uppercase;">
            {t("السيادة الرقمية", "DIGITAL SOVEREIGNTY")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # User info chip
    st.markdown(f"""
    <div style="
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 14px;
        padding: 12px 16px;
        margin-bottom: 14px;
        text-align: center;
    ">
        <div style="font-size:1.4rem; margin-bottom:4px;">👤</div>
        <div style="font-weight:700; color:#f1f5f9; font-size:0.95rem;">{st.session_state.username}</div>
        <div style="
            display:inline-block;
            background: rgba({badge_color.replace('#','').upper()}, 0.15);
            color: {badge_color};
            border-radius: 20px;
            padding: 2px 12px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-top: 4px;
            border: 1px solid {badge_color}44;
        ">{badge_icon} {badge_label}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Navigation
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    st.markdown(f"<p style='color:#4b5563; font-size:0.72rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; padding: 0 4px; margin-bottom:8px;'>{t('استكشاف المحاور', 'NAVIGATION')}</p>", unsafe_allow_html=True)

    nav_items = [
        ("Dashboard",          "🏠", t("نظرة عامة",          "Overview")),
        ("Strategy Hub",       "🧠", t("محور الاستراتيجية",  "Strategy Hub")),
        ("Campaign Hub",       "🚀", t("مركز الحملات",       "Campaign Hub")),
        ("Creative Studio",    "🎥", t("استوديو الإبداع",    "Creative Studio")),
        ("Real-time Analytics","📊", t("التحليلات اللحظية",  "Live Analytics")),
        ("Workspace",          "🏢", t("مساحة العمل",        "Workspace")),
    ]

    from config import ADMIN_DEFAULT_USERNAME
    if st.session_state.username == ADMIN_DEFAULT_USERNAME:
        nav_items.insert(0, ("Owner Panel", "👑", t("لوحة المالك", "Owner Panel")))

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

    # Utility buttons
    c_about, c_asst = st.columns(2)
    with c_about:
        if st.button("ℹ️ " + t("عن المنصة", "About"), use_container_width=True):
            st.session_state.show_about = not st.session_state.get("show_about", False)
    with c_asst:
        if st.button("🤖 " + t("المساعد", "AI"), use_container_width=True):
            st.session_state.show_assistant = not st.session_state.get("show_assistant", False)

    # Language toggle
    st.markdown(f"<p style='color:#374151; font-size:0.7rem; font-weight:700; letter-spacing:1.5px; margin-top:4px;'>{t('اللغة', 'LANGUAGE')}</p>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🇸🇦 عربي", key="sidebar_ar", use_container_width=True):
            st.session_state.lang = "AR"
            st.rerun()
    with col2:
        if st.button("🇺🇸 EN", key="sidebar_en", use_container_width=True):
            st.session_state.lang = "EN"
            st.rerun()

    st.markdown("---")

    # Theme toggle
    current_mode = st.session_state.get("theme_mode", "Quantum Dark")
    new_mode     = "Solar Light" if current_mode == "Quantum Dark" else "Quantum Dark"
    if st.button(
        f"{'☀️' if current_mode == 'Quantum Dark' else '🌙'}  {t('الوضع المضيء' if current_mode == 'Quantum Dark' else 'الوضع المظلم', 'Light Mode' if current_mode == 'Quantum Dark' else 'Dark Mode')}",
        use_container_width=True
    ):
        st.session_state.theme_mode = new_mode
        st.rerun()

    if st.button("🔴  " + t("تسجيل الخروج", "Sign Out"), use_container_width=True):
        logout_user()
        st.rerun()

# ==============================
# PAGE ROUTING
# ==============================

page = st.session_state.page

page_map = {
    "Owner Panel":          owner_panel_page,
    "Dashboard":            dashboard_page,
    "Strategy Hub":         intel_hub_page,
    "Creative Studio":      creative_hub_page,
    "Real-time Analytics":  analytics_page,
    "Social Command":       social_command_page,
    "Campaign Hub":         campaign_builder_view,
    "Workspace":            workspace_page,
}

if page in page_map:
    # About overlay
    if st.session_state.get("show_about"):
        st.markdown(f"""
        <div class="glass-card animate-in" style="border-left: 5px solid {PRIMARY}; margin-bottom: 20px;">
            <h2>📌 {t("عن منصة MTSE AI v12", "About MTSE AI v12")}</h2>
            <p>{t("المنصة الرائدة في الشرق الأوسط لإدارة الحملات التسويقية والذكاء الاصطناعي السيادي.", "The leading MENA platform for AI-powered marketing campaign management and sovereign intelligence.")}</p>
            <ul>
                <li>{t("أتمتة المحتوى عبر TikTok و Instagram و YouTube", "Content automation for TikTok, Instagram & YouTube")}</li>
                <li>{t("تحليلات لحظية وتنبؤات ذكية متعددة المحركات", "Real-time analytics & multi-engine AI predictions")}</li>
                <li>{t("خطط متعددة تبدأ من المجاني", "Multiple plans starting from Free")}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # AI Assistant overlay
    if st.session_state.get("show_assistant"):
        with st.sidebar:
            st.markdown(f"""
            <div style="text-align:center; padding:14px; background:rgba(255,255,255,0.03); border-radius:16px; border:1px solid rgba(255,255,255,0.07);">
                <div style="font-size:2rem; margin-bottom:8px;">🤖</div>
                <h4 style="margin:0 0 6px; color:{PRIMARY_LIGHT};">{t("المساعد الذكي v12", "AI Assistant v12")}</h4>
            </div>
            """, unsafe_allow_html=True)
            st.info(t("كيف يمكنني مساعدتك في استراتيجيتك التسويقية؟", "How can I help with your marketing strategy?"))
            st.chat_input(t("اسأل المساعد...", "Ask the Assistant..."))

    # Graceful Global Exception Handling
    try:
        page_map[page].render()
    except Exception as e:
        import traceback
        st.error(t(
            "حدث خطأ تقني في هذه الصفحة. يرجى إعادة المحاولة.",
            "A technical error occurred. Please try again."
        ))
        with st.expander(t("تفاصيل للمطورين (Developer Details)", "Developer Details")):
            st.code(traceback.format_exc(), language="python")
else:
    dashboard_page.render()
