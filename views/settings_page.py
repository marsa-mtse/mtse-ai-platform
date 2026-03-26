# ==========================================================
# MTSE Marketing Engine - Settings Page
# ==========================================================

import streamlit as st
from utils import t, render_section_header, validate_password
from database import update_password, log_activity
from auth import hash_password, verify_password
from database import get_user, update_user_branding, get_user_branding, get_company_members, update_user_role, is_admin


def render():
    """Render the Settings page."""

    username = st.session_state.username

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>⚙️ {t("الإعدادات", "Settings")}</h2>
        <p style="color:#94a3b8;">{t("إدارة حسابك وتخصيص المنصة", "Manage account and customize platform")}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t("🔐 كلمة المرور", "🔐 Password"),
        t("🌐 اللغة", "🌐 Language"),
        t("🏷️ العلامة البيضاء", "🏷️ White Label"),
        t("🌍 الدومين", "🌍 Domain"),
        t("👥 الفريق", "👥 Team")
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

        if st.session_state.plan not in ["Command", "Business"]:
            st.warning(t(
                "هذه الميزة متاحة فقط لخطة Command فأعلى",
                "This feature is only available for the Command plan and above"
            ))
        else:
            # Load existing branding
            brand = get_user_branding(username) or {}
            
            white_label_name = st.text_input(
                t("اسم العلامة التجارية / الشركة", "Brand Name / Company"),
                value=brand.get("name", ""),
                key="wl_name"
            )
            
            # Color selector
            white_label_color = st.color_picker(
                t("لون السمة الرئيسي (Theme Color)", "Primary Theme Color"),
                value=brand.get("color", "#1a73e8"),
                key="wl_color"
            )

            white_label_logo = st.file_uploader(
                t("رفع شعار مخصص (Custom Logo)", "Upload Custom Logo"),
                type=["png", "jpg", "jpeg"],
                key="wl_logo"
            )

            # Preview
            col_pre1, col_pre2 = st.columns([1, 2])
            with col_pre1:
                if white_label_logo:
                    st.image(white_label_logo, width=120)
                elif brand.get("logo"):
                    import base64
                    st.image(f"data:image/png;base64,{brand['logo']}", width=120)
                else:
                    st.info(t("لا يوجد شعار", "No logo"))
            
            with col_pre2:
                st.markdown(f"""
                <div style="padding:10px; border-left: 5px solid {white_label_color}; background:rgba(255,255,255,0.05); border-radius:5px;">
                    <h4 style="margin:0; color:{white_label_color};">{white_label_name if white_label_name else "Brand Name"}</h4>
                    <p style="font-size:0.8rem; color:#94a3b8; margin:5px 0 0 0;">{t("معاينة شكل الترويسة في التقارير", "Report Header Preview")}</p>
                </div>
                """, unsafe_allow_html=True)

            if st.button(t("💾 حفظ كافّة إعدادات العلامة", "💾 Save All Brand Settings"), use_container_width=True):
                logo_b64 = brand.get("logo")
                if white_label_logo:
                    import base64
                    logo_b64 = base64.b64encode(white_label_logo.getvalue()).decode()
                
                update_user_branding(username, white_label_name, logo_b64, white_label_color)
                log_activity(username, f"Updated branding: {white_label_name}")
                st.success(t("تم حفظ إعدادات علامتك التجارية بنجاح! ✅", "Brand settings saved successfully! ✅"))
                st.rerun()

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
    # TEAM MANAGEMENT (RBAC)
    # ==============================

    with tab5:
        render_section_header(t("إدارة الفريق والوكالة", "Team & Agency Management"), "👥")
        
        user_info = get_user(username)
        company = user_info.get("company", t("مستقل", "Independent"))
        
        st.markdown(f"**{t('الشركة / الوكالة:', 'Company / Agency:')}** `{company}`")
        
        members = get_company_members(company)
        
        if not members:
            st.warning(t("لا توجد بيانات لأعضاء الفريق حالياً.", "No team members found for this company."))
        else:
            for member in members:
                col_m, col_r, col_a = st.columns([2, 1, 1])
                with col_m:
                    st.write(f"👤 **{member['username']}**")
                with col_r:
                    st.write(f"`{member['role']}`")
                with col_a:
                    if is_admin(username) and member['username'] != username:
                        new_role = st.selectbox(
                            t("تعديل الصلاحية", "Edit Role"),
                            ["Admin", "Editor", "Viewer"],
                            index=["Admin", "Editor", "Viewer"].index(member['role']),
                            key=f"role_{member['username']}"
                        )
                        if new_role != member['role']:
                            update_user_role(member['username'], new_role)
                            st.rerun()
                    else:
                        st.write("---")

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
