#!/usr/bin/env python3
"""
verify_subagent_output.py - Level 5 of 7-Level Synthesis Architecture

Verifies subagent extraction outputs with quote-line verification (Gap G15).
Samples patterns and checks if quoted text exists at cited line numbers.

Usage:
    python verify_subagent_output.py PROJECT_PATH --input-dir WORKING_DIR --sample-rate 0.1 --output REPORT_FILE
"""

import argparse
import sys
import re
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import yaml


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file, handling multi-document YAML (frontmatter + body)."""
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Handle multi-document YAML (frontmatter + body pattern)
    # Merge all documents into a single dict
    result = {}
    for doc in yaml.safe_load_all(content):
        if doc:
            result.update(doc)
    return result


def parse_chunk_ref(chunk_ref: str) -> Optional[Tuple[str, int, int, int]]:
    """
    Parse chunk reference format: "Paper-ID (Chunk N:Line-Line)"

    Returns: (paper_id, chunk_num, start_line, end_line) or None if invalid
    """
    # Pattern: "Paper-ID (Chunk N:Line-Line)" or "Paper-ID (Chunk N:Line)"
    pattern = r'^(.+?)\s*\(Chunk\s*(\d+):(\d+)(?:-(\d+))?\)$'
    match = re.match(pattern, chunk_ref)

    if not match:
        return None

    paper_id = match.group(1).strip()
    chunk_num = int(match.group(2))
    start_line = int(match.group(3))
    end_line = int(match.group(4)) if match.group(4) else start_line

    return (paper_id, chunk_num, start_line, end_line)


def read_chunk_file(project_path: Path, paper_id: str, chunk_num: int) -> Optional[List[str]]:
    """Read chunk file and return lines."""
    chunk_path = project_path / "02-resources" / "papers" / paper_id / f"{paper_id}_{chunk_num}.md"

    if not chunk_path.exists():
        return None

    content = chunk_path.read_text(encoding='utf-8')
    return content.split('\n')


def verify_quote_at_lines(
    lines: List[str],
    start_line: int,
    end_line: int,
    expected_quote: str,
    tolerance: int = 5
) -> Tuple[bool, str]:
    """
    Check if quote exists at or near the cited lines.

    Args:
        lines: File content as list of lines
        start_line: Expected start line (1-indexed)
        end_line: Expected end line (1-indexed)
        expected_quote: Quote to find
        tolerance: Lines to search around the cited range

    Returns:
        (verified: bool, actual_text: str)
    """
    # Normalize quote for comparison
    quote_normalized = expected_quote.lower().strip()[:50]  # First 50 chars

    # Adjust for 0-indexing and add tolerance
    search_start = max(0, start_line - 1 - tolerance)
    search_end = min(len(lines), end_line + tolerance)

    # Get text in search range
    search_text = ' '.join(lines[search_start:search_end]).lower()

    # Check if normalized quote is in search range
    if quote_normalized in search_text:
        return (True, lines[start_line - 1] if start_line <= len(lines) else "")

    # Return what we actually found at the cited lines
    actual_start = max(0, start_line - 1)
    actual_end = min(len(lines), end_line)
    actual_text = ' '.join(lines[actual_start:actual_end])[:100]

    return (False, actual_text)


def verify_batch(project_path: Path, batch_path: Path, sample_rate: float) -> Dict[str, Any]:
    """
    Verify a single batch file.

    Returns verification report for this batch.
    """
    batch_data = load_yaml(batch_path)
    batch_id = batch_data.get('batch_id', batch_path.stem)
    patterns = batch_data.get('patterns', [])

    if not patterns:
        return {
            'batch_id': batch_id,
            'patterns_total': 0,
            'patterns_sampled': 0,
            'verified': 0,
            'failed': 0,
            'failures': []
        }

    # Sample patterns
    sample_size = max(1, int(len(patterns) * sample_rate))
    sampled_patterns = random.sample(patterns, min(sample_size, len(patterns)))

    verified = 0
    failed = 0
    failures = []

    for pattern in sampled_patterns:
        name = pattern.get('name', 'Unknown')
        chunk_ref = pattern.get('chunk_ref', '')
        quote = pattern.get('quote', '')

        # Parse chunk reference
        parsed = parse_chunk_ref(chunk_ref)
        if not parsed:
            failures.append({
                'pattern': name,
                'chunk_ref': chunk_ref,
                'verdict': 'FAIL - Invalid chunk_ref format'
            })
            failed += 1
            continue

        paper_id, chunk_num, start_line, end_line = parsed

        # Read chunk file
        lines = read_chunk_file(project_path, paper_id, chunk_num)
        if lines is None:
            failures.append({
                'pattern': name,
                'chunk_ref': chunk_ref,
                'verdict': f'FAIL - Chunk file not found: {paper_id}_{chunk_num}.md'
            })
            failed += 1
            continue

        # Verify quote
        is_verified, actual_text = verify_quote_at_lines(lines, start_line, end_line, quote)

        if is_verified:
            verified += 1
        else:
            failures.append({
                'pattern': name,
                'chunk_ref': chunk_ref,
                'expected_quote': quote[:80] + '...' if len(quote) > 80 else quote,
                'actual_at_lines': actual_text[:80] + '...' if len(actual_text) > 80 else actual_text,
                'verdict': 'FAIL - Quote mismatch'
            })
            failed += 1

    return {
        'batch_id': batch_id,
        'patterns_total': len(patterns),
        'patterns_sampled': len(sampled_patterns),
        'verified': verified,
        'failed': failed,
        'failures': failures
    }


def main():
    parser = argparse.ArgumentParser(
        description='Verify subagent outputs with quote-line checking (Level 5 of 7-Level Architecture)'
    )
    parser.add_argument('project_path', type=Path, help='Path to research project')
    parser.add_argument('--input-dir', '-i', type=Path, required=True, help='Directory with batch YAML files')
    parser.add_argument('--sample-rate', '-s', type=float, default=0.1, help='Fraction of patterns to sample (default: 0.1)')
    parser.add_argument('--output', '-o', type=Path, required=True, help='Output verification report YAML')
    args = parser.parse_args()

    project_path = args.project_path
    if not project_path.is_absolute():
        project_path = Path.cwd() / project_path

    # Resolve input dir
    input_dir = args.input_dir
    if not input_dir.is_absolute():
        input_dir = project_path / input_dir

    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}", file=sys.stderr)
        sys.exit(1)

    # Find batch files
    batch_files = list(input_dir.glob('_batch_*.yaml'))
    if not batch_files:
        print(f"ERROR: No batch files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(batch_files)} batch files")
    print(f"Sample rate: {args.sample_rate:.0%}")

    # Verify each batch
    total_sampled = 0
    total_verified = 0
    total_failed = 0
    all_failures = []

    for batch_path in batch_files:
        result = verify_batch(project_path, batch_path, args.sample_rate)
        total_sampled += result['patterns_sampled']
        total_verified += result['verified']
        total_failed += result['failed']
        all_failures.extend(result['failures'])

        status = "OK" if result['failed'] == 0 else "FAIL"
        print(f"  [{status}] {result['batch_id']}: {result['verified']}/{result['patterns_sampled']} verified")

    # Calculate verification rate
    verification_rate = (total_verified / total_sampled * 100) if total_sampled > 0 else 0
    threshold = 90.0
    verdict = 'PASS' if verification_rate >= threshold else 'FAIL'

    # Build report
    report = {
        'verified_at': datetime.now().isoformat(),
        'sample_rate': args.sample_rate,
        'batches_checked': len(batch_files),
        'patterns_sampled': total_sampled,
        'patterns_verified': total_verified,
        'patterns_failed': total_failed,
        'failures': all_failures[:20],  # Limit to first 20 failures
        'stats': {
            'verification_rate': f"{verification_rate:.1f}%",
            'threshold': f"{threshold:.0f}%",
            'verdict': verdict
        }
    }

    # Write report
    output_path = args.output
    if not output_path.is_absolute():
        output_path = project_path / output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        yaml.dump(report, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

    print(f"\nLevel 5 Complete: Verification report written to {output_path}")
    print(f"\n{'='*50}")
    print(f"VERIFICATION RESULTS (Gap G15)")
    print(f"{'='*50}")
    print(f"Batches checked:    {len(batch_files)}")
    print(f"Patterns sampled:   {total_sampled}")
    print(f"Patterns verified:  {total_verified} ({verification_rate:.1f}%)")
    print(f"Patterns failed:    {total_failed}")
    print(f"\nVerdict: {verdict} ({verification_rate:.1f}% {'≥' if verdict == 'PASS' else '<'} {threshold:.0f}% threshold)")

    if verdict == 'FAIL':
        print(f"\n⚠️  Verification failed. Re-extract worst-performing batches.")
        sys.exit(1)


if __name__ == '__main__':
    main()
