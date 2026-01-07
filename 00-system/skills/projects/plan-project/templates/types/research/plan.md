# {{project_name}} - Plan

**Project Type**: Research
**Status**: Planning

---

## Context

**Load Before Reading**:
- `01-planning/02-discovery.md` - Research question and paper selection
- `02-resources/_briefing.md` - Extraction schema

---

## Approach

*Research follows the 3-phase pipeline.*

```
Phase 1: create-research-project (Planning & Acquisition)
    └── Define RQ → Search → Select → Download → Preprocess

Phase 2: analyze-research-project (Analysis)
    └── Spawn subagents → Analyze papers → Validate

Phase 3: synthesize-research-project (Synthesis)
    └── Aggregate patterns → Generate report
```

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Pipeline | 3-phase | Separation of concerns |
| Analysis | Subagent per paper | Parallel processing |
| Synthesis | 7-level | Deterministic + LLM |

---

## Dependencies & Links

**Files to Create**:

| File | Purpose |
|------|---------|
| `_briefing.md` | Research question and schema |
| `_analysis_kit.md` | Subagent context |
| `_extraction_guide.md` | Field examples |
| `papers/*/*.md` | Preprocessed papers |

**External Systems**:
- Semantic Scholar API
- OpenAlex API
- arXiv API
- CrossRef API

---

## Testing Strategy

| Test Type | What to Verify |
|-----------|----------------|
| Search | Papers returned match query |
| Download | PDFs accessible |
| Analysis | Extractions match schema |
| Synthesis | Report covers all papers |

---

*Execution via research pipeline skills*
