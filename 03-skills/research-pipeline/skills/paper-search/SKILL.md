---
name: paper-search
description: Search and download academic papers from 9 open access APIs. Load when user says "find paper", "search paper", "download paper", "get paper", "batch download", or provides a paper title/DOI. Uses Semantic Scholar, OpenAlex, Unpaywall, arXiv, CrossRef, PubMed, CORE, BASE, and DOAJ. Includes automated batch download with fallback resolution.
---

# Paper Search

Search and download academic papers from 9 open access sources with automated fallback resolution.

## APIs (1B+ documents)

| API | Coverage | Best For |
|-----|----------|----------|
| Semantic Scholar | 200M+ | CS/AI, citations |
| OpenAlex | 250M+ | Broad academic |
| arXiv | 2M+ | CS/Physics/Math preprints |
| CrossRef | 130M+ | DOI metadata |
| PubMed | 35M+ | Biomedical |
| CORE | 300M+ | UK/EU research |
| BASE | 300M+ | German aggregator |
| DOAJ | 9M+ | Verified OA journals |
| Unpaywall | - | OA PDF lookup via DOI |

## Quick Commands

| User Says | Action |
|-----------|--------|
| "find paper [title]" | Search all APIs, show results |
| "download paper [title]" | Search + download PDF |
| "batch download from selection log" | Use paper_download.py |
| "get doi:10.xxx/xxx" | DOI lookup via Unpaywall |
| "get arxiv:2301.12345" | Direct arXiv download |

---

## Scripts

### 1. paper_search.py - Search and Single Downloads

```bash
# Search all 9 APIs
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py --query "thematic analysis LLM" --limit 5

# Search specific APIs only
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py --query "..." --sources "semantic_scholar,arxiv,pubmed"

# Search and download
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py --query "..." --download --output ./papers/

# DOI / arXiv lookup
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py --doi "10.1145/3292500.3330701"
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py --arxiv "2301.12345"

# JSON output
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py --query "..." --json
```

### 2. paper_download.py - Batch Downloads with Fallback (NEW)

Automated batch downloads with multi-source URL resolution, parallel processing, and PDF verification.

```bash
# Download from selection log (research project workflow)
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --input "03-working/_selection_log.md" \
  --output "02-resources/" \
  --parallel 5

# Download from JSON file
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --input papers.json \
  --output ./papers/

# Single paper by DOI
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --doi "10.1145/3292500.3330701" \
  --output ./papers/

# Single paper by arXiv ID
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --arxiv "2401.07324" \
  --output ./papers/

# Search by title and download
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --title "Attention Is All You Need" \
  --output ./papers/
```

#### Features

- **Multi-source fallback**: arXiv → Semantic Scholar → Unpaywall → Direct URL
- **Parallel downloads**: `--parallel N` for concurrent downloads
- **PDF verification**: Checks magic bytes to detect HTML error pages
- **Retry logic**: Exponential backoff on failures
- **Rate limiting**: Per-source rate limits to avoid bans
- **Download report**: Generates `_download_report.md` with success/fail stats

#### Input Formats

**Selection Log (markdown table):**
```markdown
| # | Paper | URL |
|---|-------|-----|
| 1 | AutoGen | https://arxiv.org/abs/2308.08155 |
| 2 | LangChain | doi:10.1234/example |
```

**JSON file:**
```json
{
  "papers": [
    {"id": "1", "title": "AutoGen", "arxiv_id": "2308.08155"},
    {"id": "2", "title": "Paper", "doi": "10.1234/example"}
  ]
}
```

#### Output

```
02-resources/
├── 1-AutoGen.pdf
├── 2-LangChain.pdf
└── _download_report.md
```

---

## Workflow Integration

### Research Project Download Workflow

In `create-research-project`, Step 7 now uses `paper_download.py`:

```bash
# After user approves selection
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_download.py \
  --input "02-projects/NN-slug/03-working/_selection_log.md" \
  --output "02-projects/NN-slug/02-resources/" \
  --parallel 3
```

This replaces manual curl commands with automated batch downloads.

### URL Resolution Priority

1. **arXiv ID** → Direct PDF (most reliable)
2. **DOI via Semantic Scholar** → Often has PDF + arXiv link
3. **DOI via Unpaywall** → OA PDF from repositories
4. **Title search on arXiv** → Fallback for paywalled papers
5. **Direct URL** → Original URL if from known OA source

### Paywall Fallback Strategy

See `alt_sources.yaml` for domain-specific fallback rules:

```yaml
acm.org:
  fallback: arxiv
  pattern: "Search arXiv by exact title"

springer.com:
  fallback: semanticscholar
  pattern: "Check S2 for open access PDF"
```

---

## Configuration

```bash
export PAPER_SEARCH_EMAIL="your-email@example.com"  # Higher rate limits
```

## Testing

```bash
# Test paper search APIs (9 sources)
python 03-skills/research-pipeline/skills/paper-search/scripts/test_paper_search.py

# Test paper download (34 tests)
python 03-skills/research-pipeline/skills/paper-search/scripts/test_paper_download.py
```

**Download tests cover:**
- PDF verification (magic bytes, HTML detection)
- arXiv ID extraction from various formats
- Selection log parsing (markdown tables)
- JSON input parsing
- URL resolution (arXiv, S2, Unpaywall)
- Title search fallback
- Single and batch downloads

## Files in This Skill

| File | Purpose |
|------|---------|
| `paper_search.py` | Search APIs, single downloads |
| `paper_download.py` | Batch downloads with fallback |
| `alt_sources.yaml` | Paywall → OA fallback mappings |
| `test_paper_search.py` | API test suite |
| `test_paper_download.py` | Download test suite (34 tests) |

## Limitations

- Only downloads **open access** papers (legal, free)
- Rate limits: ~1 req/sec (arXiv: 3s delay)
- Some APIs may require API keys for full access (CORE)
- Paywalled papers without OA versions will fail (tracked in report)

---

**Version**: 2.0 (2025-12-19)
**Changes**: Added paper_download.py for batch downloads with multi-source fallback
