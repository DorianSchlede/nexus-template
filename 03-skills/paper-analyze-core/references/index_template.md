# Index.md Template

**Purpose**: Template for paper analysis output. Subagents MUST follow this exact structure.

---

## YAML Frontmatter (REQUIRED)

```yaml
---
# REQUIRED (always present)
title: ""                    # Paper title from _metadata.json
authors: []                  # List of authors (if available)
year: null                   # Publication year (if available)
doi: ""                      # DOI if available
chunks: 0                    # Total chunks in paper (from _metadata.json)
tokens_estimated: 0          # Estimated token count (chars / 5 * 1.3)
analyzed_at: ""              # ISO timestamp (YYYY-MM-DDTHH:MM:SS)

# DYNAMIC (from _briefing.md extraction_schema)
# Populate ALL fields listed in briefing, or mark N/A
topics: []
methods: []
key_findings: []
limitations: []
relevance_triggers: []
# ... additional custom fields from briefing
---
```

---

## Body Structure (REQUIRED)

```markdown
# {Paper Title} - Analysis Index

## Paper Overview

- **Source**: {pdf filename from _metadata.json}
- **Chunks**: {N} chunks, ~{tokens_estimated} tokens
- **Analyzed**: {ISO timestamp}

## Key Extractions

[2-3 paragraph summary of most important findings, organized by schema fields from briefing]

### Topics
- Topic 1: Brief description (Chunk X)
- Topic 2: Brief description (Chunk Y)

### Methods
- Method 1: Brief description with chunk reference (Chunk X)

### Key Findings
- Finding 1 (Chunk X): "Direct quote if available" or summary
- Finding 2 (Chunk Y): "Direct quote if available" or summary

### Limitations
- Limitation 1 (Chunk X): Description
- [UNCERTAIN: ...] if not clearly stated

## Chunk Navigation

### Chunk 1: {Section Title from chunk header}
- **Summary**: 2-3 sentence description of chunk content
- **Key concepts**: [concept1, concept2, concept3]
- **Load when**: "User asks about X" / "Query mentions Y"

### Chunk 2: {Section Title}
- **Summary**: ...
- **Key concepts**: [...]
- **Load when**: "..."

[Continue for ALL chunks - every chunk MUST have an entry]
```

---

## Quality Checklist

Before writing index.md, verify:

- [ ] YAML frontmatter has ALL fields from _briefing.md extraction_schema
- [ ] Empty fields marked as `[]` or `N/A - not mentioned in paper`
- [ ] Every finding has chunk reference (e.g., "Chunk 3")
- [ ] Every chunk has navigation entry with Summary, Key concepts, Load when
- [ ] Uncertain extractions flagged with `[UNCERTAIN: reason]`
- [ ] Direct quotes include chunk reference

---

## Example Output

```yaml
---
title: "Auto-TA: Automated Thematic Analysis with Multi-Agent Systems"
authors: ["Smith, J.", "Chen, L."]
year: 2024
doi: "10.1234/example"
chunks: 4
tokens_estimated: 24000
analyzed_at: "2025-12-19T14:30:00"

topics: ["thematic analysis automation", "multi-agent systems", "LLM coding"]
methods: ["role conditioning", "3-tier architecture", "RLHF refinement"]
key_findings:
  - "Multi-agent ensemble improves credibility by 16%"
  - "Temperature=0 essential for reproducibility"
limitations: ["Single domain tested", "No comparison to human coders"]
relevance_triggers: ["multi-agent TA", "automated coding", "role conditioning"]
---

# Auto-TA: Automated Thematic Analysis - Analysis Index

## Paper Overview

- **Source**: Auto_TA.pdf
- **Chunks**: 4 chunks, ~24,000 tokens
- **Analyzed**: 2025-12-19T14:30:00

## Key Extractions

This paper presents Auto-TA, a multi-agent system for automating thematic analysis...

### Topics
- Thematic analysis automation (Chunks 1-2)
- Multi-agent architecture (Chunk 2)

### Methods
- Role conditioning: Agents assigned researcher personas (Chunk 2)
- 3-tier architecture: Generation → Evaluation → Refinement (Chunk 3)

### Key Findings
- Finding 1 (Chunk 3): "Role conditioning improved credibility scores by 16%"
- Finding 2 (Chunk 4): Temperature=0 required for reproducible outputs

## Chunk Navigation

### Chunk 1: Introduction and Background
- **Summary**: Introduces thematic analysis challenges and motivation for automation. Reviews prior work on LLM-based qualitative analysis.
- **Key concepts**: [thematic analysis, Braun & Clarke, automation challenges]
- **Load when**: "User asks about TA background" / "Query mentions prior work"

### Chunk 2: System Architecture
- **Summary**: Describes the 3-tier multi-agent architecture with role-conditioned coders.
- **Key concepts**: [multi-agent, role conditioning, generation tier]
- **Load when**: "User asks about architecture" / "Query mentions agent design"

[... continue for all chunks]
```

---

**Version**: 1.0 (2025-12-19)
