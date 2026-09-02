"""
SourceMatch - Main Entry Point
Day 3: OCR → Extraction → Comparison
"""

import os
from datetime import datetime
from ocr_engine import OCREngine
from extractor import NumberExtractor
from comparator import Comparator
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a clean (non-scanned) PDF using pdfplumber."""
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def run_day3_pipeline(
    source_folder: str,
    target_pdf: str,
    output_dir: str,
    tesseract_path: str = None,
    poppler_path: str = None
):
    """
    Full Day 3 pipeline:
    1. OCR source PDFs (or load existing text)
    2. Extract numbers from source documents
    3. Extract numbers from target (compiled) PDF
    4. Compare and calculate match rate
    """
    print("=" * 70)
    print("SourceMatch — Day 3: Comparison Pipeline")
    print("=" * 70)
    print(f"Start time    : {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"Source folder : {source_folder}")
    print(f"Target file   : {target_pdf}")
    print(f"Output dir    : {output_dir}\n")

    os.makedirs(output_dir, exist_ok=True)

    # ---------- Stage 1: OCR Source PDFs ----------
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

    # ---------- Stage 2: Extract numbers from source ----------
    print("\nSTAGE 2: Extracting numbers from source documents")
    print("-" * 70)
    extractor = NumberExtractor(min_value=1)
    source_numbers = extractor.get_all_unique(ocr_results)
    print(f"Unique numbers found in source PDFs: {len(source_numbers):,}")

    # ---------- Stage 3: Extract numbers from target ----------
    print("\nSTAGE 3: Extracting numbers from target (compiled) file")
    print("-" * 70)

    if not os.path.exists(target_pdf):
        print(f"ERROR: Target file not found → {target_pdf}")
        return

    target_text = extract_text_from_pdf(target_pdf)
    target_numbers = extractor.extract_unique(target_text)
    print(f"Unique numbers found in target file: {len(target_numbers):,}")

    # ---------- Stage 4: Compare ----------
    print("\nSTAGE 4: Comparing source vs target")
    print("-" * 70)

    comparator = Comparator()
    result = comparator.compare_and_report(
        source_numbers,
        target_numbers,
        title="SourceMatch — Accuracy Report"
    )

    # ---------- Stage 5: Save basic results ----------
    report_path = os.path.join(output_dir, "day3_comparison_summary.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("SourceMatch — Day 3 Comparison Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated : {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n\n")
        f.write(f"Source unique numbers : {result.source_total}\n")
        f.write(f"Target unique numbers : {result.target_total}\n")
        f.write(f"Matched               : {result.matched_count}\n")
        f.write(f"Missing in target     : {result.missing_count}\n")
        f.write(f"Extra in target       : {result.extra_count}\n")
        f.write(f"Match Rate / Accuracy : {result.match_rate:.2f}%\n\n")

        f.write("Missing numbers (present in source but not in target):\n")
        f.write(", ".join(result.missing_numbers[:200]))
        if len(result.missing_numbers) > 200:
            f.write(" ... (truncated)")
        f.write("\n\n")

        f.write("Extra numbers (present only in target):\n")
        f.write(", ".join(result.extra_numbers[:200]))
        if len(result.extra_numbers) > 200:
            f.write(" ... (truncated)")

    print(f"\nSummary saved → {report_path}")
    print("\nDay 3 pipeline completed.")
    return result


if __name__ == "__main__":
    # ========== CONFIGURE THESE PATHS ==========
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"

    SOURCE_FOLDER = r"C:\Users\padma\OneDrive\Desktop\Anjuman\her office work august 28\Annual reports-20260804T103947Z-1-001\Annual reports"
    TARGET_PDF = r"C:\Users\padma\Downloads\divyajyoti-historical-dataset-v9.pdf"
    OUTPUT_DIR = r"C:\Users\padma\Documents\SourceMatch_OCR_Output"
    # ===========================================

    run_day3_pipeline(
        source_folder=SOURCE_FOLDER,
        target_pdf=TARGET_PDF,
        output_dir=OUTPUT_DIR,
        tesseract_path=TESSERACT_PATH,
        poppler_path=POPPLER_PATH
    )
