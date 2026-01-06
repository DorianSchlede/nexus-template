#!/usr/bin/env python3
"""
validate_analysis.py - Validate paper analysis logs against Schema v2.0-2.2

Validates:
- Schema version (2.0, 2.1, 2.2 with 3-point evidence)
- All steps completed
- All chunks read in order
- 3-point evidence integrity (start, mid, end, hash)
- Quote cross-validation

Usage:
    python validate_analysis.py {collection_path}
    python validate_analysis.py {collection_path} --paper {paper_name}
    python validate_analysis.py {collection_path} --strict
    python validate_analysis.py {collection_path} --output report.md

Examples:
    python validate_analysis.py 04-workspace/papers/TA_LLM
    python validate_analysis.py 02-projects/08-research/02-resources --strict
"""

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Try to import yaml, fall back to basic parsing if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def parse_yaml_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return None

    # Find end of frontmatter
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return None

    yaml_content = content[3:end_match.start() + 3]

    if HAS_YAML:
        try:
            return yaml.safe_load(yaml_content)
        except yaml.YAMLError as e:
            return {"_parse_error": str(e)}
    else:
        # Basic parsing without yaml library
        return {"_parse_error": "PyYAML not installed, cannot parse YAML"}


def read_file(path: Path) -> Optional[str]:
    """Read file content, return None if not found."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except (FileNotFoundError, IOError):
        return None


def compute_hash(content: str) -> str:
    """Compute SHA256 hash of content."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def get_content_after_header(content: str) -> str:
    """Get content after the first header line (# ...)."""
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('#'):
            # Return everything after this line
            return '\n'.join(lines[i + 1:]).lstrip('\n')
    # No header found, return original
    return content


class ValidationResult:
    """Result of validating a single paper."""

    def __init__(self, paper_id: str, paper_path: Path):
        self.paper_id = paper_id
        self.paper_path = paper_path
        self.status = "PENDING"  # PASSED, FAILED, WARNING, SKIPPED
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: Dict[str, Any] = {}

    def fail(self, reason: str):
        self.status = "FAILED"
        self.errors.append(reason)

    def warn(self, reason: str):
        if self.status not in ("FAILED",):
            self.status = "WARNING"
        self.warnings.append(reason)

    def passed(self):
        if self.status == "PENDING":
            self.status = "PASSED"

    def skip(self, reason: str):
        self.status = "SKIPPED"
        self.info["skip_reason"] = reason

    def to_dict(self) -> Dict[str, Any]:
        return {
            "paper_id": self.paper_id,
            "paper_path": str(self.paper_path),
            "status": self.status,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }


def validate_paper(paper_path: Path, strict: bool = False) -> ValidationResult:
    """Validate a single paper's analysis log."""
    paper_id = paper_path.name
    result = ValidationResult(paper_id, paper_path)

    # Check for analysis log
    log_path = paper_path / "_analysis_log.md"
    if not log_path.exists():
        result.skip("No _analysis_log.md found (old format or not analyzed)")
        return result

    # Read and parse log
    log_content = read_file(log_path)
    if not log_content:
        result.fail("Could not read _analysis_log.md")
        return result

    log = parse_yaml_frontmatter(log_content)
    if not log:
        result.fail("No YAML frontmatter in _analysis_log.md")
        return result

    if "_parse_error" in log:
        result.fail(f"YAML parse error: {log['_parse_error']}")
        return result

    # Rule 1: Schema version
    schema_version = log.get("schema_version")
    if schema_version not in ("2.0", "2.1", "2.2"):
        if strict:
            result.fail(f"Schema version {schema_version} not supported (need 2.0, 2.1, or 2.2)")
        else:
            result.warn(f"Schema version {schema_version} not supported (upgrade recommended)")
        if schema_version is None:
            return result  # Can't validate old format

    # Schema 2.1+ requires mid-point evidence
    requires_mid_evidence = schema_version in ("2.1", "2.2")

    # Rule 2: All steps completed
    steps = log.get("steps", {})
    for step_name, step_data in steps.items():
        if isinstance(step_data, dict) and not step_data.get("completed", False):
            result.fail(f"Step '{step_name}' not completed")

    if result.status == "FAILED":
        return result

    # Rule 3: All chunks read (in order)
    step3 = steps.get("step3_analyze_chunks", {})
    chunks_total = step3.get("chunks_total", 0)
    chunks_read = step3.get("chunks_read", [])

    if chunks_total == 0:
        result.fail("Corrupted PDF: 0 chunks")
        return result

    expected_chunks = list(range(1, chunks_total + 1))

    # Check all chunks present
    if sorted(chunks_read) != expected_chunks:
        missing = set(expected_chunks) - set(chunks_read)
        result.fail(f"Missing chunks: {sorted(missing)}")

    # Check chunks read in correct order (detects random access pattern)
    if chunks_read != expected_chunks:
        result.warn(f"Chunks read out of order: {chunks_read[:5]}... (expected sequential 1,2,3...)")
        result.info["chunks_read_order"] = chunks_read[:10]  # First 10 for inspection

    # Rule 4: Evidence integrity (anti-hallucination)
    chunk_evidence = step3.get("chunk_evidence", {})
    if not chunk_evidence:
        result.fail("No chunk evidence provided")
        return result

    # ANTI-2: Check for duplicate evidence (same start/mid for all chunks)
    all_starts = [e.get("start", "").strip() for e in chunk_evidence.values() if isinstance(e, dict)]
    if len(all_starts) > 1 and len(set(all_starts)) == 1:
        result.fail("Duplicate evidence detected: all chunks have identical start text")

    # ANTI-3: Check for duplicate mid evidence (schema 2.1)
    if requires_mid_evidence:
        all_mids = [e.get("mid", "").strip() for e in chunk_evidence.values() if isinstance(e, dict)]
        if len(all_mids) > 1 and len(set(all_mids)) == 1 and all_mids[0]:
            result.fail("Duplicate evidence detected: all chunks have identical mid text")

    for chunk_num_str, evidence in chunk_evidence.items():
        chunk_num = int(chunk_num_str) if isinstance(chunk_num_str, str) else chunk_num_str

        # Find chunk file
        chunk_files = list(paper_path.glob(f"*_{chunk_num}.md"))
        if not chunk_files:
            result.fail(f"Chunk {chunk_num} file not found")
            continue

        chunk_content = read_file(chunk_files[0])
        if not chunk_content:
            result.fail(f"Could not read chunk {chunk_num}")
            continue

        # ANTI-7: Check for empty chunk
        if len(chunk_content.strip()) == 0:
            result.fail(f"Chunk {chunk_num}: file is empty")
            continue

        # Validate start (after header)
        content_after_header = get_content_after_header(chunk_content)
        expected_start = content_after_header[:100].strip()
        actual_start = evidence.get("start", "").strip()

        if expected_start != actual_start:
            # Allow some flexibility for whitespace
            if expected_start.replace('\n', ' ').strip() != actual_start.replace('\n', ' ').strip():
                result.fail(f"Chunk {chunk_num}: start evidence mismatch")
                result.info[f"chunk_{chunk_num}_expected_start"] = expected_start[:50] + "..."
                result.info[f"chunk_{chunk_num}_actual_start"] = actual_start[:50] + "..."

        # Validate mid (50% position) - required for schema 2.1
        if requires_mid_evidence:
            mid_pos = len(content_after_header) // 2
            mid_start = max(0, mid_pos - 50)
            mid_end = min(len(content_after_header), mid_pos + 50)
            expected_mid = content_after_header[mid_start:mid_end].strip()
            actual_mid = evidence.get("mid", "").strip()

            if not actual_mid:
                result.fail(f"Chunk {chunk_num}: mid evidence missing (required for schema 2.1)")
            elif expected_mid != actual_mid:
                if expected_mid.replace('\n', ' ').strip() != actual_mid.replace('\n', ' ').strip():
                    result.fail(f"Chunk {chunk_num}: mid evidence mismatch")
                    result.info[f"chunk_{chunk_num}_expected_mid"] = expected_mid[:50] + "..."
                    result.info[f"chunk_{chunk_num}_actual_mid"] = actual_mid[:50] + "..."

        # Validate end
        expected_end = chunk_content[-100:].strip()
        actual_end = evidence.get("end", "").strip()

        if expected_end != actual_end:
            if expected_end.replace('\n', ' ').strip() != actual_end.replace('\n', ' ').strip():
                result.fail(f"Chunk {chunk_num}: end evidence mismatch")

        # Validate hash
        expected_hash = compute_hash(chunk_content)
        actual_hash = evidence.get("hash", "")

        if expected_hash != actual_hash:
            result.fail(f"Chunk {chunk_num}: hash mismatch (content modified?)")
            result.info[f"chunk_{chunk_num}_expected_hash"] = expected_hash[:16] + "..."
            result.info[f"chunk_{chunk_num}_actual_hash"] = actual_hash[:16] + "..."

    # Rule 5: Index created
    outputs = log.get("outputs", {})
    if not outputs.get("index_md_created"):
        result.fail("index.md not created")

    # Rule 6: Index file actually exists
    index_path = paper_path / "index.md"
    if not index_path.exists():
        result.fail("index.md file missing (claimed created but not found)")
    else:
        # ANTI-6: Quote cross-validation (check quotes in index.md exist in chunks)
        index_content = read_file(index_path)
        if index_content:
            # Find quoted text in index.md (text in "..." or '...')
            quotes = re.findall(r'"([^"]{20,})"', index_content)

            # Load all chunk contents
            all_chunk_content = ""
            for chunk_file in paper_path.glob("*_[0-9]*.md"):
                chunk_text = read_file(chunk_file)
                if chunk_text:
                    all_chunk_content += chunk_text + "\n"

            # Check each quote exists in chunks
            for quote in quotes[:5]:  # Check first 5 quotes (avoid excessive checking)
                # Normalize whitespace for comparison
                quote_normalized = ' '.join(quote.split())
                if quote_normalized not in ' '.join(all_chunk_content.split()):
                    result.warn(f"Quote not found in chunks: \"{quote[:50]}...\"")

    # Collect quality info
    quality = log.get("quality", {})
    result.info["relevance_score"] = quality.get("relevance_score")
    result.info["extraction_confidence"] = quality.get("extraction_confidence")
    result.info["domain_match"] = quality.get("domain_match")

    # Performance info
    performance = log.get("performance", {})
    result.info["tokens_used"] = performance.get("tokens_used")
    result.info["duration_seconds"] = log.get("duration_seconds")

    # Mark as passed if no errors
    result.passed()
    return result


def find_papers(collection_path: Path) -> List[Path]:
    """Find all paper folders in a collection."""
    papers = []
    for item in collection_path.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            # Check if it looks like a paper folder (has _metadata.json or chunks)
            if (item / "_metadata.json").exists() or list(item.glob("*_1.md")):
                papers.append(item)
    return sorted(papers)


def generate_report(results: List[ValidationResult], collection_path: Path) -> str:
    """Generate markdown validation report."""
    report = []
    report.append("# Validation Report")
    report.append("")
    report.append(f"**Collection**: `{collection_path}`")
    report.append(f"**Validated**: {datetime.now().isoformat()}")
    report.append("")

    # Summary
    passed = sum(1 for r in results if r.status == "PASSED")
    failed = sum(1 for r in results if r.status == "FAILED")
    warnings = sum(1 for r in results if r.status == "WARNING")
    skipped = sum(1 for r in results if r.status == "SKIPPED")
    total = len(results)

    report.append("## Summary")
    report.append("")
    report.append(f"| Status | Count |")
    report.append(f"|--------|-------|")
    report.append(f"| PASSED | {passed} |")
    report.append(f"| FAILED | {failed} |")
    report.append(f"| WARNING | {warnings} |")
    report.append(f"| SKIPPED | {skipped} |")
    report.append(f"| **Total** | **{total}** |")
    report.append("")

    # Pass rate
    analyzed = passed + failed + warnings
    if analyzed > 0:
        pass_rate = (passed / analyzed) * 100
        report.append(f"**Pass Rate**: {pass_rate:.1f}% ({passed}/{analyzed} analyzed)")
    report.append("")

    # Details
    report.append("## Paper Details")
    report.append("")

    for r in results:
        status_icon = {
            "PASSED": "\u2705",  # ✓
            "FAILED": "\u274C",  # ✗
            "WARNING": "\u26A0\uFE0F",  # ⚠
            "SKIPPED": "\u23ED"   # ⏭
        }.get(r.status, "?")

        report.append(f"### {status_icon} {r.paper_id}")
        report.append("")
        report.append(f"**Status**: {r.status}")

        if r.errors:
            report.append("")
            report.append("**Errors**:")
            for err in r.errors:
                report.append(f"- {err}")

        if r.warnings:
            report.append("")
            report.append("**Warnings**:")
            for warn in r.warnings:
                report.append(f"- {warn}")

        if r.info:
            report.append("")
            report.append("**Info**:")
            for key, value in r.info.items():
                if value is not None:
                    report.append(f"- {key}: {value}")

        report.append("")

    return "\n".join(report)


def main():
    parser = argparse.ArgumentParser(
        description="Validate paper analysis logs against Schema v2.0-2.2"
    )
    parser.add_argument(
        "collection_path",
        type=str,
        help="Path to paper collection folder"
    )
    parser.add_argument(
        "--paper",
        type=str,
        help="Validate specific paper only"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output report to file (default: _validation_report.md in collection)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output JSON instead of markdown"
    )

    args = parser.parse_args()

    # Resolve collection path
    collection_path = Path(args.collection_path)
    if not collection_path.is_absolute():
        # Try relative to current dir, then common locations
        if not collection_path.exists():
            for prefix in ["", "04-workspace/papers/", "02-projects/"]:
                test_path = Path(prefix) / args.collection_path
                if test_path.exists():
                    collection_path = test_path
                    break

    if not collection_path.exists():
        print(f"ERROR: Collection not found: {args.collection_path}")
        sys.exit(1)

    # Find papers
    if args.paper:
        paper_path = collection_path / args.paper
        if not paper_path.exists():
            print(f"ERROR: Paper not found: {args.paper}")
            sys.exit(1)
        papers = [paper_path]
    else:
        papers = find_papers(collection_path)

    if not papers:
        print(f"ERROR: No papers found in {collection_path}")
        sys.exit(1)

    print(f"Validating {len(papers)} paper(s) in {collection_path}...")
    print()

    # Validate each paper
    results = []
    for paper_path in papers:
        result = validate_paper(paper_path, strict=args.strict)
        results.append(result)

        # Print progress (ASCII-safe for Windows)
        status_icon = {
            "PASSED": "[OK]",
            "FAILED": "[FAIL]",
            "WARNING": "[WARN]",
            "SKIPPED": "[SKIP]"
        }.get(result.status, "[?]")
        print(f"  {status_icon} {result.paper_id}: {result.status}")
        for err in result.errors:
            print(f"      ERROR: {err}")
        for warn in result.warnings:
            print(f"      WARN: {warn}")

    print()

    # Summary
    passed = sum(1 for r in results if r.status == "PASSED")
    failed = sum(1 for r in results if r.status == "FAILED")
    warnings = sum(1 for r in results if r.status == "WARNING")
    skipped = sum(1 for r in results if r.status == "SKIPPED")

    print(f"Results: {passed} passed, {failed} failed, {warnings} warnings, {skipped} skipped")

    # Output report
    if args.json:
        output = json.dumps([r.to_dict() for r in results], indent=2)
        ext = ".json"
    else:
        output = generate_report(results, collection_path)
        ext = ".md"

    output_path = args.output
    if not output_path:
        output_path = collection_path / f"_validation_report{ext}"
    else:
        output_path = Path(output_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(output)
    print(f"\nReport written to: {output_path}")

    # Exit code
    if failed > 0:
        sys.exit(1)
    elif warnings > 0 and args.strict:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
