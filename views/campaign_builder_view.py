import streamlit as st
import time
from utils import t, render_section_header
from ai_engine.router import router

def render():
    render_section_header(t("غرفة العمليات الابتكارية", "Campaign Command Hub"), "🚀")
    
    st.markdown(f"""
    <div class="glass-card animate-in">
        <h3>{t("أتمتة الحملات الشاملة (v12)", "Unified Campaign Automation (v12)")}</h3>
        <p>{t("قم بتوليد استراتيجية كاملة، محتوى فيديو، منشورات اجتماعية، وحملات بريدية في ثوانٍ.", "Generate full strategy, video scripts, social posts, and email campaigns in seconds.")}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])
    with col1:
        campaign_goal = st.text_input(t("هدف الحملة", "Campaign Objective"), placeholder=t("مثال: إطلاق منتج جديد، زيادة الوعي بالعلامة التجارية...", "e.g. Product launch, Brand awareness..."))
        target_audience = st.text_input(t("الجمهور المستهدف", "Target Audience"), placeholder=t("مثال: مهندسي الديكور، أصحاب المشاريع الصغيرة...", "e.g. Interior designers, Small business owners..."))
    with col2:
        platforms = st.multiselect(t("المنصات المستهدفة", "Target Platforms"), ["TikTok", "Instagram", "Facebook", "Email", "YouTube"], default=["TikTok", "Instagram"])
        priority = st.select_slider(t("أولوية الإبداع", "Creative Priority"), options=[t("توفير", "Budget"), t("متوازن", "Balanced"), t("جودة فنية", "High Creative")])

    if st.button(t("🚀 توليد الحملة المتكاملة", "🚀 Generate Unified Campaign"), use_container_width=True):
        if not campaign_goal:
            st.error(t("يرجى إدخال هدف الحملة أولاً.", "Please enter a campaign objective first."))
        else:
            # Route to appropriate model
            model = router.route_task("creative")
            meta = router.simulate_thinking(model)
            
            with st.status(t(f"جاري التوليد عبر {model}...", f"Generating via {model}..."), expanded=True) as status:
                st.write(t("🧠 تحليل السوق والجمهور...", "Analysing market and audience..."))
                time.sleep(1.5)
                st.write(t("🎬 كتابة نصوص الفيديوهات (Reels/TikToks)...", "Drafting video scripts (Reels/TikToks)..."))
                time.sleep(2)
                st.write(t("✍️ صياغة منشورات التواصل الاجتماعي...", "Crafting social posts..."))
                time.sleep(1.5)
                status.update(label=t("✅ اكتمل التوليد!", "✅ Campaign Generated!"), state="complete")

            st.success(t(f"تمت العملية بنجاح! المستدعى: {model} (الكمون: {meta['latency']})", f"Operation successful! Model used: {model} (Latency: {meta['latency']})"))
            
            # Display Results in Tabs
            res_tabs = st.tabs(platforms)
            for i, p in enumerate(platforms):
                with res_tabs[i]:
                    st.markdown(f"### {p} Content")
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4>{t("المحتوى المقترح للـ", "Suggested Content for ")}{p}</h4>
                        <p><b>{t("تم التوليد باستخدام:", "Generated via:")}</b> {model}</p>
                        <hr>
                        <p>{t("هذا محتوى تجريبي مخصص لـ " + p + " بناءً على هدفك: " + campaign_goal, "Sample content for " + p + " based on your goal: " + campaign_goal)}</p>
                    </div>
                    """, unsafe_allow_html=True)

# Note: This view will be imported in app.py similarly to others.
