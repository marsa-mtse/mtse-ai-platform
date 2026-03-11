import streamlit as st
import pandas as pd
import random
from utils import t, render_section_header
from config import BORDER_GLOW

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(90deg, rgba(239, 68, 68, 0.05) 0%, rgba(30, 41, 59, 0.1) 100%); border-left: 4px solid #ef4444;">
        <h1 style="color:#f472b6;">⚔️ {t("الذكاء القتالي الاستراتيجي", "MTSE Combat AI")}</h1>
        <p style="color:#94a3b8;">{t("مراقبة المنافسين في الوقت الفعلي واقتناص الثغرات التسويقية", "Real-time competitor shadowing and tactical entry engine")}</p>
    </div>
    """, unsafe_allow_html=True)

    col_mon, col_stats = st.columns([1, 2])

    with col_mon:
        st.markdown(f"#### 🔍 {t('أهداف المراقبة', 'Shadowing Targets')}")
        target = st.text_input(t("رابط موقع/حساب منافس", "Competitor URL/Social Handle"), placeholder="e.g., competitor-brand.com")
        if st.button(t("📡 ابدأ التتبع الاستخباراتي", "Start Combat Shadowing"), use_container_width=True):
            with st.spinner(t("تحليل دفاعات المنافس...", "Analyzing competitor defenses...")):
                st.session_state.target_analyzed = target
                st.success(t("✅ تم اكتشاف ثغرات تكتيكية!", "Tactical gaps identified!"))

    with col_stats:
        render_section_header(t("تحليلات ساحة المعركة", "Battlefield Analytics"), "🛡️")
        cols = st.columns(3)
        cols[0].metric(t("قوة المنافس", "Competitor Strength"), "84/100", "-2", delta_color="inverse")
        cols[1].metric(t("حصة التفاعل", "Engagement Share"), "12%", "+1.5%")
        cols[2].metric(t("الثغرات المكتشفة", "Gaps Detected"), "7", "+2")

    st.markdown("---")

    tab1, tab2 = st.tabs([t("خارطة التحركات", "Movement Map"), t("الهجوم الاستراتيجي", "Strategic Counter")])

    with tab1:
        st.markdown(f"#### 🗺️ {t('آخر تحركات المنافسين', 'Recent Competitor Moves')}")
        moves = [
            {"Time": "2h ago", "Target": "Competitor A", "Move": "Launched Discount Campaign (15%)", "Impact": "Medium"},
            {"Time": "5h ago", "Target": "Competitor B", "Move": "Partnered with Tech Influencer", "Impact": "High"},
            {"Time": "1d ago", "Target": "Competitor A", "Move": "Abandoned 'Eco-Friendly' SEO Keywords", "Impact": "Opportunity!"}
        ]
        for move in moves:
            bg_color = "rgba(16, 185, 129, 0.1)" if "Opportunity" in move["Move"] else "rgba(255,255,255,0.05)"
            st.markdown(f"""
            <div class="glass-card" style="padding:10px; background:{bg_color}; margin-bottom:10px; border-radius:12px;">
                <span style="color:#94a3b8; font-size:0.8rem;">[{move['Time']}]</span> 
                <b>{move['Target']}</b>: {move['Move']} 
                <span class="status-badge" style="float:left; background:rgba(99, 102, 241, 0.1);">{move['Impact']}</span>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown(f"#### 🎯 {t('اقتراح رد الفعل التكتيكي', 'Tactical Counter Proposal')}")
        if 'target_analyzed' in st.session_state:
            st.markdown(f"""
            <div class="glass-card" style="border: 1px solid {BORDER_GLOW};">
                <h4 style="color:#fbbf24;">📍 {t("خطة الهجوم المقترحة", "Strategic Attack Plan")}</h4>
                <p>1. <b>Keyword Hijacking</b>: Focus on '{st.session_state.target_analyzed}' abandoned keywords immediately.</p>
                <p>2. <b>Social Blitz</b>: Launch a counter-offer specifically targeting '{st.session_state.target_analyzed}' audience sentiment.</p>
                <p>3. <b>Price War</b>: Match identified discount with a +2% value-add bundle.</p>
            </div>
            """, unsafe_allow_html=True)
            st.button(t("🚀 تنفيذ الهجوم عبر Social Command", "Execute Counter via Social Command"), type="primary", use_container_width=True)
        else:
            st.warning(t("يرجى إدخال هدف للمراقبة أولاً", "Please enter a target to generate a counter-strategy"))
