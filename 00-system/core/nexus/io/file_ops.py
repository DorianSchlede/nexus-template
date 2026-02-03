"""
Nexus File Operations

Safe file operation wrappers that prevent data loss and enforce best practices
like read-before-write, automatic backups, and existence checks.

Created: 2026-02-02
Purpose: Fix Session Quality Issues (Build 02, Phase 1)
"""

import shutil
import time
from pathlib import Path
from typing import Optional, Union


class FileOperationError(Exception):
    """Raised when a file operation violates safety rules."""
    pass


def safe_write(
    file_path: Union[str, Path],
    content: str,
    force: bool = False,
    backup: bool = True,
    size_threshold: int = 100
) -> None:
    """
    Write file with existence check and automatic backup.

    This prevents accidental overwrites of existing files without first reading
    them to understand what's there. Enforces the "read-before-write" pattern.

    Args:
        file_path: Path to the file to write
        content: Content to write to the file
        force: If True, skip existence check and overwrite (default: False)
        backup: If True, create backup before overwriting (default: True)
        size_threshold: Minimum file size (bytes) to trigger safety check (default: 100)

    Raises:
        FileOperationError: If file exists and force=False

    Example:
        >>> # Safe write - will check existence first
        >>> safe_write("output.md", "# New content")
        FileOperationError: output.md exists with 5432 bytes. Read it first or use force=True.

        >>> # After reading the existing file:
        >>> existing = Path("output.md").read_text()
        >>> # ... decide if safe to overwrite ...
        >>> safe_write("output.md", "# Updated content", force=True)
        📦 Backed up to output.backup-1675432100.md
        ✅ Wrote 18 bytes to output.md

    When to use:
        - Before ANY Write or Edit operation
        - When creating files in existing directories
        - When generating output files

    Exception:
        - New files in empty directories (e.g., BUILD initialization)
        - Files you JUST created in the same session
        - Temporary files in scratchpad

    Why this matters:
        Without safe_write(), agents might:
        - Overwrite 10KB planning documents with new content
        - Destroy existing work without reading it first
        - Lose data that was never backed up
    """
    file_path = Path(file_path)

    # Check if file exists
    if file_path.exists():
        if not file_path.is_file():
            raise FileOperationError(
                f"{file_path} exists but is not a file (directory or special file)"
            )

        # Get existing file info
        existing_size = file_path.stat().st_size

        # If file is non-trivial and force not set, block the write
        if existing_size > size_threshold and not force:
            existing_kb = existing_size / 1024

            raise FileOperationError(
                f"{file_path.name} exists with {existing_size} bytes ({existing_kb:.1f} KB)\n"
                f"\n"
                f"CRITICAL: Read the file first to check if it's safe to overwrite.\n"
                f"\n"
                f"Options:\n"
                f"1. Read it first: Path('{file_path}').read_text()\n"
                f"2. Use force=True if you already read it: safe_write(..., force=True)\n"
                f"3. Use a different filename\n"
                f"4. Use Edit tool to modify instead of replacing\n"
                f"\n"
                f"This check prevents accidental data loss."
            )

        # Backup existing file before overwriting
        if backup and existing_size > 0:
            backup_path = file_path.with_suffix(f".backup-{int(time.time())}{file_path.suffix}")
            shutil.copy(file_path, backup_path)
            print(f"📦 Backed up to {backup_path.name}")

    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write the file
    file_path.write_text(content, encoding='utf-8')

    new_size = len(content.encode('utf-8'))
    new_kb = new_size / 1024
    print(f"✅ Wrote {new_size} bytes ({new_kb:.1f} KB) to {file_path.name}")


def safe_read_then_write(
    file_path: Union[str, Path],
    content: str,
    backup: bool = True
) -> Optional[str]:
    """
    Read existing file, then write new content (with automatic backup).

    This is the RECOMMENDED pattern for overwriting files: read first, decide,
    then write. The existing content is returned so you can verify it's safe
    to overwrite.

    Args:
        file_path: Path to the file
        content: New content to write
        backup: If True, create backup before overwriting (default: True)

    Returns:
        Existing content if file existed, None if new file

    Example:
        >>> # Read existing file (if any)
        >>> existing = safe_read_then_write(
        ...     "output.md",
        ...     "# New content"
        ... )
        ✅ Read 5432 bytes from output.md
        📦 Backed up to output.backup-1675432100.md
        ✅ Wrote 14 bytes to output.md

        >>> if existing:
        ...     print(f"Overwrote {len(existing)} bytes")
        >>> else:
        ...     print("Created new file")
    """
    file_path = Path(file_path)

    existing_content = None

    # Read existing file if it exists
    if file_path.exists():
        if not file_path.is_file():
            raise FileOperationError(
                f"{file_path} exists but is not a file"
            )

        existing_content = file_path.read_text(encoding='utf-8')
        existing_size = len(existing_content.encode('utf-8'))
        print(f"✅ Read {existing_size} bytes from {file_path.name}")

        # Backup if requested
        if backup and existing_size > 0:
            backup_path = file_path.with_suffix(f".backup-{int(time.time())}{file_path.suffix}")
            shutil.copy(file_path, backup_path)
            print(f"📦 Backed up to {backup_path.name}")

    # Create parent directories if needed
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # Write new content
    file_path.write_text(content, encoding='utf-8')

    new_size = len(content.encode('utf-8'))
    print(f"✅ Wrote {new_size} bytes to {file_path.name}")

    return existing_content


def check_file_exists_and_warn(file_path: Union[str, Path]) -> tuple[bool, int]:
    """
    Check if file exists and get size without reading content.

    Use this before Write operations to decide whether to proceed.

    Args:
        file_path: Path to check

    Returns:
        Tuple of (exists: bool, size_bytes: int)

    Example:
        >>> exists, size = check_file_exists_and_warn("output.md")
        >>> if exists and size > 1000:
        ...     print(f"⚠️  File exists ({size} bytes). Read it first!")
        ...     existing = Path("output.md").read_text()
        ...     # ... analyze existing content ...
        >>> # Now safe to write
        >>> safe_write("output.md", new_content, force=True)
    """
    file_path = Path(file_path)

    if not file_path.exists():
        return False, 0

    if not file_path.is_file():
        raise FileOperationError(
            f"{file_path} exists but is not a file"
        )

    size = file_path.stat().st_size

    if size > 100:  # Non-trivial file
        size_kb = size / 1024
        print(f"⚠️  {file_path.name} exists ({size} bytes / {size_kb:.1f} KB)")
        print("Consider reading it first to check if it's safe to overwrite.")

    return True, size


# Example usage documentation
if __name__ == "__main__":
    print(__doc__)
    print("\n" + "="*80)
    print("EXAMPLE USAGE")
    print("="*80)
    print("""
# Example 1: Safe write with existence check
# -------------------------------------------
from nexus.io.file_ops import safe_write

# This will fail if file exists and is >100 bytes
try:
    safe_write("output.md", "# New content")
except FileOperationError as e:
    print(f"Blocked: {e}")
    # Now read the file to check what's there
    existing = Path("output.md").read_text()
    print(f"Existing content: {existing[:100]}...")

    # After reading, if safe to overwrite:
    safe_write("output.md", "# New content", force=True)


# Example 2: Read-then-write pattern (RECOMMENDED)
# -------------------------------------------------
from nexus.io.file_ops import safe_read_then_write

# This automatically reads, backs up, then writes
existing = safe_read_then_write(
    "output.md",
    "# Updated content"
)

if existing:
    print(f"Overwrote {len(existing)} bytes")
else:
    print("Created new file")


# Example 3: Check before writing
# --------------------------------
from nexus.io.file_ops import check_file_exists_and_warn

exists, size = check_file_exists_and_warn("output.md")

if exists:
    # Read to understand what's there
    existing = Path("output.md").read_text()

    # Make decision based on content
    if "important" in existing.lower():
        print("File contains important content, using Edit instead of Write")
        # Use Edit tool to modify specific sections
    else:
        print("Safe to overwrite")
        safe_write("output.md", new_content, force=True)
else:
    # New file, safe to write
    safe_write("output.md", new_content)


# Example 4: Integration with orchestrator guidance
# --------------------------------------------------
'''
In orchestrator.md "Never Do" section:

BEFORE Write or Edit:
1. Check if file exists (ls, glob, or try Read)
2. If exists: Read it to see what's there
3. Decide: Overwrite, append, or new filename
4. If overwriting: Consider backup first
5. THEN write

Use safe_write() to enforce this pattern automatically.

Example workflow:
```python
from nexus.io.file_ops import safe_write
from pathlib import Path

# WRONG - just write without checking
Path("output.md").write_text(content)  # ❌ Could lose data

# RIGHT - use safe_write
safe_write("output.md", content)  # ✅ Will block if file exists
```

Exception: New files in empty directories (e.g., BUILD initialization)
'''


# Example 5: Batch processing with safe writes
# ---------------------------------------------
def process_batch_outputs(batch_results):
    '''Process multiple outputs safely'''
    from nexus.io.file_ops import safe_write

    for batch_num, result in enumerate(batch_results, 1):
        output_file = f"output-{batch_num:02d}.md"

        # safe_write will check if file exists from previous run
        try:
            safe_write(output_file, result)
        except FileOperationError:
            # File exists from previous run, check if we should overwrite
            existing = Path(output_file).read_text()

            if existing == result:
                print(f"Batch {batch_num} unchanged, skipping")
            else:
                print(f"Batch {batch_num} updated, overwriting")
                safe_write(output_file, result, force=True)
""")
