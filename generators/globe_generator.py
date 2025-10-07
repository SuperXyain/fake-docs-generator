"""Globe Telecom bill generator with configurable realism levels."""

import random
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

from .base_generator import DocumentGenerator


class GlobeGenerator(DocumentGenerator):
    """Generate realistic Globe Telecom bills."""

    def generate_account_number(self):
        """Generate a realistic Globe account number."""
        return f"{random.randint(1000000000, 9999999999)}"

    def generate_mobile_number(self):
        """Generate a realistic Philippine mobile number."""
        return f"917{random.randint(1000000, 9999999)}"

    def generate_invoice_number(self):
        """Generate invoice number."""
        return f"{random.randint(10000000000, 99999999999)}"

    def generate_bill(self, filename, bill_num=1):
        """
        Generate a Globe Telecom bill PDF.

        Args:
            filename: Output PDF filename
            bill_num: Bill number (for unique identifiers)
        """
        # Customer info
        name = self.get_random_name()
        address = self.get_random_address()

        # Account details
        account_number = self.generate_account_number()
        primary_number = self.generate_mobile_number()
        invoice_number = self.generate_invoice_number()

        # Plan details
        plans = ['GPlan 999', 'GPlan 1499', 'GPlan 1799', 'GPlan 2499']
        plan_name = random.choice(plans)
        plan_amount = int(plan_name.split()[1])

        # Dates
        year = random.choice([2024, 2025])
        month = random.randint(1, 12)
        start_date = datetime(year, month, 1)

        # Calculate last day of month
        if month == 12:
            end_date = datetime(year, month, 31)
        else:
            end_date = (datetime(year, month + 1, 1) - timedelta(days=1))

        invoice_date = end_date
        due_date = end_date + timedelta(days=random.randint(25, 30))

        # Bill number
        bill_no = random.randint(1, 12)

        # Calculate charges
        vatable_sales = round(plan_amount / 1.12, 2)
        vat = round(plan_amount - vatable_sales, 2)

        # Previous bill info
        previous_bill_amount = plan_amount
        payment_amount = previous_bill_amount
        remaining_balance = 0.00

        # Total amount to pay
        total_amount = plan_amount

        # Payment details
        payment_date = start_date - timedelta(days=random.randint(1, 5))
        payment_reference = f"GPNC{random.randint(1000000, 9999999)}OR{random.randint(1000000, 9999999)}"
        payment_method = random.choice(['GLOBESS1 - G-Cash', 'GLOBESS1 - Maya', 'GLOBESS1 - BPI', 'GLOBESS1 - BDO'])

        # Usage details
        data_usage_gb = round(random.uniform(0.5, 2.0), 2)
        data_cost = round(data_usage_gb * 1832, 2)  # Approximate cost per GB

        # BIR details
        bir_control_no = f"AC_126_11{year}_00{random.randint(100, 999)}"
        bir_series_from = "000000000001"
        bir_series_to = "999999999999"
        bir_date_issued = f"11/{random.randint(10, 20)}/{year}"
        tin_number = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(10000, 99999)}"

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=40, leftMargin=40,
                                topMargin=30, bottomMargin=30)
        story = []
        styles = getSampleStyleSheet()

        # Define Globe color scheme
        globe_blue = colors.HexColor('#1C439B')
        globe_light_blue = colors.HexColor('#6B8CC4')

        # Define styles
        title_style = ParagraphStyle(
            'GlobeTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.white,
            alignment=TA_CENTER
        )

        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=colors.black,
            spaceBefore=10,
            spaceAfter=6
        )

        normal_text = ParagraphStyle(
            'NormalText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9
        )

        small_text = ParagraphStyle(
            'SmallText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=7
        )

        # Header section with Globe branding
        header_data = [
            [Paragraph("<b>Globe</b>", title_style),
             Paragraph("<b>INVOICE</b>", ParagraphStyle('inv_title', parent=title_style, fontSize=16))]
        ]
        header_table = Table(header_data, colWidths=[3*inch, 3.5*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), globe_blue),
            ('BACKGROUND', (1, 0), (1, 0), colors.white),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (0, 0), 'CENTER'),
            ('ALIGN', (1, 0), (1, 0), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.05*inch))

        # Company info
        story.append(Paragraph("<b>Globe Telecom, Inc.</b>",
                              ParagraphStyle('company', parent=normal_text, fontSize=10, textColor=colors.white,
                                           backColor=globe_light_blue, leftIndent=10)))
        story.append(Paragraph(f"Invoice No. {invoice_number}",
                              ParagraphStyle('inv_no', parent=normal_text, fontSize=9, alignment=TA_RIGHT)))
        story.append(Spacer(1, 0.1*inch))

        # Customer and bill info
        info_data = [
            [Paragraph(f"<b>{name}</b><br/>{address}", normal_text),
             Paragraph(f"<b>Bill no. {bill_no}</b><br/><br/><b>Page 1 of 2</b>",
                      ParagraphStyle('bill_no', parent=normal_text, alignment=TA_RIGHT))]
        ]
        info_table = Table(info_data, colWidths=[3.5*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.1*inch))

        # Amount to pay box
        amount_data = [
            [Paragraph("<b>Amount to Pay</b><br/>(total amount due)", normal_text),
             Paragraph(f"<b>Php {total_amount:,.2f}</b>",
                      ParagraphStyle('amount', parent=normal_text, fontSize=16, fontName='Helvetica-Bold', alignment=TA_RIGHT))]
        ]
        amount_table = Table(amount_data, colWidths=[3*inch, 3.5*inch])
        amount_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 2, colors.black),
            ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(amount_table)
        story.append(Spacer(1, 0.1*inch))

        # Account details
        account_data = [
            ['Account Number', 'Primary Number'],
            [account_number, primary_number],
            ['Customer TIN', 'Invoice Date'],
            ['', invoice_date.strftime('%m/%d/%y')],
            ['Billing Period', 'Due Date'],
            [f"{start_date.strftime('%m/%d/%y')} to {end_date.strftime('%m/%d/%y')}", due_date.strftime('%m/%d/%y')]
        ]

        account_table_data = []
        for row in account_data:
            account_table_data.append([
                Paragraph(f"<b>{row[0]}</b>" if account_data.index(row) % 2 == 0 else row[0], normal_text),
                Paragraph(f"<b>{row[1]}</b>" if account_data.index(row) % 2 == 0 else row[1],
                         ParagraphStyle('right', parent=normal_text, alignment=TA_RIGHT))
            ])

        account_table = Table(account_table_data, colWidths=[3*inch, 3.5*inch])
        account_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(account_table)
        story.append(Spacer(1, 0.15*inch))

        # Plan info box
        story.append(Paragraph(plan_name, ParagraphStyle('plan', parent=normal_text,
                                                         backColor=globe_blue, textColor=colors.white,
                                                         leftIndent=10, fontName='Helvetica-Bold')))
        story.append(Spacer(1, 0.1*inch))

        # Statement Summary
        story.append(Paragraph("<b>Statement Summary</b>", header_style))

        # Charges for this month
        charges_data = [
            [Paragraph('<b>Charges For This Month</b>', normal_text), ''],
            [Paragraph('Monthly Recurring Fee', normal_text), ''],
            [Paragraph('  Monthly Plan', normal_text), f'P {plan_amount:,.2f}'],
            [Paragraph('<b>Total</b>', ParagraphStyle('bold', parent=normal_text, fontName='Helvetica-Bold')),
             Paragraph(f'<b>Php {plan_amount:,.2f}</b>', ParagraphStyle('bold', parent=normal_text, fontName='Helvetica-Bold', alignment=TA_RIGHT))]
        ]

        charges_table = Table(charges_data, colWidths=[4.5*inch, 2*inch])
        charges_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ]))
        story.append(charges_table)
        story.append(Spacer(1, 0.1*inch))

        # Previous Bill Activity
        previous_data = [
            [Paragraph('<b>Previous Bill Activity</b>', normal_text), ''],
            [Paragraph('Previous Bill Amount', normal_text), f'P {previous_bill_amount:,.2f}'],
            [Paragraph('Less :', normal_text), ''],
            [Paragraph('  Payment', normal_text), f'(P {payment_amount:,.2f})'],
            [Paragraph('<b>Remaining Balance</b>', ParagraphStyle('bold', parent=normal_text, fontName='Helvetica-Bold')),
             Paragraph(f'<b>P {remaining_balance:.2f}</b>', ParagraphStyle('bold', parent=normal_text, fontName='Helvetica-Bold', alignment=TA_RIGHT))],
            [Paragraph('<b>Amount to Pay</b>', ParagraphStyle('bold', parent=normal_text, fontName='Helvetica-Bold')),
             Paragraph(f'<b>P {total_amount:,.2f}</b>', ParagraphStyle('bold', parent=normal_text, fontName='Helvetica-Bold', alignment=TA_RIGHT))]
        ]

        previous_table = Table(previous_data, colWidths=[4.5*inch, 2*inch])
        previous_table.setStyle(TableStyle([
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, -2), (-1, -2), 1, colors.grey),
            ('LINEBELOW', (0, -1), (-1, -1), 2, colors.black),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ]))
        story.append(previous_table)
        story.append(Spacer(1, 0.2*inch))

        # Payment channels info
        story.append(Paragraph("<b>Pay your Globe bills at any of our convenient payment channels</b>", small_text))
        story.append(Spacer(1, 0.05*inch))

        payment_channels = """<b>Same-day Posting:</b> Globe Online Bills Payment, GCash, Bayad Center,
SM Payment Center, Robinsons Department Store<br/>
<b>Other Payment Channels:</b> BDO, BPI, UnionBank, Landbank, Metrobank, Security Bank,
PNB, UCPB, Cebuana Lhuillier, M. Lhuillier, 7-11, and more"""

        story.append(Paragraph(payment_channels, small_text))
        story.append(Spacer(1, 0.1*inch))

        # Footer with BIR info
        story.append(Paragraph(f"BIR AC Control No. {bir_control_no}", small_text))
        story.append(Paragraph(f"Series from {bir_series_from} to {bir_series_to}", small_text))
        story.append(Paragraph(f"Date Issued: {bir_date_issued}", small_text))
        story.append(Paragraph(f"Invoice No. {invoice_number}", small_text))
        story.append(Spacer(1, 0.1*inch))

        # Important notices
        notice_text = """<b>In compliance with RA 9510 or the Credit Information Systems Act (CISA),</b>
we'll be sending basic credit information about your Globe account/s, including any overdue balance,
to the Credit Information Corp. (CIC), a state-run agency, on a monthly basis.<br/><br/>
<b>Please examine your Statement of Account immediately.</b> If no discrepancy is reported within
30 days from this bill's cut-off date, the contents of this statement will be considered correct."""

        story.append(Paragraph(notice_text, small_text))

        # Build PDF
        doc.build(story)

        return filename


def generate_globe_bill(filename, bill_num=1):
    """
    Generate a Globe Telecom bill.

    Args:
        filename: Output PDF filename
        bill_num: Bill number (for unique identifiers)
    """
    generator = GlobeGenerator()
    return generator.generate_bill(filename, bill_num)
