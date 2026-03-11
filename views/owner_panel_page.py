# ==========================================================
# MTSE Marketing Engine - Owner Control Panel (ELITE)
# Exclusive to: username == "admin" (platform owner only)
# ==========================================================

import streamlit as st
import pandas as pd
import datetime
from utils import t, render_section_header
from database import (
    get_connection, get_all_users, get_user, get_activity_log,
    update_plan, log_activity, get_all_leads, get_scheduled_posts,
    get_post_stats
)
from auth import hash_password, is_admin
from config import PLAN_LIMITS, PLAN_PRICING, ADMIN_DEFAULT_USERNAME, APP_VERSION


def render():
    """Owner-only Control Panel. Blocks all non-owners."""
    username = st.session_state.get("username", "")

    # ═══════════════════════════════════
    # OWNER GUARD — only "admin" can enter
    # ═══════════════════════════════════
    if username != ADMIN_DEFAULT_USERNAME:
        st.error("🔒 " + t("هذه اللوحة حصرية لمالك المنصة فقط.", "This panel is exclusive to the platform owner."))
        st.stop()

    # ── Header ───────────────────────────────────────────────
    st.markdown("""
    <div class="glass-card animate-in" style="
        background: linear-gradient(135deg, rgba(220,38,38,0.15), rgba(139,92,246,0.15));
        border: 2px solid rgba(220,38,38,0.4);
        text-align:center; padding:30px;">
        <div style="font-size:3rem;">👑</div>
        <h1 style="margin:8px 0;">Owner Control Panel</h1>
        <p style="color:#94a3b8;">لوحة التحكم المطلقة — صلاحيات غير محدودة</p>
        <div style="display:flex; justify-content:center; gap:20px; margin-top:12px; flex-wrap:wrap;">
            <span style="background:rgba(16,185,129,0.2); border:1px solid #10b981;
                         border-radius:20px; padding:4px 14px; font-size:0.8rem;">
                🟢 v{version}
            </span>
            <span style="background:rgba(139,92,246,0.2); border:1px solid #8b5cf6;
                         border-radius:20px; padding:4px 14px; font-size:0.8rem;">
                👑 Owner Mode
            </span>
        </div>
    </div>
    """.replace("{version}", APP_VERSION), unsafe_allow_html=True)

    # ── Real-time KPIs ────────────────────────────────────────
    conn = get_connection()
    all_users_raw = get_all_users()
    total_users = len(all_users_raw)
    plan_counts = {}
    for u in all_users_raw:
        p = u.get("plan", "Explorer")
        plan_counts[p] = plan_counts.get(p, 0) + 1

    all_leads = get_all_leads()
    all_activities = get_activity_log(limit=1000)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    today_active = len({a["username"] for a in all_activities if a["timestamp"].startswith(today)})

    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("👥 إجمالي المستخدمين", total_users)
    k2.metric("🎯 Strategist", plan_counts.get("Strategist", 0))
    k3.metric("💎 Command", plan_counts.get("Command", 0))
    k4.metric("📈 نشطون اليوم", today_active)
    k5.metric("📇 عملاء CRM", len(all_leads))

    st.markdown("---")

    # ── Tabs ──────────────────────────────────────────────────
    tabs = st.tabs([
        "👥 إدارة المستخدمين",
        "💰 الخطط والإيرادات",
        "📊 نشاط المنصة",
        "🔑 API Keys",
        "⚙️ إعدادات النظام",
        "🗄️ قاعدة البيانات",
    ])

    # ═══════════════════════════════════════════════════════════
    # TAB 1 — USER MANAGEMENT
    # ═══════════════════════════════════════════════════════════
    with tabs[0]:
        render_section_header("إدارة كاملة للمستخدمين", "👥")

        users = get_all_users()
        search = st.text_input("🔍 بحث عن مستخدم", key="owner_user_search", placeholder="اسم المستخدم...")
        if search:
            users = [u for u in users if search.lower() in u.get("username", "").lower()]

        for u in users:
            user_detail = get_user(u["username"]) or {}
            with st.expander(f"👤 {u['username']} | {u.get('plan','?')} | {u.get('role','?')}"):
                c1, c2, c3 = st.columns(3)
                new_plan = c1.selectbox(
                    "الخطة", ["Explorer", "Strategist", "Command"],
                    index=["Explorer", "Strategist", "Command"].index(u.get("plan", "Explorer")),
                    key=f"owner_plan_{u['username']}"
                )
                new_role = c2.selectbox(
                    "الدور", ["Admin", "Marketing Manager", "Analyst", "Viewer"],
                    index=["Admin", "Marketing Manager", "Analyst", "Viewer"].index(
                        u.get("role", "Viewer") if u.get("role") in ["Admin", "Marketing Manager", "Analyst", "Viewer"] else "Viewer"
                    ),
                    key=f"owner_role_{u['username']}"
                )
                new_status = c3.selectbox(
                    "حالة الحساب", ["Active", "Suspended", "Trial"],
                    index=["Active", "Suspended", "Trial"].index(
                        user_detail.get("billing_status", "Active") if user_detail.get("billing_status") in ["Active", "Suspended", "Trial"] else "Active"
                    ),
                    key=f"owner_status_{u['username']}"
                )

                col_save, col_reset, col_del = st.columns(3)
                if col_save.button("💾 حفظ التغييرات", key=f"owner_save_{u['username']}", use_container_width=True):
                    conn.execute(
                        "UPDATE users SET plan=?, role=?, billing_status=? WHERE username=?",
                        (new_plan, new_role, new_status, u["username"])
                    )
                    conn.commit()
                    log_activity(username, f"Owner updated user: {u['username']} → plan={new_plan}, role={new_role}")
                    st.success(f"✅ تم تحديث {u['username']}")
                    st.rerun()

                if col_reset.button("🔑 إعادة تعيين كلمة المرور", key=f"owner_pwd_{u['username']}", use_container_width=True):
                    default_pwd = "Mtse@2026"
                    conn.execute(
                        "UPDATE users SET password=?, login_attempts=0, locked_until=NULL WHERE username=?",
                        (hash_password(default_pwd), u["username"])
                    )
                    conn.commit()
                    st.success(f"✅ تم إعادة كلمة المرور إلى: `{default_pwd}`")

                if col_del.button("🗑️ حذف المستخدم", key=f"owner_del_{u['username']}", use_container_width=True,
                                   disabled=(u["username"] == ADMIN_DEFAULT_USERNAME)):
                    conn.execute("DELETE FROM users WHERE username=?", (u["username"],))
                    conn.commit()
                    st.warning(f"⚠️ تم حذف {u['username']}")
                    st.rerun()

                # Usage stats
                usage_row = conn.execute(
                    "SELECT reports_used, uploads_used FROM users WHERE username=?",
                    (u["username"],)
                ).fetchone()
                if usage_row:
                    st.caption(f"📊 الاستخدام: {usage_row['reports_used']} تقرير | {usage_row['uploads_used']} رفع")

    # ═══════════════════════════════════════════════════════════
    # TAB 2 — PLANS & REVENUE
    # ═══════════════════════════════════════════════════════════
    with tabs[1]:
        render_section_header("الإيرادات والخطط", "💰")

        # Revenue estimation
        rev_total = sum(
            PLAN_PRICING.get(u.get("plan", "Explorer"), 0)
            for u in all_users_raw
            if u.get("billing_status") == "Active"
        )
        r1, r2, r3 = st.columns(3)
        r1.metric("💵 الإيراد الشهري المقدّر (USD)", f"${rev_total:,}")
        r2.metric("📅 السنوي (تقدير)", f"${rev_total*12:,}")
        r3.metric("💳 المشتركون النشطون", sum(1 for u in all_users_raw if u.get("billing_status") == "Active"))

        # Plan distribution chart
        st.markdown("#### توزيع الخطط")
        if all_users_raw:
            plan_df = pd.DataFrame(
                [(p, c, PLAN_PRICING.get(p, 0) * c) for p, c in plan_counts.items()],
                columns=["الخطة", "عدد المستخدمين", "الإيراد الشهري (USD)"]
            )
            st.dataframe(plan_df, use_container_width=True, hide_index=True)

        # Manual plan override
        st.markdown("---")
        render_section_header("تعديل خطة مستخدم يدوياً", "🛠️")
        col_u, col_p = st.columns(2)
        m_user = col_u.text_input("اسم المستخدم", key="owner_manual_user")
        m_plan = col_p.selectbox("الخطة الجديدة", ["Explorer", "Strategist", "Command"], key="owner_manual_plan")
        if st.button("🚀 تطبيق الخطة فوراً", use_container_width=True):
            if m_user:
                update_plan(m_user, m_plan)
                log_activity(username, f"Owner manually set plan: {m_user} → {m_plan}")
                st.success(f"✅ تم ترقية {m_user} إلى {m_plan}")
            else:
                st.error("أدخل اسم المستخدم")

    # ═══════════════════════════════════════════════════════════
    # TAB 3 — PLATFORM ACTIVITY
    # ═══════════════════════════════════════════════════════════
    with tabs[2]:
        render_section_header("سجل نشاط المنصة الكامل", "📊")
        limit = st.slider("عدد السجلات", 20, 500, 100, key="owner_log_limit")
        activities = get_activity_log(limit=limit)
        if activities:
            act_df = pd.DataFrame(activities)
            act_df.columns = ["المستخدم", "الإجراء", "الوقت"]
            # Filter
            filter_user = st.text_input("🔍 فلترة بالمستخدم", key="owner_act_filter")
            if filter_user:
                act_df = act_df[act_df["المستخدم"].str.contains(filter_user, case=False)]
            st.dataframe(act_df, use_container_width=True, hide_index=True)

            # Export
            csv = act_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 تحميل السجل CSV", csv, "activity_log.csv", "text/csv")
        else:
            st.info("لا يوجد نشاط بعد")

    # ═══════════════════════════════════════════════════════════
    # TAB 4 — API KEYS (Global)
    # ═══════════════════════════════════════════════════════════
    with tabs[3]:
        render_section_header("مفاتيح API — إعداد عالمي للمنصة", "🔑")
        st.info("🔐 المفاتيح تُحفظ في الـ Session — لحفظها دائماً ضعها في `.streamlit/secrets.toml`")

        keys_config = [
            ("🤖 Google Gemini API Key", "GEMINI_API_KEY", "AIzaSy..."),
            ("📸 Meta (FB/IG) Access Token", "META_ACCESS_TOKEN", "EAAx..."),
            ("📘 Meta Page ID", "META_PAGE_ID", "12345678..."),
            ("🎵 TikTok Access Token", "TIKTOK_ACCESS_TOKEN", "..."),
            ("🎵 TikTok Advertiser ID", "TIKTOK_ADVERTISER_ID", "..."),
            ("🐦 Twitter/X Bearer Token", "TWITTER_BEARER_TOKEN", "AAAA..."),
            ("💳 Stripe Secret Key", "STRIPE_SECRET_KEY", "sk_live_..."),
        ]
        changed = False
        for label, key, placeholder in keys_config:
            current = st.session_state.get(key, "")
            new_val = st.text_input(label, value=current, type="password",
                                     placeholder=placeholder, key=f"owner_key_{key}")
            if new_val != current:
                st.session_state[key] = new_val
                changed = True

        if st.button("💾 حفظ جميع المفاتيح", use_container_width=True):
            log_activity(username, "Owner updated global API keys")
            st.success("✅ تم حفظ جميع المفاتيح في الـ Session")
            st.markdown("""
            **لحفظ دائم:** أضف في `.streamlit/secrets.toml`:
            ```toml
            GEMINI_API_KEY = "..."
            META_ACCESS_TOKEN = "..."
            ...
            ```
            """)

        st.markdown("---")
        render_section_header("اختبار الاتصال", "🔗")
        if st.button("🧪 اختبار Gemini API", use_container_width=True):
            gemini_key = st.session_state.get("GEMINI_API_KEY", "")
            if gemini_key:
                import urllib.request
                try:
                    req = urllib.request.Request(
                        f"https://generativelanguage.googleapis.com/v1beta/models?key={gemini_key}",
                        headers={"Content-Type": "application/json"}
                    )
                    urllib.request.urlopen(req, timeout=5)
                    st.success("✅ Gemini API متصل وجاهز!")
                except Exception as e:
                    st.error(f"❌ خطأ في الاتصال: {str(e)[:80]}")
            else:
                st.warning("أدخل Gemini API Key أولاً")

    # ═══════════════════════════════════════════════════════════
    # TAB 5 — SYSTEM SETTINGS
    # ═══════════════════════════════════════════════════════════
    with tabs[4]:
        render_section_header("إعدادات النظام العالمية", "⚙️")

        c_a, c_b = st.columns(2)
        with c_a:
            st.markdown("#### 🔒 أمان المنصة")
            max_attempts = st.number_input("حد محاولات تسجيل الدخول", min_value=3, max_value=20, value=5, key="owner_max_att")
            lockout_mins = st.number_input("مدة القفل (دقائق)", min_value=5, max_value=60, value=15, key="owner_lockout")
            allow_register = st.toggle("السماح بالتسجيل الذاتي", value=True, key="owner_allow_reg")

        with c_b:
            st.markdown("#### 📢 إشعارات النظام")
            maintenance_mode = st.toggle("🛠️ وضع الصيانة (يمنع دخول الجميع عدا Admin)", value=False, key="owner_maint")
            sys_msg = st.text_area("📢 رسالة للمستخدمين (تظهر لكل من يدخل)", key="owner_sys_msg", height=80)
            if st.button("📢 نشر الرسالة", use_container_width=True):
                st.session_state["system_broadcast"] = sys_msg
                st.success("✅ ستظهر الرسالة لكل المستخدمين")

        st.markdown("---")
        st.markdown("#### 📦 نسخ احتياطي للبيانات")
        if st.button("📥 تحميل قاعدة البيانات SQLite", use_container_width=True):
            try:
                with open("mtse_saas.db", "rb") as f:
                    db_bytes = f.read()
                st.download_button(
                    "⬇️ تحميل mtse_saas.db",
                    db_bytes,
                    f"mtse_backup_{today}.db",
                    "application/octet-stream"
                )
            except FileNotFoundError:
                st.error("قاعدة البيانات غير موجودة محلياً (ربما PostgreSQL)")

        if st.button("📜 تصدير كل المستخدمين CSV", use_container_width=True):
            df_u = pd.DataFrame(all_users_raw)
            csv = df_u.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ users_export.csv", csv, "users_export.csv", "text/csv")

    # ═══════════════════════════════════════════════════════════
    # TAB 6 — RAW DB QUERY (Owner only)
    # ═══════════════════════════════════════════════════════════
    with tabs[5]:
        render_section_header("استعلامات SQL مباشرة", "🗄️")
        st.warning("⚠️ هذه الأداة للاستخدام المتقدم فقط. الاستعلامات تُنفَّذ مباشرة على قاعدة البيانات.")
        sql_query = st.text_area("🗄️ SQL Query", value="SELECT username, plan, role FROM users LIMIT 10;",
                                  height=100, key="owner_sql")
        if st.button("▶️ تنفيذ الاستعلام", use_container_width=True):
            try:
                rows = conn.execute(sql_query).fetchall()
                if rows:
                    df_r = pd.DataFrame([dict(r) for r in rows])
                    st.dataframe(df_r, use_container_width=True, hide_index=True)
                    csv = df_r.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 تحميل النتيجة CSV", csv, "query_result.csv", "text/csv")
                else:
                    st.info("تم تنفيذ الاستعلام — لا توجد نتائج (ربما UPDATE/DELETE)")
                    conn.commit()
            except Exception as e:
                st.error(f"❌ خطأ: {e}")
