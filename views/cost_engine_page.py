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
        engine = get_cost_engine()
        with st.spinner(t("جاري معالجة البيانات واستخراج الجداول...", "Processing data and extracting tables...")):
            if boq_file:
                # Handle file upload
                file_bytes = boq_file.getvalue()
                st.session_state.boq_items = engine.extract_boq_from_file(file_bytes, boq_file.type)
                st.success(t("✅ تم استخراج البنود من الملف بنجاح!", "✅ Items extracted from file successfully!"))
            elif boq_input:
                # Handle text input
                st.session_state.boq_items = engine.extract_boq_items(boq_input)
                st.success(t("✅ تم استخراج البنود من النص بنجاح!", "✅ Items extracted from text successfully!"))
            else:
                st.warning(t("⚠️ يرجى إدخال نص المقايسة أو رفع ملف أولاً.", "⚠️ Please enter BOQ text or upload a file first."))

    if st.session_state.get("boq_items"):
        items = st.session_state.boq_items
        
        # Check if the result is an error message
        if isinstance(items, list) and len(items) > 0 and "error" in items[0]:
            st.error(f"❌ {items[0]['error']}")
            if st.button(t("🗑️ تصفير", "Clear")):
                st.session_state.boq_items = None
                st.rerun()
            return

        df = pd.DataFrame(items)
        
        # Basic validation of expected columns
        required_cols = ['item', 'unit', 'quantity']
        if not all(col in df.columns for col in required_cols):
             st.error(t("❌ البيانات المستخرجة ليست بالشكل المطلوب. يرجى المحاولة مرة أخرى أو استخدام نص المقايسة.", "❌ Extracted data is not in the required format. Please try again or use text input."))
             if st.button(t("🗑️ تصفير", "Clear")):
                st.session_state.boq_items = None
                st.rerun()
             return

        render_section_header(t("مرحلة التسعير والتقدير", "Pricing & Estimation Phase"), "🏗️")
        
        # User dynamic pricing input
        st.markdown(t("### 📝 أدخل سعر الوحدة لكل بند:", "### 📝 Enter unit price for each item:"))
        base_prices = {}
        for i, row in df.iterrows():
            item_name = row.get('item', t('بند غير معروف', 'Unknown Item'))
            item_unit = row.get('unit', '-')
            item_qty = row.get('quantity', 0)
            
            c1, c2, c3 = st.columns([3, 1, 2])
            c1.write(f"**{item_name}** ({item_unit})")
            c2.write(f"Qty: {item_qty}")
            base_prices[str(i)] = c3.number_input(f"Unit Price for {item_name}", min_value=0.0, step=1.0, key=f"price_{i}")

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
