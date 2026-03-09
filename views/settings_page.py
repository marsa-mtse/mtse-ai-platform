# ==========================================================
# MTSE Marketing Engine - Settings Page
# ==========================================================

import streamlit as st
from utils import t, render_section_header, validate_password
from database import update_password, log_activity
from auth import hash_password, verify_password
from database import get_user


def render():
    """Render the Settings page."""

    username = st.session_state.username

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>⚙️ {t("الإعدادات", "Settings")}</h2>
        <p style="color:#94a3b8;">{t("إدارة حسابك وتخصيص المنصة", "Manage account and customize platform")}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        t("🔐 كلمة المرور", "🔐 Password"),
        t("🌐 اللغة", "🌐 Language"),
        t("🏷️ العلامة البيضاء", "🏷️ White Label"),
        t("🌍 الدومين", "🌍 Domain")
    ])

    # ==============================
    # CHANGE PASSWORD
    # ==============================

    with tab1:
        render_section_header(t("تغيير كلمة المرور", "Change Password"), "🔐")

        with st.form("change_password_form"):
            current_password = st.text_input(
                t("كلمة المرور الحالية", "Current Password"),
                type="password"
            )
            new_password = st.text_input(
                t("كلمة المرور الجديدة", "New Password"),
                type="password"
            )
            confirm_password = st.text_input(
                t("تأكيد كلمة المرور", "Confirm Password"),
                type="password"
            )

            submitted = st.form_submit_button(
                t("🔄 تحديث كلمة المرور", "🔄 Update Password"),
                use_container_width=True
            )

            if submitted:
                # Validate current password
                user = get_user(username)
                if not user or not verify_password(current_password, user["password"]):
                    st.error(t("كلمة المرور الحالية غير صحيحة", "Current password is incorrect"))
                elif new_password != confirm_password:
                    st.error(t("كلمة المرور الجديدة غير متطابقة", "New passwords don't match"))
                else:
                    valid, msg = validate_password(new_password)
                    if not valid:
                        st.error(msg)
                    else:
                        update_password(username, hash_password(new_password))
                        log_activity(username, "Changed password")
                        st.success(t("تم تحديث كلمة المرور بنجاح ✅", "Password updated successfully ✅"))

    # ==============================
    # LANGUAGE SETTINGS
    # ==============================

    with tab2:
        render_section_header(t("إعدادات اللغة", "Language Settings"), "🌐")

        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <p>{t("اللغة الحالية", "Current Language")}: <strong>{'العربية 🇪🇬' if st.session_state.lang == 'AR' else 'English 🇺🇸'}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🇪🇬 العربية", use_container_width=True, key="lang_ar"):
                st.session_state.lang = "AR"
                st.rerun()
        with col2:
            if st.button("🇺🇸 English", use_container_width=True, key="lang_en"):
                st.session_state.lang = "EN"
                st.rerun()

    # ==============================
    # WHITE LABEL
    # ==============================

    with tab3:
        render_section_header(t("وضع العلامة البيضاء", "White Label Mode"), "🏷️")

        if st.session_state.plan != "Business":
            st.warning(t(
                "هذه الميزة متاحة فقط لخطة Business",
                "This feature is only available for the Business plan"
            ))
        else:
            white_label_name = st.text_input(
                t("اسم العلامة التجارية", "Brand Name"),
                key="wl_name"
            )
            white_label_logo = st.file_uploader(
                t("رفع الشعار", "Upload Logo"),
                type=["png", "jpg", "jpeg"],
                key="wl_logo"
            )

            if white_label_name:
                st.markdown(f"""
                <div class="glass-card" style="text-align:center;">
                    <h2>{white_label_name}</h2>
                    <p style="color:#94a3b8;">{t("معاينة العلامة التجارية", "Brand Preview")}</p>
                </div>
                """, unsafe_allow_html=True)

            if white_label_logo:
                st.image(white_label_logo, width=150)

            if st.button(t("حفظ إعدادات العلامة", "Save Brand Settings"), use_container_width=True):
                st.session_state["white_label"] = {
                    "name": white_label_name,
                    "has_logo": white_label_logo is not None
                }
                st.success(t("تم الحفظ ✅ (وضع المحاكاة)", "Saved ✅ (Simulation Mode)"))

    # ==============================
    # CUSTOM DOMAIN
    # ==============================

    with tab4:
        render_section_header(t("إعدادات الدومين المخصص", "Custom Domain Settings"), "🌍")

        if st.session_state.plan != "Business":
            st.warning(t(
                "هذه الميزة متاحة فقط لخطة Business",
                "This feature is only available for the Business plan"
            ))
        else:
            custom_domain = st.text_input(
                t("الدومين المخصص", "Custom Domain"),
                placeholder="marketing.yourcompany.com",
                key="custom_domain"
            )

            if custom_domain:
                st.markdown(f"""
                <div class="glass-card">
                    <h4>🌍 DNS Configuration</h4>
                    <div style="font-family:monospace; background:#0f172a; padding:16px; border-radius:8px; margin:12px 0;">
                        <div style="color:#06b6d4;">CNAME {custom_domain}</div>
                        <div style="color:#94a3b8;">→ mtse-platform.streamlit.app</div>
                    </div>
                    <p style="color:#94a3b8; font-size:0.85rem;">{t("أضف هذا السجل في إعدادات DNS الخاصة بك", "Add this record in your DNS settings")}</p>
                </div>
                """, unsafe_allow_html=True)

            if st.button(t("ربط الدومين", "Link Domain"), use_container_width=True):
                if custom_domain:
                    st.success(t(
                        f"تم ربط {custom_domain} ✅ (وضع المحاكاة)",
                        f"Domain {custom_domain} linked ✅ (Simulation Mode)"
                    ))

    # ==============================
    # EMAIL CAMPAIGN SIMULATION
    # ==============================

    st.markdown("---")
    render_section_header(t("حملات البريد الإلكتروني", "Email Campaigns"), "📧")

    with st.form("email_campaign_form"):
        email_subject = st.text_input(t("الموضوع", "Subject"))
        email_body = st.text_area(t("محتوى الرسالة", "Email Content"), height=120)

        if st.form_submit_button(t("📧 إرسال الحملة (محاكاة)", "📧 Send Campaign (Simulation)"), use_container_width=True):
            if email_subject and email_body:
                log_activity(username, f"Email campaign simulated: {email_subject}")
                st.success(t("تم إرسال الحملة ✅ (وضع المحاكاة)", "Campaign sent ✅ (Simulation Mode)"))
            else:
                st.error(t("أدخل الموضوع والمحتوى", "Enter subject and content"))

    # ==============================
    # LOGOUT
    # ==============================

    st.markdown("---")
    if st.button(t("🚪 تسجيل الخروج", "🚪 Logout"), use_container_width=True, type="primary"):
        from auth import logout_user
        log_activity(username, "Logged out")
        logout_user()
        st.rerun()
