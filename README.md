# Fake Docs Generator

A Streamlit-based application for generating realistic fake documents to benchmark AI fraud detection systems.

## ⚠️ Disclaimer

**FOR TESTING PURPOSES ONLY**

This application generates fake documents for:
- ✅ Testing and benchmarking fraud detection systems
- ✅ Educational and research purposes
- ✅ Improving document security

**DO NOT USE FOR:**
- ❌ Fraud or deception
- ❌ Distributing as genuine documents
- ❌ Any malicious purposes

## Features

### Supported Document Types

1. **MERALCO Bills** - Philippine electricity bills
   - Realistic customer information
   - Billing period and consumption data
   - Detailed charge breakdown
   - Consumption graphs
   - Environmental impact section
   - MERALCO branding and logo

2. **Maynilad Water Bills** - Water utility bills
   - Contract account and meter information
   - Water consumption data and history
   - Detailed billing breakdown
   - FCDA and environmental charges
   - Payment history section

3. **Globe Telecom Bills** - Mobile/telecom bills
   - Account and mobile number details
   - Plan information and data usage
   - VAT breakdown
   - Globe branding and colors
   - Payment channel listings

4. **BPI Bank Statements** - Bank of the Philippine Islands statements
   - Account holder information
   - Transaction history with running balance
   - Account summary
   - BPI branding elements

5. **BIR Tax Exemption Certificates** - Bureau of Internal Revenue certificates
   - Official BIR Form 2333-A format
   - Certificate number and organization details
   - Tax Identification Number (TIN)
   - CDA registration information
   - Complete list of 8 tax exemptions
   - 5-year validity period
   - Regional Director signature

### Realism Levels

- **High**: Maximum realism with only subtle inconsistencies (e.g., minor calculation errors)
- **Medium**: Moderate realism with some noticeable errors
- **Low**: Obvious fakes with clear red flags

### Additional Features

- Batch generation (1-50 documents)
- ZIP download for multiple files
- Metadata CSV export with generation parameters
- Progress tracking
- Configurable realism levels

## Installation

### Prerequisites

- Python 3.12 or higher
- `uv` package manager (recommended) or `pip`

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd fake-docs
```

2. Install dependencies:

Using `uv`:
```bash
uv sync
```

Using `pip`:
```bash
pip install -e .
```

## Usage

### Running the Application

Start the Streamlit app:

```bash
streamlit run main.py
```

Or with `uv`:
```bash
uv run streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

### Using the Web Interface

1. **Select Document Type**: Choose between MERALCO Bill or BPI Bank Statement
2. **Set Realism Level**: Use the sidebar slider (Low/Medium/High)
3. **Choose Quantity**: Select how many documents to generate (1-50)
4. **Generate**: Click the "Generate Documents" button
5. **Download**: Download individual files or ZIP archives

### Metadata

When enabled, a CSV file is generated with:
- Filename
- Document type
- Realism level
- Generation timestamp

Use this metadata to track which documents should be flagged as fake in your testing.

## Project Structure

```
fake-docs/
├── main.py                      # Streamlit application
├── generators/
│   ├── __init__.py
│   ├── base_generator.py        # Shared utilities
│   ├── meralco_generator.py     # MERALCO bill generator
│   └── bpi_generator.py         # BPI statement generator
├── assets/
│   └── meralco_logo.png         # MERALCO logo
├── outputs/                     # Generated PDFs (gitignored)
├── .streamlit/
│   └── config.toml              # Streamlit configuration
├── pyproject.toml               # Python dependencies
└── README.md
```

## Deployment

### Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repository
4. The app will use the configuration in `.streamlit/config.toml`

### Docker (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install -e .

EXPOSE 8501

CMD ["streamlit", "run", "main.py"]
```

Build and run:
```bash
docker build -t fake-docs .
docker run -p 8501:8501 fake-docs
```

## Development

### Adding New Document Types

1. Create a new generator in `generators/` (e.g., `new_doc_generator.py`)
2. Inherit from `DocumentGenerator` base class
3. Implement the generation logic
4. Export the generator function in `generators/__init__.py`
5. Add the document type to `main.py`

### Customizing Realism Levels

Adjust the fraud indicators in each generator:
- **High realism**: Subtle calculation errors, minor date variations
- **Medium realism**: Moderate inconsistencies, some formatting issues
- **Low realism**: Obvious errors, missing information, clear red flags

## Dependencies

- **streamlit**: Web application framework
- **faker**: Generate fake data (names, addresses)
- **reportlab**: PDF generation
- **matplotlib**: Consumption graphs
- **pillow**: Image processing
- **qrcode**: QR code generation

## License

This project is for educational and testing purposes only.

## Contributing

Contributions are welcome! Please ensure any new document generators:
1. Include configurable realism levels
2. Generate realistic-looking documents
3. Follow the existing code structure
4. Include appropriate fraud indicators

## Support

For issues or questions, please open an issue on the GitHub repository.
