# Template System Design for plan-project

**Purpose**: Define how type-specific templates enable smart project planning

---

## Current State

`init_project.py` already supports:
- `--type` flag (build, research, strategy, content, process, generic)
- Loads `templates/template-{type}.md` for plan.md sections
- But templates don't exist yet!

---

## Proposed Template Structure

```
plan-project/
├── scripts/
│   └── init_project.py          # Already has --type support
├── templates/
│   ├── plan/                    # Plan.md section templates
│   │   ├── template-build.md
│   │   ├── template-research.md
│   │   ├── template-strategy.md
│   │   ├── template-content.md
│   │   ├── template-process.md
│   │   ├── template-integration.md  # NEW
│   │   └── template-generic.md
│   ├── steps/                   # Steps.md phase templates
│   │   ├── steps-build.md
│   │   ├── steps-research.md       # Points to skill
│   │   ├── steps-strategy.md
│   │   ├── steps-content.md
│   │   ├── steps-process.md
│   │   ├── steps-integration.md    # Points to skill
│   │   └── steps-generic.md
│   └── discovery/               # Discovery templates (NEW)
│       ├── discovery-template.md   # Base template (exists)
│       ├── discovery-integration.md
│       └── discovery-research.md
└── references/
    ├── project-types.md         # Type definitions + mental models
    ├── workflows.md             # Workflow references
    └── routing-logic.md         # NEW: How routing works
```

---

## Template: template-integration.md

```markdown
## Integration Configuration

**Service**: [Service name]
**API Documentation**: [URL]

### Authentication
| Setting | Value |
|---------|-------|
| Auth Type | [oauth2/api_key/bearer] |
| Environment Variable | [ENV_KEY] |

### Selected Endpoints
| Endpoint | Method | Path | Purpose |
|----------|--------|------|---------|
| [name] | GET | /path | [description] |

### Integration Architecture
Using 3-tier pattern:
- `{service}-master/` - Shared resources
- `{service}-connect/` - User entry point
- `{service}-{operation}/` - Per-endpoint skills

---

**Config Location**: `02-resources/integration-config.json`
**Scaffold Command**: `python 00-system/skills/system/add-integration/scripts/scaffold_integration.py`
```

---

## Template: template-research.md

```markdown
## Research Configuration

### Research Question
**Primary RQ**: [From _briefing.md]

**Research Purpose**: [Why this matters, what you'll use insights for]

### Extraction Schema
| Field | Description | Priority |
|-------|-------------|----------|
| [field_1] | [description] | high |
| [field_2] | [description] | medium |

### Paper Corpus
| Paper ID | Chunks | Status |
|----------|--------|--------|
| [paper_1] | [N] | ready |

### Analysis Configuration
- Subagents: [calculated count]
- Max concurrent: 15
- Anti-hallucination: 3-point evidence + SHA256

---

**Briefing**: `02-resources/_briefing.md`
**Analysis Kit**: `02-resources/_analysis_kit.md`
**Execute**: `analyze research project {name}`
```

---

## Template: steps-integration.md

```markdown
## Phase 1: Planning
- [ ] Complete 01-overview.md
- [ ] Apply mental models (success criteria, risks)
- [ ] Complete 02-discovery.md

## Phase 2: API Discovery
**Load skill**: `add-integration`
- [ ] Search for API documentation
- [ ] Parse and cache endpoints
- [ ] Select endpoints to implement
- [ ] Generate integration-config.json

## Phase 3: Scaffolding
- [ ] Run scaffold_integration.py
- [ ] Verify generated skill structure
- [ ] Test config check script

## Phase 4: Implementation
- [ ] Implement each operation skill
- [ ] Test with sample data
- [ ] Document in setup-guide.md

## Phase 5: Completion
- [ ] Full integration test
- [ ] Update orchestrator routing
- [ ] Close session
```

---

## Template: steps-research.md

```markdown
## Phase 1: Planning
- [ ] Complete 01-overview.md
- [ ] Apply mental models (success criteria, risks)
- [ ] Complete 02-discovery.md

## Phase 2: Research Setup
**Load skill**: `create-research-project`
- [ ] Define research question and extraction schema
- [ ] Search academic databases
- [ ] Review abstracts and assess relevance
- [ ] User approves paper selection
- [ ] Download approved papers
- [ ] Preprocess PDFs to markdown chunks
- [ ] Generate analysis kit and extraction guide

## Phase 3: Analysis
**Load skill**: `analyze-research-project`
- [ ] Spawn analysis subagents
- [ ] Validate analysis logs
- [ ] Mark ready for synthesis

## Phase 4: Synthesis
**Load skill**: `synthesize-research-project`
- [ ] Build synthesis routing
- [ ] Run extraction batches
- [ ] Aggregate patterns
- [ ] Generate final report

## Phase 5: Completion
- [ ] Review synthesis report
- [ ] Export findings
- [ ] Close session
```

---

## How Templates Get Used

### In init_project.py (already implemented)
```python
def load_type_template(project_type):
    """Load type-specific template sections from templates/ directory."""
    templates_dir = script_dir / "templates"
    template_file = templates_dir / f"template-{project_type}.md"

    if not template_file.exists():
        print(f"[WARNING] Template not found for type '{project_type}', using minimal")
        return ""

    return template_file.read_text(encoding='utf-8')
```

### In SKILL.md (routing logic)
```markdown
## Step 4: Type-Specific Discovery

IF type == "integration":
  - Load `templates/plan/template-integration.md` into plan.md
  - Load `templates/steps/steps-integration.md` into steps.md
  - Route to `add-integration` skill for API discovery

IF type == "research":
  - Load `templates/plan/template-research.md` into plan.md
  - Load `templates/steps/steps-research.md` into steps.md
  - Route to `create-research-project` skill for research setup

ELSE:
  - Load `templates/plan/template-{type}.md` into plan.md
  - Load `templates/steps/steps-{type}.md` into steps.md
  - Continue inline
```

---

## Smart TODO Integration

The steps templates can be loaded into TodoWrite:
```python
# Parse steps template and create todos
steps_content = load_template(f"steps-{project_type}.md")
todos = parse_checkboxes(steps_content)
TodoWrite(todos)
```

This gives structured progress tracking tied to project type.
