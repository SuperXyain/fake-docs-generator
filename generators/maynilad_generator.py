"""Maynilad water bill generator with configurable realism levels."""

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


class MayniladGenerator(DocumentGenerator):
    """Generate realistic Maynilad water bills."""

    def generate_contract_account_number(self):
        """Generate a realistic Maynilad contract account number."""
        return f"{random.randint(50000000, 59999999)}"

    def generate_meter_number(self):
        """Generate a realistic meter number."""
        return f"AJP-{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(100000, 999999)}"

    def generate_mru_number(self):
        """Generate MRU number."""
        return f"{random.randint(64000000, 64999999)}"

    def generate_bill(self, filename, bill_num=1):
        """
        Generate a Maynilad water bill PDF.

        Args:
            filename: Output PDF filename
            bill_num: Bill number (for unique identifiers)
        """
        # Customer info
        name = self.get_random_name().upper()
        address = self.get_random_address()

        # Account details
        contract_account = self.generate_contract_account_number()
        meter_number = self.generate_meter_number()
        mru_number = self.generate_mru_number()
        seq_number = random.randint(3000, 5000)

        # ORCA number
        orca_number = f"{random.randint(1, 9)}"

        # Rate class
        rate_class = random.choice(['Residential', 'Commercial', 'Industrial'])
        business_area = random.choice(['South Quezon City', 'North Quezon City', 'Manila', 'Pasay', 'Paranaque'])

        # Dates - billing period
        year = random.choice([2024, 2025])
        month = random.randint(1, 12)
        start_date = datetime(year, month, random.randint(15, 25))
        reading_date = start_date + timedelta(days=random.randint(25, 35))
        due_date = reading_date + timedelta(days=random.randint(15, 20))

        # Invoice number
        invoice_number = f"0{random.randint(100000000000000000, 999999999999999999)}"

        # Machine SN
        machine_sn = ""

        # Meter readings
        previous_reading = random.randint(100, 300)
        consumption = random.randint(5, 15)  # in cubic meters
        present_reading = previous_reading + consumption

        # Previous 3 months consumption
        prev_month_1 = random.randint(5, 12)
        prev_month_2 = random.randint(5, 12)
        prev_month_3 = random.randint(5, 12)

        # Calculate charges
        basic_charge_minimum = round(random.uniform(2000, 2500), 2)
        fcda = round(random.uniform(-20, -10), 2)  # Usually negative
        environmental_charge = round(basic_charge_minimum * 0.25, 2)
        maintenance_service_charge = 1.50

        total_current_charges_before_tax = round(
            basic_charge_minimum + fcda + environmental_charge + maintenance_service_charge, 2
        )

        # VAT exempt amount
        vat_exempt = total_current_charges_before_tax
        govt_taxes = round(total_current_charges_before_tax * 0.025, 2)  # Approx 2.5%

        # Previous unpaid amount
        previous_unpaid = round(random.uniform(0, 1000), 2) if random.random() > 0.5 else 0

        # Total amount due
        total_amount_due = round(total_current_charges_before_tax + govt_taxes + previous_unpaid, 2)

        # Payment history
        payment_history = []
        if random.random() > 0.3:  # 70% chance of having payment history
            num_payments = random.randint(1, 2)
            for i in range(num_payments):
                payment_date = reading_date - timedelta(days=random.randint(30, 90))
                payment_amount = round(random.uniform(1000, 4000), 2)
                payment_or_number = f"{random.randint(100000000000, 999999999999)}"
                payment_history.append({
                    'amount': payment_amount,
                    'or_number': payment_or_number,
                    'date': payment_date.strftime('%m/%d/%Y')
                })

        # TIN and permit info
        tin = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(10000, 99999)}"
        permit_number = f"AC_116_03{random.randint(2020, 2025)}_00{random.randint(100, 999)}"
        date_issued = f"MARCH {random.randint(10, 20)}, {random.choice([2024, 2025])}"
        inclusive_serial = f"0{random.randint(100000000000000000, 999999999999999999)}-0{random.randint(100000000000000000, 999999999999999999)}"

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=50, leftMargin=50,
                                topMargin=40, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        # Define styles
        header_style = ParagraphStyle(
            'MayniladHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_CENTER
        )

        section_header = ParagraphStyle(
            'SectionHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=9,
            alignment=TA_CENTER,
            spaceBefore=6,
            spaceAfter=4
        )

        normal_text = ParagraphStyle(
            'NormalText',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8,
            alignment=TA_LEFT
        )

        small_text = ParagraphStyle(
            'SmallText',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=7
        )

        # Header with logo (if available) and company info
        story.append(Paragraph("<b>Maynilad Water Services, Inc.</b>", header_style))
        story.append(Paragraph("203 CORDILLERA ST BRGY MAHARLIKA<br/>STA MESA HEIGHTS QUEZON CITY",
                              ParagraphStyle('addr', parent=normal_text, fontSize=8, alignment=TA_CENTER)))
        story.append(Paragraph(f"VAT Reg TIN 005-393-442-00008<br/>SPM No.:<br/>Machine SN: {machine_sn}",
                              ParagraphStyle('tin', parent=small_text, alignment=TA_CENTER)))
        story.append(Spacer(1, 0.1*inch))

        # Invoice number and ORCA
        story.append(Paragraph(f"I N V #  {invoice_number}",
                              ParagraphStyle('inv', parent=normal_text, alignment=TA_CENTER, fontName='Courier-Bold')))
        story.append(Spacer(1, 0.05*inch))
        story.append(Paragraph(f"I N V O I C E<br/>For the Month of: April {year}",
                              ParagraphStyle('inv_title', parent=section_header, fontSize=10)))
        story.append(Spacer(1, 0.1*inch))

        # Service Information
        story.append(Paragraph("<b>SERVICE INFORMATION</b>", section_header))
        story.append(Spacer(1, 0.05*inch))

        service_info = f"""Contract Account No: <b>{contract_account}</b>
Account Name       : {name}
Service Address: {address.replace(chr(10), ' ')}
TIN                :
ORCA No.           :
Cardholder's Signature :
Rate Class         : {rate_class}
Business Area      : {business_area}"""

        story.append(Paragraph(service_info, normal_text))
        story.append(Spacer(1, 0.1*inch))

        # Metering Information
        story.append(Paragraph("─" * 60, normal_text))
        story.append(Paragraph("<b>METERING INFORMATION</b>", section_header))
        story.append(Spacer(1, 0.05*inch))

        metering_info = f"""Meter No.              MRU No.         Seq No.
{meter_number}    {mru_number}       {seq_number}
Reading Date       Present Reading Previous Reading
{reading_date.strftime('%m/%d/%Y')}         {present_reading:>3}            {previous_reading:>3}
                   Qty         Unit        Desc
Consumption        {consumption:>2}          (cu.m)      ACTUAL

Previous 3 Months  MAR         FEB         JAN

  Consumption      {prev_month_1:>2}          {prev_month_2:>2}          {prev_month_3:>2}"""

        story.append(Paragraph(metering_info, normal_text))
        story.append(Spacer(1, 0.1*inch))

        # Payment History
        if payment_history:
            story.append(Paragraph("─" * 60, normal_text))
            story.append(Paragraph("<b>PAYMENT HISTORY</b>", section_header))
            story.append(Spacer(1, 0.05*inch))

            payment_text = "Total Amount       OR#                  Date\n"
            for payment in payment_history:
                payment_text += f"{payment['amount']:>10.2f}     {payment['or_number']:>15}    {payment['date']}\n"

            story.append(Paragraph(payment_text, normal_text))
            story.append(Spacer(1, 0.1*inch))

        # Billing Summary
        story.append(Paragraph("─" * 60, normal_text))
        story.append(Paragraph("<b>BILLING SUMMARY</b>", section_header))
        story.append(Spacer(1, 0.05*inch))

        billing_summary = f"""BILLING PERIOD :{start_date.strftime('%m/%d/%Y')} TO {reading_date.strftime('%m/%d/%Y')}
Current Charges                                  {total_current_charges_before_tax:>10.2f}
Water bill:
  Basic Charge   Minimum                         {basic_charge_minimum:>10.2f}
  FCDA                                            {fcda:>10.2f}
  Environmental Charges (25% of Basic Charge)    {environmental_charge:>10.2f}
  Maintenance Service Charge (MSC)               {maintenance_service_charge:>10.2f}
Total Current Charges Before Taxes               {total_current_charges_before_tax:>10.2f}
                         VATable                 -
                         VAT Zero-rated          -
                         VAT Exempt              {vat_exempt:>10.2f}
VAT
Government Taxes                                 {govt_taxes:>10.2f}
Less Withholding Tax                             -

Previous Unpaid Amount                           {previous_unpaid:>10.2f}
         <Please pay immediately>
<b>AMOUNT DUE                                       {total_amount_due:>10.2f}</b>
  (Does not include current other charges)

<b>PAYMENT DUE DATE                              {due_date.strftime('%m/%d/%Y')}</b>"""

        story.append(Paragraph(billing_summary, normal_text))
        story.append(Spacer(1, 0.1*inch))

        # Footer with permit info
        story.append(Paragraph(f"Permit Number: {permit_number}", small_text))
        story.append(Paragraph(f"Date Issued: {date_issued}", small_text))
        story.append(Paragraph(f"Inclusive Series: {inclusive_serial}", small_text))
        story.append(Spacer(1, 0.1*inch))

        # Reminders
        story.append(Paragraph("─" * 60, normal_text))
        story.append(Paragraph("<b>REMINDERS</b>", section_header))
        story.append(Spacer(1, 0.05*inch))

        reminders = """Please examine your bill carefully. If no complaint is made within 60 days of receipt,
the bill is considered correct. Maynilad employees are not allowed to receive
cash payments. Pay your bill via safe and convenient digital channels, e.g Maya, GCash,
and online banking.

To avoid the inconvenience of a disconnected water service, please pay your water bill
on time. Kindly disregard this notice if payment has been made.

Check payment will not be accepted without the invoice effective October 01, 2019. For
inquiries, call Customer Care Hotline 1626 (Metro Manila) or 1800-1000-92937 (Cavite Area),
send a message to Maynilad's Text Hotline 0998-8641446, send an email to
customer.helpdesk@mayniladwater.com.ph, or follow us on social media accounts (Twitter/X:
@maynilad, Facebook: /Mayniladwater)"""

        story.append(Paragraph(reminders, small_text))

        # Build PDF
        doc.build(story)

        return filename


def generate_maynilad_bill(filename, bill_num=1):
    """
    Generate a Maynilad water bill.

    Args:
        filename: Output PDF filename
        bill_num: Bill number (for unique identifiers)
    """
    generator = MayniladGenerator()
    return generator.generate_bill(filename, bill_num)
