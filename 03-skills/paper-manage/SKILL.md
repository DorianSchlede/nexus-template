---
name: paper-manage
description: Manage paper collections - list, rebuild indexes, view stats. Load when user says "list collections", "rebuild index", "paper stats", "collection status", or "manage papers". Scans collection folders and generates _collection.md indexes.
---

# Paper Manage

Manage paper collections in `04-workspace/papers/`.

## Commands

| User Says | Action |
|-----------|--------|
| "list collections" | Show all collections with stats |
| "collection status [name]" | Detailed status for one collection |
| "rebuild index [name]" | Regenerate _collection.md |
| "paper stats" | Aggregate stats across all collections |

## Workflow

### List Collections

1. Scan `04-workspace/papers/` for folders
2. For each collection folder:
   - Count paper folders (exclude `_*` files)
   - Check for `_briefing.md` (configured vs unconfigured)
   - Count papers with `index.md` (analyzed)
   - Count papers without `index.md` (pending)
3. Display summary table

### Rebuild Index

1. Read all `index.md` YAML frontmatter in collection
2. Read all `_metadata.json` for papers without index.md
3. Generate `_collection.md`:

```markdown
---
name: "{collection-name}"
papers_total: 15
papers_analyzed: 12
papers_pending: 3
total_tokens: 450000
last_updated: "2025-12-18"
---

# {Collection Name}

## Overview

- **Total Papers**: 15
- **Analyzed**: 12 (80%)
- **Pending**: 3

## Papers

### Analyzed

| Paper | Year | Topics | Chunks |
|-------|------|--------|--------|
| Braun_Clarke_2006 | 2006 | thematic analysis, qualitative | 5 |
| ... | ... | ... | ... |

### Pending Analysis

| Paper | Chunks | Est. Tokens |
|-------|--------|-------------|
| QualiGPT_2024 | 8 | ~45000 |
| ... | ... | ... |

## Topics (Aggregated)

- thematic analysis (8 papers)
- LLM coding (5 papers)
- qualitative research (12 papers)

## Last Updated

2025-12-18 14:30:00
```

### Collection Status

1. Read `_collection.md` if exists
2. If not exists, run rebuild index first
3. Display detailed stats:
   - Papers by status
   - Topics distribution
   - Total tokens
   - Last analysis date

## Script Usage

```bash
# List all collections
python 03-skills/paper-manage/scripts/paper_manage.py --list

# Rebuild collection index
python 03-skills/paper-manage/scripts/paper_manage.py --rebuild TA_LLM

# Get stats
python 03-skills/paper-manage/scripts/paper_manage.py --stats TA_LLM
```

## Error Handling

| Error | Action |
|-------|--------|
| No collections found | "No collections in 04-workspace/papers/" |
| Collection not found | List available collections |
| No index.md files | Mark all papers as pending |
