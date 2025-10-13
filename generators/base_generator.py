
from faker import Faker
import random
from datetime import datetime, timedelta
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER

fake = Faker('en_PH')

class DocumentGenerator:
    """Base class for document generators."""

    def __init__(self):
        """Initialize document generator."""
        self.fake = fake

    def get_random_name(self):
        """Generate a random Filipino name."""
        return self.fake.name()

    def get_random_address(self):
        """Generate a random Filipino address."""
        street_num = random.randint(1, 999)
        street = self.fake.street_name().upper()
        barangay = random.choice([
            'KAUNLARAN', 'STA. LUCIA', 'UGONG', 'KAPITOLYO',
            'VALENCIA', 'PINAGBUHATAN', 'BAGUMBAYAN', 'RIZAL'
        ])
        city = random.choice([
            'Pasig City', 'Quezon City', 'Makati City', 'Manila',
            'Mandaluyong City', 'Taguig City', 'Muntinlupa City', 'Parañaque City'
        ])
        return f"{street_num} {street}, BARANGAY {barangay}\n{city.upper()}\nMETRO MANILA"

    def get_random_date_range(self, days=30):
        """
        Generate random billing period dates.

        Args:
            days: Number of days in the billing period

        Returns:
            Tuple of (start_date, end_date, due_date)
        """
        year = random.choice([2022, 2023, 2024])
        month = random.randint(1, 12)
        start_day = random.randint(1, 10)

        start_date = datetime(year, month, start_day)
        end_date = start_date + timedelta(days=days)
        due_date = end_date + timedelta(days=random.randint(10, 12))

        return start_date, end_date, due_date


    def format_currency(self, amount):
        """Format amount as Philippine Peso."""
        return f"₱ {amount:,.2f}"

    def get_paragraph_style(self, name, parent, **kwargs):
        """Create a custom paragraph style."""
        return ParagraphStyle(name, parent=parent, **kwargs)


def generate_random_transactions(num_transactions=10, starting_balance=50000):
    """
    Generate realistic bank transactions.

    Args:
        num_transactions: Number of transactions to generate
        starting_balance: Starting account balance

    Returns:
        List of transaction dicts with date, description, debit, credit, balance
    """
    transactions = []
    balance = starting_balance

    debit_types = [
        "ATM WITHDRAWAL",
        "ONLINE PURCHASE",
        "BILLS PAYMENT",
        "INTERBANK TRANSFER",
        "CHECK PAYMENT",
        "POS PURCHASE",
        "ANNUAL FEE",
        "SERVICE CHARGE"
    ]

    credit_types = [
        "SALARY CREDIT",
        "FUND TRANSFER",
        "CASH DEPOSIT",
        "CHECK DEPOSIT",
        "INTEREST CREDIT",
        "REFUND"
    ]

    current_date = datetime.now()

    for i in range(num_transactions):
        days_ago = random.randint(1, 30)
        trans_date = current_date - timedelta(days=days_ago)

        is_debit = random.random() < 0.7

        if is_debit:
            trans_type = random.choice(debit_types)
            amount = round(random.uniform(100, 5000), 2)
            debit = amount
            credit = 0
            balance -= amount

            if "PURCHASE" in trans_type:
                merchant = random.choice(["SHOPEE", "LAZADA", "SM STORE", "GRAB", "FOODPANDA"])
                description = f"{trans_type} - {merchant}"
            elif trans_type == "BILLS PAYMENT":
                biller = random.choice(["MERALCO", "PLDT", "CONVERGE", "MAYNILAD"])
                description = f"{trans_type} - {biller}"
            else:
                description = trans_type
        else:
            trans_type = random.choice(credit_types)
            amount = round(random.uniform(500, 20000), 2)
            debit = 0
            credit = amount
            balance += amount
            description = trans_type

        transactions.append({
            'date': trans_date.strftime('%m/%d/%Y'),
            'description': description,
            'debit': debit,
            'credit': credit,
            'balance': round(balance, 2)
        })

    transactions.sort(key=lambda x: datetime.strptime(x['date'], '%m/%d/%Y'))

    balance = starting_balance
    for trans in transactions:
        if trans['debit'] > 0:
            balance -= trans['debit']
        else:
            balance += trans['credit']
        trans['balance'] = round(balance, 2)

    return transactions
