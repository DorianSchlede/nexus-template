---
name: paper-query
description: Query paper collections with 3-level progressive disclosure. Load when user says "query papers", "find papers about", "search collection", "what papers discuss", or asks questions about analyzed papers. Uses lightweight frontmatter scan (Level 1), full index.md reading (Level 2), and chunk loading (Level 3).
---

# Paper Query

Query analyzed paper collections using progressive disclosure.

## Quick Commands

| User Says | Action |
|-----------|--------|
| "query papers about [topic]" | Search across all collections |
| "find papers in [collection] about [topic]" | Search specific collection |
| "what papers discuss [concept]" | Topic-based search |

## 3-Level Progressive Disclosure

### Level 1: Frontmatter Scan (Script)

Lightweight Python script extracts YAML frontmatter from all `index.md` files:

```bash
python 03-skills/paper-query/scripts/scan_frontmatter.py --collection TA_LLM --query "coding methods"
```

**Returns**: Ranked list of papers with match scores based on:
- `relevance_triggers` matches (highest weight)
- `topics` matches
- `methods` matches
- `key_findings` keyword matches

### Level 2: Full Index Reading (AI)

For top-N relevant papers from Level 1, AI reads full `index.md`:
- Chunk summaries and navigation
- Identifies which chunks likely contain the answer
- Reports: "Load chunk X from Paper Y for details on [topic]"

### Level 3: Chunk Loading (AI)

AI loads specific `{paper}_N.md` chunks on-demand:
- Extract precise answer with chunk reference
- Return with citation: "According to Braun & Clarke (Chunk 2)..."

## Workflow

### Simple Query

```
User: "What methods are used for thematic coding?"

1. Run: scan_frontmatter.py --query "thematic coding methods"
   → Returns: Braun_Clarke_2006 (score: 0.85), QualiGPT_2024 (score: 0.72)

2. AI reads index.md for top 3 papers
   → Finds: "Chunk 2 covers six-phase methodology"

3. AI loads Braun_Clarke_2006_2.md
   → Returns answer with citation
```

### Multi-Collection Query

```bash
# Search all collections
python 03-skills/paper-query/scripts/scan_frontmatter.py --query "LLM qualitative" --all

# Search specific collection
python 03-skills/paper-query/scripts/scan_frontmatter.py --collection TA_LLM --query "evaluation metrics"
```

## Ranking Factors

| Factor | Weight | Source |
|--------|--------|--------|
| relevance_triggers match | 3x | index.md YAML |
| topics match | 2x | index.md YAML |
| methods match | 2x | index.md YAML |
| key_findings match | 1x | index.md YAML |
| year (newer preferred) | 0.5x | index.md YAML |

## Script Usage

```bash
# Basic query
python 03-skills/paper-query/scripts/scan_frontmatter.py --query "thematic analysis"

# With collection filter
python 03-skills/paper-query/scripts/scan_frontmatter.py --collection TA_LLM --query "coding"

# JSON output for programmatic use
python 03-skills/paper-query/scripts/scan_frontmatter.py --query "..." --json

# Limit results
python 03-skills/paper-query/scripts/scan_frontmatter.py --query "..." --limit 5
```

## Error Handling

| Error | Action |
|-------|--------|
| No index.md files | "Collection not analyzed. Run paper-analyze first." |
| No matches | "No papers match query. Try broader terms." |
| Collection not found | List available collections |
