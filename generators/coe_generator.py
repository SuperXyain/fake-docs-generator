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


class COEGenerator(DocumentGenerator):
    """Generate realistic Certificate of Employment documents."""

    def __init__(self):
        """Initialize COE generator."""
        super().__init__()

    def get_company_info(self):
        """Generate realistic company information."""
        companies = [
            {
                'name': 'Techlog Center Philippines (TCP)',
                'address': '4F Two Evotech Building, Nuvali\nCity of Sta. Rosa, Laguna Philippines',
                'position': 'Customer Support Expert - Voice',
                'department': 'Customer Support',
                'supervisor': self.fake.name()
            },
            {
                'name': 'Asurion Philippines Inc.',
                'address': '25th Floor, Net One Center\nCrescent Park West, BGC, Taguig City',
                'position': 'Technical Support Specialist',
                'department': 'Technical Support',
                'supervisor': self.fake.name()
            },
            {
                'name': 'Concentrix Philippines',
                'address': '5th Avenue corner 26th Street\nBonifacio Global City, Taguig',
                'position': 'Customer Service Representative',
                'department': 'Customer Service',
                'supervisor': self.fake.name()
            },
            {
                'name': 'Teleperformance Manila',
                'address': 'Cyber Sigma Building, Eastwood City\nLibis, Quezon City',
                'position': 'Account Executive',
                'department': 'Sales and Operations',
                'supervisor': self.fake.name()
            }
        ]
        return random.choice(companies)

    def get_salary_range(self):
        """Generate realistic salary information."""
        base_salaries = [
            {'monthly': 22000, 'annual': 264000},
            {'monthly': 25000, 'annual': 300000},
            {'monthly': 27000, 'annual': 324000},
            {'monthly': 30000, 'annual': 360000},
            {'monthly': 32000, 'annual': 384000},
            {'monthly': 35000, 'annual': 420000}
        ]
        return random.choice(base_salaries)

    def generate_certificate(self, filename, cert_num=1):
        """
        Generate a Certificate of Employment PDF.

        Args:
            filename: Output PDF filename
            cert_num: Certificate number (for unique identification)
        """
        # Employee info
        employee_name = self.get_random_name()

        # Company info
        company = self.get_company_info()

        # Salary info
        salary = self.get_salary_range()

        # Dates
        # Start date: random date in the past (6 months to 3 years ago)
        start_date = datetime.now() - timedelta(days=random.randint(180, 1095))

        # Probation period (typically 3-6 months)
        probation_days = random.choice([90, 120, 150, 180])
        probation_end = start_date + timedelta(days=probation_days)

        # Certificate generation date (recent)
        cert_date = datetime.now() - timedelta(days=random.randint(1, 30))

        # Create PDF
        doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=60, leftMargin=60,
                                topMargin=50, bottomMargin=50)
        story = []
        styles = getSampleStyleSheet()

        # Define custom styles
        title_style = ParagraphStyle(
            'CompanyTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            alignment=TA_CENTER,
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            'CompanySubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#666666'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        doc_title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=20,
            spaceBefore=10
        )

        body_style = ParagraphStyle(
            'BodyText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            alignment=TA_LEFT,
            leading=16,
            spaceAfter=10
        )

        section_header_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            alignment=TA_LEFT,
            spaceAfter=6,
            spaceBefore=8
        )

        small_text_style = ParagraphStyle(
            'SmallText',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8,
            alignment=TA_LEFT,
            leading=12
        )

        # Header - Company name and info
        story.append(Paragraph(f"<b>{company['name']}</b>", title_style))
        story.append(Paragraph(company['address'].replace('\n', '<br/>'), subtitle_style))
        story.append(Spacer(1, 0.1*inch))

        # Date generated
        date_style = ParagraphStyle('DateStyle', parent=styles['Normal'], fontSize=9, alignment=TA_LEFT)
        story.append(Paragraph(f"Date Generated: {cert_date.strftime('%B %d, %Y')}", date_style))
        story.append(Spacer(1, 0.2*inch))

        # Recipient name
        story.append(Paragraph(f"<b>{employee_name}</b>", body_style))
        story.append(Spacer(1, 0.1*inch))

        # Salutation
        last_name = employee_name.split()[-1]
        story.append(Paragraph(f"Dear Mr./Ms. {last_name},", body_style))
        story.append(Spacer(1, 0.1*inch))

        # Main body - offer letter style
        intro_text = f"""<b>{company['name']}</b> is pleased to extend this offer of employment to you. We are extremely excited by the prospect of you joining our team. We believe the combination of your experience and skills will allow you to have a significant impact on the future success of {company['name'].split()[0]}."""
        story.append(Paragraph(intro_text, body_style))
        story.append(Spacer(1, 0.15*inch))

        # Section A - Employment Offer
        story.append(Paragraph("<b>A. Employment Offer</b>", section_header_style))

        position_text = f"""<b>Position:</b> We are offering you the position of <b>{company['position']}</b> reporting to {company['supervisor']} in {company['name'].split()[0]}. The position will be based at the <b>{company['address'].split(',')[0]}</b>."""
        story.append(Paragraph(position_text, body_style))

        start_date_text = f"""<b>Start Date:</b> We anticipate that upon acceptance of this job offer, your starting date of employment with {company['name'].split()[0]} will be no later than <b>{start_date.strftime('%B %d, %Y')}</b> subject to the <b>Conditions set forth in Part B of this letter</b>."""
        story.append(Paragraph(start_date_text, body_style))

        probation_text = f"""<b>Probationary Period:</b> From your starting date of employment, you will be on probation for no more than {probation_days} days effective {start_date.strftime('%B %d, %Y')} to {probation_end.strftime('%B %d, %Y')} ("Probation Period")."""
        story.append(Paragraph(probation_text, body_style))
        story.append(Spacer(1, 0.05*inch))

        probation_detail = """Your attainment of regular employment status is subject to your submission of all pre-employment documents and the successful and satisfactory completion of probationary period in accordance to the Company's employment standards. At any time during the probation period, your probationary employment may be terminated for just and authorized causes provided by law and/or your failure to meet the employment standards."""
        story.append(Paragraph(probation_detail, body_style))
        story.append(Spacer(1, 0.05*inch))

        probation_benefits = """During such probationary period, you will be entitled to statutory benefits available to you under Philippine laws."""
        story.append(Paragraph(probation_benefits, body_style))
        story.append(Spacer(1, 0.1*inch))

        # Basic Salary section
        story.append(Paragraph(f"<b>Basic Salary:</b> Your starting salary will be <b>PhP {salary['monthly']:,}</b> per month, which is equal to <b>PhP {salary['annual']:,}</b> on an annualized basis. Deductions for contributions to Social Security System, PhilHealth, Pag-Ibig and other relevant government agencies and withholding taxes on your compensation shall be made from your salary as required by law.", body_style))
        story.append(Spacer(1, 0.1*inch))

        # Management Incentive Bonus
        bonus_plan = random.choice(['Customer Care Incentive Plan Bonus', 'Performance Excellence Bonus', 'Achievement Incentive Bonus'])
        story.append(Paragraph(f"<b>Management Incentive Bonus:</b> You will also have the opportunity to earn a monthly bonus (<b>{bonus_plan}</b>), contingent upon your personal achievements and contributions to the success of the Company and other factors, including the performance of {company['name'].split()[0]} and the overall success of the business.", body_style))
        story.append(Spacer(1, 0.1*inch))

        # Holiday and Benefits
        story.append(Paragraph("<b>Holiday and other Statutory Benefits:</b> You will be entitled to take statutory holidays as are observed in the Philippines. The manner in which such holidays are taken may be provided for by rules no less favorable than applicable law as in force and as amended from time to time. You shall also enjoy all statutory benefits as are applicable to you under Philippine laws.", body_style))
        story.append(Spacer(1, 0.1*inch))

        # Leave Benefits
        pto_days = random.choice([15, 20, 25, 30])
        story.append(Paragraph(f"<b>Leave Benefits:</b> You will also be entitled to <b>{pto_days} days Paid Time Off (PTO)</b> for each calendar year upon regularization. <b>Annual PTO</b> entitlement accrues on a pro-rata basis throughout the year. <b>Annual PTO</b> is to be taken only with the prior agreement of the Company at such times as may be mutually convenient and in accordance with", body_style))

        # New page or continue
        story.append(Spacer(1, 0.2*inch))

        # Footer text
        footer_text = f"""the Company's HR policies. Any unused leave credits will be forfeited and will not be carried over to the next year unless expressly allowed by the Company.<br/><br/>
We look forward to having you join our team and are confident that you will make valuable contributions to {company['name']}. Should you have any questions or concerns, please feel free to contact the Human Resources Department.<br/><br/>
<b>Sincerely,</b>"""
        story.append(Paragraph(footer_text, body_style))
        story.append(Spacer(1, 0.4*inch))

        # Signature line
        hr_director = self.fake.name()
        signature_style = ParagraphStyle('Signature', parent=styles['Normal'], fontSize=10,
                                        fontName='Helvetica-Bold', alignment=TA_LEFT)
        story.append(Paragraph(f"<b>{hr_director}</b>", signature_style))
        story.append(Paragraph("Human Resources Director",
                              ParagraphStyle('Title', parent=styles['Normal'], fontSize=9, alignment=TA_LEFT)))
        story.append(Spacer(1, 0.15*inch))

        # Co-authored by line
        story.append(Paragraph(f"<i>Generated with Document Testing System</i>",
                              ParagraphStyle('Generated', parent=styles['Normal'], fontSize=7,
                                           textColor=colors.grey, alignment=TA_CENTER)))

        # Build PDF
        doc.build(story)

        return filename


def generate_coe(filename, cert_num=1):
    """
    Generate a Certificate of Employment document.

    Args:
        filename: Output PDF filename
        cert_num: Certificate number (for unique identification)
    """
    generator = COEGenerator()
    return generator.generate_certificate(filename, cert_num)
