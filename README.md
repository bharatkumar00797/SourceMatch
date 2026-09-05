# SourceMatch

**Verify the accuracy of compiled data against original scanned documents.**

SourceMatch is an open-source tool that answers one critical question:

> How accurately does a compiled Excel or PDF reflect the original source documents?

Built for analysts, auditors, researchers, and organizations working with scanned institutional reports.

---

## Current Status

| Day | Module | Status |
|-----|--------|--------|
| 1 | Multi-PDF OCR Engine | ✅ Complete |
| 2 | Numerical Data Extraction | ✅ Complete |
| 3 | Comparison Engine | ✅ Complete |
| 4 | Professional Reporting | ✅ Complete |
| 5 | Command-Line Interface | ✅ Complete |
| 6 | Streamlit Web Interface | ✅ Complete (Basic) |
| 7 | UI Polish & Improvements | Upcoming |
| 8 | Final Documentation | Upcoming |

---

## Features

- OCR multiple scanned PDFs
- Extract and normalize numerical data
- Compare source documents against a compiled file
- Calculate Match Rate / Accuracy
- Identify missing and extra values
- Generate professional Excel + text audit reports
- Clean command-line interface
- **Web interface** (Streamlit)

---

## Project Structure

```
SourceMatch/
│
├── src/
│   ├── ocr_engine.py
│   ├── extractor.py
│   ├── comparator.py
│   ├── reporter.py
│   ├── cli.py
│   └── main.py
├── app/
│   └── streamlit_app.py    ✅ Day 6
└── docs/
```

---

## Setup

```bash
git clone https://github.com/bharatkumar00797/SourceMatch.git
cd SourceMatch
pip install -r requirements.txt
```

### System Dependencies

- **Tesseract OCR** → https://github.com/UB-Mannheim/tesseract/wiki
- **Poppler** (required by pdf2image on Windows)

---

## Usage

### 1. Web Interface (Recommended for most users)

```bash
cd app
streamlit run streamlit_app.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

- Upload one or more original scanned PDFs
- Upload the compiled target PDF
- Click **Run Accuracy Audit**
- View results and download reports

### 2. Command Line Interface

```bash
cd src

python cli.py --source "path/to/original_pdfs" --target "path/to/compiled.pdf"
```

Full options:

```bash
python cli.py --help
```

### 3. Quick local testing

```bash
cd src
python main.py
```

---

## Output

- OCR text files for each source PDF
- `SourceMatch_Audit_Report.xlsx` (Summary + Missing + Extra + Matched)
- `SourceMatch_Audit_Report.txt`

---

## Accuracy Formula

```
Match Rate = (Matched Numbers / Total Unique Numbers in Source) × 100
```

---

## License

MIT License
