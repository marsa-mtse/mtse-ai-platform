# ==========================================================
# MTSE Marketing Engine - Video Intelligence Page
# ==========================================================
import streamlit as st
import os
import tempfile
from utils import t, render_section_header, generate_branded_pdf
from ai_engine.video_analyzer import get_video_analyzer
from database import get_user_branding, log_activity
from billing.plans import PlanManager

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>🎬 {t("استخبارات الفيديو الذكية", "AI Video Intelligence")}</h2>
        <p style="color:#94a3b8;">{t("حلل إعلاناتك وفيديوهاتك ثانية بثانية برؤية استراتيجية", "Analyze ads & videos second-by-second with strategic insights")}</p>
    </div>
    """, unsafe_allow_html=True)

    pm = PlanManager(st.session_state.get("plan", "Starter"))
    
    if st.session_state.plan not in ["Command", "Business"]:
        st.warning(t(
            "هذه الميزة متاحة فقط لخطة Command فأعلى (قوة Gemini 1.5 Pro)",
            "This feature is only available for Command plan and above (Powered by Gemini 1.5 Pro)"
        ))
        return

    uploaded_file = st.file_uploader(
        t("ارفع فيديو الإعلان (Reels, TikTok, Ad)", "Upload Marketing Video"),
        type=["mp4", "mov", "avi"]
    )

    if uploaded_file:
        st.video(uploaded_file)
        
        if st.button(t("🚀 ابدأ التحليل العميق", "🚀 Start Deep Analysis"), use_container_width=True, type="primary"):
            # Use temp file for Gemini Upload
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            try:
                analyzer = get_video_analyzer()
                res = analyzer.analyze_video(tmp_path)
                
                if "error" in res:
                    st.error(f"Error: {res['error']}")
                else:
                    st.session_state.video_result = res
                    log_activity(st.session_state.username, f"Analyzed video: {uploaded_file.name}")
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

    # Display Results
    if st.session_state.get("video_result"):
        res = st.session_state.video_result
        
        st.markdown("---")
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.metric(t("التقييم العام", "Overall Score"), f"{res['overall_score']}/100")
            st.info(f"🎯 **{t('قوة الـ Hook:', 'Hook Power:')}**\n{res['hook_effectiveness']}")
        
        with col2:
            st.success(f"🎬 **{t('سرعة المشاهد:', 'Visual Pacing:')}**\n{res['visual_pacing']}")
            st.warning(f"📝 **{t('جودة السيناريو:', 'Script Quality:')}**\n{res['script_quality']}")

        render_section_header(t("نقاط خطر التسرب (Retention Risks)", "Retention Risk Points"), "⚠️")
        for risk in res['retention_risk_points']:
            st.write(f"• {risk}")

        render_section_header(t("تحليل المشاهد (Timeline Insights)", "Timeline Insights"), "🎞️")
        for scene in res['scenes_analysis']:
            with st.expander(f"⏲️ {scene['timestamp']} - {scene['visual_description'][:30]}..."):
                st.write(f"**{t('وصف:', 'Visual:')}** {scene['visual_description']}")
                st.write(f"**{t('رؤية تسويقية:', 'Marketing Insight:')}** {scene['marketing_insight']}")
                st.write(f"**{t('مقترح تطوير:', 'Suggestion:')}** {scene['suggestion']}")

        st.markdown(f"""
        <div class="glass-card" style="border-top: 4px solid #10b981;">
            <h4>🏆 {t('خلاصة النجاح (Final Strategy)', 'Final Strategy')}</h4>
            <p>{res['final_recommendation']}</p>
        </div>
        """, unsafe_allow_html=True)

        # PDF Export
        if st.button(t("📄 تصدير تقرير تحليل الفيديو (Branded PDF)", "📄 Export Video Report (Branded PDF)"), use_container_width=True):
            brand = get_user_branding(st.session_state.username)
            pdf_data = {
                "title": t("تقرير تحليل الفيديو الاستراتيجي", "Strategic Video Intelligence Report"),
                "sections": [
                    {"heading": t("ملخص الأداء", "Performance Summary"), "content": f"Score: {res['overall_score']}/100\nHook: {res['hook_effectiveness']}\nPacing: {res['visual_pacing']}"},
                    {"heading": t("توصية النجاح", "Final Strategy"), "content": res['final_recommendation']}
                ]
            }
            # Add scene insights to PDF
            scenes_txt = ""
            for s in res['scenes_analysis']:
                scenes_txt += f"➤ {s['timestamp']}: {s['marketing_insight']}\n"
            pdf_data["sections"].append({"heading": t("تحليل التوقيتات", "Timeline Insights"), "content": scenes_txt})
            
            pdf_bytes = generate_branded_pdf(pdf_data, brand_data=brand)
            if pdf_bytes:
                st.download_button(t("📥 تحميل ملف PDF", "📥 Download PDF"), pdf_bytes, "video_report.pdf", "application/pdf", use_container_width=True)

        if st.button(t("🗑️ تحليل فيديو آخر", "🗑️ Analyze Another Video"), use_container_width=True):
            st.session_state.video_result = None
            st.rerun()
