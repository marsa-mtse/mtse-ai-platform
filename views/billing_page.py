import streamlit as st
import pandas as pd
from utils import t, render_section_header
from config import PLAN_PRICING, PRIMARY, ACCENT, SUCCESS, WARNING, DANGER, PRIMARY_LIGHT
from billing.stripe import BillingEngine

def render():
    """Render the Billing & Subscription page."""
    
    username = st.session_state.username
    from database import get_user
    user_data = get_user(username)
    current_plan = user_data.get("plan", "Explorer")
    status = user_data.get("subscription_status", "Active")
    expiry = user_data.get("plan_expiry", "N/A")
    billing = BillingEngine()

    st.markdown(f"""
    <div class="glass-card animate-in" style="
        background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(6,182,212,0.06));
        border-bottom: 4px solid {PRIMARY};
        text-align: center; margin-bottom: 28px;
    ">
        <h1 style="margin:0 0 6px;">💳 {t("الفوترة والاشتراكات", "Billing & Subscriptions")}</h1>
        <p style="color:#94a3b8; margin:0;">{t("إدارة خطتك الحالية وترقية حسابك للحصول على إمكانيات أكثر", "Manage your plan and upgrade for more capabilities")}</p>
        <div style="display:flex; justify-content:center; gap:16px; margin-top:16px; flex-wrap:wrap;">
            <span class="status-badge badge-active">{t('الخطة الحالية:', 'Current Plan:')} <b>{current_plan}</b></span>
            <span class="status-badge badge-warning">{t('الحالة:', 'Status:')} {status}</span>
            <span class="status-badge" style="background:rgba(255,255,255,0.07); color:#94a3b8;">{t('انتهاء:', 'Expiry:')} {expiry[:10] if expiry and expiry != 'N/A' else 'N/A'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── PRICING CARDS ────────────────────────────────────────────────────────
    plans_info = [
        {
            "name": "Explorer", "price": 0, "period": t("مجاناً","Free"),
            "color": SUCCESS, "icon": "🆓",
            "label": "FREE",
            "features": [
                t("3 تقارير ذكية/شهر", "3 AI Reports/month"),
                t("3 عمليات رفع/شهر", "3 Uploads/month"),
                t("لوحة التحكم الأساسية", "Basic Dashboard"),
                t("محلل الروابط العالمي", "Universal Link Analyzer"),
                t("دعم عبر البريد", "Email Support"),
            ],
            "disabled": []
        },
        {
            "name": "Starter", "price": 19, "period": "/mo",
            "color": WARNING, "icon": "⚡",
            "label": "STARTER",
            "features": [
                t("30 تقرير/شهر", "30 Reports/month"),
                t("30 عملية رفع/شهر", "30 Uploads/month"),
                t("توليد الحملات", "Campaign Generator"),
                t("ستوديو الإبداع", "Creative Studio"),
                t("دعم سريع", "Priority Support"),
            ],
            "disabled": []
        },
        {
            "name": "Strategist", "price": 69, "period": "/mo",
            "color": PRIMARY, "icon": "🚀",
            "label": "STRATEGIST",
            "featured": True,
            "features": [
                t("200 تقرير/شهر", "200 Reports/month"),
                t("200 عملية رفع/شهر", "200 Uploads/month"),
                t("ساحة معركة المنافسين", "Competitor Battleground"),
                t("مختبر الانتشار الفيروسي", "Virality Lab"),
                t("تكامل TikTok & Instagram", "TikTok & Instagram APIs"),
                t("دعم تقني متميز", "Priority Tech Support"),
            ],
            "disabled": []
        },
        {
            "name": "Command", "price": 199, "period": "/mo",
            "color": DANGER, "icon": "👑",
            "label": "COMMAND",
            "features": [
                t("تقارير غير محدودة", "Unlimited Reports"),
                t("رفع غير محدود", "Unlimited Uploads"),
                t("تحليل المشاعر النفسي", "Sentiment Command"),
                t("تكامل APIs الكامل", "Full API Integration"),
                t("العلامة البيضاء (White Label)", "White Label Engine"),
                t("مدير حساب مخصص 24/7", "24/7 Dedicated Manager"),
            ],
            "disabled": []
        },
    ]

    p_cols = st.columns(4)
    for i, plan in enumerate(plans_info):
        with p_cols[i]:
            is_current = (current_plan == plan["name"])
            c = plan["color"]
            is_featured = plan.get("featured", False)
            border = f"2px solid {c}" if (is_current or is_featured) else f"1px solid {c}33"
            shadow  = f"0 0 0 2px {c}33, 0 20px 40px rgba(0,0,0,0.3)" if is_featured else ""

            # Price display
            price_txt = (
                f"<span style='color:{c};font-size:1.8rem;font-weight:900;'>{t('مجاناً','FREE')}</span>"
                if plan["price"] == 0
                else f"<span style='font-size:1.1rem;color:{c};'>$</span><span style='font-size:2.6rem;font-weight:900;color:white;'>{plan['price']}</span><span style='color:#64748b;font-size:0.9rem;'>{plan['period']}</span>"
            )

            featured_badge = f"""<div style='position:absolute;top:-12px;left:50%;transform:translateX(-50%);background:{c};color:white;font-size:0.72rem;font-weight:800;padding:3px 14px;border-radius:12px;letter-spacing:1px;white-space:nowrap;'>⭐ {t("الأكثر شعبية","Most Popular")}</div>""" if is_featured else ""

            features_html = "".join([
                f"<li style='margin:8px 0; display:flex; align-items:center; gap:8px; color:#cbd5e1; font-size:0.88rem;'><span style='color:{c};'>✓</span> {feat}</li>"
                for feat in plan["features"]
            ])

            st.markdown(f"""
            <div style="
                background: rgba(255,255,255,0.03);
                border: {border};
                border-radius: 24px; padding: 28px 22px;
                text-align: center;
                position: relative; overflow: visible;
                min-height: 480px;
                box-shadow: {shadow};
                transition: transform 0.3s ease;
            ">
                {featured_badge}
                <div style='font-size:2.2rem; margin-bottom:8px;'>{plan['icon']}</div>
                <h3 style='color:{c}; margin:0 0 6px; font-weight:900; letter-spacing:0.5px;'>{plan['name']}</h3>
                <div style='margin: 18px 0;'>{price_txt}</div>
                <ul style='list-style:none; padding:0; text-align:left; margin:0 0 20px;'>{features_html}</ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)
            if is_current:
                st.button(t("✅ خطتك الحالية", "✅ Your Current Plan"), disabled=True, use_container_width=True, key=f"cur_{plan['name']}")
            else:
                btn_label = t(f"ابدأ مجاناً", "Get Started Free") if plan["price"] == 0 else t(f"ترقية إلى {plan['name']}", f"Upgrade to {plan['name']}")
                if st.button(btn_label, key=f"up_{plan['name']}", use_container_width=True):
                    if plan["price"] == 0:
                        from database import update_plan
                        update_plan(username, "Explorer")
                        st.success(t("✅ تم التحويل للخطة المجانية!", "✅ Switched to Free Plan!"))
                        st.rerun()
                    else:
                        result = billing.create_checkout_session(plan["name"], plan["price"], username=username)
                        if result["status"] in ["success", "simulation"]:
                            st.success(t("🔗 اختر وسيلة الدفع المناسبة", "🔗 Choose Payment Method"))
                            # New Multiple Payment Gateways Simulation
                            pcol1, pcol2 = st.columns(2)
                            with pcol1:
                                st.markdown(f'<a href="{result["url"]}" target="_blank" style="display:block;text-align:center;background:#000000;color:white;padding:10px;border-radius:10px;text-decoration:none;margin-bottom:8px;font-weight:bold;">🍎 Apple Pay</a>', unsafe_allow_html=True)
                                st.markdown(f'<a href="{result["url"]}" target="_blank" style="display:block;text-align:center;background:#003087;color:white;padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;">🅿️ PayPal</a>', unsafe_allow_html=True)
                            with pcol2:
                                st.markdown(f'<a href="{result["url"]}" target="_blank" style="display:block;text-align:center;background:#20a672;color:white;padding:10px;border-radius:10px;text-decoration:none;margin-bottom:8px;font-weight:bold;">💳 مدى / KNET</a>', unsafe_allow_html=True)
                                st.markdown(f'<a href="{result["url"]}" target="_blank" style="display:block;text-align:center;background:{PRIMARY};color:white;padding:10px;border-radius:10px;text-decoration:none;font-weight:bold;">🌐 Crypto (USDT)</a>', unsafe_allow_html=True)


    # Simulation tools for V10 testing
    st.markdown("---")
    with st.expander(t("🛠️ أدوات المطور (فحص الترقية)", "Developer Tools (Audit Upgrade)")):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button(t("🚀 محاكاة نجاح الدفع (ترقية لـ Command)", "Simulate Payment Success (To Command)")):
                from billing.webhook_handler import simulate_upgrade
                success, msg = simulate_upgrade(username, "Command")
                if success:
                    st.success(msg)
                    st.rerun()
        with col_s2:
            if st.button(t("🔄 تصفير الحساب لـ Explorer", "Reset to Explorer")):
                from database import update_plan
                update_plan(username, "Explorer")
                st.rerun()

    # Invoices history mock
    st.markdown("---")
    render_section_header(t("سجل الفواتير", "Invoices History"), "🧾")
    
    mock_invoices = pd.DataFrame({
        t("التاريخ", "Date"): ["2026-03-01", "2026-02-01", "2026-01-01"],
        t("المبلغ", "Amount"): [f"${PLAN_PRICING[current_plan]}"] * 3,
        t("الحالة", "Status"): ["Paid", "Paid", "Paid"],
        t("تحميل", "Download"): ["PDF ⬇️", "PDF ⬇️", "PDF ⬇️"]
    })
    st.dataframe(mock_invoices, use_container_width=True)
    
    if st.button(t("❌ إلغاء الاشتراك", "❌ Cancel Subscription")):
        st.warning(t("سيتم إيقاف الميزات المتقدمة فوراً.", "Advanced features will be downgraded."))
        res, msg = billing.cancel_subscription("sub_mock_123")
        if res:
            st.success(msg)
