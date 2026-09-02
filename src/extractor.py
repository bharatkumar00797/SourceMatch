"""
SourceMatch - Numerical Data Extractor
Extracts and normalizes numbers from OCR or clean text.
"""

import re
from typing import List, Dict, Set


class NumberExtractor:
    """
    Extracts numerical values from text and normalizes them
    for reliable comparison.
    """

    # Pattern captures:
    # - integers with optional thousand separators (1,234 or 1234)
    # - decimal numbers (12.5, 1,234.56)
    NUMBER_PATTERN = re.compile(
        r"\b\d{1,3}(?:,\d{3})*(?:\.\d+)?\b|"   # 1,234.56 or 1,234
        r"\b\d+\.\d+\b|"                       # 12.34
        r"\b\d+\b"                             # plain integers
    )

    def __init__(self, min_value: float = None, max_value: float = None):
        """
        Args:
            min_value: Optional lower bound to ignore very small numbers (e.g. page numbers)
            max_value: Optional upper bound to ignore unrealistic values
        """
        self.min_value = min_value
        self.max_value = max_value

    def normalize(self, raw: str) -> str:
        """
        Normalize a raw number string.
        - Removes thousand separators
        - Keeps decimal point
        - Returns clean string representation
        """
        cleaned = raw.replace(",", "").strip()
        try:
            # Convert to float then back to string to standardize
            value = float(cleaned)
            # Avoid scientific notation for normal ranges
            if value == int(value) and abs(value) < 1e15:
                return str(int(value))
            return str(value)
        except ValueError:
            return cleaned

    def is_valid(self, normalized: str) -> bool:
        """Apply optional min/max filters."""
        try:
            value = float(normalized)
        except ValueError:
            return False

        if self.min_value is not None and value < self.min_value:
            return False
        if self.max_value is not None and value > self.max_value:
            return False
        return True

    def extract_from_text(self, text: str) -> List[str]:
        """
        Extract all valid normalized numbers from a text string.
        Returns a list (order preserved, duplicates kept for frequency analysis).
        """
        if not text:
            return []

        raw_matches = self.NUMBER_PATTERN.findall(text)
        results = []

        for raw in raw_matches:
            normalized = self.normalize(raw)
            if self.is_valid(normalized):
                results.append(normalized)

        return results

    def extract_unique(self, text: str) -> List[str]:
        """
        Extract unique normalized numbers (order of first appearance preserved).
        """
        all_numbers = self.extract_from_text(text)
        seen = set()
        unique = []
        for num in all_numbers:
            if num not in seen:
                seen.add(num)
                unique.append(num)
        return unique

    def extract_from_multiple(self, texts: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Extract unique numbers from multiple documents.

        Args:
            texts: Dictionary {filename: text_content}

        Returns:
            Dictionary {filename: list_of_unique_numbers}
        """
        result = {}
        for name, text in texts.items():
            result[name] = self.extract_unique(text)
        return result

    def get_all_unique(self, texts: Dict[str, str]) -> List[str]:
        """
        Collect every unique number across all documents.
        """
        combined = set()
        for text in texts.values():
            combined.update(self.extract_unique(text))

        # Sort numerically where possible
        def sort_key(x):
            try:
                return float(x)
            except ValueError:
                return 0

        return sorted(list(combined), key=sort_key)

    def summary(self, texts: Dict[str, str]) -> Dict:
        """
        Generate a quick summary of extracted numbers.
        """
        per_file = self.extract_from_multiple(texts)
        all_unique = self.get_all_unique(texts)

        return {
            "total_documents": len(texts),
            "numbers_per_document": {k: len(v) for k, v in per_file.items()},
            "total_unique_numbers": len(all_unique),
            "all_unique_numbers": all_unique,
            "per_document_numbers": per_file
        }


def demo():
    """Simple demonstration of the extractor."""
    sample_text = """
    In the year 2023-24, New OPD was 15,117 and Old OPD was 15,009.
    Total cataract surgeries: 9,148 (Free: 8,423 / Subsidised: 1,149 / Paid: 4009).
    ECG tests conducted: 5,635. HCV tests: 312.
    Budget allocated: 12.5 million. Page 14 of 48.
    """

    extractor = NumberExtractor(min_value=1)  # ignore pure zeros if any

    print("Sample text extraction:")
    print("-" * 50)
    numbers = extractor.extract_unique(sample_text)
    for n in numbers:
        print(f"  {n}")

    print(f"\nTotal unique numbers found: {len(numbers)}")


if __name__ == "__main__":
    demo()
