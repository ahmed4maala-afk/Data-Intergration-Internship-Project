"""
PRYZM Solutions — Professional PDF Report Generator
Author: Ahmed Maala
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate, Frame
import json, os

# ─────────────────────────────────────────
# Config
# ─────────────────────────────────────────
OUTPUT_DIR = "/home/ubuntu/pryzm-internship/outputs"
PDF_PATH   = f"{OUTPUT_DIR}/PRYZM_DataQuality_AhmedMaala.pdf"

with open(f"{OUTPUT_DIR}/stats.json") as f:
    S = json.load(f)

# Brand colours
PRYZM_BLUE  = colors.HexColor('#1A3C5E')
PRYZM_TEAL  = colors.HexColor('#2E9E8F')
PRYZM_AMBER = colors.HexColor('#F5A623')
PRYZM_RED   = colors.HexColor('#E74C3C')
PRYZM_LIGHT = colors.HexColor('#F0F4F8')
PRYZM_GREY  = colors.HexColor('#7F8C8D')
WHITE       = colors.white
BLACK       = colors.HexColor('#1C1C1C')

# ─────────────────────────────────────────
# Custom Page Template with header/footer
# ─────────────────────────────────────────
class PRYZMDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            self.leftMargin, self.bottomMargin,
            self.width, self.height,
            id='main'
        )
        template = PageTemplate(id='main', frames=[frame],
                                onPage=self._draw_page)
        self.addPageTemplates([template])

    def _draw_page(self, c, doc):
        W, H = A4
        # ── Top bar ──
        c.setFillColor(PRYZM_BLUE)
        c.rect(0, H - 1.4*cm, W, 1.4*cm, fill=1, stroke=0)
        c.setFillColor(PRYZM_TEAL)
        c.rect(0, H - 1.55*cm, W, 0.15*cm, fill=1, stroke=0)

        # Header text
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 9)
        c.drawString(1.5*cm, H - 1.0*cm, 'PRYZM SOLUTIONS')
        c.setFont('Helvetica', 8)
        c.drawRightString(W - 1.5*cm, H - 1.0*cm,
                          'Data Integration Internship — Ahmed Maala')

        # ── Bottom bar ──
        c.setFillColor(PRYZM_BLUE)
        c.rect(0, 0, W, 0.9*cm, fill=1, stroke=0)
        c.setFillColor(PRYZM_TEAL)
        c.rect(0, 0.9*cm, W, 0.1*cm, fill=1, stroke=0)

        c.setFillColor(WHITE)
        c.setFont('Helvetica', 7.5)
        c.drawString(1.5*cm, 0.3*cm,
                     'Confidential — Prepared for PRYZM Solutions GmbH, Germany')
        c.drawRightString(W - 1.5*cm, 0.3*cm, f'Page {doc.page}')


# ─────────────────────────────────────────
# Styles
# ─────────────────────────────────────────
base_styles = getSampleStyleSheet()

def S_title():
    return ParagraphStyle('title',
        fontName='Helvetica-Bold', fontSize=22, textColor=PRYZM_BLUE,
        spaceAfter=4, leading=28)

def S_subtitle():
    return ParagraphStyle('subtitle',
        fontName='Helvetica', fontSize=11, textColor=PRYZM_GREY,
        spaceAfter=2)

def S_h1():
    return ParagraphStyle('h1',
        fontName='Helvetica-Bold', fontSize=13, textColor=PRYZM_BLUE,
        spaceBefore=14, spaceAfter=6, leading=18,
        borderPad=4)

def S_h2():
    return ParagraphStyle('h2',
        fontName='Helvetica-Bold', fontSize=10.5, textColor=PRYZM_TEAL,
        spaceBefore=10, spaceAfter=4)

def S_body():
    return ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, textColor=BLACK,
        leading=15, spaceAfter=6, alignment=TA_JUSTIFY)

def S_caption():
    return ParagraphStyle('caption',
        fontName='Helvetica-Oblique', fontSize=8, textColor=PRYZM_GREY,
        alignment=TA_CENTER, spaceAfter=8)

def S_bullet():
    return ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9.5, textColor=BLACK,
        leading=15, spaceAfter=3, leftIndent=14,
        bulletIndent=4)

def S_code():
    return ParagraphStyle('code',
        fontName='Courier', fontSize=8.5, textColor=PRYZM_BLUE,
        backColor=PRYZM_LIGHT, leading=13, spaceAfter=4,
        leftIndent=8, rightIndent=8, borderPad=6)

def S_highlight():
    return ParagraphStyle('highlight',
        fontName='Helvetica-Bold', fontSize=9.5, textColor=WHITE,
        backColor=PRYZM_TEAL, leading=15, spaceAfter=0,
        leftIndent=8, rightIndent=8, borderPad=6, alignment=TA_LEFT)

# ─────────────────────────────────────────
# Helper: KPI Card Row
# ─────────────────────────────────────────
def kpi_table(items):
    """items: list of (label, value, color) tuples"""
    cell_data = []
    for label, value, color in items:
        cell_data.append(
            Table(
                [[Paragraph(f'<font size=18><b>{value}</b></font>',
                            ParagraphStyle('kv', fontName='Helvetica-Bold',
                                           fontSize=18, textColor=WHITE,
                                           alignment=TA_CENTER))],
                 [Paragraph(f'<font size=8>{label}</font>',
                            ParagraphStyle('kl', fontName='Helvetica',
                                           fontSize=8, textColor=WHITE,
                                           alignment=TA_CENTER))]],
                colWidths=[3.8*cm],
                rowHeights=[1.1*cm, 0.6*cm],
                style=TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), color),
                    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                    ('ROUNDEDCORNERS', [6]),
                    ('LEFTPADDING', (0,0), (-1,-1), 4),
                    ('RIGHTPADDING', (0,0), (-1,-1), 4),
                ])
            )
        )
    return Table([cell_data],
                 colWidths=[4.0*cm]*len(items),
                 style=TableStyle([
                     ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                     ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                     ('LEFTPADDING', (0,0), (-1,-1), 3),
                     ('RIGHTPADDING', (0,0), (-1,-1), 3),
                 ]))

# ─────────────────────────────────────────
# Build Story
# ─────────────────────────────────────────
story = []

# ── Cover Section ──────────────────────────
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph('Data Quality Assessment', S_title()))
story.append(Paragraph('&amp; Intake Specification Proposal', S_title()))
story.append(Spacer(1, 0.3*cm))
story.append(HRFlowable(width='100%', thickness=2, color=PRYZM_TEAL,
                         spaceAfter=8))
story.append(Paragraph(
    'UCI Online Retail II Dataset — 1,067,371 Transactions | 2009–2011',
    S_subtitle()))
story.append(Paragraph(
    'Prepared by <b>Ahmed Maala</b> &nbsp;|&nbsp; '
    'Application: Data Integration Intern &nbsp;|&nbsp; '
    'PRYZM Solutions GmbH, Germany',
    S_subtitle()))
story.append(Spacer(1, 0.6*cm))

# KPI cards
kpis = [
    ('Total Records',   f'{S["total_rows"]/1e6:.2f}M', PRYZM_BLUE),
    ('Missing Cust. ID', f'{S["missing_customer_id_pct"]:.1f}%', PRYZM_RED),
    ('Duplicates',      f'{S["dup_pct"]:.1f}%',        PRYZM_AMBER),
    ('Cancellations',   f'{S["cancel_pct"]:.1f}%',     PRYZM_TEAL),
]
story.append(kpi_table(kpis))
story.append(Spacer(1, 0.5*cm))

# ── Section 1 ──────────────────────────────
story.append(HRFlowable(width='100%', thickness=1, color=PRYZM_LIGHT,
                         spaceAfter=4))
story.append(Paragraph('1. Data Quality Assessment', S_h1()))
story.append(Paragraph(
    'The UCI Online Retail II dataset contains <b>1,067,371 transaction records</b> '
    'spanning two years of wholesale activity (December 2009 – December 2011). '
    'This assessment mirrors the type of raw data PRYZM Solutions receives from '
    'industrial and pharmaceutical clients. Six distinct quality dimensions were '
    'evaluated, revealing issues that range from critical data gaps to minor '
    'formatting inconsistencies.',
    S_body()))

# Fig 1
img1 = Image(f"{OUTPUT_DIR}/fig1_quality_overview.png",
             width=15*cm, height=8.5*cm)
story.append(img1)
story.append(Paragraph(
    'Figure 1 — Data quality issues ranked by severity. '
    'Red = Critical (>10%), Amber = Warning (2–10%), Teal = Minor (<2%).',
    S_caption()))

# 1.1
story.append(Paragraph('1.1  Completeness — Missing Values', S_h2()))
story.append(Paragraph(
    'The most critical finding is that <b>22.77% of all records lack a Customer ID</b> '
    f'({S["missing_customer_id_count"]:,} rows). This completely prevents any '
    'customer-level analysis, including cohort tracking, lifetime value calculation, '
    'or churn prediction. A secondary gap exists in the Description field '
    f'({S["missing_description_pct"]:.2f}%, {S["missing_description_count"]:,} rows), '
    'which affects product categorisation pipelines.',
    S_body()))

# Fig 4 (missing heatmap)
img4 = Image(f"{OUTPUT_DIR}/fig4_missing_heatmap.png",
             width=15*cm, height=5*cm)
story.append(img4)
story.append(Paragraph(
    'Figure 2 — Missing value pattern across all columns in a random sample of 5,000 records. '
    'The dense red band on Customer_ID confirms the systemic nature of this gap.',
    S_caption()))

# 1.2
story.append(Paragraph('1.2  Accuracy — Anomalous Values', S_h2()))

anomaly_data = [
    ['Issue', 'Count', '% of Total', 'Severity'],
    ['Negative Quantities', f'{S["neg_qty"]:,}', '2.15%', 'Warning'],
    ['Zero-Price Entries', f'{S["zero_price"]:,}', '0.58%', 'Minor'],
    ['Non-standard Stock Codes', f'{S["non_std_codes"]:,}', f'{S["non_std_pct"]:.2f}%', 'Minor'],
    ['Negative Prices', f'{S["neg_price"]:,}', '<0.01%', 'Minor'],
]
anomaly_table = Table(anomaly_data,
                      colWidths=[5.5*cm, 2.5*cm, 2.5*cm, 2.5*cm])
anomaly_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRYZM_BLUE),
    ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
    ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',   (0,0), (-1,-1), 9),
    ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [PRYZM_LIGHT, WHITE]),
    ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#D5DDE5')),
    ('LEFTPADDING', (0,0), (-1,-1), 8),
    ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('TEXTCOLOR', (3,1), (3,1), PRYZM_AMBER),
    ('TEXTCOLOR', (3,2), (3,-1), PRYZM_TEAL),
    ('FONTNAME', (3,1), (3,-1), 'Helvetica-Bold'),
]))
story.append(anomaly_table)
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    'Negative quantities (22,950 records) are the most impactful accuracy issue. '
    'While some correspond to legitimate return transactions, others appear to be '
    'data entry errors unrelated to any cancellation invoice. Non-standard stock codes '
    'such as "POST", "DOT", and "BANK CHARGES" represent operational charges rather '
    'than physical products and must be excluded from inventory analytics.',
    S_body()))

# 1.3
story.append(Paragraph('1.3  Consistency — Duplicates & Cancellations', S_h2()))
story.append(Paragraph(
    f'Exact duplicate rows account for <b>{S["dup_pct"]:.2f}% ({S["dup_count"]:,} records)</b>. '
    'These are likely caused by repeated API calls or batch re-submissions and will '
    'inflate revenue figures if not removed at the staging layer. '
    f'Cancellation records ({S["cancel_pct"]:.2f}%, {S["cancel_count"]:,} rows, '
    'identified by an invoice prefix of "C") are currently mixed with standard sales, '
    'making it impossible to compute accurate net revenue without additional filtering.',
    S_body()))

# 1.4 — Temporal & Geographic
story.append(Paragraph('1.4  Temporal & Geographic Distribution', S_h2()))
story.append(Paragraph(
    'Transaction volume shows a clear <b>seasonal peak in Q4</b> each year, '
    'consistent with retail demand patterns. The dataset is heavily skewed toward '
    'the United Kingdom (92% of all records), with Germany, France, and Ireland '
    'representing the next largest markets — directly relevant to PRYZM\'s '
    'European client base.',
    S_body()))

img2 = Image(f"{OUTPUT_DIR}/fig2_monthly_volume.png",
             width=15*cm, height=5.5*cm)
story.append(img2)
story.append(Paragraph(
    'Figure 3 — Monthly transaction volume. Q4 spikes are consistent across both years.',
    S_caption()))

img3 = Image(f"{OUTPUT_DIR}/fig3_top_countries.png",
             width=15*cm, height=6*cm)
story.append(img3)
story.append(Paragraph(
    'Figure 4 — Top 10 countries by transaction volume. '
    'UK dominates at 92%; Germany ranks third.',
    S_caption()))

# ── Section 2 ──────────────────────────────
story.append(PageBreak())
story.append(HRFlowable(width='100%', thickness=1, color=PRYZM_LIGHT,
                         spaceAfter=4))
story.append(Paragraph('2. Proposed Intake Specification', S_h1()))
story.append(Paragraph(
    'To prevent the identified issues at the source and ensure clean, '
    'analysis-ready data from day one, I propose the following intake '
    'specification for client data submissions. This specification is designed '
    'to be lightweight enough for clients to implement quickly, while providing '
    'PRYZM\'s pipeline with reliable, validated inputs.',
    S_body()))

# 2.1 Required Fields
story.append(Paragraph('2.1  Required Fields & Accepted Formats', S_h2()))

fields_data = [
    ['Field Name', 'Type', 'Requirement', 'Validation Rule'],
    ['InvoiceNo',    'String (20)',  'Mandatory', 'No spaces; prefix "C" reserved for returns'],
    ['StockCode',    'String (15)',  'Mandatory', 'Pattern: ^\\d{5}[A-Z]?$'],
    ['Description',  'String (255)', 'Optional',  'Free text; UTF-8 encoded'],
    ['Quantity',     'Integer',      'Mandatory', 'Must be ≠ 0; negative = return'],
    ['InvoiceDate',  'Datetime',     'Mandatory', 'ISO 8601: YYYY-MM-DD HH:MM:SS'],
    ['UnitPrice',    'Decimal(10,2)','Mandatory', 'Must be ≥ 0'],
    ['CustomerID',   'String (20)',  'Mandatory', 'Non-null; unique per customer'],
    ['Country',      'String',       'Optional',  'ISO 3166-1 alpha-2 preferred'],
]
fields_table = Table(fields_data,
                     colWidths=[3.0*cm, 2.5*cm, 2.2*cm, 6.3*cm])
fields_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRYZM_BLUE),
    ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
    ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',   (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [PRYZM_LIGHT, WHITE]),
    ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#D5DDE5')),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ('FONTNAME',   (2,1), (2,-1), 'Helvetica-Bold'),
    ('TEXTCOLOR',  (2,1), (2,4), PRYZM_RED),
    ('TEXTCOLOR',  (2,5), (2,-1), PRYZM_TEAL),
]))
story.append(fields_table)
story.append(Spacer(1, 0.3*cm))

# 2.2 Automated Checks
story.append(Paragraph('2.2  Automated Pre-Ingestion Validation Checks', S_h2()))
story.append(Paragraph(
    'The following checks should be executed automatically at the staging layer '
    'before any record reaches the data warehouse. Each check produces a structured '
    'quality report that is logged and, where thresholds are exceeded, triggers '
    'an alert to the client.',
    S_body()))

checks_data = [
    ['#', 'Check Name', 'Logic', 'Action on Failure'],
    ['1', 'Null Rate Guard',
     'CustomerID null rate > 5%',
     'Reject batch; notify client'],
    ['2', 'Type Enforcement',
     'Quantity not integer OR UnitPrice not numeric',
     'Reject affected rows'],
    ['3', 'Price Sanity',
     'UnitPrice < 0',
     'Flag & quarantine row'],
    ['4', 'Duplicate Removal',
     'Exact row-level duplicate',
     'Drop silently; log count'],
    ['5', 'Return Separation',
     'Quantity < 0 OR Invoice starts with "C"',
     'Route to returns_fact table'],
    ['6', 'StockCode Pattern',
     'Does not match ^\\d{5}[A-Z]?$',
     'Flag as operational code'],
]
checks_table = Table(checks_data,
                     colWidths=[0.6*cm, 3.0*cm, 5.2*cm, 4.2*cm])
checks_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), PRYZM_TEAL),
    ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
    ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',   (0,0), (-1,-1), 8.5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [PRYZM_LIGHT, WHITE]),
    ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#D5DDE5')),
    ('LEFTPADDING', (0,0), (-1,-1), 7),
    ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ('TOPPADDING',  (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
    ('ALIGN',      (0,0), (0,-1), 'CENTER'),
]))
story.append(checks_table)
story.append(Spacer(1, 0.3*cm))

# ── Section 3 ──────────────────────────────
story.append(HRFlowable(width='100%', thickness=1, color=PRYZM_LIGHT,
                         spaceAfter=4))
story.append(Paragraph('3. Top Priority Improvement', S_h1()))

# Highlight box
story.append(Table(
    [[Paragraph(
        '<b>Priority #1: Implement a Returns &amp; Cancellations '
        'Separation Protocol</b>',
        ParagraphStyle('hl', fontName='Helvetica-Bold', fontSize=10.5,
                       textColor=WHITE, leading=16)
    )]],
    colWidths=[16*cm],
    style=TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRYZM_BLUE),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ('TOPPADDING',  (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ])
))
story.append(Spacer(1, 0.3*cm))

story.append(Paragraph(
    '<b>The Problem.</b> Returns (negative quantities) and cancellations '
    '(Invoice prefix "C") are currently co-mingled with standard sales records. '
    'This single issue cascades into at least four downstream failures: '
    'gross revenue is overstated, inventory levels are incorrect, '
    'customer purchase frequency is inflated, and any machine-learning model '
    'trained on this data will learn from corrupted signals.',
    S_body()))

story.append(Paragraph(
    '<b>The Solution.</b> Introduce a two-table architecture at the staging layer: '
    'a <b>sales_fact</b> table containing only clean, positive-quantity transactions, '
    'and a <b>returns_fact</b> table containing all negative-quantity and '
    'cancellation records. A reconciliation step then links each return to its '
    'original sale using a SQL Window Function or Pandas merge on '
    '(CustomerID, StockCode, |Quantity|), enabling accurate net revenue '
    'and return-rate reporting.',
    S_body()))

story.append(Paragraph('<b>Implementation Sketch (Python/Pandas):</b>', S_h2()))

code_text = (
    'df_sales   = df[df["Quantity"] > 0 &amp; ~df["Invoice"].str.startswith("C")]\n'
    'df_returns = df[df["Quantity"] &lt; 0 | df["Invoice"].str.startswith("C")]\n\n'
    '# Reconcile returns to original invoices\n'
    'df_net = df_sales.merge(\n'
    '    df_returns.rename(columns={"Quantity": "ReturnQty"}),\n'
    '    on=["CustomerID", "StockCode"], how="left"\n'
    ').assign(NetQty=lambda x: x["Quantity"] + x["ReturnQty"].fillna(0))'
)
story.append(Paragraph(code_text, S_code()))

story.append(Paragraph(
    '<b>Why this matters most.</b> Resolving this single issue immediately '
    'delivers clean data to every downstream consumer — dashboards, forecasting '
    'models, and financial reports — without requiring any schema changes or '
    'client-side modifications. It is the highest-leverage action available '
    'and can be deployed within one sprint.',
    S_body()))

# ── Closing ──────────────────────────────
story.append(Spacer(1, 0.5*cm))
story.append(HRFlowable(width='100%', thickness=1, color=PRYZM_TEAL,
                         spaceAfter=8))
story.append(Table(
    [[Paragraph(
        'Ahmed Maala &nbsp;|&nbsp; contact@ahmedmaala.com &nbsp;|&nbsp; '
        'LinkedIn: linkedin.com/in/ahmedmaala &nbsp;|&nbsp; '
        'GitHub: github.com/ahmedmaala',
        ParagraphStyle('footer_text', fontName='Helvetica', fontSize=8.5,
                       textColor=PRYZM_GREY, alignment=TA_CENTER)
    )]],
    colWidths=[16*cm],
    style=TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
    ])
))

# ─────────────────────────────────────────
# Build PDF
# ─────────────────────────────────────────
doc = PRYZMDocTemplate(
    PDF_PATH,
    pagesize=A4,
    leftMargin=1.8*cm,
    rightMargin=1.8*cm,
    topMargin=2.0*cm,
    bottomMargin=1.8*cm,
)
doc.build(story)
print(f"✅  PDF generated: {PDF_PATH}")
