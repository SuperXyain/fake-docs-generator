"""Fake document generators for AI fraud detection testing."""

from .meralco_generator import generate_meralco_bill
from .bpi_generator import generate_bpi_statement
from .maynilad_generator import generate_maynilad_bill
from .globe_generator import generate_globe_bill
from .bir_generator import generate_bir_certificate
from .coe_generator import generate_coe
from .passport_generator import generate_passport

__all__ = [
    'generate_meralco_bill',
    'generate_bpi_statement',
    'generate_maynilad_bill',
    'generate_globe_bill',
    'generate_bir_certificate',
    'generate_coe',
    'generate_passport'
]
