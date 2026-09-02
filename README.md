# SourceMatch

**Verify the accuracy of compiled data against original scanned documents.**

SourceMatch is an open-source tool designed to answer one critical question:

> How accurately does a compiled Excel or PDF reflect the original source documents?

It is built for analysts, auditors, researchers, and organizations that work with scanned institutional reports.

---

## Current Status

| Day | Module | Status |
|-----|--------|--------|
| 1 | Multi-PDF OCR Engine | ✅ Complete |
| 2 | Numerical Data Extraction | ✅ Complete |
| 3 | Comparison Engine | ✅ Complete |
| 4 | Accuracy + Reporting | Upcoming |
| 5 | Complete CLI Tool | Upcoming |
| 6–7 | Streamlit Web Interface | Upcoming |
| 8 | Final Documentation | Upcoming |

---

## The Problem

Organizations often maintain compiled datasets created from original scanned documents. It is difficult to know:

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
4. Extracts and normalizes numerical data
5. Calculates Match Rate and Accuracy
6. Identifies missing and extra values
7. Generates clear audit reports

---

## Project Structure

```
SourceMatch/
│
├── src/
│   ├── ocr_engine.py      ✅ Day 1
│   ├── extractor.py       ✅ Day 2
│   ├── comparator.py      ✅ Day 3
│   ├── main.py
│   └── reporter.py        ← Day 4
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

Update paths in `src/main.py`:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH   = r"C:\poppler\Library\bin"
SOURCE_FOLDER  = r"path\to\original\pdfs"
TARGET_PDF     = r"path\to\compiled\file.pdf"
```

---

## Usage (Current — Day 3)

```bash
cd src
python main.py
```

This runs the full pipeline:

1. OCR all source PDFs
2. Extract numbers from source documents
3. Extract numbers from the target compiled file
4. Compare both sets
5. Display Match Rate / Accuracy
6. Save a summary report

---

## Accuracy Formula

```
Match Rate = (Matched Numbers / Total Unique Numbers in Source) × 100
```

---

## Day 3 Highlights

The new `Comparator` class provides:

- Clean separation of matched / missing / extra numbers
- Precise match rate calculation
- Structured `ComparisonResult` object
- Ready for advanced reporting (Day 4)

---

## License

MIT License
