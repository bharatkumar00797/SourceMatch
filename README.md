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
| 6–7 | Streamlit Web Interface | Upcoming |
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

---

## Project Structure

```
SourceMatch/
│
├── src/
│   ├── ocr_engine.py      ✅
│   ├── extractor.py       ✅
│   ├── comparator.py      ✅
│   ├── reporter.py        ✅
│   ├── cli.py             ✅ Day 5
│   └── main.py            (quick local testing)
├── app/                   ← Streamlit (Day 6-7)
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

### Professional CLI (Recommended)

```bash
cd src

python cli.py --source "path/to/original_pdfs" --target "path/to/compiled.pdf"
```

#### Full options

```bash
python cli.py \
  --source "./original_reports" \
  --target "./compiled_data.pdf" \
  --output "./audit_output" \
  --tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe" \
  --poppler "C:\poppler\Library\bin" \
  --dpi 200 \
  --min-value 1
```

#### View help

```bash
python cli.py --help
```

### Quick local testing

```bash
python main.py
```
(Uses hard-coded paths — edit the file to change them.)

---

## Output

After a successful run you will get:

- OCR text files for each source PDF
- `reports/SourceMatch_Audit_Report.xlsx`
  - Summary sheet with accuracy
  - Missing Numbers
  - Extra Numbers
  - Matched Numbers
- `reports/SourceMatch_Audit_Report.txt`

---

## Accuracy Formula

```
Match Rate = (Matched Numbers / Total Unique Numbers in Source) × 100
```

---

## License

MIT License
