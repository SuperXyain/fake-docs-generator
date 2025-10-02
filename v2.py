from faker import Faker
import random
from datetime import datetime, timedelta
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Line, Rect
from reportlab.graphics.barcode import code128
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics import renderPDF
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

fake = Faker('en_PH')

def generate_consumption_graph(current_consumption, filename='temp_graph.png'):
    """Generate a consumption graph similar to real Meralco bills"""
    # Generate historical data (12 months)
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Current year and previous year data
    current_year_data = [random.randint(100, 300) for _ in range(11)]
    current_year_data.append(current_consumption)  # Last month is current

    previous_year_data = [random.randint(100, 300) for _ in range(12)]

    # Create figure
    fig, ax = plt.subplots(figsize=(4.5, 2.5))

    x = range(len(months))
    width = 0.35

    # Create bars
    ax.bar([i - width/2 for i in x], previous_year_data, width, label='2020', color='#CCCCCC')
    ax.bar([i + width/2 for i in x], current_year_data, width, label='2021', color='#333333')

    # Customize
    ax.set_ylabel('kWh', fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(months, fontsize=7)
    ax.legend(loc='upper left', fontsize=7)
    ax.set_ylim(0, max(max(current_year_data), max(previous_year_data)) + 50)
    ax.grid(axis='y', alpha=0.3)

    # Add consumption values below bars
    for i in x:
        ax.text(i, -30, str(current_year_data[i]), ha='center', fontsize=6, color='#333333')

    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()

    return filename

def generate_account_number():
    return f"{random.randint(20000000000, 29999999999)}"

def generate_bill_number():
    return f"PT344-PBTRMT"

def generate_can():
    return f"{random.randint(200000000000, 299999999999)}"

def generate_meter_number():
    return f"{random.randint(100000000, 199999999)}"

def generate_meralco_bill_pdf(filename, bill_num):
    # Generate realistic-looking data with some inconsistencies
    name = fake.name()
    street_num = random.randint(1, 999)
    barangay = random.choice(['KAUNLARAN', 'STA. LUCIA', 'UGONG', 'KAPITOLYO', 'VALENCIA', 'PINAGBUHATAN'])
    city = random.choice(['Pasig City', 'Quezon City', 'Makati City', 'Manila', 'Mandaluyong City', 'Taguig City'])
    address = f"{street_num} {fake.street_name().upper()}, BARANGAY {barangay}\n{city.upper()}\nMETRO MANILA"

    # Generate CAN (Customer Account Number) - realistic format
    can = f"{random.randint(1000000000, 9999999999)}"

    # Meter number - realistic format
    meter_number = f"{random.randint(100, 999)}AB{random.randint(100000, 999999)}"

    # Invoice number
    invoice_number = f"{random.randint(1000000000000, 9999999999999)}"

    # Route and Print sequence
    route_seq = f"{random.randint(1000, 9999)} {random.randint(10, 99)} {random.randint(1000, 9999)}"
    print_seq = random.randint(10000, 99999)

    # TIN
    tin = "000-101-528-000-VAT"

    # Dates - more realistic billing cycle
    year = random.choice([2021, 2022, 2023, 2024])
    month = random.randint(1, 12)
    start_day = random.randint(1, 10)
    start_date = datetime(year, month, start_day)
    end_date = start_date + timedelta(days=random.randint(28, 31))
    due_date = end_date + timedelta(days=random.randint(10, 12))


    # Meter readings - realistic
    previous_reading = random.randint(2000, 4000)
    consumption = random.randint(150, 350)
    current_reading = previous_reading + consumption
    multiplier = 1

    # Rate per kWh (matching real bill)
    rate_per_kwh = round(random.uniform(8.00, 9.50), 2)

    # Charges breakdown (realistic structure)
    generation = round(consumption * random.uniform(4.0, 5.0), 2)
    transmission = round(consumption * random.uniform(0.6, 0.9), 2)
    system_loss = round(consumption * random.uniform(0.3, 0.5), 2)
    distribution = round(consumption * random.uniform(1.5, 2.0), 2)
    subsidies = round(consumption * random.uniform(0.05, 0.08), 2)
    govt_taxes = round(consumption * random.uniform(0.7, 1.0), 2)
    universal_charges = round(consumption * random.uniform(0.15, 0.25), 2)
    fit_all = round(consumption * random.uniform(0.08, 0.12), 2)

    # Introduce subtle calculation error for semi-fake aspect
    charges_subtotal = generation + transmission + system_loss + distribution + subsidies + govt_taxes + universal_charges + fit_all

    # Add remaining balance (sometimes)
    remaining_balance = round(random.uniform(0, 2000), 2) if random.random() > 0.5 else 0.0

    # Other charges
    other_charges = round(random.uniform(0, 50), 2)
    installment_due = 0.0

    # Total - sometimes with slight calculation error
    total_current = round(charges_subtotal + remaining_balance + other_charges + installment_due, 2)

    # Previous month consumption for comparison
    previous_consumption = int(consumption * random.uniform(0.85, 1.20))


    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    styles = getSampleStyleSheet()

    # Define styles matching Meralco branding
    title_style = ParagraphStyle(
        'MeralcoTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=colors.HexColor('#FF6600'),  # Meralco orange
        alignment=TA_LEFT
    )

    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        spaceBefore=8,
        spaceAfter=4
    )

    small_text = ParagraphStyle(
        'SmallText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6
    )

    normal_text = ParagraphStyle(
        'NormalText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8
    )

    # Header section with logo and addresses
    header_left = ParagraphStyle('header_left', parent=normal_text, fontSize=7, alignment=TA_LEFT)
    customer_address = f"<b>{name}</b><br/>{address}"

    # Try to add logo on the right
    try:
        logo = Image('images/meralco_logo.png', width=1.2*inch, height=1.2*inch)
        logo.hAlign = 'RIGHT'
    except:
        logo = None

    # Company info section
    company_info = f"""<b>CORINTHIAN EXECUTIVE REGENCY</b><br/>
Meter No.: {meter_number}<br/>
Route Seq.: {route_seq}    Print Seq.: {print_seq}"""

    # Create header with customer address, company info, and logo
    if logo:
        header_data = [
            [Paragraph(customer_address, header_left),
             Paragraph(f"<b>ESPANA-TUTUBAN BUSINESS CENTER</b><br/>LUBIRAN STREET BACOOD, STA. MESA<br/>MANILA, 1016 METRO MANILA<br/>{tin}",
                       ParagraphStyle('header_right', parent=normal_text, fontSize=7, alignment=TA_LEFT)),
             logo]
        ]
        header_table = Table(header_data, colWidths=[2.5*inch, 2.5*inch, 1.5*inch])
    else:
        header_data = [
            [Paragraph(customer_address, header_left),
             Paragraph(f"<b>ESPANA-TUTUBAN BUSINESS CENTER</b><br/>LUBIRAN STREET BACOOD, STA. MESA<br/>MANILA, 1016 METRO MANILA<br/>{tin}",
                       ParagraphStyle('header_right', parent=normal_text, fontSize=7, alignment=TA_LEFT))]
        ]
        header_table = Table(header_data, colWidths=[3*inch, 3*inch])

    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.1*inch))

    # Add Meralco branding info
    story.append(Paragraph(company_info, header_left))
    story.append(Spacer(1, 0.05*inch))

    # Invoice number (matching real bill format)
    invoice_style = ParagraphStyle('invoice', parent=normal_text, fontSize=7, alignment=TA_LEFT)
    story.append(Paragraph(f"Invoice No.: {invoice_number}", invoice_style))
    story.append(Spacer(1, 0.1*inch))


    # Bill title with invoice number
    billtitle_style = ParagraphStyle('billtitle', parent=styles['Normal'], fontSize=11, fontName='Helvetica-Bold', alignment=TA_LEFT)
    story.append(Paragraph("Your electric bill", billtitle_style))
    story.append(Spacer(1, 0.05*inch))

    # Account info section
    bill_period_text = f"<b>Billing Period</b><br/><b>{start_date.strftime('%d %b %Y')} to {end_date.strftime('%d %b %Y')}</b>"
    bill_date_text = f"<b>Bill Date</b><br/>{end_date.strftime('%d %b %Y')}"

    info_style = ParagraphStyle('info', parent=normal_text, fontSize=7)
    bill_info_data = [
        [Paragraph(bill_period_text, info_style), Paragraph(bill_date_text, info_style)]
    ]
    bill_info_table = Table(bill_info_data, colWidths=[2.5*inch, 2*inch])
    story.append(bill_info_table)
    story.append(Spacer(1, 0.1*inch))

    # Meter reading dates
    reading_date_text = f"""<b>Date of Meter Reading</b><br/>{end_date.strftime('%d %b %Y')}<br/><br/>
<b>Date of Next Meter Reading</b><br/>{(end_date + timedelta(days=30)).strftime('%d %b %Y')}"""

    meter_info_text = f"""<b>Electric Meter Number</b><br/>{meter_number}<br/><br/>
<b>Current Reading</b><br/>{current_reading:,}"""

    reading_info_data = [
        [Paragraph(reading_date_text, info_style), Paragraph(meter_info_text, info_style)]
    ]
    reading_info_table = Table(reading_info_data, colWidths=[2.5*inch, 2*inch])
    story.append(reading_info_table)
    story.append(Spacer(1, 0.05*inch))


    # Consumption info with previous reading
    consumption_header = ParagraphStyle('cons_header', parent=normal_text, fontSize=7)
    previous_text = f"<b>Previous Reading</b><br/>{previous_reading:,}"
    actual_text = f"<b>Actual Consumption</b><br/><font size=10><b>{consumption} kWh</b></font>"

    consumption_header_data = [
        [Paragraph(previous_text, consumption_header), "", Paragraph(actual_text, consumption_header)]
    ]
    consumption_header_table = Table(consumption_header_data, colWidths=[1.5*inch, 0.5*inch, 2*inch])
    story.append(consumption_header_table)
    story.append(Spacer(1, 0.1*inch))

    # Customer type and rate
    customer_type = "Residential"
    rate_text = f"<b>Your rate this month</b><br/><b>₱ {rate_per_kwh} per kWh</b><br/><font size=5>See formula in Addtl Bill Information</font>"
    story.append(Paragraph(f"<b>Customer Type</b><br/>{customer_type}", consumption_header))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(rate_text, consumption_header))
    story.append(Spacer(1, 0.1*inch))

    # Amount due box (matching real bill style)
    can_due_style = ParagraphStyle('can_due', parent=normal_text, fontSize=8, alignment=TA_CENTER)
    amount_due_style = ParagraphStyle('amount_due', parent=normal_text, fontSize=20, fontName='Helvetica-Bold', alignment=TA_RIGHT)

    amount_box_data = [
        [Paragraph(f"Customer Account Number (CAN)<br/><font size=14><b>{can}</b></font>", can_due_style),
         Paragraph(f"Due Date<br/><b>{due_date.strftime('%d %b %Y')}</b>", can_due_style)],
        ['', ''],
        [Paragraph("Please Pay", ParagraphStyle('please_pay', parent=normal_text, fontSize=10, alignment=TA_LEFT)),
         Paragraph(f"₱ {total_current:,.2f}", amount_due_style)]
    ]

    amount_table = Table(amount_box_data, colWidths=[3*inch, 2.5*inch])
    amount_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#E8F4F8')),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.black),
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (1, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(amount_table)
    story.append(Spacer(1, 0.15*inch))


    story.append(Paragraph("<b>Your monthly consumption</b>", section_header))

    # Generate and add consumption graph
    graph_file = None
    try:
        graph_file = f'temp_graph_{bill_num}.png'
        generate_consumption_graph(consumption, graph_file)
        graph_img = Image(graph_file, width=4.5*inch, height=2.5*inch)
        story.append(graph_img)
        story.append(Spacer(1, 0.1*inch))
    except Exception:
        # If graph generation fails, just continue without it
        pass

    # Consumption comparison text
    avg_temp = round(random.uniform(32, 35), 1)
    consumption_change = round((consumption / previous_consumption - 1) * 100, 1) if previous_consumption > 0 else 0
    comparison_text = f"""<b>Ave. temp this month</b><br/>{avg_temp}°C<br/>
0.7 deg lower than prev."""

    story.append(Paragraph(comparison_text, ParagraphStyle('comparison', parent=normal_text, fontSize=7)))
    story.append(Spacer(1, 0.1*inch))

    # Consumption explained section
    explanation_text = f"""<b>Your consumption explained</b><br/>
▲This bill is {abs(consumption_change):.1f}% {'higher' if consumption_change > 0 else 'lower'} (+{consumption - previous_consumption}kWh)<br/>
vs previous billing period<br/><br/>
▲This bill is {random.uniform(3, 6):.1f}% {'higher' if random.random() > 0.5 else 'lower'} (+{random.randint(5, 15)}kWh)<br/>
vs same period last year"""

    story.append(Paragraph(explanation_text, ParagraphStyle('explanation', parent=normal_text, fontSize=7)))
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

    # Add remaining balance if present
    charges_data_list = []
    charges_style = ParagraphStyle('charges_item', parent=normal_text, fontSize=7)

    if remaining_balance > 0:
        charges_data_list.append([
            Paragraph('Remaining Balance from previous bill', charges_style),
            f'{remaining_balance:,.2f}'
        ])
        charges_data_list.append([
            Paragraph('<i>(see details under What Remains Unpaid; does not include bills under review and installment)</i>', charges_style),
            ''
        ])

    charges_data_list.extend([
        [Paragraph('<b>Charges for this billing period</b>', charges_style), ''],
        [Paragraph('<i>Generation</i>', charges_style), f'{generation:,.2f}'],
        [Paragraph('<i>Transmission</i>', charges_style), f'{transmission:,.2f}'],
        [Paragraph('<i>System Loss</i>', charges_style), f'{system_loss:,.2f}'],
        [Paragraph('<i>Distribution (Meralco)</i>', charges_style), f'{distribution:,.2f}'],
        [Paragraph('<i>Subsidies</i>', charges_style), f'{subsidies:,.2f}'],
        [Paragraph('<i>Government Taxes</i>', charges_style), f'{govt_taxes:,.2f}'],
        [Paragraph('<i>Universal Charges</i>', charges_style), f'{universal_charges:,.2f}'],
        [Paragraph('<i>FIT-All (Renewable)</i>', charges_style), f'{fit_all:,.2f}'],
        [Paragraph('<i>Applied Credits</i>', charges_style), '0.00'],
        [Paragraph('<i>Other Charges</i>', charges_style), f'{other_charges:,.2f}'],
        [Paragraph('<i>Installment Due</i>', charges_style), f'{installment_due:,.2f}'],
        [Paragraph('<i>(see details under Additional Bill Information)</i>', charges_style), ''],
        [Paragraph('<b>Total Amount Due</b>', ParagraphStyle('total', parent=charges_style, fontName='Helvetica-Bold')),
         Paragraph(f'<b>₱ {total_current:,.2f}</b>', ParagraphStyle('total_amt', parent=charges_style, fontName='Helvetica-Bold'))]
    ])

    charges_table = Table(charges_data_list, colWidths=[4*inch, 1.5*inch])
    charges_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
        ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.black),
    ]))
    story.append(charges_table)
    story.append(Spacer(1, 0.15*inch))


    # Environmental Impact section
    story.append(Paragraph("<b>Environmental Impact</b>", section_header))
    story.append(Paragraph("Be energy efficient. Save and help take care of our environment", small_text))
    story.append(Spacer(1, 0.05*inch))

    # Calculate environmental data
    co2_equiv = round(consumption * 0.7144, 4)
    trees_offset = random.randint(5, 10)

    env_data = [
        ['Electricity Used', 'Equiv. GHG Emissions', 'Offset Emissions'],
        [f'{consumption} kWh', f'{co2_equiv} tCO2e*', f'{trees_offset} Trees**']
    ]

    env_table = Table(env_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch])
    env_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(env_table)
    story.append(Spacer(1, 0.05*inch))

    # Environmental footnotes
    story.append(Paragraph("*Using DOE's 2015-2017 National Emission Grid Factor of 0.0007122 tCO2e/kWh", small_text))
    story.append(Paragraph("**Per Arbor Day Foundation: One tree can absorb 48 pounds (0.0218 tonnes) of CO2/year", small_text))
    story.append(Spacer(1, 0.15*inch))

    # Payment Instruction section
    story.append(Paragraph("<b>Payment Instruction</b>", section_header))

    # Generate barcode-like text (simulated)
    barcode_text = f"||{'|' * random.randint(40, 60)}||"

    story.append(Paragraph("Please pay at any Meralco Business Center or through any accredited payment partner before the due date.", small_text))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(f"<font name='Courier' size=8>{barcode_text}</font>", small_text))
    story.append(Spacer(1, 0.05*inch))

    # Payment stub
    stub_style = ParagraphStyle('stub_label', parent=normal_text, fontSize=9)
    stub_bold_style = ParagraphStyle('stub_bold', parent=stub_style, fontName='Helvetica-Bold')

    payment_stub_data = [
        [Paragraph('Customer Account No. (CAN)', stub_style), Paragraph('Please pay', stub_style)],
        [Paragraph(f'<b>{can}</b>', stub_bold_style), Paragraph(f'<b>₱ {total_current:,.2f}</b>', stub_bold_style)]
    ]

    payment_table = Table(payment_stub_data, colWidths=[2.5*inch, 2.5*inch])
    payment_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(payment_table)
    story.append(Spacer(1, 0.1*inch))

    # Footer with contact information
    story.append(Paragraph("Payment made after {0} will be reflected on your next bill.".format(
        (due_date + timedelta(days=random.randint(5, 10))).strftime('%d %b %Y')), small_text))
    story.append(Paragraph("Permit No.: 0305-00036-BA/AR dtd: March 21, 2005", small_text))
    story.append(Spacer(1, 0.1*inch))

    # Contact channels
    contact_text = """<b>For more information, you may reach us through any of our channels</b><br/>
    @meralco | customercare@meralco.com.ph | www.meralco.com.ph | 16211"""

    story.append(Paragraph(contact_text, small_text))
    story.append(Spacer(1, 0.1*inch))

    # Bill concerns section (matching real bill)
    concerns_text = """<b>Bill Concerns?</b><br/>
Connect with us through our 24/7 channels:<br/>
fb.com/meralco | @meralco | Hotline 16211 | customercare@meralco.com.ph"""

    story.append(Paragraph(concerns_text, small_text))

    # Disclaimer
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("Please be informed that MERALCO may conduct a routine maintenance inspection of our customer metering facilities within this quarter", small_text))


    doc.build(story)

    # Clean up temp graph file after PDF is built
    if graph_file and os.path.exists(graph_file):
        try:
            os.remove(graph_file)
        except:
            pass


output_dir = "fake_meralco_bills_v2"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print("Generating 50 semi-realistic MERALCO bills (mix of authentic and inauthentic elements)...")
for i in range(1, 51):
    pdf_filename = f"{output_dir}/semi_realistic_bill_{i:03d}.pdf"
    generate_meralco_bill_pdf(pdf_filename, i)
    print(f"Generated: {pdf_filename}")

print(f"\nSuccessfully generated 50 semi-realistic MERALCO bills in '{output_dir}/' directory")
