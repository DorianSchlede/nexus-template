# Discovery

**Time**: 5-15 min max | **Purpose**: Surface dependencies before planning

---

## Context

**Load First**: `01-planning/01-overview.md` - Understand project purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

---

## Add-Integration Skill Analysis (COMPLETE)

### Location
`00-system/skills/system/add-integration/`

### What It Does
1. **Step 1-2**: User names service → Claude does web search for API docs
2. **Step 3-4**: Parse and cache API documentation (endpoints, auth, base URL)
3. **Step 5**: Present endpoint list → User selects which to implement
4. **Step 6**: Create integration project with config JSON
5. **Step 7**: Execute project using `scaffold_integration.py`

### Key Files
```
add-integration/
├── SKILL.md                          # 7-step workflow definition
├── scripts/
│   └── scaffold_integration.py       # Generates entire integration structure
├── templates/
│   ├── master-skill.md.template      # Master skill template
│   ├── connect-skill.md.template     # Connect skill template
│   ├── operation-skill.md.template   # Per-endpoint skill
│   ├── api-client.py.template        # Shared API client
│   ├── config-check.py.template      # Pre-flight validation
│   ├── setup-wizard.py.template      # Interactive setup
│   ├── operation-script.py.template  # Endpoint script
│   └── references/
│       ├── api-reference.md.template
│       ├── authentication.md.template
│       ├── error-handling.md.template
│       └── setup-guide.md.template
└── references/
    ├── integration-architecture.md   # 3-tier pattern docs
    ├── integration-ideas.md          # Use cases/inspiration
    ├── mcp-guide.md                  # MCP setup instructions
    ├── mcp-introduction.md           # MCP conceptual overview
    ├── mcp-setup-guide.md            # Detailed MCP setup
    └── troubleshooting-guide.md      # Error resolution
```

### Integration Config JSON Format
```json
{
  "service_name": "HubSpot",
  "service_slug": "hubspot",
  "base_url": "https://api.hubapi.com",
  "auth_type": "oauth2|api_key|bearer",
  "env_key": "HUBSPOT_API_KEY",
  "api_docs_url": "https://developers.hubspot.com/docs/api",
  "endpoints": [
    {
      "name": "List Contacts",
      "slug": "list-contacts",
      "method": "GET",
      "path": "/crm/v3/objects/contacts",
      "description": "Retrieve all contacts",
      "triggers": ["list contacts", "get contacts"]
    }
  ]
}
```

### Generated Output Structure (3-Tier Architecture)
```
03-skills/{service}/
├── {service}-master/           # Tier 1: Shared resources (NEVER loaded directly)
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── {service}_client.py
│   │   ├── check_{service}_config.py
│   │   └── setup_{service}.py
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
├── {service}-connect/          # Tier 2: User entry point
│   └── SKILL.md
└── {service}-{operation}/      # Tier 3: Per-endpoint skills
    ├── SKILL.md
    └── scripts/
        └── {operation}.py
```

### Key Workflow Features to Preserve
1. **Web Search for API Discovery** - Uses WebSearch to find API docs
2. **Endpoint Selection UI** - User picks which endpoints to implement
3. **Scaffolding Script** - Generates all files from templates
4. **3-Tier Architecture** - Master/Connect/Operation pattern
5. **Config Check Pattern** - `--json` flag for AI-consumable output

---

## Research Pipeline Analysis (COMPLETE)

### Location
`03-skills/research-pipeline/`

### Architecture Overview
A **3-phase skill-chain** with **11 components** (3 orchestrators, 6 skills, 1 master router, 1 shared methodology).

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

### Key Files
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

### What create-research-project Does (Phase 1)
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

### Key Files Created by Phase 1
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

### Key Workflow Features to Preserve
1. **Interactive RQ Definition** - AI suggests extraction fields based on research question
2. **9-API Paper Search** - Semantic Scholar, OpenAlex, arXiv, CrossRef, PubMed, CORE, BASE, DOAJ, Unpaywall
3. **Batch Download with Fallback** - Multi-source resolution (arXiv → S2 → Unpaywall → direct)
4. **PDF Preprocessing** - pymupdf4llm, max 1000 lines/chunk
5. **Subagent Allocation Calculation** - Token budget planning
6. **Anti-Hallucination Measures** - 3-point evidence, SHA256 hashes, chunk:line references
7. **7-Level Synthesis** - 5 deterministic scripts + 2 LLM subagent levels

### Documentation
- `00-system/documentation/research-algorithm-en.md` - Comprehensive v6.0 docs (651 lines)

---

## Dependencies

*Files, systems, APIs this project will touch*

### Files to Modify
| File | Changes Needed |
|------|----------------|
| `00-system/skills/projects/plan-project/SKILL.md` | Add type detection, integration workflow, research workflow |
| `00-system/skills/projects/plan-project/references/project-types.md` | Add Integration + Research type details |
| `00-system/skills/projects/plan-project/references/workflows.md` | Add type-specific discovery workflows |

### Files to Create (Integration)
| File | Purpose |
|------|---------|
| `plan-project/references/integration-workflow.md` | Step-by-step integration discovery |
| `plan-project/templates/integration-config.json.template` | Config JSON template |

### Files to Create (Research)
| File | Purpose |
|------|---------|
| `plan-project/references/research-workflow.md` | Step-by-step research setup |
| `plan-project/templates/research-briefing.md.template` | _briefing.md template |
| `plan-project/templates/research-analysis-kit.md.template` | _analysis_kit.md template |

### Files to Deprecate/Redirect
| File | Action |
|------|--------|
| `00-system/skills/system/add-integration/SKILL.md` | Redirect to `plan-project --type integration` |
| `03-skills/research-pipeline/orchestrators/create-research-project/SKILL.md` | Keep as execute-only, redirect planning to `plan-project --type research` |

### External Systems
- **WebSearch** - For API documentation discovery (integration)
- **paper-search skill** - For academic paper discovery (research)
- **pdf-preprocess skill** - For PDF conversion (research)

---

## Existing Patterns

*Skills, templates, code to reuse*

### Integration Patterns to Reuse
| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| API Discovery via WebSearch | `add-integration/SKILL.md` Step 2-4 | Extract to reference doc |
| Endpoint Selection UI | `add-integration/SKILL.md` Step 5 | Keep as-is |
| 3-Tier Scaffolding | `scaffold_integration.py` | Keep in add-integration, call from plan-project |
| Templates (9 files) | `add-integration/templates/*` | Keep in add-integration |
| Reference docs (6 files) | `add-integration/references/*` | Keep in add-integration |

### Research Patterns to Reuse
| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| RQ Definition + Field Generation | `create-research-project/SKILL.md` Step 2 | Extract to reference doc |
| Abstract Review Criteria | `references/abstract_review.md` | Copy to plan-project |
| Analysis Kit Generation | `create-research-project/SKILL.md` Step 10 | Extract to template |
| Extraction Guide Generation | `create-research-project/SKILL.md` Step 11 | Extract to template |
| Subagent Allocation Calculation | `create-research-project/SKILL.md` Step 12 | Keep in create-research-project |

### Common Patterns (Both Types)
| Pattern | Current Implementation | Unified Approach |
|---------|----------------------|------------------|
| Project Structure Init | `init_project.py` | Add `--type` flag |
| Mental Model Selection | `plan-project/SKILL.md` | Keep, apply to all types |
| User Approval Gates | Both skills | Standardize UI |

---

## Risks & Unknowns

*What could derail? What don't we know?*

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking add-integration users | Medium | High | Keep as redirect skill |
| Breaking create-research-project users | Medium | High | Keep Phase 1 in skill, just add plan-project routing |
| Complex skill becomes unwieldy | Medium | Medium | Modular type-specific references |
| Token budget miscalculation | Low | High | Keep existing calculation code |
| Web search rate limits | Low | Low | Cache results, single search |

### Architectural Decisions Needed

1. **Where do type-specific workflows live?**
   - Option A: Inline in plan-project/SKILL.md (bloat)
   - Option B: Separate reference files (clean) ← PREFERRED

2. **How do deprecated skills redirect?**
   - Option A: Error message + instructions
   - Option B: Auto-invoke plan-project with args ← PREFERRED

3. **What happens to Phase 2/3 of research?**
   - Answer: Unchanged. Only Phase 1 (planning) merges into plan-project.
   - `execute-research-project` → `analyze-research-project` → `synthesize-research-project`

### Open Questions
- [x] Should scaffold_integration.py move to plan-project? → **NO, keep in add-integration, call via reference**
- [x] How to handle type-specific plan.md structure? → **Type-specific reference docs**
- [ ] Should plan-project auto-detect type from user input? (e.g., "integrate Slack" → Integration)
- [ ] Should type selection happen before or after mental model selection?

---

## Key Insight: Plan vs Execute Separation

Both add-integration and create-research-project **mix planning with execution**:
- add-integration: Steps 1-6 = planning, Step 7 = execution
- create-research-project: Steps 1-9 = planning, Steps 10-13 = execution prep

**Proposed Split:**
| Current Skill | Planning (→ plan-project) | Execution (→ stays/new) |
|---------------|---------------------------|------------------------|
| add-integration | Steps 1-6 (API discovery + config) | Step 7 (scaffolding) → keep as `build-integration` |
| create-research-project | Steps 1-9 (RQ, search, download) | Steps 10-13 → keep in skill |

This means plan-project handles **discovery and configuration**, not execution.

---

*Auto-populate 03-plan.md Dependencies section from findings above*
