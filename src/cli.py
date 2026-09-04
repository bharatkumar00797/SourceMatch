"""
SourceMatch - Command Line Interface
Professional CLI entry point for the full audit pipeline.
"""

import argparse
import os
import sys
from datetime import datetime

from ocr_engine import OCREngine
from extractor import NumberExtractor
from comparator import Comparator
from reporter import Reporter
import pdfplumber


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a clean (non-scanned) PDF."""
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    pages.append(text)
    except Exception as e:
        print(f"Error reading target PDF: {e}")
        return ""
    return "\n\n".join(pages)


def run_pipeline(args):
    """Execute the full SourceMatch audit pipeline."""
    print("=" * 70)
    print("SourceMatch — Data Integrity Audit")
    print("=" * 70)
    print(f"Start time     : {datetime.now().strftime('%d %B %Y, %I:%M %p')}")
    print(f"Source folder  : {args.source}")
    print(f"Target file    : {args.target}")
    print(f"Output dir     : {args.output}")
    print()

    # Validate inputs
    if not os.path.isdir(args.source):
        print(f"ERROR: Source folder not found → {args.source}")
        sys.exit(1)

    if not os.path.isfile(args.target):
        print(f"ERROR: Target file not found → {args.target}")
        sys.exit(1)

    os.makedirs(args.output, exist_ok=True)
    reports_dir = os.path.join(args.output, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    # ---------- Stage 1: OCR ----------
    print("STAGE 1: OCR on source PDFs")
    print("-" * 70)
    engine = OCREngine(
        tesseract_path=args.tesseract,
        poppler_path=args.poppler,
        dpi=args.dpi
    )
    ocr_results = engine.ocr_folder(args.source, output_dir=args.output)

    if not ocr_results:
        print("No source documents processed. Exiting.")
        sys.exit(1)

    # ---------- Stage 2: Extract from source ----------
    print("\nSTAGE 2: Extracting numbers from source documents")
    print("-" * 70)
    extractor = NumberExtractor(min_value=args.min_value)
    source_numbers = extractor.get_all_unique(ocr_results)
    print(f"Unique numbers found in source : {len(source_numbers):,}")

    # ---------- Stage 3: Extract from target ----------
    print("\nSTAGE 3: Extracting numbers from target file")
    print("-" * 70)
    target_text = extract_text_from_pdf(args.target)
    if not target_text.strip():
        print("WARNING: No text extracted from target file. It may be scanned.")
        print("         Consider running OCR on the target as well if needed.")

    target_numbers = extractor.extract_unique(target_text)
    print(f"Unique numbers found in target : {len(target_numbers):,}")

    # ---------- Stage 4: Compare ----------
    print("\nSTAGE 4: Comparing source vs target")
    print("-" * 70)
    comparator = Comparator()
    result = comparator.compare_and_report(
        source_numbers,
        target_numbers,
        title="SourceMatch — Accuracy Report"
    )

    # ---------- Stage 5: Reports ----------
    print("\nSTAGE 5: Generating audit reports")
    print("-" * 70)
    reporter = Reporter(output_dir=reports_dir)
    paths = reporter.generate_all(
        result,
        source_name=os.path.basename(args.source.rstrip("\\/")),
        target_name=os.path.basename(args.target)
    )

    print(f"Excel report → {paths['excel']}")
    print(f"Text report  → {paths['text']}")

    print("\n" + "=" * 70)
    print("AUDIT COMPLETED SUCCESSFULLY")
    print(f"Final Match Rate / Accuracy : {result.match_rate:.2f}%")
    print("=" * 70)

    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sourcematch",
        description="SourceMatch — Verify accuracy of compiled data against original scanned documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py --source "./original_pdfs" --target "./compiled.pdf"
  python cli.py -s "./reports" -t "./summary.pdf" -o "./output" --dpi 250
  python cli.py -s "./pdfs" -t "./data.pdf" --tesseract "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
        """
    )

    parser.add_argument(
        "-s", "--source",
        required=True,
        help="Folder containing original scanned PDF files"
    )
    parser.add_argument(
        "-t", "--target",
        required=True,
        help="Compiled Excel/PDF file to verify against the source"
    )
    parser.add_argument(
        "-o", "--output",
        default="./sourcematch_output",
        help="Directory to store OCR text and audit reports (default: ./sourcematch_output)"
    )
    parser.add_argument(
        "--tesseract",
        default=None,
        help="Path to tesseract executable (required on Windows if not in PATH)"
    )
    parser.add_argument(
        "--poppler",
        default=None,
        help="Path to poppler bin folder (required on Windows)"
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=200,
        help="DPI for PDF to image conversion (default: 200)"
    )
    parser.add_argument(
        "--min-value",
        type=float,
        default=1.0,
        help="Ignore numbers smaller than this value (default: 1)"
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    run_pipeline(args)


if __name__ == "__main__":
    main()
