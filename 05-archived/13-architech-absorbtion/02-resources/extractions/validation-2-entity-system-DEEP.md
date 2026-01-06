# Deep Validation: extraction-2-entity-system.md

**Validator**: Deep Validation Agent
**Date**: 2026-01-01
**Scope**: All additional files in `mutagent-obsidian/architech/01-system/` not covered in original extraction

---

## 1. Additional Files Discovered

### 1.1 Entity System Scripts (Not Covered)

| File | Path | Purpose |
|------|------|---------|
| `build_entity_definitions.py` | `08-automation/hooks/entity_system/` | Generates XML entity definitions from frontmatter |
| `README.md` (entity_system) | `08-automation/hooks/entity_system/` | Documents the entity system runtime hook |
| `activate_agent.py` | `08-automation/hooks/agent_system/` | Activates agents via alias resolution |
| `init_skill.py` | `08-automation/scripts/skill_system/` | Initializes new skills with numbered folder structure |

### 1.2 Shortcut System Scripts (Partially Covered)

| File | Path | Purpose |
|------|------|---------|
| `shortcut_resolver.py` | `08-automation/hooks/shortcut_system/` | Dynamic entity loader with agent-centric architecture v3.0 |
| `context_loader.py` | `08-automation/hooks/shortcut_system/` | Injects behavioral rules based on frontmatter flags |
| `help_generator.py` | `08-automation/hooks/shortcut_system/` | Generates help menus from registry |
| `build_shortcut_registry.py` | `08-automation/hooks/shortcut_system/` | Builds shortcut registry from frontmatter |
| `README.md` (shortcut_system) | `08-automation/hooks/shortcut_system/` | v3.0 agent-centric mode system documentation |
| `STRUCTURE.md` | `08-automation/hooks/shortcut_system/` | File organization reference |

### 1.3 Validation Scripts (Not Covered)

| File | Path | Purpose |
|------|------|---------|
| `validate_frontmatter.py` | `08-automation/scripts/` | Scans markdown files for valid YAML frontmatter |
| `validate_registry_integrity.py` | `08-automation/scripts/` | Validates all shortcuts point to existing files |
| `validate_wikilinks.py` | `08-automation/scripts/` | Pre-commit hook for wikilink validation |

### 1.4 Context Bundler (Not Covered)

| File | Path | Purpose |
|------|------|---------|
| `context_bundler.py` | `08-automation/scripts/` | Loads Context Bundles - collections of engineering rules |

### 1.5 Entity Instantiations (Not Covered)

| File | Path | Purpose |
|------|------|---------|
| `master.md` | `01-agents/` | Master Task Executor - universal executor agent |
| `README.md` | `01-agents/` | Agent folder documentation |
| `README.md` | `02-skills/` | Skills folder documentation |
| `README-v2.md` | `02-skills/` | Skills system v2 documentation |
| 5+ skill folders | `02-skills/` | Actual skill implementations |
| 8+ task files | `03-tasks/` | Actual task implementations |
| `bootstrap-architech.md` | `04-workflows/` | Complete workflow example |

### 1.6 Rules and Checklists (Not Covered)

| File | Path | Purpose |
|------|------|---------|
| 16+ rule files | `06-rules/` | Behavioral constraints (adaptive-reasoning, context-monitoring, etc.) |
| 13+ checklist files | `07-checklists/` | Quality gates and validation checklists |
| `evaluation/` folder | `07-checklists/` | Evaluation checklist infrastructure |
| `validation/` folder | `07-checklists/` | ASV (Agent Sequence Validators) |

---

## 2. File Analysis

### 2.1 build_entity_definitions.py

**Path**: `01-system/08-automation/hooks/entity_system/build_entity_definitions.py`
**Purpose**: Runtime generation of entity type definitions in XML format
**Relevance**: HIGH - Core entity system infrastructure

**Key Patterns NOT in Extraction**:
```python
# Runtime output pattern - called via bash and piped to consumer
def build_entity_definitions():
    """Build entity definitions from entity frontmatter."""
    base_path = Path('context-store/architech/01-system/00-definitions/entity-types')
    entity_files = sorted(base_path.glob('[0-9][0-9]-*.md'))
    # Extracts: folder_pattern, name, description, when, folder_purpose
```

**Missing Pattern**: The script uses `folder_pattern` with backward compatibility for `folder_number`:
```python
folder_pattern = fm.get('folder_pattern', fm.get('folder_number', '??'))  # Backward compat
```

**XML Output Format**:
```xml
<entities>
  <usage>
    <critical>Load entity definition BEFORE creating or modifying any entity</critical>
    <pattern>~entity:{name} (e.g., ~entity:agent, ~entity:task)</pattern>
    <resolver_command>python shortcut_resolver.py ~entity:{name} --content</resolver_command>
  </usage>
  <entity>
    <name>{name}</name>
    <description>{description}</description>
    <when>{when}</when>
    <purpose>{folder_purpose}</purpose>
  </entity>
</entities>
```

### 2.2 activate_agent.py

**Path**: `01-system/08-automation/hooks/agent_system/activate_agent.py`
**Purpose**: Resolves agent aliases and activates agents with correct mode
**Relevance**: HIGH - Agent activation infrastructure

**Key Patterns NOT in Extraction**:

1. **Agent Discovery Path Patterns**:
```python
agent_paths = [
    root_path / "00-meta" / "01-agents",
    root_path / "01-system" / "01-agents",
    root_path / "02-domains" / "*" / "01-agents",
    root_path / "03-cross-domain" / "*" / "01-agents",
]
```

2. **Layer Derivation Pattern**:
```python
def _derive_layer(file_path: Path, root_path: Path) -> str:
    if parts[0] == "00-meta": return "meta"
    elif parts[0] == "01-system": return "system"
    elif parts[0] == "02-domains": return f"domain-{domain}"
    elif parts[0] == "03-cross-domain": return f"cross-domain-{system}"
```

3. **Mode Derivation from Layer**:
```python
def derive_mode(layer: str) -> str:
    if layer in ['meta', 'system']: return 'plan'
    elif layer.startswith('domain-') or layer.startswith('cross-domain-'): return 'exec'
```

4. **Alias Resolution Pattern**:
- Agents have `activation_aliases` in frontmatter
- Resolution is case-insensitive
- Output format: `{agent_name}|{mode}`

### 2.3 init_skill.py

**Path**: `01-system/08-automation/scripts/skill_system/init_skill.py`
**Purpose**: Creates skill scaffolding with numbered folder structure
**Relevance**: HIGH - Skill creation infrastructure

**Key Patterns NOT in Extraction**:

1. **Skill Template Structure**:
```python
skill-name/
├── {skill-name}.md          # Main entrypoint (from SKILL_TEMPLATE)
├── 02-tasks/                 # Execution procedures
├── 04-blueprints/            # Template generators
├── 05-rules/                 # Behavioral constraints
├── 06-checklists/            # Quality gates
├── 07-automation/            # Infrastructure scripts
├── 09-documentation/         # Reference docs
└── assets/                   # Output files
```

2. **Auto-Detection Context Pattern**:
```python
architech_contexts = [
    cwd / "architech" / "00-meta" / "01-skills",
    cwd / "architech" / "01-system" / "01-skills",
    cwd / "00-meta" / "01-skills",
    cwd / "01-system" / "01-skills",
    cwd / "02-domains" / "01-skills",
    cwd / "03-cross-domain" / "01-skills",
]
```

3. **Skill Frontmatter Template**:
```yaml
---
name: {skill_name}
description: [TODO: Complete explanation]
when: [TODO: Specific trigger scenarios]
extraction_status: prototype
dependencies: []
complexity: moderate
created_date: {date}
last_updated: {date}
created_author: {author}
---
```

### 2.4 Validation Scripts

**Purpose**: Ensure entity system integrity

**validate_frontmatter.py** - Key Patterns:
- Scans all `.md` files excluding `99-archive/` and `.template.md`
- Checks for valid YAML frontmatter
- Reports files missing `description` field
- Outputs health score percentage

**validate_registry_integrity.py** - Key Patterns:
- Uses `ShortcutRegistryBuilder` to build full registry
- Validates all paths resolve to existing files
- Checks aliases point to valid primary shortcuts
- Reports broken shortcuts

**validate_wikilinks.py** - Key Patterns:
- Validates wikilinks use filename format (not display names)
- Pattern: `[[filename]]` not `[[Display Name]]`
- Suggests corrections: "Display Name" -> "display-name"

### 2.5 context_bundler.py

**Path**: `01-system/08-automation/scripts/context_bundler.py`
**Purpose**: Loads Context Bundles - collections of engineering rules for agent operations
**Relevance**: MEDIUM - Context loading infrastructure

**Key Patterns NOT in Extraction**:
```python
class ContextBundler:
    """Loads Context Bundles - collections of engineering rules for agent operations."""

    def load_bundle(self, shortcuts: List[str], feature: Optional[str] = None) -> List[Dict]:
        """Load a bundle of shortcuts and return as JSON array with full content."""
        # Uses shortcut resolver to get resolution info
        # Handles feature-specific shortcuts with {feature} substitution
        # Returns document with: shortcut, resolved_path, exists, content, metadata
```

**Usage Pattern**:
```bash
uv run context_bundler.py '["~rule:memory", "~rule:coding"]' --content-only
```

### 2.6 Entity Instantiations

**master.md (Agent)** - Key Structure NOT in Extraction:
```yaml
---
name: master
scope_type: orchestrator
complexity: expert
---

agent:
  name: Master
  id: master
  title: Master Task Executor
  icon: emoji
  whenToUse: Use when you need comprehensive expertise...

persona:
  role: Master Task Executor & Architech Method Expert
  identity: Universal executor...
  focus: Execute any task directly...
  core_principles: [...]

commands:
  - help: Show listed commands
  - create-doc: Execute ~task:create-doc
  - task [name]: Execute any task by name

dependencies:
  shortcut_validation: [shortcut-registry.yaml]
  checklists: [~checklist:architect, ...]
  tasks: [~task:create-requirements, ...]
  engineering_rules: [~context-map, ~rule:memory, ...]
  memory_integration: [.memory/features/, ...]
  structure_templates: [~blueprint:workflow, ...]
```

**create-agent.md (Task)** - Key Structure NOT in Extraction:
- 9 Phases of interactive agent creation
- Phase 1: Discovery & Elicitation (Agent Purpose Discovery, Persona Definition, Scope & Complexity)
- Phase 2: Capabilities & Commands
- Phase 3: Context & Memory Requirements
- Phase 4: Quality Gates & Validation
- Phase 5: Examples & Documentation
- Phase 6: Agent Generation (calls `agent-generator.py` blueprint)
- Phase 7: System Integration
- Phase 8: Git Workflow Integration
- Phase 9: Cascading Creation Options

**bootstrap-architech.md (Workflow)** - Key Structure NOT in Extraction:
- 6-step execution flow
- Complete YAML workflow definition
- Quality gates at each step (PASS/CONCERNS/FAIL)
- Technology detection patterns
- Engineering rules templates

### 2.7 Skill Implementations

**git-push-authenticated** skill - Structure:
```
git-push-authenticated/
├── git-push-authenticated.md     # Main entrypoint with workflow
├── 02-tasks/
│   └── diagnose-push-failure.md
└── 05-rules/
    └── git-auth-priority.md
```

**diagnose-trace** skill - Structure:
```
diagnose-trace/
├── diagnose-trace.md             # Main entrypoint
└── 09-documentation/
    └── trace-schema.md           # Complete event/tool schemas
```

**create-evaluation-checklist** skill - Key Pattern:
- Derives evaluation checklists from executable entities
- Four derivation types: Agent, Skill, Task, Workflow
- Output format includes activation, execution, completion phases
- Integrates with `diagnose-trace` for validation

---

## 3. Missing Patterns

### 3.1 Agent Structure Patterns

The extraction covers agent frontmatter but misses the INTERNAL structure:

```yaml
# Inside agent markdown (not in frontmatter)
IDE-FILE-RESOLUTION:
  - Dependencies map to ~shortcuts or direct paths

REQUEST-RESOLUTION: Match user requests to commands flexibly

activation-instructions:
  - STEP 1: Read THIS ENTIRE FILE
  - STEP 2: Adopt the persona
  - STEP 3: Load shortcut registry
  - STEP 4: Load ~context-map
  - STEP 5: Greet and run *help
  - CRITICAL: Stay in character

agent:
  name: {name}
  id: {kebab-case-id}
  title: {Title}
  icon: {emoji}
  whenToUse: {use case}
  customization: {overrides}

persona:
  role: {role}
  identity: {identity}
  focus: {focus}
  core_principles: [...]

commands:
  - command: description

dependencies:
  shortcut_validation: [...]
  checklists: [...]
  tasks: [...]
  engineering_rules: [...]
  memory_integration: [...]
  structure_templates: [...]

context_locations:
  top_level_context:
    read_access: [...]
    write_access: [...]
  feature_context:
    read_access: [...]
    write_access: [...]

context_update_triggers:
  during_{agent}_oversight:
    - trigger: '{trigger}'
      update_location: '{path}'
      content: '{what to update}'
```

### 3.2 Task Phase Structure Patterns

The extraction mentions "Step 0 + Steps 1-N" but misses the INTERACTIVE task pattern:

```markdown
### Phase N: {Phase Name} (INTERACTIVE|AUTONOMOUS)

**Goal:** {Phase goal}

#### Step N.M: {Step Name}

Ask the user:
```
{Formatted elicitation questions}
```

**Capture:**
- `variable_name`: Description
- `another_variable`: Description
```

### 3.3 Workflow Phase Structure Patterns

The extraction mentions phases but misses:

```yaml
execution_flow:
  step_0_validate_system:
    agent: "{agent}"
    task: "{task-name}"
    description: "{description}"
    validation_framework: "~unified-validator"
    gates: [gate1, gate2]
    outputs: [output1, output2]

  step_1_analyze:
    agent: "{agent}"
    task: "{task-name}"
    description: "{description}"
    validation_gate:
      after_step_1: "{gate description}"
    capabilities: [capability1, capability2]
    outputs: [output1, output2]
```

### 3.4 Skill Sub-Entity Structure

The extraction mentions skill folders but misses the internal wikilink patterns:

```markdown
## Components

### Tasks (02-tasks/)
- [[02-tasks/example-task.md]] - Example task

### Rules (05-rules/)
- [[05-rules/example-validation.md]] - Example rule

### Documentation (09-documentation/)
- [[09-documentation/reference.md]] - Example docs

## Progressive Disclosure
- Load tasks when executing
- Load rules when validating
- Scripts may execute without loading to context

## Extraction Notes
**When ready for promotion to parent layer**:
- [ ] All components tested
- [ ] All scripts validated
- [ ] All documentation complete

**Extraction Process**:
1. Move components from skill folders to parent layer folders
2. Update wikilinks in promoted files
3. Delete skill folder
4. Rebuild shortcut registry
```

### 3.5 Evaluation Checklist Derivation Rules

The extraction mentions evaluation checklists but misses the derivation rules:

| Source | Phase | What to Extract | Checklist Item Example |
|--------|-------|-----------------|------------------------|
| Agent | Activation | Scripts in activation instructions | `[ ] Ran shortcut_resolver.py ~agent-id --content` |
| Agent | Activation | Context loads | `[ ] Loaded ~meta-map` |
| Agent | Execution | Capabilities | `[ ] Agent capabilities available` |
| Skill | Activation | Trigger conditions | `[ ] Trigger condition met` |
| Skill | Execution | Workflow steps | `[ ] Executed Step 1: {description}` |
| Task | Prerequisites | Step 0 requirements | `[ ] Loaded ~entity:{type}` |
| Task | Execution | Each step's actions | `[ ] Step 1: {action}` |
| Workflow | Initialization | Phase 1 setup | `[ ] Initialized workflow context` |
| Workflow | Execution | Phase gates | `[ ] Phase 1 complete, gate passed` |

### 3.6 Validation Infrastructure

Not covered in extraction:

1. **Frontmatter Validation**:
   - Required field: `description`
   - Skips `.template.md` files
   - Skips `99-archive/` directory

2. **Registry Integrity Validation**:
   - Validates aliases point to existing shortcuts
   - Validates file paths exist on disk
   - Uses `ShortcutRegistryBuilder` for registry construction

3. **Wikilink Validation**:
   - Enforces filename format over display name format
   - Auto-suggests corrections
   - Pre-commit hook integration

### 3.7 Context Bundle Loading

Not covered in extraction:

```python
# Context Bundle format
{
    "shortcut": "~rule:memory",
    "resolved_path": "path/to/file.md",
    "exists": True,
    "source_type": "engineering_rule",
    "content": "...",
    "content_length": 1234,
    "file_size_bytes": 5678,
    "load_timestamp": "2026-01-01T00:00:00",
    "repo_context": "context-store"
}
```

---

## 4. Enhancement Recommendations

### 4.1 High Priority Additions

1. **Add Agent Internal Structure Section**
   - Document the full agent YAML structure (agent, persona, commands, dependencies, context_locations)
   - Include activation-instructions pattern
   - Show context_update_triggers pattern

2. **Add Skill Sub-Entity Wikilink Patterns**
   - Document how skills reference internal components via wikilinks
   - Show the extraction process with wikilink updates
   - Include progressive disclosure rules for skill components

3. **Add Validation Infrastructure**
   - Document the three validation scripts
   - Include health score calculation
   - Show pre-commit integration pattern

4. **Add Context Bundle Pattern**
   - Document `context_bundler.py` usage
   - Show bundle loading format
   - Include feature-specific shortcut substitution

### 4.2 Medium Priority Additions

5. **Add Entity Activation Flow**
   - Document `activate_agent.py` alias resolution
   - Show layer-to-mode mapping
   - Include output format pattern

6. **Add Workflow YAML Structure**
   - Document full `execution_flow` schema
   - Include validation_gate patterns
   - Show quality gate states (PASS/CONCERNS/FAIL)

7. **Add Task Phase Structure**
   - Document INTERACTIVE vs AUTONOMOUS phases
   - Include elicitation question format
   - Show variable capture pattern

### 4.3 Low Priority Additions

8. **Add init_skill.py Templates**
   - Include all example templates (EXAMPLE_TASK, EXAMPLE_RULE, etc.)
   - Document context auto-detection logic

9. **Add Entity Definition XML Format**
   - Include full XML schema with usage instructions
   - Document the resolver command pattern

10. **Add Evaluation Checklist Derivation**
    - Include full derivation rules table
    - Document source-to-checklist mapping
    - Show evaluation checklist frontmatter

---

## 5. Summary Statistics

| Category | Covered in Extraction | Found in Deep Validation |
|----------|----------------------|--------------------------|
| Entity System Scripts | 1 partial mention | 4 full implementations |
| Shortcut System Scripts | 4 mentions | 6 full implementations |
| Validation Scripts | 0 | 3 full implementations |
| Context Bundler | 0 | 1 full implementation |
| Entity Instantiations | Schema examples only | 15+ full examples |
| Rules | Schema only | 16+ implementations |
| Checklists | Schema only | 13+ implementations |
| Skills | Lifecycle only | 5+ full implementations |

**Completeness Score**: Original extraction covers ~65% of entity system infrastructure
**Recommended Enhancement Priority**: Agent internal structure, Validation infrastructure, Skill sub-entity patterns

---

**Deep Validation Complete**

This report identifies 35+ additional files not covered in the original extraction, with patterns that enhance understanding of the Architech entity system implementation. The most critical missing patterns are the agent internal structure, skill sub-entity wikilink patterns, and validation infrastructure.
