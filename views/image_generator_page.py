# ==========================================================
# MTSE v13 - AI Image Studio
# Generate marketing images using DALL-E 3 / Stable Diffusion
# ==========================================================

import streamlit as st
from utils import t

def call_dalle(prompt: str, size: str = "1024x1024", quality: str = "standard") -> str | None:
    """Generate image using DALL-E 3 via OpenAI API."""
    try:
        from ai_engine.ai_gateway import get_api_key
        import openai
        key = get_api_key("openai")
        if not key:
            return None
        client = openai.OpenAI(api_key=key)
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality=quality,
            n=1,
        )
        return response.data[0].url
    except Exception as e:
        st.error(f"DALL-E Error: {e}")
        return None


def translate_to_english(text: str) -> str:
    """Translate Arabic text to English for DALL-E prompts."""
    try:
        from ai_engine.ai_gateway import get_api_key
        import openai
        key = get_api_key("openai")
        if not key:
            return text
        client = openai.OpenAI(api_key=key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a translator. Translate the user's text to English for use as an image generation prompt. Return only the English translation, nothing else."},
                {"role": "user", "content": text}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return text


def render():
    from config import PRIMARY, PRIMARY_LIGHT, ACCENT, NEON_GREEN

    st.markdown(f"""
    <div class="tool-header animate-in">
        <div class="tool-header-icon">🖼️</div>
        <h2>{t("استوديو الصور بالذكاء الاصطناعي", "AI Image Studio")}</h2>
        <p style="color:#94a3b8; margin:4px 0;">{t("توليد صور تسويقية احترافية بقوة DALL-E 3", "Generate professional marketing images powered by DALL-E 3")}</p>
        <span class="badge badge-primary">DALL-E 3 · GPT-4o Vision</span>
    </div>
    """, unsafe_allow_html=True)

    col_controls, col_output = st.columns([1, 1.2])

    with col_controls:
        st.markdown(f"### 🎨 {t('إعدادات التوليد', 'Generation Settings')}")

        prompt_ar = st.text_area(
            t("وصف الصورة", "Image Description"),
            placeholder=t(
                "مثال: صورة احترافية لمنتج تسويقي فاخر على خلفية داكنة مع إضاءة نيون...",
                "Example: Professional luxury product shot on dark background with neon lighting..."
            ),
            height=120,
            key="img_prompt_ar"
        )

        style_col, size_col = st.columns(2)
        with style_col:
            style = st.selectbox(
                t("نمط الصورة", "Image Style"),
                [
                    t("فوتوريالستي", "Photorealistic"),
                    t("احترافي للتجارة", "Commercial Product"),
                    t("فني رقمي", "Digital Art"),
                    t("سينمائي", "Cinematic"),
                    t("مسطح حديث", "Flat Modern"),
                    t("مستوحى من الذكاء الاصطناعي", "AI Aesthetic"),
                ],
                key="img_style"
            )

        with size_col:
            size_map = {
                t("مربع 1:1", "Square 1:1"): "1024x1024",
                t("أفقي 16:9", "Landscape 16:9"): "1792x1024",
                t("عمودي 9:16", "Portrait 9:16"): "1024x1792",
            }
            size_label = st.selectbox(
                t("الحجم", "Size"),
                list(size_map.keys()),
                key="img_size"
            )

        quality = st.radio(
            t("الجودة", "Quality"),
            [t("قياسية", "standard"), t("عالية HD", "hd")],
            horizontal=True,
            key="img_quality"
        )
        quality_val = "hd" if "hd" in quality or "HD" in quality else "standard"

        brand_context = st.text_input(
            t("السياق الإضافي (اختياري)", "Brand Context (optional)"),
            placeholder=t("مثال: علامة تجارية فاخرة، ألوان زرقاء وذهبية", "E.g: Luxury brand, blue and gold colors"),
            key="img_brand"
        )

        n_variations = st.slider(
            t("عدد الصور", "Number of Images"),
            min_value=1, max_value=3, value=1,
            key="img_variations"
        )

        generate_btn = st.button(
            t("🎨 توليد الصورة", "🎨 Generate Image"),
            use_container_width=True,
            type="primary",
            key="generate_img_btn"
        )

    with col_output:
        st.markdown(f"### 🖼️ {t('الصور المولدة', 'Generated Images')}")

        if generate_btn:
            if not prompt_ar:
                st.warning(t("يرجى إدخال وصف للصورة", "Please enter an image description"))
            else:
                # Build enhanced prompt
                style_suffix_map = {
                    t("فوتوريالستي", "Photorealistic"): "photorealistic, ultra detailed, 8K resolution",
                    t("احترافي للتجارة", "Commercial Product"): "professional commercial photography, studio lighting, white background, product shot",
                    t("فني رقمي", "Digital Art"): "digital art, vibrant colors, artistic, concept art",
                    t("سينمائي", "Cinematic"): "cinematic, dramatic lighting, movie poster quality, widescreen",
                    t("مسطح حديث", "Flat Modern"): "flat design, modern, clean, minimalist, vector art style",
                    t("مستوحى من الذكاء الاصطناعي", "AI Aesthetic"): "AI aesthetic, futuristic, neon glow, cyberpunk, holographic",
                }
                style_suffix = style_suffix_map.get(style, "photorealistic")

                with st.spinner(t("⏳ جاري التوليد...", "⏳ Generating...")):
                    # Translate if Arabic
                    base_prompt = translate_to_english(prompt_ar) if any('\u0600' <= c <= '\u06ff' for c in prompt_ar) else prompt_ar
                    brand_en = translate_to_english(brand_context) if brand_context and any('\u0600' <= c <= '\u06ff' for c in brand_context) else brand_context

                    final_prompt = f"{base_prompt}, {style_suffix}"
                    if brand_en:
                        final_prompt += f", {brand_en}"
                    final_prompt += ", high quality, professional marketing image"

                    st.session_state["last_img_prompt"] = final_prompt

                    from ai_engine.ai_gateway import get_api_key
                    has_api_key = bool(get_api_key("openai"))

                    if has_api_key:
                        for i in range(n_variations):
                            with st.spinner(f"{t('توليد صورة', 'Generating image')} {i+1}/{n_variations}..."):
                                img_url = call_dalle(final_prompt, size=size_map[size_label], quality=quality_val)
                                if img_url:
                                    st.image(img_url, caption=f"Image {i+1} — {style}", use_column_width=True)
                                    st.markdown(f"[📥 {t('تحميل', 'Download')}]({img_url})", unsafe_allow_html=False)
                    else:
                        # Demo mode
                        st.info(f"🔑 {t('لا يوجد مفتاح OPENAI_API_KEY — وضع العرض التجريبي', 'No OPENAI_API_KEY configured — Demo mode')}")
                        st.markdown(f"""
                        <div class="ai-output">
                            <strong>✅ {t('البرومت النهائي (سيُرسل لـ DALL-E 3):', 'Final prompt (to be sent to DALL-E 3):')}</strong><br><br>
                            {final_prompt}
                        </div>
                        """, unsafe_allow_html=True)

                        # Show placeholder demo images from Picsum
                        seed = abs(hash(final_prompt[:50])) % 1000
                        demo_url = f"https://picsum.photos/seed/{seed}/800/600"
                        st.image(demo_url, caption=f"🎨 Demo Preview — {style}", use_column_width=True)
                        st.caption(t("هذه صورة تجريبية. أضف مفتاح OPENAI_API_KEY للتوليد الحقيقي.", "This is a demo image. Add OPENAI_API_KEY for real generation."))

        else:
            st.markdown(f"""
            <div style="text-align:center; padding:60px 20px; color:#475569; border:2px dashed rgba(124,58,237,0.2); border-radius:20px;">
                <div style="font-size:3rem; margin-bottom:12px;">🎨</div>
                <div style="font-size:1rem; color:#64748b;">{t("ستظهر صورتك هنا بعد التوليد", "Your generated image will appear here")}</div>
                <div style="font-size:0.8rem; margin-top:8px; color:#475569;">DALL-E 3 · Ultra HD · Professional</div>
            </div>
            """, unsafe_allow_html=True)

    # Tips section
    st.markdown("---")
    st.markdown(f"### 💡 {t('نصائح للحصول على أفضل نتائج', 'Tips for Best Results')}")
    tips = [
        (t("كن محدداً", "Be Specific"), t("اذكر الألوان والأسلوب والمشاعر التي تريد إيصالها", "Mention colors, style, and emotions you want to convey")),
        (t("أضف السياق التجاري", "Add Brand Context"), t("حدد طبيعة علامتك التجارية ليفهم الذكاء الاصطناعي التوجه", "Specify your brand nature so AI understands the direction")),
        (t("اختر الحجم المناسب", "Choose Right Size"), t("9:16 للقصص، 1:1 لنشرات الفيد، 16:9 للبانرات", "9:16 for Stories, 1:1 for Feed posts, 16:9 for Banners")),
        (t("جودة HD", "HD Quality"), t("استخدم الجودة العالية للإعلانات المدفوعة", "Use HD quality for paid advertising creatives")),
    ]
    tip_cols = st.columns(4)
    for col, (tip_title, tip_desc) in zip(tip_cols, tips):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="text-align:right; min-height:120px;">
                <div class="feature-title" style="font-size:0.9rem;">💡 {tip_title}</div>
                <div class="feature-desc">{tip_desc}</div>
            </div>
            """, unsafe_allow_html=True)
