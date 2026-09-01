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

## Current Status

**Day 1 Complete** — Multi-PDF OCR Engine is ready.

You can already run OCR on a full folder of scanned PDFs and save clean text files.

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
│   ├── __init__.py
│   ├── ocr_engine.py      ← Day 1 (ready)
│   ├── main.py
│   ├── extractor.py      ← Day 2
│   ├── comparator.py     ← Day 3
│   └── reporter.py       ← Day 4
├── app/                  ← Streamlit UI (Day 6-7)
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

1. **Tesseract OCR**  
   Download: https://github.com/UB-Mannheim/tesseract/wiki

2. **Poppler** (for pdf2image)  
   Windows builds are available on GitHub.

After installing, open `src/main.py` or `src/ocr_engine.py` and update these two paths:

```python
TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
POPPLER_PATH   = r"C:\poppler\Library\bin"
```

---

## Usage (Day 1)

```bash
cd src
python main.py
```

This will:
- Scan the source folder for PDFs
- Run OCR on each file
- Save individual `.txt` files
- Skip files that were already processed

---

## 8-Day Plan

| Day | Focus | Status |
|-----|-------|--------|
| 1 | Multi-PDF OCR Engine | ✅ Complete |
| 2 | Numerical Data Extraction | Upcoming |
| 3 | Comparison Engine | Upcoming |
| 4 | Accuracy + Reporting | Upcoming |
| 5 | Complete CLI Tool | Upcoming |
| 6 | Streamlit Web Interface | Upcoming |
| 7 | Polish & Improvements | Upcoming |
| 8 | Final Documentation | Upcoming |

---

## License

MIT License
