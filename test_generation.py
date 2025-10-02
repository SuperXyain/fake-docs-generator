"""Quick test script to verify document generation."""

from generators import (
    generate_meralco_bill,
    generate_bpi_statement,
    generate_maynilad_bill,
    generate_globe_bill,
    generate_bir_certificate
)
import os

# Ensure outputs directory exists
os.makedirs('outputs', exist_ok=True)

print("=" * 60)
print("TESTING DOCUMENT GENERATORS")
print("=" * 60)

print("\n1. Testing MERALCO bill generation...")
meralco_file = "outputs/test_meralco.pdf"
generate_meralco_bill(meralco_file, bill_num=1, realism_level='high')
print(f"   [OK] Generated: {meralco_file}")

print("\n2. Testing Maynilad water bill generation...")
maynilad_file = "outputs/test_maynilad.pdf"
generate_maynilad_bill(maynilad_file, bill_num=1, realism_level='high')
print(f"   [OK] Generated: {maynilad_file}")

print("\n3. Testing Globe Telecom bill generation...")
globe_file = "outputs/test_globe.pdf"
generate_globe_bill(globe_file, bill_num=1, realism_level='high')
print(f"   [OK] Generated: {globe_file}")

print("\n4. Testing BPI bank statement generation...")
bpi_file = "outputs/test_bpi.pdf"
generate_bpi_statement(bpi_file, statement_num=1, realism_level='high')
print(f"   [OK] Generated: {bpi_file}")

print("\n5. Testing BIR Tax Exemption Certificate generation...")
bir_file = "outputs/test_bir.pdf"
generate_bir_certificate(bir_file, cert_num=1, realism_level='high')
print(f"   [OK] Generated: {bir_file}")

print("\n" + "=" * 60)
print("[SUCCESS] All tests passed! Documents generated successfully.")
print("=" * 60)
print("\nGenerated files:")
print(f"  - {meralco_file}")
print(f"  - {maynilad_file}")
print(f"  - {globe_file}")
print(f"  - {bpi_file}")
print(f"  - {bir_file}")
print("\nYou can now run: streamlit run main.py")
