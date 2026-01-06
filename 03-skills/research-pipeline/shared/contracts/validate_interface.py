#!/usr/bin/env python3
"""
Interface Validation Script

Validates that analysis outputs match the expected schema before synthesis begins.
This script bridges the gap between analyze-research-project and synthesize-research-project.

Usage:
    python validate_interface.py PROJECT_PATH [--fix]

    --fix: Attempt to convert markdown format to YAML frontmatter format

Exit codes:
    0: All papers have valid chunk_index
    1: Some papers missing chunk_index (synthesis will fail)
    2: Project path not found
"""

import sys
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
import yaml

# Standard token formula (single source of truth)
TOKEN_FORMULA = lambda chars: chars // 4


def parse_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def validate_chunk_index(frontmatter: Dict[str, Any], paper_id: str) -> Tuple[bool, List[str]]:
    """Validate chunk_index structure against schema."""
    errors = []

    # Check required fields
    if 'chunk_index' not in frontmatter:
        errors.append(f"{paper_id}: Missing 'chunk_index' in frontmatter")
        return False, errors

    chunk_index = frontmatter['chunk_index']
    if not isinstance(chunk_index, dict):
        errors.append(f"{paper_id}: 'chunk_index' must be a dictionary, got {type(chunk_index)}")
        return False, errors

    if len(chunk_index) == 0:
        errors.append(f"{paper_id}: 'chunk_index' is empty")
        return False, errors

    # Validate each chunk entry
    for chunk_num, chunk_data in chunk_index.items():
        if not isinstance(chunk_data, dict):
            errors.append(f"{paper_id}: chunk_index[{chunk_num}] must be a dictionary")
            continue

        if 'token_count' not in chunk_data:
            errors.append(f"{paper_id}: chunk_index[{chunk_num}] missing 'token_count'")

        if 'fields_found' not in chunk_data:
            errors.append(f"{paper_id}: chunk_index[{chunk_num}] missing 'fields_found'")
        elif not isinstance(chunk_data.get('fields_found'), dict):
            errors.append(f"{paper_id}: chunk_index[{chunk_num}].fields_found must be a dictionary")

    # Check schema version
    if frontmatter.get('schema_version') != '2.3':
        errors.append(f"{paper_id}: schema_version should be '2.3', got '{frontmatter.get('schema_version')}'")

    return len(errors) == 0, errors


def extract_fields_from_markdown(content: str) -> Dict[str, Any]:
    """
    Attempt to extract field information from markdown format (fallback parsing).
    This handles the case where subagents produced markdown with embedded YAML
    instead of YAML frontmatter.
    """
    fields_found = {}

    # Look for embedded YAML code blocks
    yaml_blocks = re.findall(r'```yaml\n(.*?)```', content, re.DOTALL)

    for block in yaml_blocks:
        try:
            parsed = yaml.safe_load(block)
            if isinstance(parsed, dict):
                # Check if it looks like a field extraction
                for key, value in parsed.items():
                    if isinstance(value, list) and len(value) > 0:
                        fields_found[key] = True
                    elif value and value != 'N/A':
                        fields_found[key] = True if value else False
        except yaml.YAMLError:
            continue

    return fields_found


def validate_project(project_path: Path) -> Tuple[int, int, List[str]]:
    """
    Validate all papers in a project.

    Returns:
        (valid_count, total_count, all_errors)
    """
    papers_path = project_path / "02-resources" / "papers"
    if not papers_path.exists():
        return 0, 0, [f"Papers directory not found: {papers_path}"]

    valid_count = 0
    total_count = 0
    all_errors = []

    for paper_dir in papers_path.iterdir():
        if not paper_dir.is_dir():
            continue

        index_path = paper_dir / "index.md"
        if not index_path.exists():
            continue

        total_count += 1
        content = index_path.read_text(encoding='utf-8')
        frontmatter = parse_yaml_frontmatter(content)

        is_valid, errors = validate_chunk_index(frontmatter, paper_dir.name)

        if is_valid:
            valid_count += 1
        else:
            all_errors.extend(errors)

            # Check if it's markdown format (potential fix candidate)
            if not frontmatter and '```yaml' in content:
                all_errors.append(f"  -> {paper_dir.name}: Appears to be markdown format (fixable with --fix)")

    return valid_count, total_count, all_errors


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_interface.py PROJECT_PATH [--fix]")
        sys.exit(2)

    project_path = Path(sys.argv[1])
    fix_mode = '--fix' in sys.argv

    if not project_path.exists():
        print(f"ERROR: Project path not found: {project_path}")
        sys.exit(2)

    print(f"Validating interface: {project_path}")
    print("=" * 60)

    valid_count, total_count, errors = validate_project(project_path)

    print(f"\nResults:")
    print(f"  Valid papers (with chunk_index): {valid_count}/{total_count}")
    print(f"  Invalid papers: {total_count - valid_count}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:20]:  # Limit output
            print(f"  - {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")

    if valid_count == total_count:
        print("\n[PASS] All papers have valid chunk_index. Synthesis can proceed.")
        sys.exit(0)
    else:
        print(f"\n[FAIL] {total_count - valid_count} papers missing chunk_index.")
        print("Synthesis pipeline will fail. Options:")
        print("  1. Re-analyze papers with updated skill (includes YAML template)")
        print("  2. Run with --fix to attempt automatic conversion")
        sys.exit(1)


if __name__ == "__main__":
    main()
