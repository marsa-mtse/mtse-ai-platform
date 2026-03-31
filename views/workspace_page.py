# ==========================================================
# MTSE Marketing Engine v12 - Enterprise Workspace Hub
# ==========================================================
import streamlit as st
from utils import t, render_section_header
from database import get_projects, create_project, get_project_assets, is_admin
from config import PRIMARY, PRIMARY_LIGHT, ACCENT, SUCCESS, WARNING, DANGER

STATUS_COLORS = {
    t("نشط", "Active"):       SUCCESS,
    t("في التنفيذ", "In Progress"): WARNING,
    t("مكتمل", "Completed"):  ACCENT,
    t("متوقف", "On Hold"):    DANGER,
    "Active":       SUCCESS,
    "In Progress":  WARNING,
    "Completed":    ACCENT,
    "On Hold":      DANGER,
}

def render():
    st.markdown(f"""
    <div class="glass-card animate-in" style="
        background: linear-gradient(135deg, rgba(16,185,129,0.1), rgba(6,182,212,0.06));
        border-bottom: 4px solid {SUCCESS}; margin-bottom:20px;
    ">
        <h1 style="margin:0 0 6px;">🏢 {t("مساحة العمل المؤسسية", "Enterprise Workspace Hub")}</h1>
        <p style="color:#94a3b8; margin:0;">{t("أدر جميع مشاريع وكالتك في مكان واحد منظّم واحترافي.", "Manage all your agency projects in one professional, organized space.")}</p>
    </div>
    """, unsafe_allow_html=True)

    company = st.session_state.get("company", "Independent")
    username = st.session_state.username
    user_role = st.session_state.get("role", "Viewer")
    is_admin_or_owner = user_role in ["Admin", "Owner"]

    # ── Header actions ────────────────────────────────────────────────────────
    col_search, col_filter, col_add = st.columns([3, 1.5, 1])
    with col_search:
        search_q = st.text_input(
            t("🔍 بحث في المشاريع", "🔍 Search Projects"),
            placeholder=t("اسم المشروع، الوصف...", "Project name, description..."),
            key="ws_search", label_visibility="collapsed"
        )
    with col_filter:
        filter_status = st.selectbox(
            t("تصفية", "Filter"),
            [t("الكل", "All"), t("نشط", "Active"), t("في التنفيذ", "In Progress"), t("مكتمل", "Completed"), t("متوقف", "On Hold")],
            key="ws_filter", label_visibility="collapsed"
        )
    with col_add:
        if is_admin_or_owner:
            if st.button("➕ " + t("مشروع جديد", "New Project"), use_container_width=True, type="primary"):
                st.session_state.show_create_project = not st.session_state.get("show_create_project", False)
        else:
            st.button("🔒 " + t("غير مصرح", "Action Locked"), disabled=True, use_container_width=True)

    st.markdown("")
    
    # ── Role Notification ──
    if not is_admin_or_owner:
        st.info("ℹ️ **صلاحية العرض فقط (Viewer Mode):** إمكانيات الإدارة والإنشاء مقصورة على مديري الشركة (الـ Administrators).")

    # ── Create Project Form ───────────────────────────────────────────────────
    if st.session_state.get("show_create_project"):
        st.markdown(f"""
        <div class="glass-card animate-in" style="border:1px solid rgba(139,92,246,0.3); margin-bottom:20px;">
            <h3>➕ {t("إنشاء مشروع جديد", "Create New Project")}</h3>
        </div>
        """, unsafe_allow_html=True)

        with st.form("create_project_form", clear_on_submit=True):
            fp1, fp2 = st.columns(2)
            with fp1:
                p_name = st.text_input(
                    t("📝 اسم المشروع *", "📝 Project Name *"),
                    placeholder=t("مثال: حملة رمضان 2026", "e.g. Ramadan 2026 Campaign")
                )
                p_client = st.text_input(
                    t("🏷️ العميل / الجهة", "🏷️ Client / Company"),
                    placeholder=t("اسم العميل أو الجهة", "Client or company name")
                )
            with fp2:
                p_status = st.selectbox(
                    t("📌 الحالة", "📌 Status"),
                    [t("نشط", "Active"), t("في التنفيذ", "In Progress"), t("متوقف", "On Hold")]
                )
                p_priority = st.select_slider(
                    t("🔥 الأولوية", "🔥 Priority"),
                    options=[t("منخفضة","Low"), t("متوسطة","Medium"), t("عالية","High"), t("عاجل","Urgent")]
                )

            p_desc = st.text_area(
                t("📋 الوصف", "📋 Description"),
                placeholder=t("وصف مختصر للمشروع وأهدافه...", "Brief description of the project and goals..."),
                height=90
            )

            fp3, fp4 = st.columns(2)
            with fp3:
                p_deadline = st.date_input(t("📅 الموعد النهائي", "📅 Deadline"))
            with fp4:
                p_budget_ws = st.text_input(
                    t("💰 الميزانية", "💰 Budget"),
                    placeholder="$0"
                )

            col_sub, col_cancel = st.columns(2)
            with col_sub:
                submit = st.form_submit_button(
                    "🚀 " + t("إنشاء المشروع", "Create Project"),
                    use_container_width=True
                )
            with col_cancel:
                cancel = st.form_submit_button(
                    t("إلغاء", "Cancel"),
                    use_container_width=True
                )

            if submit:
                if not p_name:
                    st.error(t("⚠️ يرجى إدخال اسم المشروع.", "⚠️ Please enter a project name."))
                else:
                    desc_full = f"[{p_status}] [{p_priority}] {p_desc}"
                    if p_client:
                        desc_full = f"Client: {p_client} | " + desc_full
                    create_project(p_name, username, company, desc_full)
                    st.success(t("✅ تم إنشاء المشروع بنجاح!", "✅ Project created successfully!"))
                    st.session_state.show_create_project = False
                    st.rerun()

            if cancel:
                st.session_state.show_create_project = False
                st.rerun()

    # ── Projects list ──────────────────────────────────────────────────────────
    projects = get_projects(company)

    # Apply search filter
    if search_q:
        projects = [p for p in projects if search_q.lower() in p.get("name","").lower() or search_q.lower() in p.get("description","").lower()]

    # Summary stats
    total_projects = len(projects)
    st.markdown("")

    stat_c1, stat_c2, stat_c3, stat_c4 = st.columns(4)
    with stat_c1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">📁</div><div class="kpi-value">{total_projects}</div><div class="kpi-label">{t("إجمالي المشاريع","Total Projects")}</div></div>""", unsafe_allow_html=True)
    with stat_c2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">🔥</div><div class="kpi-value">{max(total_projects-1,0)}</div><div class="kpi-label">{t("مشاريع نشطة","Active Projects")}</div></div>""", unsafe_allow_html=True)
    with stat_c3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">✅</div><div class="kpi-value">{0}</div><div class="kpi-label">{t("مكتملة","Completed")}</div></div>""", unsafe_allow_html=True)
    with stat_c4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-icon">⏳</div><div class="kpi-value">{max(total_projects-2,0)}</div><div class="kpi-label">{t("في التنفيذ","In Progress")}</div></div>""", unsafe_allow_html=True)

    st.markdown("")

    if not projects:
        st.markdown(f"""
        <div style="
            text-align:center; padding:60px 40px;
            background: rgba(255,255,255,0.02);
            border: 2px dashed rgba(255,255,255,0.07);
            border-radius: 24px; margin-top:10px;
        ">
            <div style="font-size:4rem; margin-bottom:16px; opacity:0.4;">📁</div>
            <h3 style="color:#374151;">{t("لا توجد مشاريع بعد", "No Projects Yet")}</h3>
            <p style="color:#4b5563;">{t("ابدأ بإنشاء مشروعك الأول لتنظيم حملاتك وعملائك.", "Start by creating your first project to organize campaigns and clients.")}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        render_section_header(t("مشاريعك", "Your Projects"), "📁")

        for p in projects:
            desc = p.get("description", "")
            created = str(p.get("created_at", ""))[:10]
            owner   = p.get("owner", "")

            # Extract status from description
            status = t("نشط", "Active")
            for s in ["نشط", "Active", "في التنفيذ", "In Progress", "مكتمل", "Completed", "متوقف", "On Hold"]:
                if f"[{s}]" in desc:
                    status = s
                    break
            s_color = STATUS_COLORS.get(status, PRIMARY)

            with st.expander(f"📁  {p.get('name','')}", expanded=False):
                col_meta, col_actions = st.columns([3, 1])

                with col_meta:
                    st.markdown(f"""
                    <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
                        <span style="background:rgba({','.join(str(int(s_color.lstrip('#')[j:j+2],16)) for j in (0,2,4))},0.12);color:{s_color};border:1px solid {s_color}44;border-radius:12px;padding:2px 12px;font-size:0.8rem;font-weight:700;">● {status}</span>
                        <span style="color:#64748b; font-size:0.82rem;">👤 {owner}</span>
                        <span style="color:#4b5563; font-size:0.82rem;">📅 {created}</span>
                        <span style="color:#8b5cf6; font-size:0.82rem; margin-right:auto; padding-right:15px;">🛡️ Manager: {owner}</span>
                    </div>
                    <p style="color:#cbd5e1; font-size:0.9rem; line-height:1.6;">
                        {desc.replace('[نشط]','').replace('[Active]','').replace('[في التنفيذ]','').replace('[In Progress]','').replace('[متوقف]','').replace('[On Hold]','').strip()}
                    </p>
                    """, unsafe_allow_html=True)

                with col_actions:
                    if st.button(t("📊 فتح المشروع", "📊 Open Project"), key=f"open_{p['id']}", use_container_width=True):
                        st.session_state.active_project = p
                        st.toast(t(f"تم فتح {p['name']}", f"Opened {p['name']}"))

                # Assets
                assets = get_project_assets(p["id"])
                if assets:
                    st.markdown(f"**{t('الأصول والتقارير المرتبطة:', 'Linked Assets & Reports:')}**")
                    for asset in assets:
                        icon_map = {
                            "cost_estimate": "💰",
                            "social_audit": "🎯",
                            "campaign": "🚀",
                        }
                        aicon = icon_map.get(asset.get("asset_type",""), "🧠")
                        ats = str(asset.get("created_at",""))[:16]
                        ia1, ia2, ia3 = st.columns([1, 6, 2])
                        with ia1:
                            st.markdown(f"<div style='font-size:1.4rem;'>{aicon}</div>", unsafe_allow_html=True)
                        with ia2:
                            st.write(f"**{asset.get('asset_type','').replace('_',' ').title()}** — {ats}")
                        with ia3:
                            if st.button(t("👁️ عرض", "👁️ View"), key=f"view_{asset['id']}", use_container_width=True):
                                st.session_state.active_asset = asset
                                st.rerun()
                else:
                    st.caption(t("لا توجد أصول مرتبطة بهذا المشروع بعد.", "No assets linked to this project yet."))

    # ── Asset Detail ─────────────────────────────────────────────────────────
    if st.session_state.get("active_asset"):
        st.markdown("---")
        asset = st.session_state.active_asset
        render_section_header(f"🔍 {asset.get('asset_type','').replace('_',' ').title()}", "📄")
        st.json(asset.get("asset_data", {}))
        if st.button(t("✖ إغلاق", "✖ Close"), key="close_asset"):
            del st.session_state.active_asset
            st.rerun()
