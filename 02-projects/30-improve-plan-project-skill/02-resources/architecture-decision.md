# Architecture Decision: plan-project as Router

**Decision Date**: 2026-01-07
**Status**: APPROVED

---

## Decision

**Option 3: plan-project routes TO specialized skills, adding mental models BEFORE**

```
plan-project (ROUTER + SHARED PLANNING)
    │
    ├── Step 1: Type detection (from user input or ask)
    ├── Step 2: Mental models + success criteria (ALWAYS RUNS)
    ├── Step 3: Create project structure (init_project.py --type X)
    ├── Step 4: Route to type-specific skill for DISCOVERY+PLANNING
    │   ├── "integration" → Load add-integration (Steps 1-6, skip project creation)
    │   ├── "research" → Load create-research-project (Steps 2-13, skip project creation)
    │   └── other types → Continue inline with templates
    └── Returns project ready for execution
```

---

## Why This Architecture

### First Principles
1. **Natural language routing already works** - not solving for skill discovery
2. **Clean separation of concerns** - the real problem
3. **Reduce duplication** - mental models should apply everywhere
4. **Don't break existing skills** - they work well

### Lifecycle Insight
```
DISCOVER ↔ PLAN → EXECUTE → COMPLETE
    └──────┘
    (interleaved)
```

Discovery and Planning are **interleaved**, not sequential. They go back and forth:
- Research: Define RQ → Search → Refine schema → Download → Calculate allocation
- Integration: Search API → Select endpoints → Configure → Generate config

### Mental Model Injection Point
Mental models run **BEFORE** type-specific discovery, because:
1. They help frame the problem correctly
2. Success criteria should be defined upfront
3. Devil's advocate catches bad assumptions early

---

## Implementation Strategy

### What plan-project Does (Enhanced)
1. **Type Detection**: Parse user input OR ask
2. **Mental Models**: Always apply (Socratic, Devil's Advocate, First Principles)
3. **Project Creation**: Run `init_project.py --type {type}`
4. **Route to Discovery**: Load specialized skill with `skip_project_creation=true`
5. **Return**: Project ready for execution

### What Specialized Skills Do (Unchanged)
- **add-integration**: Steps 1-6 (API discovery) + Step 7 (scaffold)
- **create-research-project**: Steps 2-13 (RQ, search, download, prep)
- Both skip Step 1 (project creation) when called from plan-project

### Template System for Other Types
For non-specialized types (build, strategy, content, process, generic):
- Use `templates/template-{type}.md` for plan.md sections
- Use predefined step lists in `templates/steps-{type}.md`
- Mental models still apply

---

## Key Patterns to Implement

### 1. Type-Specific Templates
```
plan-project/
├── templates/
│   ├── template-build.md        # Technical architecture sections
│   ├── template-research.md     # Research methodology sections
│   ├── template-strategy.md     # Decision framework sections
│   ├── template-content.md      # Creative brief sections
│   ├── template-process.md      # Current state analysis sections
│   ├── template-integration.md  # API configuration sections
│   └── template-generic.md      # Minimal sections
├── templates/
│   ├── steps-build.md           # Predefined build phases
│   ├── steps-research.md        # Research phases (points to skill)
│   ├── steps-integration.md     # Integration phases (points to skill)
│   └── steps-generic.md         # Generic phases
```

### 2. Smart Routing in SKILL.md
```markdown
## Step 4: Type-Specific Discovery

Based on project type, load appropriate workflow:

| Type | Action |
|------|--------|
| integration | Load `add-integration` skill, pass `project_path`, skip Step 1 |
| research | Load `create-research-project` skill, pass `project_path`, skip Step 1 |
| build | Continue inline, use `template-build.md` |
| strategy | Continue inline, use `template-strategy.md` |
| content | Continue inline, use `template-content.md` |
| process | Continue inline, use `template-process.md` |
| generic | Continue inline, minimal template |
```

### 3. Skill Interface Contract
Specialized skills need to accept:
```yaml
# When called from plan-project
entry_mode: "from_router"  # vs "direct"
project_path: "02-projects/30-xxx/"
skip_steps: [1]  # Don't create project, already done
mental_models_applied: true
```

---

## Files to Modify

| File | Changes |
|------|---------|
| `plan-project/SKILL.md` | Add routing logic, mental model enforcement |
| `plan-project/references/project-types.md` | Add Integration + Research types |
| `add-integration/SKILL.md` | Add `entry_mode` handling, skip Step 1 |
| `create-research-project/SKILL.md` | Add `entry_mode` handling, skip Step 1 |

## Files to Create

| File | Purpose |
|------|---------|
| `plan-project/templates/template-integration.md` | Integration plan sections |
| `plan-project/templates/template-research.md` | Research plan sections |
| `plan-project/templates/steps-integration.md` | Integration phases |
| `plan-project/templates/steps-research.md` | Research phases |
| `plan-project/references/routing-logic.md` | How routing works |

---

## Benefits

1. **Single entry point** - `plan project` works for everything
2. **Mental models always applied** - consistent quality
3. **Specialized skills preserved** - no refactoring needed
4. **Clean separation** - router vs discovery vs execution
5. **Extensible** - add new types by adding templates

## Risks Mitigated

| Risk | Mitigation |
|------|------------|
| Breaking existing users | Natural language still triggers specialized skills directly |
| Complex routing logic | Simple type → skill mapping |
| Skill bloat | Templates stay in files, not inline |
| Lost functionality | Specialized skills unchanged |
