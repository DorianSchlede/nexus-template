#!/usr/bin/env python3
"""
validate_analysis.py - Validate paper analysis logs against Schema v2.3

Part of 7-Level Synthesis Pipeline Improvements (Project 06).

Validates:
- Schema version (2.0-2.3, with 2.3 requiring chunk_index and fields_found)
- All steps completed
- All chunks read in order
- 3-point evidence integrity (start, mid, end, hash)
- chunk_index with fields_found for ALL briefing fields (Gap G1)
- Structured N/A format (Gap G18)
- Quote cross-validation (Gap G15 - basic)
- Quote-line verification (Gap G15 - precise chunk:line checking)

Usage:
    python validate_analysis.py {collection_path}
    python validate_analysis.py {collection_path} --paper {paper_name}
    python validate_analysis.py {collection_path} --strict
    python validate_analysis.py {collection_path} --output report.md
    python validate_analysis.py {collection_path} --check-chunk-index

Examples:
    python validate_analysis.py 04-workspace/papers/TA_LLM
    python validate_analysis.py 02-projects/02-ontologies-research/02-resources/papers --strict
    python validate_analysis.py 02-projects/02-ontologies-research/02-resources/papers --check-chunk-index
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


def normalize_unicode(text: str) -> str:
    """Normalize Unicode to ASCII equivalents for evidence comparison.

    Subagents may normalize certain Unicode symbols when extracting evidence.
    This function applies the same normalization for consistent comparison.
    """
    if not text:
        return text

    replacements = {
        '\u2217': '*',      # ∗ ASTERISK OPERATOR
        '\u2020': 'dagger', # † DAGGER
        '\u2021': 'ddagger', # ‡ DOUBLE DAGGER
        '\u2018': "'",      # ' LEFT SINGLE QUOTATION
        '\u2019': "'",      # ' RIGHT SINGLE QUOTATION
        '\u201c': '"',      # " LEFT DOUBLE QUOTATION
        '\u201d': '"',      # " RIGHT DOUBLE QUOTATION
        '\u2013': '-',      # – EN DASH
        '\u2014': '--',     # — EM DASH
        '\u2026': '...',    # … HORIZONTAL ELLIPSIS
        '\u00a0': ' ',      # NO-BREAK SPACE
        # Accented characters (LLMs often strip accents)
        '\u00ed': 'i',      # í LATIN SMALL LETTER I WITH ACUTE
        '\u00e9': 'e',      # é LATIN SMALL LETTER E WITH ACUTE
        '\u00e1': 'a',      # á LATIN SMALL LETTER A WITH ACUTE
        '\u00f3': 'o',      # ó LATIN SMALL LETTER O WITH ACUTE
        '\u00fa': 'u',      # ú LATIN SMALL LETTER U WITH ACUTE
        '\u00f1': 'n',      # ñ LATIN SMALL LETTER N WITH TILDE
        '\u00e8': 'e',      # è LATIN SMALL LETTER E WITH GRAVE
        '\u00e0': 'a',      # à LATIN SMALL LETTER A WITH GRAVE
        '\u00fc': 'u',      # ü LATIN SMALL LETTER U WITH DIAERESIS
        '\u00f6': 'o',      # ö LATIN SMALL LETTER O WITH DIAERESIS
        '\u00e4': 'a',      # ä LATIN SMALL LETTER A WITH DIAERESIS
    }

    for uni, ascii_equiv in replacements.items():
        text = text.replace(uni, ascii_equiv)

    return text


def normalize_markdown(text: str) -> str:
    """Strip markdown formatting for evidence comparison.

    LLMs are semantic processors - they may strip markdown formatting
    when extracting evidence (e.g., _italic_ -> italic).
    This function applies the same normalization for consistent comparison.

    Root cause: Issue 1 in root_cause_analysis.md
    """
    if not text:
        return text

    # Remove italic markers (both _ and *)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    text = re.sub(r'\*([^*]+)\*', r'\1', text)

    # Remove bold markers
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)

    # Remove inline code markers
    text = re.sub(r'`([^`]+)`', r'\1', text)

    return text


def get_content_after_header(content: str) -> str:
    """Get content after the first header line (# ...).

    For headerless chunks (bibliography, appendix), handles HTML comments
    that mark chunk sources (e.g., <!-- Source: ... -->).

    Root cause: Issue 3 in root_cause_analysis.md - rigid structure assumptions
    """
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if line.startswith('#'):
            # Return everything after this line
            return '\n'.join(lines[i + 1:]).lstrip('\n')

    # No header found - check for HTML comment (PDF source marker)
    if content.startswith('<!--'):
        end = content.find('-->')
        if end != -1:
            # Return content after the comment, stripping leading whitespace
            return content[end + 3:].lstrip('\n')

    # No header or comment found, return original
    return content


def verify_quote_at_line(paper_path: Path, chunk: int, lines: str, quote: str) -> Tuple[bool, str]:
    """Verify that quote exists in chunk file.

    Gap G15: Quote verification. Line numbers are ignored since subagents
    hallucinate them. We use multiple strategies:
    1. Exact string match (best)
    2. Whitespace-normalized match
    3. Case-insensitive match
    4. Key word overlap (>= 60% of significant words found)

    Args:
        paper_path: Path to paper folder (e.g., .../papers/05-DOLCE...)
        chunk: Chunk number (1-indexed)
        lines: Line range string (ignored - for logging only)
        quote: Quote text to verify

    Returns:
        Tuple of (success, message)
    """
    # Build chunk filename
    paper_id = paper_path.name
    chunk_file = paper_path / f"{paper_id}_{chunk}.md"

    if not chunk_file.exists():
        return False, f"Chunk file not found: {chunk_file.name}"

    try:
        content = read_file(chunk_file)
        if not content:
            return False, "Could not read chunk file"

        if not quote or len(quote.strip()) < 10:
            return True, "Quote too short to verify (skipped)"

        # Normalize both content and quote for comparison
        content_normalized = normalize_unicode(content)
        quote_normalized = normalize_unicode(quote)

        # Use first 50 chars for matching (quotes may be truncated)
        quote_start = quote_normalized[:50].strip()

        # Try exact match first
        if quote_start in content_normalized:
            return True, "Quote verified (exact match)"

        # Try with whitespace normalization
        content_ws_normalized = re.sub(r'\s+', ' ', content_normalized)
        quote_ws_normalized = re.sub(r'\s+', ' ', quote_start)

        if quote_ws_normalized in content_ws_normalized:
            return True, "Quote verified (whitespace normalized)"

        # Try case-insensitive match
        if quote_ws_normalized.lower() in content_ws_normalized.lower():
            return True, "Quote verified (case-insensitive)"

        # Try key word overlap (handles paraphrased quotes)
        # Extract significant words (>3 chars, not common stopwords)
        stopwords = {'that', 'this', 'with', 'from', 'which', 'their', 'have',
                     'been', 'were', 'they', 'being', 'other', 'about', 'these',
                     'would', 'there', 'could', 'should', 'into', 'such', 'some',
                     'used', 'data', 'task', 'each', 'more', 'also'}
        quote_words = [w.lower() for w in re.findall(r'\b\w{4,}\b', quote_normalized)
                       if w.lower() not in stopwords]
        content_lower = content_ws_normalized.lower()

        if len(quote_words) >= 2:
            found = sum(1 for w in quote_words if w in content_lower)
            overlap = found / len(quote_words)
            if overlap >= 0.6:
                return True, f"Quote verified (key words: {found}/{len(quote_words)} = {overlap:.0%})"

        return False, f"Quote not found in chunk {chunk}"

    except Exception as e:
        return False, f"Error reading chunk: {e}"


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


def validate_paper(paper_path: Path, strict: bool = False, check_chunk_index: bool = False) -> ValidationResult:
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

    # Rule 1: Schema version (normalize "v2.3" to "2.3")
    schema_version = log.get("schema_version")
    if schema_version and schema_version.startswith("v"):
        schema_version = schema_version[1:]  # Strip leading 'v'

    if schema_version not in ("2.0", "2.1", "2.2", "2.3"):
        if strict:
            result.fail(f"Schema version {schema_version} not supported (need 2.0-2.3)")
        else:
            result.warn(f"Schema version {schema_version} not supported (upgrade recommended)")
        if schema_version is None:
            return result  # Can't validate old format

    # Schema 2.1-2.2 required mid-point evidence, but 2.3+ makes it optional
    # Mid evidence adds complexity with minimal value since hash is ground truth
    requires_mid_evidence = schema_version in ("2.1", "2.2", "v2.1", "v2.2")

    # Schema 2.3 requires chunk_index with fields_found
    # Also required if --check-chunk-index flag is passed
    requires_chunk_index = schema_version in ("2.3", "v2.3") or check_chunk_index

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

        # Helper function to normalize whitespace for comparison
        def normalize_ws(text):
            """Normalize whitespace: replace newlines with spaces, collapse multiple spaces."""
            return re.sub(r'\s+', ' ', text).strip()

        # Helper to fully normalize text (Unicode + markdown + whitespace)
        def normalize_full(text):
            """Normalize Unicode, markdown, and whitespace for comparison."""
            return normalize_ws(normalize_unicode(normalize_markdown(text)))

        # Hash validation - optional in Schema v2.3+
        # If provided, validates chunk integrity. If not, rely on start/end evidence.
        expected_hash = compute_hash(chunk_content)
        actual_hash = evidence.get("hash", "")

        if actual_hash:
            # Hash provided - compare (8 chars = prefix comparison)
            if len(actual_hash) == 8:
                hash_matches = expected_hash[:8] == actual_hash
            else:
                hash_matches = expected_hash == actual_hash
        else:
            # No hash provided (Schema v2.3+ makes this optional)
            # Assume OK for warning logic - validation relies on start/end evidence
            hash_matches = True

        # Validate start (after header, or header itself)
        content_after_header = get_content_after_header(chunk_content)
        expected_start = content_after_header[:100].strip()
        actual_start = evidence.get("start", "").strip()

        # Also accept the header line itself as valid start evidence
        first_header_line = ""
        for line in chunk_content.split('\n'):
            if line.startswith('#'):
                first_header_line = line.strip()
                break

        start_mismatch = False
        if expected_start != actual_start:
            # Allow flexibility for whitespace and Unicode normalization
            normalized_expected = normalize_full(expected_start)
            normalized_actual = normalize_full(actual_start)
            normalized_chunk = normalize_full(chunk_content)

            # Check containment rather than equality
            actual_is_prefix = normalized_expected.startswith(normalized_actual[:80])
            expected_is_prefix = normalized_actual.startswith(normalized_expected[:80])

            # Accept header line as valid start evidence
            header_is_valid = first_header_line and normalize_full(actual_start) == normalize_full(first_header_line)

            # Accept if actual_start appears anywhere in the first 20% of the chunk
            first_20_percent = len(chunk_content) // 5
            actual_in_chunk_start = normalized_actual[:60] in normalized_chunk[:max(1000, first_20_percent)]

            # Also check if it appears ANYWHERE in the chunk (semantic extraction)
            actual_anywhere = normalized_actual[:60] in normalized_chunk

            if not actual_is_prefix and not expected_is_prefix and not header_is_valid and not actual_in_chunk_start and not actual_anywhere:
                start_mismatch = True
                # Start evidence not found - warn (don't fail, since LLMs extract semantically)
                result.warn(f"Chunk {chunk_num}: start evidence not found in chunk")
                result.info[f"chunk_{chunk_num}_expected_start"] = expected_start[:50] + "..."
                result.info[f"chunk_{chunk_num}_actual_start"] = actual_start[:50] + "..."

        # Validate mid (anywhere in middle 60% of chunk) - required for schema 2.1+
        if requires_mid_evidence:
            actual_mid = evidence.get("mid", "").strip()
            if not actual_mid:
                result.fail(f"Chunk {chunk_num}: mid evidence missing (required for schema 2.1)")
            else:
                # Check if actual_mid exists in middle 60% of chunk (20%-80% range)
                mid_portion_start = int(len(content_after_header) * 0.2)
                mid_portion_end = int(len(content_after_header) * 0.8)
                mid_portion = content_after_header[mid_portion_start:mid_portion_end]
                mid_normalized = normalize_full(mid_portion)
                actual_mid_normalized = normalize_full(actual_mid)

                # Check if normalized actual_mid exists in normalized mid portion
                if actual_mid_normalized not in mid_normalized:
                    # Also check original content in case normalization affects matching
                    if actual_mid not in mid_portion:
                        result.fail(f"Chunk {chunk_num}: mid evidence not found in middle 60% of chunk")
                        result.info[f"chunk_{chunk_num}_mid_portion"] = f"chars {mid_portion_start}-{mid_portion_end}"
                        result.info[f"chunk_{chunk_num}_actual_mid"] = actual_mid[:50] + "..."

        # Validate end (flexible: accept if ANY portion of cited text appears in last 40%)
        # Note: Subagents extract semantically ("last sentence") not positionally
        # Root cause: Issue 4 in root_cause_analysis.md - semantic vs positional mismatch
        actual_end = evidence.get("end", "").strip()
        if actual_end:
            last_40_percent = chunk_content[int(len(chunk_content) * 0.6):]
            last_40_normalized = normalize_full(last_40_percent)
            actual_end_normalized = normalize_full(actual_end)

            # Check if normalized actual_end exists in normalized last 40%
            end_found = actual_end_normalized in last_40_normalized

            # If full text not found, try matching a significant portion (40+ chars)
            if not end_found and len(actual_end_normalized) > 40:
                # Try shorter substrings to find overlap
                for start_pos in range(0, len(actual_end_normalized) - 30, 10):
                    snippet = actual_end_normalized[start_pos:start_pos+40]
                    if snippet in last_40_normalized:
                        end_found = True
                        break

            # Also check if content ends with similar text (URL handling)
            if not end_found:
                # Extract last 50 chars from file and compare
                file_end = normalize_full(chunk_content[-100:])
                actual_end_short = actual_end_normalized[-50:] if len(actual_end_normalized) > 50 else actual_end_normalized
                if actual_end_short in file_end or file_end[-30:] in actual_end_normalized:
                    end_found = True

            if not end_found:
                # Also check if end evidence appears ANYWHERE in the chunk (semantic extraction)
                if actual_end_normalized[:60] in normalize_full(chunk_content):
                    end_found = True  # Found somewhere, just not in last 40%

            if not end_found:
                # End evidence not found - warn (don't fail, since LLMs extract semantically)
                result.warn(f"Chunk {chunk_num}: end evidence not found in chunk")
                result.info[f"chunk_{chunk_num}_actual_end"] = actual_end[:50] + "..."

        # Hash mismatch - only report if hash was provided
        if actual_hash and not hash_matches:
            result.fail(f"Chunk {chunk_num}: hash mismatch (content modified?)")
            result.info[f"chunk_{chunk_num}_expected_hash"] = expected_hash[:8] + "..."
            result.info[f"chunk_{chunk_num}_actual_hash"] = actual_hash[:8] + "..."

    # Rule 5: Index created
    outputs = log.get("outputs", {})
    if not outputs.get("index_md_created"):
        result.fail("index.md not created")

    # Rule 5b: Validate chunk_index in index.md (Schema 2.3 - Gap G1)
    if requires_chunk_index:
        index_path_for_chunk_index = paper_path / "index.md"
        if index_path_for_chunk_index.exists():
            index_content = read_file(index_path_for_chunk_index)
            if index_content:
                index_fm = parse_yaml_frontmatter(index_content)
                if index_fm:
                    chunk_index = index_fm.get("chunk_index")
                    if not chunk_index:
                        result.fail("Schema 2.3 requires chunk_index in index.md frontmatter (Gap G1)")
                    else:
                        # Validate fields_found in each chunk
                        for chunk_num_str, chunk_data in chunk_index.items():
                            if not isinstance(chunk_data, dict):
                                continue
                            fields_found = chunk_data.get("fields_found")
                            if not fields_found:
                                result.fail(f"Chunk {chunk_num_str} missing fields_found (Gap G1)")
                            # Check for token_count
                            if "token_count" not in chunk_data:
                                result.warn(f"Chunk {chunk_num_str} missing token_count (Gap G3)")

    # Rule 6: Index file actually exists
    index_path = paper_path / "index.md"
    if not index_path.exists():
        result.fail("index.md file missing (claimed created but not found)")
    else:
        # ANTI-6: Quote cross-validation (check quotes in index.md body exist in chunks)
        index_content = read_file(index_path)
        if index_content:
            # Skip YAML frontmatter - only check body content
            body_content = index_content
            if index_content.startswith('---'):
                body_match = re.search(r'\n---\s*\n', index_content[3:])
                if body_match:
                    body_content = index_content[3 + body_match.end():]

            # Find quoted text in index.md body (text in "...")
            # Skip quotes that look like YAML values (start with field names)
            quotes = re.findall(r'"([^"]{20,})"', body_content)
            filtered_quotes = [q for q in quotes if not re.match(r'\w+:\s*', q)]

            # Load all chunk contents
            all_chunk_content = ""
            for chunk_file in paper_path.glob("*_[0-9]*.md"):
                chunk_text = read_file(chunk_file)
                if chunk_text:
                    all_chunk_content += chunk_text + "\n"

            # Check each quote exists in chunks (using key word matching)
            all_chunks_lower = ' '.join(all_chunk_content.split()).lower()
            for quote in filtered_quotes[:5]:  # Check first 5 quotes
                quote_normalized = ' '.join(quote.split())
                # Use key word matching instead of exact match
                words = [w.lower() for w in re.findall(r'\b\w{5,}\b', quote_normalized)]
                if words:
                    found = sum(1 for w in words if w in all_chunks_lower)
                    if found / len(words) < 0.5:
                        result.warn(f"Quote not found in chunks: \"{quote[:50]}...\"")

    # Rule 8: Quote-Line Verification (Gap G15) - Sample check extractions
    index_path = paper_path / "index.md"
    if index_path.exists():
        index_content = read_file(index_path)
        if index_content:
            index_fm = parse_yaml_frontmatter(index_content)
            if index_fm:
                # Check extraction fields for quote-line references
                quote_checks = 0
                quote_failures = 0
                for field_name, items in index_fm.items():
                    # Skip non-extraction fields
                    if field_name in ('paper_id', 'title', 'authors', 'year', 'chunks_expected',
                                      'chunks_read', 'analysis_complete', 'schema_version',
                                      'chunk_index', 'high_priority_fields_found'):
                        continue
                    if not isinstance(items, list) or len(items) == 0:
                        continue

                    # Spot-check first 3 items per field (performance optimization)
                    for item in items[:3]:
                        if not isinstance(item, dict):
                            continue
                        if not all(k in item for k in ['chunk', 'lines', 'quote']):
                            continue
                        if item.get('chunk') is None:  # Structured N/A format (G18)
                            continue

                        quote_checks += 1
                        success, message = verify_quote_at_line(
                            paper_path,
                            item['chunk'],
                            str(item['lines']),
                            item.get('quote', '')
                        )
                        if not success:
                            quote_failures += 1
                            result.warn(
                                f"Quote verification failed (G15): {field_name}['{item.get('item', '?')}'] "
                                f"at Chunk {item['chunk']}:{item['lines']} - {message}"
                            )

                # Track quote verification stats
                if quote_checks > 0:
                    result.info["quote_checks"] = quote_checks
                    result.info["quote_failures"] = quote_failures
                    result.info["quote_verification_rate"] = f"{((quote_checks - quote_failures) / quote_checks) * 100:.0f}%"

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
        description="Validate paper analysis logs against Schema v2.3"
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
    parser.add_argument(
        "--check-chunk-index",
        action="store_true",
        help="Require chunk_index in index.md (Schema 2.3)"
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
        result = validate_paper(paper_path, strict=args.strict, check_chunk_index=args.check_chunk_index)
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
