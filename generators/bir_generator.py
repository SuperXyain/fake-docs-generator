"""BIR Certificate of Tax Exemption generator with configurable realism levels."""

import random
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY

from .base_generator import DocumentGenerator


class BIRGenerator(DocumentGenerator):
    """Generate realistic BIR Certificate of Tax Exemption documents."""

    def generate_certificate_number(self):
        """Generate a realistic BIR certificate number."""
        return f"COOP-0{random.randint(1, 9)}{random.randint(10, 99)}{random.randint(10, 99)}-RR-01-RDO-{random.randint(100, 999):03d}"

    def generate_tin(self):
        """Generate a realistic TIN."""
        return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999):03d}"

    def generate_registration_number(self):
        """Generate CDA registration number."""
        return f"{random.randint(9000, 9999)}-{random.randint(10000000, 99999999)}"

    def generate_bill(self, filename, cert_num=1):
        """
        Generate a BIR Certificate of Tax Exemption PDF.

        Args:
            filename: Output PDF filename
            cert_num: Certificate number (for unique identifiers)
        """
        # Organization info
        org_types = [
            'COOPERATIVE',
            'FOUNDATION',
            'NON-PROFIT ORGANIZATION',
            'CHARITABLE INSTITUTION',
            'EDUCATIONAL INSTITUTION'
        ]
        org_type = random.choice(org_types)

        # Generate organization name
        org_name_parts = [
            'COOPERATIVE BANK OF',
            'FEDERATION OF',
            'ASSOCIATION OF',
            'COMMUNITY',
            'PEOPLES'
        ]
        locations = [
            'LA UNION',
            'QUEZON CITY',
            'MANILA',
            'CEBU',
            'DAVAO',
            'ILOILO',
            'BAGUIO'
        ]

        org_name = f"{random.choice(org_name_parts)} {random.choice(locations)}"

        # Address
        address_street = f"National Highway Sta. Barbara, Agoo, {random.choice(locations)}"

        # RDO and Tax info
        rdo_number = random.randint(1, 99)
        city = random.choice(['San Fernando City', 'Quezon City', 'Manila', 'Makati City'])
        location_name = random.choice(locations)
        tin = self.generate_tin()

        # Registration info
        registration_number = self.generate_registration_number()
        registration_date = datetime(random.randint(2005, 2015), random.randint(1, 12), random.randint(1, 28))

        # Certificate details
        cert_number = self.generate_certificate_number()

        # Revenue region
        revenue_region = random.randint(1, 17)
        office_location = random.choice(['Calasiao, Pangasinan', 'Quezon City', 'Manila', 'Makati City'])

        # Type of certificate
        is_original = random.choice([True, False])

        # Financial details
        accumulated_reserve = round(random.uniform(5000000, 15000000), 2)

        # Issue date
        issue_year = random.choice([2021, 2022, 2023, 2024])
        issue_month = random.randint(1, 12)
        issue_day = random.randint(1, 28)
        issue_date = datetime(issue_year, issue_month, issue_day)

        # Validity period
        validity_years = 5

        # Signatory
        signatories = [
            'ATTY. ANGELINA JONATHAN G. JAMINOLA',
            'ATTY. RICARDO M. SANTOS',
            'ATTY. MARIA CRISTINA L. REYES',
            'ATTY. JOSE P. FERNANDEZ'
        ]
        signatory_name = random.choice(signatories)

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=72, leftMargin=72,
                                topMargin=50, bottomMargin=50)
        story = []
        styles = getSampleStyleSheet()

        # Define styles
        header_style = ParagraphStyle(
            'BIRHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            alignment=TA_CENTER,
            spaceAfter=3
        )

        small_header = ParagraphStyle(
            'SmallHeader',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_CENTER,
            spaceAfter=3
        )

        title_style = ParagraphStyle(
            'Title',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            alignment=TA_CENTER,
            spaceAfter=12,
            spaceBefore=12
        )

        body_text = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontName='Times-Roman',
            fontSize=11,
            alignment=TA_JUSTIFY,
            leading=16,
            firstLineIndent=0
        )

        # Form number in top left
        story.append(Paragraph("BIR FORM NO. 2333-A", ParagraphStyle('form', parent=styles['Normal'],
                                                                       fontName='Helvetica', fontSize=9)))
        story.append(Spacer(1, 0.3*inch))

        # Header
        story.append(Paragraph("<b>Republic of the Philippines</b>", header_style))
        story.append(Paragraph("Department of Finance", small_header))
        story.append(Paragraph("<b>BUREAU OF INTERNAL REVENUE</b>", header_style))
        story.append(Paragraph("<b>Office of the Regional Director</b>", header_style))
        story.append(Paragraph(f"Revenue Region No. {revenue_region}", small_header))
        story.append(Paragraph(office_location, small_header))
        story.append(Spacer(1, 0.3*inch))

        # Original/Renewal checkbox
        checkbox_data = [
            [Paragraph('/', ParagraphStyle('check', parent=styles['Normal'], fontSize=11)) if is_original else '',
             'Original'],
            ['' if is_original else Paragraph('/', ParagraphStyle('check', parent=styles['Normal'], fontSize=11)),
             'Renewal']
        ]
        checkbox_table = Table(checkbox_data, colWidths=[0.3*inch, 0.8*inch])
        checkbox_table.setStyle(TableStyle([
            ('BOX', (0, 0), (0, -1), 1, colors.black),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ]))
        story.append(checkbox_table)
        story.append(Spacer(1, 0.2*inch))

        # Certificate number
        story.append(Paragraph(f"No. <u>{cert_number}</u>",
                              ParagraphStyle('cert_no', parent=styles['Normal'], fontSize=11, alignment=TA_RIGHT)))
        story.append(Spacer(1, 0.1*inch))

        # Title
        story.append(Paragraph("<b>CERTIFICATE OF TAX EXEMPTION</b>", title_style))
        story.append(Spacer(1, 0.15*inch))

        # Body text
        intro_text = f"""THIS IS TO CERTIFY THAT <b>{org_name}</b>, a {org_type.lower()}, with registered address at {address_street} is a duly-registered taxpayer of RDO No. {rdo_number}, {city}, {location_name} under Tax Identification No. {tin} and is registered with the Cooperative Development Authority under Registration Certificate No. {registration_number} dated {registration_date.strftime('%B %d, %Y')}."""

        story.append(Paragraph(intro_text, body_text))
        story.append(Spacer(1, 0.15*inch))

        # Exemption details
        exemption_intro = f"""As a <b>cooperative transacting with both members and non-members, with accumulated reserve and undivided net savings of not more than ten million pesos (₱ {accumulated_reserve:,.2f})</b>, {org_name} is entitled to the following tax exemptions and incentives provided for under Article 60 of Republic Act No. 9520, as implemented by Section 7 of the joint Rules and Regulations Implementing Articles 60, 61 and 144 of RA No. 9520:"""

        story.append(Paragraph(exemption_intro, body_text))
        story.append(Spacer(1, 0.1*inch))

        # Exemption list
        exemptions = [
            "Exemption from Income Tax on income from CDA-registered operations;",
            "Exemption from Value-added tax on CDA registered sales or transactions;",
            "Exemption from other Percentage tax;",
            "Exemption from Donor's tax on donations to duly accredited charitable, research and educational institutions, and reinvestment to socio-economic projects within the area of operation of the cooperative;",
            "Exemption from Excise tax for which it is directly liable;",
            "Exemption from Documentary stamp tax; <i>Provided, however</i>, that the other party to the taxable document/transaction who is not exempt shall be the one directly liable for the tax;",
            "Exemption from payment of Annual Registration fee of Five hundred pesos (₱500.00);",
            "Exemption from all taxes on transactions with insurance companies and banks, including but not limited to 20% final tax on interest deposits and 15% final income tax on interest income derived from a depositary bank under the expanded foreign currency deposit system."
        ]

        for i, exemption in enumerate(exemptions, 1):
            story.append(Paragraph(f"{i}. {exemption}",
                                  ParagraphStyle('list_item', parent=body_text, leftIndent=0.3*inch,
                                               firstLineIndent=-0.2*inch, spaceBefore=3)))

        story.append(Spacer(1, 0.15*inch))

        # Validity clause
        validity_text = f"""This Certificate of Registration shall be valid for five ({validity_years}) years unless sooner revoked by this Office for violation of any provisions of the Joint Revenue Regulations, the terms and conditions on the reverse side hereof or upon withdrawal of the Certificate of Registration by the CDA."""

        story.append(Paragraph(validity_text, body_text))
        story.append(Spacer(1, 0.15*inch))

        # Testimony clause
        testimony_text = f"""In Testimony Whereof, I have hereunto set my hand at {office_location.split(',')[0]}, {office_location.split(',')[1] if ',' in office_location else 'Philippines'} this {issue_date.strftime('%d')} day of {issue_date.strftime('%B')}, {issue_date.year}."""

        story.append(Paragraph(testimony_text, body_text))
        story.append(Spacer(1, 0.4*inch))

        # Signature
        story.append(Paragraph(f"<b>{signatory_name}</b>",
                              ParagraphStyle('signature', parent=styles['Normal'], fontSize=11,
                                           alignment=TA_CENTER, fontName='Helvetica-Bold')))
        story.append(Paragraph("Regional Director",
                              ParagraphStyle('title_sig', parent=styles['Normal'], fontSize=10,
                                           alignment=TA_CENTER)))

        # Build PDF
        doc.build(story)

        return filename


def generate_bir_certificate(filename, cert_num=1, realism_level='high'):
    """
    Generate a BIR Certificate of Tax Exemption.

    Args:
        filename: Output PDF filename
        cert_num: Certificate number (for unique identifiers)
        realism_level: 'high', 'medium', or 'low'
    """
    generator = BIRGenerator(realism_level=realism_level)
    return generator.generate_bill(filename, cert_num)
