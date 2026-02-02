"""
Unit tests for nexus.validators module

Tests validation functions that prevent incomplete aggregation and data integrity issues.
Created: 2026-02-02
Purpose: Fix Session Quality Issues (Build 02, Phase 1.2)
"""

import pytest
from pathlib import Path
from nexus.validators import (
    validate_aggregation_completeness,
    validate_aggregation_files,
    extract_batch_numbers,
    ValidationError
)


class TestAggregationCompleteness:
    """Test validate_aggregation_completeness function"""

    def test_incomplete_aggregation_raises_error(self):
        """Test 1: Incomplete aggregation (expected=10, actual=1) raises ValidationError"""
        with pytest.raises(ValidationError) as exc_info:
            validate_aggregation_completeness(
                expected=10,
                actual=1,
                context="batch analysis"
            )

        error_msg = str(exc_info.value)

        # Verify error message contains required information
        assert "Missing: 9 items" in error_msg
        assert "10.0% complete" in error_msg or "10% complete" in error_msg
        assert "consider using a subagent" in error_msg.lower() or "subagent" in error_msg
        assert "batch analysis" in error_msg

    def test_complete_aggregation_passes(self):
        """Test 2: Complete aggregation (expected=10, actual=10) passes"""
        # Should not raise any exception
        validate_aggregation_completeness(
            expected=10,
            actual=10,
            context="batch analysis"
        )

        # If we get here, test passed
        assert True

    def test_edge_cases(self):
        """Test 3: Edge cases (zero items, negative, too many)"""

        # Zero items - should pass (nothing to aggregate)
        validate_aggregation_completeness(expected=0, actual=0)

        # Negative expected should raise ValueError
        with pytest.raises(ValueError):
            validate_aggregation_completeness(expected=-1, actual=0)

        # Negative actual should raise ValueError
        with pytest.raises(ValueError):
            validate_aggregation_completeness(expected=10, actual=-1)

        # Too many items (actual > expected) - should raise ValidationError
        with pytest.raises(ValidationError):
            validate_aggregation_completeness(expected=5, actual=10)

    def test_error_message_format(self):
        """Test 4: Error message contains 'Missing: X items' and subagent suggestion"""
        with pytest.raises(ValidationError) as exc_info:
            validate_aggregation_completeness(
                expected=20,
                actual=5,
                context="test aggregation"
            )

        error_msg = str(exc_info.value)

        # Check all required components in error message
        assert "Missing: 15 items" in error_msg
        assert "25.0% complete" in error_msg or "25% complete" in error_msg
        assert "test aggregation" in error_msg
        assert "CRITICAL" in error_msg
        assert "Suggestion" in error_msg or "consider" in error_msg
        assert "subagent" in error_msg


class TestAggregationFiles:
    """Test validate_aggregation_files function"""

    def test_missing_directory_raises_error(self, tmp_path):
        """Test that missing directory raises ValidationError"""
        non_existent = tmp_path / "does_not_exist"

        with pytest.raises(ValidationError) as exc_info:
            validate_aggregation_files(non_existent)

        assert "does not exist" in str(exc_info.value)

    def test_file_as_directory_raises_error(self, tmp_path):
        """Test that file path (not directory) raises ValidationError"""
        file_path = tmp_path / "file.txt"
        file_path.write_text("content")

        with pytest.raises(ValidationError) as exc_info:
            validate_aggregation_files(file_path)

        assert "not a directory" in str(exc_info.value)

    def test_no_files_matching_pattern_raises_error(self, tmp_path):
        """Test that empty directory raises ValidationError"""
        batch_dir = tmp_path / "batches"
        batch_dir.mkdir()

        with pytest.raises(ValidationError) as exc_info:
            validate_aggregation_files(batch_dir, expected_pattern="batch-*.md")

        assert "No batch files found" in str(exc_info.value)
        assert "batch-*.md" in str(exc_info.value)

    def test_successful_discovery(self, tmp_path):
        """Test successful batch file discovery"""
        batch_dir = tmp_path / "batches"
        batch_dir.mkdir()

        # Create batch files
        (batch_dir / "batch-01.md").write_text("content 1")
        (batch_dir / "batch-02.md").write_text("content 2")
        (batch_dir / "batch-03.md").write_text("content 3")

        # Should return all files
        batch_files = validate_aggregation_files(batch_dir, expected_pattern="batch-*.md")

        assert len(batch_files) == 3
        assert all(f.suffix == ".md" for f in batch_files)

    def test_incomplete_read_list_raises_error(self, tmp_path):
        """Test that incomplete files_read list raises ValidationError"""
        batch_dir = tmp_path / "batches"
        batch_dir.mkdir()

        # Create batch files
        file1 = batch_dir / "batch-01.md"
        file2 = batch_dir / "batch-02.md"
        file3 = batch_dir / "batch-03.md"

        file1.write_text("content 1")
        file2.write_text("content 2")
        file3.write_text("content 3")

        # Only mark 2 as read
        files_read = [file1, file2]

        with pytest.raises(ValidationError) as exc_info:
            validate_aggregation_files(
                batch_dir,
                expected_pattern="batch-*.md",
                files_read=files_read
            )

        error_msg = str(exc_info.value)
        assert "Incomplete aggregation" in error_msg
        assert "batch-03.md" in error_msg
        assert "1 files not read" in error_msg or "1 file not read" in error_msg


class TestExtractBatchNumbers:
    """Test extract_batch_numbers utility function"""

    def test_extract_from_standard_filenames(self):
        """Test extraction from standard batch-NN.md format"""
        files = [
            Path("batch-01.md"),
            Path("batch-05.md"),
            Path("batch-10.md")
        ]

        batch_nums = extract_batch_numbers(files)

        assert batch_nums == {1, 5, 10}

    def test_extract_from_various_formats(self):
        """Test extraction handles various filename formats"""
        files = [
            Path("batch-1.md"),  # Single digit
            Path("batch-001.md"),  # Leading zeros
            Path("batch-99.md"),  # Large number
            Path("analysis-batch-42.md"),  # Prefix before batch
        ]

        batch_nums = extract_batch_numbers(files)

        # Should extract last number in each filename
        assert 1 in batch_nums
        assert 99 in batch_nums
        # Note: batch-001.md extracts as 1 (leading zeros ignored)

    def test_skip_non_numeric_files(self):
        """Test that files without numbers are skipped"""
        files = [
            Path("batch-01.md"),
            Path("summary.md"),  # No number
            Path("batch-notes.md"),  # No number
            Path("batch-02.md")
        ]

        batch_nums = extract_batch_numbers(files)

        # Only files with numbers extracted
        assert batch_nums == {1, 2}

    def test_empty_list_returns_empty_set(self):
        """Test that empty list returns empty set"""
        batch_nums = extract_batch_numbers([])

        assert batch_nums == set()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
