#!/usr/bin/env python3
"""
Test optimized resume-context.md template parsing.

Validates that the minimal template still works with SessionStart hook YAML parser.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))

def test_optimized_template_parsing():
    """Test that optimized template can be parsed correctly."""

    # Read the optimized template
    optimized_file = Path(__file__).parent / "resume-context-OPTIMIZED.md"

    if not optimized_file.exists():
        print(f"ERROR: Optimized template not found at {optimized_file}")
        return False

    content = optimized_file.read_text(encoding='utf-8')

    # Simple YAML parser (same logic as SessionStart hook)
    if '---' not in content:
        print("ERROR: No YAML frontmatter delimiter found")
        return False

    parts = content.split('---', 2)
    if len(parts) < 3:
        print("ERROR: Invalid YAML frontmatter structure")
        return False

    yaml_content = parts[1].strip()

    # Parse YAML manually (zero-dependency approach from hook)
    metadata = {}
    current_key = None
    current_list = None

    for line in yaml_content.split('\n'):
        line_stripped = line.strip()

        # Skip comments and empty lines
        if not line_stripped or line_stripped.startswith('#'):
            continue

        # Check if this is a list item
        if line_stripped.startswith('-') and current_list is not None:
            # List item for current key
            value = line_stripped[1:].strip().strip('"').strip("'")
            current_list.append(value)
        elif ':' in line_stripped:
            # Key-value pair
            if current_list is not None:
                # Finish previous list
                metadata[current_key] = current_list
                current_list = None
                current_key = None

            key, value = line_stripped.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if not value:
                # This might be a list or multi-line value
                current_key = key
                current_list = []
            else:
                metadata[key] = value

    # Finish any pending list
    if current_list is not None:
        metadata[current_key] = current_list

    # Validate required fields
    required_fields = [
        'resume_schema_version',
        'last_updated',
        'project_id',
        'project_name',
        'current_phase',
        'next_action',
        'files_to_load',
        'current_section',
        'current_task',
        'total_tasks',
        'tasks_completed'
    ]

    missing_fields = []
    for field in required_fields:
        if field not in metadata:
            missing_fields.append(field)

    if missing_fields:
        print(f"ERROR: Missing required fields: {missing_fields}")
        return False

    # Validate field values
    print("PASS: YAML parsing successful!")
    print(f"   - resume_schema_version: {metadata['resume_schema_version']}")
    print(f"   - project_id: {metadata['project_id']}")
    print(f"   - project_name: {metadata['project_name']}")
    print(f"   - current_phase: {metadata['current_phase']}")
    print(f"   - next_action: {metadata['next_action']}")
    print(f"   - files_to_load: {len(metadata['files_to_load'])} files")
    print(f"   - current_section: {metadata['current_section']}")
    print(f"   - current_task: {metadata['current_task']}")
    print(f"   - total_tasks: {metadata['total_tasks']}")
    print(f"   - tasks_completed: {metadata['tasks_completed']}")

    # Validate files_to_load is a list
    if not isinstance(metadata['files_to_load'], list):
        print(f"ERROR: files_to_load should be a list, got {type(metadata['files_to_load'])}")
        return False

    if len(metadata['files_to_load']) != 3:
        print(f"WARNING: Expected 3 files in files_to_load, got {len(metadata['files_to_load'])}")

    # Validate integers
    try:
        int(metadata['current_section'])
        int(metadata['current_task'])
        int(metadata['total_tasks'])
        int(metadata['tasks_completed'])
    except ValueError as e:
        print(f"ERROR: Integer field validation failed: {e}")
        return False

    # Check file size
    file_size = len(content)
    print(f"\nPASS: Template size: {file_size} chars")

    if file_size > 1000:
        print(f"WARNING: Template larger than 1KB ({file_size} chars)")
    else:
        print(f"   PASS: Under 1KB target (saved {1000 - file_size} chars)")

    # Compare to original
    original_file = Path(__file__).parent.parent / "01-planning" / "resume-context.md"
    if original_file.exists():
        original_size = len(original_file.read_text(encoding='utf-8'))
        savings = original_size - file_size
        savings_pct = (savings / original_size) * 100
        print(f"\nPASS: Size comparison:")
        print(f"   - Original: {original_size} chars")
        print(f"   - Optimized: {file_size} chars")
        print(f"   - Savings: {savings} chars ({savings_pct:.1f}%)")

    return True

def test_body_content():
    """Test that body content is minimal."""

    optimized_file = Path(__file__).parent / "resume-context-OPTIMIZED.md"
    content = optimized_file.read_text(encoding='utf-8')

    # Extract body (after second ---)
    parts = content.split('---', 2)
    if len(parts) < 3:
        print("ERROR: Invalid YAML frontmatter structure")
        return False

    body = parts[2].strip()

    # Check for bloat indicators
    bloat_indicators = [
        "# Validation Gate",
        "# Session History",
        "Before continuing, you MUST verify",
        "## Session",
        "⚠️ NEXT SESSION"
    ]

    found_bloat = []
    for indicator in bloat_indicators:
        if indicator in body:
            found_bloat.append(indicator)

    if found_bloat:
        print(f"WARNING: Found bloat indicators in body:")
        for item in found_bloat:
            print(f"   - {item}")
        return False

    print("PASS: Body content is minimal (no bloat detected)")
    print(f"   - Body length: {len(body)} chars")

    # Check that footer exists
    if "*Auto-updated" not in body:
        print("WARNING: Footer note missing")
        return False

    print("PASS: Footer note present")

    return True

if __name__ == "__main__":
    print("Testing Optimized Resume Template")
    print("=" * 50)

    test1 = test_optimized_template_parsing()
    print()
    test2 = test_body_content()

    print("\n" + "=" * 50)
    if test1 and test2:
        print("ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("TESTS FAILED")
        sys.exit(1)
