import streamlit as st
from utils import t, render_section_header
from ai_engine.expert_tools import analyze_competitor_clash, analyze_sentiment_command
from ai_engine.universal_analyzer import format_expert_content
from billing.plans import PlanManager

def render():
    """Render the Expert Tools Command Center."""
    
    current_plan = st.session_state.plan
    pm = PlanManager(current_plan)
    
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>🛠️ {t("مركز أدوات النخبة", "Expert Tools Command Center")}</h2>
        <p style="color:#94a3b8;">{t("أدوات تحليلية متقدمة للتفوق على المنافسين", "Advanced analytical tools for market dominance")}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([
        f"⚔️ {t('ساحة معركة المنافسين', 'Competitor Battleground')}",
        f"🧠 {t('مركز قيادة المشاعر', 'Sentiment Command')}"
    ])

    with tab1:
        if not pm.can_access_competitor_battleground():
            st.warning(t("هذه الأداة متاحة لمشتركي باقة Strategist فما فوق.", "This tool is available for Strategist and Command subscribers."))
            if st.button(t("ترقية الحساب الآن", "Upgrade Now"), key="up_battle"):
                st.session_state.page = "Billing"
                st.rerun()
        else:
            render_section_header(t("مقارنة العمالقة", "Titan Comparison"), "⚔️")
            col_a, col_b = st.columns(2)
            with col_a:
                url1 = st.text_input(t("رابط المنافس الأول", "Competitor 1 URL"), placeholder="https://site-a.com")
            with col_b:
                url2 = st.text_input(t("رابط المنافس الثاني", "Competitor 2 URL"), placeholder="https://site-b.com")
            
            if st.button(t("إطلاق هجوم التحليل", "Launch Clash Analysis"), use_container_width=True):
                if url1 and url2:
                    with st.spinner(t("جاري تحليل ساحة المعركة...", "Analyzing the battleground...")):
                        result = analyze_competitor_clash(url1, url2)
                        
                        st.markdown("---")
                        c1, c2 = st.columns(2)
                        with c1:
                            st.info(f"🏆 {t('قوة المنافس الأول', 'Comp 1 Strengths')}")
                            st.write(format_expert_content(result.get("entity_1_strengths", [])))
                        with c2:
                            st.success(f"🏆 {t('قوة المنافس الثاني', 'Comp 2 Strengths')}")
                            st.write(format_expert_content(result.get("entity_2_strengths", [])))
                        
                        st.markdown(f"""
                        <div class="glass-card" style="border-left: 5px solid #6366f1;">
                            <h4>🎯 {t("فجوة السوق الاستراتيجية", "Strategic Market Gap")}</h4>
                            <p>{result.get('strategic_gap', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown(f"### 🔮 {t('توقعات مسار المعركة', 'Battleground Forecast')}")
                        st.write(result.get("battleground_forecast", ""))
                else:
                    st.error(t("يرجى إدخال الرابطين للمقارنة.", "Please enter both URLs to compare."))

    with tab2:
        if not pm.can_access_sentiment_command():
            st.warning(t("هذه الأداة متاحة حصرياً لمشتركي باقة Command (القيادة العليا).", "This tool is exclusive to Command (Ultimate) subscribers."))
            if st.button(t("ترقية الحساب الآن", "Upgrade Now"), key="up_sentiment"):
                st.session_state.page = "Billing"
                st.rerun()
        else:
            render_section_header(t("مسبار المشاعر العام", "Public Sentiment Probe"), "🧠")
            s_url = st.text_input(t("الرابط المراد تحليله", "Target URL for Sentiment"), placeholder="https://news-or-social.com")
            
            if st.button(t("تحليل النبض النفسي", "Analyze Psych Pulse"), use_container_width=True):
                if s_url:
                    with st.spinner(t("جاري استقراء المشاعر...", "Inducing sentiment...")):
                        s_res = analyze_sentiment_command(s_url)
                        
                        m1, m2, m3 = st.columns(3)
                        m1.metric(t("المزاج العام", "Overall Mood"), s_res.get("overall_mood", "Neutral"))
                        m2.metric(t("سرعة التغير", "Velocity"), s_res.get("emotional_velocity", "Stable"))
                        
                        st.markdown(f"#### 🌐 {t('إدراك الجمهور', 'Audience Perception')}")
                        st.write(format_expert_content(s_res.get("audience_perception", [])))
                else:
                    st.error(t("يرجى إدخال رابط للتحليل.", "Please enter a URL to analyze."))
