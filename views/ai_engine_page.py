# ==========================================================
# MTSE Marketing Engine - AI Engine Page
# ==========================================================

import streamlit as st
import numpy as np
import pandas as pd
from utils import t, render_section_header, render_empty_state
from billing.plans import PlanManager

from ai_engine.campaign_generator import generate_campaign_ideas
from ai_engine.viral_analyzer import analyze_virality
from ai_engine.trend_predictor import predict_future_trends

def render():
    """Render the AI Engine page."""

    plan_manager = PlanManager(st.session_state.plan)

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>🤖 {t("محركات الذكاء الاصطناعي", "AI Engines")}</h2>
        <p style="color:#94a3b8;">{t("أدوات متقدمة لتوليد الحملات وتحليل الانتشار الفيروسي", "Advanced tools for campaigns and virality")}</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        t("📝 مولد الحملات", "📝 Campaign Gen"),
        t("🔥 مقياس الانتشار", "🔥 Viral Analyzer"),
        t("📈 التنبؤات", "📈 Trend Predictor"),
        t("🧠 تحليل استراتيجي", "🧠 Strategy Deep Dive"),
        t("💬 المساعد الذكي", "💬 AI Assistant")
    ])

    # ==============================
    # 📝 CAMPAIGN GENERATOR
    # ==============================
    with tab1:
        render_section_header(t("مولد الحملات الإعلانية", "AI Campaign Generator"), "📝")
        
        if not plan_manager.can_access_ai_generator():
            st.warning(t("هذه الميزة متاحة للمشتركين في خطة Pro فأعلى.", "This feature requires Pro plan or higher."))
        else:
            from ai_engine.campaign_generator import get_social_preview_css, render_preview_html
            st.markdown(get_social_preview_css(), unsafe_allow_html=True)
            
            with st.form("campaign_generator_form"):
                col1, col2 = st.columns(2)
                with col1:
                    product_name = st.text_input(t("اسم المنتج/الخدمة", "Product/Service Name"), placeholder="e.g. MTSE CRM")
                    platform = st.selectbox(t("المنصة", "Platform"), ["Meta (Facebook/Instagram)", "TikTok", "Google Search"])
                with col2:
                    audience = st.text_input(t("الجمهور المستهدف", "Target Audience"), placeholder="e.g. Marketing Managers")
                    tone = st.selectbox(t("نبرة الصوت", "Tone of Voice"), [t("احترافي", "Professional"), t("حماسي", "Exciting"), t("فكاهي", "Humorous")])
                
                submitted = st.form_submit_button(t("✨ توليد نصوص إعلانية", "✨ Generate Ad Copies"), use_container_width=True)
                
                if submitted and product_name and audience:
                    variations = generate_campaign_ideas(product_name, audience, platform)
                    st.success(t("تم توليد الحملات بنجاح!", "Campaigns generated successfully!"))
                    
                    for i, var in enumerate(variations):
                        col_text, col_prev = st.columns([3, 2])
                        with col_text:
                            st.markdown(f"""
                            <div class="glass-card" style="border-left:4px solid #6366f1; height: 100%;">
                                <h4 style="margin-top:0; color:#818cf8;">Variation #{i+1}</h4>
                                <p><strong>{t("العنوان:", "Headline:")}</strong> {var['headline']}</p>
                                <p><strong>{t("النص:", "Body:")}</strong> {var['primary_text']}</p>
                                <p><strong>{t("إجراء:", "CTA:")}</strong> {var['cta']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_prev:
                            st.markdown(render_preview_html(var, username=product_name if product_name else "MTSE"), unsafe_allow_html=True)
                elif submitted:
                    st.error(t("يرجى إدخال اسم المنتج والجمهور", "Please enter product name and audience"))

    # ==============================
    # 🔥 VIRAL ANALYZER
    # ==============================
    with tab2:
        render_section_header(t("مقياس الانتشار الفيروسي وتطوير المحتوى", "Virality Analyzer & Rewriter"), "🔥")
        
        if not plan_manager.can_access_viral_analyzer():
            st.warning(t("هذه الميزة الحصرية متاحة في خطة Business فقط.", "This exclusive feature is for Business plan only."))
        else:
            content_text = st.text_area(t("ألصق محتوى المنشور هنا", "Paste your post content here"), height=150)
            has_media = st.checkbox(t("يحتوي المنشور على صورة أو فيديو", "Post includes Image/Video"))
            
            c1, c2 = st.columns(2)
            with c1:
                analyze_btn = st.button(t("تحليل الانتشار", "Analyze Virality"), use_container_width=True)
            with c2:
                rewrite_btn = st.button(t("✨ تحسين المحتوى ذكياً", "✨ AI Rewrite for Virality"), use_container_width=True)
            
            if analyze_btn:
                if content_text:
                    result = analyze_virality(content_text, has_media)
                    score = result["score"]
                    color = "#10b981" if score >= 80 else "#f59e0b" if score >= 40 else "#ef4444"
                    
                    st.markdown(f"""
                    <div style="text-align:center; padding:20px;">
                        <div style="font-size:4rem; font-weight:800; color:{color};">{score}/100</div>
                        <div style="color:#94a3b8; font-size:1.2rem;">Virality Score</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("### 📋 التقرير والفيدباك")
                    for fb in result["feedback"]:
                        st.markdown(f"- {fb}")
                        
                    if result["is_viral_candidate"]:
                        st.balloons()
                else:
                    st.error(t("أدخل النص لتحليله", "Enter text to analyze"))
            
            if rewrite_btn:
                if content_text:
                    from ai_engine.viral_analyzer import rewrite_for_virality
                    rewritten = rewrite_for_virality(content_text)
                    st.success(t("تم تحسين المحتوى لتعظيم الانتشار! 🔥", "Content optimized for maximum virality! 🔥"))
                    
                    for i, rev in enumerate(rewritten):
                        st.markdown(f"""
                        <div class="glass-card" style="border-right:4px solid #10b981;">
                            <h4 style="margin-top:0; color:#10b981;">Suggested AI Version {i+1}</h4>
                            <p style="font-style: italic; color: #cbd5e1;">"{rev}"</p>
                            <button style="background:transparent; border:1px solid #10b981; color:#10b981; padding:4px 8px; border-radius:8px; cursor:pointer;" onclick="navigator.clipboard.writeText('{rev}')">📋 Copy to Clipboard</button>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(t("أدخل النص لتحسينه", "Enter text to rewrite"))

    # ==============================
    # 📈 TREND PREDICTOR
    # ==============================
    with tab3:
        render_section_header(t("التنبؤ بالاتجاهات (Trends)", "Trend Predictor"), "📈")
        
        if not plan_manager.can_access_trend_predictor():
            st.warning(t("ميزة التنبؤ بالاتجاهات متاحة لخطة Business.", "Trend prediction available on Business plan."))
        else:
            st.info(t("هذه الأداة تحلل بياناتك التاريخية لتوقع الأداء في الـ 30 يوم القادمة.", "This tool uses your historical data to predict the next 30 days."))
            df = st.session_state.get("analysis_df")
            if df is not None:
                numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                col_choice = st.selectbox(t("اختر المقياس للتنبؤ", "Select metric to predict"), numeric_cols)
                
                if st.button(t("تنبؤ المستقبل 🔮", "Predict Future 🔮")):
                    pred_result = predict_future_trends(df, col_choice)
                    if pred_result["status"] == "success":
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown(f"#### {t('اتجاه السوق:', 'Market Trend:')} <span style='color:#06b6d4;'>{pred_result['trend_type']}</span>", unsafe_allow_html=True)
                        with col2:
                            st.markdown(f"#### {t('معدل النمو:', 'Growth Rate:')} <span style='color:#10b981;'>{pred_result['growth_pct']}%</span>", unsafe_allow_html=True)
                        
                        import plotly.express as px
                        import plotly.graph_objects as go
                        
                        y_actual = df[col_choice].fillna(0).values
                        y_pred = pred_result["predictions"]
                        
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(y=y_actual, mode='lines', name=t('التاريخي (الفعلي)', 'Historical (Actual)')))
                        # Pad prediction with NaNs for historical period to connect the line visually
                        padded_pred = [np.nan] * (len(y_actual)-1) + [y_actual[-1]] + list(y_pred)
                        fig.add_trace(go.Scatter(y=padded_pred, mode='lines', line=dict(dash='dash', color='#f59e0b'), name=t('التنبؤ 30 يوم', '30-Day Predictor')))
                        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.error(pred_result["message"])
            else:
                st.warning(t("يرجى رفع ملف بيانات من صفحة التحليلات أولاً.", "Please upload dataset in Analytics page first."))

    # ==============================
    # 🧠 STRATEGY DEEP DIVE
    # ==============================
    with tab4:
        render_section_header(t("التحليل الاستراتيجي العميق", "AI Strategy Deep Dive"), "🧠")
        
        if not plan_manager.can_access_ai_generator():
            st.warning(t("هذه الميزة متاحة للمشتركين في خطة Business فقط.", "This feature requires Business plan."))
        else:
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid var(--primary);">
                <h4>{t("خارطة الطريق العالمية لمنتجك", "Global Product Roadmap")}</h4>
                <p style="color:#94a3b8;">{t("سيقوم الذكاء الاصطناعي بتحليل منتجك ووضع خطة توسع عالمية.", "AI will analyze your product and create a global expansion plan.")}</p>
            </div>
            """, unsafe_allow_html=True)
            
            p_name = st.text_input(t("اسم المنتج للتحليل العميق", "Product Name for Deep Dive"), key="deep_dive_name")
            if st.button(t("🚀 ابدأ التحليل الاستراتيجي", "🚀 Start Strategic Analysis"), use_container_width=True):
                if p_name:
                    with st.spinner(t("جاري تحليل الأسواق العالمية...", "Analyzing global markets...")):
                        import time
                        time.sleep(2)
                        st.balloons()
                        st.markdown(f"""
                        <div class="glass-card">
                            <h3 style="color:var(--accent);">🌍 {t("خطة التوسع لـ", "Expansion Plan for")} {p_name}</h3>
                            <hr style="border-color:rgba(255,255,255,0.1);">
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                                <div>
                                    <h5 style="color:var(--success);">✅ {t("الأسواق المستهدفة", "Target Markets")}</h5>
                                    <ul>
                                        <li>{t("دول الخليج (السعودية، الإمارات)", "GCC (KSA, UAE)")}</li>
                                        <li>{t("أوروبا الغربية", "Western Europe")}</li>
                                        <li>{t("شمال أمريكا", "North America")}</li>
                                    </ul>
                                </div>
                                <div>
                                    <h5 style="color:var(--primary-light);">🎯 {t("القنوات المقترحة", "Suggested Channels")}</h5>
                                    <ul>
                                        <li>LinkedIn Ads (B2B Focus)</li>
                                        <li>Google Search (High Intent)</li>
                                        <li>TikTok (Brand Awareness)</li>
                                    </ul>
                                </div>
                            </div>
                            <div style="margin-top:20px; padding:15px; background:rgba(99, 102, 241, 0.1); border-radius:12px;">
                                <strong>💡 {t("نصيحة الخبراء:", "Expert Tip:")}</strong> 
                                {t("ركز على توطين المحتوى (Localization) لكل سوق بشكل مستقل لضمان أعلى معدل تحويل.", 
                                   "Focus on content localization for each market independently to ensure the highest conversion rate.")}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error(t("يرجى إدخال اسم المنتج", "Please enter product name"))

    # ==============================
    # 💬 CHAT ASSISTANT
    # ==============================
    with tab5:
        render_section_header(t("المساعد الذكي للبيانات", "AI Chat Assistant"), "💬")
        
        # Simple integrated chat fallback
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        chat_input = st.text_input(t("اسألني عن حملاتك...", "Ask me about your campaigns..."))
        
        if chat_input:
            st.session_state.chat_history.append({"user": chat_input, "ai": "هذا رد تجريبي من المساعد الذكي. يمكنك دمج مفتاح OpenAI API للحصول على ردود فعلية من GPT-4." if st.session_state.lang == "AR" else "This is a simulated response. Link OpenAI API key for real GPT-4 answers."})
            
        for msg in st.session_state.chat_history[-5:]:
            st.markdown(f"""
            <div style="margin:8px 0;">
                <div class="glass-card" style="border-right:3px solid #6366f1; padding:12px 18px; margin:4px 0;">
                    <strong>👤 You:</strong> {msg['user']}
                </div>
                <div class="glass-card" style="border-right:3px solid #06b6d4; padding:12px 18px; margin:4px 0;">
                    <strong>🤖 AI:</strong> {msg['ai']}
                </div>
            </div>
            """, unsafe_allow_html=True)
