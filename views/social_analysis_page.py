# ==========================================================
# MTSE Marketing Engine - Social Analysis Page
# ==========================================================

import streamlit as st
from utils import t, render_section_header
from ai_engine.social_sniper import get_social_sniper
from billing.plans import PlanManager
from database import get_user_branding
from utils import generate_branded_pdf

def render():
    """Render the Social Media Sniper page."""
    
    plan_manager = PlanManager(st.session_state.plan)
    
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; border-bottom: 4px solid #f472b6;">
        <h2>📊 {t("قناص السوشيال ميديا (Audit & Growth)", "Social Media Sniper: Audit & Growth")}</h2>
        <p style="color:#94a3b8;">{t("حلل أي حساب سوشيال ميديا واستخرج خارطة طريق للنمو.", "Analyze any social profile and extract a growth roadmap.")}</p>
    </div>
    """, unsafe_allow_html=True)

    if not plan_manager.can_access_integrations():
        st.warning(t("هذه الأداة الاحترافية متاحة لخطة Strategist فأعلى.", "This professional tool is for Strategist plan and higher."))
        return

    target_link = st.text_input(t("رابط الحساب (TikTok, FB, IG, YouTube)", "Profile Link (TikTok, FB, IG, YouTube)"), placeholder="https://...")
    profile_bio = st.text_area(t("نبذة عن الحساب (اختياري - يضمن دقة 100%)", "Profile Bio/Context (Optional - Ensures 100% accuracy)"), placeholder=t("مثلاً: صالون تجميل في القاهرة، متخصص في العناية بالبشرة...", "e.g., Beauty salon in Cairo, specializing in skincare..."), height=100)
    
    if st.button(t("🚀 ابدأ تحليل القناص", "🚀 Start Sniper Audit"), use_container_width=True):
        if target_link:
            with st.spinner(t("جاري تشريح الحساب استراتيجياً...", "Dissecting profile strategically...")):
                sniper = get_social_sniper()
                st.session_state.sniper_result = sniper.audit_profile(target_link, context=profile_bio)
                st.success(t("✅ تم التحليل بنجاح!", "✅ Audit completed!"))

    if st.session_state.get("sniper_result"):
        res = st.session_state.sniper_result
        if "error" in res:
            st.error(res["error"])
        else:
            render_section_header(t("التقرير الاستراتيجي الشامل", "Comprehensive Strategic Report"), "📢")
            
            st.markdown(f"""
            <div class="glass-card" style="border-right: 4px solid #f472b6;">
                <p><strong>{t('ملخص الأداء:', 'Performance Summary:')}</strong></p>
                {res.get('audit_summary')}
            </div>
            """, unsafe_allow_html=True)
            
            # SWOT
            c1, c2 = st.columns(2)
            swot = res.get("swot", {})
            with c1:
                st.success(f"💪 {t('نقاط القوة', 'Strengths')}")
                for s in swot.get("strengths", []): st.write(f"✅ {s}")
                st.info(f"💡 {t('الفرص', 'Opportunities')}")
                for o in swot.get("opportunities", []): st.write(f"✨ {o}")
            with c2:
                st.error(f"⚠️ {t('نقاط الضعف', 'Weaknesses')}")
                for w in swot.get("weaknesses", []): st.write(f"❌ {w}")
                st.warning(f"🛡️ {t('التهديدات', 'Threats')}")
                for th in swot.get("threats", []): st.write(f"🚩 {th}")
            
            # Content Roadmap
            st.markdown(f"### 🗺️ {t('خارطة طريق التطوير (Content Roadmap):', 'Growth Content Roadmap:')}")
            roadmap = res.get("content_roadmap", [])
            for stage in roadmap:
                with st.expander(f"📌 {stage.get('phase')}"):
                    st.write(f"**{t('الإجراء:', 'Action:')}** {stage.get('action')}")
                    st.write(f"**{t('الأثر المتوقع:', 'Expected Impact:')}** {stage.get('expected_impact')}")
            
            st.markdown("---")
            st.markdown(f"💡 **{t('تحسين التحويل (CTA Optimization):', 'CTA Optimization:')}** {res.get('cta_optimization')}")
            st.markdown(f"🔥 **{t('إمكانية التصدّر (Viral Potential):', 'Virality Score:')}** {res.get('viral_potential')}")

            st.markdown("---")
            
            # PDF Export
            if st.button(t("📄 تحميل التقرير الاستراتيجي (PDF)", "📄 Download Strategic Report (PDF)"), use_container_width=True):
                with st.spinner(t("جاري تجهيز التقرير بهوية شركتك...", "Preparing branded report...")):
                    brand = get_user_branding(st.session_state.username)
                    
                    pdf_report = {
                        "title": t("تقرير استخبارات التواصل الاجتماعي", "Social Media Intelligence Report"),
                        "sections": [
                            {
                                "heading": t("ملخص التدقيق", "Audit Summary"),
                                "content": res.get("audit_summary", "")
                            },
                            {
                                "heading": t("تحليل SWOT", "SWOT Analysis"),
                                "content": f"""◈ {t('نقاط القوة', 'Strengths')}: {', '.join(swot.get('strengths', []))}
◈ {t('نقاط الضعف', 'Weaknesses')}: {', '.join(swot.get('weaknesses', []))}
◈ {t('الفرص', 'Opportunities')}: {', '.join(swot.get('opportunities', []))}
◈ {t('التهديدات', 'Threats')}: {', '.join(swot.get('threats', []))}"""
                            }
                        ]
                    }
                    
                    # Roadmap
                    roadmap_txt = ""
                    for stage in res.get("content_roadmap", []):
                        roadmap_txt += f"➤ {stage.get('phase')}: {stage.get('action')}\n"
                    
                    pdf_report["sections"].append({
                        "heading": t("خارطة الطريق", "Content Roadmap"),
                        "content": roadmap_txt
                    })
                    
                    pdf_bytes = generate_branded_pdf(pdf_report, brand_data=brand)
                    if pdf_bytes:
                        st.download_button(
                            label=t("📥 اضغط للتحميل الآن", "📥 Click to Download Now"),
                            data=pdf_bytes,
                            file_name="mtse_social_audit.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ PDF generation failed.")

            if st.button(t("🗑️ مسح النتائج", "🗑️ Clear Results"), key="clear_sniper"):
                st.session_state.sniper_result = None
                st.rerun()
