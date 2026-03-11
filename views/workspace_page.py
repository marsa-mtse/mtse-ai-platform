# ==========================================================
# MTSE Marketing Engine - Enterprise Workspace Hub
# ==========================================================
import streamlit as st
from utils import t, render_section_header
from database import get_projects, create_project, get_project_assets, is_admin

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center; border-bottom: 4px solid #10b981;">
        <h2>🏢 {t("مساحة العمل المؤسسية", "Enterprise Workspace Hub")}</h2>
        <p style="color:#94a3b8;">{t("أدر جميع مشاريع وكالتك في مكان واحد منظّم", "Manage all your agency projects in one organized space")}</p>
    </div>
    """, unsafe_allow_html=True)

    company = st.session_state.get("company", "Independent")
    
    # Header Actions
    col_search, col_add = st.columns([3, 1])
    with col_add:
        if st.button(t("➕ مشروع جديد", "➕ New Project"), use_container_width=True, type="primary"):
            st.session_state.show_create_project = True

    if st.session_state.get("show_create_project"):
        with st.form("create_project_form"):
            st.markdown(f"### {t('إنشاء مشروع جديد', 'Create New Project')}")
            p_name = st.text_input(t("اسم المشروع", "Project Name"))
            p_desc = st.text_area(t("الوصف", "Description"))
            submit = st.form_submit_button(t("🚀 إنشاء", "🚀 Create"))
            if submit:
                if p_name:
                    create_project(p_name, st.session_state.username, company, p_desc)
                    st.success(t("✅ تم إنشاء المشروع!", "✅ Project created!"))
                    st.session_state.show_create_project = False
                    st.rerun()
                else:
                    st.error(t("يرجى إدخال اسم المشروع", "Please enter project name"))
        if st.button(t("إلغاء", "Cancel")):
            st.session_state.show_create_project = False
            st.rerun()

    # List Projects
    projects = get_projects(company)
    
    if not projects:
        st.info(t("لا توجد مشاريع حالياً. ابدأ بإنشاء مشروعك الأول!", "No projects found. Create your first project!"))
    else:
        for p in projects:
            with st.expander(f"📁 {p['name']} ({p['owner']}) - {p['created_at'][:10]}"):
                st.write(p['description'])
                
                assets = get_project_assets(p['id'])
                if not assets:
                    st.write(t("لا توجد ملفات أو تقارير لهذا المشروع بعد.", "No assets or reports linked to this project yet."))
                else:
                    st.markdown("---")
                    st.markdown(f"**{t('الأصول والتقارير:', 'Assets & Reports:')}**")
                    for asset in assets:
                        col_icon, col_info = st.columns([1, 10])
                        with col_icon:
                            icon = "💰" if asset['asset_type'] == "cost_estimate" else "🎯" if asset['asset_type'] == "social_audit" else "🧠"
                            st.markdown(f"### {icon}")
                        with col_info:
                            st.write(f"**{asset['asset_type'].replace('_', ' ').title()}** - {asset['created_at'][:16]}")
                            if st.button(t("👁️ عرض التفاصيل", "👁️ View Details"), key=f"view_asset_{asset['id']}"):
                                st.session_state.active_asset = asset
                                st.rerun()

    # Asset Detail View (Modal-like)
    if st.session_state.get("active_asset"):
        asset = st.session_state.active_asset
        st.markdown("---")
        render_section_header(f"Asset: {asset['asset_type'].title()}", "🔍")
        st.json(asset['asset_data'])
        if st.button(t("إغلاق", "Close")):
            del st.session_state.active_asset
            st.rerun()
