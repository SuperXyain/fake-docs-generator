from faker import Faker
import random
from datetime import datetime, timedelta
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.enums import TA_LEFT, TA_RIGHT

fake = Faker('en_PH')

def generate_account_number():
    return f"47-{random.randint(10000000, 99999999)}"

def generate_service_id():
    return f"{random.randint(210000000000, 219999999999)}"

def generate_meralco_bill_pdf(filename):

    name = fake.name()
    address = f"Blk {random.randint(1, 50)} Lot {random.randint(1, 50)} {fake.street_name()}, Brgy. {fake.city_suffix()}, {random.choice(['Pasig City', 'Quezon City', 'Makati City', 'Manila', 'Mandaluyong City', 'Taguig City'])}, Metro Manila"
    account_number = generate_account_number()
    service_id = generate_service_id()


    start_date = datetime(2025, 5, 1)
    end_date = datetime(2025, 5, 31)
    due_date = datetime(2025, 6, 15)


    previous_reading = random.randint(5000, 10000)
    consumption = random.randint(100, 500)
    current_reading = previous_reading + consumption
    multiplier = 1
    total_consumption = consumption * multiplier


    generation_rate = random.uniform(6.0, 7.0)
    generation_charge = round(total_consumption * generation_rate, 2)

    transmission_charge = round(total_consumption * random.uniform(0.8, 1.2), 2)
    system_loss_charge = round(total_consumption * random.uniform(1.5, 2.0), 2)
    distribution_charge = round(total_consumption * random.uniform(4.5, 5.5), 2)
    other_charges = round(random.uniform(100, 300), 2)

    subtotal = generation_charge + transmission_charge + system_loss_charge + distribution_charge + other_charges
    vat = round(subtotal * 0.12, 2)
    total_amount = round(subtotal + vat, 2)


    doc = SimpleDocTemplate(filename, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()


    title_style = ParagraphStyle('Title', parent=styles['Heading1'], textColor=colors.HexColor('#FF6600'), fontSize=20)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontSize=14)
    normal_style = styles['Normal']

    story.append(Paragraph("MERALCO - Manila Electric Company", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Customer Bill Summary", heading_style))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("<b>Customer Information</b>", normal_style))
    story.append(Spacer(1, 0.1*inch))

    customer_data = [
        ['Name:', name],
        ['Address:', address],
        ['Account Number:', account_number],
        ['Service Id:', service_id],
        ['Billing Period:', f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"],
        ['Due Date:', due_date.strftime('%B %d, %Y')]
    ]

    customer_table = Table(customer_data, colWidths=[1.5*inch, 5*inch])
    customer_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(customer_table)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("<b>Meter Reading</b>", normal_style))
    story.append(Spacer(1, 0.1*inch))

    meter_data = [
        ['Previous Reading:', f'{previous_reading} kWh'],
        ['Current Reading:', f'{current_reading} kWh'],
        ['Multiplier:', str(multiplier)],
        ['Total Consumption:', f'{total_consumption} kWh']
    ]

    meter_table = Table(meter_data, colWidths=[1.5*inch, 5*inch])
    meter_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(meter_table)
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("<b>Charges</b>", normal_style))
    story.append(Spacer(1, 0.1*inch))

    charges_data = [
        ['Generation Charge', f'PHP {generation_charge:,.2f}'],
        ['Transmission Charge', f'PHP {transmission_charge:,.2f}'],
        ['System Loss Charge', f'PHP {system_loss_charge:,.2f}'],
        ['Distribution Charge', f'PHP {distribution_charge:,.2f}'],
        ['Other Charges', f'PHP {other_charges:,.2f}'],
        ['VAT', f'PHP {vat:,.2f}'],
        ['Total Amount Due', f'PHP {total_amount:,.2f}']
    ]

    charges_table = Table(charges_data, colWidths=[4.5*inch, 2*inch])
    charges_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ]))
    story.append(charges_table)
    story.append(Spacer(1, 0.5*inch))

    story.append(Paragraph("---- Payment Stub ----", heading_style))
    story.append(Spacer(1, 0.1*inch))

    stub_data = [
        ['Account Number:', account_number],
        ['Billing Period:', f"{start_date.strftime('%b %d')} - {end_date.strftime('%b %d, %Y')}"],
        ['Amount Due:', f'PHP {total_amount:,.2f}'],
        ['Due Date:', due_date.strftime('%B %d, %Y')]
    ]

    stub_table = Table(stub_data, colWidths=[1.5*inch, 5*inch])
    stub_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(stub_table)
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Please present this stub when paying your bill.", normal_style))

    doc.build(story)

output_dir = "fake_meralco_bills_v1"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for i in range(1, 51):
    pdf_filename = f"{output_dir}/meralco_bill_{i:03d}.pdf"
    generate_meralco_bill_pdf(pdf_filename)
    print(f"Generated: {pdf_filename}")

print(f"\nSuccessfully generated 50 fake MERALCO bills in '{output_dir}/' directory")
