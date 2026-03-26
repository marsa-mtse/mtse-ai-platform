# ==========================================================
# MTSE Marketing Engine - Unified Video Studio
# ==========================================================
import streamlit as st
import os
import tempfile
import json
from utils import t, render_section_header, generate_branded_pdf
from ai_engine.video_analyzer import get_video_analyzer
from ai_engine.ai_gateway import structured_text_generation, generate_image_advanced, generate_video, generate_audio
from database import get_user_branding, log_activity

def render():
    st.markdown(f"""
    <div class="hero-v13" style="padding:40px 20px; border-radius:16px;">
        <h2 class="hero-title" style="font-size:2.5rem; margin-bottom:10px;">🎬 {t("استوديو الفيديو الذكي", "AI Video Studio")}</h2>
        <p class="hero-subtitle" style="margin-bottom:0;">{t("اكتب نصوص فيديو قوية، وصمم المشاهد، أو حلل إعلانات منافسيك لتعرف سر نجاحهم.", "Generate high-converting scripts, storyboard scenes, or analyze competitor ads.")}</p>
    </div>
    <br/>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs([f"✨ {t('تصميم وإنتاج (Script & Storyboard)', 'Generate & Storyboard')}", f"🕵️ {t('تحليل الإعلانات (Video Intel)', 'Video Intel')}"])

    # ==============================
    # TAB 1: GENERATE VIDEO SCRIPT
    # ==============================
    with tab1:
        st.markdown(f"### 📝 {t('توليد نصوص الفيديو والسيناريو', 'Video Script Generator')}")
        
        with st.form("video_script_form"):
            topic = st.text_input(t("موضوع الفيديو أو المنتج:", "Video Topic or Product:"))
            platform = st.selectbox(t("المنصة المستهدفة:", "Target Platform:"), ["TikTok (15-60s)", "Instagram Reels (30-60s)", "YouTube Shorts (60s)", "YouTube Long-form (5m+)"])
            tone = st.selectbox(t("نبرة الصوت (Tone):", "Voice Tone:"), [t("حيوي ومثير (Energetic)", "Energetic & Exciting"), t("درامي وغموض (Dramatic)", "Dramatic & Hooking"), t("تعليمي موثوق (Educational)", "Educational & Authoritative"), t("كوميدي (Humorous)", "Humorous")])
            
            submit_btn = st.form_submit_button(t("🚀 توليد السكريبت ومشاهد الفيديو", "🚀 Generate Script & Storyboard"), use_container_width=True, type="primary")

        if submit_btn and topic:
            with st.spinner(t("🧠 يتم الآن كتابة السكريبت وتصميم المشاهد المبدئية...", "🧠 Writing script & designing storyboards...")):
                sys_prompt = f"""You are OMNI-DIRECTOR, an elite Viral Video Strategist and Master Scriptwriter.
Your goal is to generate a high-retention video script that dominates the {platform} algorithm.

Creative Direction:
1. Hook Strategy: Use a psychological trigger (Curiosity, Fear of Missing Out, or Immediate Benefit) in the first 3 seconds.
2. Narrative Arc: Ensure a fast-paced 'Problem-Solution-Proof' flow.
3. Visual Richness: Scene descriptions must be cinematic, including specific lighting (e.g., 'Golden hour', 'Cyberpunk neon', 'Minimalist studio'), camera angles, and textures.
4. Retention: Include 'Text Overlay' instructions to keep users watching.

Output your response STRICTLY as valid JSON:
{{
  "title": "Elite Video Title",
  "hook": "Specific psychological hook (Text + Action)",
  "scenes": [
    {{
      "time": "0:00 - 0:05",
      "visual": "Cinematic visual prompt for AI generation",
      "audio": "Voiceover / SFX description",
      "text_overlay": "Main text on screen"
    }}
  ],
  "call_to_action": "High-intent CTA"
}}

Respond ONLY in valid JSON. Language: Arabic. Visual prompts in English for AI compatibility."""
                
                # Fetch text script
                json_str = structured_text_generation(sys_prompt, f"Topic: {topic}")
                
                if json_str:
                    try:
                        # Clean markdown json block if present
                        json_str = json_str.strip()
                        if json_str.startswith("```json"): json_str = json_str[7:]
                        if json_str.endswith("```"): json_str = json_str[:-3]
                        
                        script_data = json.loads(json_str)
                        st.session_state.video_script_data = script_data
                        log_activity(st.session_state.username, f"Generated video script for: {topic}")
                    except Exception as e:
                        st.error(t("حدث خطأ في قراءة رد الذكاء الاصطناعي.", "Error parsing AI response."))
                        st.error(e)
                else:
                    st.error(t("فشل توليد النص، تأكد من إعدادات الـ API Gateway.", "Failed to generate script. Check API Gateway."))

        # Display Script & Generate Storyboards
        if st.session_state.get("video_script_data"):
            data = st.session_state.video_script_data
            
            st.success(f"🎥 {data['title']}")
            
            st.info(f"**⚓ {t('الخطاف (Hook - First 3 Secs):', 'The Hook (First 3 Secs):')}**\n\n{data['hook']}")
            
            for i, scene in enumerate(data['scenes']):
                scene_exp = st.expander(f"🎬 {t('المشهد', 'Scene')} {i+1} | ⏱️ {scene['time']}", expanded=True)
                with scene_exp:
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"**👁️ {t('المرئيات (Visual):', 'Visual:')}**\n{scene['visual']}")
                        st.markdown(f"**🔊 {t('الصوتيات (Audio):', 'Audio:')}**\n{scene['audio']}")
                        if scene.get("text_overlay"):
                            st.markdown(f"**🔤 {t('النص على الشاشة (Overlay):', 'Text Overlay:')}**\n`{scene['text_overlay']}`")
                        
                        # Generate Image Button for this specific scene
                        btn_key = f"gen_sb_{i}"
                        if st.button(f"🖼️ {t('توليد الصورة بـ DALL-E 3', 'Generate Storyboard Image (DALL-E 3)')}", key=btn_key):
                            with st.spinner(t("جاري التوليد باستخدام DALL-E 3...", "Generating via DALL-E 3...")):
                                enhanced_prompt = f"Cinematic video frame, {scene['visual']}, highly detailed, 8k resolution, photorealistic"
                                result_url = generate_image_advanced(enhanced_prompt, provider="openai")
                                if result_url:
                                    st.success(t("نجح التوليد!", "Generation successful!"))
                                    st.image(result_url)
                                else:
                                    st.error(t("❌ فشل الاتصال بـ DALL-E. يرجى التأكد من صلاحية مفتاح الخصوصية ورصيده، أو مراجعة سجلات الـ Console لمعرفة الخطأ الدقيق.", "❌ Connection error with DALL-E. Please verify your API Key/Quota or check Console Logs for details."))
    
    # ==============================
    # TAB 2: VIDEO AD INTELLIGENCE
    # ==============================
    with tab2:
        st.markdown(f"### 🕵️ {t('تحليل إعلانات الفيديو (Video Intel)', 'Video Ad Analyzer')}")
        st.write(t("قم برفع إعلانات منافسيك لتحليل الإستراتيجية المستخدمة فيها ثانية بثانية.", "Upload competitor ads to analyze their strategy second-by-second."))
        
        if st.session_state.plan not in ["Command", "Business"]:
            st.warning(t("هذه الميزة (تحليل فيديوهات كاملة بـ Gemini 1.5 Pro) متاحة فقط لخطة Command.", "Full video analysis (Gemini 1.5 Pro) requires the Command plan."))
        
        uploaded_ad = st.file_uploader(t("ارفع الفيديو (MP4/MOV)", "Upload Video (MP4/MOV)"), type=["mp4", "mov", "avi"], key="intel_vid")
        
        if uploaded_ad:
            st.video(uploaded_ad)
            if st.button(t("🚀 ابدأ تحليل الإعلان (Intelligence Scan)", "🚀 Start Intelligence Scan"), type="primary"):
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_ad.name)[1]) as tmp:
                    tmp.write(uploaded_ad.getvalue())
                    tmp_ad_path = tmp.name

                try:
                    with st.spinner(t("يتم معالجة الإطارات واستخراج الاستراتيجية...", "Processing frames and extracting strategy...")):
                        analyzer = get_video_analyzer()
                        res = analyzer.analyze_video(tmp_ad_path)
                        if "error" in res:
                            st.error(f"Error: {res['error']}")
                        else:
                            st.session_state.video_intel_result = res
                            log_activity(st.session_state.username, f"Analyzed competitor video: {uploaded_ad.name}")
                finally:
                    if os.path.exists(tmp_ad_path): os.remove(tmp_ad_path)

        if st.session_state.get("video_intel_result"):
            res = st.session_state.video_intel_result
            st.markdown("---")
            c1, c2 = st.columns([1, 1])
            with c1:
                st.metric(t("التقييم العام للخطاف", "Hook Rating"), f"{res['overall_score']}/100")
                st.info(f"**{t('الخطاف:', 'Hook:')}**\n{res['hook_effectiveness']}")
            with c2:
                st.success(f"**{t('السرعة البصرية:', 'Pacing:')}**\n{res['visual_pacing']}")
                st.warning(f"**{t('السيناريو:', 'Script:')}**\n{res['script_quality']}")
            
            st.markdown(f"#### 🏆 {t('خلاصة الإستراتيجية (Strategy Breakdown)', 'Strategy Breakdown')}")
            st.write(res['final_recommendation'])
