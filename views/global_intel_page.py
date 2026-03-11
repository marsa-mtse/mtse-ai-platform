import streamlit as st
from utils import t, render_section_header
from config import BORDER_GLOW

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(135deg, rgba(56, 189, 248, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);">
        <h1>🌐 {t("مركز استخبارات الأعمال العالمي", "Global Intelligence Hub")}</h1>
        <p style="color:#94a3b8;">{t("تحليل اتجاهات السوق العالمية وسلوك المستهلكين في الوقت الفعلي", "Analyze global market trends and real-time consumer behavior")}</p>
    </div>
    """, unsafe_allow_html=True)

    col_map, col_trends = st.columns([1.5, 1])

    with col_map:
        st.markdown(f"""
        <div class="glass-card" style="height:400px; display:flex; align-items:center; justify-content:center; border:1px solid rgba(255,255,255,0.05);">
            <div style="text-align:center;">
                <div style="font-size:4rem; opacity:0.5;">🗺️</div>
                <p style="color:#64748b;">{t("جاري تحميل خارطة التفاعل العالمية...", "Loading Global Engagement Heatmap...")}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_trends:
        render_section_header(t("الاتجاهات الصاعدة", "Rising Trends"), "📈")
        trends = [
            {"name": "AI Automation", "growth": "+450%", "region": "Global"},
            {"name": "Sustainability", "growth": "+120%", "region": "Europe"},
            {"name": "Direct-to-Consumer", "growth": "+85%", "region": "US/MENA"}
        ]
        for tr in trends:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:12px; background:rgba(255,255,255,0.03); margin-bottom:8px; border-radius:10px;">
                <span>{tr['name']} <small style="color:#94a3b8;">({tr['region']})</small></span>
                <b style="color:#10b981;">{tr['growth']}</b>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"#### 🎙️ {t('تحليل المشاعر العامة', 'Public Sentiment Analysis')}")
        st.progress(82, text="Positive (82%)")
        st.progress(12, text="Neutral (12%)")
        st.progress(6, text="Negative (6%)")
    
    with col2:
        st.markdown(f"#### 💡 {t('توصيات الاستخبارات', 'Intelligence Alpha')}")
        st.info(t("إشارة شراء قوية لمنتجات الرفاهية في منطقة الخليج الأسبوع القادم", "Strong purchase signal for luxury goods in GCC next week"))
        st.warning(t("تراجع متوقع في الوصول العضوي لمنصات Meta يوم الخميس", "Expected drop in organic reach for Meta platforms this Thursday"))
