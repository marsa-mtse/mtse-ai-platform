# ==========================================================
# MTSE Marketing Engine - SaaS Edition v12.0
# Main Application Entry Point - Python 3.11 Compatible
# ==========================================================

import streamlit as st

st.set_page_config(
    page_title="MTSE Digital Sovereignty v12",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── IMPORTS ───────────────────────────────────────────────────────────────────
from config import (
    PREMIUM_CSS, PRIMARY, PRIMARY_LIGHT, ACCENT, SUCCESS, WARNING,
    PLAN_BADGES, ADMIN_DEFAULT_USERNAME
)
from database import init_database
from auth import init_session, login_user, create_default_admin, logout_user, is_admin as _is_admin
from utils import t

from views import dashboard_page
from views import analytics_page
from views import reports_page
from views import users_page
from views import billing_page
from views import settings_page
from views import workspace_page
from views import intel_hub_page
from views import creative_hub_page
from views import campaign_builder_view
from views import owner_panel_page
from views import social_command_page

try:
    from ai_engine.router import router
except Exception:
    router = None

try:
    from services.social_connector import social_hub
except Exception:
    social_hub = None

# ── INIT ──────────────────────────────────────────────────────────────────────
st.markdown(PREMIUM_CSS, unsafe_allow_html=True)
init_database()
create_default_admin()
init_session()

# ── LOGIN SCREEN ──────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("""
    <style>
        section[data-testid="stSidebar"] {display: none !important;}
        .block-container {padding-top: 0 !important; max-width: 100vw !important;
                          padding-left: 0 !important; padding-right: 0 !important;}
    </style>
    """, unsafe_allow_html=True)

    hero_img = "https://images.unsplash.com/photo-1639762681485-074b7f938ba0?w=1200&q=80"
    left_col, right_col = st.columns([1.3, 1], gap="small")

    # ── LEFT HERO PANEL ───────────────────────────────────────────────────────
    with left_col:
        feature_items = [
            ("🤖", t("تحليل ذكي بـ Gemini 2.0 + Groq + GPT-4o", "Smart Analysis: Gemini 2.0 + Groq + GPT-4o")),
            ("📊", t("تحليلات لحظية وتنبؤات بالذكاء الاصطناعي", "Real-time analytics & AI predictions")),
            ("🎬", t("إنتاج محتوى لـ TikTok & Instagram & YouTube", "Content for TikTok, Instagram & YouTube")),
            ("🆓", t("خطة مجانية متاحة — لا حاجة لبطاقة ائتمان", "Free plan available — no credit card needed")),
        ]
        feat_html = ""
        for icon, text in feature_items:
            feat_html += (
                '<div style="display:flex;align-items:center;gap:12px;color:#e2e8f0;margin-bottom:12px;">'
                '<div style="min-width:36px;height:36px;border-radius:10px;background:rgba(139,92,246,0.2);'
                'display:flex;align-items:center;justify-content:center;font-size:1.1rem;'
                'border:1px solid rgba(139,92,246,0.3);">' + icon + '</div>'
                '<span style="font-size:0.95rem;">' + text + '</span>'
                '</div>'
            )

        headline1 = t("نظام إدارة", "Sovereign Campaign")
        headline2 = t("الحملات الذكية", "Intelligence Platform")
        desc_txt  = t(
            "أقوى محرك لتحليل البيانات وإدارة الحملات السيادية. تحكم بالمحتوى، تصدر التريند.",
            "The most powerful AI-driven engine for data analysis. Dominate trends and shape outcomes."
        )
        badge_txt = t("MTSE DIGITAL SOVEREIGNTY v12", "MTSE DIGITAL SOVEREIGNTY v12")

        st.markdown(
            '<div style="height:100vh;'
            'background:linear-gradient(rgba(3,7,18,0.55),rgba(3,7,18,0.92)),'
            'url(' + hero_img + ') center/cover no-repeat;'
            'border-radius:0 48px 48px 0;display:flex;flex-direction:column;'
            'justify-content:center;padding:70px 60px;'
            'box-shadow:12px 0 40px rgba(0,0,0,0.6);position:relative;">'
            '<div style="background:rgba(255,255,255,0.08);padding:8px 22px;border-radius:30px;'
            'display:inline-block;width:fit-content;margin-bottom:28px;'
            'border:1px solid rgba(255,255,255,0.18);backdrop-filter:blur(12px);">'
            '<span style="color:' + PRIMARY_LIGHT + ';font-weight:700;font-size:0.88rem;letter-spacing:1.5px;">'
            '🌌 ' + badge_txt + '</span></div>'
            '<h1 style="font-size:3.6rem;color:white;margin-bottom:22px;'
            'line-height:1.08;font-weight:900;">'
            + headline1 + '<br>'
            '<span style="background:linear-gradient(90deg,' + PRIMARY_LIGHT + ',' + ACCENT + ');'
            '-webkit-background-clip:text;-webkit-text-fill-color:transparent;">'
            + headline2 + '</span></h1>'
            '<p style="font-size:1.1rem;color:#cbd5e1;max-width:88%;line-height:1.75;margin-bottom:36px;">'
            + desc_txt + '</p>'
            + feat_html +
            '</div>',
            unsafe_allow_html=True
        )

    # ── RIGHT AUTH PANEL ───────────────────────────────────────────────────────
    with right_col:
        st.markdown("<div style='height:5vh;'></div>", unsafe_allow_html=True)

        welcome_title = t("مرحباً بك مجدداً", "Welcome Back")
        welcome_sub   = t("الولوج للمنظومة الذكية", "Sign in to the sovereign system")

        st.markdown(
            '<div style="text-align:center;margin-bottom:24px;">'
            '<div style="font-size:2.6rem;margin-bottom:10px;filter:drop-shadow(0 0 12px ' + PRIMARY + '88);">🔐</div>'
            '<h2 style="font-size:2rem;color:' + PRIMARY_LIGHT + ';margin-bottom:6px;font-weight:900;">'
            + welcome_title + '</h2>'
            '<p style="color:#9ca3af;font-size:1rem;">' + welcome_sub + '</p>'
            '</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns([0.08, 1, 0.08])
        with c2:
            tab_login, tab_signup = st.tabs([
                t("🔑  تسجيل الدخول", "🔑  Sign In"),
                t("🆕  إنشاء حساب جديد", "🆕  Create Account"),
            ])

            # ── LOGIN TAB ──────────────────────────────────────────────────────
            with tab_login:
                st.markdown('<div class="glass-card animate-in" style="padding:28px;margin-top:12px;">', unsafe_allow_html=True)
                with st.form("login_form"):
                    username = st.text_input(t("📛  اسم المستخدم", "📛  Username"), placeholder="admin")
                    password = st.text_input(t("🔒  كلمة المرور", "🔒  Password"), type="password", placeholder="••••••••")
                    st.markdown("")
                    submitted = st.form_submit_button(
                        "➔  " + t("تسجيل الدخول", "Sign In"),
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
                                st.error(t("❌ بيانات الدخول غير صحيحة", "❌ Invalid credentials"))
                st.markdown("</div>", unsafe_allow_html=True)

                free_note = t(
                    "🆓 الخطة المجانية متاحة الآن — 3 تقارير شهرياً بدون بطاقة ائتمان!",
                    "🆓 Free plan now available — 3 reports/month, no credit card!"
                )
                st.markdown(
                    '<div style="background:linear-gradient(135deg,rgba(16,185,129,0.1),rgba(6,182,212,0.1));'
                    'border:1px solid rgba(16,185,129,0.25);border-radius:14px;padding:12px 18px;'
                    'text-align:center;margin-top:14px;">'
                    '<span style="color:' + SUCCESS + ';font-size:0.88rem;font-weight:700;">' + free_note + '</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

            # ── SIGNUP TAB ─────────────────────────────────────────────────────
            with tab_signup:
                st.markdown('<div class="glass-card animate-in" style="padding:28px;margin-top:12px;">', unsafe_allow_html=True)

                free_plan_note  = t("الخطة المجانية (Explorer)", "Free Plan (Explorer)")
                free_plan_desc  = t("3 تقارير + 3 رفع شهرياً، مجاناً تماماً", "3 reports + 3 uploads/month, free")
                st.markdown(
                    '<div style="background:linear-gradient(135deg,rgba(16,185,129,0.12),rgba(6,182,212,0.08));'
                    'border:1px solid rgba(16,185,129,0.3);border-radius:12px;padding:12px 16px;'
                    'margin-bottom:20px;text-align:center;">'
                    '<b style="color:' + SUCCESS + ';">🆓 ' + free_plan_note + '</b> '
                    '<span style="color:#94a3b8;font-size:0.88rem;">— ' + free_plan_desc + '</span>'
                    '</div>',
                    unsafe_allow_html=True
                )

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
                            type="password", placeholder="••••••••"
                        )
                    with col_p2:
                        confirm_pass = st.text_input(
                            t("🔒  تأكيد كلمة المرور", "🔒  Confirm Password"),
                            type="password", placeholder="••••••••"
                        )

                    # Password strength indicator — Python 3.11 safe
                    if new_pass:
                        strength = 0
                        if len(new_pass) >= 8: strength += 1
                        if any(c.isupper() for c in new_pass): strength += 1
                        if any(c.isdigit() for c in new_pass): strength += 1
                        if any(c in "!@#$%^&*" for c in new_pass): strength += 1

                        _pw_colors = ["#ef4444", "#f59e0b", "#eab308", "#10b981"]
                        _pw_labels = [
                            t("ضعيف جداً", "Very Weak"),
                            t("ضعيف", "Weak"),
                            t("متوسط", "Medium"),
                            t("قوي", "Strong"),
                        ]
                        _pw_col = _pw_colors[strength - 1]
                        _pw_bars = ""
                        for _i in range(4):
                            _bg = _pw_col if _i < strength else "rgba(255,255,255,0.08)"
                            _pw_bars += '<div style="flex:1;height:5px;border-radius:4px;background:' + _bg + '"></div>'

                        st.markdown(
                            '<div style="margin:6px 0 12px;">'
                            '<div style="display:flex;gap:4px;margin-bottom:4px;">'
                            + _pw_bars +
                            '</div><small style="color:' + _pw_col + ';font-weight:700;">'
                            + _pw_labels[strength - 1] +
                            '</small></div>',
                            unsafe_allow_html=True
                        )

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
                                st.error("❌ " + err)
                        else:
                            from auth import hash_password
                            from database import create_user
                            if create_user(new_user.strip(), hash_password(new_pass), "Viewer", "Explorer"):
                                st.success(t(
                                    "✅ مرحباً بك! تم إنشاء حسابك المجاني. سجّل دخولك الآن.",
                                    "✅ Welcome! Free account created. Sign in now."
                                ))
                            else:
                                st.error(t("❌ اسم المستخدم مسجل مسبقاً", "❌ Username already taken"))

                st.markdown("</div>", unsafe_allow_html=True)

        footer_txt = t("جميع الحقوق السيادية محفوظة", "All Sovereign Rights Reserved")
        st.markdown(
            '<div style="text-align:center;color:#374151;margin-top:40px;font-size:0.82rem;">'
            'MTSE Digital Sovereignty Engine v12.0<br><br>'
            + footer_txt + ' © 2026</div>',
            unsafe_allow_html=True
        )

    st.stop()

# ── MAIN APP (After Login) ─────────────────────────────────────────────────────
badge_icon, badge_label, badge_color = PLAN_BADGES.get(
    st.session_state.plan, ("💎", st.session_state.plan, PRIMARY)
)

with st.sidebar:
    # Logo & Branding
    st.markdown(
        '<div style="text-align:center;padding:18px 0 12px;">'
        '<div style="font-size:2.8rem;filter:drop-shadow(0 0 14px ' + PRIMARY + '88);margin-bottom:6px;">🌌</div>'
        '<h3 style="margin:2px 0 1px;color:' + PRIMARY_LIGHT + ';font-weight:900;letter-spacing:0.5px;">MTSE v12</h3>'
        '<p style="color:' + ACCENT + ';font-size:0.75rem;margin:0;font-weight:700;letter-spacing:2px;text-transform:uppercase;">'
        + t("السيادة الرقمية", "DIGITAL SOVEREIGNTY") + '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # User chip
    st.markdown(
        '<div style="background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.07);'
        'border-radius:14px;padding:12px 16px;margin-bottom:14px;text-align:center;">'
        '<div style="font-size:1.4rem;margin-bottom:4px;">👤</div>'
        '<div style="font-weight:700;color:#f1f5f9;font-size:0.95rem;">' + st.session_state.username + '</div>'
        '<div style="display:inline-block;background:rgba(16,185,129,0.12);color:' + badge_color + ';'
        'border-radius:20px;padding:2px 12px;font-size:0.75rem;font-weight:700;margin-top:4px;'
        'border:1px solid ' + badge_color + '44;">' + badge_icon + ' ' + badge_label + '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    nav_label = t("استكشاف المحاور", "NAVIGATION")
    st.markdown(
        '<p style="color:#4b5563;font-size:0.72rem;font-weight:700;letter-spacing:1.5px;'
        'text-transform:uppercase;padding:0 4px;margin-bottom:8px;">' + nav_label + '</p>',
        unsafe_allow_html=True
    )

    nav_items = [
        ("Dashboard",           "🏠", t("نظرة عامة",         "Overview")),
        ("Strategy Hub",        "🌐", t("محور الاستراتيجية", "Strategy Hub")),
        ("Campaign Hub",        "🚀", t("مركز الحملات",      "Campaign Hub")),
        ("Creative Studio",     "🎭", t("استوديو الإبداع",   "Creative Studio")),
        ("Real-time Analytics", "📊", t("التحليلات اللحظية", "Live Analytics")),
        ("Workspace",           "🏢", t("مساحة العمل",       "Workspace")),
        ("Billing",             "💳", t("الاشتراك والفواتير", "Billing")),
    ]

    if st.session_state.username == ADMIN_DEFAULT_USERNAME:
        nav_items.insert(0, ("Owner Panel", "👑", t("لوحة المالك", "Owner Panel")))

    for page_id, icon, label in nav_items:
        is_active = st.session_state.page == page_id
        if st.button(
            icon + "  " + label,
            use_container_width=True,
            key="nav_" + page_id,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = page_id
            st.rerun()

    st.markdown("---")

    # Language toggle
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

    if st.button("🔴  " + t("تسجيل الخروج", "Sign Out"), use_container_width=True):
        logout_user()
        st.rerun()

# ── PAGE ROUTING ──────────────────────────────────────────────────────────────
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
    "Billing":              billing_page,
}

target_module = page_map.get(page, dashboard_page)
try:
    target_module.render()
except Exception as e:
    import traceback
    st.error(t(
        "حدث خطأ تقني في هذه الصفحة. يرجى المحاولة مجدداً.",
        "A technical error occurred on this page. Please try again."
    ))
    with st.expander(t("تفاصيل المطور", "Developer Details")):
        st.code(traceback.format_exc(), language="python")
