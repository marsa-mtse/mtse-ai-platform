# ==========================================================
# MTSE Marketing Engine - Global Brand Voice Trainer
# ==========================================================
import streamlit as st
from utils import t, render_section_header

def render():
    render_section_header(t("مدرب بصمة العلامة (Brand Voice)", "Global Brand Voice Trainer"), "🎭")
    
    st.markdown(f"""
    <div class="glass-card" style="padding:24px; margin-bottom:24px;">
        <p style="color:#94a3b8; font-size:0.9rem;">
            {t("قم بتدريب الذكاء الاصطناعي على شخصية علامتك التجارية لضمان أن جميع المحتويات المولدة تتبع نفس النبرة والأسلوب.", 
               "Train the AI on your brand identity to ensure all generated content follows the same tone and style.")}
        </p>
    </div>
    """, unsafe_allow_html=True)

    if "brand_voice" not in st.session_state:
        st.session_state.brand_voice = {
            "personality": "",
            "target_audience": "",
            "forbidden_words": "",
            "core_values": ""
        }

    with st.form("brand_voice_form"):
        c1, c2 = st.columns(2)
        with c1:
            personality = st.text_area(t("شخصية العلامة (مثلاً: مرحة، جادة، تقنية):", "Brand Personality (e.g. Playful, Serious, Tech):"), value=st.session_state.brand_voice["personality"])
            core_values = st.text_area(t("القيم الأساسية (مثلاً: الابتكار، الاستدامة):", "Core Values (e.g. Innovation, Sustainability):"), value=st.session_state.brand_voice["core_values"])
        with c2:
            target_audience = st.text_area(t("الجمهور المستهدف بالتفصيل:", "Detailed Target Audience:"), value=st.session_state.brand_voice["target_audience"])
            forbidden_words = st.text_input(t("كلمات محظورة (تجنبها):", "Forbidden Words (Avoid):"), value=st.session_state.brand_voice["forbidden_words"])
            
        submit = st.form_submit_button(t("🚀 حفظ بصمة العلامة", "🚀 Save Brand Pulse"), use_container_width=True, type="primary")
        
        if submit:
            st.session_state.brand_voice = {
                "personality": personality,
                "target_audience": target_audience,
                "forbidden_words": forbidden_words,
                "core_values": core_values
            }
            st.success(t("تم حفظ البصمة! سيقوم المساعد الذكي الآن بتبني شخصية علامتك التجارية في كافة المهام.", "Brand Pulse saved! The AI will now adopt your brand identity in all tasks."))

    st.markdown("---")
    st.markdown(f"### 💡 {t('كيف يعمل هذا؟', 'How does this work?')}")
    st.info(t("عندما تقوم بتوليد حملة أو نص فيديو، سنقوم بحقن هذه المعلومات سراً في 'عقل' الذكاء الاصطناعي لضمان الاتساق.", 
             "When you generate a campaign or script, we secretly inject this info into the AI's 'brain' to ensure consistency."))
