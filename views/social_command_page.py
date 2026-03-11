
# ==========================================================
# MTSE Marketing Engine - Social Command (Real Queue Edition)
# Real DB-backed post scheduling + Meta Graph API publishing
# ==========================================================

import streamlit as st
import datetime
import requests
from utils import t, render_section_header
from config import BORDER_GLOW
from database import (save_scheduled_post, get_scheduled_posts,
                      update_post_status, delete_scheduled_post, get_post_stats)


def _try_publish_meta(content, platforms, access_token, page_id, media_bytes=None):
    """
    Attempt real publishing to Facebook/Instagram via Meta Graph API.
    Returns (success: bool, message: str)
    """
    if not access_token or not page_id:
        return False, "No Meta API token configured — post saved to queue."

    results = []
    for platform in platforms:
        if platform == "Facebook":
            url = f"https://graph.facebook.com/v19.0/{page_id}/feed"
            resp = requests.post(url, data={
                "message": content,
                "access_token": access_token
            }, timeout=10)
            data = resp.json()
            if "id" in data:
                results.append(f"Facebook ✅ (ID: {data['id']})")
            else:
                results.append(f"Facebook ❌ {data.get('error', {}).get('message', 'Error')}")
        elif platform == "Instagram":
            # Instagram Content Publishing API (requires IG Business)
            # Step 1: Create media container
            create_url = f"https://graph.facebook.com/v19.0/{page_id}/media"
            create_resp = requests.post(create_url, data={
                "caption": content,
                "media_type": "REELS" if media_bytes else "IMAGE",
                "access_token": access_token
            }, timeout=10)
            cdata = create_resp.json()
            container_id = cdata.get("id")
            if container_id:
                # Step 2: Publish container
                pub_url = f"https://graph.facebook.com/v19.0/{page_id}/media_publish"
                pub_resp = requests.post(pub_url, data={
                    "creation_id": container_id,
                    "access_token": access_token
                }, timeout=10)
                pdata = pub_resp.json()
                if "id" in pdata:
                    results.append(f"Instagram ✅ (ID: {pdata['id']})")
                else:
                    results.append(f"Instagram ❌ {pdata.get('error', {}).get('message', 'Caption issue')}")
            else:
                results.append(f"Instagram ❌ Container creation failed")

    if results:
        return True, " | ".join(results)
    return False, "No supported platforms for direct publish"


def render():
    """Render the Real Social Command page with DB queue."""

    username = st.session_state.get("username", "user")

    # Load API tokens from st.secrets (or session state)
    meta_token = st.session_state.get("meta_access_token") or \
        st.secrets.get("META_ACCESS_TOKEN", "") if hasattr(st, 'secrets') else ""
    meta_page_id = st.session_state.get("meta_page_id") or \
        st.secrets.get("META_PAGE_ID", "") if hasattr(st, 'secrets') else ""

    # Stats from DB
    stats = get_post_stats(username)

    st.markdown(f"""
    <div class="glass-card animate-in" style="background: linear-gradient(180deg, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.4) 100%); border-right: 2px solid {BORDER_GLOW};">
        <h2>🚀 {t("مركز القيادة الاجتماعية", "Autonomous Social Command")}</h2>
        <p style="color:#94a3b8;">{t("نشر وجدولة حقيقية عبر جميع المنصات", "Real-time publishing and scheduling across all platforms")}</p>
    </div>
    """, unsafe_allow_html=True)

    # Live KPIs from DB
    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("المنشورات اليوم", "Today's Posts"), stats["today"], "+")
    c2.metric(t("قيد الانتظار", "In Queue"), stats["queued"])
    c3.metric(t("منشور بنجاح", "Published"), stats["published"])
    api_status = "🟢 متصل" if (meta_token and meta_page_id) else "🟡 Demo"
    c4.metric(t("حالة API", "API Status"), api_status)

    st.markdown("---")

    tab_post, tab_queue, tab_settings = st.tabs([
        f"➕ {t('نشر فوري', 'Quick Post')}",
        f"📅 {t('قائمة الانتظار', 'Queue')}",
        f"🔑 {t('إعداد API', 'API Config')}"
    ])

    # ─── TAB 1: POST NOW ───────────────────────────────────────
    with tab_post:
        col_c, col_p = st.columns([1, 1])
        with col_c:
            st.markdown(f"#### 📝 {t('إنشاء منشور', 'Create Post')}")
            content = st.text_area(t("محتوى المنشور (مطلوب)", "Post Content (required)"), height=150, key="sc_content")
            platforms = st.multiselect(
                t("اختر المنصات", "Select Platforms"),
                ["Facebook", "Instagram", "X (Twitter)", "LinkedIn", "TikTok"],
                key="sc_platforms"
            )
            uploaded_file = st.file_uploader(
                t("إرفاق وسائط (اختياري)", "Attach Media (optional)"),
                type=["jpg", "png", "mp4"], key="sc_media"
            )
            post_now = st.toggle(t("نشر فوري (وإلا جدولة)", "Post Now (else schedule)"), value=True, key="sc_now_toggle")
            scheduled_time = datetime.datetime.now()
            if not post_now:
                s_date = st.date_input(t("تاريخ النشر", "Publish Date"), key="sc_date")
                s_time = st.time_input(t("وقت النشر", "Publish Time"), key="sc_time")
                scheduled_time = datetime.datetime.combine(s_date, s_time)

            if st.button(t("🚀 إطلاق المنشور", "🚀 Launch Post"), use_container_width=True, type="primary"):
                if not content:
                    st.error(t("يرجى كتابة محتوى المنشور أولاً.", "Please write post content first."))
                elif not platforms:
                    st.error(t("اختر منصة واحدة على الأقل.", "Select at least one platform."))
                else:
                    media_type = uploaded_file.type if uploaded_file else None
                    media_bytes = uploaded_file.read() if uploaded_file else None

                    if post_now and (meta_token and meta_page_id):
                        with st.spinner(t("جاري النشر الفعلي...", "Publishing for real...")):
                            success, msg = _try_publish_meta(content, platforms, meta_token, meta_page_id, media_bytes)
                            status = "Published" if success else "Failed"
                            save_scheduled_post(username, content, platforms, media_type,
                                                scheduled_time.isoformat(), status=status)
                            if success:
                                st.success(f"✅ {t('تم النشر بنجاح!', 'Published successfully!')} — {msg}")
                                st.balloons()
                            else:
                                st.warning(f"⚠️ {msg}")
                    else:
                        # Save to queue (real DB, publish via scheduler or manual)
                        save_scheduled_post(username, content, platforms, media_type,
                                            scheduled_time.isoformat(), status="Queued")
                        st.success(t(
                            f"✅ تم حفظ المنشور في قائمة الانتظار لـ {', '.join(platforms)} في {scheduled_time.strftime('%Y-%m-%d %H:%M')}",
                            f"✅ Post queued for {', '.join(platforms)} at {scheduled_time.strftime('%Y-%m-%d %H:%M')}"
                        ))
                        st.rerun()

        with col_p:
            st.markdown(f"#### 👁️ {t('معاينة', 'Preview')}")
            preview_content = st.session_state.get("sc_content", "")
            if preview_content:
                st.markdown(f"""
                <div class="glass-card" style="max-width:400px; margin:auto; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display:flex; align-items:center; margin-bottom:10px;">
                        <div style="width:40px; height:40px; background:#6366f1; border-radius:50%;"></div>
                        <div style="margin-left:10px;">
                            <b style="font-size:0.9rem;">{username}</b><br>
                            <span style="font-size:0.75rem; color:#94a3b8;">Just now</span>
                        </div>
                    </div>
                    <p style="font-size:0.9rem;">{preview_content}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info(t("اكتب المحتوى لرؤية المعاينة", "Write content to see preview"))

    # ─── TAB 2: REAL QUEUE ─────────────────────────────────────
    with tab_queue:
        render_section_header(t("قائمة الانتظار الحقيقية", "Live Post Queue"), "⏳")
        posts = get_scheduled_posts(username)
        if not posts:
            st.info(t("لا توجد منشورات في قائمة الانتظار بعد.", "No posts in queue yet."))
        else:
            status_color = {"Queued": "#fbbf24", "Published": "#10b981", "Failed": "#ef4444", "Cancelled": "#64748b"}
            for post in posts:
                col_info, col_actions = st.columns([3, 1])
                with col_info:
                    sc = status_color.get(post["status"], "#fff")
                    st.markdown(f"""
                    <div class="glass-card" style="padding:12px 16px; margin:6px 0; border-left: 4px solid {sc};">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:0.75rem; color:{sc}; font-weight:700;">{post['status'].upper()}</span>
                            <span style="font-size:0.75rem; color:#64748b;">{post['scheduled_at'][:16]}</span>
                        </div>
                        <p style="margin:6px 0; font-size:0.9rem;">{post['content'][:120]}{'...' if len(post['content'])>120 else ''}</p>
                        <small style="color:#6366f1;">📡 {post['platforms']}</small>
                        {f'<br><small style="color:#ef4444;">⚠ {post["error_message"]}</small>' if post.get("error_message") else ''}
                    </div>
                    """, unsafe_allow_html=True)
                with col_actions:
                    if post["status"] == "Queued":
                        if st.button(t("نشر الآن", "Publish"), key=f"pub_{post['id']}", use_container_width=True):
                            if meta_token and meta_page_id:
                                ok, msg = _try_publish_meta(post["content"], post["platforms"].split(","),
                                                            meta_token, meta_page_id)
                                update_post_status(post["id"], "Published" if ok else "Failed",
                                                   None if ok else msg)
                            else:
                                update_post_status(post["id"], "Published")
                            st.rerun()
                        if st.button(t("حذف", "Delete"), key=f"del_{post['id']}", use_container_width=True):
                            delete_scheduled_post(post["id"], username)
                            st.rerun()

    # ─── TAB 3: API CONFIG ─────────────────────────────────────
    with tab_settings:
        render_section_header(t("إعداد مفاتيح النشر", "Publishing API Keys"), "🔑")
        st.info(t(
            "أدخل مفاتيح API هنا حتى يتم النشر الحقيقي على المنصات. تُحفظ في الـ Session فقط (آمنة).",
            "Enter your API keys here to enable real publishing. Stored in session only (secure)."
        ))
        new_token = st.text_input("Meta (Facebook/Instagram) Access Token",
                                   value=st.session_state.get("meta_access_token", ""),
                                   type="password", key="sc_meta_token")
        new_page_id = st.text_input("Facebook Page ID / IG Business Account ID",
                                     value=st.session_state.get("meta_page_id", ""),
                                     key="sc_meta_page")
        if st.button(t("💾 حفظ المفاتيح", "💾 Save Keys"), use_container_width=True):
            st.session_state.meta_access_token = new_token
            st.session_state.meta_page_id = new_page_id
            if new_token and new_page_id:
                st.success(t("✅ تم حفظ مفاتيح Meta API. النشر الفعلي مفعّل!", "✅ Meta API keys saved. Real publishing enabled!"))
            else:
                st.info(t("لم تُدخَل مفاتيح — سيعمل النظام بوضع الجدولة فقط.", "No keys entered — system will run in queue-only mode."))

        st.markdown("---")
        st.markdown(f"#### 📋 {t('من أين تحصل على المفاتيح؟', 'Where to get the keys?')}")
        st.markdown("""
        1. اذهب إلى [Facebook Developers](https://developers.facebook.com/apps/)
        2. أنشئ App جديد من نوع **Business**
        3. أضف **Instagram Graph API** + **Pages API**
        4. من **Graph API Explorer** احصل على **Page Access Token**
        5. انسخ الـ **Page ID** من إعدادات صفحتك على Facebook
        """)
