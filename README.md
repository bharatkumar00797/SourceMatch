# SourceMatch

**Verify the accuracy of compiled data against original scanned documents.**

SourceMatch is an open-source tool that answers one practical question:

> How accurately does a compiled Excel or PDF reflect the original source documents?

It is designed for analysts, auditors, researchers, and organizations that work with scanned institutional reports (annual reports, financial statements, activity reports, and similar documents).

---

## Why SourceMatch?

Many teams maintain a compiled dataset created from original scanned PDFs. Over time it becomes difficult to know:

- How much of the original data is still present?
- Which numbers are missing?
- What extra values were introduced during compilation?
- What is the overall match rate?

Manual checking is slow and error-prone. SourceMatch automates the verification and produces clear audit reports.

---

## Features

- OCR support for multiple scanned PDFs
- Robust numerical data extraction and normalization
- Match / Missing / Extra value detection
- Match Rate (Accuracy) calculation
- Professional Excel and text audit reports
- Command-line interface
- Web interface built with Streamlit

---

## Project Structure

```
SourceMatch/
│
├── app/
│   └── streamlit_app.py      # Web interface
│
├── src/
│   ├── ocr_engine.py         # Multi-PDF OCR
│   ├── extractor.py          # Number extraction
│   ├── comparator.py         # Match / Missing / Extra logic
│   ├── reporter.py           # Excel + text reports
│   ├── cli.py                # Command-line interface
│   └── main.py               # Quick local testing entry point
│
├── docs/
│   └── development_plan.md
│
├── requirements.txt
├── LICENSE
└── README.md
```

---

## Setup

```bash
git clone https://github.com/bharatkumar00797/SourceMatch.git
cd SourceMatch
pip install -r requirements.txt
```

### System Dependencies

| Dependency | Purpose | Link |
|------------|---------|------|
| **Tesseract OCR** | Text recognition from images | [UB Mannheim builds](https://github.com/UB-Mannheim/tesseract/wiki) |
| **Poppler** | PDF → image conversion | Required by `pdf2image` on Windows |

After installing, note the paths to `tesseract.exe` and the Poppler `bin` folder. You will need them for the CLI or web interface.

---

## Usage

### Option 1 — Web Interface (Recommended)

```bash
cd app
streamlit run streamlit_app.py
```

Open the URL shown in the terminal (usually `http://localhost:8501`).

1. Upload one or more original scanned PDFs
2. Upload the compiled target PDF
3. Click **Run Accuracy Audit**
4. Review the Match Rate and download the reports

### Option 2 — Command Line

```bash
cd src

python cli.py --source "path/to/original_pdfs" --target "path/to/compiled.pdf"
```

Common options:

```bash
python cli.py \
  --source "./original_reports" \
  --target "./compiled_data.pdf" \
  --output "./audit_output" \
  --tesseract "C:\Program Files\Tesseract-OCR\tesseract.exe" \
  --poppler "C:\poppler\Library\bin" \
  --dpi 200
```

View all options:

```bash
python cli.py --help
```

### Option 3 — Quick local test

Edit the paths inside `src/main.py`, then run:

```bash
cd src
python main.py
```

---

## Output

After a successful run you receive:

| File | Contents |
|------|----------|
| `SourceMatch_Audit_Report.xlsx` | Summary sheet with accuracy, plus sheets for Missing, Extra, and Matched numbers |
| `SourceMatch_Audit_Report.txt` | Clean text version of the same audit |
| Individual `.txt` files | OCR text for each source PDF (cached for faster re-runs) |

---

## Accuracy Formula

```
Match Rate = (Matched Numbers / Total Unique Numbers in Source) × 100
```

- **Source** = original scanned documents (treated as ground truth)
- **Matched** = numbers found in both source and compiled file
- **Missing** = numbers present in source but absent from compiled file
- **Extra** = numbers present only in the compiled file

---

## Development Timeline

This project was built over an 8-day focused cycle:

1. OCR engine for multiple PDFs
2. Numerical extraction and normalization
3. Comparison engine
4. Professional reporting
5. Command-line interface
6. Streamlit web interface
7. UI polish
8. Final documentation and release preparation

See [docs/development_plan.md](docs/development_plan.md) for details.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

Built by [Bharatkumar Chandvani](https://github.com/bharatkumar00797)
