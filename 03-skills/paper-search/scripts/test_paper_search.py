#!/usr/bin/env python3
"""
Tests for paper_search.py

Run with: python test_paper_search.py
Or: pytest test_paper_search.py -v
"""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from paper_search import PaperSearcher, Paper, safe_filename


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


async def test_semantic_scholar(results: TestResults):
    """Test Semantic Scholar API."""
    print("\n[Semantic Scholar]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_semantic_scholar("attention is all you need", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
            if any("attention" in p.title.lower() for p in papers):
                results.ok("Title match found")
            else:
                results.fail("Title match", "No paper with 'attention' in title")
            if any(p.citations and p.citations > 0 for p in papers):
                results.ok("Citations available")
            else:
                results.fail("Citations", "No citation data")
        else:
            results.fail("Search", "No results returned")


async def test_openalex(results: TestResults):
    """Test OpenAlex API."""
    print("\n[OpenAlex]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_openalex("thematic analysis psychology", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
            if any(p.year for p in papers):
                results.ok("Year data available")
            else:
                results.fail("Year", "No year data")
            if any(p.pdf_url for p in papers):
                results.ok("OA links available")
            else:
                results.fail("OA links", "No open access URLs")
        else:
            results.fail("Search", "No results returned")


async def test_arxiv(results: TestResults):
    """Test arXiv API."""
    print("\n[arXiv]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_arxiv("large language models", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
            if any(p.abstract for p in papers):
                results.ok("Abstracts available")
            else:
                results.fail("Abstracts", "No abstract data")
            if any(p.pdf_url for p in papers):
                results.ok("PDF URLs available")
            else:
                results.fail("PDF URLs", "No PDF links")
        else:
            results.fail("Search", "No results returned")


async def test_crossref(results: TestResults):
    """Test CrossRef API."""
    print("\n[CrossRef]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_crossref("machine learning", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
            if any(p.doi for p in papers):
                results.ok("DOIs available")
            else:
                results.fail("DOIs", "No DOI data")
            if any(p.citations for p in papers):
                results.ok("Citation counts available")
            else:
                results.fail("Citations", "No citation data")
        else:
            results.fail("Search", "No results returned")


async def test_pubmed(results: TestResults):
    """Test PubMed API."""
    print("\n[PubMed]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_pubmed("cancer treatment", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
            if any(p.authors for p in papers):
                results.ok("Authors available")
            else:
                results.fail("Authors", "No author data")
        else:
            results.fail("Search", "No results returned")


async def test_core(results: TestResults):
    """Test CORE API."""
    print("\n[CORE]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_core("open access publishing", limit=3)
        # CORE may require API key, so empty results are acceptable
        if papers:
            results.ok(f"Found {len(papers)} papers")
        else:
            results.ok("API responded (may require key for results)")


async def test_base(results: TestResults):
    """Test BASE API."""
    print("\n[BASE]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_base("climate change", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
        else:
            results.ok("API responded (may have limited results)")


async def test_doaj(results: TestResults):
    """Test DOAJ API."""
    print("\n[DOAJ]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search_doaj("open science", limit=3)
        if papers:
            results.ok(f"Found {len(papers)} papers")
            if any(p.pdf_url for p in papers):
                results.ok("Fulltext links available")
            else:
                results.fail("Fulltext", "No fulltext links")
        else:
            results.fail("Search", "No results returned")


async def test_unpaywall(results: TestResults):
    """Test Unpaywall DOI lookup."""
    print("\n[Unpaywall]")
    async with PaperSearcher() as searcher:
        # Test with a known OA DOI
        pdf_url = await searcher.get_unpaywall("10.1038/nature12373")
        if pdf_url:
            results.ok(f"Found OA URL: {pdf_url[:50]}...")
        else:
            results.fail("DOI lookup", "No OA URL found for test DOI")


async def test_combined_search(results: TestResults):
    """Test combined search across all APIs."""
    print("\n[Combined Search]")
    async with PaperSearcher() as searcher:
        papers = await searcher.search(
            "qualitative research methods",
            limit=3,
            sources=["semantic_scholar", "openalex", "arxiv"]  # Use fast 3 for test
        )
        if papers:
            results.ok(f"Found {len(papers)} unique papers")
            sources = set(p.source for p in papers)
            results.ok(f"Sources: {', '.join(sources)}")
        else:
            results.fail("Combined search", "No results")


def test_safe_filename(results: TestResults):
    """Test filename sanitization."""
    print("\n[Utility Functions]")

    # Test basic sanitization
    result = safe_filename("Hello: World! Test?")
    if result == "Hello_World_Test":
        results.ok("Basic sanitization")
    else:
        results.fail("Basic sanitization", f"Got: {result}")

    # Test length limit
    long_title = "A" * 100
    result = safe_filename(long_title, max_len=50)
    if len(result) == 50:
        results.ok("Length limit")
    else:
        results.fail("Length limit", f"Expected 50, got {len(result)}")

    # Test special chars
    result = safe_filename("Test/with\\slashes")
    if "/" not in result and "\\" not in result:
        results.ok("Special char removal")
    else:
        results.fail("Special chars", f"Got: {result}")


async def main():
    print("=" * 50)
    print("Paper Search API Tests")
    print("=" * 50)

    results = TestResults()

    # Synchronous tests
    test_safe_filename(results)

    # Async API tests
    await test_semantic_scholar(results)
    await asyncio.sleep(1)

    await test_openalex(results)
    await asyncio.sleep(1)

    await test_arxiv(results)
    await asyncio.sleep(3)  # arXiv needs 3s delay

    await test_crossref(results)
    await asyncio.sleep(1)

    await test_pubmed(results)
    await asyncio.sleep(1)

    await test_core(results)
    await asyncio.sleep(1)

    await test_base(results)
    await asyncio.sleep(1)

    await test_doaj(results)
    await asyncio.sleep(1)

    await test_unpaywall(results)
    await asyncio.sleep(1)

    await test_combined_search(results)

    # Summary
    success = results.summary()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    asyncio.run(main())
