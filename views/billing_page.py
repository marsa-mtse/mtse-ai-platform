# ==========================================================
# MTSE Marketing Engine - Billing Page Update
# ==========================================================

import streamlit as st
import pandas as pd
from utils import t, render_section_header
from config import PLAN_PRICING
from billing.stripe import BillingEngine

def render():
    """Render the Billing & Subscription page."""
    
    username = st.session_state.username
    from database import get_user
    user_data = get_user(username)
    current_plan = user_data.get("plan", "Starter")
    status = user_data.get("subscription_status", "Active")
    expiry = user_data.get("plan_expiry", "N/A")
    billing = BillingEngine()

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>💳 {t("الفوترة والاشتراكات", "Billing & Subscriptions")}</h2>
        <p style="color:#94a3b8;">{t("إدارة خطتك الحالية وترقية حسابك", "Manage your plan and upgrade account")}</p>
        <div style="display:flex; justify-content:center; gap:20px; margin-top:15px;">
            <span class="status-badge badge-active">{t('الخطة:', 'Plan:')} {current_plan}</span>
            <span class="status-badge badge-warning">{t('الحالة:', 'Status:')} {status}</span>
            <span class="status-badge" style="background:rgba(255,255,255,0.1);">{t('تاريخ الانتهاء:', 'Expiry:')} {expiry[:10] if expiry else 'N/A'}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    plans_info = [
        {"name": "Starter", "price": PLAN_PRICING["Starter"], "features": [t("التحليل العالمي المنفرد", "Single Omni-Analysis"), t("5 حملات تسويقية/شهر", "5 AI Campaigns/mo"), t("دعم المجتمع", "Community Support")]},
        {"name": "Pro", "price": PLAN_PRICING["Pro"], "features": [t("استوديو الصور (DALL-E 3)", "AI Image Studio"), t("قناص السوشيال ميديا", "Social Sniper"), t("200 تقرير نخبوي/شهر", "200 Elite Reports/mo"), t("دعم تقني سريع", "Priority Support")]},
        {"name": "Command", "price": PLAN_PRICING["Command"], "features": [t("مركز قيادة المشاعر", "Sentiment Command"), t("التنبؤ بالاتجاهات (Trends)", "Trend Predictor"), t("العلامة البيضاء (White Label)", "White Label Engine"), t("دعم مخصص 24/7", "Dedicated Elite Support")]}
    ]
    
    cols = [col1, col2, col3]
    
    for i, plan in enumerate(plans_info):
        with cols[i]:
            is_current = (current_plan == plan["name"])
            accent_color = "#34d399" if plan["name"] == "Starter" else "#a78bfa" if plan["name"] == "Pro" else "#f0abfc"
            border_color = "#6366f1" if is_current else ("#34d399" if plan["name"] == "Starter" else "#a855f7" if plan["name"] == "Pro" else "#e879f9")
            
            st.markdown(f"""
            <div class="glass-card" style="border: 2px solid {border_color}; text-align:center; background:rgba(255,255,255,0.03); min-height:510px;">
                <h3 style="color:#f8fafc;">{plan["name"]}</h3>
                <div style="font-size:2.8rem; font-weight:900; color:white; margin:15px 0;">
                    <span style="font-size:1.2rem; color:{accent_color};">{t("ج.م", "EGP")}</span>{plan["price"]}
                </div>
                <ul style="list-style:none; padding:0; text-align:left; color:#94a3b8; font-size: 0.9rem;">
                    {''.join([f'<li style="margin:10px 0;">✅ {feat}</li>' for feat in plan['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_current:
                if st.button(t(f"ترقية إلى {plan['name']}", f"Upgrade to {plan['name']}"), key=f"up_bil_{plan['name']}", use_container_width=True):
                    result = billing.create_checkout_session(plan["name"], plan["price"], username=username)
                    if result["status"] in ["success", "simulation"]:
                        st.success(t("🔗 الرابط جاهز للدفع", "🔗 Payment Link Ready"))
                        st.markdown(f'<a href="{result["url"]}" target="_blank" style="display:block; text-align:center; background:#6366f1; color:white; padding:10px; border-radius:8px; text-decoration:none;">💳 {t("إتمام الدفع الان", "Complete Payment Now")}</a>', unsafe_allow_html=True)
            else:
                st.button(t("خطتك الحالية", "Current Plan"), disabled=True, key=f"curr_bil_{plan['name']}", use_container_width=True)

    # Simulation tools for V10 testing
    st.markdown("---")
    with st.expander(t("🛠️ أدوات المطور (فحص الترقية)", "Developer Tools (Audit Upgrade)")):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            if st.button(t("🚀 محاكاة نجاح الدفع (ترقية لـ Command)", "Simulate Payment Success (To Command)"), key="sim_cmd"):
                from billing.webhook_handler import simulate_upgrade
                success, msg = simulate_upgrade(username, "Command")
                if success:
                    st.success(msg)
                    st.rerun()
        with col_s2:
            if st.button(t("🔄 تصفير الحساب لـ Starter", "Reset to Starter"), key="sim_reset"):
                from database import update_plan
                update_plan(username, "Starter")
                st.rerun()

    # Invoices history mock
    st.markdown("---")
    render_section_header(t("سجل الفواتير", "Invoices History"), "🧾")
    
    # Safely get current plan price for invoice mock
    price_val = PLAN_PRICING.get(current_plan, 0)
    
    mock_invoices = pd.DataFrame({
        t("التاريخ", "Date"): ["2026-03-01", "2026-02-01", "2026-01-01"],
        t("المبلغ", "Amount"): [f"{price_val} {t('ج.م', 'EGP')}"] * 3,
        t("الحالة", "Status"): ["Paid", "Paid", "Paid"],
        t("تحميل", "Download"): ["PDF ⬇️", "PDF ⬇️", "PDF ⬇️"]
    })
    st.dataframe(mock_invoices, use_container_width=True)
    
    if st.button(t("❌ إلغاء الاشتراك", "❌ Cancel Subscription")):
        st.warning(t("سيتم إيقاف الميزات المتقدمة فوراً.", "Advanced features will be downgraded."))
        res, msg = billing.cancel_subscription("sub_mock_123")
        if res:
            st.success(msg)

    st.dataframe(mock_invoices, use_container_width=True)
    
    if st.button(t("❌ إلغاء الاشتراك", "❌ Cancel Subscription")):
        st.warning(t("سيتم إيقاف الميزات المتقدمة فوراً.", "Advanced features will be downgraded."))
        res, msg = billing.cancel_subscription("sub_mock_123")
        if res:
            st.success(msg)
