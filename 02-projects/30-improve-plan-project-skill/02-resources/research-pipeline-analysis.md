# Research Pipeline Analysis

**Location**: `03-skills/research-pipeline/`

---

## Architecture Overview

A **3-phase skill-chain** with **11 components**:
- 3 orchestrators
- 6 sub-skills
- 1 master router
- 1 shared methodology

```
Phase 1: create-research-project (Planning & Acquisition)
    ├── Steps 0-3: Research Definition (RQ, extraction schema)
    ├── Steps 4-6: Paper Selection (search, review, approve)
    ├── Steps 7-9: Paper Acquisition (download, preprocess, verify)
    └── Steps 10-13: Readiness Gate (analysis kit, extraction guide, orchestrator plan)

Phase 2: analyze-research-project (Analysis)
    ├── Step 0-1: Validate readiness, read pre-calculated allocation
    ├── Step 2: Spawn subagents per paper (max 15 concurrent)
    └── Steps 3-4: Validate analysis logs, mark READY_FOR_SYNTHESIS

Phase 3: synthesize-research-project (7-Level Synthesis)
    ├── L1: Routing Script (build_synthesis_routing.py)
    ├── L2: Allocation Script (calculate_subagent_allocation.py)
    ├── L3: Prompts Script (generate_subagent_prompts.py)
    ├── L4: Extraction Subagents (parallel, max 15)
    ├── L5: Verification Script (verify_subagent_output.py)
    ├── L6: Aggregation Script (aggregate_patterns.py)
    └── L7: Report Subagent → _synthesis_report.md
```

---

## File Structure

```
research-pipeline/
├── SKILL.md                    # Master router (like beam-connect)
├── _chain.yaml                 # Validation contract
├── _index.md                   # Auto-generated docs
├── orchestrators/
│   ├── create-research-project/    # Phase 1 (1073 lines!)
│   │   ├── SKILL.md
│   │   └── references/
│   │       ├── abstract_review.md
│   │       ├── analysis_kit_template.md
│   │       ├── orchestrator_template.md
│   │       └── phase1_planning.md
│   ├── analyze-research-project/   # Phase 2 (757 lines)
│   │   └── SKILL.md
│   └── synthesize-research-project/ # Phase 3 (1154 lines!)
│       └── SKILL.md
├── skills/
│   ├── paper-search/           # Search 9 academic APIs
│   ├── pdf-preprocess/         # PDF → markdown chunks
│   ├── paper-analyze/          # Spawn analysis subagents
│   ├── paper-synthesize/       # Field-level synthesis helpers
│   ├── paper-query/            # Query analyzed papers
│   └── paper-manage/           # Collection management
├── shared/
│   ├── paper-analyze-core/     # Analysis methodology (for subagents)
│   └── contracts/              # Schema validation
├── validation/
│   ├── scripts/                # Level 1-3, 5-6 deterministic scripts
│   └── validate_*.py           # Validation scripts
└── dynamic-subagents/          # Subagent spawning utilities
```

---

## What create-research-project Does (Phase 1)

1. **Step 1**: Create project structure using init_project.py
2. **Step 2**: Define research question → `_briefing.md` with extraction schema
3. **Step 3**: Search papers using paper-search skill (9 APIs)
4. **Step 4-6**: Review abstracts, user selection, approval gate
5. **Step 7**: Download papers (batch with fallback resolution)
6. **Step 8**: Preprocess PDFs to markdown chunks
7. **Step 9**: Acquisition report + user gate
8. **Step 10**: Generate `_analysis_kit.md` (subagent context)
9. **Step 11**: Generate `_extraction_guide.md` (field examples)
10. **Step 12**: Calculate subagent allocation, write to plan.md
11. **Step 13**: Readiness gate → handoff to Phase 2

---

## Key Files Created by Phase 1

| File | Purpose |
|------|---------|
| `_briefing.md` | Research question + extraction schema |
| `_analysis_kit.md` | Consolidated subagent context |
| `_extraction_guide.md` | Field examples + controlled vocabulary |
| `_search_results.md` | API search results |
| `_abstract_reviews.md` | AI assessments |
| `_selection_log.md` | Approved papers + acquisition status |
| `papers/*/*.pdf` | Downloaded papers |
| `papers/*/*_N.md` | Markdown chunks |
| `papers/*/_metadata.json` | Chunk index |

---

## Key Workflow Features to Preserve

1. **Interactive RQ Definition** - AI suggests extraction fields based on research question
2. **9-API Paper Search** - Semantic Scholar, OpenAlex, arXiv, CrossRef, PubMed, CORE, BASE, DOAJ, Unpaywall
3. **Batch Download with Fallback** - Multi-source resolution (arXiv → S2 → Unpaywall → direct)
4. **PDF Preprocessing** - pymupdf4llm, max 1000 lines/chunk
5. **Subagent Allocation Calculation** - Token budget planning
6. **Anti-Hallucination Measures** - 3-point evidence, SHA256 hashes, chunk:line references
7. **7-Level Synthesis** - 5 deterministic scripts + 2 LLM subagent levels

---

## Documentation

- `00-system/documentation/research-algorithm-en.md` - Comprehensive v6.0 docs (651 lines)

---

## Modification for Router Pattern

When called from plan-project:
- **Skip Step 1** (project creation) - already done by plan-project
- **Accept project_path parameter** - where to store files
- **Continue from Step 2** - RQ definition

```yaml
# Entry mode from plan-project
entry_mode: "from_router"
project_path: "02-projects/32-ontologies-research/"
skip_steps: [1]  # Don't create project
mental_models_applied: true
success_criteria:
  - "Analyze 20+ papers on foundational ontologies"
  - "Generate synthesis report with citations"
```

---

## Discover ↔ Plan Interleaving

Research projects have heavy interleaving:
```
Discover: "What papers exist?"
Plan: "What fields should I extract?"
Discover: "Do these papers cover my fields?"
Plan: "Refine extraction schema"
Discover: "Download and preprocess"
Plan: "Calculate subagent allocation"
```

This is why create-research-project stays as ONE skill (Steps 2-13).
Mental models apply BEFORE this dance begins.
