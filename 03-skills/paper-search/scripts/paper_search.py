#!/usr/bin/env python3
"""
Paper Search - Search and download academic papers from open access sources.

APIs: Semantic Scholar, OpenAlex, Unpaywall, arXiv, CrossRef, PubMed, CORE, BASE, DOAJ

Usage:
    python paper_search.py --title "Attention Is All You Need"
    python paper_search.py --doi "10.1145/3292500.3330701"
    python paper_search.py --arxiv "2301.12345"
    python paper_search.py --query "thematic analysis LLM" --limit 10
    python paper_search.py --query "..." --download --output ./papers/
"""

import os
import sys
import json
import re
import asyncio
import argparse
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, asdict
from urllib.parse import quote
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
RATE_LIMIT_DELAY = 1.0


@dataclass
class Paper:
    title: str
    authors: List[str]
    year: Optional[int]
    doi: Optional[str]
    abstract: Optional[str]
    citations: Optional[int]
    pdf_url: Optional[str]
    source: str  # Which API found it

    def to_dict(self) -> dict:
        return asdict(self)


class PaperSearcher:
    def __init__(self, email: str = EMAIL):
        self.email = email
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        self.session = aiohttp.ClientSession(
            connector=connector,
            headers={"User-Agent": f"PaperSearch/1.0 (mailto:{self.email})"}
        )
        return self

    async def __aexit__(self, *args):
        if self.session:
            await self.session.close()

    # --- 1. Semantic Scholar ---
    async def search_semantic_scholar(self, query: str, limit: int = 10) -> List[Paper]:
        """Search Semantic Scholar (200M+ papers, best for CS/AI)."""
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query[:200],
            "limit": limit,
            "fields": "paperId,title,authors,year,citationCount,openAccessPdf,externalIds,abstract"
        }
        papers = []
        try:
            async with self.session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("data", []):
                        pdf_url = None
                        if item.get("openAccessPdf"):
                            pdf_url = item["openAccessPdf"].get("url")
                        papers.append(Paper(
                            title=item.get("title", ""),
                            authors=[a.get("name", "") for a in item.get("authors", [])],
                            year=item.get("year"),
                            doi=item.get("externalIds", {}).get("DOI"),
                            abstract=item.get("abstract"),
                            citations=item.get("citationCount"),
                            pdf_url=pdf_url,
                            source="semantic_scholar"
                        ))
                elif resp.status == 429:
                    print("Rate limited by Semantic Scholar, waiting 60s...")
                    await asyncio.sleep(60)
        except Exception as e:
            print(f"Semantic Scholar error: {e}")
        return papers

    # --- 2. OpenAlex ---
    async def search_openalex(self, query: str, limit: int = 10) -> List[Paper]:
        """Search OpenAlex (250M+ works, broad academic coverage)."""
        url = f"https://api.openalex.org/works?search={quote(query[:100])}&per_page={limit}&mailto={self.email}"
        papers = []
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("results", []):
                        pdf_url = item.get("open_access", {}).get("oa_url")
                        papers.append(Paper(
                            title=item.get("title", ""),
                            authors=[a.get("author", {}).get("display_name", "")
                                    for a in item.get("authorships", [])],
                            year=item.get("publication_year"),
                            doi=item.get("doi", "").replace("https://doi.org/", "") if item.get("doi") else None,
                            abstract=None,
                            citations=item.get("cited_by_count"),
                            pdf_url=pdf_url,
                            source="openalex"
                        ))
        except Exception as e:
            print(f"OpenAlex error: {e}")
        return papers

    # --- 3. Unpaywall (DOI lookup) ---
    async def get_unpaywall(self, doi: str) -> Optional[str]:
        """Get open access PDF URL from Unpaywall via DOI."""
        url = f"https://api.unpaywall.org/v2/{doi}?email={self.email}"
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("best_oa_location"):
                        return data["best_oa_location"].get("url_for_pdf")
        except Exception as e:
            print(f"Unpaywall error: {e}")
        return None

    # --- 4. arXiv ---
    async def search_arxiv(self, query: str, limit: int = 10) -> List[Paper]:
        """Search arXiv (2M+ preprints, CS/Physics/Math)."""
        clean_query = re.sub(r'[^\w\s]', ' ', query)
        url = f"http://export.arxiv.org/api/query?search_query=all:{quote(clean_query)}&max_results={limit}"
        papers = []
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    text = await resp.text()
                    root = ET.fromstring(text)
                    ns = {'atom': 'http://www.w3.org/2005/Atom'}

                    for entry in root.findall('atom:entry', ns):
                        title = entry.find('atom:title', ns)
                        abstract = entry.find('atom:summary', ns)
                        published = entry.find('atom:published', ns)

                        authors = []
                        for author in entry.findall('atom:author', ns):
                            name = author.find('atom:name', ns)
                            if name is not None:
                                authors.append(name.text)

                        pdf_url = None
                        for link in entry.findall('atom:link', ns):
                            if link.get('title') == 'pdf':
                                pdf_url = link.get('href')
                                if pdf_url and not pdf_url.endswith('.pdf'):
                                    pdf_url += '.pdf'
                                break

                        year = None
                        if published is not None and published.text:
                            year = int(published.text[:4])

                        papers.append(Paper(
                            title=title.text.strip() if title is not None else "",
                            authors=authors,
                            year=year,
                            doi=None,
                            abstract=abstract.text.strip() if abstract is not None else None,
                            citations=None,
                            pdf_url=pdf_url,
                            source="arxiv"
                        ))
        except Exception as e:
            print(f"arXiv error: {e}")
        return papers

    # --- 5. CrossRef ---
    async def search_crossref(self, query: str, limit: int = 10) -> List[Paper]:
        """Search CrossRef (130M+ DOIs, metadata and references)."""
        url = f"https://api.crossref.org/works?query={quote(query[:100])}&rows={limit}&mailto={self.email}"
        papers = []
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("message", {}).get("items", []):
                        authors = []
                        for a in item.get("author", []):
                            name = f"{a.get('given', '')} {a.get('family', '')}".strip()
                            if name:
                                authors.append(name)

                        year = None
                        if item.get("published-print", {}).get("date-parts"):
                            year = item["published-print"]["date-parts"][0][0]
                        elif item.get("published-online", {}).get("date-parts"):
                            year = item["published-online"]["date-parts"][0][0]

                        # CrossRef doesn't provide PDF URLs directly
                        papers.append(Paper(
                            title=item.get("title", [""])[0] if item.get("title") else "",
                            authors=authors,
                            year=year,
                            doi=item.get("DOI"),
                            abstract=item.get("abstract", "").replace("<jats:p>", "").replace("</jats:p>", "") if item.get("abstract") else None,
                            citations=item.get("is-referenced-by-count"),
                            pdf_url=None,  # Will try Unpaywall for DOI
                            source="crossref"
                        ))
        except Exception as e:
            print(f"CrossRef error: {e}")
        return papers

    # --- 6. PubMed ---
    async def search_pubmed(self, query: str, limit: int = 10) -> List[Paper]:
        """Search PubMed (35M+ biomedical articles)."""
        # First, search for IDs
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={quote(query)}&retmax={limit}&retmode=json"
        papers = []
        try:
            async with self.session.get(search_url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    ids = data.get("esearchresult", {}).get("idlist", [])

                    if ids:
                        # Fetch details for IDs
                        ids_str = ",".join(ids)
                        fetch_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json"
                        async with self.session.get(fetch_url) as fetch_resp:
                            if fetch_resp.status == 200:
                                details = await fetch_resp.json()
                                for pmid in ids:
                                    item = details.get("result", {}).get(pmid, {})
                                    if isinstance(item, dict):
                                        authors = [a.get("name", "") for a in item.get("authors", [])]
                                        year = None
                                        if item.get("pubdate"):
                                            match = re.search(r'(\d{4})', item["pubdate"])
                                            if match:
                                                year = int(match.group(1))

                                        # Check for PMC (free full text)
                                        pdf_url = None
                                        pmc_id = item.get("pmcid")
                                        if pmc_id:
                                            pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"

                                        papers.append(Paper(
                                            title=item.get("title", ""),
                                            authors=authors,
                                            year=year,
                                            doi=item.get("elocationid", "").replace("doi: ", "") if "doi:" in item.get("elocationid", "") else None,
                                            abstract=None,
                                            citations=None,
                                            pdf_url=pdf_url,
                                            source="pubmed"
                                        ))
        except Exception as e:
            print(f"PubMed error: {e}")
        return papers

    # --- 7. CORE ---
    async def search_core(self, query: str, limit: int = 10) -> List[Paper]:
        """Search CORE (300M+ documents, UK/EU research, full-text)."""
        # CORE API v3 requires API key, using the free search endpoint
        url = f"https://api.core.ac.uk/v3/search/works?q={quote(query[:100])}&limit={limit}"
        papers = []
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("results", []):
                        authors = item.get("authors", [])
                        if authors and isinstance(authors[0], dict):
                            authors = [a.get("name", "") for a in authors]

                        pdf_url = None
                        if item.get("downloadUrl"):
                            pdf_url = item["downloadUrl"]

                        papers.append(Paper(
                            title=item.get("title", ""),
                            authors=authors if isinstance(authors, list) else [],
                            year=item.get("yearPublished"),
                            doi=item.get("doi"),
                            abstract=item.get("abstract"),
                            citations=None,
                            pdf_url=pdf_url,
                            source="core"
                        ))
                elif resp.status == 401:
                    pass  # API key required for full access
        except Exception as e:
            print(f"CORE error: {e}")
        return papers

    # --- 8. BASE (Bielefeld Academic Search Engine) ---
    async def search_base(self, query: str, limit: int = 10) -> List[Paper]:
        """Search BASE (300M+ documents, German aggregator)."""
        url = f"https://api.base-search.net/cgi-bin/BaseHttpSearchInterface.fcgi?func=PerformSearch&query={quote(query[:100])}&format=json&hits={limit}"
        papers = []
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("response", {}).get("docs", []):
                        authors = item.get("dccreator", [])
                        if isinstance(authors, str):
                            authors = [authors]

                        year = None
                        if item.get("dcdate"):
                            match = re.search(r'(\d{4})', str(item["dcdate"]))
                            if match:
                                year = int(match.group(1))

                        pdf_url = None
                        if item.get("dclink"):
                            link = item["dclink"]
                            if isinstance(link, list):
                                link = link[0]
                            if link and ('.pdf' in link.lower() or 'fulltext' in link.lower()):
                                pdf_url = link

                        papers.append(Paper(
                            title=item.get("dctitle", ""),
                            authors=authors,
                            year=year,
                            doi=item.get("dcoi"),
                            abstract=item.get("dcdescription"),
                            citations=None,
                            pdf_url=pdf_url,
                            source="base"
                        ))
        except Exception as e:
            print(f"BASE error: {e}")
        return papers

    # --- 9. DOAJ (Directory of Open Access Journals) ---
    async def search_doaj(self, query: str, limit: int = 10) -> List[Paper]:
        """Search DOAJ (9M+ verified OA articles)."""
        url = f"https://doaj.org/api/search/articles/{quote(query[:100])}?pageSize={limit}"
        papers = []
        try:
            async with self.session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    for item in data.get("results", []):
                        bibjson = item.get("bibjson", {})

                        authors = []
                        for a in bibjson.get("author", []):
                            name = a.get("name", "")
                            if name:
                                authors.append(name)

                        year = None
                        if bibjson.get("year"):
                            year = int(bibjson["year"])

                        pdf_url = None
                        for link in bibjson.get("link", []):
                            if link.get("type") == "fulltext":
                                pdf_url = link.get("url")
                                break

                        doi = None
                        for identifier in bibjson.get("identifier", []):
                            if identifier.get("type") == "doi":
                                doi = identifier.get("id")
                                break

                        papers.append(Paper(
                            title=bibjson.get("title", ""),
                            authors=authors,
                            year=year,
                            doi=doi,
                            abstract=bibjson.get("abstract"),
                            citations=None,
                            pdf_url=pdf_url,
                            source="doaj"
                        ))
        except Exception as e:
            print(f"DOAJ error: {e}")
        return papers

    # --- Download PDF ---
    async def download_pdf(self, url: str, filepath: Path) -> bool:
        """Download PDF from URL."""
        try:
            async with self.session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
                if resp.status == 200:
                    content = await resp.read()
                    is_pdf = (
                        "pdf" in resp.content_type.lower() or
                        content[:4] == b'%PDF' or
                        'arxiv.org' in url
                    )
                    if is_pdf:
                        filepath.parent.mkdir(parents=True, exist_ok=True)
                        filepath.write_bytes(content)
                        return True
        except Exception as e:
            print(f"Download error: {e}")
        return False

    # --- Combined Search ---
    async def search(self, query: str, limit: int = 10, sources: List[str] = None) -> List[Paper]:
        """Search across multiple APIs and deduplicate results."""
        if sources is None:
            sources = ["semantic_scholar", "openalex", "arxiv", "crossref", "pubmed", "core", "base", "doaj"]

        all_papers = []

        if "semantic_scholar" in sources:
            papers = await self.search_semantic_scholar(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        if "openalex" in sources:
            papers = await self.search_openalex(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        if "arxiv" in sources:
            papers = await self.search_arxiv(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(3)  # arXiv requires 3s delay

        if "crossref" in sources:
            papers = await self.search_crossref(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        if "pubmed" in sources:
            papers = await self.search_pubmed(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        if "core" in sources:
            papers = await self.search_core(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        if "base" in sources:
            papers = await self.search_base(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        if "doaj" in sources:
            papers = await self.search_doaj(query, limit)
            all_papers.extend(papers)
            await asyncio.sleep(RATE_LIMIT_DELAY)

        # Try to get PDF URLs for papers with DOI but no PDF
        for paper in all_papers:
            if paper.doi and not paper.pdf_url:
                pdf_url = await self.get_unpaywall(paper.doi)
                if pdf_url:
                    paper.pdf_url = pdf_url
                await asyncio.sleep(RATE_LIMIT_DELAY)

        # Deduplicate by title similarity
        seen_titles = set()
        unique_papers = []
        for paper in all_papers:
            title_key = paper.title.lower()[:50]
            if title_key not in seen_titles:
                seen_titles.add(title_key)
                unique_papers.append(paper)

        return unique_papers


def safe_filename(title: str, max_len: int = 50) -> str:
    """Convert title to safe filename."""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    return safe[:max_len]


async def main():
    parser = argparse.ArgumentParser(description="Search and download academic papers from 9 APIs")
    parser.add_argument("--title", help="Search by exact title")
    parser.add_argument("--query", "-q", help="Search by query terms")
    parser.add_argument("--doi", help="Lookup by DOI")
    parser.add_argument("--arxiv", help="Lookup by arXiv ID")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Max results per API (default: 10)")
    parser.add_argument("--output", "-o", type=Path, default=DEFAULT_OUTPUT, help="Output directory")
    parser.add_argument("--download", "-d", action="store_true", help="Download PDFs")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--sources", "-s", help="Comma-separated list of sources (default: all)")
    args = parser.parse_args()

    if not any([args.title, args.query, args.doi, args.arxiv]):
        parser.print_help()
        sys.exit(1)

    sources = None
    if args.sources:
        sources = [s.strip() for s in args.sources.split(",")]

    async with PaperSearcher() as searcher:
        papers = []

        if args.doi:
            # DOI lookup via Unpaywall
            pdf_url = await searcher.get_unpaywall(args.doi)
            if pdf_url:
                papers.append(Paper(
                    title=f"DOI: {args.doi}",
                    authors=[],
                    year=None,
                    doi=args.doi,
                    abstract=None,
                    citations=None,
                    pdf_url=pdf_url,
                    source="unpaywall"
                ))
        elif args.arxiv:
            # Direct arXiv lookup
            pdf_url = f"https://arxiv.org/pdf/{args.arxiv}.pdf"
            papers.append(Paper(
                title=f"arXiv: {args.arxiv}",
                authors=[],
                year=None,
                doi=None,
                abstract=None,
                citations=None,
                pdf_url=pdf_url,
                source="arxiv"
            ))
        else:
            # Search by title or query
            query = args.title or args.query
            papers = await searcher.search(query, args.limit, sources)

        if args.json:
            print(json.dumps([p.to_dict() for p in papers], indent=2))
        else:
            print(f"\nFound {len(papers)} papers:\n")
            for i, paper in enumerate(papers, 1):
                oa = "✓ OA" if paper.pdf_url else "✗ No OA"
                year = paper.year or "?"
                authors = ", ".join(paper.authors[:3])
                if len(paper.authors) > 3:
                    authors += " et al."
                print(f"{i}. [{year}] {paper.title[:70]}")
                print(f"   Authors: {authors}")
                print(f"   Citations: {paper.citations or '?'} | {oa} | Source: {paper.source}")
                if paper.abstract:
                    print(f"   Abstract: {paper.abstract[:150]}...")
                print()

        # Download if requested
        if args.download:
            output_dir = args.output
            downloaded = 0
            for paper in papers:
                if paper.pdf_url:
                    filename = safe_filename(paper.title) + ".pdf"
                    filepath = output_dir / filename
                    print(f"Downloading: {paper.title[:50]}...")
                    if await searcher.download_pdf(paper.pdf_url, filepath):
                        print(f"  ✓ Saved: {filepath}")
                        downloaded += 1
                    else:
                        print(f"  ✗ Failed")
            print(f"\nDownloaded {downloaded}/{len([p for p in papers if p.pdf_url])} papers")


if __name__ == "__main__":
    asyncio.run(main())
