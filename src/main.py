"""
SourceMatch - Main Entry Point
"""

from ocr_engine import OCREngine
from datetime import datetime
import os


def run_ocr_pipeline(source_folder: str, output_dir: str,
                     tesseract_path: str = None, poppler_path: str = None):
    """
    Run the full OCR pipeline on a folder of PDFs.
    """
    print("=" * 65)
    print("SourceMatch — OCR Pipeline")
    print("=" * 65)
    print(f"Start time : {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"Source     : {source_folder}")
    print(f"Output     : {output_dir}\n")

    engine = OCREngine(
        tesseract_path=tesseract_path,
        poppler_path=poppler_path,
        dpi=200
    )

    results = engine.ocr_folder(source_folder, output_dir=output_dir)

    successful = sum(1 for text in results.values() if text.strip())
    print("\n" + "-" * 65)
    print(f"Files processed : {len(results)}")
    print(f"Successful OCR  : {successful}")
    print(f"Failed / Empty  : {len(results) - successful}")
    print("-" * 65)

    return results


if __name__ == "__main__":
    # ========== CONFIGURE THESE PATHS ==========
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"

    SOURCE_FOLDER = r"C:\Users\padma\OneDrive\Desktop\Anjuman\her office work august 28\Annual reports-20260804T103947Z-1-001\Annual reports"
    OUTPUT_DIR = r"C:\Users\padma\Documents\SourceMatch_OCR_Output"
    # ===========================================

    run_ocr_pipeline(
        source_folder=SOURCE_FOLDER,
        output_dir=OUTPUT_DIR,
        tesseract_path=TESSERACT_PATH,
        poppler_path=POPPLER_PATH
    )
