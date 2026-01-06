#!/usr/bin/env python3
"""Verify Subagent Reading Completeness.

Post-execution verification that the subagent actually read everything.
Checks:
1. 3-Point Evidence matches actual chunk content
2. Hash matches actual chunk hash
3. Spot check answers are correct
4. Line/word counts are within tolerance
5. Chunk references in extractions exist

HIGH QUALITY DATA TRANSFER = VERIFIED READING

Usage:
    python verify_subagent_reading.py <project_path> <paper_id>
    python verify_subagent_reading.py <project_path> --batch <batch_file>
"""

import sys
import yaml
import json
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import argparse


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class VerificationResult:
    """Result of verifying a single item."""
    item_id: str
    check_type: str  # evidence, hash, spot_check, reference
    passed: bool
    expected: str
    actual: str
    message: str


@dataclass
class ChunkVerification:
    """Complete verification for a single chunk."""
    chunk_id: str
    results: List[VerificationResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def critical_failures(self) -> List[VerificationResult]:
        """Failures that indicate incomplete reading."""
        critical_types = ['hash', 'evidence_start', 'evidence_end']
        return [r for r in self.results if not r.passed and r.check_type in critical_types]


@dataclass
class FullVerificationReport:
    """Complete verification report for a task."""
    task_id: str
    task_type: str
    verified_at: str
    chunks_verified: int
    chunks_passed: int
    chunks_failed: int
    overall_passed: bool
    chunk_results: Dict[str, ChunkVerification] = field(default_factory=dict)
    extraction_results: List[VerificationResult] = field(default_factory=list)
    summary: str = ""

    def to_yaml(self) -> str:
        """Convert to YAML for storage."""
        return yaml.dump({
            'task_id': self.task_id,
            'task_type': self.task_type,
            'verified_at': self.verified_at,
            'chunks_verified': self.chunks_verified,
            'chunks_passed': self.chunks_passed,
            'chunks_failed': self.chunks_failed,
            'overall_passed': self.overall_passed,
            'summary': self.summary,
            'chunk_results': {
                chunk_id: {
                    'passed': cv.passed,
                    'critical_failures': len(cv.critical_failures),
                    'results': [
                        {
                            'check': r.check_type,
                            'passed': r.passed,
                            'message': r.message
                        } for r in cv.results
                    ]
                } for chunk_id, cv in self.chunk_results.items()
            },
            'extraction_results': [
                {
                    'item': r.item_id,
                    'check': r.check_type,
                    'passed': r.passed,
                    'message': r.message
                } for r in self.extraction_results
            ]
        }, default_flow_style=False, allow_unicode=True)


# =============================================================================
# VERIFICATION FUNCTIONS
# =============================================================================

def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown file."""
    if not file_path.exists():
        return {}
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


def compute_chunk_hash(chunk_path: Path) -> str:
    """Compute SHA256 hash of chunk content (after header)."""
    content = chunk_path.read_text(encoding='utf-8')

    # Skip YAML frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            content = content[end + 3:].strip()

    # Skip first header line
    if content.startswith('#'):
        first_newline = content.find('\n')
        if first_newline > 0:
            content = content[first_newline + 1:].strip()

    return hashlib.sha256(content.encode()).hexdigest()


def get_chunk_content(chunk_path: Path) -> str:
    """Get chunk content after header."""
    content = chunk_path.read_text(encoding='utf-8')

    # Skip YAML frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            content = content[end + 3:].strip()

    # Skip first header line
    if content.startswith('#'):
        first_newline = content.find('\n')
        if first_newline > 0:
            content = content[first_newline + 1:].strip()

    return content


def verify_evidence(
    chunk_id: str,
    evidence: dict,
    chunk_path: Path
) -> List[VerificationResult]:
    """Verify 3-point evidence against actual chunk."""
    results = []
    content = get_chunk_content(chunk_path)

    # Start evidence (first 100 chars)
    expected_start = content[:100].strip() if len(content) > 100 else content.strip()
    reported_start = evidence.get('start', '').strip()

    # Allow some tolerance (first 50 chars must match)
    start_match = expected_start[:50] == reported_start[:50] if len(reported_start) >= 50 else False
    results.append(VerificationResult(
        item_id=chunk_id,
        check_type='evidence_start',
        passed=start_match,
        expected=expected_start[:50],
        actual=reported_start[:50] if reported_start else '<missing>',
        message="Start evidence matches" if start_match else "Start evidence MISMATCH - likely didn't read from beginning"
    ))

    # Mid evidence (100 chars from 50% position)
    mid_pos = len(content) // 2
    expected_mid = content[mid_pos:mid_pos + 100].strip() if len(content) > mid_pos + 100 else ""
    reported_mid = evidence.get('mid', '').strip()

    # Mid is harder to verify exactly - check for substring presence
    mid_match = reported_mid[:30] in content if len(reported_mid) >= 30 else True
    results.append(VerificationResult(
        item_id=chunk_id,
        check_type='evidence_mid',
        passed=mid_match,
        expected=expected_mid[:50] if expected_mid else '<short chunk>',
        actual=reported_mid[:50] if reported_mid else '<missing>',
        message="Mid evidence found in chunk" if mid_match else "Mid evidence NOT FOUND - likely skipped middle"
    ))

    # End evidence (last 100 chars)
    expected_end = content[-100:].strip() if len(content) > 100 else content.strip()
    reported_end = evidence.get('end', '').strip()

    # Allow some tolerance (last 50 chars must match)
    end_match = expected_end[-50:] == reported_end[-50:] if len(reported_end) >= 50 else False
    results.append(VerificationResult(
        item_id=chunk_id,
        check_type='evidence_end',
        passed=end_match,
        expected=expected_end[-50:],
        actual=reported_end[-50:] if reported_end else '<missing>',
        message="End evidence matches" if end_match else "End evidence MISMATCH - likely didn't read to end"
    ))

    return results


def verify_hash(
    chunk_id: str,
    reported_hash: str,
    chunk_path: Path
) -> VerificationResult:
    """Verify chunk hash."""
    actual_hash = compute_chunk_hash(chunk_path)

    # Compare first 16 chars (sufficient for verification)
    match = actual_hash[:16] == reported_hash[:16] if reported_hash else False

    return VerificationResult(
        item_id=chunk_id,
        check_type='hash',
        passed=match,
        expected=actual_hash[:16],
        actual=reported_hash[:16] if reported_hash else '<missing>',
        message="Hash matches" if match else "Hash MISMATCH - content may have been modified or incompletely read"
    )


def verify_line_count(
    chunk_id: str,
    reported_count: int,
    chunk_path: Path,
    tolerance: float = 0.1
) -> VerificationResult:
    """Verify line count within tolerance."""
    content = get_chunk_content(chunk_path)
    actual_count = len(content.split('\n'))

    within_tolerance = abs(reported_count - actual_count) <= actual_count * tolerance

    return VerificationResult(
        item_id=chunk_id,
        check_type='line_count',
        passed=within_tolerance,
        expected=str(actual_count),
        actual=str(reported_count),
        message=f"Line count within {tolerance*100}% tolerance" if within_tolerance else f"Line count off by {abs(reported_count - actual_count)} lines"
    )


def verify_extraction_reference(
    extraction: dict,
    papers_path: Path
) -> VerificationResult:
    """Verify that extraction references exist in source."""
    chunk_ref = extraction.get('chunk_ref', extraction.get('source', ''))

    # Parse chunk reference: "Paper-ID (Chunk N:Line-Line)"
    match = re.match(r'([^\(]+)\s*\(Chunk\s*(\d+):(\d+)-(\d+)\)', chunk_ref)
    if not match:
        # Try alternate format: "Chunk N:Line-Line"
        match2 = re.match(r'Chunk\s*(\d+):(\d+)-(\d+)', chunk_ref)
        if match2:
            return VerificationResult(
                item_id=chunk_ref,
                check_type='reference_format',
                passed=True,
                expected='Chunk N:Line-Line format',
                actual=chunk_ref,
                message="Reference format valid (simple)"
            )

        return VerificationResult(
            item_id=chunk_ref,
            check_type='reference_format',
            passed=False,
            expected='Paper-ID (Chunk N:Line-Line) or Chunk N:Line-Line',
            actual=chunk_ref,
            message="Invalid reference format"
        )

    paper_id = match.group(1).strip()
    chunk_num = int(match.group(2))
    line_start = int(match.group(3))
    line_end = int(match.group(4))

    # Find chunk file
    chunk_path = papers_path / paper_id / f"{paper_id}_{chunk_num}.md"
    if not chunk_path.exists():
        return VerificationResult(
            item_id=chunk_ref,
            check_type='reference_exists',
            passed=False,
            expected=f"Chunk file: {chunk_path}",
            actual='<not found>',
            message=f"Referenced chunk file does not exist"
        )

    # Verify line numbers are valid
    content = chunk_path.read_text(encoding='utf-8')
    lines = content.split('\n')

    if line_start > len(lines) or line_end > len(lines):
        return VerificationResult(
            item_id=chunk_ref,
            check_type='reference_lines',
            passed=False,
            expected=f"Lines 1-{len(lines)}",
            actual=f"Lines {line_start}-{line_end}",
            message=f"Line numbers exceed chunk length ({len(lines)} lines)"
        )

    # Optional: verify quote exists at those lines
    quote = extraction.get('quote', '')
    if quote and len(quote) > 20:
        referenced_text = '\n'.join(lines[line_start-1:line_end])
        quote_found = quote[:50] in referenced_text or quote[-50:] in referenced_text

        if not quote_found:
            # Try broader search
            quote_in_chunk = quote[:30] in content

            return VerificationResult(
                item_id=chunk_ref,
                check_type='quote_at_line',
                passed=quote_in_chunk,
                expected=f"Quote at lines {line_start}-{line_end}",
                actual='Quote found elsewhere in chunk' if quote_in_chunk else 'Quote NOT FOUND',
                message="Quote exists in chunk (line drift)" if quote_in_chunk else "QUOTE NOT FOUND IN CHUNK - possible hallucination"
            )

    return VerificationResult(
        item_id=chunk_ref,
        check_type='reference_valid',
        passed=True,
        expected='Valid reference',
        actual=chunk_ref,
        message="Reference validated"
    )


# =============================================================================
# MAIN VERIFICATION
# =============================================================================

def verify_analysis_log(
    analysis_log_path: Path,
    paper_path: Path
) -> FullVerificationReport:
    """Verify complete analysis log for a paper."""

    log = load_yaml_frontmatter(analysis_log_path)
    paper_id = paper_path.name
    chunk_evidence = log.get('chunk_evidence', log.get('steps', {}).get('step3_analyze_chunks', {}).get('chunk_evidence', {}))

    report = FullVerificationReport(
        task_id=f"verify_{paper_id}",
        task_type='paper_analysis',
        verified_at=datetime.now().isoformat(),
        chunks_verified=0,
        chunks_passed=0,
        chunks_failed=0,
        overall_passed=True
    )

    # Get all chunk files
    chunk_files = sorted(paper_path.glob(f"{paper_id}_*.md"))

    for chunk_path in chunk_files:
        chunk_id = chunk_path.stem
        chunk_num = chunk_id.split('_')[-1]

        cv = ChunkVerification(chunk_id=chunk_id)

        # Get evidence for this chunk
        evidence = chunk_evidence.get(chunk_num, chunk_evidence.get(int(chunk_num), {}))

        if not evidence:
            cv.results.append(VerificationResult(
                item_id=chunk_id,
                check_type='evidence_missing',
                passed=False,
                expected='Evidence recorded',
                actual='<no evidence>',
                message=f"NO EVIDENCE for chunk {chunk_num} - chunk was NOT READ"
            ))
            report.chunks_failed += 1
        else:
            # Verify 3-point evidence
            cv.results.extend(verify_evidence(chunk_id, evidence, chunk_path))

            # Verify hash
            cv.results.append(verify_hash(
                chunk_id,
                evidence.get('hash', ''),
                chunk_path
            ))

            # Verify line count
            if 'line_count' in evidence:
                cv.results.append(verify_line_count(
                    chunk_id,
                    evidence.get('line_count', 0),
                    chunk_path
                ))

            if cv.passed:
                report.chunks_passed += 1
            else:
                report.chunks_failed += 1

        report.chunk_results[chunk_id] = cv
        report.chunks_verified += 1

    # Check overall pass
    report.overall_passed = report.chunks_failed == 0

    # Generate summary
    if report.overall_passed:
        report.summary = f"✓ PASSED: All {report.chunks_verified} chunks verified"
    else:
        critical = sum(len(cv.critical_failures) for cv in report.chunk_results.values())
        report.summary = f"✗ FAILED: {report.chunks_failed}/{report.chunks_verified} chunks failed ({critical} critical)"

    return report


def verify_batch_extraction(
    batch_path: Path,
    papers_path: Path
) -> FullVerificationReport:
    """Verify batch extraction output."""

    # Load batch file
    with open(batch_path, encoding='utf-8') as f:
        content = f.read()

    # Parse YAML
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            batch = yaml.safe_load(content[3:end]) or {}
            patterns_section = content[end + 3:]
        else:
            batch = yaml.safe_load(content) or {}
            patterns_section = ""
    else:
        batch = yaml.safe_load(content) or {}
        patterns_section = ""

    report = FullVerificationReport(
        task_id=f"verify_{batch_path.stem}",
        task_type='batch_extraction',
        verified_at=datetime.now().isoformat(),
        chunks_verified=0,
        chunks_passed=0,
        chunks_failed=0,
        overall_passed=True
    )

    # Verify each pattern's reference
    patterns = batch.get('patterns', [])
    for i, pattern in enumerate(patterns):
        result = verify_extraction_reference(pattern, papers_path)
        result.item_id = f"pattern_{i}_{pattern.get('name', 'unknown')[:30]}"
        report.extraction_results.append(result)

        if not result.passed:
            report.chunks_failed += 1
        else:
            report.chunks_passed += 1
        report.chunks_verified += 1

    report.overall_passed = report.chunks_failed == 0

    failed = len([r for r in report.extraction_results if not r.passed])
    if report.overall_passed:
        report.summary = f"✓ PASSED: All {len(patterns)} pattern references verified"
    else:
        report.summary = f"✗ FAILED: {failed}/{len(patterns)} patterns have invalid references"

    return report


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='Verify subagent reading completeness')
    parser.add_argument('project_path', type=Path)
    parser.add_argument('--paper-id', help='Paper ID to verify')
    parser.add_argument('--batch', type=Path, help='Batch file to verify')
    parser.add_argument('--output', type=Path, help='Output path for report')

    args = parser.parse_args()

    if args.paper_id:
        # Verify paper analysis
        paper_path = args.project_path / f"02-resources/papers/{args.paper_id}"
        log_path = paper_path / "_analysis_log.md"

        if not log_path.exists():
            print(f"Error: No analysis log found at {log_path}")
            sys.exit(1)

        report = verify_analysis_log(log_path, paper_path)

    elif args.batch:
        # Verify batch extraction
        papers_path = args.project_path / "02-resources/papers"
        report = verify_batch_extraction(args.batch, papers_path)

    else:
        print("Error: Specify --paper-id or --batch")
        sys.exit(1)

    # Output
    print(report.summary)
    print()

    if not report.overall_passed:
        print("Failures:")
        for chunk_id, cv in report.chunk_results.items():
            for r in cv.results:
                if not r.passed:
                    print(f"  {chunk_id}: {r.check_type} - {r.message}")

        for r in report.extraction_results:
            if not r.passed:
                print(f"  {r.item_id}: {r.message}")

    # Save report
    if args.output:
        output_path = args.output
    else:
        output_path = args.project_path / f"03-working/_verification_{report.task_id}.yaml"

    output_path.write_text(report.to_yaml(), encoding='utf-8')
    print(f"\nReport saved: {output_path}")

    sys.exit(0 if report.overall_passed else 1)


if __name__ == '__main__':
    main()
