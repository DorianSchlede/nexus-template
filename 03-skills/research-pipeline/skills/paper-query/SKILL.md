---
name: paper-query
description: Query paper collections with 3-level progressive disclosure. Load when user says "query papers", "find papers about", "search collection", "what papers discuss", or asks questions about analyzed papers. Uses lightweight frontmatter scan (Level 1), full index.md reading (Level 2), and chunk loading (Level 3).
---

# Paper Query

Query analyzed paper collections using progressive disclosure.

## Key Scripts

| Script | Purpose |
|--------|---------|
| `scan_frontmatter.py` | Query papers by keyword matching (generic fields) |
| `aggregate_frontmatter.py` | Aggregate ALL frontmatter for field queries |
| `prepare_synthesis_chunks.py` | Route chunks to synthesis questions |

---

## Synthesis Preparation (NEW - Pre-Synthesis Step)

Before synthesis, run these scripts to prepare intelligent chunk routing:

### 1. Aggregate Frontmatter

```bash
# Get field coverage summary across all papers
python aggregate_frontmatter.py {papers_path} --summary

# Query which papers have a specific extraction field
python aggregate_frontmatter.py {papers_path} --query ai_integration

# Export to JSON for subagent context
python aggregate_frontmatter.py {papers_path} \
  --fields "entity_types,ai_integration,framework_comparison" \
  --output _aggregated_index.json
```

### 2. Prepare Chunk Routing

```bash
# Generate routing table mapping fields to chunks
python prepare_synthesis_chunks.py {project_path}

# Output: 02-resources/_synthesis_routing.yaml
```

**Output example:**
```yaml
fields:
  entity_types:
    priority: high
    papers:
    - paper_id: 02-Knowledge_Graphs
      chunks_to_read: [2, 6, 4]  # Specific chunks with entity data
      items_extracted: 21
    - paper_id: 05-DOLCE
      chunks_to_read: [1, 2]
      items_extracted: 24
  ai_integration:
    priority: high
    papers:
    - paper_id: 16-KG-Agent
      chunks_to_read: [1, 2]
      items_extracted: 8
```

This routing tells subagents EXACTLY which chunks to read for each synthesis field.

### 3. Synthesis Subagent Pattern

Use the routing to spawn focused subagents:

```
Task(
  subagent_type="general-purpose",
  prompt="""
  SYNTHESIS TASK: ai_integration

  Read _synthesis_routing.yaml for chunk assignments.

  For each paper listed under ai_integration:
    1. Read the specified chunks (e.g., 16-KG-Agent chunks 1, 2)
    2. Extract ai_integration patterns with chunk:line citations
    3. Aggregate across papers

  Write: 04-outputs/_synthesis_ai_integration.md
  """
)
```

---

## Quick Commands

| User Says | Action |
|-----------|--------|
| "query papers about [topic]" | Search across all collections |
| "find papers in [collection] about [topic]" | Search specific collection |
| "what papers discuss [concept]" | Topic-based search |
| "prepare synthesis" | Run aggregate + routing scripts |

---

## 3-Level Progressive Disclosure

### Level 1: Frontmatter Scan (Script)

Lightweight Python script extracts YAML frontmatter from all `index.md` files:

```bash
python scan_frontmatter.py --root {papers_path} --query "coding methods"
```

**Returns**: Ranked list of papers with match scores based on:
- `relevance_triggers` matches (highest weight)
- `topics` matches
- `methods` matches
- `key_findings` keyword matches

**Note**: For project-specific fields (entity_types, ai_integration, etc.), use `aggregate_frontmatter.py` instead.

### Level 2: Full Index Reading (AI)

For top-N relevant papers from Level 1, AI reads full `index.md`:
- Chunk summaries and navigation
- Identifies which chunks likely contain the answer
- Reports: "Load chunk X from Paper Y for details on [topic]"

### Level 3: Chunk Loading (AI)

AI loads specific `{paper}_N.md` chunks on-demand:
- Extract precise answer with chunk reference
- Return with citation: "According to Braun & Clarke (Chunk 2)..."

---

## Workflow Examples

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

### Synthesis Query

```
User: "Synthesize AI integration patterns across papers"

1. Run: prepare_synthesis_chunks.py {project_path}
   → Creates: _synthesis_routing.yaml

2. For field 'ai_integration':
   - Paper 16-KG-Agent: read chunks 1, 2
   - Paper 18-Multi-Agent-Taxonomy: read chunks 1
   - Paper 20-Agentic_RAG: read chunks 1, 3

3. Spawn subagent with routing table
   → Reads ONLY the specified chunks
   → Aggregates patterns with chunk:line citations

4. Output: _synthesis_ai_integration.md
```

---

## Script Usage

### scan_frontmatter.py (Generic Keyword Search)

```bash
# Basic query
python scan_frontmatter.py --root {papers_path} --query "thematic analysis"

# JSON output for programmatic use
python scan_frontmatter.py --root {papers_path} --query "..." --json

# Limit results
python scan_frontmatter.py --root {papers_path} --query "..." --limit 5
```

### aggregate_frontmatter.py (Field-Specific Queries)

```bash
# Summary of all fields across papers
python aggregate_frontmatter.py {papers_path} --summary

# Query specific field
python aggregate_frontmatter.py {papers_path} --query ai_integration

# Export specific fields to JSON
python aggregate_frontmatter.py {papers_path} \
  --fields "entity_types,framework_comparison" \
  --format json \
  --output _aggregated.json
```

### prepare_synthesis_chunks.py (Chunk Routing)

```bash
# Generate routing table for all fields
python prepare_synthesis_chunks.py {project_path}

# Output: {project_path}/02-resources/_synthesis_routing.yaml
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No index.md files | "Collection not analyzed. Run paper-analyze first." |
| No matches | "No papers match query. Try broader terms." |
| Collection not found | List available collections |
| No _briefing.md | Script infers fields from first paper's frontmatter |

---

**Version**: 2.0 (2025-12-28)
**Added**: aggregate_frontmatter.py, prepare_synthesis_chunks.py, synthesis preparation workflow
