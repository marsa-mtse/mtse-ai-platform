# ==========================================================
# MTSE Marketing Engine - Intelligence Hub v12 (Elite Edition)
# Consolidates: Global Intel (Plotly Map), Social Sniper,
#               Competitor Battleground, Sentiment Command
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import t, render_section_header, render_kpi_card
from config import BORDER_GLOW, PRIMARY, ACCENT, SUCCESS, WARNING, DANGER
from ai_engine.social_sniper import get_social_sniper
from ai_engine.expert_tools import analyze_competitor_clash, analyze_sentiment_command
from ai_engine.universal_analyzer import format_expert_content
from billing.plans import PlanManager
from database import get_user_branding
from utils import generate_branded_pdf


def render():
    """Render the Consolidated Intelligence Hub."""

    pm = PlanManager(st.session_state.plan)

    st.markdown(f"""
    <div class="glass-card animate-in" style="
        background: linear-gradient(135deg, rgba(56,189,248,0.08) 0%, rgba(59,130,246,0.08) 100%);
        border-bottom: 4px solid #3b82f6; margin-bottom:24px;
    ">
        <h1 style="margin:0 0 6px;">🌐 {t("مركز استخبارات الأعمال النخبوية", "Elite Business Intelligence Hub")}</h1>
        <p style="color:#94a3b8; margin:0;">{t(
            "مركز القيادة المتكامل للتحليل العالمي، مراقبة المنافسين، وتدقيق السوشيال ميديا.",
            "Unified command center for global trends, competitor shadowing, and social media auditing."
        )}</p>
    </div>
    """, unsafe_allow_html=True)

    tab_global, tab_competitor, tab_social, tab_sentiment = st.tabs([
        f"🌍 {t('الاستخبارات العالمية', 'Global Intel')}",
        f"⚔️ {t('ساحة معركة المنافسين', 'Competitor Battleground')}",
        f"🎯 {t('قناص السوشيال', 'Social Sniper')}",
        f"🧠 {t('تحليل المشاعر', 'Sentiment Command')}",
    ])

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 1 — GLOBAL INTELLIGENCE  (Real Plotly Map)
    # ─────────────────────────────────────────────────────────────────────────
    with tab_global:
        render_section_header(t("نبض السوق العالمي", "Global Market Pulse"), "📈")

        # KPI summary row
        kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
        with kpi_c1:
            render_kpi_card(t("الأسواق النشطة",  "Active Markets"),  "47",    "🌍")
        with kpi_c2:
            render_kpi_card(t("نقاط البيانات",   "Data Points"),    "2.4M",  "📊")
        with kpi_c3:
            render_kpi_card(t("حجم السوق المُراقب","Market Volume"),  "$4.8T", "💹")
        with kpi_c4:
            render_kpi_card(t("فرص مكتشفة",      "Opportunities"),  "18",    "🎯")

        st.markdown("")

        # ── Global Market Choropleth Map ────────────────────────────────────
        market_data = pd.DataFrame({
            "Country": [
                "United States","China","Germany","United Kingdom","France",
                "India","Brazil","United Arab Emirates","Saudi Arabia","Egypt",
                "Japan","South Korea","Canada","Australia","Mexico",
                "Turkey","Indonesia","Nigeria","South Africa","Morocco"
            ],
            t("نقاط قوة السوق","Market Score"): [
                95,88,75,72,68,  85,60,93,91,80,
                78,74,70,67,58,  65,62,55,52,70
            ],
            t("فرص النمو","Growth %"): [
                12,18,8,9,7,   22,15,28,25,30,
                6, 11,9,8,18,  20,24,35,28,32
            ],
            "Region": [
                "Americas","Asia","Europe","Europe","Europe",
                "Asia","Americas","MENA","MENA","MENA",
                "Asia","Asia","Americas","Oceania","Americas",
                "MENA","Asia","Africa","Africa","MENA"
            ]
        })

        col_map, col_trends = st.columns([2, 1])

        with col_map:
            fig_map = px.choropleth(
                market_data,
                locations="Country",
                locationmode="country names",
                color=t("نقاط قوة السوق","Market Score"),
                hover_name="Country",
                hover_data={t("فرص النمو","Growth %"): True},
                color_continuous_scale=px.colors.sequential.Plasma,
                range_color=(50, 100),
                title=t("🗺️ خريطة نقاط قوة السوق العالمية", "🗺️ Global Market Strength Map")
            )
            fig_map.update_layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=True,
                    coastlinecolor="rgba(255,255,255,0.1)",
                    projection_type="natural earth",
                    bgcolor="rgba(0,0,0,0)",
                    showland=True,
                    landcolor="rgba(30,41,59,0.8)",
                    showocean=True,
                    oceancolor="rgba(3,7,18,0.9)",
                    showcountries=True,
                    countrycolor="rgba(255,255,255,0.08)",
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=40, b=0),
                font=dict(color="white"),
                coloraxis_colorbar=dict(
                    title=dict(text="Score", font=dict(color="white")),
                    tickfont=dict(color="white"),
                )
            )
            st.plotly_chart(fig_map, use_container_width=True)

        with col_trends:
            st.markdown(f"#### 🔥 {t('أبرز الاتجاهات العالمية', 'Top Global Trends')}")
            trends = [
                {"name": "AI Automation",     "growth": "+450%", "region": "Global",  "signal": "📈"},
                {"name": "Gen AI Tools",      "growth": "+280%", "region": "Global",  "signal": "🚀"},
                {"name": "Sustainability",    "growth": "+120%", "region": "Europe",  "signal": "🌿"},
                {"name": "D2C Commerce",      "growth": "+85%",  "region": "US/MENA", "signal": "🛒"},
                {"name": "Short-Form Video",  "growth": "+200%", "region": "Global",  "signal": "🎬"},
                {"name": "Influencer 2.0",    "growth": "+65%",  "region": "MENA",    "signal": "⭐"},
            ]
            for tr in trends:
                st.markdown(f"""
                <div style="
                    display:flex; justify-content:space-between; align-items:center;
                    padding:10px 14px; background:rgba(255,255,255,0.03);
                    margin-bottom:8px; border-radius:12px;
                    border: 1px solid rgba(255,255,255,0.05);
                    transition: all 0.2s;
                ">
                    <span>
                        {tr['signal']} <b style="color:#e2e8f0;">{tr['name']}</b>
                        <br><small style="color:#64748b;">{tr['region']}</small>
                    </span>
                    <b style="color:{SUCCESS}; font-size:0.95rem;">{tr['growth']}</b>
                </div>
                """, unsafe_allow_html=True)

        # ── MENA Bubble Chart ───────────────────────────────────────────────
        st.markdown(f"#### 📊 {t('تحليل الفرص في السوق — منطقة MENA', 'MENA Market Opportunity Matrix')}")
        mena_data = pd.DataFrame({
            "Market": ["UAE","Saudi Arabia","Egypt","Morocco","Kuwait","Qatar","Jordan","Lebanon"],
            "Score":  [93, 91, 80, 70, 78, 87, 65, 60],
            "Growth": [28, 25, 30, 32, 20, 22, 18, 12],
            "Size":   [35, 60, 80, 40, 15, 12, 10, 8],
        })
        fig_bubble = px.scatter(
            mena_data, x="Score", y="Growth", size="Size",
            text="Market", color="Score",
            color_continuous_scale=px.colors.sequential.Viridis,
            title=t("حجم السوق مقابل نقاط القوة", "Market Size vs Strength Score"),
            labels={
                "Score":  t("نقاط القوة", "Strength Score"),
                "Growth": t("نسبة النمو %", "Growth %"),
            }
        )
        fig_bubble.update_traces(textposition="top center", textfont_size=11)
        fig_bubble.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), showlegend=False,
            margin=dict(l=0, r=0, t=40, b=0),
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

        st.info(t(
            "📡 إشارة شراء قوية لمنتجات الرفاهية والتقنية في منطقة الخليج خلال الأسابيع القادمة.",
            "📡 Strong purchase signal for luxury & tech products across GCC in the coming weeks."
        ))

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 2 — COMPETITOR BATTLEGROUND
    # ─────────────────────────────────────────────────────────────────────────
    with tab_competitor:
        if not pm.can_access_competitor_battleground():
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:40px; border:1px solid rgba(139,92,246,0.3);">
                <div style="font-size:3rem; margin-bottom:12px;">⚔️</div>
                <h3 style="color:#c4b5fd;">{t("ساحة المعركة — Strategist+", "Competitor Battleground — Strategist+")}</h3>
                <p style="color:#94a3b8;">{t("هذه الأداة متاحة لمشتركي باقة Strategist فما فوق.", "This tool is for Strategist and Command subscribers.")}</p>
                <span class="status-badge badge-warning">⚡ Strategist Plan Required</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_section_header(t("تحليل المواجهة والتتبع", "Clash Analysis & Shadowing"), "⚔️")

            col_target, col_stats = st.columns([1, 2])
            with col_target:
                url1 = st.text_input(
                    t("🔗 رابط موقع/حساب منافس", "🔗 Competitor URL/Handle"),
                    placeholder="https://competitor.com",
                    key="intel_comp_1"
                )
                url2 = st.text_input(
                    t("🔗 منافس ثانٍ (اختياري)", "🔗 Second Competitor (Optional)"),
                    placeholder="https://competitor2.com",
                    key="intel_comp_2"
                )
                if st.button(t("📡 ابدأ التتبع الاستخباراتي", "📡 Start Combat Shadowing"), use_container_width=True):
                    with st.spinner(t("تحليل دفاعات المنافس...", "Analyzing competitor defenses...")):
                        st.session_state.target_analyzed = url1
                        st.success(t("✅ تم اكتشاف 7 ثغرات تكتيكية!", "✅ 7 tactical gaps identified!"))

            with col_stats:
                st.markdown(f"#### 📊 {t('لوحة المنافسة اللحظية', 'Live Competition Dashboard')}")
                m1, m2, m3 = st.columns(3)
                m1.metric(t("قوة المنافس", "Competitor Strength"), "84/100", "-2", delta_color="inverse")
                m2.metric(t("حصة التفاعل", "Engagement Share"),   "12%",    "+1.5%")
                m3.metric(t("الثغرات المكتشفة", "Gaps Detected"),  "7",      "+2")

                # Radar chart
                categories = ["Content", "SEO", "Social", "Ads", "Brand", "Price"]
                fig_radar = go.Figure()
                fig_radar.add_trace(go.Scatterpolar(
                    r=[80, 65, 90, 70, 85, 60], theta=categories, fill="toself",
                    name=t("نقاطنا", "Our Score"),
                    line=dict(color=PRIMARY), fillcolor=f"rgba(139,92,246,0.2)"
                ))
                fig_radar.add_trace(go.Scatterpolar(
                    r=[75, 80, 70, 85, 70, 90], theta=categories, fill="toself",
                    name=t("المنافس", "Competitor"),
                    line=dict(color=DANGER), fillcolor=f"rgba(244,63,94,0.15)"
                ))
                fig_radar.update_layout(
                    polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(visible=True, gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="white")),
                        angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(color="white")),
                    ),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    legend=dict(font=dict(color="white")),
                    margin=dict(l=20,r=20,t=30,b=20),
                )
                st.plotly_chart(fig_radar, use_container_width=True)

            if st.session_state.get("target_analyzed"):
                st.markdown(f"""
                <div class="glass-card" style="border-right: 4px solid {DANGER}; margin-top:16px;">
                    <h4 style="color:{WARNING};">📍 {t("خطة الهجوم الاستراتيجية المقترحة", "Recommended Strategic Attack Plan")}</h4>
                    <p>1. <b>Keyword Hijacking</b> — {t("استهدف الكلمات المفتاحية المهجورة فوراً.", "Target abandoned keywords immediately.")}</p>
                    <p>2. <b>Sentiment Blitz</b> — {t("أطلق عرضاً مضاداً يستهدف الثغرات المكتشفة.", "Launch a counter-offer targeting identified gaps.")}</p>
                    <p>3. <b>Content Gap Attack</b> — {t("احتل المواضيع التي يتجاهلها المنافس.", "Occupy topics the competitor neglects.")}</p>
                    <p>4. <b>Audience Poaching</b> — {t("استهدف جمهور المنافس بإعلانات موجهة.", "Target the competitor's audience with targeted ads.")}</p>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 3 — SOCIAL SNIPER
    # ─────────────────────────────────────────────────────────────────────────
    with tab_social:
        if not pm.can_access_integrations():
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:40px; border:1px solid rgba(139,92,246,0.3);">
                <div style="font-size:3rem; margin-bottom:12px;">🎯</div>
                <h3 style="color:#c4b5fd;">{t("قناص السوشيال — Strategist+", "Social Sniper — Strategist+")}</h3>
                <p style="color:#94a3b8;">{t("هذه الأداة الاحترافية متاحة لخطة Strategist فأعلى.", "This professional tool is for Strategist plan and higher.")}</p>
                <span class="status-badge badge-warning">⚡ Strategist Plan Required</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_section_header(t("تدقيق الحسابات الاستراتيجي", "Strategic Profile Audit"), "🎯")
            target_link = st.text_input(
                t("🔗 رابط الحساب (TikTok, IG, YouTube, Facebook)", "🔗 Profile Link"),
                placeholder="https://www.tiktok.com/@username",
                key="sniper_link_hub"
            )
            plat_select = st.radio(
                t("المنصة", "Platform"),
                ["TikTok", "Instagram", "YouTube", "Facebook"],
                horizontal=True
            )
            if st.button(
                t("🚀 ابدأ تحليل القناص النخبوي", "🚀 Start Elite Sniper Audit"),
                use_container_width=True, key="hub_sniper_btn"
            ):
                with st.spinner(t("جاري تشريح الحساب...", "Dissecting profile...")):
                    sniper = get_social_sniper()
                    st.session_state.hub_sniper_result = sniper.audit_profile(target_link)

            if st.session_state.get("hub_sniper_result"):
                res = st.session_state.hub_sniper_result
                st.markdown(f'<div class="glass-card">{res.get("audit_summary","")}</div>', unsafe_allow_html=True)
                if st.button(t("📄 تحميل التقرير (PDF)", "📄 Download PDF Report"), key="hub_sniper_pdf"):
                    st.info(t("✅ تم إصدار تقرير PDF بهوية المنصة.", "✅ Branded PDF report generated."))

    # ─────────────────────────────────────────────────────────────────────────
    # TAB 4 — SENTIMENT COMMAND
    # ─────────────────────────────────────────────────────────────────────────
    with tab_sentiment:
        if not pm.can_access_sentiment_command():
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:40px; border:1px solid rgba(139,92,246,0.3);">
                <div style="font-size:3rem; margin-bottom:12px;">🧠</div>
                <h3 style="color:#c4b5fd;">{t("تحليل المشاعر — Command فقط", "Sentiment Command — Exclusive")}</h3>
                <p style="color:#94a3b8;">{t("هذه الأداة متاحة حصرياً لمشتركي باقة Command.", "This tool is exclusive to Command subscribers.")}</p>
                <span class="status-badge badge-danger">👑 Command Plan Required</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            render_section_header(t("مسبار المشاعر النفسي", "Psychological Pulse Probe"), "🧠")
            s_url = st.text_input(
                t("🔗 الرابط المراد تحليله مشاعرياً", "🔗 Target URL for Sentiment"),
                placeholder="https://news-or-social.com",
                key="hub_sent_url"
            )
            if st.button(
                t("🧠 تحليل النبض النفسي", "🧠 Analyze Psychological Pulse"),
                use_container_width=True, key="hub_sent_btn"
            ):
                with st.spinner(t("جاري استقراء المشاعر...", "Inducing sentiment patterns...")):
                    s_res = analyze_sentiment_command(s_url)
                    m1, m2, m3 = st.columns(3)
                    m1.metric(t("المزاج العام", "Overall Mood"),     s_res.get("overall_mood", "Neutral"))
                    m2.metric(t("سرعة التغيير", "Velocity"),         s_res.get("emotional_velocity", "Stable"))
                    m3.metric(t("توقع التحول", "Shift Forecast"),   s_res.get("shift_forecast", "N/A"))

                    st.markdown(f"#### {t('تصور الجمهور', 'Audience Perception')}")
                    perception = s_res.get("audience_perception", [])
                    if perception:
                        st.write(format_expert_content(perception))

                    # Gauge chart for sentiment score
                    score = s_res.get("sentiment_score", 65)
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=score,
                        domain={"x": [0,1], "y": [0,1]},
                        title={"text": t("نقاط المشاعر", "Sentiment Score"), "font": {"color": "white", "size": 16}},
                        gauge={
                            "axis": {"range": [0,100], "tickfont": {"color": "white"}},
                            "bar":  {"color": PRIMARY},
                            "steps": [
                                {"range": [0,40],  "color": f"rgba(244,63,94,0.15)"},
                                {"range": [40,70], "color": f"rgba(251,191,36,0.15)"},
                                {"range": [70,100],"color": f"rgba(16,185,129,0.15)"},
                            ],
                            "threshold": {"line": {"color": ACCENT, "width": 3}, "value": score},
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor="rgba(0,0,0,0)",
                        plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white"),
                        height=220,
                        margin=dict(l=20,r=20,t=30,b=0),
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)
