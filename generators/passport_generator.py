"""Philippine Passport generator for fraud detection testing."""

import random
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfgen import canvas

from .base_generator import DocumentGenerator


class PassportGenerator(DocumentGenerator):
    """Generate realistic Philippine Passport documents for testing."""

    def generate_passport_number(self):
        """Generate a realistic passport number."""
        # Philippine passport format: P + 7 digits + letter
        return f"P{random.randint(1000000, 9999999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}"

    def generate_mrz(self, surname, given_names, passport_num, nationality, dob, sex, expiry, personal_num):
        """
        Generate Machine Readable Zone (MRZ) for passport.
        Format: TD3 (2 lines, 44 characters each)
        """
        # Line 1: Type, Country Code, Surname, Given Names
        type_code = "P<"
        country_code = "PHL"

        # Format names (replace spaces with <, pad with <)
        surname_clean = surname.upper().replace(' ', '<')
        given_clean = given_names.upper().replace(' ', '<')

        # Combine names with separator
        full_name = f"{surname_clean}<<{given_clean}"
        # Pad or truncate to fill rest of line 1 (44 - 5 = 39 chars)
        full_name = (full_name + '<' * 39)[:39]

        line1 = f"{type_code}{country_code}{full_name}"

        # Line 2: Passport num, check digit, nationality, DOB, check digit, sex, expiry, check digit, personal num
        passport_clean = passport_num.replace(' ', '')
        check1 = self._calculate_check_digit(passport_clean)

        dob_str = dob.strftime('%y%m%d')
        check2 = self._calculate_check_digit(dob_str)

        expiry_str = expiry.strftime('%y%m%d')
        check3 = self._calculate_check_digit(expiry_str)

        # Personal number (often passport number + some identifier)
        personal_clean = (personal_num + '<' * 14)[:14]
        check4 = self._calculate_check_digit(personal_clean)

        # Final check digit for line 2
        line2_data = f"{passport_clean}{check1}{nationality}{dob_str}{check2}{sex}{expiry_str}{check3}{personal_clean}{check4}"
        check_final = self._calculate_check_digit(line2_data)

        line2 = f"{passport_clean}{check1}{nationality}{dob_str}{check2}{sex}{expiry_str}{check3}{personal_clean}{check4}{check_final}"

        # Pad line 2 to 44 characters if needed
        line2 = (line2 + '<' * 44)[:44]

        return f"{line1}\n{line2}"

    def _calculate_check_digit(self, data):
        """Calculate MRZ check digit using mod 10."""
        weights = [7, 3, 1]
        total = 0

        for i, char in enumerate(data):
            if char == '<':
                value = 0
            elif char.isdigit():
                value = int(char)
            elif char.isalpha():
                value = ord(char) - ord('A') + 10
            else:
                value = 0

            total += value * weights[i % 3]

        return str(total % 10)

    def generate_passport(self, filename, passport_num=1):
        """
        Generate a Philippine Passport PDF.

        Args:
            filename: Output PDF filename
            passport_num: Passport number (for unique identifiers)
        """
        # Personal data
        surnames = ['DELA CRUZ', 'SANTOS', 'REYES', 'GARCIA', 'RAMOS', 'MENDOZA', 'CRUZ', 'BAUTISTA']
        given_names_list = [
            'MARIA', 'JUAN', 'JOSE', 'ANA', 'CARLOS', 'ROSA', 'PEDRO', 'ANGELA',
            'RICARDO', 'CRISTINA', 'MIGUEL', 'ISABELA', 'FERNANDO', 'SOFIA'
        ]

        surname = random.choice(surnames)
        given_name = random.choice(given_names_list)
        middle_name = random.choice(given_names_list[:8])
        full_given = f"{given_name} {middle_name}"

        # Date of birth (18-65 years old)
        dob_year = random.randint(1959, 2006)
        dob_month = random.randint(1, 12)
        dob_day = random.randint(1, 28)
        date_of_birth = datetime(dob_year, dob_month, dob_day)

        # Sex
        sex = random.choice(['M', 'F'])

        # Place of birth
        places = ['MANILA', 'QUEZON CITY', 'DAVAO', 'CEBU', 'MAKATI', 'PASIG', 'TAGUIG', 'CALOOCAN']
        place_of_birth = random.choice(places)

        # Nationality
        nationality = 'FILIPINO'

        # Issue date (within last 5 years)
        issue_year = random.randint(2020, 2024)
        issue_month = random.randint(1, 12)
        issue_day = random.randint(1, 28)
        date_of_issue = datetime(issue_year, issue_month, issue_day)

        # Expiry date (10 years from issue)
        date_of_expiry = date_of_issue + timedelta(days=3650)

        # Passport number
        passport_number = self.generate_passport_number()

        # Authority
        authority = 'DFA MANILA'

        # Personal number for MRZ
        personal_num = passport_number + 'PHL' + date_of_birth.strftime('%y%m%d')

        # Generate MRZ
        mrz_text = self.generate_mrz(
            surname, full_given, passport_number,
            'PHL', date_of_birth, sex,
            date_of_expiry, personal_num
        )

        # Create PDF with landscape A5 (passport size)
        page_size = landscape(A5)
        doc = SimpleDocTemplate(
            filename,
            pagesize=page_size,
            rightMargin=15*mm,
            leftMargin=15*mm,
            topMargin=10*mm,
            bottomMargin=10*mm
        )

        story = []
        styles = getSampleStyleSheet()

        # Define custom styles
        header_style = ParagraphStyle(
            'PassportHeader',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#003f87')
        )

        field_label_style = ParagraphStyle(
            'FieldLabel',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=7,
            textColor=colors.grey
        )

        field_value_style = ParagraphStyle(
            'FieldValue',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10
        )

        mrz_style = ParagraphStyle(
            'MRZ',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=9,
            leading=11,
            textColor=colors.black
        )

        watermark_style = ParagraphStyle(
            'Watermark',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=24,
            alignment=TA_CENTER,
            textColor=colors.red
        )

        # Add flag image if available
        flag_path = 'assets/PH_FLAG.png'
        if os.path.exists(flag_path):
            flag_img = Image(flag_path, width=0.6*inch, height=0.4*inch)
        else:
            # Create placeholder if flag not found
            flag_img = Paragraph("🇵🇭", header_style)

        # Header section
        header_data = [
            [flag_img,
             Paragraph('<b>REPUBLIKA NG PILIPINAS | REPUBLIC OF THE PHILIPPINES</b><br/>'
                      'PASAPORTE / PASSPORT', header_style),
             Paragraph(f'<b>Passport No.</b><br/>{passport_number}',
                      ParagraphStyle('PassNum', parent=header_style, fontSize=9, alignment=TA_RIGHT))]
        ]

        header_table = Table(header_data, colWidths=[0.8*inch, 3.2*inch, 1.5*inch])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 2),
            ('RIGHTPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 0.15*inch))

        # TEST DOCUMENT watermark

        # Personal information section
        info_data = [
            [Paragraph('Surname', field_label_style),
             Paragraph(surname, field_value_style)],
            [Paragraph('Given name(s)', field_label_style),
             Paragraph(full_given, field_value_style)],
            [Paragraph('Date of birth', field_label_style),
             Paragraph(date_of_birth.strftime('%d %b %Y').upper(), field_value_style)],
            [Paragraph('Place of birth', field_label_style),
             Paragraph(place_of_birth, field_value_style)],
            [Paragraph('Nationality', field_label_style),
             Paragraph(nationality, field_value_style)],
            [Paragraph('Sex', field_label_style),
             Paragraph(sex, field_value_style)],
            [Paragraph('Date of issue', field_label_style),
             Paragraph(date_of_issue.strftime('%d %b %Y').upper(), field_value_style)],
            [Paragraph('Date of expiry', field_label_style),
             Paragraph(date_of_expiry.strftime('%d %b %Y').upper(), field_value_style)],
            [Paragraph('Authority', field_label_style),
             Paragraph(authority, field_value_style)],
        ]

        info_table = Table(info_data, colWidths=[1.3*inch, 4*inch])
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, colors.grey),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 0.2*inch))

        # MRZ section
        story.append(Paragraph('<b>Machine Readable Zone:</b>', field_label_style))
        story.append(Spacer(1, 0.05*inch))

        # MRZ with background
        mrz_data = [[Paragraph(mrz_text.replace('\n', '<br/>'), mrz_style)]]
        mrz_table = Table(mrz_data, colWidths=[5.5*inch])
        mrz_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f0f0f0')),
            ('BOX', (0, 0), (-1, -1), 1, colors.grey),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(mrz_table)
        # Build PDF
        doc.build(story)

        return filename


def generate_passport(filename, passport_num=1):
    """
    Generate a Philippine Passport for testing.

    Args:
        filename: Output PDF filename
        passport_num: Passport number (for unique identifiers)
    """
    generator = PassportGenerator()
    return generator.generate_passport(filename, passport_num)
