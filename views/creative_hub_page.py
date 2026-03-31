# ==========================================================
# MTSE Marketing Engine - Creative War Room v12
# Consolidates: Strategy Orchestrator, Production Studio,
#               Virality Lab with real AI + gauge chart
# ==========================================================

import streamlit as st
import plotly.graph_objects as go
from utils import t, render_section_header
from config import BORDER_GLOW, PRIMARY, PRIMARY_LIGHT, ACCENT, SUCCESS, WARNING, DANGER
from ai_engine.campaign_orchestrator import get_orchestrator
from ai_engine.campaign_generator import generate_campaign_ideas, render_preview_html, get_social_preview_css
from ai_engine.viral_analyzer import analyze_virality, rewrite_for_virality
from billing.plans import PlanManager


def render():
    """Render the Consolidated Creative Hub."""

    pm = PlanManager(st.session_state.plan)

    st.markdown(f"""
    <div class="glass-card animate-in" style="
        background: linear-gradient(135deg, rgba(109,40,217,0.1) 0%, rgba(6,182,212,0.08) 100%);
        border-bottom: 4px solid {PRIMARY}; margin-bottom:24px;
    ">
        <h1 style="margin:0 0 6px;">🎭 {t("غرفة الحرب الإبداعية", "Creative War Room")}</h1>
        <p style="color:#94a3b8; margin:0;">{t(
            "صمم استراتيجيتك، ولّد محتواك، وحلّل مدى انتشاره في مكان واحد.",
            "Orchestrate strategy, generate content, and analyze virality in one place."
        )}</p>
    </div>
    """, unsafe_allow_html=True)

    tab_orch, tab_studio, tab_viral = st.tabs([
        f"🧠 {t('الأوركسترا الاستراتيجية', 'Strategy Orchestrator')}",
        f"🎨 {t('ستوديو الإنتاج', 'Production Studio')}",
        f"🔥 {t('مختبر الانتشار', 'Virality Lab')}",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1 — STRATEGY ORCHESTRATOR
    # ─────────────────────────────────────────────────────────────────────────
    with tab_orch:
        render_section_header(t("بناء الحملات المتكاملة", "Multi-Channel Campaign Builder"), "🧠")

        with st.expander(t("📋 إعدادات الحملة", "📋 Campaign Setup"), expanded=True):
            co1, co2 = st.columns(2)
            with co1:
                p_desc = st.text_area(
                    t("📝 وصف المنتج/الخدمة *", "📝 Product / Service Description *"),
                    placeholder=t(
                        "مثال: تطبيق توصيل طعام سريع يستهدف الشباب في الرياض...",
                        "e.g. Fast food delivery app targeting youth in Riyadh..."
                    ),
                    key="hub_orch_desc", height=100
                )
                t_aud = st.text_input(
                    t("👥 الجمهور المستهدف *", "👥 Target Audience *"),
                    key="hub_orch_aud",
                    placeholder=t("مثال: رجال أعمال 25-45، مهتمون بالتكنولوجيا", "e.g. Business men 25-45 interested in tech")
                )
            with co2:
                obj = st.selectbox(
                    t("🎯 هدف الحملة", "🎯 Campaign Objective"),
                    [
                        t("زيادة الوعي بالعلامة التجارية", "Brand Awareness"),
                        t("توليد الطلبات / العملاء المحتملين", "Lead Generation"),
                        t("زيادة المبيعات المباشرة", "Direct Sales"),
                        t("الاحتفاظ بالعملاء", "Customer Retention"),
                        t("إطلاق منتج جديد", "Product Launch"),
                    ],
                    key="hub_orch_obj"
                )
                budget_orch = st.select_slider(
                    t("💰 الميزانية التقديرية", "💰 Budget"),
                    options=["$500", "$1,000", "$2,500", "$5,000", "$10,000", "$25,000+"],
                    key="hub_orch_budget"
                )

            lang_choice = st.radio(
                t("🌍 لغة الاستراتيجية", "🌍 Strategy Language"),
                [t("عربي", "Arabic"), "English", t("الاثنين", "Bilingual")],
                horizontal=True, key="hub_orch_lang"
            )

            if st.button(t("🚀 توليد الاستراتيجية الكاملة", "🚀 Generate Full Strategy"), use_container_width=True, key="hub_orch_gen"):
                if not p_desc:
                    st.error(t("⚠️ يرجى إدخال وصف المنتج.", "⚠️ Please enter product description."))
                else:
                    with st.spinner(t("جاري الأوركسترا الاستراتيجية...", "Running strategy orchestration...")):
                        orch = get_orchestrator()
                        st.session_state.hub_orch_res = orch.orchestrate(
                            p_desc, t_aud, obj, budget_orch
                        )

        # Results
        if st.session_state.get("hub_orch_res"):
            res = st.session_state.hub_orch_res
            st.markdown("---")
            st.markdown(f"""
            <div class="glass-card animate-in" style="border-top:4px solid {PRIMARY}; text-align:center; margin-bottom:20px;">
                <h2 style="background:linear-gradient(135deg,{PRIMARY_LIGHT},{ACCENT});-webkit-background-clip:text;-webkit-text-fill-color:transparent; margin-bottom:6px;">
                    🎯 {res.get('campaign_name', t('الحملة الاستراتيجية','Strategic Campaign'))}
                </h2>
            </div>
            """, unsafe_allow_html=True)

            # Strategy timeline
            roadmap = res.get("overall_roadmap", "")
            if roadmap:
                st.markdown(f"#### 🗺️ {t('خارطة الطريق التنفيذية', 'Execution Roadmap')}")
                phases = [
                    (t("التخطيط والإعداد", "Planning & Setup"),         "📋", SUCCESS),
                    (t("بناء المحتوى والأصول", "Content & Asset Build"), "🎨", ACCENT),
                    (t("الإطلاق والتوزيع", "Launch & Distribution"),    "🚀", PRIMARY),
                    (t("القياس والتحسين", "Measure & Optimize"),        "📊", WARNING),
                ]
                p_cols = st.columns(4)
                for i, (phase, icon, color) in enumerate(phases):
                    with p_cols[i]:
                        st.markdown(f"""
                        <div style="
                            text-align:center; padding:18px 12px;
                            background: rgba({','.join(str(int(color.lstrip('#')[j:j+2],16)) for j in (0,2,4))}, 0.1);
                            border-radius:14px; border:1px solid {color}44;
                        ">
                            <div style="font-size:1.8rem;">{icon}</div>
                            <div style="color:{color}; font-weight:700; font-size:0.85rem; margin-top:6px; line-height:1.3;">{phase}</div>
                            <div style="color:#64748b; font-size:0.75rem; margin-top:4px;">{t(f'المرحلة {i+1}', f'Phase {i+1}')}</div>
                        </div>
                        """, unsafe_allow_html=True)

                st.markdown("")
                st.info(f"📋 {roadmap}")

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2 — PRODUCTION STUDIO
    # ─────────────────────────────────────────────────────────────────────────
    with tab_studio:
        st.markdown(get_social_preview_css(), unsafe_allow_html=True)

        render_section_header(t("ستوديو توليد المحتوى", "Content Generation Studio"), "🎨")

        col_inp, col_out = st.columns([1, 1.2])

        with col_inp:
            prod_name = st.text_input(
                t("🏷️ اسم المنتج/الخدمة", "🏷️ Product / Service Name"),
                placeholder=t("مثال: عطر نور المساء", "e.g. Midnight Aura Perfume"),
                key="hub_prod_name"
            )
            prod_platform = st.selectbox(
                t("📱 المنصة المستهدفة", "📱 Target Platform"),
                ["Instagram", "TikTok", "Facebook", "Twitter", "LinkedIn"],
                key="hub_prod_platform"
            )
            prod_style = st.selectbox(
                t("🎨 أسلوب المحتوى", "🎨 Content Style"),
                [
                    t("احترافي ومرموق", "Professional"),
                    t("مرح وترفيهي",   "Fun & Entertainment"),
                    t("ملهم وتحفيزي",  "Inspirational"),
                    t("جريء وعدواني",  "Bold & Aggressive"),
                ],
                key="hub_prod_style"
            )
            num_variants = st.slider(t("عدد البدائل", "Number of Variants"), 1, 4, 2, key="hub_prod_vars")

            if st.button(
                t("✨ توليد نصوص وأفكار إبداعية", "✨ Generate Creative Copy"),
                use_container_width=True, key="hub_prod_gen"
            ):
                if not prod_name:
                    st.error(t("⚠️ يرجى إدخال اسم المنتج.", "⚠️ Please enter product name."))
                else:
                    with st.spinner(t("تحليق الأفكار الإبداعية...", "Brainstorming creative ideas...")):
                        st.session_state.hub_copy_res = generate_campaign_ideas(
                            prod_name, prod_style, prod_platform
                        )

        with col_out:
            if st.session_state.get("hub_copy_res"):
                render_section_header(t("معاينة المحتوى", "Content Preview"), "👁️")
                for i, var in enumerate(st.session_state.hub_copy_res[:num_variants]):
                    with st.expander(f"📄 {t('النسخة', 'Variant')} {i+1}", expanded=i == 0):
                        st.markdown(render_preview_html(var, username=prod_name), unsafe_allow_html=True)
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.button(t("📋 نسخ", "📋 Copy"), key=f"copy_var_{i}", use_container_width=True):
                                st.toast(t("✅ تم النسخ!", "✅ Copied!"))
                        with c2:
                            if st.button(t("♻️ تحديث", "♻️ Regenerate"), key=f"regen_var_{i}", use_container_width=True):
                                st.session_state.hub_copy_res = generate_campaign_ideas(prod_name, prod_style, prod_platform)
                                st.rerun()
            else:
                st.markdown(f"""
                <div style="
                    height:300px;
                    display:flex; align-items:center; justify-content:center;
                    background:rgba(255,255,255,0.02);
                    border:2px dashed rgba(255,255,255,0.08);
                    border-radius:20px; flex-direction:column; gap:12px;
                ">
                    <div style="font-size:3rem; opacity:0.3;">🎨</div>
                    <p style="color:#374151; margin:0;">{t("المعاينة ستظهر هنا", "Preview will appear here")}</p>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3 — VIRALITY LAB
    # ─────────────────────────────────────────────────────────────────────────
    with tab_viral:
        if not pm.can_access_viral_analyzer():
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:40px; border:1px solid rgba(139,92,246,0.3);">
                <div style="font-size:3rem; margin-bottom:12px;">🔥</div>
                <h3 style="color:#c4b5fd;">{t("مختبر الانتشار — Strategist+", "Virality Lab — Strategist+")}</h3>
                <p style="color:#94a3b8;">{t("هذه الأداة متاحة لخطة Strategist فأعلى.", "This tool requires Strategist plan or higher.")}</p>
                <span class="status-badge badge-warning">⚡ Strategist Plan Required</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_section_header(t("تحليل وتحسين الانتشار الفيروسي", "Viral Spread Analysis & Optimization"), "🔥")

            col_v1, col_v2 = st.columns([1.2, 1])

            with col_v1:
                v_text = st.text_area(
                    t("📝 نص المنشور للتحليل", "📝 Post Text to Analyze"),
                    placeholder=t(
                        "الصق نصك هنا لتحليل مدى قابليته للانتشار...",
                        "Paste your post text here to analyze its virality potential..."
                    ),
                    key="hub_v_text", height=160
                )
                v_platform = st.radio(
                    t("المنصة", "Platform"),
                    ["TikTok", "Instagram", "Twitter", "Facebook"],
                    horizontal=True, key="hub_v_platform"
                )

                c_analyze, c_rewrite = st.columns(2)
                do_analyze = c_analyze.button(
                    t("📊 تحليل الانتشار", "📊 Analyze Virality"),
                    use_container_width=True, key="hub_v_analyze"
                )
                do_rewrite = c_rewrite.button(
                    t("✨ تحسين ذكي", "✨ AI Rewrite"),
                    use_container_width=True, key="hub_v_rewrite"
                )

                if do_analyze and v_text:
                    with st.spinner(t("تحليل الانتشار...", "Analyzing viral potential...")):
                        res = analyze_virality(v_text, False)
                        st.session_state.viral_result = res

                if do_rewrite and v_text:
                    with st.spinner(t("تحسين النص...", "Rewriting for virality...")):
                        st.session_state.viral_rewrites = rewrite_for_virality(v_text)

            with col_v2:
                if st.session_state.get("viral_result"):
                    res = st.session_state.viral_result
                    score = res.get("score", 50)

                    # Gauge chart
                    color_score = SUCCESS if score >= 70 else (WARNING if score >= 45 else DANGER)
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=score,
                        delta={"reference": 50, "valueformat": ".0f"},
                        domain={"x": [0,1], "y": [0,1]},
                        title={"text": t("نقاط الانتشار الفيروسي", "Viral Score"), "font": {"color": "white", "size": 15}},
                        number={"suffix": "/100", "font": {"color": color_score, "size": 36}},
                        gauge={
                            "axis": {"range": [0,100], "tickfont": {"color": "white"}, "nticks": 5},
                            "bar":  {"color": color_score, "thickness": 0.25},
                            "bgcolor": "rgba(0,0,0,0)",
                            "bordercolor": "rgba(0,0,0,0)",
                            "steps": [
                                {"range": [0,40],   "color": "rgba(244,63,94,0.12)"},
                                {"range": [40,70],  "color": "rgba(251,191,36,0.12)"},
                                {"range": [70,100], "color": "rgba(16,185,129,0.12)"},
                            ],
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white"),
                        height=200,
                        margin=dict(l=20,r=20,t=30,b=0),
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)

                    # Breakdown
                    factors = res.get("factors", {})
                    if factors:
                        st.markdown(f"#### {t('تفصيل العوامل', 'Factor Breakdown')}")
                        for k, v in factors.items():
                            bar_color = SUCCESS if v >= 70 else (WARNING if v >= 40 else DANGER)
                            st.markdown(f"""
                            <div style="margin-bottom:10px;">
                                <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                                    <span style="color:#cbd5e1; font-size:0.85rem;">{k}</span>
                                    <span style="color:{bar_color}; font-weight:700; font-size:0.85rem;">{v}/100</span>
                                </div>
                                <div class="usage-bar">
                                    <div class="usage-bar-fill" style="width:{v}%; background: linear-gradient(90deg, {bar_color}aa, {bar_color});"></div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

            # AI rewrites panel
            if st.session_state.get("viral_rewrites"):
                st.markdown(f"### ✨ {t('النسخ المحسّنة بالذكاء الاصطناعي', 'AI-Optimized Rewrites')}")
                for i, rw in enumerate(st.session_state.viral_rewrites):
                    with st.expander(f"📝 {t('النسخة المحسّنة', 'Optimized Variant')} {i+1}", expanded=i==0):
                        st.code(rw, language=None)
                        if st.button(t("📋 استخدام هذه النسخة", "📋 Use this version"), key=f"use_rw_{i}", use_container_width=True):
                            st.session_state["hub_v_text"] = rw
                            st.toast(t("✅ تم نقل النص!", "✅ Text applied!"))
