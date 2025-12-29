#!/usr/bin/env python3
"""
Paper Download - Automated paper downloads with multi-source fallback.

Features:
- Input: _selection_log.md, paper list file, or direct URLs
- Multi-source URL resolution (arXiv, Semantic Scholar, OpenAlex, Unpaywall)
- Parallel downloads with progress tracking
- PDF verification (magic bytes check)
- Retry logic with exponential backoff
- Rate limiting per source
- Download status tracking and reporting

Usage:
    python paper_download.py --input _selection_log.md --output ./papers/
    python paper_download.py --input papers.json --output ./papers/ --parallel 5
    python paper_download.py --url "https://arxiv.org/pdf/2301.12345" --output ./papers/
    python paper_download.py --title "Attention Is All You Need" --output ./papers/
"""

import os
import sys
import json
import re
import asyncio
import argparse
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Tuple, Any
from dataclasses import dataclass, asdict, field
from datetime import datetime
from urllib.parse import quote, urlparse
import xml.etree.ElementTree as ET

# Fix Windows console encoding
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

try:
    import aiohttp
    import ssl
except ImportError:
    print("ERROR: aiohttp required. Install with: pip install aiohttp")
    sys.exit(1)


# Configuration
EMAIL = os.environ.get("PAPER_SEARCH_EMAIL", "research@example.com")
DEFAULT_OUTPUT = Path("04-workspace/papers")
DEFAULT_PARALLEL = 3
MAX_RETRIES = 3
RETRY_DELAY_BASE = 2  # seconds, exponential backoff
RATE_LIMITS = {
    "arxiv": 3.0,  # 3 seconds between requests
    "semantic_scholar": 1.0,
    "openalex": 0.5,
    "unpaywall": 1.0,
    "crossref": 1.0,
    "default": 1.0,
}


@dataclass
class DownloadResult:
    """Result of a download attempt."""
    paper_id: str
    title: str
    status: str  # "success", "failed", "skipped"
    pdf_path: Optional[str] = None
    source_used: Optional[str] = None
    urls_tried: List[str] = field(default_factory=list)
    error: Optional[str] = None
    file_size: int = 0
    download_time: float = 0.0


@dataclass
class PaperEntry:
    """Paper entry for download."""
    id: str
    title: str
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    urls: List[str] = field(default_factory=list)
    source: Optional[str] = None


def verify_pdf(content: bytes) -> Tuple[bool, str]:
    """Verify if content is a valid PDF by checking magic bytes."""
    if len(content) < 5:
        return False, "File too small"

    # PDF magic bytes
    if content[:5] == b'%PDF-':
        return True, "Valid PDF"

    # Check for HTML error page
    if b'<html' in content[:200].lower() or b'<!doctype' in content[:200].lower():
        return False, "HTML error page (not PDF)"

    # Check for gzip (sometimes PDFs are compressed)
    if content[:2] == b'\x1f\x8b':
        return True, "Gzip-compressed PDF"

    return False, f"Unknown format (first bytes: {content[:10]})"


def extract_arxiv_id(text: str) -> Optional[str]:
    """Extract arXiv ID from URL or text."""
    patterns = [
        r'arxiv\.org/abs/(\d{4}\.\d{4,5}(?:v\d+)?)',
        r'arxiv\.org/pdf/(\d{4}\.\d{4,5}(?:v\d+)?)',
        r'arxiv:(\d{4}\.\d{4,5}(?:v\d+)?)',
        r'\b(\d{4}\.\d{4,5}(?:v\d+)?)\b',  # Plain arXiv ID
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None


def safe_filename(title: str, max_len: int = 50) -> str:
    """Convert title to safe filename."""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    return safe[:max_len].strip('_')


class PaperDownloader:
    """Download papers with multi-source fallback and retry logic."""

    def __init__(self, email: str = EMAIL, parallel: int = DEFAULT_PARALLEL):
        self.email = email
        self.parallel = parallel
        self.session: Optional[aiohttp.ClientSession] = None
        self.semaphore: Optional[asyncio.Semaphore] = None
        self.rate_limiters: Dict[str, float] = {}  # Last request time per source

    async def __aenter__(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = aiohttp.TCPConnector(ssl=ssl_context, limit=self.parallel * 2)
        timeout = aiohttp.ClientTimeout(total=120)
        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=timeout,
            headers={"User-Agent": f"PaperDownloader/1.0 (mailto:{self.email})"}
        )
        self.semaphore = asyncio.Semaphore(self.parallel)
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    async def _rate_limit(self, source: str):
        """Enforce rate limiting per source."""
        delay = RATE_LIMITS.get(source, RATE_LIMITS["default"])
        now = asyncio.get_event_loop().time()
        last = self.rate_limiters.get(source, 0)
        wait = delay - (now - last)
        if wait > 0:
            await asyncio.sleep(wait)
        self.rate_limiters[source] = asyncio.get_event_loop().time()

    async def resolve_arxiv_url(self, arxiv_id: str) -> Optional[str]:
        """Resolve arXiv ID to PDF URL."""
        # Clean the ID
        arxiv_id = arxiv_id.replace(".pdf", "")
        if arxiv_id.startswith("arxiv:"):
            arxiv_id = arxiv_id[6:]
        return f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    async def resolve_doi_urls(self, doi: str) -> List[str]:
        """Resolve DOI to PDF URLs via multiple sources."""
        urls = []

        # 1. Try Unpaywall
        await self._rate_limit("unpaywall")
        try:
            url = f"https://api.unpaywall.org/v2/{doi}?email={self.email}"
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("best_oa_location"):
                        pdf_url = data["best_oa_location"].get("url_for_pdf")
                        if pdf_url:
                            urls.append(pdf_url)
                    # Also check other locations
                    for loc in data.get("oa_locations", []):
                        pdf_url = loc.get("url_for_pdf")
                        if pdf_url and pdf_url not in urls:
                            urls.append(pdf_url)
        except Exception as e:
            print(f"  Unpaywall error for {doi}: {e}")

        # 2. Try Semantic Scholar
        await self._rate_limit("semantic_scholar")
        try:
            url = f"https://api.semanticscholar.org/graph/v1/paper/DOI:{doi}?fields=openAccessPdf,externalIds"
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("openAccessPdf"):
                        pdf_url = data["openAccessPdf"].get("url")
                        if pdf_url and pdf_url not in urls:
                            urls.append(pdf_url)
                    # Check for arXiv
                    if data.get("externalIds", {}).get("ArXiv"):
                        arxiv_id = data["externalIds"]["ArXiv"]
                        arxiv_url = await self.resolve_arxiv_url(arxiv_id)
                        if arxiv_url and arxiv_url not in urls:
                            urls.insert(0, arxiv_url)  # Prefer arXiv
        except Exception as e:
            print(f"  S2 error for {doi}: {e}")

        return urls

    async def search_arxiv_by_title(self, title: str) -> Optional[str]:
        """Search arXiv for a paper by title and return PDF URL."""
        await self._rate_limit("arxiv")
        try:
            # Clean title for search - remove special chars
            clean_title = re.sub(r'[^\w\s]', ' ', title)
            # Use all:title for better matching
            url = f"http://export.arxiv.org/api/query?search_query=all:{quote(clean_title[:100])}&max_results=5"
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    root = ET.fromstring(text)
                    ns = {'atom': 'http://www.w3.org/2005/Atom'}

                    # Find best match - be more lenient with matching
                    search_words = set(title.lower().split())

                    for entry in root.findall('atom:entry', ns):
                        entry_title = entry.find('atom:title', ns)
                        if entry_title is not None and entry_title.text:
                            entry_text = entry_title.text.strip()
                            entry_words = set(entry_text.lower().split())

                            # Calculate word overlap
                            common = len(search_words & entry_words)
                            total = len(search_words | entry_words)
                            similarity = common / total if total > 0 else 0

                            # Accept if >50% word overlap or first 30 chars match
                            entry_clean = re.sub(r'\s+', ' ', entry_text.lower())[:30]
                            search_clean = re.sub(r'\s+', ' ', title.lower())[:30]

                            if similarity > 0.5 or entry_clean == search_clean:
                                for link in entry.findall('atom:link', ns):
                                    if link.get('title') == 'pdf':
                                        pdf_url = link.get('href')
                                        if pdf_url and not pdf_url.endswith('.pdf'):
                                            pdf_url += '.pdf'
                                        print(f"  Found on arXiv: {entry_text[:50]}...")
                                        return pdf_url
        except Exception as e:
            print(f"  arXiv search error: {e}")
        return None

    async def search_semantic_scholar_by_title(self, title: str) -> List[str]:
        """Search Semantic Scholar by title and return PDF URLs."""
        await self._rate_limit("semantic_scholar")
        urls = []
        try:
            search_url = f"https://api.semanticscholar.org/graph/v1/paper/search?query={quote(title[:100])}&limit=3&fields=openAccessPdf,externalIds,title"
            async with self.session.get(search_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for paper in data.get("data", []):
                        # Check title match
                        paper_title = paper.get("title", "").lower()
                        search_title = title.lower()

                        # Accept if titles are similar
                        if paper_title[:40] == search_title[:40] or any(
                            w in paper_title for w in search_title.split()[:3]
                        ):
                            # Check for arXiv ID
                            if paper.get("externalIds", {}).get("ArXiv"):
                                arxiv_id = paper["externalIds"]["ArXiv"]
                                arxiv_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                                if arxiv_url not in urls:
                                    urls.insert(0, arxiv_url)
                                    print(f"  Found arXiv ID via S2: {arxiv_id}")

                            # Check for direct PDF
                            if paper.get("openAccessPdf"):
                                pdf_url = paper["openAccessPdf"].get("url")
                                if pdf_url and pdf_url not in urls:
                                    urls.append(pdf_url)
        except Exception as e:
            print(f"  S2 title search error: {e}")
        return urls

    async def resolve_all_urls(self, paper: PaperEntry) -> List[str]:
        """Resolve all possible PDF URLs for a paper."""
        urls = list(paper.urls)  # Start with provided URLs

        # 1. arXiv ID takes priority
        if paper.arxiv_id:
            arxiv_url = await self.resolve_arxiv_url(paper.arxiv_id)
            if arxiv_url and arxiv_url not in urls:
                urls.insert(0, arxiv_url)

        # 2. Try DOI resolution
        if paper.doi:
            doi_urls = await self.resolve_doi_urls(paper.doi)
            for url in doi_urls:
                if url not in urls:
                    urls.append(url)

        # 3. Try Semantic Scholar title search
        if not urls or not any('arxiv.org' in u for u in urls):
            s2_urls = await self.search_semantic_scholar_by_title(paper.title)
            for url in s2_urls:
                if url not in urls:
                    urls.append(url)

        # 4. Try arXiv title search as fallback
        if not urls or not any('arxiv.org' in u for u in urls):
            arxiv_url = await self.search_arxiv_by_title(paper.title)
            if arxiv_url and arxiv_url not in urls:
                urls.append(arxiv_url)

        return urls

    async def download_with_retry(self, url: str, filepath: Path, max_retries: int = MAX_RETRIES) -> Tuple[bool, str, bytes]:
        """Download with exponential backoff retry."""
        last_error = ""
        content = b""

        for attempt in range(max_retries):
            try:
                # Determine source for rate limiting
                parsed = urlparse(url)
                if "arxiv" in parsed.netloc:
                    source = "arxiv"
                elif "semanticscholar" in parsed.netloc:
                    source = "semantic_scholar"
                elif "openalex" in parsed.netloc:
                    source = "openalex"
                else:
                    source = "default"

                await self._rate_limit(source)

                async with self.session.get(url, allow_redirects=True) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        is_pdf, msg = verify_pdf(content)
                        if is_pdf:
                            filepath.parent.mkdir(parents=True, exist_ok=True)
                            filepath.write_bytes(content)
                            return True, msg, content
                        else:
                            last_error = msg
                    elif resp.status == 429:
                        # Rate limited
                        retry_after = int(resp.headers.get("Retry-After", 60))
                        print(f"  Rate limited, waiting {retry_after}s...")
                        await asyncio.sleep(retry_after)
                        continue
                    else:
                        last_error = f"HTTP {resp.status}"

            except asyncio.TimeoutError:
                last_error = "Timeout"
            except Exception as e:
                last_error = str(e)

            # Exponential backoff
            if attempt < max_retries - 1:
                delay = RETRY_DELAY_BASE ** attempt
                await asyncio.sleep(delay)

        return False, last_error, content

    async def download_paper(self, paper: PaperEntry, output_dir: Path) -> DownloadResult:
        """Download a single paper with fallback URLs."""
        async with self.semaphore:
            start_time = asyncio.get_event_loop().time()

            # Resolve all possible URLs
            urls = await self.resolve_all_urls(paper)

            if not urls:
                return DownloadResult(
                    paper_id=paper.id,
                    title=paper.title,
                    status="failed",
                    error="No download URLs found",
                    urls_tried=[],
                )

            # Try each URL
            filename = f"{paper.id}-{safe_filename(paper.title)}.pdf"
            filepath = output_dir / filename

            for url in urls:
                print(f"  Trying: {url[:60]}...")
                success, msg, content = await self.download_with_retry(url, filepath)

                if success:
                    elapsed = asyncio.get_event_loop().time() - start_time
                    return DownloadResult(
                        paper_id=paper.id,
                        title=paper.title,
                        status="success",
                        pdf_path=str(filepath),
                        source_used=url,
                        urls_tried=urls[:urls.index(url) + 1],
                        file_size=len(content),
                        download_time=elapsed,
                    )

            # All URLs failed
            elapsed = asyncio.get_event_loop().time() - start_time
            return DownloadResult(
                paper_id=paper.id,
                title=paper.title,
                status="failed",
                error=f"All URLs failed: {msg}",
                urls_tried=urls,
                download_time=elapsed,
            )

    async def download_batch(self, papers: List[PaperEntry], output_dir: Path) -> List[DownloadResult]:
        """Download multiple papers in parallel."""
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        total = len(papers)

        for i, paper in enumerate(papers, 1):
            print(f"\n[{i}/{total}] Downloading: {paper.title[:50]}...")
            result = await self.download_paper(paper, output_dir)
            results.append(result)

            if result.status == "success":
                size_mb = result.file_size / (1024 * 1024)
                print(f"  ✓ Success: {size_mb:.1f} MB in {result.download_time:.1f}s")
            else:
                print(f"  ✗ Failed: {result.error}")

        return results


def parse_selection_log(filepath: Path) -> List[PaperEntry]:
    """Parse _selection_log.md to extract papers for download."""
    papers = []
    content = filepath.read_text(encoding='utf-8')

    # Look for markdown table format
    # | # | Paper | URL | Status |
    table_pattern = r'\|\s*(\d+)\s*\|\s*([^|]+)\s*\|\s*([^|]*)\s*\|'

    for match in re.finditer(table_pattern, content):
        paper_id = match.group(1).strip()
        title = match.group(2).strip()
        url_or_info = match.group(3).strip()

        # Skip header rows
        if paper_id.lower() in ['#', 'id', 'no'] or title.lower() in ['paper', 'title']:
            continue

        # Extract URL if present
        urls = re.findall(r'https?://[^\s\)]+', url_or_info)

        # Try to extract DOI
        doi_match = re.search(r'10\.\d{4,}/[^\s]+', url_or_info)
        doi = doi_match.group(0).rstrip('.,)') if doi_match else None

        # Try to extract arXiv ID
        arxiv_id = extract_arxiv_id(url_or_info)

        papers.append(PaperEntry(
            id=paper_id,
            title=title,
            doi=doi,
            arxiv_id=arxiv_id,
            urls=urls,
        ))

    # Also look for YAML frontmatter format
    if not papers:
        yaml_section = re.search(r'papers:\s*((?:\s+-\s+.*)+)', content, re.DOTALL)
        if yaml_section:
            # Parse simple YAML-like list
            for i, line in enumerate(yaml_section.group(1).split('\n'), 1):
                if line.strip().startswith('-'):
                    title = line.strip()[1:].strip()
                    papers.append(PaperEntry(id=str(i), title=title))

    return papers


def parse_papers_json(filepath: Path) -> List[PaperEntry]:
    """Parse JSON file with paper entries."""
    data = json.loads(filepath.read_text(encoding='utf-8'))
    papers = []

    # Handle list of papers
    paper_list = data if isinstance(data, list) else data.get('papers', [])

    for i, item in enumerate(paper_list, 1):
        if isinstance(item, str):
            papers.append(PaperEntry(id=str(i), title=item))
        elif isinstance(item, dict):
            papers.append(PaperEntry(
                id=str(item.get('id', i)),
                title=item.get('title', ''),
                doi=item.get('doi'),
                arxiv_id=item.get('arxiv_id') or item.get('arxiv'),
                urls=item.get('urls', []) or ([item['url']] if item.get('url') else []),
            ))

    return papers


def generate_report(results: List[DownloadResult], output_dir: Path) -> str:
    """Generate download report."""
    success = [r for r in results if r.status == "success"]
    failed = [r for r in results if r.status == "failed"]
    skipped = [r for r in results if r.status == "skipped"]

    total_size = sum(r.file_size for r in success)
    total_time = sum(r.download_time for r in results)

    report = f"""# Paper Download Report
**Generated**: {datetime.now().isoformat()}
**Output Directory**: {output_dir}

## Summary

| Metric | Value |
|--------|-------|
| Total Papers | {len(results)} |
| Downloaded | {len(success)} |
| Failed | {len(failed)} |
| Skipped | {len(skipped)} |
| **Success Rate** | **{len(success)/len(results)*100:.0f}%** |
| Total Size | {total_size / (1024*1024):.1f} MB |
| Total Time | {total_time:.1f}s |

"""

    if success:
        report += "## Downloaded Papers\n\n"
        report += "| # | Paper | Size | Source |\n|---|-------|------|--------|\n"
        for r in success:
            size_mb = r.file_size / (1024 * 1024)
            source = urlparse(r.source_used).netloc if r.source_used else "?"
            report += f"| {r.paper_id} | {r.title[:50]} | {size_mb:.1f} MB | {source} |\n"
        report += "\n"

    if failed:
        report += "## Failed Downloads\n\n"
        report += "| # | Paper | Error | URLs Tried |\n|---|-------|-------|------------|\n"
        for r in failed:
            urls_count = len(r.urls_tried)
            report += f"| {r.paper_id} | {r.title[:50]} | {r.error} | {urls_count} URLs |\n"
        report += "\n"

        # Detailed failures
        report += "### Failure Details\n\n"
        for r in failed:
            report += f"**Paper {r.paper_id}**: {r.title}\n"
            report += f"- Error: {r.error}\n"
            report += f"- URLs tried:\n"
            for url in r.urls_tried:
                report += f"  - {url}\n"
            report += "\n"

    return report


async def main():
    parser = argparse.ArgumentParser(description="Download papers with multi-source fallback")
    parser.add_argument("--input", "-i", type=Path, help="Input file (_selection_log.md or papers.json)")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT, help="Output directory")
    parser.add_argument("--parallel", "-p", type=int, default=DEFAULT_PARALLEL, help="Parallel downloads")
    parser.add_argument("--url", "-u", help="Download single URL")
    parser.add_argument("--title", "-t", help="Search and download by title")
    parser.add_argument("--doi", help="Download by DOI")
    parser.add_argument("--arxiv", help="Download by arXiv ID")
    parser.add_argument("--retry", "-r", type=int, default=MAX_RETRIES, help="Max retries per URL")
    parser.add_argument("--verify", "-v", action="store_true", help="Verify existing PDFs")
    parser.add_argument("--report", action="store_true", help="Generate download report")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    args = parser.parse_args()

    papers = []

    # Parse input
    if args.input:
        if not args.input.exists():
            print(f"ERROR: Input file not found: {args.input}")
            sys.exit(1)

        if args.input.suffix == '.json':
            papers = parse_papers_json(args.input)
        elif args.input.suffix == '.md' or args.input.name.startswith('_selection'):
            papers = parse_selection_log(args.input)
        else:
            print(f"ERROR: Unknown input format: {args.input}")
            sys.exit(1)

        print(f"Loaded {len(papers)} papers from {args.input}")

    elif args.url:
        papers = [PaperEntry(id="1", title="Direct URL", urls=[args.url])]

    elif args.doi:
        papers = [PaperEntry(id="1", title=f"DOI: {args.doi}", doi=args.doi)]

    elif args.arxiv:
        papers = [PaperEntry(id="1", title=f"arXiv: {args.arxiv}", arxiv_id=args.arxiv)]

    elif args.title:
        papers = [PaperEntry(id="1", title=args.title)]

    else:
        parser.print_help()
        sys.exit(1)

    if not papers:
        print("ERROR: No papers to download")
        sys.exit(1)

    # Download
    async with PaperDownloader(parallel=args.parallel) as downloader:
        results = await downloader.download_batch(papers, args.output)

    # Output
    success = sum(1 for r in results if r.status == "success")
    failed = sum(1 for r in results if r.status == "failed")

    print(f"\n{'='*50}")
    print(f"Download Complete: {success}/{len(results)} papers")
    print(f"Success: {success} | Failed: {failed}")
    print(f"Output: {args.output}")

    if args.json:
        print(json.dumps([asdict(r) for r in results], indent=2))

    if args.report or True:  # Always generate report
        report = generate_report(results, args.output)
        report_path = args.output / "_download_report.md"
        report_path.write_text(report, encoding='utf-8')
        print(f"Report: {report_path}")

    # Exit code based on success
    sys.exit(0 if success > 0 else 1)


if __name__ == "__main__":
    asyncio.run(main())
