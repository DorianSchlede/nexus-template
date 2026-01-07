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

### Open Questions (ALL RESOLVED in v2.1)
- [x] Should scaffold_integration.py move to plan-project? → **NO, keep in add-integration, call via reference**
- [x] How to handle type-specific plan.md structure? → **Type-specific templates in types/{type}/ folders**
- [x] Should plan-project auto-detect type from user input? → **YES, semantic matching from _type.yaml descriptions**
- [x] Should type selection happen before or after mental model selection? → **BEFORE, but mental models run AFTER discovery**
- [x] How to preserve context across compaction? → **02-discovery.md MANDATORY + resume-context.md dynamic updates**
- [x] How to prevent AI forgetting to return from sub-skills? → **Steps are ENFORCEMENT MECHANISM**

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

## Kiro Spec-Driven Development Patterns (NEW DISCOVERY)

**Source**: Amazon's Kiro IDE - battle-tested at scale

### What Kiro Does (3 Phases)

| Phase | Artifact | Key Features |
|-------|----------|--------------|
| **Requirements** | `requirements.md` | EARS patterns, INCOSE quality rules, iterate until approved |
| **Design** | `design.md` | Research → Design → Correctness Properties → Testing Strategy |
| **Tasks** | `tasks.md` | Coding tasks only, property tests as sub-tasks, checkpoints |

### EARS Patterns (6 Requirement Templates)

Every requirement follows exactly ONE pattern:

1. **Ubiquitous**: THE `<system>` SHALL `<response>`
2. **Event-driven**: WHEN `<trigger>`, THE `<system>` SHALL `<response>`
3. **State-driven**: WHILE `<condition>`, THE `<system>` SHALL `<response>`
4. **Unwanted**: IF `<condition>`, THEN THE `<system>` SHALL `<response>`
5. **Optional**: WHERE `<option>`, THE `<system>` SHALL `<response>`
6. **Complex**: [WHERE] [WHILE] [WHEN/IF] THE `<system>` SHALL `<response>`

### INCOSE Quality Rules

**Clarity**: Active voice, no vague terms, no pronouns, consistent terminology
**Testability**: Explicit conditions, measurable criteria, one thought per requirement
**Completeness**: No escape clauses, no absolutes, solution-free

### Correctness Properties

Universal quantifications for property-based testing:
- Each property has "for all" or "for any" statement
- Each property references requirements it validates
- Enables property-based testing (not just example-based)

### Task Patterns

**Checkpoints**: `- [ ] **CHECKPOINT**: Verify X works, ask user if questions arise`
**Optional marking**: `- [ ]* Write unit tests (optional)` - `*` postfix
**No standalone test phases**: Tests are sub-tasks of implementation
**Reference format**: `- [ ] Implement X **[REQ-2]**`

### How We Adopt This

| Pattern | Adoption | Types |
|---------|----------|-------|
| EARS requirements | Full | Build, Skill |
| INCOSE quality rules | Full | Build, Skill |
| Correctness properties | Full | Build, Skill |
| Checkpoint tasks | Full | ALL types |
| Optional `*` marking | Full | ALL types |
| Task references | Full | ALL types |

**Rationale**: Build/Skill produce testable code → need formal requirements. Other types don't produce code → checkpoints and optional marking still useful.

---

## Create-Skill Skill Analysis (COMPLETE)

### Location
`00-system/skills/skill-dev/create-skill/`

### What It Does
1. **Pre-flight check**: Suggests 'learn skills' tutorial for first-time users
2. **Anti-pattern detection**: Identifies when repetitive items should be skills
3. **Skill creation guidance**: Provides SKILL.md format, bundled resources structure
4. **Scripts for validation**: init_skill.py, quick_validate.py, package_skill.py

### Key Files
```
create-skill/
├── SKILL.md                    # Skill creation guidance
├── scripts/
│   ├── init_skill.py           # Scaffold new skill structure
│   ├── package_skill.py        # Package for distribution
│   ├── quick_validate.py       # Fast validation
│   └── validate_for_notion.py  # Notion export validation
└── references/
    ├── description-guide.md    # How to write descriptions
    ├── error-scenarios.md      # Common errors
    ├── naming-guidelines.md    # Naming conventions
    ├── output-patterns.md      # Output format patterns
    ├── skill-format-specification.md  # Full format spec
    ├── splitting-large-skills.md      # When to split skills
    └── workflows.md            # Workflow patterns
```

### Key Workflow Features to Preserve
1. **Skill-worthiness criteria** - 3-criteria framework for when to create skills
2. **Anatomy structure** - SKILL.md + scripts/ + references/ + assets/
3. **Degrees of freedom** - High/Medium/Low freedom based on task fragility
4. **Conciseness principle** - Only add what Claude doesn't already know

### Integration with Router
- Route type "skill" → `create-skill` skill
- Skill load command: `python 00-system/core/nexus-loader.py --skill create-skill`
- Entry mode: `from_router`

---

## COMPREHENSIVE DEPENDENCY ANALYSIS

### Current State vs Architecture v2.3 (Simplified)

| Component | Current State | Architecture v2.3 Target | Gap |
|-----------|---------------|--------------------------|-----|
| **plan-project/SKILL.md** | 370 lines, old workflow | Router-only pattern | MAJOR rewrite |
| **init_project.py** | 6 types, schema v1.0 | 8 types, schema v2.0 | Add skill type |
| **Templates folder** | `scripts/templates/` (6 files) | `templates/types/` (8×5 files) | NEW structure |
| **resume-context.md schema** | v1.0 | v2.0 (current_skill field) | ADD field |
| **Type detection** | Keyword-based (--type arg) | Semantic (_type.yaml) | NEW approach |
| **Mental models** | Hardcoded in workflows.md | Dynamic via script | EXISTS |
| **add-integration** | Standalone skill | Normal invocation + deprecation notice | Minor update |
| **create-research-project** | Standalone skill | Normal invocation + deprecation notice | Minor update |
| **create-skill** | Standalone skill | Normal invocation + deprecation notice | Minor update |
| **SessionStart hook** | No skill tracking | DEFERRED to future project | No change now |

---

## FILES TO MODIFY (Complete List - v2.3 Simplified)

### Core Skill Files (4 files)
| File | Changes |
|------|---------|
| `00-system/skills/projects/plan-project/SKILL.md` | **REWRITE** - Router logic only |
| `00-system/skills/projects/plan-project/scripts/init_project.py` | ADD: --type skill, schema v2.0 |
| `00-system/skills/projects/plan-project/references/workflows.md` | **REWRITE** - Template flow |
| `00-system/skills/projects/plan-project/references/project-types.md` | ADD: skill type |

### Skills to Update (3 files) - DEPRECATION NOTICE ONLY
| File | Changes |
|------|---------|
| `00-system/skills/system/add-integration/SKILL.md` | ADD: deprecation notice, recommend plan-project |
| `03-skills/research-pipeline/orchestrators/create-research-project/SKILL.md` | ADD: deprecation notice |
| `00-system/skills/skill-dev/create-skill/SKILL.md` | ADD: deprecation notice |

**NOTE**: No entry_mode contract needed (v2.3 simplification). Skills run normally.

---

## FILES TO CREATE (Complete List)

### Template Structure (40 files: 8 types × 5 files)

```
plan-project/templates/types/
├── build/
│   ├── _type.yaml        # Semantic description, inline discovery
│   ├── overview.md       # Overview template
│   ├── discovery.md      # EARS requirements (Build type)
│   ├── plan.md           # Correctness Properties section
│   └── steps.md          # Checkpoint tasks
├── integration/
│   ├── _type.yaml        # Routes to add-integration skill
│   ├── overview.md
│   ├── discovery.md      # API discovery output format
│   ├── plan.md
│   └── steps.md
├── research/
│   ├── _type.yaml        # Routes to create-research-project skill
│   ├── overview.md
│   ├── discovery.md      # RQ + extraction schema output
│   ├── plan.md
│   └── steps.md
├── strategy/
│   ├── _type.yaml        # Inline discovery, decision frameworks
│   ├── overview.md
│   ├── discovery.md
│   ├── plan.md
│   └── steps.md
├── content/
│   ├── _type.yaml        # Inline discovery, creative brief
│   ├── overview.md
│   ├── discovery.md
│   ├── plan.md
│   └── steps.md
├── process/
│   ├── _type.yaml        # Inline discovery, workflow optimization
│   ├── overview.md
│   ├── discovery.md
│   ├── plan.md
│   └── steps.md
├── skill/
│   ├── _type.yaml        # Routes to create-skill skill
│   ├── overview.md
│   ├── discovery.md      # EARS requirements (Skill type)
│   ├── plan.md           # Correctness Properties section
│   └── steps.md
└── generic/
    ├── _type.yaml        # Minimal inline discovery
    ├── overview.md
    ├── discovery.md
    ├── plan.md
    └── steps.md
```

### Reference Files (4 files - v2.3 Simplified)
| File | Purpose |
|------|---------|
| `references/routing-logic.md` | How router works, skill invocation |
| `references/type-detection.md` | Semantic matching guide |
| `references/ears-patterns.md` | EARS requirement templates |
| `references/incose-rules.md` | INCOSE quality rules |

**NOTE**: No entry-mode-contract.md needed (v2.3 simplification).

---

## EXTERNAL SYSTEM DEPENDENCIES

| System | Used By | Notes |
|--------|---------|-------|
| **WebSearch** | Integration discovery | API doc lookup |
| **paper-search skill** | Research discovery | 9 academic APIs |
| **create-skill skill** | Skill discovery | Skill scaffolding |
| **mental-models skill** | ALL types | 59 models, 12 categories |
| **select_mental_models.py** | Dynamic loading | Already exists |
| **nexus-loader.py** | Skill loading | Already supports --skill |

**NOTE**: SessionStart hook changes DEFERRED to future project (v2.3).

---

## SKILL ROUTING TABLE (v2.3 - Simplified)

Skills are invoked normally - no special contract needed.

| Type | Discovery Method | Skill to Load | Notes |
|------|------------------|---------------|-------|
| **build** | Inline | - | Use discovery.md template |
| **integration** | Skill | add-integration | Runs normal workflow |
| **research** | Skill | create-research-project | Runs normal workflow |
| **strategy** | Inline | - | Use discovery.md template |
| **content** | Inline | - | Use discovery.md template |
| **process** | Inline | - | Use discovery.md template |
| **skill** | Skill | create-skill | Runs normal workflow |
| **generic** | Inline | - | Use discovery.md template |

**Load Command**: `python 00-system/core/nexus-loader.py --skill {skill-name}`

---

## SIMPLIFIED SKILL INVOCATION (v2.3)

**Key Insight**: No special "sub-skill" contract needed. Just invoke skills normally.

### How It Works:

```
Router → update resume-context.md (skill: add-integration)
       → load skill via nexus-loader.py
       → skill runs its normal workflow
       → skill writes to project's 02-discovery.md
       → skill completes, clears skill field in resume
       → router continues with mental models
```

### What Router Does:
1. Detect type
2. Create project structure
3. Update resume-context.md: `current_skill: add-integration`
4. Load skill: `python nexus-loader.py --skill add-integration`
5. Skill runs normally, writes findings to `{project}/01-planning/02-discovery.md`
6. Skill completes, updates resume-context.md: `current_skill: ""`
7. Router continues with mental models phase

### What Skills Do (unchanged):
- Run their normal workflow
- Write outputs to the active project folder (from resume-context.md)
- No entry_mode checking needed
- No structured discovery_output return needed

### Enforcement:
- **TodoWrite** tracks progress (AI updates resume-context.md)
- **Steps** enforce sequence (embedded in 04-steps.md)
- **Hook enforcement** deferred to future project

---

## UPDATED RISKS & MITIGATIONS (v2.3)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Breaking existing projects | Medium | High | Migration script for resume-context.md |
| AI forgetting to return to router | Medium | Medium | Steps enforce sequence, TodoWrite tracks |
| Template explosion (45 files) | Medium | Medium | Use template inheritance where possible |
| Type detection ambiguity | Low | Medium | Clear semantic descriptions in _type.yaml |
| Skills not writing to project folder | Low | Medium | Document convention in SKILL.md |

---

## RESOLVED OPEN QUESTIONS (v2.3)

| Question | Resolution |
|----------|------------|
| Does create-skill skill exist? | **YES** - at `00-system/skills/skill-dev/create-skill/` |
| Where do type-specific workflows live? | `templates/types/{type}/` folders |
| How do deprecated skills redirect? | Auto-invoke plan-project with deprecation notice |
| What happens to Phase 2/3 of research? | Unchanged - only Phase 1 merges |
| Should type detection use keywords? | **NO** - semantic matching from description |
| How to handle mental model timing? | AFTER discovery, BEFORE finalization |
| How to prevent AI forgetting returns? | Steps + TodoWrite enforce sequence |
| Do we need entry_mode contract? | **NO** - just invoke skills normally (v2.3 simplification) |
| Do we need hook enforcement? | **DEFERRED** - future project, not this one |

---

## DETAILED GAP ANALYSIS: Current SKILL.md vs Architecture v2.2

### Section-by-Section Comparison

| Current SKILL.md Section | Architecture v2.2 Target | Gap Type | Action Required |
|--------------------------|-------------------------|----------|-----------------|
| **Onboarding Awareness** (lines 6-40) | Keep | PRESERVE | No change needed |
| **Critical Execution Requirements** (43-82) | Router pattern | REWRITE | Replace with router sequence |
| **Two Modes** (102-114) | Keep but simplify | MODIFY | Mode detection stays, workflow refs change |
| **Mode Detection Logic** (118-135) | Keep | PRESERVE | No change needed |
| **Quick Start / One True Workflow** (138-171) | Router pattern | REWRITE | Replace with template-based flow |
| **Mental Models Selection** (175-242) | Keep but move timing | MODIFY | Run AFTER discovery, not during plan.md |
| **Dependency Research** (245-268) | Integrated into discovery | ABSORB | Move to discovery.md templates |
| **Example Interaction Flow** (272-293) | Update for new flow | MODIFY | New example with router pattern |
| **Resources** (296-310) | Expand with templates | MODIFY | Add templates/types/ structure |
| **Error Handling** (314-337) | Keep | PRESERVE | No change needed |
| **Why This Design** (340-367) | Keep rationale | PRESERVE | No change needed |

### Critical Structural Changes

| Current Structure | v2.2 Structure | Migration Path |
|-------------------|----------------|----------------|
| Single workflow in SKILL.md | Router + template references | Split into router logic + templates |
| `scripts/templates/` (6 files) | `templates/types/` (40 files) | Create new structure, deprecate old |
| Mental models in plan.md step | Mental models after discovery | Resequence workflow |
| No type-specific discovery | discovery.md per type | Create 8 discovery templates |
| No sub-skill routing | _type.yaml with skill reference | Add routing table |

### Lines to KEEP (Copy Forward)

| Line Range | Content | Reason |
|------------|---------|--------|
| 1-4 | YAML frontmatter | Identity |
| 6-40 | Onboarding awareness | UX quality |
| 118-135 | Mode detection logic | Still valid |
| 314-337 | Error handling | Still valid |
| 340-367 | Why this design | Philosophy |

### Lines to REWRITE

| Line Range | Current Content | New Content |
|------------|-----------------|-------------|
| 43-82 | Old critical requirements | Router pattern requirements |
| 138-171 | One true workflow | Template-based workflow |
| 175-242 | Mental models (during plan) | Mental models (after discovery) |
| 272-293 | Old example flow | Router pattern example |
| 296-310 | Resources section | Expanded with templates |

### New Sections to ADD

| Section | Purpose | Content Source |
|---------|---------|----------------|
| **Router Logic** | Core decision tree | architecture-v2.md §Full Flow |
| **Type Detection** | Semantic matching | architecture-v2.md §_type.yaml |
| **Sub-Skill Loading** | Bash commands | architecture-v2.md §Sub-Skill Routing |
| **Discovery Sequence** | BEFORE mental models | architecture-v2.md §The Sequence |
| **Template References** | Type folder structure | architecture-v2.md §Directory Structure |
| **Entry Mode Contract** | For sub-skills | discovery.md §Entry Mode Contract |

---

## KIRO/EARS/INCOSE RECONCILIATION

### Already Integrated in architecture-v2.md v2.2

| Pattern | Location in architecture-v2.md | Status |
|---------|--------------------------------|--------|
| EARS Patterns | §EARS Requirements Patterns | ✅ Complete |
| INCOSE Quality Rules | §EARS Requirements Patterns | ✅ Complete |
| Correctness Properties | §Correctness Properties | ✅ Complete |
| Checkpoint Tasks | §Task Patterns | ✅ Complete |
| Optional `*` marking | §Task Patterns | ✅ Complete |
| Task References | §Task Patterns | ✅ Complete |

### Application Matrix

| Project Type | EARS Requirements | Correctness Properties | Checkpoints | Optional Tasks |
|--------------|-------------------|------------------------|-------------|----------------|
| **build** | YES (mandatory) | YES (mandatory) | YES | YES |
| **skill** | YES (mandatory) | YES (mandatory) | YES | YES |
| **integration** | NO (API discovery only) | NO | YES | YES |
| **research** | NO (RQ/schema only) | NO | YES | YES |
| **strategy** | NO (decisions only) | NO | YES | YES |
| **content** | NO (creative brief) | NO | YES | YES |
| **process** | NO (workflow only) | NO | YES | YES |
| **generic** | NO | NO | YES | YES |

### Template Implications

For **build** and **skill** types, the discovery.md template MUST include:
```markdown
## Requirements (EARS Format)

### Functional Requirements
**REQ-1**: [EARS pattern]
**REQ-2**: [EARS pattern]

### Non-Functional Requirements
**REQ-NF-1**: [EARS pattern]

### Quality Checklist
- [ ] All requirements use EARS patterns
- [ ] No vague terms
- [ ] Each requirement independently testable
```

For **build** and **skill** types, the plan.md template MUST include:
```markdown
## Correctness Properties

**Property 1**: [Universal quantification]
**Validates**: REQ-X, REQ-Y

**Property 2**: [Universal quantification]
**Validates**: REQ-Z
```

---

## IMPLEMENTATION ORDER (v2.3 Simplified)

Based on dependency analysis, implement in this order:

### Phase 2A: Foundation (No Dependencies)
1. Create `templates/types/` directory structure
2. Create _type.yaml for all 8 types
3. Create generic templates (overview, discovery, plan, steps)

### Phase 2B: Type-Specific Templates (Depends on 2A)
4. Create build type templates (with EARS/INCOSE)
5. Create skill type templates (with EARS/INCOSE)
6. Create inline discovery templates (strategy, content, process, generic)
7. Create skill-invocation templates (integration, research)

### Phase 2C: References (Depends on 2A)
8. Create routing-logic.md
9. Create ears-patterns.md and incose-rules.md
10. Create type-detection.md

### Phase 3: SKILL.md Rewrite (Depends on 2A, 2B, 2C)
11. Rewrite SKILL.md with router pattern
12. Update workflows.md and project-types.md

### Phase 4: Deprecation Notices (Simple)
13. Add deprecation notice to add-integration
14. Add deprecation notice to create-research-project
15. Add deprecation notice to create-skill

### Phase 5: Testing (Depends on Phase 4)
16. Test all 8 types through router
17. Test skill invocation flow
18. Test resume-context.md updates

**NOTE**: Hook enforcement DEFERRED to future project.

---

*This discovery document is MANDATORY output. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above*
