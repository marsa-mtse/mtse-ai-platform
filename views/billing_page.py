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
    
    current_plan = st.session_state.plan
    username = st.session_state.username
    billing = BillingEngine()

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>💳 {t("الفوترة والاشتراكات", "Billing & Subscriptions")}</h2>
        <p style="color:#94a3b8;">{t("إدارة خطتك الحالية وترقية حسابك", "Manage your plan and upgrade account")}</p>
        <span class="status-badge status-active">{t('الخطة الحالية:', 'Current Plan:')} {current_plan}</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    plans_info = [
        {"name": "Explorer", "price": PLAN_PRICING["Explorer"], "features": [t("التحليل العالمي المنفرد", "Single Omni-Analysis"), t("10 تقارير نخبورية/شهر", "10 Elite Reports/mo"), t("دعم البريد الإلكتروني", "Email Support")]},
        {"name": "Strategist", "price": PLAN_PRICING["Strategist"], "features": [t("ساحة معركة المنافسين", "Competitor Battleground"), t("تكامل المنصات (APIs)", "Platform APIs"), t("100 تقرير نخبوي/شهر", "100 Elite Reports/mo"), t("دعم تقني سريع", "Priority Support")]},
        {"name": "Command", "price": PLAN_PRICING["Command"], "features": [t("مركز قيادة المشاعر", "Sentiment Command"), t("تحليل غير محدود", "Unlimited Analysis"), t("العلامة البيضاء (White Label)", "White Label Engine"), t("دعم مخصص 24/7", "Dedicated Elite Support")]}
    ]
    
    cols = [col1, col2, col3]
    
    for i, plan in enumerate(plans_info):
        with cols[i]:
            is_current = (current_plan == plan["name"])
            # Using brighter, high-contrast colors for prices
            accent_color = "#818cf8" if plan["name"] == "Strategist" else "#22d3ee" if plan["name"] == "Command" else "#94a3b8"
            border_color = "#6366f1" if plan["name"] == "Strategist" else "#0ea5e9" if plan["name"] == "Command" else "#334155"
            bg_color = "rgba(99, 102, 241, 0.1)" if is_current else "rgba(30, 41, 59, 0.5)"
            
            st.markdown(f"""
            <div class="glass-card" style="border: 2px solid {border_color}; text-align:center; position:relative; background:{bg_color}; min-height:480px;">
                {"<div style='position:absolute; top:-12px; right:10px; background:#6366f1; color:white; padding:4px 12px; border-radius:12px; font-size:12px; font-weight:bold;'>Current</div>" if is_current else ""}
                <h3 style="margin-top:0; color:#f8fafc;">{plan["name"]}</h3>
                <div style="font-size:3rem; font-weight:800; color:white; margin:16px 0;">
                    <span style="font-size:1.5rem; vertical-align:top; color:{accent_color};">$</span>{plan["price"]}
                    <span style="font-size:1.1rem; color:#94a3b8; font-weight:400;">/mo</span>
                </div>
                <ul style="list-style:none; padding:0; text-align:left; color:#cbd5e1; margin-bottom:24px; font-size: 0.95rem;">
                    {''.join([f'<li style="margin:12px 0;">🔹 {feat}</li>' for feat in plan['features']])}
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_current:
                if st.button(f"{t('ترقية إلى', 'Upgrade to')} {plan['name']}", key=f"upgrade_{plan['name']}", use_container_width=True):
                    result = billing.create_checkout_session(plan["name"], plan["price"])
                    if result["status"] in ["success", "simulation"]:
                        st.info(f"🔗 {result['message']}" if 'message' in result else "🔗 Redirecting to Stripe...")
                        st.markdown(f"[💳 {t('رابط الدفع المباشر', 'Pay Here')} -> {plan['name']}]({result['url']})")
                    else:
                        st.error(f"Error: {result['message']}")
            else:
                st.button(t("الخطة الحالية", "Current Plan"), key=f"curr_{plan['name']}", disabled=True, use_container_width=True)

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
