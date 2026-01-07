# Improve Plan-Project Skill - Plan

**Last Updated**: 2026-01-07
**Status**: REVISED v2.4 - Simplified Skill Invocation
**Project Type**: Build

---

## Context

**Load Before Reading**:
- `02-resources/architecture-v2.md` - **SINGLE SOURCE OF TRUTH v2.3**
- `02-resources/KIRO-spec.md` - EARS patterns, INCOSE rules, task patterns
- `01-planning/02-discovery.md` - Full analysis of dependencies

**Critical Insight**: Skills are invoked normally - no special contract needed. Steps + TodoWrite enforce sequence.

---

## Requirements (EARS Format)

### Functional Requirements

**REQ-1**: THE plan-project skill SHALL be the mandatory router for all project creation in Nexus.

**REQ-2**: WHEN a user requests project creation, THE router SHALL detect project type by semantic matching against _type.yaml descriptions.

**REQ-3**: WHEN project type is detected, THE router SHALL create project structure using init_project.py with the detected type.

**REQ-4**: WHEN project type requires skill-based discovery (integration, research, skill), THE router SHALL load the skill normally via: `python 00-system/core/nexus-loader.py --skill {skill-name}`.

**REQ-5**: WHEN project type uses inline discovery (build, strategy, content, process, generic), THE router SHALL use the discovery.md template from `templates/types/{type}/`.

**REQ-6**: THE router SHALL execute discovery BEFORE mental models in the workflow sequence.

**REQ-7**: WHEN discovery completes, THE router SHALL load mental models dynamically via `python 00-system/mental-models/scripts/select_mental_models.py`.

**REQ-8**: WHEN mental models identify gaps AND rediscovery_round is less than 2, THE router SHALL trigger re-discovery for identified gaps.

**REQ-9**: THE router SHALL write all discovery findings to `{project_path}/01-planning/02-discovery.md`.

**REQ-10**: THE router SHALL update resume-context.md at every phase transition with current_phase, current_section, and files_to_load.

**REQ-11**: WHEN a skill is loaded for discovery, THE router SHALL set `current_skill` field in resume-context.md.

**REQ-12**: WHEN skill-based discovery completes, THE skill SHALL write findings to `{project_path}/01-planning/02-discovery.md`.

**REQ-13**: IF a user directly invokes add-integration, create-research-project, or create-skill, THEN THE skill SHALL display a deprecation notice and instruct the user to use plan-project instead.

**NOTE**: Hook enforcement for skill tracking is DEFERRED to future project.

### Non-Functional Requirements

**REQ-NF-1**: THE template structure SHALL use `templates/types/{type}/` folders containing exactly 5 files: _type.yaml, overview.md, discovery.md, plan.md, steps.md.

**REQ-NF-2**: THE _type.yaml schema SHALL include: name, description, discovery.skill (optional), discovery.inline (boolean), outputs.discovery_file, mental_models.dynamic.

**REQ-NF-3**: THE router SHALL support exactly 8 project types: build, integration, research, strategy, content, process, skill, generic.

**REQ-NF-4**: FOR build and skill project types, THE discovery.md template SHALL include EARS-formatted requirements and INCOSE quality checklist.

**REQ-NF-5**: FOR build and skill project types, THE plan.md template SHALL include Correctness Properties section with universal quantifications.

### Quality Checklist

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)

---

## Correctness Properties

*Correctness properties are universally quantified statements that must hold for all valid inputs. They enable property-based testing rather than just example-based testing.*

**Property 1: Router Completeness**
For all user requests containing project creation intent, the router either successfully detects a project type from the 8 supported types OR prompts the user to select a type explicitly.
**Validates**: REQ-1, REQ-2

**Property 2: Discovery Sequence Integrity**
For any project creation workflow, the discovery phase completes and writes to 02-discovery.md BEFORE mental models are loaded.
**Validates**: REQ-6, REQ-9

**Property 3: Skill Discovery Output**
For all skill-based discovery invocations, the skill writes discovery findings to the project's 02-discovery.md file.
**Validates**: REQ-12

**Property 4: Resume Context Consistency**
For any phase transition in the workflow, the resume-context.md file reflects the actual current state including current_phase, current_section, and tasks_completed.
**Validates**: REQ-10, REQ-11

**Property 5: Template Structure Invariant**
For all 8 project types, the templates/types/{type}/ folder contains exactly 5 files (_type.yaml, overview.md, discovery.md, plan.md, steps.md) with valid content.
**Validates**: REQ-NF-1, REQ-NF-3

**Property 6: Type Detection Determinism**
For any given user input describing a project, repeated semantic matching against _type.yaml descriptions produces the same project type detection result.
**Validates**: REQ-2

---

## Approach: MANDATORY Router + Template-First + Discovery-First

**Decision**: plan-project is the ONLY way to create projects. Discovery happens BEFORE mental models.

```
plan-project (MANDATORY ROUTER)
    │
    ├── PHASE 1: SETUP [REQ-1, REQ-2, REQ-3]
    │   ├── Type detection (semantic from _type.yaml)
    │   ├── Create project structure (init_project.py)
    │   └── Load templates from types/{type}/
    │
    ├── PHASE 2: DISCOVERY [REQ-4, REQ-5, REQ-9]
    │   ├── Route to skill (integration→add-integration, research→create-research-project, skill→create-skill)
    │   └── OR use inline discovery.md (build, strategy, content, process, generic)
    │
    ├── PHASE 3: MENTAL MODELS [REQ-6, REQ-7]
    │   ├── Load dynamically via select_mental_models.py
    │   ├── Apply to discovery findings
    │   └── Identify gaps for re-discovery
    │
    ├── PHASE 4: RE-DISCOVERY [REQ-8]
    │   └── Fill gaps (max 2 rounds)
    │
    └── PHASE 5: FINALIZATION [REQ-10]
        └── Merge into plan.md, generate steps.md, update resume-context.md
```

---

## Key Decisions (REVISED v2.4 - Simplified)

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| Router | **MANDATORY** | Single entry point, consistent quality | REQ-1 |
| Type detection | **SEMANTIC** | AI matches from description, no keywords | REQ-2 |
| Discovery timing | **BEFORE mental models** | Can't stress-test what you don't understand | REQ-6 |
| Discovery output | **02-discovery.md MANDATORY** | Preserves intelligence across compaction | REQ-9 |
| Skill invocation | **NORMAL** | No special contract, skills run their workflow | REQ-4 |
| Enforcement | **Steps + TodoWrite** | AI forgets; steps don't | REQ-10 |
| Template structure | **types/{type}/ folder** | Self-contained, auto-discoverable | REQ-NF-1 |
| EARS/INCOSE | **Build + Skill types** | Testable requirements for code projects | REQ-NF-4, REQ-NF-5 |
| Hook enforcement | **DEFERRED** | Future project, not this one | - |

---

## Template-First Directory Structure

```
plan-project/
├── SKILL.md                      # Router logic only
├── scripts/
│   └── init_project.py           # Enhanced with type support
│
├── templates/
│   └── types/                    # ONE FOLDER PER TYPE
│       ├── build/
│       │   ├── _type.yaml        # Semantic description, inline discovery
│       │   ├── overview.md       # Overview template
│       │   ├── discovery.md      # EARS requirements template [REQ-NF-4]
│       │   ├── plan.md           # Correctness Properties template [REQ-NF-5]
│       │   └── steps.md          # Checkpoint tasks template
│       ├── integration/          # Routes to add-integration [REQ-4]
│       ├── research/             # Routes to create-research-project [REQ-4]
│       ├── strategy/             # Inline discovery
│       ├── content/              # Inline discovery
│       ├── process/              # Inline discovery
│       ├── skill/                # Routes to create-skill [REQ-4]
│       └── generic/              # Minimal inline discovery
│
└── references/
    ├── routing-logic.md          # Router decision tree
    ├── type-detection.md         # Semantic matching guide
    ├── ears-patterns.md          # EARS templates [REQ-NF-4]
    └── incose-rules.md           # Quality rules [REQ-NF-4]
```

---

## Dependencies & Links

**Files to Modify** (8 files):
| File | Changes | Validates |
|------|---------|-----------|
| `plan-project/SKILL.md` | Rewrite to router pattern | REQ-1, REQ-2, REQ-6 |
| `plan-project/scripts/init_project.py` | Add skill type, schema v2.0 | REQ-3 |
| `plan-project/references/workflows.md` | Rewrite for template flow | REQ-6 |
| `plan-project/references/project-types.md` | Add skill type | REQ-NF-3 |
| `add-integration/SKILL.md` | Add entry_mode check | REQ-12, REQ-15 |
| `create-research-project/SKILL.md` | Add entry_mode check | REQ-12, REQ-15 |
| `create-skill/SKILL.md` | Add entry_mode check | REQ-12, REQ-15 |
| `.claude/hooks/session_start.py` | Add sub_skill routing | REQ-13 |

**Files to Create** (45 files):
- 40 templates: 8 types × 5 files (_type.yaml, overview.md, discovery.md, plan.md, steps.md)
- 5 references: routing-logic.md, entry-mode-contract.md, ears-patterns.md, incose-rules.md, type-detection.md

**External Systems**:
- WebSearch (integration API discovery)
- paper-search skill (research paper discovery)
- create-skill skill (skill scaffolding)
- mental-models skill (dynamic model loading)

---

## Sub-Skill Routing Table

| Type | Discovery | Skill | Load Command | Validates |
|------|-----------|-------|--------------|-----------|
| build | Inline | - | - | REQ-5 |
| integration | Skill | add-integration | `python 00-system/core/nexus-loader.py --skill add-integration` | REQ-4 |
| research | Skill | create-research-project | `python 00-system/core/nexus-loader.py --skill create-research-project` | REQ-4 |
| strategy | Inline | - | - | REQ-5 |
| content | Inline | - | - | REQ-5 |
| process | Inline | - | - | REQ-5 |
| skill | Skill | create-skill | `python 00-system/core/nexus-loader.py --skill create-skill` | REQ-4 |
| generic | Inline | - | - | REQ-5 |

---

## Testing Strategy

### Property-Based Tests

Each correctness property maps to a property-based test:

| Property | Test Strategy | Library |
|----------|---------------|---------|
| P1: Router Completeness | Fuzz test with varied user inputs, verify type detection | hypothesis (Python) |
| P2: Discovery Sequence | Verify 02-discovery.md timestamp < mental model load time | - |
| P3: Sub-Skill Contract | Mock sub-skill, verify entry_mode and project_path passed | pytest |
| P4: Resume Context | State machine verification across phase transitions | - |
| P5: Template Structure | File existence and schema validation | pytest |
| P6: Type Detection | Determinism test with same input repeated | hypothesis |

### Unit Tests

| Component | Test Cases |
|-----------|------------|
| Type detection | 8 types × 3 synonyms each |
| _type.yaml parsing | Valid/invalid schema |
| Entry mode handling | from_router vs direct invocation |
| Resume context updates | Each phase transition |

---

## Open Questions (ALL RESOLVED)

| Question | Resolution | Validates |
|----------|------------|-----------|
| Router mandatory? | YES - single entry point | REQ-1 |
| Type detection method? | Semantic from _type.yaml description | REQ-2 |
| Discovery timing? | BEFORE mental models | REQ-6 |
| Sub-skill contract? | entry_mode + project_path | REQ-11, REQ-12 |
| EARS/INCOSE scope? | Build + Skill types only | REQ-NF-4, REQ-NF-5 |

---

*Execution steps in 04-steps.md*
