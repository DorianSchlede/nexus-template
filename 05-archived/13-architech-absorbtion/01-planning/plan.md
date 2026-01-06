# Architech Absorbtion - Plan

**Last Updated**: 2025-12-31
**Source**: `mutagent-obsidian/architech/` (NOT auto-company/architech)
**Type**: Extraction + Planning (NO implementation in this project)

---

## Project Scope

**THIS PROJECT DOES NOT IMPLEMENT CODE.**

| Task | In This Project? |
|------|------------------|
| Read Architech source code | YES |
| Document pattern mechanics | YES |
| Design Nexus integration specs | YES |
| Create implementation checklists | YES |
| Write actual code | **NO** → Separate projects |
| Modify nexus-loader.py | **NO** → Project 14+ |

---

## Approach

**Strategy**: Perfect extraction → Granular planning → Separate implementation projects

1. Read and analyze each pattern's source code
2. Document the key mechanisms (not just what, but HOW it works)
3. Design simplified Nexus version (remove unnecessary complexity)
4. Create implementation checklist with files to create/modify
5. Output: Extraction doc ready to spawn implementation project

**Principle**: Extract mechanisms, not files. The value is in how things work, not the YAML itself.

---

## The 5 Patterns - Detailed Specs

### Pattern 1: Mental Model Smart Selection

**Source**: `mutagent-obsidian/architech/01-system/08-automation/scripts/mental_models/select_mental_models.py`

**What it does in Architech**:
- O(1) quick lookup via SITUATION_MODELS dictionary
- 9 situation types: starting, stuck, deciding, disagreement, failure, improving, creative, debugging, risk
- Model bundles: strategic-planning, decision-making, problem-solving, risk-assessment, innovation, team-alignment, ultrathink
- 30+ models across 8 categories

**Nexus integration design**:
```python
# Port select_mental_models.py logic to nexus-loader.py
# Add situation detection based on skill category or user query

SITUATION_MODELS = {
    "starting": ["jobs-to-be-done", "first-principles", "stakeholder-mapping"],
    "stuck": ["lateral-thinking", "inversion", "constraint-analysis"],
    "deciding": ["expected-value", "opportunity-cost", "decision-matrix"],
    # ... etc
}

# On skill load, suggest relevant models
```

**Implementation scope**: Port Python logic, integrate with loader

---

### Pattern 2: FULL Entity System Extraction (01-SYSTEM Layer)

**Source**: `mutagent-obsidian/architech/01-system/` (ENTIRE layer)

**Structure** (12 folders):
```
01-system/
├── 00-definitions/     # Entity type definitions (12 types)
│   └── entity-types/   # What each entity IS
├── 01-agents/          # System-level agents
├── 02-skills/          # Reusable skills
├── 03-tasks/           # Atomic tasks
├── 04-workflows/       # Multi-step workflows
├── 05-blueprints/      # Templates/patterns
├── 06-rules/           # Behavioral rules
├── 07-checklists/      # Quality checklists
├── 08-automation/      # Python scripts (27 total)
├── 10-documentation/   # System docs
├── 11-mental-models/   # Thinking frameworks
└── 99-archive/         # Archived items
```

**What to extract (HYPERDETAIL)**:
1. **Entity Type Definitions** - All 12 types with frontmatter schemas
2. **Folder Numbering Convention** - Why 00, 01, 02... not random
3. **Entity Interrelationships** - How agents use tasks, tasks use skills, etc.
4. **Frontmatter Schema** - `description`, `when`, `entity_type`, `agent_scope`
5. **Behavioral Flags** - `interactive`, `cognitive_mode`, `progressive`, `reasoning`
6. **The Shortcut Pattern** - How `~entity:name` maps to folder structure

**Key insight**: The 01-system layer IS the operating system. Everything else (00-meta, 02-domains, 03-cross-domain) builds on this foundation.

**Extraction deliverable**: Complete architectural documentation of the 01-system layer with every convention, pattern, and interrelationship documented

---

### Pattern 3: Quality Gate Framework

**Source**: `mutagent-obsidian/architech/01-system/00-definitions/entity-types/07-checklist.md`

**What it does in Architech**:
- PASS/CONCERNS/FAIL/WAIVED decision framework
- Evidence-based validation
- Evaluation checklists generated for executables
- Scoring formula: Overall = (Activation × 0.30) + (Execution × 0.40) + (Completion × 0.30)

**Nexus integration design**:
```yaml
# Add to skill outputs
## Quality Gate
status: [PASS|CONCERNS|FAIL|WAIVED]
confidence: [1-5]
evidence:
  - What supports this output
issues:
  - What's uncertain or incomplete
```

**Implementation scope**: Add to skill template, update skill execution convention

---

### Pattern 4: Structured Resume Schema

**Source**: `mutagent-obsidian/architech/00-meta/01-agents/meta-architect/memory/`

**What it does in Architech**:
- Handoff protocol with explicit fields
- Context preservation validated
- State machine transitions
- Memory structure: extraction-logs, pattern-analysis, synthesis

**Nexus integration design**:
```yaml
# _resume.md upgrade - YAML frontmatter
---
project_id: "13-architech-absorbtion"
phase: DISCOVERY | PLANNING | EXECUTION | REVIEW | COMPLETE
status: "Ready for Phase 2"
updated: 2025-12-31
---

# MANDATORY LOAD section (required)
## MANDATORY LOAD
| Shortcut | Path | Why |
|----------|------|-----|
| `~plan` | 01-planning/plan.md | Implementation specs |
| `~steps` | 01-planning/steps.md | Task checklist |

# Then: Current State, Next Action, etc.
```

**Required sections**:
1. **MANDATORY LOAD** - Files Claude MUST read before proceeding (shortcuts + paths + reason)
2. **Current State** - What's done
3. **Next Action** - What to do next
4. **Pattern/Task Summary** - Quick reference

**Implementation scope**: Create template, modify loader to validate mandatory_load field exists

---

### Pattern 5: Self-Assessment Loop

**Source**: `mutagent-obsidian/architech/00-meta/01-agents/meta-architect/memory/`
- `global-learnings.md`
- `vacuum-state.md`
- `pattern-analysis/`

**What it does in Architech**:
- Meta-memory tracks patterns and learnings
- Vacuum state tracks extraction status
- Pattern analysis identifies recurring behaviors
- Evolution log tracks changes

**Nexus integration design**:
```
01-memory/self-assessment/
  ├── weekly-synthesis.md    # Claude-generated weekly
  ├── changelog.md           # What changed and why
  └── patterns.md            # Recurring observations

Weekly ritual:
1. Claude summarizes week's _resume.md files
2. Identifies top 3 issues
3. Human reviews (30 min)
4. Approves 1-2 changes
```

**Implementation scope**: Create folder structure, create weekly-review skill

---

### Pattern 6: META Layer Architecture (NEW)

**Source**: `mutagent-obsidian/architech/00-meta/` (ENTIRE layer)

**Structure**:
```
00-meta/
├── 00-definitions/     # Meta-level definitions
├── 01-agents/          # Meta-architect, orchestrators
│   └── meta-architect/
│       ├── current/    # Active version
│       └── memory/     # Agent memory structure
├── 02-skills/          # Meta-level skills
├── 03-tasks/           # Meta tasks
├── 04-workflows/       # Meta workflows
├── 05-blueprints/      # Meta blueprints
├── 06-rules/           # Meta rules
├── 07-checklists/      # Meta checklists
├── 08-automation/      # Meta automation
├── 09-navigation/      # Navigation maps
├── 10-documentation/   # Meta docs
├── 10-mental-models/   # (duplicate numbering?)
├── 11-mental-models/   # Mental models
├── 20-project-management/  # Project management
└── 99-archive/         # Archived
```

**What to extract (HYPERDETAIL)**:
1. **Meta-Architect Memory Structure** - How agent memory works
   - `extraction-logs/` - What was learned
   - `pattern-analysis/` - Recurring patterns
   - `synthesis/` - Aggregated insights
   - `vacuum-state.md` - Extraction status
   - `global-learnings.md` - Cross-session learnings
2. **Agent Memory Pattern** - `current/` vs `evolution/` versioning
3. **Meta → System Interplay** - How 00-meta controls 01-system
4. **Navigation Maps** - How 09-navigation provides routing
5. **Layer Hierarchy** - Why meta sits above system

**Key insight**: 00-meta is the "control plane" that orchestrates 01-system. Understanding this interplay is critical for Nexus architecture.

**Extraction deliverable**: Complete META layer documentation with memory patterns, agent versioning, and control flow to system layer

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Source Architech | mutagent-obsidian | Has 27 Python scripts, 150+ tests, active |
| Port mechanism vs files | Mechanisms | Files are context-specific, mechanisms are reusable |
| All 5 at once vs incremental | Incremental | Reduce risk, validate each works |
| Start with which pattern | Pattern 4 (Resume Schema) | Highest immediate impact, lowest complexity |

---

## Resources Needed

**Files to Create**:
- `00-system/templates/_resume.template.yaml`
- `00-system/schemas/skill.schema.yaml`
- `01-memory/mental-models/situation-map.yaml`
- `01-memory/self-assessment/` folder structure

**Files to Modify**:
- `00-system/core/nexus-loader.py` - Add resume validation, model suggestion

**Python Scripts to Port** (from mutagent-obsidian/architech/):
- `01-system/08-automation/scripts/mental_models/select_mental_models.py`
- Logic from `01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py`

---

## Dependencies & Links

**Architech Source Files (mutagent-obsidian/architech/)**:
| Path | What to Extract |
|------|-----------------|
| `01-system/08-automation/scripts/mental_models/select_mental_models.py` | Situation mapping, bundle loading |
| `01-system/00-definitions/entity-types/07-checklist.md` | Quality gate pattern |
| `00-meta/01-agents/meta-architect/memory/` | Self-assessment structure |
| `HYPERMAP.md` | Complete cross-reference |
| `01-system/08-automation/hooks/entity_system/build_entity_definitions.py` | Entity XML generation (154 lines) |
| `01-system/08-automation/scripts/context_bundler.py` | Bundle loading (300 lines) |
| `01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py` | Mode system, agent scoping (1162 lines) |
| `01-system/08-automation/hooks/shortcut_system/shortcut_resolver.py` | 2-tier cascade, dependency loading (828 lines) |

**Nexus Files Impacted**:
- `00-system/core/nexus-loader.py`
- `00-system/templates/` (new)
- `00-system/schemas/` (new)
- `01-memory/mental-models/` (enhanced)
- `01-memory/self-assessment/` (new)

---

## Open Questions

- [x] Which Architech is source? → mutagent-obsidian
- [ ] Which 3 patterns to implement first? → Recommend: 4, 3, 5
- [ ] How strict should resume validation be? (warn vs error)
- [ ] Port select_mental_models.py directly or rewrite?

---

## Mental Models Applied

**First Principles**:
- What is the core value of Architech? → Structured execution with validation + smart selection
- What does Nexus actually lack? → Formal quality feedback, auto-suggestions, proper state tracking

**Inversion**:
- What would make this fail? → Over-porting complexity, breaking existing skills
- Prevention: Strict 5-pattern limit, test each before next

**Pareto**:
- Which 20% of Architech provides 80% of value? → The 5 patterns identified
- The 27 Python scripts contain the real value, not the 200+ markdown files

---

## Additional Patterns Discovered (From Python Scripts)

The following patterns emerged from reviewing the 27 Python automation scripts. These are **bonus patterns** beyond the core 5, to consider for future extraction.

### Bonus Pattern A: Entity Definitions Builder (Entity Loader)

**Source**: `mutagent-obsidian/architech/01-system/08-automation/hooks/entity_system/build_entity_definitions.py` (154 lines)

**What it does**:
- Scans `00-definitions/entity-types/*.md` files
- Extracts YAML frontmatter → generates XML definitions
- Ultra-minimal schema per entity: `d` (description), `w` (when to use), `p` (purpose)
- Outputs XML for agent consumption with usage instructions
- Single source of truth: entity frontmatter defines everything

**Key mechanism** (from source):
```python
def build_entity_definitions():
    entity_files = sorted(base_path.glob('[0-9][0-9]-*.md'))
    for file in entity_files:
        fm = extract_frontmatter(file)
        entities.append({
            'name': fm.get('name', file.stem),
            'description': fm.get('description', ''),  # d
            'when': fm.get('when', ''),  # w
            'purpose': fm.get('folder_purpose', ''),  # p
        })
```

**Output format**:
```xml
<entities>
  <usage>
    <critical>Load entity definition BEFORE creating or modifying any entity</critical>
    <pattern>~entity:{name}</pattern>
  </usage>
  <entity>
    <name>skill</name>
    <description>Reusable workflow for repeating tasks</description>
    <when>User wants to automate patterns</when>
    <purpose>Store skill definitions</purpose>
  </entity>
</entities>
```

**Nexus integration design**:
```python
# Add to nexus-loader.py: --generate-skill-index
# Scans 03-skills/**/*.md, extracts frontmatter, outputs skill index
# Could replace static metadata.skills with dynamic generation
```

**Verdict**: Low priority. Nexus already has `nexus-loader.py --startup` that builds skill metadata. Only useful if skill count grows significantly (100+ skills where static is slow).

---

### Bonus Pattern B: Context Bundler (Shortcut Bundles)

**Source**: `mutagent-obsidian/architech/01-system/08-automation/scripts/context_bundler.py` (300 lines)

**What it does**:
- Loads multiple shortcuts as a single "bundle" in one call
- Returns JSON array with full file content for each resolved shortcut
- Handles errors gracefully (missing files, encoding issues)
- Supports validation mode (`--validate`) to check bundle integrity
- Tracks metadata: load timestamp, file size, content length, repo context

**Usage**:
```bash
uv run context_bundler.py '["~rule:memory", "~rule:coding"]'           # JSON output
uv run context_bundler.py '["~rule:memory", "~rule:coding"]' --content-only  # Just content
uv run context_bundler.py '["~rule:memory", "~rule:coding"]' --validate      # Check only
```

**Key mechanism** (from source):
```python
class ContextBundler:
    def load_bundle(self, shortcuts: List[str], feature: Optional[str] = None) -> List[Dict]:
        bundle_documents = []
        for shortcut in shortcuts:
            resolved_path = self.shortcut_resolver.resolve(actual_shortcut, feature)
            content = open(resolved_path, 'r', encoding='utf-8').read()
            bundle_documents.append({
                "shortcut": actual_shortcut,
                "resolved_path": str(resolved_path),
                "exists": True,
                "content": content,
                "content_length": len(content),
                "load_timestamp": timestamp,
            })
        return bundle_documents
```

**Output format**:
```json
[
  {
    "shortcut": "~rule:memory",
    "resolved_path": "architech/01-system/02-rules/memory-rules.md",
    "exists": true,
    "content": "# Memory Rules...",
    "content_length": 2456,
    "load_timestamp": "2025-12-31T10:30:00"
  }
]
```

**Nexus integration design**:
```python
# Add to nexus-loader.py: --bundle <bundle-name>
# Predefined bundles in 00-system/bundles.yaml:
bundles:
  research:
    - "03-skills/research-pipeline/SKILL.md"
    - "03-skills/research-pipeline/skills/paper-analyze/SKILL.md"
    - "03-skills/research-pipeline/skills/paper-synthesize/SKILL.md"
  airtable:
    - "03-skills/airtable/airtable-connect/SKILL.md"
    - "03-skills/airtable/airtable-master/SKILL.md"

# Usage: python nexus-loader.py --bundle research
# Returns all skill contents in one JSON blob
```

**Verdict**: Medium priority. Useful for complex skill-chains where related skills should load together. Research-pipeline and integration skills (airtable, hubspot) would benefit from bundle loading.

---

### Bonus Pattern C: Dynamic Shortcut Registry (SELF-DOCUMENTING)

**Source**: `mutagent-obsidian/architech/01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py` (1162 lines, v5.2.0)

**REVISED VERDICT: HIGH PRIORITY - User wants self-documenting, not static maintenance.**

**What it does**:
- Builds registry dynamically from frontmatter (NO static YAML to maintain!)
- **Mode system**: `plan`, `exec`, `discover` - filters entity types per mode
- **Layer filtering**: meta, system, domains, cross-domain
- **Agent scoping**: `agent_scope` frontmatter field filters executables by agent
- **Output formats**: XML and JSON (compact and full)
- **Auto-derives**: shortcut, layer, category, entity type FROM FILE PATHS

**Mode entity types**:
```python
MODE_ENTITY_TYPES = {
    'plan': {'definition', 'agent', 'skill', 'task', 'workflow', 'blueprint', 'rule', 'checklist', 'navigation', 'documentation', 'mental-model'},
    'exec': {'agent', 'skill', 'task', 'workflow'},
    'discover': {'definition', 'rule', 'navigation', 'documentation', 'mental-model'}
}
```

**Key mechanism** (from source):
```python
class ShortcutRegistryBuilder:
    """
    Builds ultra-efficient shortcut registry from file frontmatter.

    Key features:
    - Entity metadata loaded FIRST (progressive disclosure foundation)
    - 1-2 level scanning (progressive disclosure)
    - Auto-derives layer, category, shortcut from paths
    - Smart collision detection (aliases only when needed)
    - Reference-based storage (44% token reduction)
    """

    def _derive_layer(self, file_path: Path) -> str:
        """Auto-derive layer from file path."""
        # 00-meta → "meta"
        # 01-system → "system"
        # 02-domains/01-strategy → "domain-strategy"
        # 03-cross-domain/10-project-management → "cross-domain-project-management"

    def _derive_category(self, file_path: Path) -> str:
        """Auto-derive category from parent folders using entity metadata."""
        # Uses 00-definitions/entity-types/ to map folder names to entity types
        # 01-agents → "agent"
        # 02-skills → "skill"
        # etc.
```

**Why dynamic beats static**:
| Aspect | Static YAML | Dynamic Frontmatter |
|--------|-------------|---------------------|
| Maintenance | Manual updates needed | Self-documenting |
| Single source of truth | No (YAML + files) | Yes (files only) |
| Consistency | Can drift | Always accurate |
| New entities | Add to YAML | Just add file |
| Cognitive load | Remember to update | Zero |

**Nexus integration design**:
```python
# Nexus version - simplified but still dynamic
# Scans 03-skills/**/*.md for frontmatter
# Auto-generates: ~skill:research-pipeline, ~skill:airtable-master
# No static shortcuts.yaml to maintain

# Required frontmatter in skill files:
---
description: "What this skill does"
when: "When to use it"
---
```

**Extraction deliverable**: Full analysis of dynamic registry mechanism, adapted for Nexus skill structure

---

### Bonus Pattern D: 2-Tier Cascade Shortcut Resolver

**Source**: `mutagent-obsidian/architech/01-system/08-automation/hooks/shortcut_system/shortcut_resolver.py` (828 lines, v3.0.0)

**What it does**:
- **2-tier architecture**: Base registry always loaded, domain registries loaded on-demand
- **Session caching**: Domain registries cached per session for performance
- **Dependency loading**: Recursively loads dependencies from frontmatter (up to 3 levels)
- **Auto-root detection**: Robustly finds architech root from any working directory
- **Domain cascade**: Detects domain-specific shortcuts (e.g., `~sales:agent:closer`)

**Key mechanism** (from source):
```python
class ShortcutResolver:
    """
    Dynamic shortcut resolver with 2-tier cascade architecture.

    Architecture:
    - Base registry: 00-architech only (loaded at session start)
    - Domain registries: Loaded on-demand when domain shortcut detected
    - Session caching: Domain registries cached for session duration
    """

    def __init__(self, root_path="context-store"):
        self.root_path = self._resolve_root_path(root_path)  # Auto-finds architech/
        self.cache = {}  # Path resolution cache
        self.loaded_domains = {}  # Domain registry cache
        self.registry = self._load_base_registry()  # Base shortcuts

    def resolve(self, shortcut: str, feature: Optional[str] = None) -> str:
        # 1. Detect if shortcut needs domain cascade
        domain = self._detect_domain_trigger(shortcut)
        if domain and domain not in self.loaded_domains:
            self._load_domain_registry(domain)  # On-demand loading

        # 2. Check cache
        cache_key = f"{shortcut}:{self.repo_context}:{feature}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # 3. Resolve from registry
        return self._resolve_shortcut(shortcut, feature)

    def load_with_dependencies(self, shortcut, feature=None, max_depth=3, _visited=None):
        """Load shortcut AND its dependencies from frontmatter."""
        if _visited is None:
            _visited = set()

        # Prevent circular dependencies
        if shortcut in _visited:
            return shortcut, None, []
        _visited.add(shortcut)

        # Load primary file
        resolved_path, content = self.load_content(shortcut, feature)

        # Extract dependencies from YAML frontmatter
        dependencies = self.extract_dependencies(content)  # Parses dependencies: [~a, ~b]

        # Recursively load each dependency
        dep_docs = []
        for dep_shortcut in dependencies:
            if dep_shortcut not in _visited:
                dep_path, dep_content, nested = self.load_with_dependencies(
                    dep_shortcut, feature, max_depth=max_depth-1, _visited=_visited
                )
                dep_docs.append({"shortcut": dep_shortcut, "path": dep_path, "content": dep_content})
                dep_docs.extend(nested)

        return resolved_path, content, dep_docs
```

**CLI usage**:
```bash
# Resolve path only
python shortcut_resolver.py ~orchestrator

# Load content
python shortcut_resolver.py ~orchestrator --content-only

# Load with all dependencies (recursive)
python shortcut_resolver.py ~orchestrator --with-deps --json

# Validate shortcut exists
python shortcut_resolver.py ~orchestrator --validate

# Show dependencies without loading content
python shortcut_resolver.py ~orchestrator --deps-only
```

**Nexus integration design** (if we wanted to port):
```python
# Add to nexus-loader.py: --with-deps flag
# Skills declare dependencies in frontmatter:
# ---
# dependencies: ["03-skills/slack/slack-master/SKILL.md"]
# ---
#
# Loader auto-loads master skill when loading slack-connect
```

**Verdict**: **HIGH PRIORITY - Implement with dynamic registry (Pattern C).**

User wants shortcuts to avoid typing full paths everywhere. The Nexus shortcut resolver will:
- Use DYNAMIC registry from frontmatter (self-documenting, Pattern C)
- Simplified tier structure (Nexus is flatter than Architech)
- Keep core resolution logic + dependency loading

---

### Nexus Shortcut System Design (Dynamic, Self-Documenting)

**Goal**: Replace full paths with `~shortcuts` everywhere. NO static YAML to maintain.

**How it works**:
1. Scan `03-skills/` for SKILL.md files with frontmatter
2. Scan `02-projects/` for _resume.md files with frontmatter
3. Auto-derive shortcuts from folder structure
4. Cache registry at startup (rebuild on --refresh)

**Auto-derived shortcuts** (no manual maintenance):
```
# From folder structure (convention-based):
~skill:{name}     → 03-skills/{name}/SKILL.md  (scans 03-skills/**/SKILL.md)
~project:{id}     → 02-projects/{id}/          (scans 02-projects/*/)
~resume:{id}      → 02-projects/{id}/_resume.md
~plan:{id}        → 02-projects/{id}/01-planning/plan.md

# Fixed system paths (hardcoded, don't change):
~loader           → 00-system/core/nexus-loader.py
~orchestrator     → 00-system/ORCHESTRATOR.md
~goals            → 01-memory/goals.md
~config           → 01-memory/user-config.yaml

# Context-aware (set by --project flag):
~current          → 02-projects/{current}/
~current:resume   → 02-projects/{current}/_resume.md
```

**CLI usage**:
```bash
# Resolve shortcut to path
python nexus-loader.py --resolve ~goals
# → 01-memory/goals.md

# Resolve with content
python nexus-loader.py --resolve ~skill:research-pipeline --content
# → Returns SKILL.md content

# List all available shortcuts (dynamic scan)
python nexus-loader.py --list-shortcuts
# → Shows all auto-discovered shortcuts

# Refresh shortcut cache
python nexus-loader.py --refresh-shortcuts
```

**Implementation scope**:
1. Add `ShortcutResolver` class to `nexus/resolver.py` (~200 lines)
2. Add `--resolve`, `--list-shortcuts`, `--refresh-shortcuts` flags
3. Scan frontmatter for `description`, `when` fields
4. Cache results in `.cache/shortcuts.json`

**Key design from Architech**:
| Feature | Architech | Nexus (Simplified) |
|---------|-----------|---------------------|
| Registry | Dynamic (frontmatter) | Dynamic (frontmatter) |
| Maintenance | Zero | Zero |
| Tiers | 2-tier cascade | Single tier |
| Domains | 7 domains | None (flat) |
| Mode system | plan/exec/discover | Optional (future) |
| Agent scoping | Yes | No |
| Lines of code | 1162 + 828 | ~200 |

---

## Pattern Priority Matrix (REVISED)

| # | Pattern | Impact | Complexity | Extraction Priority |
|---|---------|--------|------------|---------------------|
| **C+D** | **Dynamic Shortcut System** | High | Medium | **#1 - Extract first** |
| **2** | **Entity System (01-SYSTEM)** | High | High | **#2 - Full layer extraction** |
| **6** | **META Layer (00-META)** | High | High | **#3 - Control plane analysis** |
| **4** | Resume Schema | High | Low | #4 |
| **3** | Quality Gates | High | Medium | #5 |
| **5** | Self-Assessment | Medium | Low | #6 |
| 1 | Mental Models | Medium | Medium | Optional |
| A | Entity Builder | Low | Low | Reference only |
| B | Context Bundler | Medium | Medium | After C+D |

**Key insights**:
1. **C+D combined** - Dynamic registry (C) + resolver (D) work together. Self-documenting, no static YAML.
2. **Pattern 2 expanded** - Not just validation, but ENTIRE 01-system layer architecture.
3. **Pattern 6 added** - META layer is the control plane. Must understand meta→system interplay.
4. **Self-documenting always** - User explicitly requested no static shortcuts that need maintenance.

---

## Output Deliverables

This project produces pattern extraction documents in `02-resources/extractions/`:

| # | Pattern | Extraction Doc | Status | Implementation Project |
|---|---------|----------------|--------|----------------------|
| **C+D** | **Dynamic Shortcut System** | `extraction-CD-shortcuts.md` | TODO | Project 14 |
| **2** | **Entity System (01-SYSTEM)** | `extraction-2-entity-system.md` | TODO | Project 15 |
| **6** | **META Layer (00-META)** | `extraction-6-meta-layer.md` | TODO | Project 16 |
| **4** | Resume Schema | `extraction-4-resume.md` | TODO | Project 17 |
| **3** | Quality Gates | `extraction-3-gates.md` | TODO | Project 18 |
| **5** | Self-Assessment | `extraction-5-assessment.md` | TODO | Project 19 |
| 1 | Mental Models | `extraction-1-models.md` | TODO | Optional |
| B | Context Bundler | `extraction-B-bundler.md` | TODO | After C+D |
| A | Entity Loader | `extraction-A-loader.md` | TODO | Reference only |

### Extraction Doc Template

Each extraction doc follows this structure:

```markdown
# Pattern X: [Name] - Extraction

## Source
- **File**: `mutagent-obsidian/architech/path/to/file.py`
- **Lines**: XXX
- **Key functions**: `function1()`, `function2()`

## What It Does
[Plain English explanation]

## How It Works
[Key mechanisms with code samples]

## Nexus Design
[Simplified version for Nexus]

## Implementation Checklist
- [ ] Create `00-system/file.yaml`
- [ ] Create `nexus/module.py`
- [ ] Add flag to nexus-loader.py
- [ ] Test with X, Y, Z

## Files to Create/Modify
| File | Action | Purpose |
|------|--------|---------|
| `00-system/shortcuts.yaml` | Create | Static registry |
| `nexus/resolver.py` | Create | Resolver class |
| `nexus-loader.py` | Modify | Add --resolve flag |

## Test Plan
1. Test case 1
2. Test case 2
```

---

*This project extracts patterns. Implementation happens in Projects 14-17.*
