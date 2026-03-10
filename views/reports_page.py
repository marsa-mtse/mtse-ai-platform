# ==========================================================
# MTSE Marketing Engine - Reports Page
# ==========================================================

import streamlit as st
import io
import numpy as np
from utils import t, render_section_header, render_empty_state, format_arabic
from database import (
    get_usage, get_user_reports, get_report_pdf,
    save_report, increment_reports, log_activity
)
from config import PLAN_LIMITS


def render():
    """Render the Reports page."""

    username = st.session_state.username
    plan = st.session_state.plan
    usage = get_usage(username)
    limits = PLAN_LIMITS.get(plan, PLAN_LIMITS["Explorer"])

    st.markdown(f"""
    <div class="glass-card animate-in" style="text-align:center;">
        <h2>📁 {t("التقارير", "Reports")}</h2>
        <p style="color:#94a3b8;">{t("إنشاء وإدارة تقارير PDF الاحترافية", "Generate & manage enterprise PDF reports")}</p>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state.get("analysis_df")
    strategy_output = st.session_state.get("strategy_output", "")
    uploaded_filename = st.session_state.get("uploaded_filename", "")

    # ==============================
    # GENERATE NEW REPORT
    # ==============================

    render_section_header(t("إنشاء تقرير جديد", "Generate New Report"), "📄")

    reports_used = usage["reports_used"]
    reports_limit = limits["reports"]

    if df is None:
        render_empty_state(
            t("ارفع بيانات من صفحة التحليلات أولاً لإنشاء تقرير", "Upload data from Analytics page first to generate a report"),
            "📤"
        )
    elif reports_used >= reports_limit:
        st.error(t(
            "تم الوصول لحد التقارير في خطتك. قم بالترقية.",
            "Report limit reached for your plan. Upgrade to continue."
        ))
    else:
        st.info(t(
            f"متبقي {reports_limit - reports_used} تقرير",
            f"{reports_limit - reports_used} reports remaining"
        ))

        report_language = st.selectbox(
            t("لغة التقرير", "Report Language"),
            ["Arabic + English", "Arabic Only", "English Only"]
        )

        if st.button(t("📄 إنشاء تقرير PDF احترافي", "📄 Generate Enterprise PDF"), use_container_width=True):
            with st.spinner(t("جاري إنشاء التقرير...", "Generating report...")):
                try:
                    pdf_buffer = generate_enterprise_pdf(
                        df=df,
                        strategy_text=strategy_output,
                        username=username,
                        filename=uploaded_filename,
                        report_language=report_language
                    )

                    # Save to archive
                    save_report(username, uploaded_filename, strategy_output, pdf_buffer.getvalue())
                    increment_reports(username)
                    log_activity(username, f"Generated PDF report for {uploaded_filename}")

                    st.success(t("تم إنشاء التقرير وحفظه في الأرشيف ✅", "Report Generated & Saved ✅"))

                    st.download_button(
                        t("⬇️ تحميل التقرير", "⬇️ Download Report"),
                        data=pdf_buffer,
                        file_name=f"MTSE_Report_{uploaded_filename}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(t(f"خطأ في إنشاء التقرير: {e}", f"Error generating report: {e}"))

    # ==============================
    # REPORT ARCHIVE
    # ==============================

    render_section_header(t("أرشيف التقارير", "Reports Archive"), "🗄️")

    reports = get_user_reports(username)

    if not reports:
        render_empty_state(
            t("لا توجد تقارير بعد", "No reports yet"),
            "📭"
        )
    else:
        for report in reports:
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.markdown(f"📄 **{report['file_name']}**")
            with col2:
                st.markdown(f"🕐 {report['created_at'][:16]}")
            with col3:
                pdf_data = get_report_pdf(report["id"])
                if pdf_data:
                    st.download_button(
                        t("⬇️ تحميل", "⬇️ Download"),
                        data=pdf_data,
                        file_name=f"{report['file_name']}_report.pdf",
                        mime="application/pdf",
                        key=f"download_{report['id']}"
                    )
            st.markdown("---")


def generate_enterprise_pdf(df=None, strategy_text="", username="User", filename="File", report_language="Arabic + English"):
    """Generate a full enterprise PDF report."""
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import inch
    except ImportError:
        raise ImportError("reportlab is required for PDF generation. Install with: pip install reportlab")

    # Try to register Arabic font
    arabic_font_available = False
    try:
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        pdfmetrics.registerFont(TTFont('Amiri', 'Amiri-Regular.ttf'))
        arabic_font_available = True
    except Exception:
        pass

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    # Arabic style
    if arabic_font_available:
        arabic_style = ParagraphStyle(
            'ArabicStyle',
            parent=styles['Normal'],
            fontName='Amiri',
            fontSize=12,
            leading=18,
            alignment=2
        )
    else:
        arabic_style = styles['Normal']

    english_style = styles['Normal']

    # ==============================
    # COVER PAGE
    # ==============================

    elements.append(Paragraph("MTSE Marketing Engine", styles["Heading1"]))
    elements.append(Spacer(1, 15))

    if report_language in ["English Only", "Arabic + English"]:
        elements.append(Paragraph("Enterprise Marketing Report", english_style))
        elements.append(Spacer(1, 10))

    if report_language in ["Arabic Only", "Arabic + English"]:
        ar_text = format_arabic("تقرير التسويق الاحترافي")
        elements.append(Paragraph(ar_text, arabic_style))
        elements.append(Spacer(1, 10))

    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"Client: {username}", english_style))
    elements.append(Paragraph(f"File: {filename}", english_style))
    elements.append(PageBreak())

    # ==============================
    # EXECUTIVE SUMMARY
    # ==============================

    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    elements.append(Spacer(1, 10))

    if report_language in ["English Only", "Arabic + English"]:
        elements.append(Paragraph(
            "This report analyzes performance data and provides marketing strategy recommendations.",
            english_style
        ))
        elements.append(Spacer(1, 10))

    if report_language in ["Arabic Only", "Arabic + English"]:
        ar_summary = format_arabic("يقوم هذا التقرير بتحليل البيانات وتقديم توصيات استراتيجية تسويقية.")
        elements.append(Paragraph(ar_summary, arabic_style))
        elements.append(Spacer(1, 10))

    elements.append(Spacer(1, 15))

    # ==============================
    # DATA METRICS TABLE
    # ==============================

    if df is not None:
        numeric_cols = df.select_dtypes(include=np.number).columns

        if len(numeric_cols) > 0:
            elements.append(Paragraph("Performance Metrics", styles["Heading2"]))
            elements.append(Spacer(1, 10))

            table_data = [["Metric", "Average", "Min", "Max"]]
            for col_name in numeric_cols:
                table_data.append([
                    col_name,
                    str(round(df[col_name].mean(), 2)),
                    str(round(df[col_name].min(), 2)),
                    str(round(df[col_name].max(), 2))
                ])

            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4f46e5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#f8fafc'), colors.white]),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
                ('TOPPADDING', (0, 0), (-1, 0), 10),
            ]))

            elements.append(table)
            elements.append(Spacer(1, 20))

    # ==============================
    # STRATEGY SECTION
    # ==============================

    if strategy_text:
        elements.append(Paragraph("Strategic Recommendations", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        for line in strategy_text.split("\n"):
            if line.strip():
                elements.append(Paragraph(line.strip(), english_style))
                elements.append(Spacer(1, 4))

        elements.append(Spacer(1, 20))

    # ==============================
    # BUILD WITH WATERMARK
    # ==============================

    def add_watermark(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 55)
        canvas.setFillGray(0.93)
        canvas.drawCentredString(A4[0] / 2, A4[1] / 2, "MTSE Marketing Engine")
        canvas.restoreState()

        canvas.setFont("Helvetica", 8)
        canvas.drawString(30, 20, "Generated by MTSE Marketing Engine")
        canvas.drawRightString(A4[0] - 30, 20, "Confidential")

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)

    buffer.seek(0)
    return buffer
