import streamlit as st
import json
from utils import t, render_section_header
from ai_engine.ai_gateway import structured_text_generation, generate_image_advanced
from database import log_activity

def render():
    st.markdown(f"""
    <div class="hero-v13" style="padding:40px 20px; border-radius:16px; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);">
        <h2 class="hero-title" style="font-size:2.5rem; margin-bottom:10px;">🚀 {t("غرفة العمليات الابتكارية", "Campaign Command Hub")}</h2>
        <p class="hero-subtitle" style="margin-bottom:0; color:#fff;">{t("أتمتة الحملات الشاملة (v13.5). ضغطة واحدة لتوليد استراتيجية كاملة عبر جميع المنصات.", "Unified Campaign Automation (v13.5) - One click omnichannel deployment.")}</p>
    </div>
    <br/>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        campaign_goal = st.text_input(t("هدف الحملة (المنتج/العرض):", "Campaign Objective:"), placeholder=t("مثال: إطلاق عطر صيفي جديد، زيادة مبيعات العقارات...", "e.g. Summer perfume launch..."))
        target_audience = st.text_input(t("الجمهور المستهدف:", "Target Audience:"), placeholder=t("مثال: الشباب من 18-25، المهتمين بالفخامة...", "e.g. Youth 18-25, Luxury buyers..."))
    with col2:
        platforms = st.multiselect(t("المنصات المستهدفة:", "Target Platforms:"), ["TikTok", "Instagram", "Facebook", "Email", "YouTube", "X (Twitter)"], default=["Facebook", "Instagram", "Email"])
        tone = st.selectbox(t("نبرة الصوت (Tone):", "Voice Tone:"), [t("احترافي", "Professional"), t("عاطفي/مؤثر", "Emotional"), t("شبابي/عفوي", "Casual/Youthful"), t("تسويقي/مباشر", "Direct Sales")])

    if st.button(t("🚀 توليد الحملة المتكاملة (1-Click)", "🚀 Generate Unified Campaign"), use_container_width=True, type="primary"):
        if not campaign_goal or not platforms:
            st.error(t("يرجى إدخال هدف الحملة واختيار منصة واحدة على الأقل.", "Please enter a campaign goal and select at least one platform."))
            return

        with st.status(t("جاري التوليد وربط الذكاء الاصطناعي متعدد الأبعاد...", "Orchestrating multi-modal AI generation..."), expanded=True) as status:
            st.write(t("🧠 تحليل السوق وتوليد المحتوى بـ GPT-4o...", "Analyzing market & generating content..."))
            
            # Construct JSON schema dynamically based on requested platforms
            schema_parts = []
            if "Facebook" in platforms:
                schema_parts.append('"Facebook": {"post_text": "Engaging FB post", "image_prompt": "Cinematic visual description for the post image..."}')
            if "Instagram" in platforms:
                schema_parts.append('"Instagram": {"caption": "IG Caption with emojis", "hashtags": "#like #this"}')
            if "Email" in platforms:
                schema_parts.append('"Email": {"subject": "Catchy subject line", "body": "Full persuasive email body"}')
            if "TikTok" in platforms:
                schema_parts.append('"TikTok": {"hook": "First 3s text", "script": "Full script", "visuals": "What is shown"}')
            if "YouTube" in platforms:
                schema_parts.append('"YouTube": {"title": "YT Title", "description": "YT Desc", "thumbnail_idea": "Visual for thumbnail"}')
            if "X (Twitter)" in platforms:
                schema_parts.append('"X": {"tweet": "Persuasive tweet text with hashtags"}')
            
            schema_json = "{" + ", ".join(schema_parts) + ", \"Strategy\": \"Overall 1-paragraph summary\"}"

            sys_prompt = f"""You are OMNI-STRATEGIST, a world-class AI Marketing Director with 20+ years of experience in global brand scaling.
Your goal is to create a masterpiece omnichannel campaign for: {campaign_goal}.

Strategic Methodology:
1. Conduct a brief mental SWOT analysis based on the product.
2. Generate highly persuasive, high-converting copy tailored to each platform's unique psychology.
3. For Facebook: focus on social proof and community triggers.
4. For Instagram: focus on lifestyle, aesthetics, and aspirational value.
5. For Email: use a 'Problem-Agitate-Solve' (PAS) framework with extreme professional polish.
6. For TikTok/YouTube: focus on 'The Hook' (retention editing style) and 'The Value'.

Output ONLY valid JSON corresponding to this schema (Do NOT use Markdown wrapping):
{schema_json}

Write all content in professional and highly engaging Arabic. Ensure 'image_prompt' or 'thumbnail_idea' fields are written as cinematic photorealistic DALL-E 3 prompts in English for best quality."""
            
            json_res = structured_text_generation(sys_prompt, "Generate the elite campaign now.")
            
            if json_res:
                try:
                    json_res = json_res.strip()
                    if json_res.startswith("```json"): json_res = json_res[7:]
                    if json_res.endswith("```"): json_res = json_res[:-3]
                    
                    campaign_data = json.loads(json_res)
                    st.session_state.unified_campaign = campaign_data
                    
                    st.write(t("🖼️ توليد الصور للحملة عبر DALL-E 3...", "Generating core image assets via DALL-E 3..."))
                    
                    # Try to generate specific images if requested
                    if "Facebook" in campaign_data and "image_prompt" in campaign_data["Facebook"]:
                        img_url = generate_image_advanced("Professional marketing photography: " + campaign_data["Facebook"]["image_prompt"], provider="openai")
                        st.session_state.unified_campaign["_fb_image"] = img_url
                        
                    log_activity(st.session_state.username, f"Generated Omnichannel Campaign for: {campaign_goal}")
                    status.update(label=t("✅ اكتمل توليد الحملة المتكاملة!", "✅ Unified Campaign Generated!"), state="complete")
                    
                except Exception as e:
                    st.error(f"Failed to parse or generate: {e}")
                    status.update(label="❌ Error", state="error")
            else:
                st.error("API Error")
                status.update(label="❌ Failed", state="error")

    # Display Results
    if st.session_state.get("unified_campaign"):
        cd = st.session_state.unified_campaign
        
        st.success(f"**{t('الاستراتيجية العامة:', 'Overall Strategy:')}** {cd.get('Strategy', '')}")
        
        # Tabs for each platform requested
        avail_platforms = [p for p in ["Facebook", "Instagram", "Email", "TikTok", "YouTube"] if p in cd]
        if avail_platforms:
            tabs = st.tabs([f"📱 {p}" for p in avail_platforms])
            
            for index, p in enumerate(avail_platforms):
                with tabs[index]:
                    data = cd[p]
                    if p == "Facebook":
                        st.markdown(f"**نص المنشور:**\n\n{data.get('post_text', '')}")
                        st.info(f"**اقتراح صورة التصميم:**\n{data.get('image_prompt', '')}")
                        if cd.get("_fb_image"):
                            st.image(cd["_fb_image"], caption="Generated via DALL-E 3")
                        elif data.get('image_prompt'):
                            st.warning(t("تأكد من تفعيل مفتاح OpenAI لتوليد الصورة فوراً.", "Ensure OpenAI API key is active to auto-generate image."))
                            
                    elif p == "Instagram":
                        st.markdown(f"**التعليق (Caption):**\n\n{data.get('caption', '')}")
                        st.markdown(f"**الهاشتاجات:** {data.get('hashtags', '')}")
                        
                    elif p == "Email":
                        st.markdown(f"**موضوع الإيميل (Subject):**\n`{data.get('subject', '')}`")
                        st.markdown(f"**نص الإيميل (Body):**\n\n{data.get('body', '')}")
                        
                    elif p == "TikTok":
                        st.markdown(f"**الخطاف (Hook):**\n`{data.get('hook', '')}`")
                        st.markdown(f"**السكريبت:**\n\n{data.get('script', '')}")
                        st.info(f"**المشاهد (Visuals):**\n{data.get('visuals', '')}")
                        
                    elif p == "YouTube":
                        st.markdown(f"**العنوان (Title):**\n`{data.get('title', '')}`")
                        st.markdown(f"**الوصف (Description):**\n\n{data.get('description', '')}")
                        st.info(f"**فكرة الصورة المصغرة (Thumbnail):**\n{data.get('thumbnail_idea', '')}")
                        
                    elif p == "X (Twitter)":
                        st.markdown(f"**نص التغريدة (Tweet):**\n\n{data.get('tweet', '')}")
                    
                    # --- SHARED PUBLISH BUTTON ---
                    if p in ["Facebook", "Instagram", "X (Twitter)"]:
                        if st.button(t(f"🚀 جدولة/نشر لـ {p}", f"🚀 Schedule/Publish to {p}"), key=f"pub_{p}"):
                            from database import save_scheduled_post
                            from views.social_command_page import _try_publish
                            
                            content_to_pub = data.get('post_text') or data.get('tweet') or data.get('caption')
                            custom_keys = st.session_state.get("custom_keys", {})
                            
                            with st.spinner(t("جاري النشر المباشر...", "Direct publishing in progress...")):
                                success, msg = _try_publish(content_to_pub, [f"{p}"], custom_keys)
                                status_db = "Published" if success else "Queued"
                                save_scheduled_post(st.session_state.username, content_to_pub, [p], None, None, status=status_db)
                                
                                if success: st.success(t("✅ تم النشر فوراً!", "✅ Published instantly!"))
                                else: st.info(t("✅ تم حفظ المنشور في قائمة الانتظار (Social Command).", "✅ Saved to publishing queue (Social Command)."))

        st.markdown("---")
        if st.button("📥 تحميل الحملة كاملة كملف (Branded PDF)", use_container_width=True):
            from utils import generate_branded_pdf, t
            from database import get_user_branding
            
            brand = get_user_branding(st.session_state.username)
            pdf_data = {
                "title": t("خطة الحملة التسويقية (Omnichannel)", "Marketing Campaign Plan"),
                "sections": [{"heading": t("استراتيجية الحملة", "Strategy Overview"), "content": cd.get('Strategy', '')}]
            }
            
            for p in avail_platforms:
                content_str = ""
                for k, v in cd[p].items():
                    content_str += f"{k.title()}:\n{v}\n\n"
                pdf_data["sections"].append({"heading": f"منصة {p}", "content": content_str})
                
            pdf_bytes = generate_branded_pdf(pdf_data, brand_data=brand)
            if pdf_bytes:
                st.download_button(t("📥 اضغط للتحميل الفعلي (PDF)", "📥 Click to Download PDF"), pdf_bytes, "campaign_plan.pdf", "application/pdf", use_container_width=True)
            else:
                st.error("فشل تكوين ملف الـ PDF. جرب مرة أخرى.")
