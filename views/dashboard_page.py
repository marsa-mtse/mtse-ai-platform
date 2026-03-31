# ==========================================================
# MTSE Marketing Engine v12 - Dashboard Page (Enhanced)
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from utils import t, render_kpi_card, render_usage_bar, render_section_header
from database import get_usage, get_user_reports, get_activity_log, reset_usage_if_new_month
from config import PLAN_LIMITS, PLAN_BADGES, PRIMARY, PRIMARY_LIGHT, ACCENT, SUCCESS, WARNING, DANGER
from auth import is_admin


def _get_greeting():
    """Time-based greeting."""
    hour = datetime.now().hour
    if hour < 12:
        return t("☀️ صباح الخير", "☀️ Good Morning")
    elif hour < 17:
        return t("🌤️ مساء النور", "🌤️ Good Afternoon")
    else:
        return t("🌙 مساء الخير", "🌙 Good Evening")


def render():
    """Render the enhanced Dashboard page."""

    username = st.session_state.username
    plan     = st.session_state.plan
    role     = st.session_state.role

    reset_usage_if_new_month(username)

    # ─────────────────────────────────────────────────────────────────────────
    # WELCOME HERO BANNER
    # ─────────────────────────────────────────────────────────────────────────
    badge_icon, badge_label, badge_color = PLAN_BADGES.get(plan, ("💎", plan, PRIMARY))
    greeting = _get_greeting()

    st.markdown(f"""
    <div class="glass-card animate-in" style="
        background: linear-gradient(135deg, rgba(139,92,246,0.12) 0%, rgba(6,182,212,0.08) 100%);
        border-bottom: 4px solid {PRIMARY};
        padding: 32px 36px;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 6px;
    ">
        <div>
            <p style="color:#94a3b8; font-size:1rem; margin:0 0 4px;">{greeting}</p>
            <h1 style="
                margin:0; font-size:2.2rem; font-weight:900;
                background: linear-gradient(135deg, {PRIMARY_LIGHT}, {ACCENT});
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">
                {username}! 👋
            </h1>
            <div style="margin-top:10px; display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                <span style="
                    background: rgba({','.join(str(int(badge_color.lstrip('#')[j:j+2],16)) for j in (0,2,4))}, 0.15);
                    color: {badge_color};
                    border:1px solid {badge_color}44;
                    border-radius:20px; padding:3px 14px;
                    font-size:0.82rem; font-weight:700;
                ">{badge_icon} {badge_label}</span>
                <span style="color:#64748b; font-size:0.85rem;">
                    {role} · {t("منصة MTSE v12", "MTSE v12 Platform")}
                </span>
            </div>
        </div>
        <div style="font-size:5rem; opacity:0.7; filter:drop-shadow(0 0 14px {PRIMARY}66);">🌌</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("")

    # ─────────────────────────────────────────────────────────────────────────
    # KPI CARDS — 4 COLUMNS
    # ─────────────────────────────────────────────────────────────────────────
    usage       = get_usage(username)
    limits      = PLAN_LIMITS.get(plan, PLAN_LIMITS["Explorer"])
    reports_used  = usage["reports_used"]
    uploads_used  = usage["uploads_used"]
    reports_limit = limits["reports"]
    uploads_limit = limits["uploads"]
    user_reports  = get_user_reports(username)
    total_reports = len(user_reports)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card(t("التقارير المنشأة", "Reports Created"), total_reports, "📄")
    with col2:
        pct_reports = int(reports_used / reports_limit * 100) if reports_limit else 0
        render_kpi_card(t("التقارير المستخدمة", "Reports Used"), f"{reports_used}/{reports_limit}", "📊")
    with col3:
        render_kpi_card(t("مرات الرفع", "Uploads Used"), f"{uploads_used}/{uploads_limit}", "📁")
    with col4:
        render_kpi_card(t("الخطة الحالية", "Current Plan"), f"{badge_icon} {plan}", "💎")

    st.markdown("")

    # ─────────────────────────────────────────────────────────────────────────
    # USAGE PROGRESS BARS  +  USAGE TREND CHART
    # ─────────────────────────────────────────────────────────────────────────
    col_usage, col_chart = st.columns([1, 2])

    with col_usage:
        render_section_header(t("استهلاك الخطة", "Plan Usage"), "📈")
        render_usage_bar(t("التقارير", "Reports"), reports_used, reports_limit)
        render_usage_bar(t("الرفع", "Uploads"), uploads_used, uploads_limit)

        # Quick upgrade prompt for free plan
        if plan == "Explorer":
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(6,182,212,0.08));
                border: 1px solid rgba(139,92,246,0.25);
                border-radius: 14px; padding: 14px 16px; margin-top:14px;
            ">
                <b style="color:{PRIMARY_LIGHT};">⚡ {t("ترقية الخطة", "Upgrade Your Plan")}</b>
                <p style="color:#94a3b8; font-size:0.85rem; margin:6px 0 0;">
                    {t("للوصول لجميع الأدوات وإمكانيات الذكاء الاصطناعي الكاملة.", "Get full access to all AI tools and unlimited reports.")}
                </p>
            </div>
            """, unsafe_allow_html=True)

    with col_chart:
        render_section_header(t("تحليلات الاستخدام", "Usage Analytics"), "📊")

        # Simulated weekly usage trend
        import numpy as np
        days   = [t(d, d) for d in ["السبت","الأحد","الاثنين","الثلاثاء","الأربعاء","الخميس","الجمعة"]]
        days_en = ["Sat","Sun","Mon","Tue","Wed","Thu","Fri"]
        labels  = days if st.session_state.get("lang","AR") == "AR" else days_en
        reports_trend = [0] * 6 + [reports_used] if reports_used <= 6 else [int(reports_used * i / 7) for i in range(1,8)]
        uploads_trend = [0] * 6 + [uploads_used] if uploads_used <= 6 else [int(uploads_used * i / 7) for i in range(1,8)]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=labels, y=reports_trend, mode="lines+markers",
            name=t("التقارير", "Reports"),
            line=dict(color=PRIMARY, width=3, shape="spline"),
            marker=dict(size=8, color=PRIMARY,
                        line=dict(color="white", width=2)),
            fill="tozeroy", fillcolor=f"rgba(139,92,246,0.1)"
        ))
        fig.add_trace(go.Scatter(
            x=labels, y=uploads_trend, mode="lines+markers",
            name=t("الرفع", "Uploads"),
            line=dict(color=ACCENT, width=3, shape="spline"),
            marker=dict(size=8, color=ACCENT,
                        line=dict(color="white", width=2)),
            fill="tozeroy", fillcolor=f"rgba(6,182,212,0.08)"
        ))
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            showlegend=True,
            legend=dict(font=dict(color="white"), bgcolor="rgba(0,0,0,0)"),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#64748b")),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#64748b"), rangemode="tozero"),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("")

    # ─────────────────────────────────────────────────────────────────────────
    # AI MARKETING ASSISTANT
    # ─────────────────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="glass-card animate-in" style="
        border-top: 4px solid {ACCENT};
        background: linear-gradient(135deg, rgba(6,182,212,0.08), rgba(30,41,59,0.5));
        display:flex; justify-content:space-between; align-items:center;
        margin-bottom:12px;
    ">
        <div>
            <h3 style="margin:0;">🤖 {t("المساعد التسويقي الذكي", "AI Marketing Assistant")}</h3>
            <p style="color:#94a3b8; margin:4px 0 0; font-size:0.9rem;">
                {t("رؤى مخصصة بناءً على أحدث بياناتك", "Personalized insights based on your latest data")}
            </p>
        </div>
        <div style="font-size:2.5rem; opacity:0.6;">🧠</div>
    </div>
    """, unsafe_allow_html=True)

    ai_col1, ai_col2 = st.columns([2, 1])

    with ai_col1:
        df = st.session_state.get("analysis_df")
        if df is not None:
            numeric_summary = df.describe().loc[["mean", "max"]].T
            top_metric = numeric_summary["mean"].idxmax() if not numeric_summary.empty else "N/A"
            st.markdown(f"""
            <div style="padding:14px 20px; color:#cbd5e1; line-height:1.65;">
                💡 <strong>{t("تحليل ذكي:", "AI Insight:")}</strong>
                {t(
                    f"بناءً على ملف البيانات المرفوع، نلاحظ أن '{top_metric}' هو المحرك الأساسي للأداء. ننصح بالتركيز على تحسين الاستهداف بناءً على هذا المؤشر.",
                    f"Based on your uploaded dataset, '{top_metric}' is the primary performance driver. We recommend refining audience targeting based on this metric."
                )}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info(t(
                "📁 قم برفع ملف بيانات في صفحة التحليلات للحصول على توصيات ذكية مخصصة لك.",
                "📁 Upload a dataset in Analytics to receive personalized AI marketing recommendations."
            ))

    with ai_col2:
        if st.button(
            "🎙️ " + t("موجز تكتيكي صوتي", "Voice Tactical Briefing"),
            use_container_width=True
        ):
            from utils import generate_voice_briefing
            briefing = generate_voice_briefing(f"Welcome back Commander {username}. Platform status: all systems nominal.")
            if briefing.get("status") == "success":
                st.audio(briefing["audio_url"])
                st.success("✨ " + briefing["message"])
            else:
                st.info(t("الميزة الصوتية تتطلب مفاتيح API.", "Voice feature requires API keys."))

    st.markdown("")

    # ─────────────────────────────────────────────────────────────────────────
    # PLATFORM QUICK ACTIONS
    # ─────────────────────────────────────────────────────────────────────────
    render_section_header(t("الإجراءات السريعة", "Quick Actions"), "⚡")

    act_cols = st.columns(4)
    quick_actions = [
        ("🚀", t("إنشاء حملة",    "New Campaign"),   "Campaign Hub"),
        ("🧠", t("تحليل رابط",    "Analyze URL"),    "Real-time Analytics"),
        ("🌍", t("استكشاف السوق", "Explore Market"), "Strategy Hub"),
        ("🎨", t("توليد محتوى",   "Generate Content"),"Creative Studio"),
    ]
    for i, (icon, label, page) in enumerate(quick_actions):
        with act_cols[i]:
            if st.button(f"{icon}\n{label}", use_container_width=True, key=f"quick_{page}"):
                st.session_state.page = page
                st.rerun()

    st.markdown("")

    # ─────────────────────────────────────────────────────────────────────────
    # RECENT ACTIVITY (Admin Only)
    # ─────────────────────────────────────────────────────────────────────────
    if is_admin():
        render_section_header(t("النشاط الأخير للمنصة", "Recent Platform Activity"), "🕐")
        activities = get_activity_log(limit=10)
        if activities:
            for act in activities:
                ts = str(act.get("timestamp",""))[:16]
                st.markdown(f"""
                <div class="glass-card" style="padding:11px 18px; margin:5px 0; display:flex; justify-content:space-between; align-items:center;">
                    <span>
                        <b style="color:{PRIMARY_LIGHT};">{act.get('username','')}</b>
                        <span style="color:#94a3b8;"> — {act.get('action','')}</span>
                    </span>
                    <span style="color:#4b5563; font-size:0.8rem;">{ts}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(t("لا يوجد نشاط بعد", "No activity yet"))
