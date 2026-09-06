# SourceMatch

**Verify the accuracy of compiled data against original scanned documents.**

SourceMatch is an open-source tool that answers one critical question:

> How accurately does a compiled Excel or PDF reflect the original source documents?

Built for analysts, auditors, researchers, and organizations working with scanned institutional reports.

---

## Status

| Day | Module | Status |
|-----|--------|--------|
| 1 | Multi-PDF OCR Engine | ✅ Complete |
| 2 | Numerical Data Extraction | ✅ Complete |
| 3 | Comparison Engine | ✅ Complete |
| 4 | Professional Reporting | ✅ Complete |
| 5 | Command-Line Interface | ✅ Complete |
| 6 | Streamlit Web Interface | ✅ Complete |
| 7 | UI Polish & Improvements | ✅ Complete |
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
- Polished web interface (Streamlit)

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
│   └── streamlit_app.py
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

### Web Interface (Recommended)

```bash
cd app
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

1. Upload one or more original scanned PDFs
2. Upload the compiled target PDF
3. Click **Run Accuracy Audit**
4. Review results and download reports

### Command Line Interface

```bash
cd src
python cli.py --source "path/to/original_pdfs" --target "path/to/compiled.pdf"
```

```bash
python cli.py --help
```

### Quick local testing

```bash
cd src
python main.py
```

---

## Output

- OCR text files for each source PDF
- `SourceMatch_Audit_Report.xlsx`
  - Summary sheet with accuracy
  - Missing Numbers
  - Extra Numbers
  - Matched Numbers
- `SourceMatch_Audit_Report.txt`

---

## Accuracy Formula

```
Match Rate = (Matched Numbers / Total Unique Numbers in Source) × 100
```

---

## License

MIT License
