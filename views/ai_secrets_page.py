# ==========================================================
# MTSE Marketing Engine - AI Secrets Management
# ==========================================================
import streamlit as st
from utils import t, render_section_header
from config import FALLBACK_API_KEYS

def render():
    render_section_header(t("إدارة مفاتيح الذكاء الاصطناعي", "AI Secrets Management"), "🔑")
    
    st.markdown(f"""
    <div class="glass-card" style="padding:24px; margin-bottom:24px;">
        <p style="color:#94a3b8; font-size:0.9rem;">
            {t("هذه الصفحة تتيح لك إدخال مفاتيحك الخاصة لتجاوز الحدود المفروضة على الحسابات التجريبية. يتم حفظ هذه المفاتيح في الجلسة الحالية فقط لضمان الأمان.", 
               "This page allows you to enter your private API keys to bypass limits on demo accounts. Keys are saved in the current session for security.")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "custom_keys" not in st.session_state:
        st.session_state.custom_keys = {}

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### 💬 {t('محركات النصوص', 'Text Engines')}")
        
        # Google Gemini
        google_key = st.text_input("Google AI (Gemini) Key", 
                                   value=st.session_state.custom_keys.get("google", ""), 
                                   type="password", 
                                   help="Get it from Google AI Studio")
        if google_key: st.session_state.custom_keys["google"] = google_key
        
        # Groq
        groq_key = st.text_input("Groq API Key (Llama 3)", 
                                 value=st.session_state.custom_keys.get("groq", ""), 
                                 type="password",
                                 help="Get it from Groq Console")
        if groq_key: st.session_state.custom_keys["groq"] = groq_key

        # Anthropic
        anthropic_key = st.text_input("Anthropic API Key (Claude)", 
                                      value=st.session_state.custom_keys.get("anthropic", ""), 
                                      type="password")
        if anthropic_key: st.session_state.custom_keys["anthropic"] = anthropic_key

    with col2:
        st.markdown(f"### 🖼️ {t('محركات الوسائط', 'Multimedia Engines')}")
        
        # OpenAI
        openai_key = st.text_input("OpenAI API Key (DALL-E 3 / GPT-4)", 
                                   value=st.session_state.custom_keys.get("openai", ""), 
                                   type="password")
        if openai_key: st.session_state.custom_keys["openai"] = openai_key

        # Leonardo
        leonardo_key = st.text_input("Leonardo AI Key", 
                                     value=st.session_state.custom_keys.get("leonardo", ""), 
                                     type="password")
        if leonardo_key: st.session_state.custom_keys["leonardo"] = leonardo_key

    with col3:
        st.markdown(f"### 📡 {t('مفاتيح النشر', 'Publishing Keys')}")
        
        # Meta (FB/IG)
        meta_token = st.text_input("Meta (FB/IG) Access Token", 
                                   value=st.session_state.custom_keys.get("meta_token", ""), 
                                   type="password")
        if meta_token: st.session_state.custom_keys["meta_token"] = meta_token
        
        meta_page = st.text_input("Meta Page ID", 
                                  value=st.session_state.custom_keys.get("meta_page", ""))
        if meta_page: st.session_state.custom_keys["meta_page"] = meta_page
        
        # TikTok
        tt_token = st.text_input("TikTok Access Token", 
                                 value=st.session_state.custom_keys.get("tt_token", ""), 
                                 type="password")
        if tt_token: st.session_state.custom_keys["tt_token"] = tt_token
        
        # X / Twitter
        x_token = st.text_input("X (Twitter) Bearer Token", 
                                value=st.session_state.custom_keys.get("x_token", ""), 
                                type="password")
        if x_token: st.session_state.custom_keys["x_token"] = x_token

    st.markdown("---")
    
    if st.button(t("✅ حفظ المفاتيح للجلسة الحالية", "✅ Save Keys for Current Session"), type="primary", use_container_width=True):
        st.success(t("تم تحديث المفاتيح بنجاح! المنصة ستستخدم مفاتيحك الآن.", "Keys updated successfully! The platform will use your keys now."))
        st.balloons()

    st.markdown(f"""
    <div style="background:rgba(234,179,8,0.1); border:1px solid rgba(234,179,8,0.2); border-radius:12px; padding:16px; margin-top:24px;">
        <h4 style="color:#eab308; margin-top:0;">⚠️ {t("تنبيه أمني", "Security Note")}</h4>
        <p style="font-size:0.85rem; color:#94a3b8; margin-bottom:0;">
            {t("المفاتيح التي تدخلها هنا لا يتم تخزينها في قاعدة البيانات؛ ستختفي بمجرد إغلاق المتصفح أو تسجيل الخروج. لتخزينها بشكل دائم، يرجى إضافتها إلى ملف config.py أو استخدام Streamlit Secrets.",
               "Keys entered here are not stored in the database; they will disappear once you close the browser or logout. For permanent storage, add them to config.py or use Streamlit Secrets.")}
        </p>
    </div>
    """, unsafe_allow_html=True)
