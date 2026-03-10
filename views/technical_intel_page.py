# ==========================================================
# MTSE Engineering Intelligence - Blueprint Analysis Page
# ==========================================================

import streamlit as st
import pandas as pd
import json
from utils import t, render_section_header
from ai_engine.multimodal_processor import get_processor
from billing.plans import PlanManager

def render():
    """Render the Blueprint & Technical Drawing Intelligence page."""
    
    plan_manager = PlanManager(st.session_state.plan)
    
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; border-bottom: 4px solid #3b82f6;">
        <h2>📐 {t("استخبارات المخططات الهندسية", "Engineering Blueprint Intelligence")}</h2>
        <p style="color:#94a3b8;">{t("تحليل المخططات، استخراج القياسات، وتجهيز بنود المقايسة آلياً.", "Analyze blueprints, extract measurements, and auto-prepare BOQ items.")}</p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.plan != "Command":
         st.warning(t("هذه الميزة الهندسية المتقدمة حصرية لخطة Command.", "This advanced Engineering feature is exclusive to Command plan."))
         if st.button(t("🚀 ترقية الخطة الآن", "🚀 Upgrade Plan Now")):
             st.session_state.page = "Billing"
             st.rerun()
         return

    col1, col2 = st.columns([2, 1])
    
    with col1:
        blueprint_file = st.file_uploader(t("رفع مخطط هندسي (Image/PDF Drawing)", "Upload Blueprint (Image/PDF Drawing)"), type=["png", "jpg", "jpeg", "pdf"])
        tech_prompt = st.text_area(t("تعليمات إضافية للمهندس الاصطناعي", "Instructions for AI Engineer"), 
                                  placeholder=t("مثلاً: ركز على تمديدات السباكة، أو استخرج عدد الأعمدة...", "e.g. Focus on plumbing, or extract column count..."))
    
    with col2:
        st.info(t("💡 **نصيحة:** ارفع صور عالية الجودة لضمان دقة استخراج القياسات من الرسومات الفنية.", "💡 **Tip:** Upload high-res images for better measurement accuracy in technical drawings."))

    if blueprint_file and st.button(t("🧠 تشغيل التحليل الهندسي العميق", "🧠 Run Deep Engineering Analysis"), use_container_width=True):
        with st.spinner(t("جاري تشريح المخطط هندسياً...", "Dissecting blueprint structurally...")):
            processor = get_processor()
            result = processor.analyze_technical_drawing(blueprint_file.getvalue(), prompt=tech_prompt)
            st.session_state.tech_drawing_analysis = result
            st.success(t("✅ تم الانتهاء من التحليل الاستخباري!", "✅ Intelligence analysis complete!"))

    if st.session_state.get("tech_drawing_analysis"):
        analysis = st.session_state.tech_drawing_analysis
        
        render_section_header(t("الرؤى الهندسية والكميات", "Engineering Insights & Quantities"), "🏗️")
        
        st.markdown(f"""
        <div class="glass-card" style="border-right: 4px solid #3b82f6; padding: 25px;">
            {analysis}
        </div>
        """, unsafe_allow_html=True)
        
        # Action: Send to Cost Engine
        if st.button(t("💰 إرسال البنود المستخرجة إلى محرك التكاليف", "💰 Send Extracted Items to Cost Engine"), use_container_width=True):
            try:
                # Robust extraction: find the JSON list structure
                start = analysis.find("[")
                end = analysis.rfind("]")
                if start != -1 and end != -1:
                    raw_json = analysis[start:end+1]
                    items = json.loads(raw_json)
                    st.session_state.boq_items = items
                    st.success(t("✅ تم إرسال البيانات للمقايسة! انتقل لصفحة محرك التكاليف الآن.", "✅ Data sent to BOQ! Go to Cost Engine page now."))
                else:
                    st.error(t("❌ لم يتم العثور على جدول بيانات منظم في التحليل.", "❌ No structured data table found in analysis."))
            except Exception as e:
                 st.error(t(f"❌ فشل في استخراج البيانات المنظمة آلياً: {str(e)}", f"❌ Failed to auto-extract structured data: {str(e)}"))

        if st.button(t("🗑️ تصفير التحليل", "🗑️ Clear Analysis")):
            st.session_state.tech_drawing_analysis = None
            st.rerun()
