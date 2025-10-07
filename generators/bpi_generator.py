import random
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

from .base_generator import DocumentGenerator, generate_random_transactions


class BPIGenerator(DocumentGenerator):
    """Generate realistic BPI bank statements."""

    def generate_account_number(self):
        """Generate a realistic BPI account number."""
        # BPI account numbers are typically 10-12 digits
        return f"{random.randint(1000000000, 9999999999)}"

    def generate_statement(self, filename, statement_num=1):
        """
        Generate a BPI bank statement PDF.

        Args:
            filename: Output PDF filename
            statement_num: Statement number (for unique identifiers)
        """
        # Customer info
        name = self.get_random_name()
        address = self.get_random_address()

        # Account info
        account_number = self.generate_account_number()
        account_type = random.choice(['Savings Account', 'Checking Account', 'Current Account'])

        # Branch info
        branches = [
            'Ortigas Center Branch',
            'Makati Branch',
            'BGC Branch',
            'Quezon Avenue Branch',
            'Eastwood Branch',
            'Alabang Branch'
        ]
        branch = random.choice(branches)

        # Statement period (last month)
        end_date = datetime.now() - timedelta(days=random.randint(1, 10))
        start_date = end_date - timedelta(days=30)

        # Statement date
        statement_date = end_date + timedelta(days=random.randint(1, 3))

        # Generate transactions
        starting_balance = round(random.uniform(30000, 100000), 2)
        num_transactions = random.randint(8, 20)
        transactions = generate_random_transactions(num_transactions, starting_balance)

        # Calculate summary
        total_credits = sum(t['credit'] for t in transactions)
        total_debits = sum(t['debit'] for t in transactions)
        ending_balance = transactions[-1]['balance'] if transactions else starting_balance
        display_ending_balance = ending_balance

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=50, leftMargin=50,
                                topMargin=40, bottomMargin=40)
        story = []
        styles = getSampleStyleSheet()

        # Define BPI color scheme
        bpi_red = colors.HexColor('#C8102E')
        bpi_gray = colors.HexColor('#58595B')

        # Define styles
        title_style = ParagraphStyle(
            'BPITitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=16,
            textColor=bpi_red,
            alignment=TA_LEFT
        )

        header_style = ParagraphStyle(
            'Header',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=bpi_gray,
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

        # Header section
        story.append(Paragraph("<b>BPI</b>", title_style))
        story.append(Paragraph("BANK OF THE PHILIPPINE ISLANDS",
                              ParagraphStyle('subtitle', parent=normal_text, fontSize=8, textColor=bpi_gray)))
        story.append(Spacer(1, 0.2*inch))

        # Statement title
        story.append(Paragraph("<b>STATEMENT OF ACCOUNT</b>", header_style))
        story.append(Spacer(1, 0.1*inch))

        # Account information section
        account_info_data = [
            ['<b>Account Name:</b>', name],
            ['<b>Account Number:</b>', account_number],
            ['<b>Account Type:</b>', account_type],
            ['<b>Branch:</b>', branch],
            ['', ''],
            ['<b>Statement Period:</b>', f"{start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}"],
            ['<b>Statement Date:</b>', statement_date.strftime('%B %d, %Y')],
        ]

        account_table_data = []
        for row in account_info_data:
            account_table_data.append([
                Paragraph(row[0], normal_text),
                Paragraph(row[1], normal_text)
            ])

        account_table = Table(account_table_data, colWidths=[2*inch, 4*inch])
        account_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(account_table)
        story.append(Spacer(1, 0.15*inch))

        # Account Summary
        story.append(Paragraph("<b>ACCOUNT SUMMARY</b>", header_style))
        story.append(Spacer(1, 0.05*inch))

        summary_data = [
            ['<b>Beginning Balance:</b>', f'PHP {starting_balance:,.2f}'],
            ['<b>Total Credits:</b>', f'PHP {total_credits:,.2f}'],
            ['<b>Total Debits:</b>', f'PHP {total_debits:,.2f}'],
            ['<b>Ending Balance:</b>', f'PHP {display_ending_balance:,.2f}'],
        ]

        summary_table_data = []
        for row in summary_data:
            summary_table_data.append([
                Paragraph(row[0], normal_text),
                Paragraph(row[1], ParagraphStyle('summary_amt', parent=normal_text, alignment=TA_RIGHT))
            ])

        summary_table = Table(summary_table_data, colWidths=[4*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (0, -1), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, -1), (-1, -1), 1, colors.black),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 0.2*inch))

        # Transaction History
        story.append(Paragraph("<b>TRANSACTION HISTORY</b>", header_style))
        story.append(Spacer(1, 0.05*inch))

        # Transaction table header
        trans_header = [
            Paragraph('<b>Date</b>', ParagraphStyle('th', parent=small_text, fontName='Helvetica-Bold')),
            Paragraph('<b>Description</b>', ParagraphStyle('th', parent=small_text, fontName='Helvetica-Bold')),
            Paragraph('<b>Debit</b>', ParagraphStyle('th', parent=small_text, fontName='Helvetica-Bold', alignment=TA_RIGHT)),
            Paragraph('<b>Credit</b>', ParagraphStyle('th', parent=small_text, fontName='Helvetica-Bold', alignment=TA_RIGHT)),
            Paragraph('<b>Balance</b>', ParagraphStyle('th', parent=small_text, fontName='Helvetica-Bold', alignment=TA_RIGHT))
        ]

        trans_data = [trans_header]

        # Add opening balance row
        trans_data.append([
            Paragraph(start_date.strftime('%m/%d/%Y'), small_text),
            Paragraph('OPENING BALANCE', small_text),
            Paragraph('', small_text),
            Paragraph('', small_text),
            Paragraph(f'{starting_balance:,.2f}', ParagraphStyle('bal', parent=small_text, alignment=TA_RIGHT))
        ])

        # Add transactions
        for trans in transactions:
            debit_str = f"{trans['debit']:,.2f}" if trans['debit'] > 0 else ''
            credit_str = f"{trans['credit']:,.2f}" if trans['credit'] > 0 else ''

            trans_data.append([
                Paragraph(trans['date'], small_text),
                Paragraph(trans['description'], small_text),
                Paragraph(debit_str, ParagraphStyle('debit', parent=small_text, alignment=TA_RIGHT)),
                Paragraph(credit_str, ParagraphStyle('credit', parent=small_text, alignment=TA_RIGHT)),
                Paragraph(f"{trans['balance']:,.2f}", ParagraphStyle('bal', parent=small_text, alignment=TA_RIGHT))
            ])

        # Add closing balance row
        trans_data.append([
            Paragraph(end_date.strftime('%m/%d/%Y'), small_text),
            Paragraph('CLOSING BALANCE', ParagraphStyle('closing', parent=small_text, fontName='Helvetica-Bold')),
            Paragraph('', small_text),
            Paragraph('', small_text),
            Paragraph(f'{display_ending_balance:,.2f}',
                     ParagraphStyle('closing_bal', parent=small_text, fontName='Helvetica-Bold', alignment=TA_RIGHT))
        ])

        trans_table = Table(trans_data, colWidths=[0.9*inch, 2.4*inch, 0.9*inch, 0.9*inch, 1*inch])
        trans_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BACKGROUND', (0, 0), (-1, 0), bpi_gray),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('LINEABOVE', (0, -1), (-1, -1), 1.5, colors.black),
        ]))
        story.append(trans_table)
        story.append(Spacer(1, 0.2*inch))

        # Important notices
        story.append(Paragraph("<b>IMPORTANT REMINDERS</b>", header_style))
        story.append(Spacer(1, 0.05*inch))

        notices = [
            "Please verify your account statement immediately. Report any discrepancies within 30 days from statement date.",
            "For inquiries, please contact BPI Customer Service at (02) 889-10000 or visit your branch of account.",
            "Keep your account information confidential. BPI will never ask for your password or OTP.",
            "Ensure sufficient funds in your account to avoid penalties and service charges."
        ]

        for notice in notices:
            story.append(Paragraph(f"• {notice}", small_text))
            story.append(Spacer(1, 0.05*inch))

        story.append(Spacer(1, 0.1*inch))

        # Footer
        footer_text = """<b>Bank of the Philippine Islands</b><br/>
BPI Head Office, Ayala Avenue corner Paseo de Roxas, Makati City, Philippines<br/>
Tel: (02) 889-10000 | www.bpi.com.ph | customercare@bpi.com.ph<br/>
<i>This is a computer-generated statement and does not require a signature.</i>"""

        story.append(Paragraph(footer_text, ParagraphStyle('footer', parent=small_text, alignment=TA_CENTER)))

        # Confidentiality notice
        story.append(Spacer(1, 0.1*inch))
        confidential_text = """<i>CONFIDENTIAL: This statement is intended solely for the account holder named above.
If you have received this statement in error, please contact BPI immediately.</i>"""
        story.append(Paragraph(confidential_text, ParagraphStyle('confidential', parent=small_text, fontSize=6, alignment=TA_CENTER)))

        # Build PDF
        doc.build(story)

        return filename


def generate_bpi_statement(filename, statement_num=1):
    """
    Generate a BPI bank statement.

    Args:
        filename: Output PDF filename
        statement_num: Statement number (for unique identifiers)
    """
    generator = BPIGenerator()
    return generator.generate_statement(filename, statement_num)
