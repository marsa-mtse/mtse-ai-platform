# ==========================================================
# MTSE Marketing Engine - Users Page (Admin)
# ==========================================================

import streamlit as st
import pandas as pd
from utils import t, render_section_header, render_empty_state, render_status_badge, validate_username, validate_password, validate_email
from database import (
    get_all_users, create_user, get_activity_log,
    add_lead, get_all_leads, update_lead_status,
    create_team, assign_user_to_company
)
from auth import hash_password, is_admin
from config import AVAILABLE_ROLES


def render():
    """Render the Users page."""

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>👥 {t("إدارة المستخدمين", "User Management")}</h2>
        <p style="color:#94a3b8;">{t("إدارة الحسابات والفريق والعملاء", "Manage accounts, teams, and leads")}</p>
    </div>
    """, unsafe_allow_html=True)

    if not is_admin():
        st.warning(t("هذه الصفحة متاحة للمشرفين فقط", "This page is for admins only"))
        _render_my_company()
        return

    tab1, tab2, tab3, tab4 = st.tabs([
        t("👥 المستخدمين", "👥 Users"),
        t("➕ إنشاء مستخدم", "➕ Create User"),
        t("🏢 الفرق", "🏢 Teams"),
        t("📇 العملاء (CRM)", "📇 CRM Leads")
    ])

    with tab1:
        _render_users_list()

    with tab2:
        _render_create_user()

    with tab3:
        _render_teams()

    with tab4:
        _render_crm()


def _render_users_list():
    """Display all users in a table."""
    render_section_header(t("جميع المستخدمين", "All Users"), "📋")

    users = get_all_users()

    if not users:
        render_empty_state(t("لا يوجد مستخدمين", "No users found"))
        return

    df = pd.DataFrame(users)
    df.columns = [
        t("اسم المستخدم", "Username"),
        t("الدور", "Role"),
        t("الخطة", "Plan"),
        t("الشركة", "Company"),
        t("حالة الاشتراك", "Billing Status")
    ]
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Activity Log
    render_section_header(t("سجل النشاط", "Activity Log"), "🕐")

    activities = get_activity_log(limit=20)
    if activities:
        act_df = pd.DataFrame(activities)
        act_df.columns = [
            t("المستخدم", "User"),
            t("الإجراء", "Action"),
            t("الوقت", "Time")
        ]
        st.dataframe(act_df, use_container_width=True, hide_index=True)
    else:
        st.info(t("لا يوجد نشاط بعد", "No activity yet"))


def _render_create_user():
    """Form to create a new user."""
    render_section_header(t("إنشاء مستخدم جديد", "Create New User"), "➕")

    with st.form("create_user_form", clear_on_submit=True):
        new_username = st.text_input(t("اسم المستخدم", "Username"))
        new_password = st.text_input(t("كلمة المرور", "Password"), type="password")
        new_plan = st.selectbox(t("الخطة", "Plan"), ["Starter", "Pro", "Business"])
        new_role = st.selectbox(t("الدور", "Role"), AVAILABLE_ROLES)

        submitted = st.form_submit_button(
            t("✅ إنشاء المستخدم", "✅ Create User"),
            use_container_width=True
        )

        if submitted:
            # Validate inputs
            valid_user, user_msg = validate_username(new_username)
            valid_pass, pass_msg = validate_password(new_password)

            if not valid_user:
                st.error(user_msg)
            elif not valid_pass:
                st.error(pass_msg)
            else:
                success = create_user(
                    new_username,
                    hash_password(new_password),
                    new_role,
                    new_plan
                )
                if success:
                    st.success(t("تم إنشاء المستخدم بنجاح ✅", "User Created Successfully ✅"))
                else:
                    st.error(t("اسم المستخدم موجود بالفعل", "Username already exists"))


def _render_teams():
    """Team management section."""
    render_section_header(t("إدارة الفرق", "Team Management"), "🏢")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"#### {t('إنشاء فريق', 'Create Team')}")
        company_name = st.text_input(
            t("اسم الشركة", "Company Name"),
            key="team_company"
        )
        if st.button(t("إنشاء فريق", "Create Team"), use_container_width=True):
            if company_name:
                create_team(company_name, st.session_state.username)
                st.success(t("تم إنشاء الفريق ✅", "Team Created ✅"))
            else:
                st.error(t("أدخل اسم الشركة", "Enter company name"))

    with col2:
        st.markdown(f"#### {t('تعيين مستخدم لشركة', 'Assign User to Company')}")
        assign_username = st.text_input(
            t("اسم المستخدم", "Username to Assign"),
            key="assign_user"
        )
        assign_company = st.text_input(
            t("اسم الشركة", "Company Name"),
            key="assign_company"
        )
        if st.button(t("تعيين", "Assign"), use_container_width=True):
            if assign_username and assign_company:
                assign_user_to_company(assign_username, assign_company)
                st.success(t("تم تعيين المستخدم ✅", "User Assigned ✅"))
            else:
                st.error(t("أدخل جميع البيانات", "Fill all fields"))


def _render_crm():
    """CRM leads management."""
    render_section_header(t("إدارة العملاء المحتملين", "CRM Leads"), "📇")

    with st.form("add_lead_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            lead_name = st.text_input(t("اسم العميل", "Lead Name"))
        with col2:
            lead_email = st.text_input(t("البريد الإلكتروني", "Email"))
        with col3:
            lead_company = st.text_input(t("الشركة", "Company"))

        submitted = st.form_submit_button(
            t("➕ إضافة عميل", "➕ Add Lead"),
            use_container_width=True
        )

        if submitted:
            if lead_name and lead_email:
                valid_email, email_msg = validate_email(lead_email)
                if valid_email:
                    add_lead(lead_name, lead_email, lead_company)
                    st.success(t("تم إضافة العميل ✅", "Lead Added ✅"))
                else:
                    st.error(email_msg)
            else:
                st.error(t("أدخل الاسم والبريد على الأقل", "Enter name and email at minimum"))

    # Display leads
    leads = get_all_leads()
    if leads:
        for lead in leads:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.write(f"**{lead['name']}**")
            with col2:
                st.write(lead['email'])
            with col3:
                st.write(lead.get('company', '—'))
            with col4:
                new_status = st.selectbox(
                    "Status",
                    ["New", "Contacted", "Qualified", "Lost"],
                    index=["New", "Contacted", "Qualified", "Lost"].index(lead.get('status', 'New')),
                    key=f"lead_status_{lead['id']}",
                    label_visibility="collapsed"
                )
                if new_status != lead.get('status'):
                    update_lead_status(lead['id'], new_status)
            st.markdown("---")
    else:
        render_empty_state(t("لا يوجد عملاء بعد", "No leads yet"), "📭")


def _render_my_company():
    """Show company info for non-admin users."""
    from database import get_user_company

    company = get_user_company(st.session_state.username)
    if company:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-size:2rem;">🏢</div>
            <div style="font-weight:600;">{t("حساب الشركة", "Company Account")}</div>
            <div class="kpi-value" style="font-size:1.3rem;">{company}</div>
        </div>
        """, unsafe_allow_html=True)
