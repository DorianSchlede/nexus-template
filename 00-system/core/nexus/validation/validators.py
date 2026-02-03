"""
Nexus Validation Utilities

Validation functions to ensure data integrity and prevent common errors
like incomplete aggregation, write-without-read, and other critical violations.

Created: 2026-02-02
Purpose: Fix Session Quality Issues (Build 02, Phase 1)
"""

from typing import List, Set, Optional
from pathlib import Path


class ValidationError(Exception):
    """Raised when validation fails."""
    pass


def validate_aggregation_completeness(
    expected: int,
    actual: int,
    context: str = "aggregation"
) -> None:
    """
    Validate that all expected items were processed before aggregation.

    This prevents incomplete aggregation where a summary is written after
    reading only a subset of source files, leading to hallucinated data.

    Args:
        expected: Number of items that should have been processed
        actual: Number of items actually processed
        context: Description of what's being aggregated (for error messages)

    Raises:
        ValidationError: If actual != expected

    Example:
        >>> # Before writing aggregation summary:
        >>> batch_files = list(Path("batches").glob("batch-*.md"))
        >>> files_read = [f for f in batch_files if f in read_files]
        >>> validate_aggregation_completeness(
        ...     expected=len(batch_files),
        ...     actual=len(files_read),
        ...     context="batch analysis"
        ... )

    When to use:
        - Before writing any aggregation summary
        - After batch processing with subagents
        - When combining multiple source files into one output
        - Anytime you're synthesizing data from multiple sources

    Why this matters:
        Without validation, agents might:
        - Read 1/10 files and write summary claiming to cover all 10
        - Hallucinate content about unread files
        - Create incomplete or misleading aggregations
    """
    if not isinstance(expected, int) or expected < 0:
        raise ValueError(f"expected must be a non-negative integer, got: {expected}")

    if not isinstance(actual, int) or actual < 0:
        raise ValueError(f"actual must be a non-negative integer, got: {actual}")

    if actual != expected:
        missing_count = expected - actual
        percentage_complete = (actual / expected * 100) if expected > 0 else 0

        raise ValidationError(
            f"Incomplete {context}: Expected {expected} items, but only processed {actual}.\n"
            f"Missing: {missing_count} items ({percentage_complete:.1f}% complete)\n"
            f"\n"
            f"CRITICAL: Do not write aggregation summary until ALL items are processed.\n"
            f"\n"
            f"To fix:\n"
            f"1. Read all {expected} items\n"
            f"2. Validate all were read\n"
            f"3. THEN write aggregation\n"
            f"\n"
            f"Suggestion: If >{expected} items, consider using a subagent for aggregation."
        )


def validate_aggregation_files(
    batch_dir: Path,
    expected_pattern: str = "batch-*.md",
    files_read: Optional[List[Path]] = None
) -> List[Path]:
    """
    Validate that all batch files exist and optionally that all were read.

    Args:
        batch_dir: Directory containing batch files
        expected_pattern: Glob pattern for batch files (default: "batch-*.md")
        files_read: Optional list of files that were actually read

    Returns:
        List of all batch files found

    Raises:
        ValidationError: If no batch files found, or if files_read provided and incomplete

    Example:
        >>> # Discover all batch files and validate all were read
        >>> batch_files = validate_aggregation_files(
        ...     batch_dir=Path("batches"),
        ...     files_read=read_files_list
        ... )
        >>> # Now safe to aggregate
    """
    if not batch_dir.exists():
        raise ValidationError(f"Batch directory does not exist: {batch_dir}")

    if not batch_dir.is_dir():
        raise ValidationError(f"Path is not a directory: {batch_dir}")

    # Discover all batch files
    batch_files = sorted(batch_dir.glob(expected_pattern))

    if not batch_files:
        raise ValidationError(
            f"No batch files found in {batch_dir} matching pattern '{expected_pattern}'"
        )

    # If files_read provided, validate completeness
    if files_read is not None:
        files_read_set = set(files_read)
        batch_files_set = set(batch_files)

        missing_files = batch_files_set - files_read_set

        if missing_files:
            missing_names = [f.name for f in sorted(missing_files)]
            raise ValidationError(
                f"Incomplete aggregation: {len(missing_files)} files not read.\n"
                f"Missing files: {', '.join(missing_names)}\n"
                f"\n"
                f"Read all {len(batch_files)} files before aggregating."
            )

    return batch_files


def extract_batch_numbers(batch_files: List[Path]) -> Set[int]:
    """
    Extract batch numbers from filenames like 'batch-01.md', 'batch-02.md'.

    Args:
        batch_files: List of batch file paths

    Returns:
        Set of batch numbers extracted from filenames

    Example:
        >>> files = [Path("batch-01.md"), Path("batch-05.md")]
        >>> extract_batch_numbers(files)
        {1, 5}
    """
    batch_nums = set()

    for file in batch_files:
        # Extract number from filename like "batch-01.md" or "batch-1.md"
        stem = file.stem  # "batch-01"
        parts = stem.split("-")

        if len(parts) >= 2:
            try:
                num = int(parts[-1])  # Last part should be the number
                batch_nums.add(num)
            except ValueError:
                # Skip files that don't match expected pattern
                continue

    return batch_nums


# Example usage documentation
if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*80)
    print("EXAMPLE USAGE")
    print("="*80)
    print("""
# Example 1: Basic aggregation validation
# ----------------------------------------
batch_dir = Path("02-builds/active/build-01/03-working/batches")
batch_files = list(batch_dir.glob("batch-*.md"))

# Read all batch files
files_read = []
for batch_file in batch_files:
    content = batch_file.read_text()
    files_read.append(batch_file)

# VALIDATE before aggregating
validate_aggregation_completeness(
    expected=len(batch_files),
    actual=len(files_read),
    context="batch analysis"
)

# NOW safe to write aggregation
summary = aggregate_all_batches(files_read)
output_file.write_text(summary)


# Example 2: Using validate_aggregation_files
# -------------------------------------------
from nexus.validation.validators import validate_aggregation_files

# This discovers files AND validates all were read
batch_files = validate_aggregation_files(
    batch_dir=Path("batches"),
    files_read=my_read_files_list  # List of Path objects actually read
)

# If we get here, validation passed
aggregate_and_write(batch_files)


# Example 3: In analyze-context skill
# ------------------------------------
def aggregate_batch_analysis(batch_dir: Path, expected_count: int):
    '''Aggregate batch files with validation.'''

    # 1. Discover all batch files
    batch_files = sorted(batch_dir.glob("batch-*.md"))

    # 2. VALIDATE count
    validate_aggregation_completeness(
        expected=expected_count,
        actual=len(batch_files),
        context="batch file discovery"
    )

    # 3. Read ALL files
    all_content = []
    for i, batch_file in enumerate(batch_files, 1):
        print(f"Reading batch {i}/{len(batch_files)}: {batch_file.name}")
        content = batch_file.read_text()
        all_content.append({"file": batch_file.name, "content": content})

    # 4. VALIDATE all were read
    validate_aggregation_completeness(
        expected=expected_count,
        actual=len(all_content),
        context="batch file reading"
    )

    # 5. NOW aggregate
    summary = create_summary(all_content)
    return summary
""")
