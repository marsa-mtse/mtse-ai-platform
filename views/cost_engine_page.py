# ==========================================================
# MTSE Marketing Engine - Cost Engine Page
# ==========================================================

import streamlit as st
import pandas as pd
import io
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

    if not plan_manager.can_access_multimodal():
        st.info(t("💡 تلميح: ترقية خطتك تتيح معالجة ملفات PDF والصور مباشرة.", "💡 Tip: Upgrade your plan to enable direct PDF/Image processing."))

    # --- INPUT SECTION ---
    col1, col2 = st.columns([2, 1])
    with col1:
        boq_input = st.text_area(t("ألصق نص المقايسة أو حمل ملفاً", "Paste BOQ text or upload a file"), height=150)
    with col2:
        boq_file = st.file_uploader(t("رفع مقايسة (PDF/Excel)", "Upload BOQ (PDF/Excel)"), type=["pdf", "xlsx"])

    if st.button(t("🔍 استخراج البنود والكميات ذكياً", "🔍 Extract Items & Qty Smartly"), use_container_width=True):
        engine = get_cost_engine()
        with st.spinner(t("جاري معالجة البيانات واستخراج الجداول...", "Processing data and extracting tables...")):
            if boq_file:
                file_bytes = boq_file.getvalue()
                result = engine.extract_boq_from_file(file_bytes, boq_file.type)
                st.session_state.boq_items = result
                st.session_state.cost_calculation = None
                if result and "error" not in result[0]:
                    st.success(t("✅ تم استخراج البنود من الملف بنجاح!", "✅ Items extracted from file successfully!"))
                else:
                    st.error(f"❌ {result[0].get('error', 'خطأ غير معروف')}")
            elif boq_input:
                result = engine.extract_boq_items(boq_input)
                st.session_state.boq_items = result
                st.session_state.cost_calculation = None
                if result and "error" not in result[0]:
                    st.success(t("✅ تم استخراج البنود بنجاح!", "✅ Items extracted successfully!"))
                else:
                    st.error(f"❌ {result[0].get('error', 'خطأ غير معروف')}")
            else:
                st.warning(t("⚠️ يرجى إدخال نص المقايسة أو رفع ملف أولاً.", "⚠️ Please enter BOQ text or upload a file first."))

    if st.session_state.get("boq_items"):
        items = st.session_state.boq_items
        
        if isinstance(items, list) and len(items) > 0 and "error" in items[0]:
            st.error(f"❌ {items[0]['error']}")
            if st.button(t("🗑️ تصفير", "Clear"), key="clear_err"):
                st.session_state.boq_items = None
                st.rerun()
            return

        df = pd.DataFrame(items)
        
        required_cols = ['item', 'unit', 'quantity']
        if not all(col in df.columns for col in required_cols):
            st.error(t("❌ البيانات المستخرجة ليست بالشكل المطلوب.", "❌ Extracted data not in required format."))
            if st.button(t("🗑️ تصفير", "Clear"), key="clear_fmt"):
                st.session_state.boq_items = None
                st.rerun()
            return

        render_section_header(t("مرحلة التسعير والتقدير", "Pricing & Estimation Phase"), "🏗️")

        # --- AI MARKET PRICE SUGGESTION ---
        if st.button(t("🤖 اقتراح أسعار السوق بالذكاء الاصطناعي", "🤖 AI Market Price Suggestions"), use_container_width=True):
            engine = get_cost_engine()
            with st.spinner(t("جاري الاستعلام عن أسعار السوق...", "Fetching market prices...")):
                suggestions = engine.suggest_market_prices(items)
                if suggestions:
                    st.session_state.market_prices = suggestions
                    st.success(t("✅ تم جلب أسعار السوق المرجعية!", "✅ Market prices fetched!"))
                else:
                    st.warning(t("⚠️ لم نتمكن من جلب أسعار السوق. أدخل الأسعار يدوياً.", "⚠️ Could not fetch market prices. Enter manually."))

        # --- PRICING INPUTS ---
        st.markdown(t("### 📝 أدخل سعر الوحدة لكل بند:", "### 📝 Enter unit price for each item:"))
        market_prices = st.session_state.get("market_prices", {})
        base_prices = {}
        for i, row in df.iterrows():
            item_name = row.get('item', t('بند غير معروف', 'Unknown Item'))
            item_unit = row.get('unit', '-')
            item_qty = row.get('quantity', 0)
            suggested = market_prices.get(str(i), market_prices.get(item_name, 0.0))
            
            c1, c2, c3, c4 = st.columns([3, 1, 1, 2])
            c1.write(f"**{item_name}** ({item_unit})")
            c2.write(f"Qty: {item_qty}")
            if suggested:
                c3.markdown(f"<small style='color:#10b981'>~{suggested:.0f}</small>", unsafe_allow_html=True)
            base_prices[str(i)] = c4.number_input(
                f"Price", min_value=0.0, value=float(suggested or 0.0),
                step=1.0, key=f"price_{i}", label_visibility="collapsed"
            )

        st.markdown("---")
        
        # --- COST FACTORS ---
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
            
            # --- SUMMARY CARDS ---
            st.markdown(f"""
            <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin-bottom:20px;">
                <div class="glass-card" style="border-top: 4px solid #6366f1;">
                    <small>{t("إجمالي التكلفة المباشرة", "Total Direct Cost")}</small>
                    <h3>{calc['summary']['total_direct']:,.2f}</h3>
                </div>
                <div class="glass-card" style="border-top: 4px solid #f59e0b;">
                    <small>{t("إجمالي شامل الهالك", "Total with Waste")}</small>
                    <h3>{calc['summary']['total_with_waste']:,.2f}</h3>
                </div>
                <div class="glass-card" style="border-top: 4px solid #10b981;">
                    <small>{t("السعر النهائي للمشروع", "Final Project Price")}</small>
                    <h2 style="color:#10b981;">{calc['summary']['total_grand']:,.2f}</h2>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.dataframe(res_df, use_container_width=True)
            
            # --- PIE CHART ---
            try:
                import plotly.express as px
                chart_df = res_df[res_df['direct_total'] > 0].copy()
                if not chart_df.empty:
                    fig = px.pie(
                        chart_df, values='final_price', names='item',
                        title=t("توزيع تكاليف المشروع", "Project Cost Distribution"),
                        color_discrete_sequence=px.colors.sequential.Teal
                    )
                    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                    st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass

            # --- EXCEL EXPORT ---
            st.markdown(f"### 📥 {t('تصدير التقرير', 'Export Report')}")
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Sheet 1: Detailed items
                export_df = res_df.rename(columns={
                    'item': t('البند', 'Item'), 'qty': t('الكمية', 'Qty'),
                    'unit': t('الوحدة', 'Unit'), 'base_price': t('سعر الوحدة', 'Unit Price'),
                    'direct_total': t('التكلفة المباشرة', 'Direct Cost'),
                    'with_waste': t('شامل الهالك', 'With Waste'),
                    'with_overhead': t('شامل الغير مباشر', 'With Overhead'),
                    'final_price': t('السعر النهائي', 'Final Price')
                })
                export_df.to_excel(writer, sheet_name=t('تفاصيل البنود', 'Item Details'), index=False)
                # Sheet 2: Summary
                summary_df = pd.DataFrame([{
                    t('البيان', 'Description'): t('التكلفة المباشرة الإجمالية', 'Total Direct Cost'),
                    t('القيمة', 'Value'): calc['summary']['total_direct']
                }, {
                    t('البيان', 'Description'): t('إجمالي شامل الهالك', 'Total with Waste'),
                    t('القيمة', 'Value'): calc['summary']['total_with_waste']
                }, {
                    t('البيان', 'Description'): t('السعر النهائي للمشروع', 'Final Project Price'),
                    t('القيمة', 'Value'): calc['summary']['total_grand']
                }])
                summary_df.to_excel(writer, sheet_name=t('الملخص', 'Summary'), index=False)

            st.download_button(
                label=t("📥 تحميل تقرير Excel", "📥 Download Excel Report"),
                data=output.getvalue(),
                file_name="mtse_cost_estimate.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

            st.info(f"💡 **{t('تحليل المخاطر:', 'Risk Insight:')}** " + 
                    t("بناءً على التضخم الحالي، يفضل إضافة نسبة 5% إضافية كمخزون للطوارئ.", 
                      "Based on current inflation, adding a 5% contingency buffer is recommended."))

            if st.button(t("🗑️ تصفير البيانات", "🗑️ Reset Data")):
                st.session_state.boq_items = None
                st.session_state.cost_calculation = None
                st.session_state.market_prices = None
                st.rerun()

def render():
    """Render the Cost Engine page."""
    
    plan_manager = PlanManager(st.session_state.plan)
    
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; border-bottom: 4px solid #10b981;">
        <h2>💰 {t("محرك مقايسات الأسعار والتكاليف", "Industrial Cost & Pricing Engine")}</h2>
        <p style="color:#94a3b8;">{t("استخرج البنود وحلل التكاليف مباشرة من مقايسات المشاريع.", "Extract items and analyze costs directly from project BOQs.")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Show a warning for lower plans but don't block entirely
    if not plan_manager.can_access_multimodal():
        st.info(t("💡 تلميح: ترقية خطتك تتيح معالجة ملفات PDF والصور مباشرة.", "💡 Tip: Upgrade your plan to enable direct PDF/Image processing."))

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
                file_bytes = boq_file.getvalue()
                result = engine.extract_boq_from_file(file_bytes, boq_file.type)
                st.session_state.boq_items = result
                if result and "error" not in result[0]:
                    st.success(t("✅ تم استخراج البنود من الملف بنجاح!", "✅ Items extracted from file successfully!"))
                else:
                    st.error(f"❌ {result[0].get('error', 'خطأ غير معروف')}")
            elif boq_input:
                result = engine.extract_boq_items(boq_input)
                st.session_state.boq_items = result
                if result and "error" not in result[0]:
                    st.success(t("✅ تم استخراج البنود بنجاح!", "✅ Items extracted successfully!"))
                else:
                    st.error(f"❌ {result[0].get('error', 'خطأ غير معروف')}")
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
