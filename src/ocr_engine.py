"""
SourceMatch - OCR Engine
Handles conversion of scanned PDFs to text using Tesseract OCR.
"""

import os
from pathlib import Path
from pdf2image import convert_from_path
import pytesseract
from datetime import datetime


class OCREngine:
    def __init__(self, tesseract_path: str = None, poppler_path: str = None, dpi: int = 200):
        """
        Initialize the OCR engine.

        Args:
            tesseract_path: Path to tesseract executable (required on Windows)
            poppler_path: Path to poppler bin folder (required on Windows)
            dpi: Resolution for PDF to image conversion (higher = better quality, slower)
        """
        self.dpi = dpi
        self.poppler_path = poppler_path

        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path

    def ocr_single_pdf(self, pdf_path: str, output_txt_path: str = None) -> str:
        """
        Perform OCR on a single PDF file.

        Args:
            pdf_path: Full path to the PDF file
            output_txt_path: Optional path to save the extracted text

        Returns:
            Extracted text as a string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        print(f"  Converting PDF to images (DPI={self.dpi})...")

        convert_kwargs = {"dpi": self.dpi}
        if self.poppler_path:
            convert_kwargs["poppler_path"] = self.poppler_path

        images = convert_from_path(pdf_path, **convert_kwargs)
        total_pages = len(images)

        all_text = []
        for i, image in enumerate(images, start=1):
            print(f"  OCR page {i}/{total_pages}", end="\r")
            text = pytesseract.image_to_string(image, lang="eng")
            all_text.append(f"\n\n----- PAGE {i} -----\n\n{text}")

        full_text = "".join(all_text)
        print(f"\n  Completed: {total_pages} pages extracted")

        if output_txt_path:
            os.makedirs(os.path.dirname(output_txt_path), exist_ok=True)
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"  Saved text → {output_txt_path}")

        return full_text

    def ocr_folder(self, folder_path: str, output_dir: str = None) -> dict:
        """
        Perform OCR on all PDF files inside a folder.

        Args:
            folder_path: Path to folder containing PDFs
            output_dir: Directory to save individual .txt files (optional)

        Returns:
            Dictionary {pdf_filename: extracted_text}
        """
        if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Folder not found: {folder_path}")

        pdf_files = sorted([
            f for f in os.listdir(folder_path)
            if f.lower().endswith(".pdf")
        ])

        if not pdf_files:
            print("No PDF files found in the folder.")
            return {}

        print(f"\nFound {len(pdf_files)} PDF file(s)\n")
        results = {}

        for idx, pdf_name in enumerate(pdf_files, start=1):
            print(f"[{idx}/{len(pdf_files)}] {pdf_name}")
            pdf_path = os.path.join(folder_path, pdf_name)

            txt_path = None
            if output_dir:
                txt_name = Path(pdf_name).stem + ".txt"
                txt_path = os.path.join(output_dir, txt_name)

                # Skip if already processed
                if os.path.exists(txt_path):
                    print("  → Using previously saved OCR text")
                    with open(txt_path, "r", encoding="utf-8") as f:
                        results[pdf_name] = f.read()
                    continue

            try:
                text = self.ocr_single_pdf(pdf_path, output_txt_path=txt_path)
                results[pdf_name] = text
            except Exception as e:
                print(f"  ERROR: {e}")
                results[pdf_name] = ""

        return results


def main_demo():
    """Simple demo / test run"""
    print("=" * 60)
    print("SourceMatch — OCR Engine (Day 1)")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%d %B %Y, %I:%M %p')}\n")

    # ========== UPDATE THESE PATHS ==========
    TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    POPPLER_PATH = r"C:\poppler\Library\bin"

    SOURCE_FOLDER = r"C:\Users\padma\OneDrive\Desktop\Anjuman\her office work august 28\Annual reports-20260804T103947Z-1-001\Annual reports"
    OUTPUT_DIR = r"C:\Users\padma\Documents\SourceMatch_OCR_Output"
    # ========================================

    engine = OCREngine(
        tesseract_path=TESSERACT_PATH,
        poppler_path=POPPLER_PATH,
        dpi=200
    )

    results = engine.ocr_folder(SOURCE_FOLDER, output_dir=OUTPUT_DIR)

    print("\n" + "=" * 60)
    print(f"OCR complete. Processed {len(results)} file(s).")
    print(f"Text files saved in: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main_demo()
