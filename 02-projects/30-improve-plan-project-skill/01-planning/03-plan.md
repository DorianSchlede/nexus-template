# Improve Plan-Project Skill - Plan

**Last Updated**: 2026-01-07
**Status**: REVISED after stakeholder review

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Full analysis of add-integration and research-pipeline
- `02-resources/revised-architecture.md` - **CURRENT** architecture (supersedes others)
- `02-resources/architecture-decision.md` - Original router pattern decision
- `02-resources/mental-models-analysis.md` - Mental model injection timing

---

## Approach: MANDATORY Router + Template-First

**Decision**: plan-project is the ONLY way to create projects. Templates define types.

```
plan-project (MANDATORY ROUTER)
    │
    ├── Step 1: Type detection
    │   └── Match keywords against templates/types/*/_type.yaml
    │
    ├── Step 2: Mental models (ALWAYS, scaled by type)
    │   └── Quick types: First Principles + Success Criteria
    │   └── Complex types: Full suite with type-specific focus
    │
    ├── Step 3: Create project structure
    │   └── init_project.py --type X
    │   └── Populate plan.md + steps.md from type templates
    │
    ├── Step 4: Type-specific discovery
    │   ├── IF has skill → Route (entry_mode=from_router)
    │   └── ELSE → Use inline discovery.md template
    │
    └── Returns project ready for execution
```

**Why Mandatory Router?**
1. **Consistency** - Mental models ALWAYS applied
2. **Extensibility** - Add type = add folder (no code changes)
3. **Single entry point** - Users learn one command
4. **This is the product core** - Different tasks need different planning

---

## Key Decisions (REVISED)

| Decision | Choice | Why |
|----------|--------|-----|
| Router | **MANDATORY** | No direct skill invocation for project creation |
| Template structure | **types/{type}/ folder** | Self-contained, auto-discoverable |
| Type detection | **From _type.yaml keywords** | Declarative, no code changes to add types |
| Mental models | **Per-type in _type.yaml** | Different types need different depth |
| Backwards compat | **NO** | Clean break, deprecate direct invocation |
| Naming | **Keep "Project"** | Distinct enough from Claude/ChatGPT projects |

---

## Template-First Directory Structure

```
plan-project/
├── SKILL.md                      # Simplified router logic
├── scripts/
│   └── init_project.py           # Enhanced with type support
│
├── templates/
│   └── types/                    # ONE FOLDER PER TYPE
│       ├── build/
│       │   ├── _type.yaml        # Type metadata
│       │   ├── plan.md
│       │   ├── steps.md
│       │   └── discovery.md
│       ├── integration/          # Routes to add-integration
│       ├── research/             # Routes to create-research-project
│       ├── strategy/
│       ├── content/
│       ├── process/
│       └── generic/
│
└── references/
    ├── type-detection.md         # Auto-generated from _type.yaml files
    └── routing-logic.md
```

---

## Dependencies & Links

**Files to Modify**:
- `00-system/skills/projects/plan-project/SKILL.md` - Simplify to reference templates
- `00-system/skills/system/add-integration/SKILL.md` - Add entry_mode handling
- `03-skills/research-pipeline/orchestrators/create-research-project/SKILL.md` - Add entry_mode

**Files to Create**:
- `plan-project/templates/types/build/_type.yaml` + templates
- `plan-project/templates/types/integration/_type.yaml` + templates
- `plan-project/templates/types/research/_type.yaml` + templates
- `plan-project/templates/types/strategy/_type.yaml` + templates
- `plan-project/templates/types/content/_type.yaml` + templates
- `plan-project/templates/types/process/_type.yaml` + templates
- `plan-project/templates/types/generic/_type.yaml` + templates
- `plan-project/references/routing-logic.md`

**External Systems**:
- WebSearch (integration API discovery)
- paper-search skill (research paper discovery)

---

## Implementation Phases

### Phase 1: Create Template Structure (~1 hr)
- Create `templates/types/` directory structure
- Write _type.yaml for each type
- Write plan.md, steps.md, discovery.md for each type

### Phase 2: Update plan-project SKILL.md (~30 min)
- Simplify to reference templates
- Add type detection from _type.yaml keywords
- Add routing logic

### Phase 3: Update Specialized Skills (~30 min)
- Add entry_mode to add-integration
- Add entry_mode to create-research-project
- Add deprecation notice for direct invocation

### Phase 4: Testing (~30 min)
- Test router → integration flow
- Test router → research flow
- Test all inline types (build, strategy, etc.)

**Total: ~2.5 hours AI time**

---

## Open Questions (RESOLVED)

- [x] Should plan-project auto-detect type? → Yes, from _type.yaml keywords
- [x] Mental model timing? → Before discovery, scaled by type
- [x] Template format? → Markdown with YAML frontmatter
- [x] How to pass mental model outputs to specialized skills? → Via entry_mode contract
- [x] Backwards compatibility? → NO, mandatory router only
- [x] Rename "project"? → NO, keep as is

---

*Execution steps in 04-steps.md*
