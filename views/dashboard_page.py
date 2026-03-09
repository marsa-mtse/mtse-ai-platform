# ==========================================================
# MTSE Marketing Engine - Dashboard Page
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import t, render_kpi_card, render_usage_bar, render_section_header
from database import get_usage, get_user_reports, get_activity_log, reset_usage_if_new_month
from config import PLAN_LIMITS
from auth import is_admin


def render():
    """Render the Dashboard page."""

    username = st.session_state.username
    plan = st.session_state.plan
    role = st.session_state.role

    # Reset usage if new month
    reset_usage_if_new_month(username)

    # ==============================
    # WELCOME HEADER
    # ==============================

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; padding:30px;">
        <h2 style="margin:0;">👋 {t("مرحباً", "Welcome")}, {username}!</h2>
        <p style="color:#94a3b8; margin-top:8px;">
            {t("الدور", "Role")}: <strong>{role}</strong> &nbsp;|&nbsp;
            {t("الخطة", "Plan")}: <strong>{plan}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ==============================
    # KPI CARDS
    # ==============================

    usage = get_usage(username)
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["Starter"])

    reports_used = usage["reports_used"]
    uploads_used = usage["uploads_used"]
    reports_limit = limits["reports"]
    uploads_limit = limits["uploads"]

    user_reports = get_user_reports(username)
    total_reports = len(user_reports)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card(
            t("التقارير المنشأة", "Reports Created"),
            total_reports, "📄"
        )

    with col2:
        render_kpi_card(
            t("التقارير المستخدمة", "Reports Used"),
            f"{reports_used}/{reports_limit}", "📊"
        )

    with col3:
        render_kpi_card(
            t("مرات الرفع", "Uploads Used"),
            f"{uploads_used}/{uploads_limit}", "📁"
        )

    with col4:
        render_kpi_card(
            t("الخطة الحالية", "Current Plan"),
            plan, "💎"
        )

    st.markdown("")

    # ==============================
    # USAGE PROGRESS BARS
    # ==============================

    render_section_header(t("استهلاك الخطة", "Plan Usage"), "📈")

    col1, col2 = st.columns(2)
    with col1:
        render_usage_bar(
            t("التقارير", "Reports"),
            reports_used, reports_limit
        )
    with col2:
        render_usage_bar(
            t("الرفع", "Uploads"),
            uploads_used, uploads_limit
        )

    st.markdown("")

    # ==============================
    # USAGE CHART
    # ==============================

    render_section_header(t("تحليلات الاستخدام", "Usage Analytics"), "📊")

    usage_data = pd.DataFrame({
        t("المقياس", "Metric"): [
            t("التقارير المستخدمة", "Reports Used"),
            t("مرات الرفع", "Uploads Used")
        ],
        t("القيمة", "Value"): [reports_used, uploads_used]
    })

    fig = px.bar(
        usage_data,
        x=t("المقياس", "Metric"),
        y=t("القيمة", "Value"),
        title=t("الاستخدام الحالي", "Current Usage"),
        color=t("المقياس", "Metric"),
        color_discrete_sequence=["#6366f1", "#06b6d4"]
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # ==============================
    # RECENT ACTIVITY (Admin)
    # ==============================

    if is_admin():
        render_section_header(t("النشاط الأخير", "Recent Activity"), "🕐")

        activities = get_activity_log(limit=10)
        if activities:
            for act in activities:
                st.markdown(f"""
                <div class="glass-card" style="padding:12px 20px; margin:6px 0;">
                    <strong>{act['username']}</strong> — {act['action']}
                    <span style="color:#94a3b8; float:left; font-size:0.8rem;">{act['timestamp'][:16]}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t("لا يوجد نشاط بعد", "No activity yet"))
