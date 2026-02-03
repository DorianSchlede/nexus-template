"""
Unit tests for nexus.file_ops module

Tests safe file operation wrappers that prevent data loss through read-before-write patterns.
Created: 2026-02-02
Purpose: Fix Session Quality Issues (Build 02, Phase 1.4)
"""

import pytest
import time
from pathlib import Path
from nexus.io.file_ops import (
    safe_write,
    safe_read_then_write,
    check_file_exists_and_warn,
    FileOperationError
)


class TestSafeWrite:
    """Test safe_write function"""

    def test_blocks_overwrite_large_file_without_force(self, tmp_path):
        """Test 1: Blocks overwrite of existing file >100 bytes without force"""
        test_file = tmp_path / "existing.md"

        # Create file with >100 bytes
        large_content = "x" * 200  # 200 bytes
        test_file.write_text(large_content)

        # Attempt to overwrite without force - should raise error
        with pytest.raises(FileOperationError) as exc_info:
            safe_write(test_file, "new content", force=False)

        error_msg = str(exc_info.value)

        # Verify error message contains required information
        assert "200 bytes" in error_msg
        assert "CRITICAL" in error_msg
        assert "Read the file first" in error_msg or "Read it first" in error_msg
        assert "force=True" in error_msg

        # Verify file was NOT modified
        assert test_file.read_text() == large_content

    def test_allows_overwrite_with_force(self, tmp_path):
        """Test 2: Allows overwrite with force=True"""
        test_file = tmp_path / "existing.md"

        # Create file with >100 bytes
        large_content = "x" * 200
        test_file.write_text(large_content)

        # Overwrite with force=True - should succeed
        new_content = "new content after reading"
        safe_write(test_file, new_content, force=True)

        # Verify file was modified
        assert test_file.read_text() == new_content

    def test_creates_backup_before_overwriting(self, tmp_path, capsys):
        """Test 3: Creates backup before overwriting"""
        test_file = tmp_path / "document.md"

        # Create initial file
        original_content = "original content"
        test_file.write_text(original_content)

        # Wait a moment to ensure different timestamp
        time.sleep(0.1)

        # Overwrite with backup enabled (default)
        new_content = "updated content"
        safe_write(test_file, new_content, force=True, backup=True)

        # Check backup was created
        backups = list(tmp_path.glob("document.backup-*.md"))
        assert len(backups) == 1

        backup_file = backups[0]

        # Verify backup contains original content
        assert backup_file.read_text() == original_content

        # Verify main file has new content
        assert test_file.read_text() == new_content

        # Verify output message
        captured = capsys.readouterr()
        assert "📦 Backed up to" in captured.out
        assert backup_file.name in captured.out

    def test_allows_small_files_without_force(self, tmp_path):
        """Test 4: Allows small files (<100 bytes) without force"""
        test_file = tmp_path / "small.md"

        # Create file with exactly 50 bytes (below threshold)
        small_content = "x" * 50
        test_file.write_text(small_content)

        # Overwrite without force - should succeed for small files
        new_content = "replaced"
        safe_write(test_file, new_content, force=False)

        # Verify file was modified
        assert test_file.read_text() == new_content

    def test_allows_new_file_creation(self, tmp_path):
        """Test that new files can be created without force"""
        test_file = tmp_path / "newfile.md"

        # File doesn't exist yet
        assert not test_file.exists()

        # Create new file - should succeed
        content = "brand new content"
        safe_write(test_file, content, force=False)

        assert test_file.exists()
        assert test_file.read_text() == content

    def test_custom_size_threshold(self, tmp_path):
        """Test custom size_threshold parameter"""
        test_file = tmp_path / "custom.md"

        # Create file with 150 bytes
        content = "x" * 150
        test_file.write_text(content)

        # With default threshold (100), should block
        with pytest.raises(FileOperationError):
            safe_write(test_file, "new", force=False, size_threshold=100)

        # With higher threshold (200), should allow
        safe_write(test_file, "new", force=False, size_threshold=200)

        assert test_file.read_text() == "new"

    def test_backup_disabled(self, tmp_path):
        """Test that backup can be disabled"""
        test_file = tmp_path / "nobkp.md"

        # Create initial file
        test_file.write_text("original")

        # Overwrite with backup disabled
        safe_write(test_file, "updated", force=True, backup=False)

        # Verify no backup created
        backups = list(tmp_path.glob("nobkp.backup-*"))
        assert len(backups) == 0

        # Verify file was still updated
        assert test_file.read_text() == "updated"

    def test_directory_as_path_raises_error(self, tmp_path):
        """Test that attempting to write to a directory raises error"""
        dir_path = tmp_path / "subdir"
        dir_path.mkdir()

        with pytest.raises(FileOperationError) as exc_info:
            safe_write(dir_path, "content", force=True)

        assert "not a file" in str(exc_info.value)


class TestSafeReadThenWrite:
    """Test safe_read_then_write function"""

    def test_read_then_write_existing_file(self, tmp_path, capsys):
        """Test read-then-write pattern on existing file"""
        test_file = tmp_path / "existing.md"

        # Create initial file
        original = "original content"
        test_file.write_text(original)

        # Read then write
        existing_content = safe_read_then_write(
            test_file,
            "new content"
        )

        # Verify existing content was returned
        assert existing_content == original

        # Verify file was updated
        assert test_file.read_text() == "new content"

        # Verify output shows read and write
        captured = capsys.readouterr()
        assert "Read" in captured.out
        assert "Wrote" in captured.out

    def test_read_then_write_new_file(self, tmp_path):
        """Test read-then-write pattern on new file"""
        test_file = tmp_path / "newfile.md"

        # File doesn't exist
        assert not test_file.exists()

        # Read then write
        existing_content = safe_read_then_write(
            test_file,
            "brand new"
        )

        # Should return None for new file
        assert existing_content is None

        # Verify file was created
        assert test_file.exists()
        assert test_file.read_text() == "brand new"

    def test_creates_parent_directories(self, tmp_path):
        """Test that parent directories are created automatically"""
        nested_file = tmp_path / "level1" / "level2" / "file.md"

        # Parent directories don't exist
        assert not nested_file.parent.exists()

        # Write file
        safe_write(nested_file, "content")

        # Verify parent directories created
        assert nested_file.parent.exists()
        assert nested_file.exists()


class TestCheckFileExistsAndWarn:
    """Test check_file_exists_and_warn utility function"""

    def test_returns_false_for_nonexistent_file(self, tmp_path):
        """Test that nonexistent file returns (False, 0)"""
        test_file = tmp_path / "doesnotexist.md"

        exists, size = check_file_exists_and_warn(test_file)

        assert exists is False
        assert size == 0

    def test_returns_true_and_size_for_existing_file(self, tmp_path):
        """Test that existing file returns (True, size)"""
        test_file = tmp_path / "exists.md"
        content = "x" * 500
        test_file.write_text(content)

        exists, size = check_file_exists_and_warn(test_file)

        assert exists is True
        assert size == 500

    def test_warns_for_large_files(self, tmp_path, capsys):
        """Test that warning is printed for files >100 bytes"""
        test_file = tmp_path / "large.md"
        test_file.write_text("x" * 200)

        check_file_exists_and_warn(test_file)

        captured = capsys.readouterr()
        assert "⚠️" in captured.out or "exists" in captured.out.lower()
        assert "200 bytes" in captured.out

    def test_no_warning_for_small_files(self, tmp_path, capsys):
        """Test that no warning for files ≤100 bytes"""
        test_file = tmp_path / "small.md"
        test_file.write_text("x" * 50)

        check_file_exists_and_warn(test_file)

        captured = capsys.readouterr()
        # Should not have warning message for small files
        assert "⚠️" not in captured.out

    def test_directory_raises_error(self, tmp_path):
        """Test that directory path raises error"""
        dir_path = tmp_path / "subdir"
        dir_path.mkdir()

        with pytest.raises(FileOperationError):
            check_file_exists_and_warn(dir_path)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
