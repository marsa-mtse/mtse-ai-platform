# ==========================================================
# MTSE Marketing Engine - Utility Functions
# ==========================================================
import streamlit as st

# ==============================
# TRANSLATION HELPER
# ==============================

def t(ar, en):
    """Return Arabic or English text based on language setting."""
    return ar if st.session_state.get("lang") == "AR" else en


# ==============================
# ARABIC TEXT FORMATTING
# ==============================

def get_pdf_engine():
    """Safely load PDF libraries and report errors."""
    missing = []
    FPDF, reshaper, bidi = None, None, None
    
    try:
        from fpdf import FPDF
    except ImportError:
        missing.append("fpdf2")
    
    try:
        import arabic_reshaper as reshaper
    except ImportError:
        missing.append("arabic-reshaper")
        
    try:
        from bidi.algorithm import get_display as bidi
    except ImportError:
        missing.append("python-bidi")
    
    if missing:
        st.error(f"⚠️ Missing libraries for PDF: {', '.join(missing)}")
        return None, None, None
        
    return FPDF, reshaper, bidi

def format_arabic(text):
    """Reshape Arabic text for PDF rendering."""
    _, reshaper, bidi = get_pdf_engine()
    if not reshaper or not bidi:
        return text
    try:
        reshaped = reshaper.reshape(text)
        return bidi(reshaped)
    except Exception as e:
        st.warning(f"Arabic Formatting Error: {e}")
        return text

def generate_branded_pdf(report_data, lang="Both"):
    """
    Generates a professional PDF with branding.
    """
    import os
    FPDF, _, _ = get_pdf_engine()
    if not FPDF:
        return None

    try:
        class BrandedPDF(FPDF):
            def header(self):
                logo_path = 'assets/logo_premium.png'
                if os.path.exists(logo_path):
                    try:
                        self.image(logo_path, 10, 8, 30)
                    except Exception as e:
                        st.warning(f"Logo print error: {e}")
                else:
                    self.set_font('Helvetica', 'B', 15)
                    self.cell(0, 10, 'MTSE AI Platform', 0, 0, 'L')
                
                self.ln(20)
                self.set_draw_color(26, 115, 232)
                self.line(10, 32, 200, 32)
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font('Helvetica', 'I', 8)
                self.set_text_color(150)
                self.cell(0, 10, f'Page {self.page_no()} | MTSE Digital Marketing Engine', 0, 0, 'C')

        pdf = BrandedPDF()
        pdf.add_page()
        
        pdf.set_font('Helvetica', 'B', 18)
        pdf.set_text_color(26, 115, 232)
        title = format_arabic(report_data.get("title", "Strategic Report"))
        pdf.cell(0, 12, title, 0, 1, 'C')
        pdf.ln(8)

        for section in report_data.get("sections", []):
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(33, 33, 33)
            heading = format_arabic(section.get("heading", ""))
            pdf.cell(0, 10, heading, 0, 1, 'L')
            
            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(66, 66, 66)
            content = format_arabic(section.get("content", ""))
            pdf.multi_cell(0, 7, content)
            pdf.ln(4)

        return pdf.output()
    except Exception as e:
        st.error(f"Critical PDF Runtime Error: {e}")
        return None


# ==============================
# UI COMPONENTS
# ==============================

def render_kpi_card(label, value, icon="📊", delta=None):
    """Render a styled KPI card."""
    delta_html = ""
    if delta is not None:
        color = "#10b981" if delta >= 0 else "#ef4444"
        arrow = "↑" if delta >= 0 else "↓"
        delta_html = f'<div style="color:{color}; font-size:0.85rem; margin-top:4px;">{arrow} {abs(delta)}%</div>'

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <div style="font-size:1.8rem; margin-bottom:4px;">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def render_usage_bar(label, used, total):
    """Render a usage progress bar."""
    percentage = min((used / total * 100) if total > 0 else 0, 100)

    if percentage < 50:
        color = "linear-gradient(90deg, #10b981, #06b6d4)"
    elif percentage < 80:
        color = "linear-gradient(90deg, #f59e0b, #ef4444)"
    else:
        color = "linear-gradient(90deg, #ef4444, #dc2626)"

    st.markdown(f"""
    <div style="margin: 12px 0;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="font-weight:600; font-size:0.9rem;">{label}</span>
            <span style="color:#94a3b8; font-size:0.85rem;">{used} / {total}</span>
        </div>
        <div class="usage-bar">
            <div class="usage-bar-fill" style="width:{percentage}%; background:{color};"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_status_badge(status):
    """Render a colored status badge."""
    badge_class = {
        "Active": "badge-active",
        "New": "badge-active",
        "Contacted": "badge-warning",
        "Qualified": "badge-active",
        "Lost": "badge-danger",
        "Expired": "badge-danger",
    }.get(status, "badge-warning")

    return f'<span class="status-badge {badge_class}">{status}</span>'


def render_section_header(title, icon=""):
    """Render a styled section header."""
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)


def render_empty_state(message, icon="📭"):
    """Render an empty state message."""
    st.markdown(f"""
    <div class="glass-card" style="text-align:center; padding:40px;">
        <div style="font-size:3rem; margin-bottom:12px;">{icon}</div>
        <div style="color:#94a3b8; font-size:1rem;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


# ==============================
# DATA VALIDATION
# ==============================

def validate_username(username):
    """Validate username format."""
    if not username or len(username) < 3:
        return False, t("اسم المستخدم يجب أن يكون 3 أحرف على الأقل", "Username must be at least 3 characters")
    if len(username) > 30:
        return False, t("اسم المستخدم طويل جداً", "Username is too long")
    if not username.isalnum() and "_" not in username:
        return False, t("اسم المستخدم يجب يحتوي على حروف وأرقام فقط", "Username must be alphanumeric")
    return True, ""


def validate_password(password):
    """Validate password strength."""
    if not password or len(password) < 6:
        return False, t("كلمة المرور يجب أن تكون 6 أحرف على الأقل", "Password must be at least 6 characters")
    return True, ""


def validate_email(email):
    """Basic email validation."""
    if not email or "@" not in email or "." not in email:
        return False, t("بريد إلكتروني غير صالح", "Invalid email address")
    return True, ""
