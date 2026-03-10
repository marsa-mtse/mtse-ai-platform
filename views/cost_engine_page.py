# ==========================================================
# MTSE Marketing Engine - Cost Engine Page
# ==========================================================

import streamlit as st
import pandas as pd
from utils import t, render_section_header
from ai_engine.cost_engine import get_cost_engine
from billing.plans import PlanManager

def render():
    """Render the Cost Engine page."""
    
    plan_manager = PlanManager(st.session_state.plan)
    
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; border-bottom: 4px solid #10b981;">
        <h2>💰 {t("محرك مقايسات الأسعار والتكاليف", "Industrial Cost & Pricing Engine")}</h2>
        <p style="color:#94a3b8;">{t("استخرج البنود وحلل التكاليف مباشرة من مقايسات المشاريع.", "Extract items and analyze costs directly from project BOQs.")}</p>
    </div>
    """, unsafe_allow_html=True)

    if not plan_manager.can_access_multimodal(): # Placeholder flag for Cost Engine
        st.warning(t("هذه الميزة الهندسية والمالية متاحة لخطة Strategist فأعلى.", "This Engineering/Financial tool is for Strategist plan and higher."))
        return

    # --- ARCHIVE/FILE SELECTION ---
    col1, col2 = st.columns([2, 1])
    with col1:
        boq_input = st.text_area(t("ألصق نص المقايسة أو حمل ملفاً", "Paste BOQ text or upload a file"), height=150)
    with col2:
        boq_file = st.file_uploader(t("رفع مقايسة (PDF/Excel)", "Upload BOQ (PDF/Excel)"), type=["pdf", "xlsx"])

    if st.button(t("🔍 استخراج البنود والكميات ذكياً", "🔍 Extract Items & Qty Smartly"), use_container_width=True):
        if boq_input:
            with st.spinner(t("جاري معالجة البيانات واستخراج الجداول...", "Processing data and extracting tables...")):
                engine = get_cost_engine()
                st.session_state.boq_items = engine.extract_boq_items(boq_input)
                st.success(t("✅ تم استخراج البنود بنجاح!", "✅ Items extracted successfully!"))

    if st.session_state.get("boq_items"):
        items = st.session_state.boq_items
        df = pd.DataFrame(items)
        
        render_section_header(t("مرحلة التسعير والتقدير", "Pricing & Estimation Phase"), "🏗️")
        
        # User dynamic pricing input
        st.markdown(t("### 📝 أدخل سعر الوحدة لكل بند:", "### 📝 Enter unit price for each item:"))
        base_prices = {}
        for i, row in df.iterrows():
            c1, c2, c3 = st.columns([3, 1, 2])
            c1.write(f"**{row['item']}** ({row['unit']})")
            c2.write(f"Qty: {row['quantity']}")
            base_prices[str(i)] = c3.number_input(f"Unit Price for {row['item']}", min_value=0.0, step=1.0, key=f"price_{i}")

        st.markdown("---")
        
        # Scenario Factors
        with st.expander(t("⚙️ إعدادات نسب التكاليف الإضافية", "⚙️ Cost Factor Settings"), expanded=False):
            sc1, sc2, sc3 = st.columns(3)
            waste_pct = sc1.slider(t("نسبة الهالك %", "Waste %"), 0, 20, 5) / 100
            overhead_pct = sc2.slider(t("المصاريف غير المباشرة %", "Overhead %"), 0, 30, 15) / 100
            profit_pct = sc3.slider(t("نسبة الربح %", "Profit %"), 0, 50, 20) / 100

        if st.button(t("📊 حساب المقايسة النهائية", "📊 Calculate Final Project Cost"), use_container_width=True):
            engine = get_cost_engine()
            calculation = engine.calculate_cost_matrix(items, base_prices, overhead=overhead_pct, waste=waste_pct, profit=profit_pct)
            st.session_state.cost_calculation = calculation
            st.success(t("✅ تم الحساب!", "✅ Calculation complete!"))

        if st.session_state.get("cost_calculation"):
            calc = st.session_state.cost_calculation
            res_df = pd.DataFrame(calc["items"])
            
            st.markdown(f"""
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-bottom:20px;">
                <div class="glass-card" style="border-top: 4px solid #6366f1;">
                    <small>{t("إجمالي التكلفة المباشرة", "Total Direct Cost")}</small>
                    <h3>${calc['summary']['total_direct']:.2f}</h3>
                </div>
                <div class="glass-card" style="border-top: 4px solid #f59e0b;">
                    <small>{t("إجمالي شامل الهالك", "Total with Waste")}</small>
                    <h3>${calc['summary']['total_with_waste']:.2f}</h3>
                </div>
                <div class="glass-card" style="border-top: 4px solid #10b981;">
                    <small>{t("السعر النهائي للمشروع", "Final Project Price")}</small>
                    <h2 style="color:#10b981;">${calc['summary']['total_grand']:.2f}</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(res_df, use_container_width=True)
            
            # Risk/Insight
            st.info(f"💡 **{t('تحليل المخاطر:', 'Risk Insight:')}** " + 
                    t("بناءً على التضخم الحالي، يفضل إضافة نسبة 5% إضافية كمخزون للطوارئ.", 
                      "Based on current inflation, adding a 5% contingency buffer is recommended."))

            if st.button(t("🗑️ تصفير البيانات", "🗑️ Reset Data")):
                st.session_state.boq_items = None
                st.session_state.cost_calculation = None
                st.rerun()
