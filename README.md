# SourceMatch

**Verify the accuracy of compiled data against original scanned documents.**

SourceMatch is an open-source tool designed to answer one critical question:

> How accurately does a compiled Excel or PDF reflect the original source documents?

It is built for analysts, auditors, researchers, and organizations that work with scanned institutional reports (annual reports, financial statements, activity reports, etc.).

---

## The Problem

Many organizations maintain compiled datasets (Excel / summary PDFs) that are created from original scanned documents. Over time, questions arise:

- How much of the original data is actually present in the compiled version?
- Which numbers are missing?
- What extra values were introduced?
- What is the overall match rate?

Manual verification is slow and error-prone. SourceMatch automates this process.

---

## What SourceMatch Does

1. Accepts multiple original scanned PDFs (source of truth)
2. Accepts one compiled Excel or PDF file
3. Performs OCR on scanned documents
4. Extracts numerical data points
5. Calculates Match Rate and Accuracy
6. Identifies missing and extra values
7. Generates clear audit reports (Excel + summary)

---

## Key Features

- Multi-PDF OCR support
- Numerical data extraction and comparison
- Match Rate / Accuracy calculation
- Missing & Extra values detection
- Clean Excel and text reports
- Designed for real institutional documents

---

## Tech Stack

- Python 3.12+
- `pdfplumber` — text extraction from clean PDFs
- `pdf2image` + Tesseract OCR — scanned document processing
- `openpyxl` — Excel report generation
- `python-docx` — optional Word reports
- Streamlit (planned) — simple web interface

---

## Project Structure

```
SourceMatch/
│
├── README.md
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── ocr_engine.py
│   ├── extractor.py
│   ├── comparator.py
│   ├── reporter.py
│   └── main.py
├── app/                  # Streamlit interface (Day 6-8)
├── reports/               # Generated output
└── sample_data/           # Optional sample files
```

---

## 8-Day Development Plan

| Day | Focus |
|-----|-------|
| 1 | Project setup + OCR pipeline for multiple PDFs |
| 2 | Numerical data extraction engine |
| 3 | Core comparison logic (match / missing / extra) |
| 4 | Accuracy calculation + detailed reporting |
| 5 | End-to-end CLI tool |
| 6 | Streamlit web interface (basic) |
| 7 | Polish reports + UI improvements |
| 8 | Documentation, final testing, GitHub polish |

---

## Quick Start (Coming Soon)

```bash
git clone https://github.com/bharatkumar00797/SourceMatch.git
cd SourceMatch
pip install -r requirements.txt
python src/main.py
```

---

## Status

Currently under active development (8-day build cycle).

---

## License

MIT License
