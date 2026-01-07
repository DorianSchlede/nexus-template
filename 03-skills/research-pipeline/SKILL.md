---
name: research-pipeline
description: "Triggers: research papers, analyze papers, paper synthesis, literature review."
type: skill-chain
version: "2.0"
---

# Research Pipeline

A complete skill-chain for academic paper research, from search to synthesis.

**This is a CONNECT/ROUTER skill** - like `beam-connect`, it routes to specialized skills.

## How It Works

1. **User talks to this skill** (the parent)
2. **This skill routes to the appropriate child** based on intent
3. **User never needs to know the internal structure**

## Quick Start

| What You Want | Say This |
|--------------|----------|
| Start new research project | "create research project on [topic]" |
| Continue existing project | "execute research project [name]" |
| Search for papers | "search papers about [topic]" |
| Analyze downloaded papers | "analyze papers in [project]" |
| Synthesize findings | "synthesize research on [project]" |

## Routing Table

Based on user intent, **load the appropriate child skill**:

| User Intent | Route To |
|-------------|----------|
| "create research project", "new research on [topic]", "start literature review" | `orchestrators/create-research-project/SKILL.md` |
| "analyze research project", "execute research project", "continue research", "run phase 2" | `orchestrators/analyze-research-project/SKILL.md` |
| "synthesize research project", "generate synthesis", "cross-paper synthesis", "run phase 3" | `orchestrators/synthesize-research-project/SKILL.md` |
| "search for papers", "find papers about", "paper search" | `skills/paper-search/SKILL.md` |
| "preprocess pdf", "convert pdf", "pdf to markdown" | `skills/pdf-preprocess/SKILL.md` |
| "analyze paper", "run analysis" | `skills/paper-analyze/SKILL.md` |
| "synthesize papers", "aggregate findings" | `skills/paper-synthesize/SKILL.md` |
| "query papers", "what papers discuss" | `skills/paper-query/SKILL.md` |
| "manage collection", "list papers", "paper status" | `skills/paper-manage/SKILL.md` |

**DO NOT load `shared/paper-analyze-core/` directly** - it's loaded by subagents.

## Chain Documentation

- **Contract**: See `_chain.yaml` for validation contract
- **Documentation**: See `_index.md` for auto-generated docs with Mermaid diagrams

## Skill Inventory

### Orchestrators (User-Facing Entry Points)

| Skill | Phase | Purpose |
|-------|-------|---------|
| [create-research-project](orchestrators/create-research-project/SKILL.md) | 1 | Planning & Acquisition - Define research question, search, select, download |
| [analyze-research-project](orchestrators/analyze-research-project/SKILL.md) | 2 | Analysis - Preprocess, analyze papers, validate |
| [synthesize-research-project](orchestrators/synthesize-research-project/SKILL.md) | 3 | Synthesis - Cross-paper synthesis with full citations |

### Sub-Skills (Called by Orchestrators)

| Skill | Purpose | Called By |
|-------|---------|-----------|
| [paper-search](skills/paper-search/SKILL.md) | Search 9 academic APIs | Phase 1 |
| [pdf-preprocess](skills/pdf-preprocess/SKILL.md) | Convert PDF to markdown chunks | Phase 1 |
| [paper-analyze](skills/paper-analyze/SKILL.md) | Spawn subagents for analysis | Phase 2 |
| [paper-synthesize](skills/paper-synthesize/SKILL.md) | Field-level synthesis helpers | Phase 3 |
| [paper-query](skills/paper-query/SKILL.md) | Query analyzed papers + routing | Phase 3 |
| [paper-manage](skills/paper-manage/SKILL.md) | Collection management | Ad-hoc |

### Shared Methodologies (DO NOT LOAD DIRECTLY)

| Skill | Purpose |
|-------|---------|
| [paper-analyze-core](shared/paper-analyze-core/SKILL.md) | Analysis methodology - Loaded by subagents spawned by paper-analyze |

## Validation

Validation scripts are in `validation/`:
- `validate_analysis.py` - Validates individual paper analysis logs
- `validate_synthesis.py` - Validates synthesis documents

Run validation:
```bash
python 03-skills/research-pipeline/validation/validate_analysis.py {project_path}
python 03-skills/research-pipeline/validation/validate_synthesis.py {project_path}
```

## Pipeline Flow

```
Phase 1: Planning (create-research-project)
├── Define research question → _briefing.md
├── Search papers → paper-search
├── Review abstracts → _abstract_reviews.md
├── User selection → _selection_log.md
├── Download PDFs → papers/*/*.pdf
├── Preprocess PDFs → pdf-preprocess → papers/*/*_N.md
└── Gate: READY_FOR_ANALYSIS

Phase 2: Analysis (analyze-research-project)
├── Analyze papers → paper-analyze → papers/*/index.md
│   └── Subagents use → paper-analyze-core methodology
├── Validate → validate_analysis.py → _validation_report.md
└── Gate: READY_FOR_SYNTHESIS

Phase 3: Synthesis (synthesize-research-project)
├── Generate routing → paper-query → _synthesis_routing.yaml
├── Batch extraction → subagents → 03-working/_batch_*.md
├── Field aggregation → subagents → 04-outputs/_synthesis_*.md
├── Final report → _synthesis_report.md (FULL MARKDOWN WITH CITATIONS)
├── Validate → validate_synthesis.py → _synthesis_validation.md
└── Gate: COMPLETE
```

## Anti-Hallucination Patterns

This skill-chain includes anti-hallucination measures:
- **3-point evidence**: Start, mid, end text samples from each chunk
- **SHA256 hashes**: Cryptographic verification of chunk content
- **Chunk references**: All claims traced to specific chunk:line
- **Schema validation**: Analysis logs validated against Schema v2.2

---

**Version**: 2.0 (2025-12-27)
**Architecture**: Nested skill-chain
