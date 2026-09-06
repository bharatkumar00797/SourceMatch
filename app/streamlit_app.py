"""
SourceMatch - Streamlit Web Interface (Day 7 - Polished)
Upload source PDFs + a compiled file and get an accuracy audit report.
"""

import os
import sys
import tempfile
import io
from pathlib import Path
from datetime import datetime

import streamlit as st
import pdfplumber

# Add src folder to path
SYS_PATH = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SYS_PATH))

from ocr_engine import OCREngine
from extractor import NumberExtractor
from comparator import Comparator
from reporter import Reporter


# -------------------- Page Config --------------------
st.set_page_config(
    page_title="SourceMatch | Data Integrity Auditor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for cleaner look
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #f8f9fa;
        border-radius: 8px;
        padding: 1rem;
        border-left: 4px solid #1F4E79;
    }
    .stProgress > div > div > div > div {
        background-color: #1F4E79;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- Sidebar --------------------
with st.sidebar:
    st.markdown("## SourceMatch")
    st.caption("Data Integrity Auditor")
    st.markdown("---")

    st.markdown(
        "Upload **original scanned PDFs** and one **compiled file**. "
        "SourceMatch calculates how accurately the compiled version matches the originals."
    )

    st.markdown("---")
    st.markdown("### Settings")

    dpi = st.slider("OCR Quality (DPI)", min_value=150, max_value=300, value=200, step=50,
                    help="Higher DPI improves accuracy but takes longer.")

    min_value = st.number_input(
        "Ignore numbers smaller than",
        min_value=0.0,
        value=1.0,
        step=1.0,
        help="Useful to filter out page numbers or tiny values."
    )

    with st.expander("Advanced Paths (Windows)"):
        tesseract_path = st.text_input(
            "Tesseract path",
            value=r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        )
        poppler_path = st.text_input(
            "Poppler path",
            value=r"C:\poppler\Library\bin"
        )

    st.markdown("---")
    st.caption("SourceMatch • Day 7")


# -------------------- Main Header --------------------
st.markdown('<p class="main-header">SourceMatch</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Verify how accurately a compiled Excel/PDF matches the original scanned source documents.</p>',
    unsafe_allow_html=True
)

# -------------------- File Upload Section --------------------
st.markdown("### 1. Upload Files")

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("**Original Source PDFs**")
    st.caption("The scanned documents that represent the source of truth")
    source_files = st.file_uploader(
        "Upload one or more PDF files",
        type=["pdf"],
        accept_multiple_files=True,
        key="source_uploader",
        label_visibility="collapsed"
    )
    if source_files:
        st.success(f"{len(source_files)} file(s) selected")

with col2:
    st.markdown("**Compiled / Target File**")
    st.caption("The Excel-converted or summary PDF you want to verify")
    target_file = st.file_uploader(
        "Upload the compiled PDF",
        type=["pdf"],
        accept_multiple_files=False,
        key="target_uploader",
        label_visibility="collapsed"
    )
    if target_file:
        st.success(f"Selected: {target_file.name}")

st.markdown("")
run_button = st.button("Run Accuracy Audit", type="primary", use_container_width=True)


def extract_text_from_pdf_bytes(file_bytes: bytes) -> str:
    """Extract text from a clean PDF."""
    pages = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages.append(text)
    return "\n\n".join(pages)


# -------------------- Run Pipeline --------------------
if run_button:
    if not source_files:
        st.error("Please upload at least one original source PDF.")
        st.stop()

    if not target_file:
        st.error("Please upload the compiled target file.")
        st.stop()

    status_box = st.empty()
    status_box.info("Starting audit... This may take several minutes if the PDFs are scanned images.")

    with tempfile.TemporaryDirectory() as temp_dir:
        source_dir = os.path.join(temp_dir, "source")
        output_dir = os.path.join(temp_dir, "output")
        reports_dir = os.path.join(output_dir, "reports")
        os.makedirs(source_dir, exist_ok=True)
        os.makedirs(reports_dir, exist_ok=True)

        # Save uploaded files
        for uploaded in source_files:
            with open(os.path.join(source_dir, uploaded.name), "wb") as f:
                f.write(uploaded.getbuffer())

        target_path = os.path.join(temp_dir, target_file.name)
        with open(target_path, "wb") as f:
            f.write(target_file.getbuffer())

        progress = st.progress(0)
        step_text = st.empty()

        try:
            # Stage 1: OCR
            step_text.markdown("**Step 1/5** — Running OCR on source PDFs...")
            progress.progress(10)

            engine = OCREngine(
                tesseract_path=tesseract_path.strip() or None,
                poppler_path=poppler_path.strip() or None,
                dpi=dpi
            )
            ocr_results = engine.ocr_folder(source_dir, output_dir=output_dir)

            if not ocr_results:
                st.error("No text could be extracted from the source PDFs. Check that Tesseract and Poppler are correctly installed.")
                st.stop()

            progress.progress(40)
            step_text.markdown("**Step 2/5** — Extracting numbers from source documents...")

            extractor = NumberExtractor(min_value=min_value)
            source_numbers = extractor.get_all_unique(ocr_results)

            progress.progress(55)
            step_text.markdown("**Step 3/5** — Extracting numbers from compiled file...")

            target_text = extract_text_from_pdf_bytes(target_file.getvalue())
            target_numbers = extractor.extract_unique(target_text)

            progress.progress(70)
            step_text.markdown("**Step 4/5** — Comparing data and calculating accuracy...")

            comparator = Comparator()
            result = comparator.compare(source_numbers, target_numbers)

            progress.progress(85)
            step_text.markdown("**Step 5/5** — Generating audit reports...")

            reporter = Reporter(output_dir=reports_dir)
            paths = reporter.generate_all(
                result,
                source_name=f"{len(source_files)} source PDF(s)",
                target_name=target_file.name
            )

            progress.progress(100)
            step_text.empty()
            status_box.empty()

        except Exception as e:
            st.error(f"An error occurred during processing:\n\n`{e}`")
            st.stop()

        # -------------------- Results --------------------
        st.success("Audit completed successfully")

        # Accuracy highlight
        accuracy_color = "normal"
        if result.match_rate >= 80:
            accuracy_color = "off"
        elif result.match_rate >= 50:
            accuracy_color = "normal"

        st.markdown("### Accuracy Overview")

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Source Numbers", f"{result.source_total:,}")
        m2.metric("Target Numbers", f"{result.target_total:,}")
        m3.metric("Matched", f"{result.matched_count:,}")
        m4.metric("Match Rate", f"{result.match_rate:.2f}%",
                  delta=None)

        st.caption(
            f"Formula: (Matched Numbers ÷ Total Unique Numbers in Source) × 100  •  "
            f"Generated on {datetime.now().strftime('%d %b %Y, %I:%M %p')}"
        )

        st.markdown("---")

        # Missing & Extra side by side
        c1, c2 = st.columns(2, gap="large")

        with c1:
            st.markdown("#### Missing Numbers")
            st.caption("Present in original source PDFs but **not found** in the compiled file")

            if result.missing_numbers:
                st.warning(f"**{result.missing_count}** numbers are missing")
                st.dataframe(
                    {"Missing Number": result.missing_numbers},
                    use_container_width=True,
                    height=320
                )
            else:
                st.success("None — Every source number was found in the compiled file.")

        with c2:
            st.markdown("#### Extra Numbers")
            st.caption("Present only in the compiled file (not found in originals)")

            if result.extra_numbers:
                st.info(f"**{result.extra_count}** extra numbers detected")
                st.dataframe(
                    {"Extra Number": result.extra_numbers},
                    use_container_width=True,
                    height=320
                )
            else:
                st.success("None — No extra numbers were introduced.")

        st.markdown("---")

        # Downloads
        st.markdown("### Download Audit Reports")

        with open(paths["excel"], "rb") as f:
            excel_data = f.read()
        with open(paths["text"], "rb") as f:
            text_data = f.read()

        dl1, dl2, _ = st.columns([1, 1, 2])

        with dl1:
            st.download_button(
                label="📊 Download Excel Report",
                data=excel_data,
                file_name="SourceMatch_Audit_Report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        with dl2:
            st.download_button(
                label="📄 Download Text Report",
                data=text_data,
                file_name="SourceMatch_Audit_Report.txt",
                mime="text/plain",
                use_container_width=True
            )

        with st.expander("View matched numbers"):
            if result.matched_numbers:
                st.write(f"**{result.matched_count}** numbers matched successfully between source and target.")
                st.code(", ".join(result.matched_numbers[:120]), language=None)
                if len(result.matched_numbers) > 120:
                    st.caption(f"Showing first 120 of {result.matched_count} matched numbers.")
            else:
                st.write("No numbers matched.")

else:
    st.info("Upload your source PDFs and compiled file above, then click **Run Accuracy Audit**.")

    with st.expander("How SourceMatch works"):
        st.markdown("""
**Step-by-step process:**

1. **OCR** — Converts scanned PDF pages into text using Tesseract
2. **Extraction** — Pulls all numerical values from the text
3. **Comparison** — Matches numbers from original documents against the compiled file
4. **Accuracy** — Calculates Match Rate = (Matched ÷ Source Total) × 100
5. **Reporting** — Generates downloadable Excel and text audit reports

This helps analysts and auditors quickly see what data is missing or was added during compilation.
        """)
