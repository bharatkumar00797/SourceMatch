# SourceMatch — Development Plan

## Goal

Build a working tool that compares original scanned PDFs against a compiled Excel/PDF and produces a clear accuracy audit report.

---

## 8-Day Build Cycle

| Day | Focus | Status |
|-----|-------|--------|
| 1 | Project setup + Multi-PDF OCR pipeline | ✅ Complete |
| 2 | Numerical data extraction engine | ✅ Complete |
| 3 | Comparison logic (match / missing / extra) | ✅ Complete |
| 4 | Accuracy calculation + Excel & text reporting | ✅ Complete |
| 5 | Professional command-line interface | ✅ Complete |
| 6 | Streamlit web interface (basic) | ✅ Complete |
| 7 | UI polish and usability improvements | ✅ Complete |
| 8 | Final documentation and project polish | ✅ Complete |

---

## Architecture Overview

```
Source PDFs (scanned)
        ↓
   OCR Engine (ocr_engine.py)
        ↓
Number Extractor (extractor.py)
        ↓
   Comparator (comparator.py)  ←  Target compiled PDF
        ↓
   Reporter (reporter.py)
        ↓
 Excel + Text Audit Reports
```

---

## Key Design Decisions

- **OCR text is cached** on disk so re-runs skip already processed files.
- **Numbers are normalized** (commas removed, decimals standardized) before comparison.
- **Match Rate** is always calculated against the source (original documents) as the ground truth.
- **CLI and Web UI** share the same core modules — no duplicated logic.

---

## Future Improvements

- Image preprocessing (deskew, contrast) before OCR
- Per-document accuracy breakdown
- Support for Excel (.xlsx) as target input
- Configurable paths via a settings file
- Multi-language OCR support
