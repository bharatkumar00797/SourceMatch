"""
SourceMatch - Comparison Engine
Compares numerical data between source documents and a target compiled file.
Calculates match rate, missing values, and extra values.
"""

from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class ComparisonResult:
    """Structured result of a comparison."""
    source_total: int = 0
    target_total: int = 0
    matched_count: int = 0
    missing_count: int = 0
    extra_count: int = 0
    match_rate: float = 0.0

    matched_numbers: List[str] = field(default_factory=list)
    missing_numbers: List[str] = field(default_factory=list)
    extra_numbers: List[str] = field(default_factory=list)

    def summary_dict(self) -> Dict:
        return {
            "source_total": self.source_total,
            "target_total": self.target_total,
            "matched_count": self.matched_count,
            "missing_count": self.missing_count,
            "extra_count": self.extra_count,
            "match_rate": round(self.match_rate, 2),
        }


class Comparator:
    """
    Compares two sets of normalized numbers and produces
    match / missing / extra statistics + accuracy.
    """

    def __init__(self):
        pass

    @staticmethod
    def _to_set(numbers: List[str]) -> Set[str]:
        return set(numbers)

    @staticmethod
    def _sort_numerically(numbers: List[str]) -> List[str]:
        def key(x):
            try:
                return float(x)
            except ValueError:
                return 0.0
        return sorted(numbers, key=key)

    def compare(self, source_numbers: List[str], target_numbers: List[str]) -> ComparisonResult:
        """
        Compare source (original) numbers against target (compiled) numbers.

        Args:
            source_numbers: Unique numbers extracted from original documents
            target_numbers: Unique numbers extracted from the compiled file

        Returns:
            ComparisonResult with full statistics
        """
        source_set = self._to_set(source_numbers)
        target_set = self._to_set(target_numbers)

        matched = source_set.intersection(target_set)
        missing = source_set - target_set
        extra = target_set - source_set

        source_total = len(source_set)
        matched_count = len(matched)

        match_rate = (matched_count / source_total * 100) if source_total > 0 else 0.0

        result = ComparisonResult(
            source_total=source_total,
            target_total=len(target_set),
            matched_count=matched_count,
            missing_count=len(missing),
            extra_count=len(extra),
            match_rate=match_rate,
            matched_numbers=self._sort_numerically(list(matched)),
            missing_numbers=self._sort_numerically(list(missing)),
            extra_numbers=self._sort_numerically(list(extra)),
        )
        return result

    def print_report(self, result: ComparisonResult, title: str = "Comparison Result") -> None:
        """Print a clean console report."""
        print("\n" + "=" * 70)
        print(title)
        print("=" * 70)
        print(f"Unique numbers in Source (originals) : {result.source_total:,}")
        print(f"Unique numbers in Target (compiled)  : {result.target_total:,}")
        print(f"Numbers successfully matched         : {result.matched_count:,}")
        print(f"Numbers missing in Target            : {result.missing_count:,}")
        print(f"Numbers only in Target (extra)       : {result.extra_count:,}")
        print("-" * 70)
        print(f"MATCH RATE / ACCURACY                : {result.match_rate:.2f}%")
        print("=" * 70)

    def compare_and_report(self, source_numbers: List[str], target_numbers: List[str],
                           title: str = "SourceMatch Comparison") -> ComparisonResult:
        """Convenience method: compare + print report."""
        result = self.compare(source_numbers, target_numbers)
        self.print_report(result, title=title)
        return result


def demo():
    """Simple demonstration."""
    source = ["15117", "15009", "9148", "8423", "1149", "4009", "5635", "312"]
    target = ["15117", "15009", "9148", "8423", "5635", "9999", "100"]  # missing some, has extras

    comparator = Comparator()
    result = comparator.compare_and_report(source, target, title="Demo Comparison")

    print("\nMissing numbers:", result.missing_numbers)
    print("Extra numbers  :", result.extra_numbers)


if __name__ == "__main__":
    demo()
