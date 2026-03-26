# ==========================================================
# MTSE v13 - Competitor Intelligence Hub
# Analyze competitors using AI + web analysis
# ==========================================================

import streamlit as st
from utils import t

def analyze_competitor_with_ai(brand_name: str, industry: str, lang: str) -> str:
    """Use AI Gateway to analyze a competitor brand and generate insights."""
    from ai_engine.ai_gateway import structured_text_generation
    
    system_prompt = """You are an expert marketing strategist and competitive intelligence analyst.
    Analyze the given competitor brand and provide comprehensive, actionable insights.
    Structure your response with clear sections: Brand Overview, Strengths, Weaknesses, Market Position, 
    Content Strategy, Pricing Strategy, Target Audience, Top Products/Services, and Strategic Recommendations.
    Be specific, data-driven, and actionable. If responding in Arabic, use professional marketing Arabic."""
    
    user_prompt = f"""
    Analyze the competitor: {brand_name}
    Industry: {industry}
    Response language: {"Arabic" if lang == "AR" else "English"}
    
    Provide a comprehensive competitive intelligence report including:
    1. Brand Overview & Market Position
    2. Key Strengths
    3. Key Weaknesses & Vulnerabilities  
    4. Content & Marketing Strategy Analysis
    5. Pricing Strategy
    6. Target Audience Profile
    7. Top Products/Services
    8. Differentiation Opportunities for my brand
    9. Tactical Recommendations to Outperform
    """
    
    result = structured_text_generation(system_prompt, user_prompt, preferred_provider="openai")
    return result if result else "Error: All models failed to generate response."


def render():
    from config import PRIMARY, PRIMARY_LIGHT, ACCENT

    st.markdown(f"""
    <div class="tool-header animate-in">
        <div class="tool-header-icon">🕵️</div>
        <h2>{t("استخبارات المنافسين", "Competitor Intelligence Hub")}</h2>
        <p style="color:#94a3b8;">{t("تحليل عميق للمنافسين واستراتيجياتهم بقوة GPT-4o", "Deep competitor analysis powered by GPT-4o")}</p>
        <span class="badge badge-primary">GPT-4o · Strategic Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

    col_input, col_results = st.columns([1, 1.4])

    with col_input:
        st.markdown(f"### 🎯 {t('بيانات التحليل', 'Analysis Input')}")

        competitor_name = st.text_input(
            t("اسم المنافس / العلامة التجارية", "Competitor Name / Brand"),
            placeholder=t("مثال: Nike، Samsung، Noon.com", "e.g: Nike, Samsung, Noon.com"),
            key="comp_name"
        )

        my_brand = st.text_input(
            t("علامتك التجارية (اختياري للمقارنة)", "Your Brand (optional for comparison)"),
            placeholder=t("اسم علامتك التجارية", "Your brand name"),
            key="my_brand"
        )

        industry = st.selectbox(
            t("القطاع / الصناعة", "Industry / Sector"),
            [
                t("التجزئة والتجارة الإلكترونية", "Retail & E-commerce"),
                t("التكنولوجيا والبرمجيات", "Technology & Software"),
                t("الغذاء والمشروبات", "Food & Beverages"),
                t("الأزياء والموضة", "Fashion & Apparel"),
                t("الرعاية الصحية", "Healthcare"),
                t("العقارات", "Real Estate"),
                t("الخدمات المالية", "Financial Services"),
                t("التعليم", "Education"),
                t("السفر والسياحة", "Travel & Tourism"),
                t("الترفيه والإعلام", "Entertainment & Media"),
                t("آخر", "Other"),
            ],
            key="comp_industry"
        )

        analysis_depth = st.radio(
            t("عمق التحليل", "Analysis Depth"),
            [t("سريع ⚡", "Quick ⚡"), t("شامل 🧠", "Comprehensive 🧠"), t("استراتيجي مع توصيات 🎯", "Strategic + Recommendations 🎯")],
            key="comp_depth"
        )

        competitive_metrics = st.multiselect(
            t("محاور التحليل", "Analysis Focus Areas"),
            [
                t("استراتيجية المحتوى", "Content Strategy"),
                t("سياسة التسعير", "Pricing Strategy"),
                t("الجمهور المستهدف", "Target Audience"),
                t("تواجد السوشيال ميديا", "Social Media Presence"),
                t("منتجات وخدمات رئيسية", "Key Products & Services"),
                t("نقاط الضعف", "Weaknesses"),
                t("فرص التميز", "Differentiation Opportunities"),
            ],
            default=[t("استراتيجية المحتوى", "Content Strategy"), t("نقاط الضعف", "Weaknesses"), t("فرص التميز", "Differentiation Opportunities")],
            key="comp_metrics"
        )

        analyze_btn = st.button(
            t("🕵️ بدء التحليل", "🕵️ Start Analysis"),
            use_container_width=True,
            type="primary",
            key="analyze_comp_btn"
        )

    with col_results:
        st.markdown(f"### 📊 {t('نتائج التحليل', 'Analysis Results')}")

        if analyze_btn:
            if not competitor_name:
                st.warning(t("يرجى إدخال اسم المنافس", "Please enter a competitor name"))
            else:
                with st.spinner(t(f"🔍 جاري تحليل {competitor_name}...", f"🔍 Analyzing {competitor_name}...")):

                    lang = st.session_state.get("lang", "AR")
                    result = analyze_competitor_with_ai(competitor_name, industry, lang)

                    if result:
                        st.markdown(f"""
                        <div class="glass-card animate-in" style="margin-bottom:16px;">
                            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
                                <span style="font-size:2rem;">🕵️</span>
                                <div>
                                    <div style="font-weight:700; font-size:1.1rem; color:{PRIMARY_LIGHT};">{competitor_name}</div>
                                    <div style="color:#64748b; font-size:0.8rem;">{industry}</div>
                                </div>
                                <span class="badge badge-success" style="margin-right:auto;">✅ {t("تم التحليل", "Analyzed")}</span>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        if result.startswith("Error:") or result is None:
                            # Demo mode
                            st.info(f"🔑 {t('لا يوجد مفتاح API — وضع العرض التجريبي', 'No API key — Demo mode')}")
                            _show_demo_competitor(competitor_name, industry)
                        else:
                            st.markdown(f"""
                            <div class="ai-output" style="direction:{'rtl' if lang == 'AR' else 'ltr'};">
                                {result.replace(chr(10), '<br>')}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        _show_demo_competitor(competitor_name, industry)

        else:
            st.markdown(f"""
            <div style="text-align:center; padding:60px 20px; color:#475569; border:2px dashed rgba(124,58,237,0.2); border-radius:20px;">
                <div style="font-size:3rem; margin-bottom:12px;">🕵️</div>
                <div style="font-size:1rem; color:#64748b;">{t("أدخل اسم المنافس لبدء التحليل", "Enter competitor name to start analysis")}</div>
                <div style="font-size:0.8rem; margin-top:8px;">GPT-4o · Strategic Intelligence</div>
            </div>
            """, unsafe_allow_html=True)

    # How it works
    st.markdown("---")
    st.markdown(f"### ⚡ {t('كيف يعمل التحليل', 'How Analysis Works')}")
    steps = [
        ("1️⃣", t("إدخال البيانات", "Input Data"), t("أدخل اسم المنافس والقطاع", "Enter competitor name and sector")),
        ("2️⃣", t("تحليل AI", "AI Analysis"), t("يحلل GPT-4o كل جوانب المنافس", "GPT-4o analyzes all competitor aspects")),
        ("3️⃣", t("رؤى استراتيجية", "Strategic Insights"), t("احصل على توصيات قابلة للتنفيذ", "Get actionable recommendations")),
        ("4️⃣", t("خطة التفوق", "Outperform Plan"), t("خطة بالخطوات للتفوق على المنافس", "Step-by-step plan to outperform them")),
    ]
    s_cols = st.columns(4)
    for col, (num, step_title, step_desc) in zip(s_cols, steps):
        with col:
            st.markdown(f"""
            <div class="kpi-card animate-in">
                <div style="font-size:1.8rem;">{num}</div>
                <div class="kpi-label" style="color:#a78bfa; margin-top:8px;">{step_title}</div>
                <div style="font-size:0.8rem; color:#64748b; margin-top:4px; line-height:1.4;">{step_desc}</div>
            </div>
            """, unsafe_allow_html=True)


def _show_demo_competitor(name: str, industry: str):
    """Show demo competitor analysis when no API key."""
    lang = st.session_state.get("lang", "AR")
    demo = f"""
🏢 **{t('نظرة عامة على العلامة التجارية', 'Brand Overview')}: {name}**
{t('قطاع', 'Sector')}: {industry}

**💪 {t('نقاط القوة', 'Strengths')}:**
- {t('حضور قوي في السوشيال ميديا', 'Strong social media presence')}
- {t('قاعدة عملاء راسخة', 'Established customer base')}
- {t('موارد تسويقية ضخمة', 'Large marketing budget')}

**⚠️ {t('نقاط الضعف', 'Weaknesses')}:**
- {t('ضعف في التواصل العاطفي مع الجمهور', 'Weak emotional connection with audience')}
- {t('محتوى معلباً غير مخصص', 'Generic, non-personalized content')}
- {t('استجابة بطيئة لتغيرات السوق', 'Slow adaptation to market changes')}

**🎯 {t('فرص التميز', 'Differentiation Opportunities')}:**
- {t('تخصيص المحتوى وبناء مجتمع', 'Content personalization and community building')}
- {t('تبني الذكاء الاصطناعي أسرع منهم', 'Faster AI adoption than them')}
- {t('التركيز على شريحة سوقية محددة بعمق', 'Deep focus on a specific market segment')}

**📋 {t('التوصيات الاستراتيجية', 'Strategic Recommendations')}:**
1. {t('بناء محتوى مجتمعي أكثر صدقاً وشخصية', 'Build more authentic, personalized community content')}
2. {t('استغلال نقاط ضعفهم في خدمة العملاء', 'Leverage their customer service weaknesses')}
3. {t('التركيز على منطقة جغرافية منهم', 'Target their underserved geographic areas')}
    """
    st.markdown(f"""
    <div class="ai-output" style="direction:{'rtl' if lang == 'AR' else 'ltr'};">
        {demo.replace(chr(10), '<br>')}
    </div>
    <div style="text-align:center; margin-top:12px;">
        <span class="badge badge-warning">⚠️ {t('وضع تجريبي — أضف OPENAI_API_KEY للتحليل الحقيقي', 'Demo Mode — Add OPENAI_API_KEY for real analysis')}</span>
    </div>
    """, unsafe_allow_html=True)
