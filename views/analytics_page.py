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
from ai_engine.universal_analyzer import analyze_universal_link, generate_strategic_insights, get_api_status
from ai_engine.multimodal_processor import get_processor
from services.social_connector import social_hub

def render():
    """Render the advanced Analytics page with Integrations."""
    
    plan_manager = PlanManager(st.session_state.plan)

    # ==============================
    # 🔗 UNIVERSAL LINK ANALYZER
    # ==============================
    render_section_header(t("التحليل العالمي العميق", "Universal Deep Analysis"), "🔗")
    
    # --- API STATUS CENTER ---
    status = get_api_status()
    with st.expander(t("📡 حالة الإتصال بالمحركات الاستخباراتية", "📡 Intelligence Engine Connectivity"), expanded=False):
        c1, c2, c3 = st.columns(3)
        c1.write(f"Gemini AI: {'✅ ' + t('متصل', 'Connected') if status['google'] else '❌ ' + t('غير متصل', 'Disconnected')}")
        c2.write(f"OpenAI GPT: {'✅ ' + t('متصل', 'Connected') if status['openai'] else '❌ ' + t('غير متصل', 'Disconnected')}")
        c3.write(f"Groq Llama: {'✅ ' + t('متصل', 'Connected') if status['groq'] else '❌ ' + t('غير متصل', 'Disconnected')}")
        
        if st.session_state.get("last_ai_error"):
            st.error(f"⚠️ {t('آخر خطأ تقني:', 'Last Technical Error:')} {st.session_state.last_ai_error}")

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
        with st.expander(t("🧠 رؤى الذكاء العالمي النخبوي (MTSE OMNI-ELITE)", "🧠 Universal Elite-Intelligence Insights (OMNI-ELITE)"), expanded=True):
            st.markdown(f"### 🌐 {t('مجال الاستخبارات:', 'Intelligence Domain:')} {res.get('domain', 'General')}")
            
            # Elite Status Check
            if "المحرك الاحتياطي" in res.get('essence', ''):
                st.warning(t("⚠️ تنبيه: أنت تستخدم المحرك الاحتياطي. يرجى تفعيل مفاتيح API للحصول على التحليل النخبوي (10x Depth).", 
                             "⚠️ Warning: Using Fallback Engine. Activate API keys for Elite Analysis (10x Depth)."))

            st.info(f"**{t('لب الموضوع وجوهره الاستراتيجي:', 'Strategic Core Essence:')}**\n\n{res.get('essence')}")
            
            # --- DEEP ANALYSIS SECTION ---
            st.markdown(f"#### 🔍 {t('التحليل الاستراتيجي المعمق (Deep Dive):', 'Strategic Deep Dive (10x Depth):')}")
            st.write(res.get('deep_analysis', ''))
            
            st.markdown("---")
            
            # --- COMMAND CENTER GRID ---
            c1, c2, c3 = st.columns(3)
            with c1:
                st.markdown(f"#### 📊 {t('مصفوفة المتجهات:', 'Strategic Matrix:')}")
                matrix = res.get('strategic_matrix', [])
                if isinstance(matrix, list):
                    for m in matrix: st.write(f"◈ {m}")
                else: st.write(matrix)
                
            with c2:
                st.markdown(f"#### ⚠️ {t('تقييم المخاطر:', 'Risk Assessment:')}")
                risks = res.get('risk_assessment', [])
                if isinstance(risks, list):
                    for r in risks: st.write(f"❌ {r}")
                else: st.write(risks)
                
            with c3:
                st.markdown(f"#### 🚀 {t('التوقعات المستقبلية:', 'Long-term Forecast:')}")
                st.success(res.get('forecast', ''))
                
            st.markdown("---")
            st.markdown(f"#### 🗺️ {t('خارطة الطريق التنفيذية (The Universal Roadmap):', 'The Executive Roadmap:')}")
            roadmap = res.get('roadmap', [])
            if isinstance(roadmap, list):
                for r in roadmap: st.write(f"➤ {r}")
            else: st.write(roadmap)

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
    # 🖼️ ELITE MULTI-MODAL ANALYSIS
    # ==============================
    render_section_header(t("التحليل الاستخباري متعدد الوسائط (AI Vision)", "Elite AI Vision & Multi-Modal Intelligence"), "🖼️")
    
    if not plan_manager.can_access_multimodal():
        st.warning(t("هذه الميزة النخبوية (رؤية الحاسوب) متاحة لخطة Strategist فأعلى.", "Elite Multi-Modal Vision is for Strategist plan and higher."))
    else:
        st.markdown(f"""
        <div class="glass-card animate-in" style="border-left: 4px solid #c084fc;">
            <p style="color:#cbd5e1;">🎯 {t("ارفع صورة (مخطط هندسي، فاتورة، رسم بياني، صورة منتج) للتحليل العميق.", "Upload an image (Engineering drawing, Invoice, Chart, Product) for deep AI analysis.")}</p>
        </div>
        """, unsafe_allow_html=True)
        
        vision_file = st.file_uploader(t("رفع صورة للتحليل 📸", "Upload Image for AI Vision 📸"), type=["png", "jpg", "jpeg"], key="vision_upload")
        
        if vision_file:
            st.image(vision_file, width=400)
            vision_prompt = st.text_area(t("ماذا تريد أن تعرف عن هذه الصورة؟", "What do you want to know about this image?"), 
                                        placeholder=t("مثلاً: استخرج البنود والكميات، أو حلل جودة التصميم...", "e.g. Extract items & quantities, or analyze design quality..."))
            
            if st.button(t("🚀 تحليل الصورة استخباراتياً", "🚀 Analyze Image with AI Vision"), use_container_width=True):
                with st.spinner(t("جاري تشغيل محرك الرؤية العالمي للـ MTSE...", "Running MTSE Global Vision Engine...")):
                    processor = get_processor()
                    vision_res = processor.process_image(vision_file.getvalue(), prompt=vision_prompt if vision_prompt else "Analyze this image in extreme detail for business and technical insights.")
                    st.session_state.vision_analysis = vision_res
                    st.success(t("✅ تم استخراج الرؤى البصرية!", "✅ Vision insights extracted!"))

        if st.session_state.get("vision_analysis"):
            st.markdown(f"""
            <div class="glass-card" style="border-top: 4px solid #c084fc; padding: 25px;">
                <h4 style="color:#c084fc;">🧠 {t('نتائج تحليل الرؤية:', 'AI Vision Results:')}</h4>
                <div style="line-height:1.7; color:#f8fafc;">
                    {st.session_state.vision_analysis}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(t("🗑️ مسح النتائج", "🗑️ Clear Vision Results")):
                st.session_state.vision_analysis = None
                st.rerun()

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
            metrics = social_hub.get_realtime_metrics("TikTok")
            st.success(t("تم الاتصال بمحرك TikTok اللحظي ✅", "Connected to Real-time TikTok Engine ✅"))
            
            c1, c2, c3 = st.columns(3)
            c1.metric(t("المشاهدات اللحظية", "Live Views"), metrics["live_views"], metrics["trend"])
            c2.metric(t("نسبة التفاعل", "Engagement Rate"), metrics["engagement"])
            c3.metric(t("التوقيت", "Sync Time"), metrics["timestamp"])
            
            if st.button(t("🔄 تحديث البيانات اللحظية", "🔄 Refresh Live Metrics"), key="refresh_tt"):
                st.rerun()
            
            st.markdown("---")
            st.markdown(f"### {t('المواضيع الرائجة (MENA)', 'Trending Topics (MENA)')}")
            trends = social_hub.get_trending_topics()
            for tr in trends:
                st.write(f"🔥 **{tr['topic']}** | {t('الحجم:', 'Volume:')} {tr['volume']} | {t('الشعور:', 'Sentiment:')} {tr['sentiment']}")

    # ==============================
    # 📸 INSTAGRAM API INTEGRATION
    # ==============================
    with tab_insta:
        render_section_header(t("Instagram Graph Analytics", "Instagram Graph Analytics"), "📸")
        if not plan_manager.can_access_integrations():
            st.warning(t("التكامل متاح لخطط Pro و Business.", "Pro and Business plans required."))
        else:
            metrics = social_hub.get_realtime_metrics("Instagram")
            st.info(f"{t('المتصل الآن:', 'Currently Streaming:')} {metrics['platform']}")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Reels Insights 🎬")
                render_kpi_card(t("تفاعل الريلز", "Reels Engagement"), metrics["engagement"], metrics["trend"])
            with col2:
                st.markdown("### Forecast 📈")
                forecast = social_hub.get_campaign_forecast(500)
                st.write(f"🎯 {t('الوصول المتوقع:', 'Predicted Reach:')} {forecast['reach']:,}")
                st.write(f"💰 {t('العائد المتوقع:', 'Predicted ROI:')} {forecast['roi']}")

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
