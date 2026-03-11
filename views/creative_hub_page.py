# ==========================================================
# MTSE Marketing Engine - Creative War Room
# Consolidates: Creative Studio, Campaign Orchestrator, AI Engine
# ==========================================================

import streamlit as st
from utils import t, render_section_header
from config import BORDER_GLOW
from ai_engine.campaign_orchestrator import get_orchestrator
from ai_engine.campaign_generator import generate_campaign_ideas, render_preview_html, get_social_preview_css
from ai_engine.viral_analyzer import analyze_virality, rewrite_for_virality
from billing.plans import PlanManager

def render():
    """Render the Consolidated Creative Hub."""
    
    pm = PlanManager(st.session_state.plan)

    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(135deg, rgba(109, 40, 217, 0.1) 0%, rgba(6, 182, 212, 0.1) 100%); border-bottom: 4px solid #8b5cf6;">
        <h1>🎭 {t("غرفة الحرب الإبداعية", "Creative War Room")}</h1>
        <p style="color:#94a3b8;">{t("صمم استراتيجيتك، ولّد محتواك، وحلّل مدى انتشاره في مكان واحد.", "Orchestrate strategy, generate content, and analyze virality in one place.")}</p>
    </div>
    """, unsafe_allow_html=True)

    tab_orch, tab_studio, tab_viral = st.tabs([
        f"🧠 {t('الأوركسترا الاستراتيجية', 'Strategy Orchestrator')}",
        f"🎨 {t('ستوديو الإنتاج', 'Production Studio')}",
        f"🔥 {t('مختبر الانتشار', 'Virality Lab')}"
    ])

    # --- TAB 1: STRATEGY ORCHESTRATOR ---
    with tab_orch:
        render_section_header(t("بناء الحملات المتكاملة", "Multi-Channel Campaign Builder"), "🧠")
        with st.expander(t("📋 إعدادات الحملة", "Campaign Setup"), expanded=True):
            p_desc = st.text_area(t("وصف المنتج/الخدمة", "Product Description"), key="hub_orch_desc")
            t_aud = st.text_input(t("الجمهور المستهدف", "Target Audience"), key="hub_orch_aud")
            if st.button(t("🚀 توليد الاستراتيجية", "Generate Strategy"), use_container_width=True):
                with st.spinner(t("جاري التخطيط...", "Planning...")):
                    orch = get_orchestrator()
                    st.session_state.hub_orch_res = orch.orchestrate(p_desc, t_aud, "Brand Awareness", "1000$")
        
        if st.session_state.get("hub_orch_res"):
            res = st.session_state.hub_orch_res
            st.success(f"Strategy: {res['campaign_name']}")
            st.markdown(f"**Roadmap:** {res['overall_roadmap']}")

    # --- TAB 2: PRODUCTION STUDIO ---
    with tab_studio:
        st.markdown(get_social_preview_css(), unsafe_allow_html=True)
        col_inp, col_out = st.columns([1, 1.2])
        with col_inp:
            render_section_header(t("توليد المحتوى", "Content Gen"), "✍️")
            prod_name = st.text_input(t("المنتج", "Product"), key="hub_prod_name")
            if st.button(t("✨ توليد نصوص وأفكار", "Generate Copy"), use_container_width=True):
                with st.spinner(t("تحليق الأفكار...", "Brainstorming...")):
                    st.session_state.hub_copy_res = generate_campaign_ideas(prod_name, "General", "Meta")
        
        with col_out:
            if st.session_state.get("hub_copy_res"):
                for i, var in enumerate(st.session_state.hub_copy_res[:2]):
                    st.markdown(render_preview_html(var, username=prod_name), unsafe_allow_html=True)

    # --- TAB 3: VIRALITY LAB ---
    with tab_viral:
        if not pm.can_access_viral_analyzer():
            st.warning(t("متاح في خطة Strategist.", "Requires Strategist plan."))
        else:
            render_section_header(t("تحليل وتحسين المحتوى", "Analyze & Optimize"), "🔥")
            v_text = st.text_area(t("نص المنشور", "Post Text"), key="hub_v_text")
            c1, c2 = st.columns(2)
            if c1.button(t("تحليل الانتشار", "Analyze"), use_container_width=True):
                res = analyze_virality(v_text, False)
                st.metric("Score", f"{res['score']}/100")
            if c2.button(t("تحسين ذكي", "AI Rewrite"), use_container_width=True):
                rewritten = rewrite_for_virality(v_text)
                for r in rewritten: st.code(r)
