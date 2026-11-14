"""
report_generator.py
Generates personalized consultation reports in both high-end HTML (print/PDF ready)
and direct PDF format using ReportLab.
"""

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Unicode Font
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial.ttf"
BOLD_FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

try:
    if os.path.exists(FONT_PATH):
        pdfmetrics.registerFont(TTFont('Arial', FONT_PATH))
    if os.path.exists(BOLD_FONT_PATH):
        pdfmetrics.registerFont(TTFont('Arial-Bold', BOLD_FONT_PATH))
    else:
        pdfmetrics.registerFont(TTFont('Arial-Bold', FONT_PATH))
except Exception:
    pass

def generate_html_report(client_profile: dict, top_matches: list) -> str:
    """Generates an executive, print-ready HTML consultation report."""
    now_str = datetime.now().strftime("%d/%m/%Y")
    client_name = client_profile.get("client_name", "Quý Khách Hàng")
    budget = client_profile.get("budget_eur", 0)
    income = client_profile.get("monthly_income_eur", 0)
    stay_mode = client_profile.get("physical_stay_capability", "full_residency")
    stay_text = {
        "minimal": "Tối thiểu (0 - 14 ngày/năm - Giữ thẻ)",
        "flexible": "Linh hoạt (1 - 3 tháng/năm)",
        "full_residency": "Định cư thường trực (>183 ngày/năm)"
    }.get(stay_mode, stay_mode)

    goal_text = {
        "citizenship_passport": "Nhập Quốc Tịch / Hộ Chiếu EU nhanh nhất",
        "pr_permanent_residency": "Lấy Thường Trú Nhân (PR) an toàn, dài hạn",
        "schengen_mobility": "Tự do đi lại 29 nước Schengen cho cả gia đình",
        "education_kids": "Giáo dục con cái miễn phí trường công",
        "expand_business": "Mở rộng kinh doanh sang thị trường EU"
    }.get(client_profile.get("primary_goal", ""), "Định cư Châu Âu")

    top3 = top_matches[:3]

    cards_html = ""
    for idx, match in enumerate(top3, 1):
        p = match["program_details"]
        pros_li = "".join([f"<li>✅ {item}</li>" for item in match["pros"]])
        caveats_li = "".join([f"<li>⚠️ {item}</li>" for item in match["caveats"]])
        score_class = "gold-badge" if match["match_score"] >= 90 else "blue-badge"

        cards_html += f"""
        <div class="program-card">
            <div class="card-header">
                <div>
                    <span class="rank-tag">LỰA CHỌN #{idx}</span>
                    <h3 class="program-title">{match['country_vi']} ({match['country_en']}) - {match['program_name']}</h3>
                    <div class="archetype-label">{match['archetype_name']}</div>
                </div>
                <div class="{score_class}">
                    <div class="score-val">{match['match_score']}%</div>
                    <div class="score-sub">Điểm Tương Thích</div>
                </div>
            </div>
            
            <div class="metrics-grid">
                <div class="metric-box">
                    <span class="metric-label">Yêu Cầu Tài Chính</span>
                    <span class="metric-val">{p['financial_requirement_text']}</span>
                </div>
                <div class="metric-box">
                    <span class="metric-label">Yêu Cầu Cư Trú</span>
                    <span class="metric-val">Tối thiểu {p['min_physical_stay_days_per_year']} ngày/năm</span>
                </div>
                <div class="metric-box">
                    <span class="metric-label">Lộ Trình PR</span>
                    <span class="metric-val">{p['timeline_pr']}</span>
                </div>
                <div class="metric-box">
                    <span class="metric-label">Lộ Trình Quốc Tịch</span>
                    <span class="metric-val">{p['timeline_citizenship']}</span>
                </div>
            </div>

            <div class="analysis-grid">
                <div class="analysis-col pros-col">
                    <h4>Ưu Điểm Nổi Bật Với Hồ Sơ Của Bạn:</h4>
                    <ul>{pros_li}</ul>
                </div>
                <div class="analysis-col caveats-col">
                    <h4>Lưu Ý Quan Trọng:</h4>
                    <ul>{caveats_li}</ul>
                </div>
            </div>
        </div>
        """

    # Checklist for #1 program
    best_p = top3[0]["program_details"]
    chk = best_p["checklist"]

    def render_chk_items(items):
        res = ""
        for i in items:
            res += f"""
            <div class="checklist-item">
                <div class="chk-box">☐</div>
                <div class="chk-text">
                    <strong>{i['item']}</strong>
                    <p>{i['detail']}</p>
                </div>
            </div>
            """
        return res

    html = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<title>Báo Cáo Đánh Giá & Định Hướng Định Cư Châu Âu - {client_name}</title>
<style>
    @page {{
        size: A4;
        margin: 15mm;
    }}
    body {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
        color: #1e293b;
        background: #f8fafc;
        margin: 0;
        padding: 24px;
        line-height: 1.5;
    }}
    .container {{
        max-width: 900px;
        margin: 0 auto;
        background: #ffffff;
        padding: 36px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
    }}
    .report-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #0f172a;
        padding-bottom: 20px;
        margin-bottom: 24px;
    }}
    .brand-title {{
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        margin: 0;
        letter-spacing: -0.5px;
    }}
    .brand-sub {{
        font-size: 13px;
        color: #64748b;
        margin-top: 4px;
    }}
    .date-badge {{
        background: #f1f5f9;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 13px;
        font-weight: 600;
        color: #334155;
    }}
    .section-title {{
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        border-left: 4px solid #2563eb;
        padding-left: 12px;
        margin: 28px 0 16px 0;
    }}
    .profile-box {{
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 20px;
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 12px 24px;
    }}
    .profile-item {{
        display: flex;
        flex-direction: column;
    }}
    .profile-label {{
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        font-weight: 600;
    }}
    .profile-val {{
        font-size: 15px;
        font-weight: 600;
        color: #0f172a;
        margin-top: 2px;
    }}
    .program-card {{
        border: 1px solid #cbd5e1;
        border-radius: 10px;
        padding: 24px;
        margin-bottom: 24px;
        background: #ffffff;
    }}
    .card-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        border-bottom: 1px solid #f1f5f9;
        padding-bottom: 14px;
        margin-bottom: 16px;
    }}
    .rank-tag {{
        display: inline-block;
        background: #dbeafe;
        color: #1e40af;
        font-size: 11px;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 4px;
        margin-bottom: 6px;
    }}
    .program-title {{
        margin: 0;
        font-size: 19px;
        color: #0f172a;
    }}
    .archetype-label {{
        font-size: 13px;
        color: #64748b;
        margin-top: 4px;
    }}
    .gold-badge {{
        background: #fef3c7;
        color: #92400e;
        border: 1px solid #fde68a;
        padding: 10px 16px;
        border-radius: 10px;
        text-align: center;
    }}
    .blue-badge {{
        background: #e0f2fe;
        color: #0369a1;
        border: 1px solid #bae6fd;
        padding: 10px 16px;
        border-radius: 10px;
        text-align: center;
    }}
    .score-val {{
        font-size: 26px;
        font-weight: 800;
        line-height: 1;
    }}
    .score-sub {{
        font-size: 10px;
        text-transform: uppercase;
        margin-top: 4px;
        font-weight: 600;
    }}
    .metrics-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 16px;
    }}
    .metric-box {{
        background: #f8fafc;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #e2e8f0;
    }}
    .metric-label {{
        display: block;
        font-size: 11px;
        color: #64748b;
    }}
    .metric-val {{
        display: block;
        font-size: 13px;
        font-weight: 700;
        color: #0f172a;
        margin-top: 2px;
    }}
    .analysis-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
    }}
    .analysis-col h4 {{
        margin: 0 0 8px 0;
        font-size: 13px;
    }}
    .pros-col h4 {{ color: #166534; }}
    .caveats-col h4 {{ color: #991b1b; }}
    .analysis-col ul {{
        margin: 0;
        padding-left: 18px;
        font-size: 12.5px;
        color: #334155;
    }}
    .analysis-col li {{
        margin-bottom: 6px;
    }}
    .checklist-section {{
        background: #fcfcfd;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 24px;
        margin-top: 24px;
    }}
    .chk-tier-title {{
        font-size: 15px;
        font-weight: 700;
        color: #1e3a8a;
        margin: 18px 0 10px 0;
        padding-bottom: 4px;
        border-bottom: 1px solid #e2e8f0;
    }}
    .checklist-item {{
        display: flex;
        align-items: flex-start;
        margin-bottom: 12px;
        font-size: 13px;
    }}
    .chk-box {{
        font-size: 16px;
        margin-right: 10px;
        color: #64748b;
    }}
    .chk-text strong {{
        color: #0f172a;
    }}
    .chk-text p {{
        margin: 2px 0 0 0;
        color: #475569;
        font-size: 12px;
    }}
    .footer-note {{
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #e2e8f0;
        text-align: center;
        font-size: 12px;
        color: #64748b;
    }}
    .btn-print {{
        background: #2563eb;
        color: #ffffff;
        padding: 10px 20px;
        font-size: 14px;
        font-weight: 600;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        display: inline-block;
        margin-bottom: 20px;
    }}
    @media print {{
        body {{
            background: #ffffff;
            padding: 0;
        }}
        .container {{
            box-shadow: none;
            padding: 0;
            max-width: 100%;
        }}
        .btn-print {{
            display: none;
        }}
        .program-card {{
            page-break-inside: avoid;
        }}
        .checklist-section {{
            page-break-before: always;
        }}
    }}
</style>
</head>
<body>
<div class="container">
    <button class="btn-print" onclick="window.print()">🖨️ In Báo Cáo / Lưu PDF</button>

    <div class="report-header">
        <div>
            <h1 class="brand-title">BÁO CÁO ĐÁNH GIÁ ĐỊNH CƯ CHÂU ÂU 2026</h1>
            <div class="brand-sub">EU & Schengen Immigration Profile Matching & Document Dossier</div>
        </div>
        <div class="date-badge">Ngày xuất: {now_str}</div>
    </div>

    <div class="section-title">THÔNG TIN HỒ SƠ KHÁCH HÀNG</div>
    <div class="profile-box">
        <div class="profile-item">
            <span class="profile-label">Khách Hàng / Đương Đơn</span>
            <span class="profile-val">{client_name}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Mục Tiêu Di Trú</span>
            <span class="profile-val">{goal_text}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Ngân Sách Khả Dụng</span>
            <span class="profile-val">€{budget:,.0f}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Thu Nhập Hàng Tháng</span>
            <span class="profile-val">€{income:,.0f} / tháng</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Khả Năng Cư Trú Thực Tế</span>
            <span class="profile-val">{stay_text}</span>
        </div>
        <div class="profile-item">
            <span class="profile-label">Trình Độ Học Vấn</span>
            <span class="profile-val">{client_profile.get('education_level', 'Đại học').upper()}</span>
        </div>
    </div>

    <div class="section-title">TOP 3 CHƯƠNG TRÌNH PHÙ HỢP NHẤT</div>
    {cards_html}

    <div class="checklist-section">
        <div class="section-title" style="margin-top:0">BỘ CHECKLIST HỒ SƠ CHI TIẾT (LỰA CHỌN TỐI ƯU #{1})</div>
        <p style="font-size:13px; color:#64748b; margin-top:-8px; margin-bottom:16px;">
            Áp dụng cho: <strong>{best_p['country_vi']} - {best_p['program_name']}</strong> ({best_p['archetype_name']})
        </p>

        <div class="chk-tier-title">1. NHÂN THÂN & HỘ TỊCH (CIVIL & IDENTITY)</div>
        {render_chk_items(chk['tier1_civil_identity'])}

        <div class="chk-tier-title">2. NĂNG LỰC TÀI CHÍNH & NGUỒN TIỀN (FINANCIAL & PROOF OF FUNDS)</div>
        {render_chk_items(chk['tier2_financial_funds'])}

        <div class="chk-tier-title">3. HỒ SƠ NGHIỆP VỤ CHUYÊN BIỆT THEO DIỆN (SPECIALIZED PROGRAM DOCUMENTS)</div>
        {render_chk_items(chk['tier3_specialized_investment'])}

        <div class="chk-tier-title">4. CHỖ Ở & BẢO HIỂM Y TẾ QUỐC TẾ (ACCOMMODATION & HEALTH)</div>
        {render_chk_items(chk['tier4_accommodation_health'])}

        <div class="chk-tier-title">5. QUY CHUẨN NỘP & HỢP PHÁP HÓA LÃNH SỰ (LEGALIZATION & SUBMISSION)</div>
        {render_chk_items(chk['tier5_legalization_submission'])}
    </div>

    <div class="footer-note">
        Báo cáo phân tích dựa trên dữ liệu Luật Di Trú Châu Âu cập nhật 2025-2026. Để hoàn tất thủ tục và kiểm tra tính hợp lệ cụ thể của chứng từ, vui lòng liên hệ chuyên viên tư vấn di trú để được hỗ trợ chuyên sâu.
    </div>
</div>
</body>
</html>
    """
    return html


def generate_pdf_report(client_profile: dict, top_matches: list, output_filepath: str) -> str:
    """Generates an executive PDF report using ReportLab with Arial font."""
    doc = SimpleDocTemplate(
        output_filepath,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    font_name = 'Arial' if 'Arial' in pdfmetrics.getRegisteredFontNames() else 'Helvetica'
    bold_font = 'Arial-Bold' if 'Arial-Bold' in pdfmetrics.getRegisteredFontNames() else font_name

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName=bold_font,
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#64748b'),
        spaceAfter=15
    )
    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading2'],
        fontName=bold_font,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1e40af'),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#1e293b')
    )
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#334155'),
        leftIndent=12,
        spaceAfter=3
    )

    story = []

    # Title
    story.append(Paragraph("BÁO CÁO ĐÁNH GIÁ ĐỊNH CƯ CHÂU ÂU 2026", title_style))
    story.append(Paragraph(f"EU & Schengen Immigration Profile Matching — Ngày xuất: {datetime.now().strftime('%d/%m/%Y')}", subtitle_style))

    # Client summary table
    client_name = client_profile.get("client_name", "Quý Khách Hàng")
    budget = client_profile.get("budget_eur", 0)
    income = client_profile.get("monthly_income_eur", 0)

    summary_data = [
        [
            Paragraph(f"<b>Đương đơn:</b> {client_name}", body_style),
            Paragraph(f"<b>Ngân sách:</b> €{budget:,.0f}", body_style)
        ],
        [
            Paragraph(f"<b>Mục tiêu:</b> {client_profile.get('primary_goal', 'Định cư EU')}", body_style),
            Paragraph(f"<b>Thu nhập:</b> €{income:,.0f}/tháng", body_style)
        ],
        [
            Paragraph(f"<b>Khả năng cư trú:</b> {client_profile.get('physical_stay_capability', 'Thường trực')}", body_style),
            Paragraph(f"<b>Trình độ:</b> {client_profile.get('education_level', 'Đại học').upper()}", body_style)
        ]
    ]
    t = Table(summary_data, colWidths=[260, 260])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # Top 3 Programs
    story.append(Paragraph("TOP CHƯƠNG TRÌNH PHÙ HỢP NHẤT", h2_style))

    for idx, match in enumerate(top_matches[:3], 1):
        p = match["program_details"]
        card_content = [
            Paragraph(f"<b>#{idx}. {match['country_vi']} ({match['country_en']}) — {match['program_name']}</b> (Độ tương thích: <b>{match['match_score']}%</b>)", body_style),
            Paragraph(f"<i>Phân loại:</i> {match['archetype_name']} | <i>Chi phí:</i> {p['financial_requirement_text']}", bullet_style),
            Paragraph(f"<i>Thời gian xử lý:</i> {p['processing_time']} | <i>Lộ trình PR:</i> {p['timeline_pr']} | <i>Quốc tịch:</i> {p['timeline_citizenship']}", bullet_style)
        ]
        for pro in match["pros"][:2]:
            card_content.append(Paragraph(f"• [Ưu điểm] {pro}", bullet_style))
        for con in match["caveats"][:2]:
            card_content.append(Paragraph(f"• [Lưu ý] {con}", bullet_style))

        box = Table([[card_content]], colWidths=[520])
        box.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#ffffff')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#94a3b8')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        story.append(box)
        story.append(Spacer(1, 6))

    # Checklist for best match
    best_p = top_matches[0]["program_details"]
    chk = best_p["checklist"]

    story.append(PageBreak())
    story.append(Paragraph(f"BỘ CHECKLIST HỒ SƠ: {best_p['country_vi']} — {best_p['program_name']}", h2_style))

    tiers = [
        ("1. Nhân Thân & Hộ Tịch", chk["tier1_civil_identity"]),
        ("2. Tài Chính & Nguồn Tiền", chk["tier2_financial_funds"]),
        ("3. Nghiệp Vụ Chuyên Biệt", chk["tier3_specialized_investment"]),
        ("4. Chỗ Ở & Bảo Hiểm Y Tế", chk["tier4_accommodation_health"]),
        ("5. Quy Chuẩn Nộp & Hợp Pháp Hóa", chk["tier5_legalization_submission"])
    ]

    for t_name, t_items in tiers:
        story.append(Paragraph(f"<b>{t_name}</b>", ParagraphStyle('SubT', parent=body_style, fontName=bold_font, spaceBefore=6, spaceAfter=3)))
        for it in t_items:
            story.append(Paragraph(f"☐ <b>{it['item']}</b>: {it['detail']}", bullet_style))

    doc.build(story)
    return output_filepath
