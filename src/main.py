"""
SourceMatch - Main Entry Point
"""

import os
from datetime import datetime
from ocr_engine import OCREngine
from extractor import NumberExtractor


def run_day2_pipeline(source_folder: str, output_dir: str,
                      tesseract_path: str = None, poppler_path: str = None):
    """
    Day 2 Pipeline:
    1. OCR all PDFs in the source folder (or load existing text)
    2. Extract unique numbers from every document
    3. Print a clear summary
    """
    print("=" * 70)
    print("SourceMatch — Day 2: Numerical Extraction Pipeline")
    print("=" * 70)
    print(f"Start time : {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"Source     : {source_folder}")
    print(f"Output     : {output_dir}\n")

    # ---------- Step 1: OCR ----------
    engine = OCREngine(
        tesseract_path=tesseract_path,
        poppler_path=poppler_path,
        dpi=200
    )

    print("STAGE 1: Running OCR on source PDFs")
    print("-" * 70)
    ocr_results = engine.ocr_folder(source_folder, output_dir=output_dir)

    if not ocr_results:
        print("No documents processed. Exiting.")
        return

    # ---------- Step 2: Extract Numbers ----------
    print("\nSTAGE 2: Extracting numerical data")
    print("-" * 70)

    extractor = NumberExtractor(min_value=1)  # ignore 0 if desired
    summary = extractor.summary(ocr_results)

    print(f"\nDocuments processed        : {summary['total_documents']}")
    print(f"Total unique numbers found : {summary['total_unique_numbers']:,}")

    print("\nNumbers per document:")
    for name, count in summary["numbers_per_document"].items():
        print(f"  • {name[:55]:<55} {count:>5} numbers")

    # ---------- Step 3: Save extraction summary ----------
    summary_path = os.path.join(output_dir, "extraction_summary.txt")
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write("SourceMatch — Numerical Extraction Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated : {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n")
        f.write(f"Documents : {summary['total_documents']}\n")
        f.write(f"Unique numbers across all files : {summary['total_unique_numbers']}\n\n")

        f.write("Per document counts:\n")
        for name, count in summary["numbers_per_document"].items():
            f.write(f"  {name}: {count}\n")

        f.write("\nAll unique numbers:\n")
        f.write(", ".join(summary["all_unique_numbers"]))

    print(f"\nSummary saved → {summary_path}")
    print("\n" + "=" * 70)
    print("Day 2 pipeline completed successfully.")
    print("=" * 70)

    return summary


if __name__ == "__main__":
    # ========== CONFIGURE THESE PATHS ==========
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"

    SOURCE_FOLDER = r"C:\Users\padma\OneDrive\Desktop\Anjuman\her office work august 28\Annual reports-20260804T103947Z-1-001\Annual reports"
    OUTPUT_DIR = r"C:\Users\padma\Documents\SourceMatch_OCR_Output"
    # ===========================================

    run_day2_pipeline(
        source_folder=SOURCE_FOLDER,
        output_dir=OUTPUT_DIR,
        tesseract_path=TESSERACT_PATH,
        poppler_path=POPPLER_PATH
    )
