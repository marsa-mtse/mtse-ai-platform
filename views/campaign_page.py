# ==========================================================
# MTSE Marketing Engine - Campaign Orchestrator Page
# ==========================================================
import streamlit as st
from utils import t, render_section_header, generate_branded_pdf
from ai_engine.campaign_orchestrator import get_orchestrator
from database import get_user_branding, log_activity

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; border-bottom: 4px solid #6366f1;">
        <h2>🧠 {t("مايسترو الحملات التسويقية", "Campaign Orchestrator")}</h2>
        <p style="color:#94a3b8;">{t("ابنِ استراتيجية تسويقية متكاملة من الألف إلى الياء", "Build a complete multichannel marketing strategy from scratch")}</p>
    </div>
    """, unsafe_allow_html=True)

    if "campaign_result" not in st.session_state:
        st.session_state.campaign_result = None

    # INPUT WIZARD
    with st.expander(t("📋 إعدادات الحملة الجديدة", "📋 New Campaign Setup"), expanded=not st.session_state.campaign_result):
        product_desc = st.text_area(t("ماذا تبيع؟ (المنتج/الخدمة)", "What are you selling? (Product/Service)"), placeholder=t("مثال: قهوة مختصة، تطبيق توصيل، دورات برمجة...", "e.g., Specialty coffee, delivery app, coding courses..."))
        target_audience = st.text_input(t("من هو جمهورك؟", "Who is your audience?"), placeholder=t("مثال: الشباب من 18-25 المهتمين بالتكنولوجيا", "e.g., Tech-savvy youth aged 18-25"))
        
        col1, col2 = st.columns(2)
        with col1:
            goal = st.selectbox(t("الهدف الرئيسي", "Primary Goal"), [
                t("زيادة الوعي بالعلامة التجارية", "Brand Awareness"),
                t("زيادة المبيعات / التحويلات", "Sales / Conversions"),
                t("جذب عملاء محتملين", "Lead Generation"),
                t("زيادة التفاعل", "Engagement")
            ])
        with col2:
            budget = st.text_input(t("الميزانية التقريبية (اختياري)", "Approximate Budget (Optional)"), placeholder="1000$")

        if st.button(t("🚀 توليد الاستراتيجية المتكاملة", "🚀 Generate Full Strategy"), use_container_width=True, type="primary"):
            if not product_desc or not target_audience:
                st.error(t("يرجى ملء البيانات الأساسية", "Please fill in the basic details"))
            else:
                with st.spinner(t("🧠 المايسترو يفكّر الآن...", "🧠 Orchestrator is thinking...")):
                    try:
                        orch = get_orchestrator()
                        res = orch.orchestrate(product_desc, target_audience, goal, budget)
                        if "error" in res:
                            st.error(f"Error: {res['error']}")
                        else:
                            st.session_state.campaign_result = res
                            log_activity(st.session_state.username, f"Orchestrated campaign: {res['campaign_name']}")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

    # RESULTS DASHBOARD
    if st.session_state.campaign_result:
        res = st.session_state.campaign_result
        
        st.markdown(f"### 🎯 {res['campaign_name']}")
        st.info(f"👥 **{t('الجمهور المستهدف:', 'Target Audience:')}** {res['target_audience']}")

        # Funnel Tabs
        tab_strategy, tab_content, tab_creative, tab_budget = st.tabs([
            t("🗺️ الاستراتيجية", "🗺️ Strategy"),
            t("✍️ المحتوى", "✍️ Content"),
            t("🎨 العينات البصرية", "🎨 Creative Prompts"),
            t("💰 الميزانية", "💰 Budget")
        ])

        with tab_strategy:
            render_section_header(t("قمع المبيعات (Sales Funnel)", "Sales Funnel"), "🌪️")
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.markdown(f"**{t('1. الوعي (Awareness)', '1. Awareness')}**\n\n{res['funnel_strategy']['awareness']}")
            with col_b:
                st.markdown(f"**{t('2. الاهتمام (Consideration)', '2. Consideration')}**\n\n{res['funnel_strategy']['consideration']}")
            with col_c:
                st.markdown(f"**{t('3. التحويل (Conversion)', '3. Conversion')}**\n\n{res['funnel_strategy']['conversion']}")
            
            st.markdown("---")
            st.markdown(f"🗓️ **{t('خارطة الطريق:', 'Roadmap:')}**\n{res['overall_roadmap']}")

        with tab_content:
            render_section_header(t("محتوى المنصات", "Platform Content"), "📱")
            for post in res['platform_content']:
                with st.chat_message("assistant"):
                    st.write(f"**Platform: {post['platform']}**")
                    st.write(f"📌 **{post['headline']}**")
                    st.write(post['body'])
                    st.code(f"CTA: {post['call_to_action']}")

        with tab_creative:
            render_section_header(t("توليد التصاميم (AI prompts)", "Creative Prompts"), "✨")
            for art in res['visual_prompts']:
                with st.expander(f"🎨 {art['platform']} - {art['concept']}"):
                    st.write(f"**Concept:** {art['concept']}")
                    st.text_area(t("Prompt (للنسخ):", "Prompt (for copy):"), art['prompt'], height=100)
                    st.caption("Tip: Use this prompt in Midjourney or DALL-E for best results.")

        with tab_budget:
            render_section_header(t("توزيع الميزانية المقترح", "Suggested Budget"), "💵")
            for plat, alloc in res['suggested_budget_allocation'].items():
                st.write(f"• **{plat}:** {alloc}")

        st.markdown("---")
        # PDF EXPORT
        if st.button(t("📄 تصدير الاستراتيجية بالهوية التجارية (PDF)", "📄 Export Strategy with Branding (PDF)"), use_container_width=True):
            brand = get_user_branding(st.session_state.username)
            pdf_data = {
                "title": f"Campaign Strategy: {res['campaign_name']}",
                "sections": [
                    {"heading": "Strategy Overview", "content": res['overall_roadmap']},
                    {"heading": "Funnel: Awareness", "content": res['funnel_strategy']['awareness']},
                    {"heading": "Funnel: Consideration", "content": res['funnel_strategy']['consideration']},
                    {"heading": "Funnel: Conversion", "content": res['funnel_strategy']['conversion']},
                ]
            }
            # Add dynamic content for PDF
            pdf_bytes = generate_branded_pdf(pdf_data, brand_data=brand)
            if pdf_bytes:
                st.download_button(t("📥 تحميل الاستراتيجية", "📥 Download Strategy"), pdf_bytes, "campaign_strategy.pdf", "application/pdf", use_container_width=True)

        if st.button(t("🔄 بناء حملة جديدة", "🔄 Build New Campaign"), use_container_width=True):
            st.session_state.campaign_result = None
            st.rerun()
