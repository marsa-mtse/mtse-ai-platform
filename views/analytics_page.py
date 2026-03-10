# ==========================================================
# MTSE Marketing Engine - Analytics Page Update
# ==========================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils import t, render_section_header, render_kpi_card, render_empty_state, generate_branded_pdf
from integrations.tiktok_api import TikTokAdsAPI
from integrations.instagram_api import InstagramGraphAPI
from integrations.youtube_api import YouTubeAnalyticsAPI
from billing.plans import PlanManager
from ai_engine.universal_analyzer import analyze_universal_link, generate_strategic_insights

def render():
    """Render the advanced Analytics page with Integrations."""
    
    plan_manager = PlanManager(st.session_state.plan)

    # ==============================
    # 🔗 UNIVERSAL LINK ANALYZER
    # ==============================
    render_section_header(t("التحليل العالمي العميق", "Universal Deep Analysis"), "🔗")
    
    st.markdown(f"""
    <div class="glass-card animate-in">
        <p style="color:#94a3b8; font-size:1rem;">
            {t("أدخل أي رابط (سوشيال ميديا، فيديو، مقال، جدول) لتحليله استراتيجياً.", 
               "Enter any link (Social, Video, Article, Sheet) for strategic analysis.")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    uc1, uc2 = st.columns([3, 1])
    with uc1:
        target_url = st.text_input(t("رابط المحتوى للتحليل", "Content URL to Analyze"), placeholder="https://youtube.com/...", key="univ_url")
    with uc2:
        analysis_depth = st.selectbox(t("دقة التحليل", "Analysis Depth"), [t("عميق جداً", "Deep Search"), t("قياسي", "Standard")], key="univ_depth")

    if st.button(t("تحليل الرابط استراتيجياً 🚀", "Analyze Strategically 🚀"), use_container_width=True):
        if not target_url:
            st.error(t("الرجاء إدخال الرابط أولاً.", "Please enter a URL first."))
        else:
            with st.spinner(t("جاري تحليل الرابط بعمق عبر Gemini 2.0...", "Performing deep link analysis via Gemini 2.0...")):
                result = analyze_universal_link(target_url, depth=analysis_depth)
                if "error" in result:
                    st.error(f"❌ {result['error']}")
                else:
                    st.session_state.universal_analysis = result
                    st.success(t("✅ تم التحليل بنجاح!", "✅ Analysis completed successfully!"))

    if st.session_state.get("universal_analysis"):
        res = st.session_state.universal_analysis
        with st.expander(t("👑 نتائج التحليل النخبوي (Elite AI Insights)", "👑 Elite AI Insights Results"), expanded=True):
            st.markdown(f"#### {t('النشاط التجاري:', 'Industry:')} {res.get('industry', 'General')}")
            
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**{t('الملخص:', 'Summary:')}**\n\n{res.get('summary')}")
                st.warning(f"**{t('الجمهور المستهدف:', 'Target Audience:')}**\n\n{res.get('audience')}")
                st.markdown(f"**{t('قمع المبيعات:', 'Conversion Funnel:')}**\n\n{res.get('funnel_analysis')}")
            with c2:
                st.success(f"**{t('تحليل SWOT (Elite):', 'Elite SWOT Analysis:')}**\n\n{res.get('swot')}")
                st.markdown(f"**{t('إمكانية الانتشار:', 'Viral Potential:')}**\n\n{res.get('viral_loop')}")
                st.write(f"**{t('خارطة الطريق:', 'The Roadmap:')}**\n\n{res.get('recommendations')}")

        # --- PDF GENERATION ---
        st.markdown("### 📄 " + t("استخراج التقرير الرسمي", "Export Official Report"))
        pdf_lang = st.radio(t("لغة التقرير", "Report Language"), [t("العربية", "Arabic"), t("English", "English"), t("اللغتين معاً", "Both Languages")], horizontal=True)
        
        if st.button(t("تجهيز التقرير للتحميل 🛠️", "Prepare Report for Download 🛠️"), use_container_width=True):
            with st.spinner(t("جاري بناء التقرير...", "Building report...")):
                report_data = generate_strategic_insights(res, lang=pdf_lang)
                pdf_bytes = generate_branded_pdf(report_data, lang=pdf_lang)
                if pdf_bytes:
                    st.session_state.pdf_report_bytes = pdf_bytes
                    st.success(t("✅ التقرير جاهز الآن!", "✅ Report is ready!"))
                else:
                    st.error(t("❌ فشل في إنشاء التقرير. تأكد من توفر المكتبات اللازمة.", "❌ Failed to create PDF. Check dependencies."))

        if st.session_state.get("pdf_report_bytes"):
            st.download_button(
                label=t("تحميل التقرير PDF ببيانات المنصة 📥", "Download PDF Branded Report 📥"),
                data=st.session_state.pdf_report_bytes,
                file_name="MTSE_Strategic_Report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key="pdf_download_incremental"
            )
    
    st.markdown("---")

    # ==============================
    # 🌍 GLOBAL MARKET TRENDS
    # ==============================
    render_section_header(t("اتجاهات السوق العالمية", "Global Market Trends"), "🌍")
    
    # Simulated global data
    global_data = pd.DataFrame({
        'Country': ['USA', 'China', 'Germany', 'UK', 'France', 'India', 'Brazil', 'UAE', 'Saudi Arabia', 'Egypt'],
        'Market Score': [95, 88, 75, 72, 68, 85, 60, 92, 90, 80]
    })
    
    fig_map = px.choropleth(
        global_data,
        locations="Country",
        locationmode="country names",
        color="Market Score",
        hover_name="Country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=t("نقاط قوة السوق حسب الدولة", "Market Sentiment Score by Country")
    )
    fig_map.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("")
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>📊 {t("التحليلات والتكامل", "Analytics & Integrations")}</h2>
        <p style="color:#94a3b8;">{t("مركز البيانات المتكامل (Uploads & APIs)", "Unified Data Hub (Uploads & APIs)")}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab_upload, tab_tiktok, tab_insta, tab_youtube = st.tabs([
        t("📁 رفع الملفات", "📁 Upload Files"),
        t("🎵 تيك توك", "🎵 TikTok Ads"),
        t("📸 انستجرام", "📸 Instagram API"),
        t("▶️ يوتيوب", "▶️ YouTube Data")
    ])

    # ==============================
    # 📁 MANUAL DATA UPLOAD
    # ==============================
    with tab_upload:
        render_section_header(t("رفع البيانات وتحليلها", "Data Upload & Analysis"), "📁")
        
        uploaded_file = st.file_uploader(t("رفع ملف (CSV, Excel)", "Upload (CSV, Excel)"), type=["csv", "xlsx"])
        
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file)
                    
                st.session_state.analysis_df = df
                st.success(t(f"تم تحميل الملف بنجاح! ({len(df)} صف) ✅", f"File loaded! ({len(df)} rows) ✅"))
                
                # Show data preview
                with st.expander(t("معاينة البيانات", "Data Preview"), expanded=False):
                    st.dataframe(df.head(10), use_container_width=True)
                
                # Dynamic Charts
                numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
                date_cols = df.select_dtypes(include=['datetime', 'object']).columns.tolist()
                
                if numeric_cols:
                    col1, col2 = st.columns(2)
                    with col1:
                        x_axis = st.selectbox("X-Axis", date_cols if date_cols else df.columns)
                    with col2:
                        y_axis = st.selectbox("Y-Axis", numeric_cols)
                        
                    chart_type = st.radio("Chart Type", ["Line", "Bar", "Scatter"], horizontal=True)
                    
                    if chart_type == "Line":
                        fig = px.line(df, x=x_axis, y=y_axis, template="plotly_dark")
                    elif chart_type == "Bar":
                        fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark")
                    else:
                        fig = px.scatter(df, x=x_axis, y=y_axis, template="plotly_dark")
                        
                    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error processing file: {e}")

    # ==============================
    # 🎵 TIKTOK ADS INTEGRATION
    # ==============================
    with tab_tiktok:
        render_section_header(t("TikTok Ads Analytics", "TikTok Ads Analytics"), "🎵")
        if not plan_manager.can_access_integrations():
            st.warning(t("التكامل مع المنصات متاح لخطط Pro و Business.", "API integrations available to Pro and Business plans."))
        else:
            api = TikTokAdsAPI(access_token="simulated_token")
            st.success(api.test_connection()["message"])
            
            if st.button(t("🔄 تحديث بيانات TikTok", "🔄 Refresh TikTok Data")):
                df = api.fetch_campaign_performance(days=14)
                
                total_spend = df["spend"].sum()
                total_impressions = df["impressions"].sum()
                avg_cpa = df["cpa"].mean()
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Total Spend", f"${total_spend:,.2f}")
                c2.metric("Impressions", f"{total_impressions:,}")
                c3.metric("Avg CPA", f"${avg_cpa:,.2f}")
                
                fig = px.bar(df, x="date", y="spend", color="campaign_name", title="Spend per Campaign", template="plotly_dark")
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(df, use_container_width=True)

    # ==============================
    # 📸 INSTAGRAM API INTEGRATION
    # ==============================
    with tab_insta:
        render_section_header(t("Instagram Graph Analytics", "Instagram Graph Analytics"), "📸")
        if not plan_manager.can_access_integrations():
            st.warning(t("التكامل متاح لخطط Pro و Business.", "Pro and Business plans required."))
        else:
            api = InstagramGraphAPI(access_token="simulated")
            auth_info = api.authenticate()
            st.info(f"{t('متصل بحساب:', 'Connected as:')} {auth_info['username']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Reels Performance 🎬")
                df_reels = api.fetch_reel_performance(limit=5)
                fig_reels = px.bar(df_reels, x="reel_id", y="engagement_rate", color="plays", title="Top Reels Engagement (%)", template="plotly_dark")
                fig_reels.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_reels, use_container_width=True)
            with col2:
                st.markdown("### Audience Demo 🌍")
                demo = api.get_audience_demographics()
                df_demo = pd.DataFrame(list(demo['cities'].items()), columns=['City', 'Percentage'])
                fig_dem = px.pie(df_demo, names='City', values='Percentage', hole=0.4, template="plotly_dark", title="Audience by City")
                fig_dem.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_dem, use_container_width=True)

    # ==============================
    # ▶️ YOUTUBE API INTEGRATION
    # ==============================
    with tab_youtube:
        render_section_header(t("YouTube Channel Analytics", "YouTube Channel Analytics"), "▶️")
        if not plan_manager.can_access_integrations():
            st.warning(t("التكامل متاح لخطط Pro و Business.", "Pro and Business plans required."))
        else:
            api = YouTubeAnalyticsAPI(api_key="simulated")
            stats = api.get_channel_stats()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Subscribers", f"{stats['subscriber_count']:,}")
            c2.metric("Total Views", f"{stats['total_views']:,}")
            c3.metric("Video Count", stats['video_count'])
            
            st.markdown("### Traffic Sources 🚦")
            sources = api.fetch_traffic_sources()
            df_sources = pd.DataFrame(sources)
            fig_sources = px.bar(df_sources, y="source", x="percentage", orientation='h', color="percentage", template="plotly_dark", title="Where viewers find you")
            fig_sources.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_sources, use_container_width=True)
