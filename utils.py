# ==========================================================
# MTSE Marketing Engine - Utility Functions
# ==========================================================

import streamlit as st

try:
    import arabic_reshaper
    from bidi.algorithm import get_display
    from fpdf import FPDF
    import base64
    ARABIC_SUPPORT = True
except ImportError:
    ARABIC_SUPPORT = False


# ==============================
# TRANSLATION HELPER
# ==============================

def t(ar, en):
    """Return Arabic or English text based on language setting."""
    return ar if st.session_state.get("lang") == "AR" else en


# ==============================
# ARABIC TEXT FORMATTING
# ==============================

def format_arabic(text):
    """Reshape Arabic text for PDF rendering."""
    if not ARABIC_SUPPORT:
        return text
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except Exception:
        return text


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


# ==============================
# PROFESSIONAL PDF REPORTING
# ==============================

class BrandedPDF(FPDF):
    def header(self):
        # Add Logo from the assets folder
        try:
            self.image('assets/logo_premium.png', 10, 8, 30)
        except Exception:
            self.set_font('Arial', 'B', 15)
            self.cell(80)
            self.cell(30, 10, 'MTSE AI Platform', 0, 0, 'L')
        
        self.ln(20)
        # Deep blue line
        self.set_draw_color(26, 115, 232)
        self.line(10, 32, 200, 32)
        self.ln(10)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(150)
        # Footer text
        self.cell(0, 10, f'Page {self.page_no()} | MTSE Digital Marketing Engine | info@mtse.com', 0, 0, 'C')

def generate_branded_pdf(report_data, lang="Both"):
    """
    Generates a professional PDF with branding and Arabic support.
    """
    pdf = BrandedPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font('Arial', 'B', 18)
    pdf.set_text_color(26, 115, 232) # Brand Blue
    title = format_arabic(report_data.get("title", "Strategic Report"))
    pdf.cell(0, 12, title, 0, 1, 'C')
    pdf.ln(8)

    # Content
    for section in report_data.get("sections", []):
        # Section Heading
        pdf.set_font('Arial', 'B', 13)
        pdf.set_text_color(33, 33, 33)
        heading = format_arabic(section.get("heading", ""))
        pdf.cell(0, 10, heading, 0, 1, 'L')
        
        # Section Content
        pdf.set_font('Arial', '', 11)
        pdf.set_text_color(66, 66, 66)
        content = format_arabic(section.get("content", ""))
        pdf.multi_cell(0, 8, content)
        pdf.ln(4)

    # Output as bytes for st.download_button
    return pdf.output()
