import html
import os
from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    Image,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

ROOT_DIR = Path(__file__).resolve().parents[2]

TEMPLATE_PAGE_SIZE = A4
TEMPLATE_MARGIN_LEFT = 40
TEMPLATE_MARGIN_RIGHT = 40
TEMPLATE_MARGIN_TOP = 50
TEMPLATE_MARGIN_BOTTOM = 55
BODY_WIDTH = TEMPLATE_PAGE_SIZE[0] - TEMPLATE_MARGIN_LEFT - TEMPLATE_MARGIN_RIGHT
BODY_HEIGHT = TEMPLATE_PAGE_SIZE[1] - TEMPLATE_MARGIN_TOP - TEMPLATE_MARGIN_BOTTOM


FONT_NAME = "STHeiti"
font_path = "/System/Library/Fonts/STHeiti Light.ttc"
if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/STHeiti Medium.ttc"
if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/Hiragino Sans GB.ttc"
if not os.path.exists(font_path):
    font_path = "/System/Library/Fonts/PingFang.ttc"

if os.path.exists(font_path):
    try:
        pdfmetrics.registerFont(TTFont(FONT_NAME, font_path))
    except Exception as exc:
        print(f"Warning: failed to register font {font_path}: {exc}")
        FONT_NAME = "Helvetica"
else:
    print("Warning: No suitable Chinese fonts found. Falling back to Helvetica.")
    FONT_NAME = "Helvetica"


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(page_count)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        self.saveState()
        width, _ = self._pagesize
        left = TEMPLATE_MARGIN_LEFT
        right = width - TEMPLATE_MARGIN_RIGHT

        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.6)
        self.line(left, 52, right, 52)

        self.setFont(FONT_NAME, 9)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(left, 24, "讯联科技（吉林省）有限公司 · 候选人简历报告")
        self.drawRightString(right, 24, f"第 {self._pageNumber} 页 / 共 {page_count} 页")
        self.restoreState()


def format_html_text(text):
    if not text:
        return ""
    escaped = html.escape(str(text))
    return escaped.replace("\n", "<br/>")


def val(field_val):
    if field_val is None:
        return "--"
    text = str(field_val).strip()
    return text if text else "--"


def make_hr():
    return HRFlowable(
        width=BODY_WIDTH,
        thickness=0.6,
        color=colors.HexColor("#dbe3ea"),
        spaceBefore=2,
        spaceAfter=8,
        hAlign="LEFT",
    )


def make_basic_info_banner(styles):
    left_style = ParagraphStyle(
        "BasicInfoCN",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#1e293b"),
        fontStyle="bold",
    )
    right_style = ParagraphStyle(
        "BasicInfoEN",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#6bb7cf"),
    )
    left = Paragraph("基本信息", left_style)
    right = Paragraph("Basic information", right_style)
    table = Table([[left, right]], colWidths=[130, BODY_WIDTH - 130])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                ("LINEBEFORE", (0, 0), (0, -1), 4, colors.HexColor("#2a66f2")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    return table


def make_heading(text, styles, variant="black"):
    if variant == "blue":
        style = ParagraphStyle(
            "SectionBlue",
            parent=styles["Normal"],
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#4fa1c0"),
            fontStyle="bold",
        )
    else:
        style = ParagraphStyle(
            "SectionBlack",
            parent=styles["Normal"],
            fontName=FONT_NAME,
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#1e293b"),
            fontStyle="bold",
        )
    return Paragraph(text, style)


def make_paragraph_style(name, parent, font_size=11, leading=17, color="#334155", bold=False, align=0):
    return ParagraphStyle(
        name,
        parent=parent,
        fontName=FONT_NAME,
        fontSize=font_size,
        leading=leading,
        textColor=colors.HexColor(color),
        alignment=align,
        fontStyle="bold" if bold else "normal",
        wordWrap="CJK",
    )


def build_header_table(styles, company_name, contract_no, project_no, headhunter_position):
    logo_img_path = os.path.join(ROOT_DIR, "backend", "app", "assets", "logo.png")
    if os.path.exists(logo_img_path):
        logo_flow = Image(logo_img_path, width=28, height=28)
    else:
        logo_flow = Spacer(28, 28)

    corp_title_style = ParagraphStyle(
        "CorpTitleStyle",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1f2937"),
        fontStyle="bold",
    )
    corp_table = Table(
        [[logo_flow, Paragraph("<b>讯联科技（吉林省）有限公司</b>", corp_title_style)]],
        colWidths=[28, 332],
    )
    corp_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )

    handwrite_cell_style = ParagraphStyle(
        "HandwriteCell",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
        alignment=1,
    )
    handwrite_data = [
        [Paragraph("合同编号", handwrite_cell_style), Paragraph(str(contract_no) if contract_no else "", handwrite_cell_style)],
        [Paragraph("项目编号", handwrite_cell_style), Paragraph(str(project_no) if project_no else "", handwrite_cell_style)],
        [Paragraph("猎头职位", handwrite_cell_style), Paragraph(str(headhunter_position) if headhunter_position else "", handwrite_cell_style)],
    ]
    handwrite_table = Table(handwrite_data, colWidths=[60, 90], rowHeights=[17, 17, 17])
    handwrite_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#475569")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )

    header_table = Table([[corp_table, handwrite_table]], colWidths=[360, 155])
    header_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return header_table


def build_recommendation_row(styles, position_name, exported_by):
    meta_style_left = make_paragraph_style("MetaLeft", styles["Normal"], font_size=9, leading=12, color="#64748b")
    meta_style_center = make_paragraph_style("MetaCenter", styles["Normal"], font_size=9, leading=12, color="#64748b", align=1)
    meta_style_right = make_paragraph_style("MetaRight", styles["Normal"], font_size=9, leading=12, color="#64748b", align=2)
    today_str = datetime.now().strftime("%Y-%m-%d")
    rec_table = Table(
        [[
            Paragraph(f"推荐职位：{position_name or '--'}", meta_style_left),
            Paragraph(f"推荐顾问：{exported_by or '顾问'}", meta_style_center),
            Paragraph(f"推荐日期：{today_str}", meta_style_right),
        ]],
        colWidths=[BODY_WIDTH / 3.0, BODY_WIDTH / 3.0, BODY_WIDTH / 3.0],
    )
    rec_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return rec_table


def build_basic_info_table(candidate, styles):
    label_style = make_paragraph_style("InfoLabel", styles["Normal"], font_size=10, leading=14, color="#334155", bold=True)
    value_style = make_paragraph_style("InfoValue", styles["Normal"], font_size=10, leading=14, color="#334155")

    grid_data = [
        [Paragraph("姓名", label_style), Paragraph(val(candidate.name), value_style), Paragraph("出生日期", label_style), Paragraph(val(candidate.birth_date), value_style)],
        [Paragraph("性别", label_style), Paragraph(val(candidate.gender), value_style), Paragraph("户口所在地", label_style), Paragraph(val(candidate.hukou_location), value_style)],
        [Paragraph("最高学历", label_style), Paragraph(val(candidate.education), value_style), Paragraph("期望薪资", label_style), Paragraph(val(candidate.expected_salary), value_style)],
        [Paragraph("到岗周期", label_style), Paragraph(val(candidate.onboard_cycle), value_style), Paragraph("家庭情况", label_style), Paragraph(val(candidate.family_status), value_style)],
    ]

    info_table = Table(grid_data, colWidths=[80, 177.5, 80, 177.5])
    info_table.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d6dee8")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#f8fafc")),
                ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#f8fafc")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    return info_table


def build_text_section(title, content, styles, variant="black"):
    body_style = make_paragraph_style("BodyTextStyle", styles["Normal"], font_size=10, leading=15, color="#334155")
    story = [make_heading(title, styles, variant=variant), make_hr()]
    content_str = str(content).strip() if content else ""
    if content_str:
        story.append(Paragraph(format_html_text(content_str), body_style))
        story.append(Spacer(1, 20))
    else:
        story.append(Spacer(1, 16))
    return story


def build_note_block(styles):
    note_style = make_paragraph_style("NoteStyle", styles["Normal"], font_size=8.5, leading=13.5, color="#64748b")
    note_html = (
        "<b>备注：</b><br/>"
        "1. 以上您所填写的内容将由我公司猎头负责严格保密。<br/>"
        "2. 将本表格填写完成后您即成为猎头的候选人，成为猎头的长期合作伙伴。<br/>"
        "3. 将免费为您推荐最适合您的岗位。<br/>"
        "4. 请保证您以上所填写的信息真实、可靠，如有虚假，您将从人才猎头候选人名单中被删除，同时被列入猎头黑名单。"
    )
    note_table = Table([[Paragraph(note_html, note_style)]], colWidths=[515])
    note_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#edf7fb")),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cfe0eb")),
                ("LINEBEFORE", (0, 0), (0, -1), 4, colors.HexColor("#38a3c7")),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                ("LEFTPADDING", (0, 0), (-1, -1), 12),
                ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ]
        )
    )
    return note_table


def generate_resume_pdf(
    candidate,
    company_name: str,
    project_name: str,
    position_name: str,
    exported_by: str,
    output_path: str,
    project_id: int | None = None,
    contract_no: str = "",
    project_no: str = "",
    headhunter_position: str = "",
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    styles = getSampleStyleSheet()
    doc = BaseDocTemplate(
        output_path,
        pagesize=TEMPLATE_PAGE_SIZE,
        leftMargin=TEMPLATE_MARGIN_LEFT,
        rightMargin=TEMPLATE_MARGIN_RIGHT,
        topMargin=TEMPLATE_MARGIN_TOP,
        bottomMargin=TEMPLATE_MARGIN_BOTTOM,
    )

    frame = Frame(
        TEMPLATE_MARGIN_LEFT,
        TEMPLATE_MARGIN_BOTTOM,
        BODY_WIDTH,
        BODY_HEIGHT,
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
        id="resume-body",
    )
    doc.addPageTemplates([PageTemplate(id="resume-template", frames=[frame])])

    story = []
    story.append(build_header_table(styles, company_name, contract_no, project_no, headhunter_position))
    main_title_style = ParagraphStyle(
        "MainTitleStyle",
        parent=styles["Normal"],
        fontName=FONT_NAME,
        fontSize=22,
        leading=28,
        textColor=colors.HexColor("#6bb7cf"),
        alignment=1,
        fontStyle="bold",
    )
    story.append(Spacer(1, 8))
    story.append(Paragraph("候选人简历报告", main_title_style))
    story.append(Spacer(1, 12))
    story.append(build_recommendation_row(styles, position_name, exported_by))
    story.append(Spacer(1, 10))
    story.append(make_basic_info_banner(styles))
    story.append(Spacer(1, 8))
    story.append(build_basic_info_table(candidate, styles))
    story.append(Spacer(1, 14))

    text_sections = [
        ("【教育背景】（倒序）", candidate.education_detail, "black"),
        ("【证    书】", candidate.certificates, "black"),
        ("综合评估：", candidate.comprehensive_evaluation, "blue"),
        ("【核 心 价 值】", candidate.core_value, "black"),
        ("【职位状态】", candidate.job_status, "black"),
        ("【薪资结构】", candidate.salary_structure, "black"),
        ("【求职意向】", candidate.job_intention, "black"),
        ("【职业经历】（倒序，每一次工作经历都要按照这个顺序来写）", candidate.work_history, "black"),
        ("【项 目 经 历】", candidate.project_history, "black"),
    ]

    for title, content, variant in text_sections:
        story.extend(build_text_section(title, content, styles, variant=variant))

    story.append(build_note_block(styles))

    doc.build(story, canvasmaker=NumberedCanvas)
