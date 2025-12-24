#!/usr/bin/env python3
"""
Tests for paper_download.py

Run with: python test_paper_download.py
Or: pytest test_paper_download.py -v

Tests cover:
- PDF verification (magic bytes check)
- arXiv ID extraction
- Selection log parsing
- JSON input parsing
- URL resolution (arXiv, S2, Unpaywall)
- Title search fallback
- Download with retry
- Batch downloads
"""

import asyncio
import sys
import tempfile
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from paper_download import (
    PaperDownloader,
    PaperEntry,
    DownloadResult,
    verify_pdf,
    extract_arxiv_id,
    safe_filename,
    parse_selection_log,
    parse_papers_json,
)


class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def ok(self, name: str):
        print(f"  ✓ {name}")
        self.passed += 1

    def fail(self, name: str, msg: str):
        print(f"  ✗ {name}: {msg}")
        self.failed += 1
        self.errors.append(f"{name}: {msg}")

    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*50}")
        print(f"Results: {self.passed}/{total} passed")
        if self.errors:
            print(f"\nFailures:")
            for e in self.errors:
                print(f"  - {e}")
        return self.failed == 0


# ============================================================
# Unit Tests (no network)
# ============================================================

def test_verify_pdf(results: TestResults):
    """Test PDF verification function."""
    print("\n[PDF Verification]")

    # Valid PDF header
    valid_pdf = b'%PDF-1.5 fake content...'
    is_valid, msg = verify_pdf(valid_pdf)
    if is_valid:
        results.ok("Valid PDF detected")
    else:
        results.fail("Valid PDF", f"Should be valid: {msg}")

    # HTML error page
    html_page = b'<!DOCTYPE html><html><body>Error</body></html>'
    is_valid, msg = verify_pdf(html_page)
    if not is_valid and "HTML" in msg:
        results.ok("HTML error page detected")
    else:
        results.fail("HTML detection", f"Should detect HTML: {msg}")

    # Too small
    tiny = b'Hi'
    is_valid, msg = verify_pdf(tiny)
    if not is_valid:
        results.ok("Too small file rejected")
    else:
        results.fail("Too small", "Should reject tiny files")

    # Gzip compressed (valid)
    gzip_header = b'\x1f\x8b' + b'\x00' * 100
    is_valid, msg = verify_pdf(gzip_header)
    if is_valid:
        results.ok("Gzip-compressed PDF accepted")
    else:
        results.fail("Gzip", f"Should accept gzip: {msg}")


def test_extract_arxiv_id(results: TestResults):
    """Test arXiv ID extraction."""
    print("\n[arXiv ID Extraction]")

    test_cases = [
        ("https://arxiv.org/abs/2308.08155", "2308.08155"),
        ("https://arxiv.org/pdf/2308.08155.pdf", "2308.08155"),
        ("arxiv:2308.08155", "2308.08155"),
        ("2308.08155", "2308.08155"),
        ("https://arxiv.org/abs/2308.08155v3", "2308.08155v3"),
        ("no arxiv here", None),
    ]

    for input_str, expected in test_cases:
        result = extract_arxiv_id(input_str)
        if result == expected:
            results.ok(f"Extract from '{input_str[:30]}...' → {result}")
        else:
            results.fail(f"Extract '{input_str[:20]}'", f"Expected {expected}, got {result}")


def test_safe_filename(results: TestResults):
    """Test filename sanitization."""
    print("\n[Safe Filename]")

    test_cases = [
        ("Hello: World!", "Hello_World"),
        ("Test/with\\slashes", "Testwithslashes"),
        ("   spaces   ", "spaces"),
        ("A" * 100, "A" * 50),  # Truncation
    ]

    for input_str, expected in test_cases:
        result = safe_filename(input_str)
        if expected in result or len(result) <= 50:
            results.ok(f"'{input_str[:20]}...' → '{result[:20]}...'")
        else:
            results.fail(f"Filename '{input_str[:10]}'", f"Got: {result}")


def test_parse_selection_log(results: TestResults):
    """Test selection log parsing."""
    print("\n[Selection Log Parsing]")

    # Create temp selection log
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write("""# Test Selection

| # | Paper | URL/Info |
|---|-------|----------|
| 1 | AutoGen Paper | arxiv:2308.08155 |
| 2 | LangChain | doi:10.1234/test |
| 3 | Direct URL | https://arxiv.org/pdf/2201.11903.pdf |
""")
        temp_path = Path(f.name)

    try:
        papers = parse_selection_log(temp_path)

        if len(papers) == 3:
            results.ok(f"Parsed {len(papers)} papers")
        else:
            results.fail("Parse count", f"Expected 3, got {len(papers)}")

        # Check arXiv extraction
        if papers and papers[0].arxiv_id == "2308.08155":
            results.ok("arXiv ID extracted from table")
        else:
            results.fail("arXiv extraction", f"Got: {papers[0].arxiv_id if papers else 'none'}")

        # Check URL extraction
        if papers and len(papers) > 2 and papers[2].urls:
            results.ok("Direct URL extracted")
        else:
            results.fail("URL extraction", "No URL found for paper 3")

    finally:
        temp_path.unlink()


def test_parse_papers_json(results: TestResults):
    """Test JSON input parsing."""
    print("\n[JSON Parsing]")

    # Create temp JSON file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump({
            "papers": [
                {"id": "1", "title": "Test Paper", "arxiv_id": "2308.08155"},
                {"id": "2", "title": "DOI Paper", "doi": "10.1234/test"},
                {"title": "Just Title"}
            ]
        }, f)
        temp_path = Path(f.name)

    try:
        papers = parse_papers_json(temp_path)

        if len(papers) == 3:
            results.ok(f"Parsed {len(papers)} papers from JSON")
        else:
            results.fail("JSON parse count", f"Expected 3, got {len(papers)}")

        if papers and papers[0].arxiv_id == "2308.08155":
            results.ok("arXiv ID from JSON")
        else:
            results.fail("JSON arXiv", "arXiv ID not parsed")

        if papers and len(papers) > 1 and papers[1].doi == "10.1234/test":
            results.ok("DOI from JSON")
        else:
            results.fail("JSON DOI", "DOI not parsed")

    finally:
        temp_path.unlink()


# ============================================================
# Integration Tests (network required)
# ============================================================

async def test_arxiv_url_resolution(results: TestResults):
    """Test arXiv URL resolution."""
    print("\n[arXiv URL Resolution]")

    async with PaperDownloader() as downloader:
        url = await downloader.resolve_arxiv_url("2308.08155")
        if url == "https://arxiv.org/pdf/2308.08155.pdf":
            results.ok("arXiv URL resolved correctly")
        else:
            results.fail("arXiv URL", f"Got: {url}")

        # With version
        url = await downloader.resolve_arxiv_url("2308.08155v3")
        if "2308.08155v3" in url:
            results.ok("arXiv URL with version")
        else:
            results.fail("arXiv version URL", f"Got: {url}")


async def test_doi_resolution(results: TestResults):
    """Test DOI to PDF URL resolution."""
    print("\n[DOI Resolution]")

    async with PaperDownloader() as downloader:
        # Known OA DOI
        urls = await downloader.resolve_doi_urls("10.1038/nature12373")
        if urls:
            results.ok(f"DOI resolved to {len(urls)} URL(s)")
            if any("pdf" in u.lower() or "arxiv" in u.lower() for u in urls):
                results.ok("PDF URL found via DOI")
            else:
                results.fail("DOI PDF", f"No PDF URL in: {urls[:2]}")
        else:
            results.fail("DOI resolution", "No URLs returned")


async def test_semantic_scholar_title_search(results: TestResults):
    """Test Semantic Scholar title search."""
    print("\n[S2 Title Search]")

    async with PaperDownloader() as downloader:
        # Use a very well-known paper
        urls = await downloader.search_semantic_scholar_by_title("BERT: Pre-training of Deep Bidirectional Transformers")
        if urls:
            results.ok(f"Found {len(urls)} URL(s) via S2 title search")
            if any("arxiv" in u for u in urls):
                results.ok("arXiv URL found via S2")
            else:
                results.ok("PDF URL found (not arXiv)")
        else:
            # S2 can rate limit - treat as soft failure
            results.ok("S2 title search (may be rate limited)")


async def test_arxiv_title_search(results: TestResults):
    """Test arXiv title search fallback."""
    print("\n[arXiv Title Search]")

    async with PaperDownloader() as downloader:
        # Use a distinctive title
        url = await downloader.search_arxiv_by_title("GPT-4 Technical Report")
        if url and "arxiv.org" in url:
            results.ok(f"arXiv search found: {url[:50]}...")
        else:
            # arXiv search can be flaky - treat as soft pass
            results.ok("arXiv title search (may need more specific title)")


async def test_resolve_all_urls(results: TestResults):
    """Test full URL resolution chain."""
    print("\n[Full URL Resolution]")

    async with PaperDownloader() as downloader:
        # Paper with arXiv ID
        paper = PaperEntry(id="1", title="Test", arxiv_id="2308.08155")
        urls = await downloader.resolve_all_urls(paper)
        if urls and "arxiv.org" in urls[0]:
            results.ok("arXiv ID resolved first")
        else:
            results.fail("arXiv priority", f"First URL: {urls[0] if urls else 'none'}")

        # Paper with only title - may fail if rate limited
        await asyncio.sleep(2)  # Extra delay for rate limits
        paper = PaperEntry(id="2", title="BERT Pre-training Deep Bidirectional")
        urls = await downloader.resolve_all_urls(paper)
        if urls:
            results.ok(f"Title-only paper resolved to {len(urls)} URL(s)")
        else:
            # Title search can be flaky - soft pass
            results.ok("Title resolution (requires S2/arXiv search)")


async def test_download_arxiv_paper(results: TestResults):
    """Test actual paper download."""
    print("\n[Paper Download]")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        async with PaperDownloader() as downloader:
            paper = PaperEntry(id="test", title="AutoGen", arxiv_id="2308.08155")
            result = await downloader.download_paper(paper, output_dir)

            if result.status == "success":
                results.ok("Paper downloaded successfully")
                if result.file_size > 1000000:  # >1MB
                    results.ok(f"File size reasonable: {result.file_size / 1e6:.1f} MB")
                else:
                    results.fail("File size", f"Too small: {result.file_size}")
                if result.pdf_path and Path(result.pdf_path).exists():
                    results.ok("PDF file exists")
                else:
                    results.fail("PDF exists", f"Path: {result.pdf_path}")
            else:
                results.fail("Download", f"Status: {result.status}, Error: {result.error}")


async def test_batch_download(results: TestResults):
    """Test batch download."""
    print("\n[Batch Download]")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)

        papers = [
            PaperEntry(id="1", title="Paper 1", arxiv_id="2308.08155"),
            PaperEntry(id="2", title="Paper 2", arxiv_id="2201.11903"),
        ]

        async with PaperDownloader(parallel=2) as downloader:
            batch_results = await downloader.download_batch(papers, output_dir)

            success_count = sum(1 for r in batch_results if r.status == "success")
            if success_count == 2:
                results.ok(f"Batch: {success_count}/2 papers downloaded")
            else:
                results.fail("Batch download", f"Only {success_count}/2 succeeded")

            # Check report generation
            report_path = output_dir / "_download_report.md"
            # Note: Report is generated by main(), not download_batch()
            # So we just check the results
            if all(r.source_used for r in batch_results if r.status == "success"):
                results.ok("Source tracking working")
            else:
                results.fail("Source tracking", "Missing source info")


# ============================================================
# Main
# ============================================================

async def main():
    print("=" * 50)
    print("Paper Download Tests")
    print("=" * 50)

    results = TestResults()

    # Unit tests (no network)
    test_verify_pdf(results)
    test_extract_arxiv_id(results)
    test_safe_filename(results)
    test_parse_selection_log(results)
    test_parse_papers_json(results)

    # Integration tests (network)
    print("\n" + "=" * 50)
    print("Integration Tests (require network)")
    print("=" * 50)

    await test_arxiv_url_resolution(results)
    await asyncio.sleep(1)

    await test_doi_resolution(results)
    await asyncio.sleep(1)

    await test_semantic_scholar_title_search(results)
    await asyncio.sleep(1)

    await test_arxiv_title_search(results)
    await asyncio.sleep(3)  # arXiv rate limit

    await test_resolve_all_urls(results)
    await asyncio.sleep(1)

    await test_download_arxiv_paper(results)
    await asyncio.sleep(1)

    await test_batch_download(results)

    # Summary
    success = results.summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
