#!/usr/bin/env python3
"""
Generate PDF from synthesis report markdown.
Uses ReportLab for PDF generation.
"""

import re
from pathlib import Path
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

def parse_markdown_table(table_text):
    """Parse markdown table into list of lists."""
    lines = [l.strip() for l in table_text.strip().split('\n') if l.strip()]
    if len(lines) < 2:
        return None

    rows = []
    for line in lines:
        if line.startswith('|') and not re.match(r'^\|[-:\s|]+\|$', line):
            cells = [c.strip() for c in line.split('|')[1:-1]]
            rows.append(cells)
    return rows if rows else None

def create_styles():
    """Create custom paragraph styles."""
    styles = getSampleStyleSheet()

    # Title style
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#1a1a2e'),
        alignment=TA_CENTER
    ))

    # Heading 1
    styles.add(ParagraphStyle(
        name='Heading1Custom',
        parent=styles['Heading1'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=12,
        textColor=HexColor('#16213e'),
        borderWidth=1,
        borderColor=HexColor('#0f3460'),
        borderPadding=5
    ))

    # Heading 2
    styles.add(ParagraphStyle(
        name='Heading2Custom',
        parent=styles['Heading2'],
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8,
        textColor=HexColor('#0f3460')
    ))

    # Heading 3
    styles.add(ParagraphStyle(
        name='Heading3Custom',
        parent=styles['Heading3'],
        fontSize=12,
        spaceBefore=12,
        spaceAfter=6,
        textColor=HexColor('#1a1a2e')
    ))

    # Body text
    styles.add(ParagraphStyle(
        name='BodyCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        alignment=TA_JUSTIFY,
        spaceAfter=8
    ))

    # Bold text
    styles.add(ParagraphStyle(
        name='BoldText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        fontName='Helvetica-Bold'
    ))

    # Bullet points
    styles.add(ParagraphStyle(
        name='BulletCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        leftIndent=20,
        spaceAfter=4
    ))

    # Code block
    styles.add(ParagraphStyle(
        name='CodeBlock',
        parent=styles['Code'],
        fontSize=8,
        leading=10,
        leftIndent=10,
        rightIndent=10,
        backColor=HexColor('#f5f5f5'),
        borderWidth=1,
        borderColor=HexColor('#cccccc'),
        borderPadding=5
    ))

    return styles

def markdown_to_flowables(md_content, styles):
    """Convert markdown content to ReportLab flowables."""
    flowables = []
    lines = md_content.split('\n')
    i = 0

    # Table collection
    in_table = False
    table_lines = []

    # Code block collection
    in_code = False
    code_lines = []

    while i < len(lines):
        line = lines[i]

        # Skip empty lines
        if not line.strip():
            if in_table and table_lines:
                # End of table
                table_data = parse_markdown_table('\n'.join(table_lines))
                if table_data:
                    flowables.append(create_table(table_data, styles))
                    flowables.append(Spacer(1, 10))
                table_lines = []
                in_table = False
            i += 1
            continue

        # Code blocks
        if line.strip().startswith('```'):
            if in_code:
                # End code block
                if code_lines:
                    code_text = '\n'.join(code_lines)
                    flowables.append(Paragraph(code_text.replace('\n', '<br/>'), styles['CodeBlock']))
                    flowables.append(Spacer(1, 8))
                code_lines = []
                in_code = False
            else:
                in_code = True
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        # Tables
        if line.strip().startswith('|'):
            in_table = True
            table_lines.append(line)
            i += 1
            continue

        if in_table and table_lines:
            # End of table (non-table line encountered)
            table_data = parse_markdown_table('\n'.join(table_lines))
            if table_data:
                flowables.append(create_table(table_data, styles))
                flowables.append(Spacer(1, 10))
            table_lines = []
            in_table = False

        # Horizontal rule / page break
        if line.strip() == '---':
            flowables.append(Spacer(1, 15))
            i += 1
            continue

        # Title (# heading)
        if line.startswith('# ') and not line.startswith('## '):
            text = clean_markdown(line[2:])
            flowables.append(Paragraph(text, styles['ReportTitle']))
            i += 1
            continue

        # Heading 1 (## heading)
        if line.startswith('## '):
            text = clean_markdown(line[3:])
            flowables.append(Paragraph(text, styles['Heading1Custom']))
            i += 1
            continue

        # Heading 2 (### heading)
        if line.startswith('### '):
            text = clean_markdown(line[4:])
            flowables.append(Paragraph(text, styles['Heading2Custom']))
            i += 1
            continue

        # Heading 3 (#### heading)
        if line.startswith('#### '):
            text = clean_markdown(line[5:])
            flowables.append(Paragraph(text, styles['Heading3Custom']))
            i += 1
            continue

        # Bullet points
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            text = clean_markdown(line.strip()[2:])
            flowables.append(Paragraph(f"• {text}", styles['BulletCustom']))
            i += 1
            continue

        # Numbered lists
        if re.match(r'^\d+\.\s', line.strip()):
            text = clean_markdown(re.sub(r'^\d+\.\s', '', line.strip()))
            num = re.match(r'^(\d+)\.', line.strip()).group(1)
            flowables.append(Paragraph(f"{num}. {text}", styles['BulletCustom']))
            i += 1
            continue

        # Regular paragraph
        text = clean_markdown(line)
        if text:
            flowables.append(Paragraph(text, styles['BodyCustom']))

        i += 1

    # Handle any remaining table
    if table_lines:
        table_data = parse_markdown_table('\n'.join(table_lines))
        if table_data:
            flowables.append(create_table(table_data, styles))

    return flowables

def clean_markdown(text):
    """Clean markdown formatting for PDF."""
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'<i>\1</i>', text)
    # Inline code
    text = re.sub(r'`(.+?)`', r'<font face="Courier">\1</font>', text)
    # Links (just show text)
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    return text

def create_table(data, styles):
    """Create a ReportLab table from parsed data."""
    if not data:
        return Spacer(1, 0)

    # Create table with proper column widths
    col_count = len(data[0]) if data else 0
    col_width = 6.5 * inch / max(col_count, 1)

    # Wrap cell content in Paragraphs
    table_data = []
    for row_idx, row in enumerate(data):
        new_row = []
        for cell in row:
            style = styles['BoldText'] if row_idx == 0 else styles['BodyCustom']
            new_row.append(Paragraph(clean_markdown(cell), style))
        table_data.append(new_row)

    table = Table(table_data, colWidths=[col_width] * col_count)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#0f3460')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f8f9fa')),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    return table

def generate_pdf(input_path, output_path):
    """Generate PDF from markdown file."""
    # Read markdown
    md_content = Path(input_path).read_text(encoding='utf-8')

    # Create PDF document
    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Create styles
    styles = create_styles()

    # Convert markdown to flowables
    flowables = markdown_to_flowables(md_content, styles)

    # Build PDF
    doc.build(flowables)
    print(f"PDF generated: {output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    input_file = script_dir / "_synthesis_report_full.md"
    output_file = script_dir / "_synthesis_report_full.pdf"

    generate_pdf(input_file, output_file)
