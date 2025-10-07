
import streamlit as st
import os
import zipfile
from datetime import datetime
import io
import csv

from generators import generate_meralco_bill, generate_bpi_statement, generate_maynilad_bill, generate_globe_bill, generate_bir_certificate, generate_coe

# Ensure output directory exists
os.makedirs('outputs', exist_ok=True)

def create_zip_file(files):
    """Create a zip file from a list of file paths."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in files:
            zip_file.write(file_path, os.path.basename(file_path))
    zip_buffer.seek(0)
    return zip_buffer

def create_metadata_csv(metadata):
    """Create CSV metadata file."""
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=['filename', 'doc_type', 'generated_at'])
    writer.writeheader()
    writer.writerows(metadata)
    return csv_buffer.getvalue()

def main_page():
    # Header
    st.title('🔧 Fake Docs Generator for Testing')
    st.write('Generate realistic fake documents to benchmark AI fraud detection systems')
    st.warning('⚠️ **FOR TESTING ONLY** - This app generates fake documents for AI fraud detection benchmarking. Do not use for malicious purposes.', icon="⚠️")

    st.divider()

    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        st.info("""
        **Document Generator**

        Generate realistic fake documents for testing your AI fraud detection system.

        All documents are generated with consistent, high-quality output.
        """)

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        st.header("📄 Document Type")
        doc_type = st.selectbox(
            "Select Document Type",
            ("MERALCO Bill", "Maynilad Water Bill", "Globe Telecom Bill", "BPI Bank Statement", "BIR Tax Exemption Certificate", "Certificate of Employment"),
            key="main_selectbox"
        )

    with col2:
        st.header("📊 Quantity")
        num_docs = st.slider(
            "Number of documents to generate",
            min_value=1,
            max_value=50,
            value=5,
            help="Select how many fake documents to generate"
        )

    st.divider()

    # Document-specific information
    if doc_type == "MERALCO Bill":
        with st.expander("ℹ️ About MERALCO Bills"):
            st.write("""
            **Generated MERALCO bills include:**
            - Realistic customer information
            - Billing period and consumption data
            - Detailed charge breakdown
            - Consumption graphs
            - Environmental impact section
            - Payment instructions
            - MERALCO branding and logo
            """)
    elif doc_type == "Maynilad Water Bill":
        with st.expander("ℹ️ About Maynilad Water Bills"):
            st.write("""
            **Generated Maynilad bills include:**
            - Contract account number and customer information
            - Meter reading details and consumption history
            - Service information (rate class, business area)
            - Detailed billing summary with water charges
            - FCDA and environmental charges
            - Payment history (if applicable)
            - Government taxes breakdown
            """)
    elif doc_type == "Globe Telecom Bill":
        with st.expander("ℹ️ About Globe Telecom Bills"):
            st.write("""
            **Generated Globe bills include:**
            - Account and mobile number information
            - Plan details and monthly recurring fees
            - Usage summary (data, calls, SMS)
            - Previous bill activity and payments
            - VAT breakdown
            - Globe branding and colors
            - Payment channel information
            """)
    elif doc_type == "BPI Bank Statement":
        with st.expander("ℹ️ About BPI Bank Statements"):
            st.write("""
            **Generated BPI statements include:**
            - Account holder information
            - Account number and branch details
            - Statement period
            - Transaction history with running balance
            - Account summary (credits, debits, balances)
            - BPI branding
            """)
    elif doc_type == "BIR Tax Exemption Certificate":
        with st.expander("ℹ️ About BIR Tax Exemption Certificates"):
            st.write("""
            **Generated BIR certificates include:**
            - BIR Form 2333-A format
            - Certificate number and organization details
            - Tax Identification Number (TIN)
            - CDA registration information
            - Complete list of tax exemptions (8 items)
            - Validity period (5 years)
            - Regional Director signature
            - Official BIR letterhead and formatting
            """)
    else:  # Certificate of Employment
        with st.expander("ℹ️ About Certificate of Employment"):
            st.write("""
            **Generated COE documents include:**
            - Company letterhead and information
            - Employee name and position details
            - Employment offer and start date
            - Salary information (monthly and annual)
            - Benefits package (PTO, bonuses, statutory benefits)
            - Probationary period details
            - HR Director signature
            - Professional formatting
            """)

    # Generation section
    st.divider()
    st.header("🚀 Generate Documents")

    col1, col2 = st.columns([3, 1])
    with col1:
        generate_button = st.button("📑 Generate Documents", type="primary", use_container_width=True)
    with col2:
        include_metadata = st.checkbox("Include metadata", value=True, help="Include CSV file with generation parameters")

    if generate_button:
        # Progress tracking
        st.info(f"Generating {num_docs} {doc_type.lower()}(s)...")
        progress_bar = st.progress(0)
        status_text = st.empty()

        generated_files = []
        metadata = []
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        # Generate documents
        for i in range(num_docs):
            status_text.text(f"Generating document {i+1} of {num_docs}...")

            if doc_type == "MERALCO Bill":
                filename = f"outputs/meralco_bill_{timestamp}_{i+1:03d}.pdf"
                generate_meralco_bill(filename, bill_num=i+1)
                doc_type_short = "MERALCO"
            elif doc_type == "Maynilad Water Bill":
                filename = f"outputs/maynilad_bill_{timestamp}_{i+1:03d}.pdf"
                generate_maynilad_bill(filename, bill_num=i+1)
                doc_type_short = "MAYNILAD"
            elif doc_type == "Globe Telecom Bill":
                filename = f"outputs/globe_bill_{timestamp}_{i+1:03d}.pdf"
                generate_globe_bill(filename, bill_num=i+1)
                doc_type_short = "GLOBE"
            elif doc_type == "BPI Bank Statement":
                filename = f"outputs/bpi_statement_{timestamp}_{i+1:03d}.pdf"
                generate_bpi_statement(filename, statement_num=i+1)
                doc_type_short = "BPI"
            elif doc_type == "BIR Tax Exemption Certificate":
                filename = f"outputs/bir_certificate_{timestamp}_{i+1:03d}.pdf"
                generate_bir_certificate(filename, cert_num=i+1)
                doc_type_short = "BIR"
            else:  # Certificate of Employment
                filename = f"outputs/coe_{timestamp}_{i+1:03d}.pdf"
                generate_coe(filename, cert_num=i+1)
                doc_type_short = "COE"

            generated_files.append(filename)
            metadata.append({
                'filename': os.path.basename(filename),
                'doc_type': doc_type_short,
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })

            progress_bar.progress((i + 1) / num_docs)

        status_text.text("✅ Generation complete!")
        st.success(f"Successfully generated {num_docs} document(s)!")

        # Create download section
        st.divider()
        st.header("📥 Download")

        if num_docs == 1:
            # Single file download
            with open(generated_files[0], 'rb') as f:
                st.download_button(
                    label=f"⬇️ Download {os.path.basename(generated_files[0])}",
                    data=f.read(),
                    file_name=os.path.basename(generated_files[0]),
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            # Multiple files - create ZIP
            zip_buffer = create_zip_file(generated_files)
            zip_filename = f"{doc_type_short.lower()}_batch_{timestamp}.zip"

            st.download_button(
                label=f"⬇️ Download All ({num_docs} files) as ZIP",
                data=zip_buffer,
                file_name=zip_filename,
                mime="application/zip",
                use_container_width=True
            )

        # Metadata download
        if include_metadata:
            csv_data = create_metadata_csv(metadata)
            st.download_button(
                label="📊 Download Metadata (CSV)",
                data=csv_data,
                file_name=f"metadata_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )

        # Display summary
        with st.expander("📋 Generation Summary"):
            st.write(f"**Document Type:** {doc_type}")
            st.write(f"**Quantity:** {num_docs}")
            st.write(f"**Generated at:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(f"**Files:**")
            for f in generated_files:
                st.write(f"- {os.path.basename(f)}")

    # Information footer
    st.divider()
    with st.expander("ℹ️ How to Use This App"):
        st.write("""
        ### Purpose
        This application generates fake documents that mimic real utility bills, telecom bills, bank statements,
        tax certificates, and employment documents. Use these documents to:
        - Benchmark your AI fraud detection system
        - Test document verification algorithms
        - Train machine learning models
        - Evaluate OCR accuracy

        ### Document Quality
        All documents are generated with consistent, high-quality output that closely mimics authentic documents.
        This allows you to test your fraud detection system's ability to identify fake documents based on
        subtle inconsistencies or other detection methods.

        ### Best Practices
        1. Use the metadata CSV to track which documents are fake in your test dataset
        2. Test various document types to ensure comprehensive coverage
        3. Combine with real documents (if available) for comprehensive testing
        4. Generate multiple batches to test consistency of your detection system

        ### Ethical Use
        - ✅ Use for testing and benchmarking fraud detection systems
        - ✅ Use for educational and research purposes
        - ✅ Use for improving document security
        - ❌ Do not use for fraud or deception
        - ❌ Do not distribute as genuine documents
        """)

    with st.expander("🔧 Technical Details"):
        st.write("""
        ### Generated Document Features

        **MERALCO Bills:**
        - Authentic-looking layout and branding
        - Realistic consumption data and graphs
        - Proper charge breakdown (generation, transmission, etc.)
        - Environmental impact section
        - Payment instructions and barcodes

        **Maynilad Water Bills:**
        - Contract account and meter information
        - Water consumption data and history
        - Detailed billing breakdown
        - FCDA and environmental charges
        - Payment history section

        **Globe Telecom Bills:**
        - Account and mobile number details
        - Plan information and data usage
        - VAT breakdown
        - Globe branding and colors
        - Payment channel listings

        **BPI Bank Statements:**
        - Professional bank statement format
        - Realistic transaction history
        - Running balance calculations
        - Account summary
        - BPI branding elements

        **BIR Tax Exemption Certificates:**
        - Official BIR Form 2333-A format
        - Certificate number and TIN
        - Organization details and CDA registration
        - Complete tax exemption list
        - Regional Director signature
        - 5-year validity period

        **Certificate of Employment:**
        - Professional company letterhead
        - Employee and position information
        - Salary and benefits breakdown
        - Employment dates and probation period
        - HR Director signature
        - Offer letter format

        ### Document Characteristics
        All documents are generated with realistic details including:
        - Authentic formatting and layouts
        - Realistic calculations and amounts
        - Appropriate branding and logos
        - Consistent dates and information
        """)

if __name__ == "__main__":
    main_page()
