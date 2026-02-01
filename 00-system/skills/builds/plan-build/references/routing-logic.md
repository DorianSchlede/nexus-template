# Router Logic

**Purpose**: How plan-build routes to type-specific workflows

---

## Type Detection

The router uses **semantic matching** against `_type.yaml` descriptions.

### Detection Flow

```
User: "plan build for X"
    │
    ├── Read all templates/types/*/_type.yaml
    ├── Compare user input against each description
    ├── Select best match OR ask user to choose
    │
    └── Proceed with detected type
```

### No Keyword Triggers

Type detection is semantic, not keyword-based:
- "build slack integration" → Integration (not Build)
- "research competitive landscape" → Research
- "create new automation" → Build or Skill (ask if ambiguous)

---

## Routing Table

| Type | Discovery Method | Skill (if any) |
|------|------------------|----------------|
| build | Inline | - |
| integration | Skill | add-integration |
| research | Skill | create-research-build |
| strategy | Inline | - |
| content | Inline | - |
| process | Inline | - |
| skill | Skill | create-skill |
| generic | Inline | - |

---

## Skill-Based Discovery

For types with `discovery.skill` in _type.yaml:

```bash
# Load skill normally
nexus-load --skill {skill-name}
```

### What Router Does

1. Update `resume-context.md` with `current_skill: {skill-name}`
2. Load skill via nexus-loader
3. Skill runs its normal workflow
4. Skill writes findings to build's `02-discovery.md`
5. Clear `current_skill` when skill completes
6. Router continues with mental models

### What Skills Do

- Run their normal workflow
- Write outputs to active build folder
- No special entry_mode handling needed
- No structured return format needed

---

## Inline Discovery

For types without `discovery.skill`:

1. Load `templates/types/{type}/discovery.md`
2. Ask discovery questions interactively
3. Write answers to build's `02-discovery.md`

---

## Workflow Sequence

```
1. TYPE DETECTION
   └── Semantic match or user selection

2. BUILD SETUP
   └── Run init_build.py --type {type}

3. DISCOVERY
   ├── IF skill-based → Load skill
   └── ELSE → Use inline discovery template

4. MENTAL MODELS
   └── Run select_mental_models.py

5. RE-DISCOVERY (if gaps, max 2 rounds)
   └── Focus on identified gaps

6. FINALIZATION
   └── Merge into plan.md, generate steps.md
```

---

## Decision Tree

```
User wants build
    │
    ├── Can detect type from input?
    │   ├── YES → Use detected type
    │   └── NO → Show type options, user selects
    │
    ├── Type has discovery.skill?
    │   ├── YES → Load skill, run discovery
    │   └── NO → Use inline discovery.md
    │
    ├── Discovery complete?
    │   └── YES → Load mental models
    │
    ├── Mental models identify gaps?
    │   ├── YES AND rounds < 2 → Re-discovery
    │   └── NO OR rounds >= 2 → Finalize
    │
    └── Finalize plan.md and steps.md
```

---

*Router is mandatory for all build creation*
