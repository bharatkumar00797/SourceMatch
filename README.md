# SourceMatch

**Verify the accuracy of compiled data against original scanned documents.**

SourceMatch is an open-source tool designed to answer one critical question:

> How accurately does a compiled Excel or PDF reflect the original source documents?

It is built for analysts, auditors, researchers, and organizations that work with scanned institutional reports (annual reports, financial statements, activity reports, etc.).

---

## Current Status

| Day | Module | Status |
|-----|--------|--------|
| 1 | Multi-PDF OCR Engine | ✅ Complete |
| 2 | Numerical Data Extraction | ✅ Complete |
| 3 | Comparison Engine | Upcoming |
| 4 | Accuracy + Reporting | Upcoming |
| 5 | Complete CLI Tool | Upcoming |
| 6–7 | Streamlit Web Interface | Upcoming |
| 8 | Final Documentation | Upcoming |

---

## The Problem

Many organizations maintain compiled datasets (Excel / summary PDFs) created from original scanned documents. Over time it becomes difficult to answer:

- How much of the original data is present in the compiled version?
- Which numbers are missing?
- What extra values were introduced?
- What is the overall match rate?

SourceMatch automates this verification.

---

## What It Does

1. Accepts multiple original scanned PDFs
2. Accepts one compiled Excel or PDF file
3. Performs OCR on scanned documents
4. Extracts and normalizes numerical data points
5. Calculates Match Rate and Accuracy
6. Identifies missing and extra values
7. Generates clear audit reports

---

## Project Structure

```
SourceMatch/
│
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   └── development_plan.md
├── src/
│   ├── ocr_engine.py      ✅ Day 1
│   ├── extractor.py       ✅ Day 2
│   ├── main.py
│   ├── comparator.py     ← Day 3
│   └── reporter.py       ← Day 4
├── app/                  ← Streamlit (Day 6-7)
└── reports/
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
- **Poppler** (required by pdf2image)

Update the paths inside `src/main.py`:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH   = r"C:\poppler\Library\bin"
```

---

## Usage (Current)

```bash
cd src
python main.py
```

This will:

1. Run OCR on all PDFs in the source folder (skips already processed files)
2. Extract every unique number from the OCR text
3. Show a per-document summary
4. Save an extraction summary file

---

## Day 2 Highlights

The new `NumberExtractor` class:

- Detects integers and decimals (including thousand separators)
- Normalizes numbers (`1,234.50` → `1234.5`)
- Removes duplicates while preserving order
- Supports optional min/max filtering
- Can process multiple documents at once
- Produces a clean summary for later comparison

---

## License

MIT License
