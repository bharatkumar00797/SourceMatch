# SourceMatch — 8-Day Development Plan

## Goal
Build a working tool that compares original scanned PDFs against a compiled Excel/PDF and produces a clear accuracy report.

---

### Day 1 — Foundation
- Finalize project structure
- Set up OCR pipeline for multiple PDFs
- Save intermediate OCR text files
- Basic logging

### Day 2 — Data Extraction
- Robust number extraction from OCR text
- Clean and normalize numbers
- Handle common OCR errors (O vs 0, etc. where possible)

### Day 3 — Comparison Engine
- Match numbers between source and target
- Identify missing values
- Identify extra values
- Calculate raw match statistics

### Day 4 — Accuracy & Reporting
- Official Accuracy / Match Rate formula
- Generate Excel report
- Generate summary text report
- Add basic statistics (total source numbers, matched, missing, extra)

### Day 5 — CLI Tool
- Complete command-line interface
- Accept folder of source PDFs + one target file
- End-to-end run producing final reports

### Day 6 — Web Interface (Basic)
- Streamlit app
- File upload for source PDFs and target file
- Show accuracy result and summary

### Day 7 — Polish
- Better UI layout
- Download buttons for reports
- Per-file breakdown (if time allows)
- Error handling improvements

### Day 8 — Finalization
- README polish
- Code cleanup
- Example usage
- Final testing
- GitHub presentation
