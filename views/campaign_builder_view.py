import streamlit as st
import time
import json
from utils import t, render_section_header
from ai_engine.router import router
from ai_engine.universal_analyzer import _safe_get_secret

# ─── AI Content Generator ────────────────────────────────────────────────────
def _generate_campaign_content(goal: str, audience: str, platforms: list,
                                tone: str, lang_out: str) -> dict:
    """Uses available AI backend to generate real campaign content."""
    try:
        import google.generativeai as genai
        key = _safe_get_secret("GOOGLE_API_KEY")
        if key and genai:
            genai.configure(api_key=key.strip())
            lang_instruction = (
                "باللغة العربية" if lang_out == "AR" else
                "in English" if lang_out == "EN" else
                "bilingual (Arabic first, then English)"
            )
            prompt = f"""
You are an elite digital marketing strategist for MENA & global markets.
Generate a complete, professional multi-platform campaign.

Campaign Goal: {goal}
Target Audience: {audience}
Platforms: {', '.join(platforms)}
Creative Tone: {tone}
Language: {lang_instruction}

Output a valid JSON with this exact structure:
{{
  "campaign_name": "...",
  "tagline": "...",
  "hook": "...",
  "strategy_overview": "...",
  "content": {{
    "TikTok": "...",
    "Instagram": "...",
    "Facebook": "...",
    "YouTube": "...",
    "Email": "..."
  }},
  "hashtags": ["...", "...", "..."],
  "cta": "...",
  "kpis": ["...", "...", "..."],
  "budget_tips": "...",
  "best_posting_times": "..."
}}
Only include keys for the platforms listed: {', '.join(platforms)}.
Make each platform's content SPECIFIC to that platform (format, length, style).
            """
            model = genai.GenerativeModel("gemini-2.0-flash")
            resp  = model.generate_content(prompt)
            txt   = resp.text.replace("```json","").replace("```","").strip()
            start = txt.find("{"); end = txt.rfind("}")
            if start != -1 and end != -1:
                return json.loads(txt[start:end+1])
    except Exception as e:
        st.session_state.last_ai_error = f"Gemini: {e}"

    # Groq fallback
    try:
        import groq as groq_lib
        key = _safe_get_secret("GROQ_API_KEY")
        if key:
            client = groq_lib.Groq(api_key=key.strip())
            prompt = f"Generate a complete campaign JSON for: Goal={goal}, Audience={audience}, Platforms={platforms}, Tone={tone}. Output JSON with keys: campaign_name, tagline, hook, strategy_overview, content (dict per platform), hashtags, cta, kpis, budget_tips, best_posting_times."
            for mdl in ["llama-3.3-70b-versatile","llama-3.1-70b-versatile"]:
                try:
                    r = client.chat.completions.create(
                        model=mdl,
                        messages=[{"role":"user","content":prompt}],
                        response_format={"type":"json_object"}
                    )
                    return json.loads(r.choices[0].message.content)
                except Exception:
                    continue
    except Exception as e:
        st.session_state.last_ai_error = f"Groq: {e}"

    # Structured fallback
    return {
        "campaign_name": f"Campaign: {goal[:40]}",
        "tagline": t("حملتك المثالية تبدأ من هنا", "Your perfect campaign starts here"),
        "hook": t(f"هل تعلم أن {audience} يبحث عن هذا؟", f"Did you know {audience} is looking for this?"),
        "strategy_overview": t(
            f"حملة متكاملة لـ {', '.join(platforms)} تستهدف {audience} بأسلوب {tone}.",
            f"Integrated campaign for {', '.join(platforms)} targeting {audience} with a {tone} tone."
        ),
        "content": {p: t(f"محتوى مخصص لـ {p} بناءً على هدف: {goal}", f"Custom {p} content based on goal: {goal}") for p in platforms},
        "hashtags": ["#MTSE", "#تسويق_رقمي", "#DigitalMarketing"],
        "cta": t("احجز الآن — العرض محدود!", "Book now — Limited offer!"),
        "kpis": [
            t("معدل التفاعل > 5%", "Engagement rate > 5%"),
            t("الوصول المستهدف 50,000", "Target reach 50,000"),
            t("معدل التحويل > 2%", "Conversion rate > 2%")
        ],
        "budget_tips": t("خصص 40% للفيديو و30% للصور الثابتة و30% للنصوص الإعلانية.", "Allocate 40% to video, 30% to static images, 30% to ad copy."),
        "best_posting_times": t("أفضل الأوقات: الثلاثاء والخميس 7-9م بتوقيت الخليج", "Best times: Tue & Thu 7-9pm Gulf Time")
    }

# ─── PLATFORM COLORS / ICONS ─────────────────────────────────────────────────
PLATFORM_META = {
    "TikTok":    {"icon": "🎵", "color": "#ff0050", "bg": "rgba(255,0,80,0.08)"},
    "Instagram": {"icon": "📸", "color": "#e1306c", "bg": "rgba(225,48,108,0.08)"},
    "Facebook":  {"icon": "📘", "color": "#1877f2", "bg": "rgba(24,119,242,0.08)"},
    "YouTube":   {"icon": "▶️", "color": "#ff0000", "bg": "rgba(255,0,0,0.08)"},
    "Email":     {"icon": "📧", "color": "#06b6d4", "bg": "rgba(6,182,212,0.08)"},
}

# ─── RENDER ───────────────────────────────────────────────────────────────────
def render():
    render_section_header(t("غرفة العمليات الابتكارية", "Campaign Command Hub"), "🚀")

    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(135deg, rgba(139,92,246,0.08), rgba(6,182,212,0.06)); border-bottom: 4px solid #8b5cf6; margin-bottom:24px;">
        <h2 style="margin:0 0 6px;">🚀 {t("توليد الحملات بالذكاء الاصطناعي", "AI-Powered Campaign Generator")}</h2>
        <p style="color:#94a3b8; margin:0;">{t("أدخل هدفك وجمهورك وسيقوم الذكاء الاصطناعي بتوليد محتوى احترافي لكل منصة.", "Enter your goal and audience — AI generates professional content for every platform.")}</p>
    </div>
    """, unsafe_allow_html=True)

    # ── INPUTS ─────────────────────────────────────────────────────────────────
    col1, col2 = st.columns([2, 1])
    with col1:
        campaign_goal = st.text_input(
            t("🎯 هدف الحملة *", "🎯 Campaign Objective *"),
            placeholder=t("مثال: زيادة مبيعات منتج العطور الجديد بنسبة 30%", "e.g. Boost new perfume sales by 30%"),
            key="camp_goal"
        )
        target_audience = st.text_input(
            t("👥 الجمهور المستهدف *", "👥 Target Audience *"),
            placeholder=t("مثال: سيدات 25-40، مهتمات بالتجميل، في السعودية والإمارات", "e.g. Women 25-40 interested in beauty, UAE & Saudi Arabia"),
            key="camp_audience"
        )

    with col2:
        platforms = st.multiselect(
            t("📱 المنصات المستهدفة", "📱 Target Platforms"),
            ["TikTok", "Instagram", "Facebook", "Email", "YouTube"],
            default=["TikTok", "Instagram"],
            key="camp_platforms"
        )
        tone = st.selectbox(
            t("🎨 أسلوب المحتوى", "🎨 Content Tone"),
            [
                t("احترافي ومرموق", "Professional & Prestigious"),
                t("ودود وقريب", "Friendly & Approachable"),
                t("جريء وعدواني", "Bold & Aggressive"),
                t("ملهم وتحفيزي", "Inspirational & Motivational"),
                t("مضحك وترفيهي", "Humorous & Entertainment"),
            ],
            key="camp_tone"
        )

    col_extra1, col_extra2, col_extra3 = st.columns(3)
    with col_extra1:
        budget = st.selectbox(
            t("💰 الميزانية التقديرية", "💰 Estimated Budget"),
            [t("أقل من $500", "Under $500"), "$500-$2,000", "$2,000-$10,000", t("أكثر من $10,000", "Over $10,000")],
            key="camp_budget"
        )
    with col_extra2:
        duration = st.selectbox(
            t("📅 مدة الحملة", "📅 Campaign Duration"),
            [t("أسبوع", "1 Week"), t("أسبوعان", "2 Weeks"), t("شهر", "1 Month"), t("3 أشهر", "3 Months")],
            key="camp_duration"
        )
    with col_extra3:
        lang_out = st.selectbox(
            t("🌍 لغة المخرجات", "🌍 Output Language"),
            [("AR", t("عربي", "Arabic")), ("EN", "English"), ("BOTH", t("الاثنين", "Bilingual"))],
            format_func=lambda x: x[1],
            key="camp_lang"
        )
        lang_out = lang_out[0]

    st.markdown("")
    generate_btn = st.button(
        "🚀  " + t("توليد الحملة الكاملة بالذكاء الاصطناعي", "Generate Full AI Campaign"),
        use_container_width=True,
        key="camp_generate"
    )

    if generate_btn:
        if not campaign_goal:
            st.error(t("⚠️ يرجى إدخال هدف الحملة أولاً.", "⚠️ Please enter a campaign objective first."))
        elif not platforms:
            st.error(t("⚠️ اختر منصة واحدة على الأقل.", "⚠️ Select at least one platform."))
        else:
            model_name = router.route_task("creative")
            steps = [
                t("🧠 تحليل السوق والمنافسين...", "🧠 Analyzing market & competitors..."),
                t("🎯 بناء شخصية المشتري المثالية...", "🎯 Building ideal buyer persona..."),
                t("✍️ توليد المحتوى لكل منصة...", "✍️ Generating platform-specific content..."),
                t("⚡ تحسين الـ Hooks والـ CTAs...", "⚡ Optimizing hooks & CTAs..."),
                t("📊 حساب مؤشرات الأداء المتوقعة...", "📊 Calculating expected KPIs..."),
            ]
            with st.status(t(f"جاري التوليد عبر {model_name}...", f"Generating via {model_name}..."), expanded=True) as status:
                for step in steps:
                    st.write(step)
                    time.sleep(0.8)
                result = _generate_campaign_content(campaign_goal, target_audience, platforms, tone, lang_out)
                st.session_state.campaign_result = result
                status.update(label=t("✅ الحملة جاهزة!", "✅ Campaign Ready!"), state="complete")

    # ── RESULTS ────────────────────────────────────────────────────────────────
    if st.session_state.get("campaign_result"):
        res = st.session_state.campaign_result
        st.markdown("---")

        # Campaign summary header
        st.markdown(f"""
        <div class="glass-card animate-in" style="border-top: 4px solid #8b5cf6; text-align:center; margin-bottom:20px;">
            <h2 style="background:linear-gradient(135deg,#c4b5fd,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:1.9rem;margin-bottom:6px;">
                🎯 {res.get('campaign_name', t('الحملة الجديدة','New Campaign'))}
            </h2>
            <p style="color:#94a3b8; font-size:1.05rem; font-style:italic;">"{res.get('tagline','')}"</p>
        </div>
        """, unsafe_allow_html=True)

        # KPI row
        kpis = res.get("kpis", [])
        if kpis:
            kpi_cols = st.columns(len(kpis))
            for i, kpi in enumerate(kpis[:4]):
                with kpi_cols[i]:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-icon">🎯</div>
                        <div class="kpi-label" style="font-size:0.8rem;color:#94a3b8;">{kpi}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("")

        # Hook & CTA
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"🪝 **{t('الـ Hook المثالي:', 'The Perfect Hook:')}**\n\n{res.get('hook', '')}")
        with c2:
            st.success(f"📣 **{t('نداء العمل (CTA):', 'Call To Action:')}**\n\n{res.get('cta', '')}")

        # Strategy overview
        with st.expander(t("📋 نظرة عامة على الاستراتيجية", "📋 Strategy Overview"), expanded=True):
            st.write(res.get("strategy_overview", ""))
            if res.get("best_posting_times"):
                st.markdown(f"🕐 **{t('أفضل أوقات النشر:', 'Best Posting Times:')}** {res.get('best_posting_times')}")
            if res.get("budget_tips"):
                st.markdown(f"💡 **{t('نصائح الميزانية:', 'Budget Tips:')}** {res.get('budget_tips')}")

        st.markdown(f"### 📱 {t('المحتوى المُولَّد لكل منصة', 'Generated Content per Platform')}")

        # Platform content tabs
        content_dict = res.get("content", {})
        available_platforms = [p for p in platforms if p in content_dict]
        if available_platforms:
            platform_tabs = st.tabs([
                f"{PLATFORM_META.get(p,{}).get('icon','📱')} {p}" for p in available_platforms
            ])
            for i, p in enumerate(available_platforms):
                meta = PLATFORM_META.get(p, {"color":"#8b5cf6","bg":"rgba(139,92,246,0.1)","icon":"📱"})
                with platform_tabs[i]:
                    st.markdown(f"""
                    <div style="
                        background: {meta['bg']};
                        border: 1px solid {meta['color']}44;
                        border-radius: 16px; padding: 22px 24px; margin-top:12px;
                    ">
                        <h3 style="color:{meta['color']}; margin-bottom:14px;">{meta['icon']} {p} Content</h3>
                        <div style="color:#e2e8f0; line-height:1.75; white-space:pre-wrap;">{content_dict.get(p,'')}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # Hashtags
        hashtags = res.get("hashtags", [])
        if hashtags:
            st.markdown(f"#### #{t('الهاشتاقات المقترحة', 'Suggested Hashtags')}")
            tags_html = " ".join([f'<span style="background:rgba(139,92,246,0.15);color:#c4b5fd;padding:4px 12px;border-radius:20px;font-size:0.85rem;margin:3px;display:inline-block;border:1px solid rgba(139,92,246,0.3);">#{h.lstrip("#")}</span>' for h in hashtags])
            st.markdown(tags_html, unsafe_allow_html=True)

        # Clear button
        st.markdown("")
        if st.button(t("🗑️ مسح وبدء حملة جديدة", "🗑️ Clear & Start New Campaign"), key="clear_campaign"):
            st.session_state.campaign_result = None
            st.rerun()
