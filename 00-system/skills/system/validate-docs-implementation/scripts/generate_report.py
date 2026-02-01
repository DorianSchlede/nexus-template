#!/usr/bin/env python3
"""
Validation Report Generator

Helper script to generate validation reports from structured data.
While AI can generate reports manually, this script provides:
- Consistent formatting
- Automatic statistics calculation
- Metadata generation
- File management (overwrite protection)

Usage:
    python generate_report.py --implementation "init-build" \\
                              --data report_data.json \\
                              --output-dir "04-workspace/validation-reports/"

Or interactively:
    python generate_report.py --interactive
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Configure UTF-8 output for cross-platform compatibility
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass  # Python < 3.7


def sanitize_filename(name: str) -> str:
    """Convert implementation name to safe filename component."""
    # Remove/replace unsafe characters
    safe = name.lower().replace(' ', '-').replace('_', '-')
    safe = ''.join(c for c in safe if c.isalnum() or c == '-')
    safe = safe.strip('-')
    return safe


def generate_filename(implementation: str, date: str = None) -> str:
    """Generate report filename."""
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    safe_name = sanitize_filename(implementation)
    return f"validation-{safe_name}-{date}.md"


def calculate_statistics(data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate report statistics from data."""
    stats = {}

    # File counts
    files_updated = data.get('files_updated', [])
    stats['files_updated_count'] = len(files_updated)

    # Total changes
    total_changes = sum(
        len(f.get('changes', [])) for f in files_updated
    )
    stats['total_changes'] = total_changes

    # Average changes per file
    stats['avg_changes_per_file'] = (
        round(total_changes / len(files_updated), 1)
        if files_updated else 0
    )

    # Largest update
    if files_updated:
        largest = max(files_updated, key=lambda f: len(f.get('changes', [])))
        stats['largest_update'] = {
            'file': largest.get('path', 'unknown'),
            'changes': len(largest.get('changes', []))
        }
    else:
        stats['largest_update'] = None

    # Mismatch counts by type
    mismatches = data.get('mismatches', {})
    stats['mismatch_types'] = {
        mtype: len(items)
        for mtype, items in mismatches.items()
    }

    return stats


def format_change(change: Dict[str, Any], index: int) -> str:
    """Format a single change for the report."""
    lines = []

    lines.append(f"**Change {index + 1}**:")
    lines.append("```markdown")

    # Line reference
    if 'line' in change:
        lines.append(f"Line {change['line']}:")
    elif 'lines' in change:
        lines.append(f"Lines {change['lines']}:")

    # Old/New
    lines.append(f"OLD: {change.get('old', '[not specified]')}")
    lines.append(f"NEW: {change.get('new', '[not specified]')}")

    # Reason
    if 'reason' in change:
        lines.append(f"Reason: {change['reason']}")

    lines.append("```")
    lines.append("")

    return "\n".join(lines)


def generate_report(data: Dict[str, Any]) -> str:
    """Generate full validation report from structured data."""

    impl_name = data.get('implementation', 'Unknown')
    date = data.get('date', datetime.now().strftime("%Y-%m-%d"))
    scope = data.get('scope', 'System-wide')
    thoroughness = data.get('thoroughness', 'Comprehensive')

    stats = calculate_statistics(data)

    # Build report
    lines = [
        "# Documentation Validation Report",
        "",
        f"**Implementation**: {impl_name}",
        f"**Date**: {date}",
        f"**Validation ID**: {generate_filename(impl_name, date).replace('.md', '')}",
        f"**Scope**: {scope}",
        f"**Thoroughness**: {thoroughness}",
        "",
        "---",
        "",
        "## Executive Summary",
        "",
    ]

    # Status
    status = data.get('status', 'complete')
    status_icon = {
        'complete': '[OK]',
        'partial': '[!]',
        'issues': '[ERROR]'
    }.get(status, '[?]')

    status_text = {
        'complete': 'All documentation matches implementation',
        'partial': 'Partial fixes applied',
        'issues': 'Issues remain'
    }.get(status, 'Unknown status')

    lines.extend([
        f"**Status**: {status_icon} {status_text}",
        "",
        "**Key Findings**:",
    ])

    for finding in data.get('key_findings', []):
        lines.append(f"- {finding}")

    lines.extend([
        "",
        "**Actions Taken**:",
        f"- Files updated: {stats['files_updated_count']}",
        f"- Total fixes: {stats['total_changes']}",
        f"- Verification: {data.get('verification_status', 'Unknown')}",
        "",
        "---",
        "",
        "## Implementation Analysis",
        "",
        "### What the Code Actually Does",
        "",
        data.get('implementation_summary', '[Summary not provided]'),
        "",
        "**Creates**:",
    ])

    for item in data.get('creates', []):
        lines.append(f"- {item}")

    lines.extend(["", "**Does NOT Create** (documented but missing):"])

    for item in data.get('does_not_create', []):
        lines.append(f"- {item}")

    lines.extend([
        "",
        "---",
        "",
        "## Mismatches Identified",
        "",
        "### By Type",
        "",
        "| Type | Count | Examples |",
        "|------|-------|----------|",
    ])

    for mtype, items in data.get('mismatches', {}).items():
        examples = ", ".join(items[:3])  # First 3 examples
        lines.append(f"| {mtype} | {len(items)} | {examples} |")

    lines.extend([
        "",
        f"**Total Mismatches**: {stats['total_changes']}",
        "",
        "---",
        "",
        "## Fixes Applied",
        "",
        "### File-by-File Changes",
        "",
    ])

    # Files updated
    for i, file_data in enumerate(data.get('files_updated', []), 1):
        lines.extend([
            f"#### {i}. {file_data.get('name', 'Unknown file')}",
            "",
            f"**Location**: `{file_data.get('path', 'unknown')}`",
            f"**Priority**: {file_data.get('priority', 'Medium')}",
            f"**Changes**: {len(file_data.get('changes', []))}",
            "",
        ])

        for j, change in enumerate(file_data.get('changes', [])):
            lines.append(format_change(change, j))

        lines.append("---")
        lines.append("")

    # Verification
    lines.extend([
        "## Verification Results",
        "",
        "### Re-Search Verification",
        "",
        "| Old Term | Expected Result | Actual Result | Status |",
        "|----------|-----------------|---------------|--------|",
    ])

    for check in data.get('verification_checks', []):
        term = check.get('term', '')
        expected = check.get('expected', '0 results')
        actual = check.get('actual', '0 results')
        passed = check.get('passed', True)
        status = '[OK] Pass' if passed else '[ERROR] Fail'
        lines.append(f"| `{term}` | {expected} | {actual} | {status} |")

    overall_verification = data.get('verification_status', 'Pass')
    verification_icon = '[OK]' if overall_verification == 'Pass' else '[ERROR]'

    lines.extend([
        "",
        f"**Overall Verification**: {verification_icon} {overall_verification}",
        "",
        "---",
        "",
        "## Statistics",
        "",
        "### Change Metrics",
        "",
        f"- **Files Updated**: {stats['files_updated_count']}",
        f"- **Total Changes**: {stats['total_changes']}",
        f"- **Average Changes per File**: {stats['avg_changes_per_file']}",
    ])

    if stats['largest_update']:
        lines.append(
            f"- **Largest Update**: {stats['largest_update']['file']} "
            f"({stats['largest_update']['changes']} changes)"
        )

    lines.extend([
        "",
        "---",
        "",
        "## Status",
        "",
        f"{status_icon} **Documentation Status**: {status_text}",
        "",
    ])

    # Recommendations
    if data.get('recommendations'):
        lines.extend([
            "## Recommendations",
            "",
            "### Immediate Next Steps",
            "",
        ])
        for rec in data.get('recommendations', []):
            lines.append(f"1. {rec}")

    lines.extend([
        "",
        "---",
        "",
        "## Metadata",
        "",
        "**Generated By**: validate-docs-implementation skill",
        "**Report Version**: 1.0",
        "**Report Format**: Markdown",
        f"**Generated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "---",
        "",
        "**End of Report**",
    ])

    return "\n".join(lines)


def save_report(content: str, output_dir: str, filename: str) -> Path:
    """Save report to file, handling overwrites."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / filename

    # Handle overwrites
    if file_path.exists():
        timestamp = datetime.now().strftime("%H%M%S")
        base = filename.replace('.md', '')
        filename = f"{base}-{timestamp}.md"
        file_path = output_path / filename

    file_path.write_text(content, encoding='utf-8')
    return file_path


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py --data <json-file> --output-dir <dir>")
        print("   or: python generate_report.py --interactive")
        sys.exit(1)

    if '--interactive' in sys.argv:
        print("Interactive mode not yet implemented.")
        print("Please provide report data as JSON file.")
        sys.exit(1)

    # Parse args
    try:
        data_file_idx = sys.argv.index('--data') + 1
        data_file = sys.argv[data_file_idx]
    except (ValueError, IndexError):
        print("ERROR: --data <json-file> required")
        sys.exit(1)

    try:
        output_dir_idx = sys.argv.index('--output-dir') + 1
        output_dir = sys.argv[output_dir_idx]
    except (ValueError, IndexError):
        output_dir = "04-workspace/validation-reports/"

    # Load data
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Data file not found: {data_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        sys.exit(1)

    # Generate report
    report_content = generate_report(data)

    # Save report
    impl_name = data.get('implementation', 'unknown')
    filename = generate_filename(impl_name)

    saved_path = save_report(report_content, output_dir, filename)

    print(f"[OK] Report generated successfully!")
    print(f"[FILE] Saved to: {saved_path}")
    print(f"")
    print(f"Summary:")
    print(f"- Implementation: {impl_name}")
    print(f"- Files updated: {len(data.get('files_updated', []))}")
    print(f"- Total changes: {calculate_statistics(data)['total_changes']}")


if __name__ == '__main__':
    main()
