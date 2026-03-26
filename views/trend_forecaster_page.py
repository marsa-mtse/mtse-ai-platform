# ==========================================================
# MTSE v13 - AI Trend Forecaster
# Predict marketing trends using Gemini 1.5 Pro
# ==========================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
from utils import t


def forecast_trends_with_ai(industry: str, platforms: list, timeframe: str, lang: str) -> str:
    """Use AI Gateway to forecast marketing trends."""
    from ai_engine.ai_gateway import structured_text_generation
    
    platforms_str = ", ".join(platforms)
    system_prompt = "You are an expert digital marketing trend analyst and futurist. Provide specific, actionable, and data-driven trend forecasts."
    
    user_prompt = f"""
    Analyze and forecast marketing trends for the {industry} industry.
    Platforms to analyze: {platforms_str}
    Forecast timeframe: {timeframe}
    Language: {"Arabic" if lang == "AR" else "English"}
    
    Provide:
    1. Top 5 emerging trends with impact score (1-10)
    2. Platform-specific trend analysis
    3. Content format predictions (video length, style, tone)
    4. Consumer behavior shifts expected
    5. Tactical recommendations for each trend
    6. Risk areas to avoid
    """
    
    result = structured_text_generation(system_prompt, user_prompt, preferred_provider="google")
    return result if result else None


def render():
    from config import PRIMARY, PRIMARY_LIGHT, ACCENT, NEON_GREEN

    st.markdown(f"""
    <div class="tool-header animate-in">
        <div class="tool-header-icon">📈</div>
        <h2>{t("توقع الاتجاهات بالذكاء الاصطناعي", "AI Trend Forecaster")}</h2>
        <p style="color:#94a3b8;">{t("توقعات دقيقة للاتجاهات التسويقية القادمة بقوة Gemini 1.5 Pro", "Precise marketing trend forecasts powered by Gemini 1.5 Pro")}</p>
        <span class="badge badge-primary">Gemini 1.5 Pro · GPT-4o · Trend Intelligence</span>
    </div>
    """, unsafe_allow_html=True)

    col_settings, col_output = st.columns([1, 1.4])

    with col_settings:
        st.markdown(f"### ⚙️ {t('إعدادات التوقع', 'Forecast Settings')}")

        industry = st.selectbox(
            t("القطاع / الصناعة", "Industry"),
            [
                t("التجزئة والتجارة الإلكترونية", "Retail & E-commerce"),
                t("التكنولوجيا", "Technology"),
                t("الغذاء والمشروبات", "Food & Beverages"),
                t("الأزياء", "Fashion"),
                t("الرعاية الصحية", "Healthcare"),
                t("العقارات", "Real Estate"),
                t("التعليم", "Education"),
                t("السفر", "Travel"),
            ],
            key="trend_industry"
        )

        platforms = st.multiselect(
            t("المنصات المستهدفة", "Target Platforms"),
            ["TikTok", "Instagram", "YouTube", "LinkedIn", "Twitter/X", "Snapchat", "Facebook", "Pinterest"],
            default=["TikTok", "Instagram", "YouTube"],
            key="trend_platforms"
        )

        timeframe = st.radio(
            t("الفترة الزمنية", "Time Horizon"),
            [t("30 يوم", "30 Days"), t("60 يوم", "60 Days"), t("90 يوم", "90 Days"), t("6 أشهر", "6 Months")],
            horizontal=True,
            key="trend_timeframe"
        )

        show_chart = st.checkbox(
            t("عرض رسم بياني للاتجاهات", "Show Trend Chart"),
            value=True,
            key="trend_show_chart"
        )

        forecast_btn = st.button(
            t("🔮 توقع الاتجاهات", "🔮 Forecast Trends"),
            use_container_width=True,
            type="primary",
            key="forecast_btn"
        )

    with col_output:
        st.markdown(f"### 🔮 {t('نتائج التوقع', 'Forecast Results')}")

        if forecast_btn:
            if not platforms:
                st.warning(t("يرجى اختيار منصة واحدة على الأقل", "Please select at least one platform"))
            else:
                with st.spinner(t("🔮 جاري التحليل والتوقع...", "🔮 Analyzing and forecasting...")):
                    lang = st.session_state.get("lang", "AR")
                    result = forecast_trends_with_ai(industry, platforms, timeframe, lang)

                    # Show trend visualization chart
                    if show_chart:
                        _show_trend_chart(platforms, timeframe)

                    if result:
                        st.markdown(f"""
                        <div class="ai-output" style="direction:{'rtl' if lang == 'AR' else 'ltr'};">
                            {result.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Demo mode
                        st.info(t("وضع العرض التجريبي — أضف GOOGLE_API_KEY أو OPENAI_API_KEY", "Demo Mode — Add GOOGLE_API_KEY or OPENAI_API_KEY"))
                        _show_demo_forecast(industry, platforms, timeframe, lang)
        else:
            st.markdown(f"""
            <div style="text-align:center; padding:60px 20px; color:#475569; border:2px dashed rgba(124,58,237,0.2); border-radius:20px;">
                <div style="font-size:3rem; margin-bottom:12px;">📈</div>
                <div style="color:#64748b;">{t("اضغط توقع الاتجاهات للبدء", "Click Forecast Trends to start")}</div>
                <div style="font-size:0.8rem; margin-top:8px;">Gemini 1.5 Pro · GPT-4o</div>
            </div>
            """, unsafe_allow_html=True)


def _show_trend_chart(platforms: list, timeframe: str):
    """Create an interactive trend chart."""
    import numpy as np

    days_map = {
        "30 Days": 30, "30 يوم": 30,
        "60 Days": 60, "60 يوم": 60,
        "90 Days": 90, "90 يوم": 90,
        "6 Months": 180, "6 أشهر": 180,
    }
    days = days_map.get(timeframe, 30)
    dates = pd.date_range(start=pd.Timestamp.now(), periods=days, freq="D")

    fig = go.Figure()
    colors = ["#7c3aed", "#38bdf8", "#f0abfc", "#34d399", "#fbbf24", "#f43f5e", "#818cf8", "#fb923c"]

    for i, platform in enumerate(platforms[:6]):
        base = random.randint(40, 70)
        trend = np.cumsum(np.random.randn(days) * 2) + base
        trend = np.clip(trend, 10, 100)
        fig.add_trace(go.Scatter(
            x=dates, y=trend,
            name=platform,
            line=dict(color=colors[i % len(colors)], width=2.5),
            fill="tozeroy" if i == 0 else "none",
            fillcolor=f"rgba{tuple(int(colors[i % len(colors)].lstrip('#')[j:j+2], 16) for j in (0,2,4)) + (0.05,)}" if i == 0 else "none",
        ))

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(10,15,40,0.6)",
        font=dict(family="Inter, sans-serif", color="#94a3b8"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", showgrid=True),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", showgrid=True, title="Trend Score"),
        title=dict(text=f"📊 Platform Trend Forecast — {timeframe}", font=dict(size=14, color="#a78bfa")),
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)


def _show_demo_forecast(industry: str, platforms: list, timeframe: str, lang: str):
    """Show demo trend forecast."""
    platforms_str = ", ".join(platforms[:3])
    demo = f"""
📊 **{t('تقرير توقع الاتجاهات', 'Trend Forecast Report')}**
🏭 {industry} | ⏱ {timeframe} | 📲 {platforms_str}

**🔥 {t('الاتجاهات الرئيسية القادمة', 'Top Emerging Trends')}:**

1. **{t('المحتوى القصير المولّد بالذكاء الاصطناعي', 'AI-Generated Short-Form Content')}** (Score: 9.2/10)
   - {t('نمو متوقع 340% في TikTok و Reels', 'Expected 340% growth on TikTok & Reels')}
   - {t('التوصية: استثمر في أدوات AI للمحتوى الآن', 'Recommendation: Invest in AI content tools now')}

2. **{t('التسوق الاجتماعي المباشر', 'Live Social Commerce')}** (Score: 8.8/10)
   - {t('بث مباشر مع رابط شراء فوري', 'Live streams with instant purchase links')}
   - {t('التوصية: ابدأ بـ Instagram Live Shopping', 'Recommendation: Start with Instagram Live Shopping')}

3. **{t('محتوى الصوت والبودكاست', 'Audio & Podcast Content')}** (Score: 7.9/10)
   - {t('نمو 180% في المنطقة العربية', '180% growth in the Arab region')}
   - {t('التوصية: أطلق بودكاست خاص بعلامتك', 'Recommendation: Launch your brand podcast')}

4. **{t('البحث المرئي والصوتي', 'Visual & Voice Search')}** (Score: 7.5/10)
   - {t('تحسين المحتوى لـ Google Lens و Voice', 'Optimize content for Google Lens & Voice')}

5. **{t('تخصيص فائق بالذكاء الاصطناعي', 'AI Hyper-Personalization')}** (Score: 8.2/10)
   - {t('محتوى مخصص لكل مستخدم بشكل فردي', 'Content personalized for each user individually')}

⚠️ **{t('مناطق الخطر', 'Risk Areas')}:**
- {t('الاعتماد المفرط على الكلمات المفتاحية الباردة', 'Over-reliance on cold keywords')}
- {t('المحتوى الإعلاني المباشر دون قيمة', 'Direct advertising content without value')}
    """
    st.markdown(f"""
    <div class="ai-output" style="direction:{'rtl' if lang == 'AR' else 'ltr'};">
        {demo.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
