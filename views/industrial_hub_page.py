# ==========================================================
# MTSE Marketing Engine - Industrial Hub (BOQ & Blueprints)
# Consolidates: Cost Engine, Technical Intel (Blueprints)
# ==========================================================

import streamlit as st
import pandas as pd
from utils import t, render_section_header
from ai_engine.cost_engine import get_cost_engine
from ai_engine.multimodal_processor import get_processor
from billing.plans import PlanManager
from database import get_user_branding
from utils import generate_branded_pdf

def render():
    """Render the Consolidated Industrial Hub."""
    
    pm = PlanManager(st.session_state.plan)

    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(30, 41, 59, 0.1) 100%); border-bottom: 4px solid #10b981;">
        <h1>💰 {t("مركز المقايسات والهندسة", "Industrial & Engineering Hub")}</h1>
        <p style="color:#94a3b8;">{t("حلل المخططات الهندسية، استخرج الكميات، وقم بتسعير المقايسات آلياً.", "Analyze blueprints, extract quantities, and price BOQs automatically.")}</p>
    </div>
    """, unsafe_allow_html=True)

    tab_blueprint, tab_pricing = st.tabs([
        f"📐 {t('استخبارات المخططات', 'Blueprint Intel')}",
        f"💰 {t('محرك التكاليف', 'Cost Engine')}"
    ])

    # --- TAB 1: BLUEPRINT INTEL ---
    with tab_blueprint:
        if st.session_state.plan != "Command":
             st.warning(t("ميزة حصرية لخطة Command.", "Command plan exclusive."))
        else:
            render_section_header(t("تحليل الرسوم الفنية", "Technical Drawing Analysis"), "🏗️")
            b_file = st.file_uploader(t("رفع مخطط (Image/PDF)", "Upload Blueprint"), type=["png", "jpg", "pdf"], key="hub_b_file")
            if b_file and st.button(t("تشغيل التحليل الهندسي", "Run Engineering Analysis"), use_container_width=True):
                with st.spinner(t("تحليل...", "Analyzing...")):
                    processor = get_processor()
                    st.session_state.hub_b_res = processor.analyze_technical_drawing(b_file.getvalue())
            
            if st.session_state.get("hub_b_res"):
                st.markdown(f'<div class="glass-card">{st.session_state.hub_b_res}</div>', unsafe_allow_html=True)
                if st.button(t("💰 إرسال للمقايسة", "Send to BOQ"), use_container_width=True):
                    st.info("Data Sent to Cost Engine Tab.")

    # --- TAB 2: COST ENGINE ---
    with tab_pricing:
        render_section_header(t("تقدير التكاليف", "Cost Estimation"), "💵")
        boq_input = st.text_area(t("نص المقايسة", "BOQ Text"), key="hub_boq_input")
        if st.button(t("🔍 استخراج وتسعير", "Extract & Price"), use_container_width=True):
            with st.spinner(t("جاري التسعير...", "Pricing...")):
                engine = get_cost_engine()
                st.session_state.hub_boq_res = engine.extract_boq_items(boq_input)
        
        if st.session_state.get("hub_boq_res"):
            df = pd.DataFrame(st.session_state.hub_boq_res)
            st.dataframe(df, use_container_width=True)
            st.success(t("المقايسة جاهزة للتصدير", "BOQ ready for export"))
