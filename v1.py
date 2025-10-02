from faker import Faker
import random
from datetime import datetime, timedelta
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

fake = Faker('en_PH')

def generate_account_number():
    return f"47-{random.randint(10000000, 99999999)}"

def generate_service_id():
    return f"{random.randint(210000000000, 219999999999)}"

def generate_meralco_bill_pdf(filename):
    # Generate fake data - obviously inauthentic
    name = fake.name()
    street = f"{random.randint(1, 999)} {fake.street_name()}"
    barangay = random.choice(['Kaunlaran', 'Sta. Lucia', 'Ugong', 'Kapitolyo'])
    city = random.choice(['Pasig City', 'Quezon City', 'Makati City', 'Manila'])
    address = f"{street}, {barangay}\n{city}, Metro Manila"

    # Wrong CAN format (should be 10 digits)
    can = f"{random.randint(100000, 999999)}"  # Too short
    meter_number = f"{random.randint(10000, 99999)}"  # Wrong format

    # Wrong date format
    year = random.choice([2020, 2021, 2022, 2023])
    month = random.randint(1, 12)
    start_date = datetime(year, month, random.randint(1, 10))
    end_date = start_date + timedelta(days=random.randint(25, 35))  # Inconsistent billing period
    due_date = end_date + timedelta(days=random.randint(5, 15))  # Wrong due date period

    # Meter readings
    previous_reading = random.randint(1500, 3000)
    consumption = random.randint(100, 400)
    current_reading = previous_reading + consumption

    # Simplified charges - missing proper breakdown
    rate = round(random.uniform(10.0, 15.0), 2)  # Wrong rate
    total_charge = round(consumption * rate, 2)

    # Wrong tax calculation
    tax = round(total_charge * 0.15, 2)  # Wrong tax rate
    total_amount = round(total_charge + tax, 2)

    # Create PDF
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=50, leftMargin=50, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    # No logo for v1 (obviously fake)

    # MERALCO header - but with wrong styling
    title_style = ParagraphStyle('Title', parent=styles['Normal'],
                                 fontName='Helvetica-Bold', fontSize=16,
                                 textColor=colors.HexColor('#FF6600'))
    story.append(Paragraph("MERALCO", title_style))
    story.append(Paragraph("<font size=9>Manila Electric Company</font>", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))

    # Missing proper header info (no TIN, no business center address)
    story.append(Paragraph("<b>Your electric bill</b>",
                          ParagraphStyle('heading', parent=styles['Normal'],
                                       fontName='Helvetica-Bold', fontSize=12)))
    story.append(Spacer(1, 0.15*inch))

    # Customer info - simplified format
    info_style = ParagraphStyle('info', parent=styles['Normal'], fontSize=9)
    customer_data = [
        ['Customer Name:', name],
        ['Address:', address],
        ['Account Number:', can],  # Wrong label (should be CAN)
        ['Meter No:', meter_number],
        ['Billing Period:', f"{start_date.strftime('%d %b %Y')} - {end_date.strftime('%d %b %Y')}"],
        ['Due Date:', due_date.strftime('%d %b %Y')]
    ]

    customer_table = Table(customer_data, colWidths=[1.5*inch, 4*inch])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 0.2*inch))

    # Amount box - simplified
    amount_style = ParagraphStyle('amount', parent=styles['Normal'],
                                  fontName='Helvetica-Bold', fontSize=16,
                                  textColor=colors.red)

    amount_data = [
        [Paragraph('Please Pay', ParagraphStyle('pay', parent=styles['Normal'],
                                                fontName='Helvetica-Bold', fontSize=10)),
         Paragraph(f'₱ {total_amount:,.2f}', amount_style)]
    ]

    amount_table = Table(amount_data, colWidths=[2*inch, 3*inch])
    amount_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('PADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(amount_table)
    story.append(Spacer(1, 0.2*inch))

    # Meter reading - no graph
    meter_header = ParagraphStyle('meter_header', parent=styles['Normal'],
                                  fontName='Helvetica-Bold', fontSize=10)
    story.append(Paragraph("Electricity Used", meter_header))
    story.append(Spacer(1, 0.1*inch))

    meter_data = [
        ['Previous Reading', 'Current Reading', 'Consumption'],
        [f'{previous_reading} kWh', f'{current_reading} kWh', f'{consumption} kWh']
    ]

    meter_table = Table(meter_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch])
    meter_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(meter_table)
    story.append(Spacer(1, 0.2*inch))

    # Simplified charges - missing proper breakdown
    story.append(Paragraph("Bill Summary", meter_header))
    story.append(Spacer(1, 0.1*inch))

    charges_data = [
        ['Electricity Charge', f'₱ {total_charge:,.2f}'],
        ['Tax (15%)', f'₱ {tax:,.2f}'],  # Wrong tax rate displayed
        ['Total Amount Due', f'₱ {total_amount:,.2f}']
    ]

    charges_table = Table(charges_data, colWidths=[4*inch, 1.5*inch])
    charges_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ]))
    story.append(charges_table)
    story.append(Spacer(1, 0.3*inch))

    # Missing: Environmental Impact, QR code, barcode, consumption graph, proper footer
    # Generic payment instructions
    small_style = ParagraphStyle('small', parent=styles['Normal'], fontSize=8)
    story.append(Paragraph("<b>Payment Instructions</b>", small_style))
    story.append(Paragraph("Pay at any Meralco center or authorized payment partner.", small_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"Account No: {can}", small_style))

    doc.build(story)

output_dir = "fake_meralco_bills_v1"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i in range(1, 51):
    pdf_filename = f"{output_dir}/meralco_bill_{i:03d}.pdf"
    generate_meralco_bill_pdf(pdf_filename)
    print(f"Generated: {pdf_filename}")

print(f"\nSuccessfully generated 50 fake MERALCO bills in '{output_dir}/' directory")
