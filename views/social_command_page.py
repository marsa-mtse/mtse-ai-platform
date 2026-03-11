import streamlit as st
import pandas as pd
import datetime
from utils import t, render_section_header
from config import BORDER_GLOW

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(180deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.4) 100%); border-right: 2px solid {BORDER_GLOW};">
        <h2>🚀 {t("مركز القيادة الاجتماعية المستقل", "Autonomous Social Command")}</h2>
        <p style="color:#94a3b8;">{t("النشر المباشر والمجدول عبر جميع المنصات بذكاء اصطناعي كامل", "Direct publishing and autonomous scheduling across all platforms")}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(t("المنشورات اليوم", "Today's Posts"), "12", "+2")
    with col2:
        st.metric(t("قيد الانتظار", "In Queue"), "45", "+5")
    with col3:
        st.metric(t("نسبة الوصول", "Total Reach"), "2.4M", "15%")
    with col4:
        st.metric(t("الصحة المركزية", "Hub Health"), "99.8%", "+0.2%")

    st.markdown("---")

    tab_post, tab_queue, tab_analytics = st.tabs([
        f"➕ {t('نشر فوري', 'Quick Post')}",
        f"📅 {t('الجدول الزمني', 'Schedule Queue')}",
        f"📊 {t('تحليلات القيادة', 'Command Analytics')}"
    ])

    with tab_post:
        col_c, col_p = st.columns([1, 1])
        with col_c:
            st.markdown(f"#### 📝 {t('إنشاء محتوى عابر للمنصات', 'Cross-Platform Content Creation')}")
            content = st.text_area(t("محتوى المنشور", "Post Content"), height=150)
            platforms = st.multiselect(t("اختر المنصات", "Select Platforms"), ["Facebook", "Instagram", "X (Twitter)", "LinkedIn", "TikTok"])
            uploaded_file = st.file_uploader(t("إرفاق وسائط", "Attach Media"), type=["jpg", "png", "mp4"])
            
            autobot = st.toggle(t("تفعيل مساعد MTSE للتحسين التلقائي", "Enable MTSE AI Auto-Optimization"), value=True)
            if autobot:
                st.caption("✨ " + t("سيقوم الذكاء الاصطناعي بتكييف النص والهاشتاجات لكل منصة تلقائياً", "AI will adapt text and hashtags for each platform automatically"))

        with col_p:
            st.markdown(f"#### 👁️ {t('معاينة ذكية', 'Smart Preview')}")
            if content:
                st.markdown(f"""
                <div class="glass-card" style="max-width:400px; margin:auto; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display:flex; align-items:center; margin-bottom:10px;">
                        <div style="width:40px; height:40px; background:#6366f1; border-radius:50%;"></div>
                        <div style="margin-left:10px;">
                            <b style="font-size:0.9rem;">MTSE Digital Hub</b><br>
                            <span style="font-size:0.75rem; color:#94a3b8;">Just now</span>
                        </div>
                    </div>
                    <p style="font-size:0.9rem;">{content}</p>
                    <div style="height:200px; background:rgba(255,255,255,0.05); border-radius:12px; display:flex; align-items:center; justify-content:center;">
                        {t('وسائط جاهزة', 'Media Preview')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button(t("🚀 إطلاق فوري لكافة المنصات", "🚀 Launch to All Platforms"), use_container_width=True, type="primary"):
                st.balloons()
                st.success(t("تم إدراج الحملة في مركز القيادة بنجاح", "Campaign successfully listed in Command Hub"))

    with tab_queue:
        render_section_header(t("المنشورات المجدولة القادمة", "Upcoming Scheduled Posts"), "⏳")
        queue_data = pd.DataFrame([
            {"Post": "New Product Launch", "Platform": "FB, IG, X", "Schedule": "2026-03-12 10:00", "Status": "Ready"},
            {"Post": "Customer Success Story", "Platform": "LinkedIn", "Schedule": "2026-03-12 14:00", "Status": "AI Optimizing"},
            {"Post": "Brand Awareness Video", "Platform": "TikTok", "Schedule": "2026-03-13 18:00", "Status": "Pending Media"}
        ])
        st.table(queue_data)

    with tab_analytics:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <h3>📊 {t("أداء مركز القيادة", "Command Hub Performance")}</h3>
            <p>سيتم عرض بيانات الأداء المباشر هنا بمجرد بدء الحملات</p>
        </div>
        """, unsafe_allow_html=True)
