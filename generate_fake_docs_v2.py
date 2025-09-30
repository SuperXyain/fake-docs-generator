from faker import Faker
import random
from datetime import datetime, timedelta
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.graphics.barcode import code128

fake = Faker('en_PH')

def generate_account_number():
    return f"{random.randint(20000000000, 29999999999)}"

def generate_bill_number():
    return f"PT344-PBTRMT"

def generate_can():
    return f"{random.randint(200000000000, 299999999999)}"

def generate_meter_number():
    return f"{random.randint(100000000, 199999999)}"

def generate_meralco_bill_pdf(filename, bill_num):

    name = fake.name()
    address = f"{random.randint(1, 999)} {fake.street_name()}, {random.choice(['Pasig City', 'Quezon City', 'Makati', 'Manila', 'Mandaluyong', 'Taguig'])}"
    account_number = generate_account_number()
    can = generate_can()
    meter_number = generate_meter_number()

    start_day = random.randint(1, 5)
    start_date = datetime(2025, 8, start_day)
    end_date = start_date + timedelta(days=random.randint(28, 31))
    due_date = end_date + timedelta(days=random.randint(18, 22))


    previous_reading = random.randint(100000, 500000)
    consumption = random.randint(120, 450)
    current_reading = previous_reading + consumption
    multiplier = 1

    generation = round(consumption * random.uniform(6.0, 7.0), 2)
    transmission = round(consumption * random.uniform(0.9, 1.1), 2)
    system_loss = round(consumption * random.uniform(0.5, 0.7), 2)
    distribution = round(consumption * random.uniform(2.5, 3.5), 2)
    subsidies = round(consumption * random.uniform(-0.1, 0.1), 2)
    govt_taxes = round(consumption * random.uniform(0.05, 0.15), 2)
    universal_charges = round(consumption * random.uniform(0.05, 0.15), 2)
    fit_all = round(consumption * random.uniform(0.01, 0.05), 2)

    current_charges_subtotal = generation + transmission + system_loss + distribution + subsidies + govt_taxes + universal_charges + fit_all


    other_charges = round(random.uniform(50, 150), 2)

    previous_consumption = round(consumption * random.uniform(0.8, 1.2), 2)


    total_current = round(current_charges_subtotal + other_charges, 2)


    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    story = []
    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        'MeralcoTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        textColor=colors.HexColor('#E63946'),
        alignment=TA_CENTER
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        spaceBefore=10,
        spaceAfter=5
    )

    small_text = ParagraphStyle(
        'SmallText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7
    )

    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9
    )


    story.append(Paragraph("MERALCO", title_style))

    subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=8, alignment=TA_CENTER)
    story.append(Paragraph("Manila Electric Company", subtitle_style))
    story.append(Spacer(1, 0.2*inch))


    billtitle_style = ParagraphStyle('billtitle', parent=styles['Normal'], fontSize=14, fontName='Helvetica-Bold', alignment=TA_LEFT)
    story.append(Paragraph("YOUR electric bill", billtitle_style))
    story.append(Spacer(1, 0.1*inch))


    account_info_data = [
        ['Customer Account Number (CAN)', can],
        ['Meter No.', meter_number],
        ['Bill Date', end_date.strftime('%d %b %Y')],
        ['Billing Period', f"{start_date.strftime('%d %b')} - {end_date.strftime('%d %b %Y')}"],
        ['Bill Seq. / 210094', f'{random.randint(1, 12)}/210094']
    ]

    account_table = Table(account_info_data, colWidths=[2.5*inch, 3*inch])
    account_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(account_table)
    story.append(Spacer(1, 0.15*inch))


    bold_text = ParagraphStyle('BoldText', parent=normal_text, fontName='Helvetica-Bold')
    story.append(Paragraph(name, bold_text))
    story.append(Paragraph(address, bold_text))
    story.append(Spacer(1, 0.15*inch))


    pay_style = ParagraphStyle('pay', parent=styles['Normal'], fontSize=10, fontName='Helvetica-Bold')
    amount_style = ParagraphStyle('amount', parent=styles['Normal'], fontSize=18, fontName='Helvetica-Bold', textColor=colors.HexColor('#E63946'), alignment=TA_RIGHT)

    amount_due_data = [
        [Paragraph("Please Pay", pay_style),
         Paragraph(f"₱ {total_current:,.2f}", amount_style)],
        ['Due Date', due_date.strftime('%d %b %Y')]
    ]

    amount_table = Table(amount_due_data, colWidths=[2*inch, 3.5*inch])
    amount_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 9),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
        ('BOX', (0, 0), (-1, -1), 2, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
    ]))
    story.append(amount_table)
    story.append(Spacer(1, 0.2*inch))


    story.append(Paragraph("<b>Your monthly consumption</b>", section_header))

    consumption_data = [
        ['', 'kWh', '₱'],
        ['This month', f'{consumption:,}', f'{total_current:,.2f}'],
        ['Last month', f'{int(previous_consumption):,}', f'{total_current * random.uniform(0.85, 1.15):,.2f}']
    ]

    consumption_table = Table(consumption_data, colWidths=[2*inch, 1.5*inch, 2*inch])
    consumption_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(consumption_table)
    story.append(Spacer(1, 0.15*inch))


    story.append(Paragraph("<b>Electricity Used</b>", section_header))

    meter_data = [
        ['Present Reading', 'Previous Reading', 'Consumption', 'Multiplier'],
        [f'{current_reading:,} kWh', f'{previous_reading:,} kWh', f'{consumption} kWh', str(multiplier)]
    ]

    meter_table = Table(meter_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    meter_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meter_table)
    story.append(Spacer(1, 0.2*inch))


    story.append(Paragraph("<b>Bill Computation Summary</b>", section_header))

    charges_data = [
        ['Charges for billing period', ''],
        ['  Generation', f'₱{generation:,.2f}'],
        ['  Transmission', f'₱{transmission:,.2f}'],
        ['  System Loss', f'₱{system_loss:,.2f}'],
        ['  Distribution', f'₱{distribution:,.2f}'],
        ['  Subsidies', f'₱{subsidies:,.2f}'],
        ['  Government Taxes', f'₱{govt_taxes:,.2f}'],
        ['  Universal Charges (Taxes)', f'₱{universal_charges:,.2f}'],
        ['  FIT-All (Renewable)', f'₱{fit_all:,.2f}'],
        ['Current Charges', f'₱{current_charges_subtotal:,.2f}'],
        ['Other Charges', f'₱{other_charges:,.2f}'],
        ['Total Amount Due', f'₱{total_current:,.2f}']
    ]

    charges_table = Table(charges_data, colWidths=[3.5*inch, 2*inch])
    charges_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, -2), (-1, -2), 'Helvetica-Bold'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E8E8E8')),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#F5F5F5')),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEABOVE', (0, -2), (-1, -2), 1, colors.black),
        ('LINEABOVE', (0, -1), (-1, -1), 2, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(charges_table)
    story.append(Spacer(1, 0.2*inch))


    story.append(Paragraph("Payment Instruction", section_header))
    story.append(Paragraph("Please pay on or before the due date to avoid disconnection.", small_text))

    can_style = ParagraphStyle('can_text', parent=small_text, fontName='Helvetica-Bold')
    story.append(Paragraph(f"Customer Account Number (CAN): {can}", can_style))
    story.append(Spacer(1, 0.1*inch))


    story.append(Paragraph("For more information, visit www.meralco.com.ph", small_text))
    story.append(Paragraph("Customer hotline: (02) 16211 | Email: customercare@meralco.com.ph", small_text))


    doc.build(story)


output_dir = "fake_meralco_bills_v2"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


print("Generating 50 realistic MERALCO bills...")
for i in range(1, 51):
    pdf_filename = f"{output_dir}/realistic_bill_{i:03d}.pdf"
    generate_meralco_bill_pdf(pdf_filename, i)
    print(f"Generated: {pdf_filename}")

print(f"\nSuccessfully generated 50 realistic MERALCO bills in '{output_dir}/' directory")
