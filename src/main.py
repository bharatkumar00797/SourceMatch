"""
SourceMatch - Main Entry Point

For the professional command-line interface, use:
    python cli.py --source <folder> --target <file>

This file remains as a simple quick-start option with hard-coded paths
for local testing.
"""

import os
from datetime import datetime
from ocr_engine import OCREngine
from extractor import NumberExtractor
from comparator import Comparator
from reporter import Reporter
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def run_full_pipeline(
    source_folder: str,
    target_pdf: str,
    output_dir: str,
    tesseract_path: str = None,
    poppler_path: str = None
):
    print("=" * 70)
    print("SourceMatch — Full Audit Pipeline")
    print("=" * 70)
    print(f"Start time    : {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"Source folder : {source_folder}")
    print(f"Target file   : {target_pdf}")
    print(f"Output dir    : {output_dir}\n")

    os.makedirs(output_dir, exist_ok=True)
    reports_dir = os.path.join(output_dir, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    print("STAGE 1: OCR on original source PDFs")
    print("-" * 70)
    engine = OCREngine(
        tesseract_path=tesseract_path,
        poppler_path=poppler_path,
        dpi=200
    )
    ocr_results = engine.ocr_folder(source_folder, output_dir=output_dir)

    if not ocr_results:
        print("No source documents processed. Exiting.")
        return

    print("\nSTAGE 2: Extracting numbers from source documents")
    print("-" * 70)
    extractor = NumberExtractor(min_value=1)
    source_numbers = extractor.get_all_unique(ocr_results)
    print(f"Unique numbers found in source PDFs: {len(source_numbers):,}")

    print("\nSTAGE 3: Extracting numbers from target (compiled) file")
    print("-" * 70)
    if not os.path.exists(target_pdf):
        print(f"ERROR: Target file not found → {target_pdf}")
        return

    target_text = extract_text_from_pdf(target_pdf)
    target_numbers = extractor.extract_unique(target_text)
    print(f"Unique numbers found in target file: {len(target_numbers):,}")

    print("\nSTAGE 4: Comparing source vs target")
    print("-" * 70)
    comparator = Comparator()
    result = comparator.compare_and_report(
        source_numbers,
        target_numbers,
        title="SourceMatch — Accuracy Report"
    )

    print("\nSTAGE 5: Generating professional audit reports")
    print("-" * 70)
    reporter = Reporter(output_dir=reports_dir)
    paths = reporter.generate_all(
        result,
        source_name=os.path.basename(source_folder),
        target_name=os.path.basename(target_pdf)
    )

    print(f"Excel report → {paths['excel']}")
    print(f"Text report  → {paths['text']}")

    print("\n" + "=" * 70)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print(f"Final Match Rate / Accuracy: {result.match_rate:.2f}%")
    print("=" * 70)

    return result


if __name__ == "__main__":
    print("Note: For the professional CLI, use:  python cli.py --help")
    print("Running with hard-coded paths for quick local testing...\n")

    # ========== CONFIGURE THESE PATHS ==========
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"

    SOURCE_FOLDER = r"C:\Users\padma\OneDrive\Desktop\Anjuman\her office work august 28\Annual reports-20260804T103947Z-1-001\Annual reports"
    TARGET_PDF = r"C:\Users\padma\Downloads\divyajyoti-historical-dataset-v9.pdf"
    OUTPUT_DIR = r"C:\Users\padma\Documents\SourceMatch_OCR_Output"
    # ===========================================

    run_full_pipeline(
        source_folder=SOURCE_FOLDER,
        target_pdf=TARGET_PDF,
        output_dir=OUTPUT_DIR,
        tesseract_path=TESSERACT_PATH,
        poppler_path=POPPLER_PATH
    )
