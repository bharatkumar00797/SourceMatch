"""
SourceMatch - Streamlit Web Interface
Upload source PDFs + a compiled file and get an accuracy audit report.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

import streamlit as st
import pdfplumber

# Add src folder to path so we can import our modules
SYS_PATH = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SYS_PATH))

from ocr_engine import OCREngine
from extractor import NumberExtractor
from comparator import Comparator
from reporter import Reporter


# -------------------- Page Config --------------------
st.set_page_config(
    page_title="SourceMatch",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- Sidebar --------------------
st.sidebar.title("SourceMatch")
st.sidebar.markdown("**Data Integrity Auditor**")
st.sidebar.markdown("---")
st.sidebar.markdown(
    "Upload original scanned PDFs and one compiled file. "
    "SourceMatch will calculate how accurately the compiled file matches the originals."
)

st.sidebar.markdown("---")
st.sidebar.subheader("Settings")

dpi = st.sidebar.slider("OCR DPI", min_value=150, max_value=300, value=200, step=50)
min_value = st.sidebar.number_input("Ignore numbers smaller than", min_value=0.0, value=1.0, step=1.0)

tesseract_path = st.sidebar.text_input(
    "Tesseract path (Windows)",
    value=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)
poppler_path = st.sidebar.text_input(
    "Poppler path (Windows)",
    value=r"C:\poppler\Library\bin"
)

st.sidebar.markdown("---")
st.sidebar.caption("Day 6 • SourceMatch")


# -------------------- Main Area --------------------
st.title("SourceMatch")
st.markdown("### Verify compiled data against original scanned documents")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Original Source PDFs")
    source_files = st.file_uploader(
        "Upload one or more scanned PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="source_uploader"
    )

with col2:
    st.subheader("2. Compiled / Target File")
    target_file = st.file_uploader(
        "Upload the compiled Excel or PDF file",
        type=["pdf"],
        accept_multiple_files=False,
        key="target_uploader"
    )

st.markdown("---")

run_button = st.button("Run Accuracy Audit", type="primary", use_container_width=True)


def extract_text_from_pdf_bytes(file_bytes) -> str:
    """Extract text from a clean PDF uploaded via Streamlit."""
    import io
    pages = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


if run_button:
    if not source_files:
        st.error("Please upload at least one original source PDF.")
        st.stop()

    if not target_file:
        st.error("Please upload the compiled target file.")
        st.stop()

    with st.spinner("Running SourceMatch audit... This may take several minutes for scanned PDFs."):

        # Create temporary working directory
        with tempfile.TemporaryDirectory() as temp_dir:
            source_dir = os.path.join(temp_dir, "source")
            output_dir = os.path.join(temp_dir, "output")
            reports_dir = os.path.join(output_dir, "reports")
            os.makedirs(source_dir, exist_ok=True)
            os.makedirs(reports_dir, exist_ok=True)

            # Save uploaded source PDFs to disk
            for uploaded in source_files:
                file_path = os.path.join(source_dir, uploaded.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded.getbuffer())

            # Save target file
            target_path = os.path.join(temp_dir, target_file.name)
            with open(target_path, "wb") as f:
                f.write(target_file.getbuffer())

            progress = st.progress(0, text="Starting OCR...")

            # ---- Stage 1: OCR ----
            try:
                engine = OCREngine(
                    tesseract_path=tesseract_path if tesseract_path.strip() else None,
                    poppler_path=poppler_path if poppler_path.strip() else None,
                    dpi=dpi
                )
                ocr_results = engine.ocr_folder(source_dir, output_dir=output_dir)
            except Exception as e:
                st.error(f"OCR failed: {e}")
                st.stop()

            progress.progress(40, text="Extracting numbers from source documents...")

            if not ocr_results:
                st.error("No text could be extracted from the source PDFs.")
                st.stop()

            # ---- Stage 2 & 3: Extract numbers ----
            extractor = NumberExtractor(min_value=min_value)
            source_numbers = extractor.get_all_unique(ocr_results)

            target_bytes = target_file.getvalue()
            target_text = extract_text_from_pdf_bytes(target_bytes)
            target_numbers = extractor.extract_unique(target_text)

            progress.progress(70, text="Comparing data...")

            # ---- Stage 4: Compare ----
            comparator = Comparator()
            result = comparator.compare(source_numbers, target_numbers)

            progress.progress(85, text="Generating reports...")

            # ---- Stage 5: Reports ----
            reporter = Reporter(output_dir=reports_dir)
            paths = reporter.generate_all(
                result,
                source_name=f"{len(source_files)} source PDF(s)",
                target_name=target_file.name
            )

            progress.progress(100, text="Done!")

            # -------------------- Results Display --------------------
            st.success("Audit completed successfully")

            st.markdown("### Accuracy Summary")

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Source Numbers", f"{result.source_total:,}")
            m2.metric("Target Numbers", f"{result.target_total:,}")
            m3.metric("Matched", f"{result.matched_count:,}")
            m4.metric("Match Rate", f"{result.match_rate:.2f}%")

            st.markdown("---")

            c1, c2 = st.columns(2)

            with c1:
                st.subheader("Missing Numbers")
                st.caption("Present in originals but missing in compiled file")
                if result.missing_numbers:
                    st.write(f"**{result.missing_count}** numbers missing")
                    st.dataframe(
                        {"Number": result.missing_numbers},
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.success("None — All source numbers were found.")

            with c2:
                st.subheader("Extra Numbers")
                st.caption("Present only in the compiled file")
                if result.extra_numbers:
                    st.write(f"**{result.extra_count}** extra numbers")
                    st.dataframe(
                        {"Number": result.extra_numbers},
                        use_container_width=True,
                        height=300
                    )
                else:
                    st.success("None — No extra numbers found.")

            st.markdown("---")
            st.subheader("Download Reports")

            # Read the generated files for download
            with open(paths["excel"], "rb") as f:
                excel_data = f.read()

            with open(paths["text"], "rb") as f:
                text_data = f.read()

            dl1, dl2 = st.columns(2)
            with dl1:
                st.download_button(
                    label="Download Excel Report",
                    data=excel_data,
                    file_name="SourceMatch_Audit_Report.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            with dl2:
                st.download_button(
                    label="Download Text Report",
                    data=text_data,
                    file_name="SourceMatch_Audit_Report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with st.expander("View Matched Numbers"):
                if result.matched_numbers:
                    st.write(f"{result.matched_count} numbers matched successfully")
                    st.write(", ".join(result.matched_numbers[:100]))
                    if len(result.matched_numbers) > 100:
                        st.caption(f"... and {len(result.matched_numbers) - 100} more")
                else:
                    st.write("No matches found.")

else:
    st.info("Upload your files above and click **Run Accuracy Audit** to begin.")
