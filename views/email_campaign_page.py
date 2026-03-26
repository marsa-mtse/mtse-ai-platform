# ==========================================================
# MTSE v13 - Email Campaign Builder
# Generate complete email sequences with AI
# ==========================================================

import streamlit as st
from utils import t


def generate_email_sequence(campaign_goal: str, brand: str, audience: str,
                             email_count: int, sequence_type: str, lang: str) -> list:
    """Generate a complete email sequence using AI Gateway."""
    from ai_engine.ai_gateway import structured_text_generation
    
    lang_instruction = "Arabic (use professional marketing Arabic, RTL)" if lang == "AR" else "English"
    
    system_prompt = f"""You are a world-class email marketing copywriter specializing in high-converting email sequences.
    Write emails that feel personal, compelling, and drive action.
    Always respond in {lang_instruction}."""

    user_prompt = f"""
    Create a {email_count}-email {sequence_type} sequence for:
    - Brand: {brand}
    - Campaign Goal: {campaign_goal}
    - Target Audience: {audience}
    
    For each email provide:
    1. Subject Line (with emoji, A/B variant)
    2. Preview Text
    3. Body (personalized, compelling, with clear CTA)
    4. Send Timing (e.g., "Day 1", "Day 3")
    5. Expected Open Rate Prediction
    
    Make each email feel personal and avoid spam triggers.
    Format as Email 1:, Email 2:, etc.
    """

    return structured_text_generation(system_prompt, user_prompt, preferred_provider="openai")


def render():
    from config import PRIMARY, PRIMARY_LIGHT, ACCENT, NEON_GREEN

    st.markdown(f"""
    <div class="tool-header animate-in">
        <div class="tool-header-icon">📧</div>
        <h2>{t("مُنشئ حملات البريد الإلكتروني", "Email Campaign Builder")}</h2>
        <p style="color:#94a3b8;">{t("أنشئ سلاسل بريدية كاملة وعالية التحويل بقوة GPT-4o", "Build complete, high-converting email sequences powered by GPT-4o")}</p>
        <span class="badge badge-primary">GPT-4o · Email Marketing · High-Converting</span>
    </div>
    """, unsafe_allow_html=True)

    col_settings, col_output = st.columns([1, 1.4])

    with col_settings:
        st.markdown(f"### ⚙️ {t('إعدادات الحملة', 'Campaign Settings')}")

        brand_name = st.text_input(
            t("اسم العلامة التجارية", "Brand Name"),
            placeholder=t("مثال: MTSE Digital", "e.g: MTSE Digital"),
            key="email_brand"
        )

        campaign_goal = st.text_area(
            t("هدف الحملة", "Campaign Goal"),
            placeholder=t(
                "مثال: الترويج لمنتج جديد وتحويل المشتركين إلى عملاء",
                "e.g: Promote a new product and convert subscribers to customers"
            ),
            height=90,
            key="email_goal"
        )

        target_audience = st.text_input(
            t("الجمهور المستهدف", "Target Audience"),
            placeholder=t("مثال: أصحاب الشركات الصغيرة، 25-45 سنة", "e.g: Small business owners, 25-45 years old"),
            key="email_audience"
        )

        sequence_type = st.selectbox(
            t("نوع السلسلة", "Sequence Type"),
            [
                t("ترحيب بمشتركين جدد", "Welcome Series"),
                t("تحويل (Nurture) تدريجي", "Nurture Sequence"),
                t("ترويج لمنتج / خدمة", "Product Promotion"),
                t("استرداد العملاء الغائبين", "Re-engagement"),
                t("متابعة ما بعد الشراء", "Post-Purchase"),
                t("إطلاق منتج جديد", "Product Launch"),
                t("سلسلة تعليمية", "Educational Series"),
            ],
            key="email_seq_type"
        )

        email_count = st.slider(
            t("عدد الرسائل في السلسلة", "Number of Emails"),
            min_value=3, max_value=10, value=5,
            key="email_count"
        )

        include_subject_ab = st.checkbox(
            t("تضمين اختبار A/B للعناوين", "Include Subject Line A/B Tests"),
            value=True,
            key="email_ab"
        )

        generate_btn = st.button(
            t("📧 إنشاء سلسلة البريد", "📧 Generate Email Sequence"),
            use_container_width=True,
            type="primary",
            key="gen_email_btn"
        )

    with col_output:
        st.markdown(f"### 📬 {t('سلسلة البريد المولّدة', 'Generated Email Sequence')}")

        if generate_btn:
            if not campaign_goal or not brand_name:
                st.warning(t("يرجى إدخال اسم العلامة التجارية وهدف الحملة", "Please enter brand name and campaign goal"))
            else:
                lang = st.session_state.get("lang", "AR")
                with st.spinner(t(f"✍️ جاري كتابة {email_count} رسائل...", f"✍️ Writing {email_count} emails...")):
                    result = generate_email_sequence(
                        campaign_goal, brand_name, target_audience or t("جمهور عام", "General Audience"),
                        email_count, sequence_type, lang
                    )

                    if result:
                        # Stats preview
                        stat_c1, stat_c2, stat_c3 = st.columns(3)
                        with stat_c1:
                            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">{email_count}</div>
                            <div class="kpi-label">{t("رسائل", "Emails")}</div></div>""", unsafe_allow_html=True)
                        with stat_c2:
                            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">~32%</div>
                            <div class="kpi-label">{t("معدل فتح متوقع", "Expected Open Rate")}</div></div>""", unsafe_allow_html=True)
                        with stat_c3:
                            st.markdown(f"""<div class="kpi-card"><div class="kpi-value">A/B</div>
                            <div class="kpi-label">{t("اختبارات العناوين", "Subject Tests")}</div></div>""", unsafe_allow_html=True)

                        st.markdown(f"""
                        <div class="ai-output animate-in" style="margin-top:16px; direction:{'rtl' if lang == 'AR' else 'ltr'};">
                            {result.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)

                        # Export buttons
                        export_c1, export_c2 = st.columns(2)
                        with export_c1:
                            st.download_button(
                                label=t("📥 تحميل كـ TXT", "📥 Download as TXT"),
                                data=result,
                                file_name=f"email_campaign_{brand_name}.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                        with export_c2:
                            st.button(t("📋 نسخ الكل", "📋 Copy All"), use_container_width=True)
                    else:
                        # Demo mode
                        st.info(t("وضع تجريبي — أضف OPENAI_API_KEY للتوليد الحقيقي", "Demo Mode — Add OPENAI_API_KEY"))
                        _show_demo_emails(brand_name, email_count, sequence_type, lang)

        else:
            st.markdown(f"""
            <div style="text-align:center; padding:60px 20px; border:2px dashed rgba(124,58,237,0.2); border-radius:20px;">
                <div style="font-size:3rem; margin-bottom:12px;">📧</div>
                <div style="color:#64748b; font-size:1rem;">{t("سلسلة رسائلك ستظهر هنا", "Your email sequence will appear here")}</div>
                <div style="font-size:0.8rem; margin-top:8px; color:#475569;">GPT-4o · High-Converting Copy</div>
            </div>
            """, unsafe_allow_html=True)

    # Best practices
    st.markdown("---")
    st.markdown(f"### 📚 {t('أفضل الممارسات للبريد الإلكتروني', 'Email Best Practices')}")
    practices = [
        ("📝", t("عنوان جذاب", "Compelling Subject"), t("استخدم أرقاماً وعواطف في العنوان، 40-50 حرف مثالي", "Use numbers & emotions, 40-50 chars ideal")),
        ("⏰", t("التوقيت المثالي", "Optimal Timing"), t("الثلاثاء والخميس 9-11 صباحاً أو 7-9 مساءً", "Tue & Thu 9-11am or 7-9pm local time")),
        ("🎯", t("شخصنة المحتوى", "Personalization"), t("ابدأ بالاسم ووفر محتوى يتحدث مباشرة لمشاكل القارئ", "Start with name, speak directly to reader's pain")),
        ("📲", t("تصميم متجاوب", "Mobile-First Design"), t("60% يقرؤون البريد على الجوال — تحسين للشاشات الصغيرة", "60% read on mobile — optimize for small screens")),
    ]
    p_cols = st.columns(4)
    for col, (icon, title, desc) in zip(p_cols, practices):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="text-align:right; min-height:120px;">
                <div style="font-size:1.5rem;">{icon}</div>
                <div class="feature-title" style="font-size:0.9rem; margin-top:8px;">{title}</div>
                <div class="feature-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


def _show_demo_emails(brand: str, count: int, seq_type: str, lang: str):
    """Demo email sequence."""
    demo = f"""
📧 **Email 1 — Day 1: {t("مرحباً بك!", "Welcome!")}**

**{t("العنوان", "Subject")}:** 🎉 {t("مرحباً في عائلة", "Welcome to")} {brand}!
**{t("نص المعاينة", "Preview")}:** {t("خطوتك الأولى نحو النجاح تبدأ من هنا...", "Your first step to success starts here...")}

{t("مرحباً [الاسم]،", "Hi [First Name],")}

{t("نحن سعداء جداً لانضمامك إلى", "We're thrilled to have you join")} {brand}!

{t("في الأيام القادمة ستتلقى:", "Over the next few days, you'll receive:")}
✅ {t("نصائح عملية قابلة للتطبيق فوراً", "Immediately actionable tips")}
✅ {t("موارد حصرية لمشتركينا فقط", "Exclusive resources for subscribers only")}  
✅ {t("عروض خاصة لن تجدها في أي مكان", "Special offers you won't find anywhere else")}

{t('احصل على اول خطوة →', 'Get your first step →')} [CTA Button]

📧 **Email 2 — Day 3: {t("القيمة الأولى", "First Value")}**

**{t("العنوان", "Subject")}:** 💡 {t("السر الذي لا يعرفه 90% من", "The secret 90% of")} {t("رواد الأعمال", "entrepreneurs")} {t("لا يعرفه", "don't know")}
...

⚠️ {t("وضع تجريبي — أضف OPENAI_API_KEY للحصول على", "Demo Mode — Add OPENAI_API_KEY for")} {count} {t("رسائل كاملة", "complete emails")}
    """
    st.markdown(f"""
    <div class="ai-output" style="direction:{'rtl' if lang == 'AR' else 'ltr'};">
        {demo.replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)
