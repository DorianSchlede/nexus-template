# Extraction 2: Entity System - 01-SYSTEM Layer Architecture

**Source**: `mutagent-obsidian/architech/01-system/`
**Extracted**: 2026-01-01
**Purpose**: HYPERDETAILED extraction of Entity System patterns for Project 15 (Nexus Entity System Implementation)

---

## 1. Folder Structure - The 12 Numbered Folders

The 01-system layer uses a strict numbered folder convention that provides **consistent organization across ALL layers** (meta, system, domain, cross-domain).

### Complete Folder Hierarchy

```
01-system/
├── 00-definitions/           # Framework specifications and schemas
│   ├── entity-types/         # 12 entity type definitions (the core)
│   │   ├── 00-definition.md
│   │   ├── 01-agent.md
│   │   ├── 02-skill.md
│   │   ├── 03-task.md
│   │   ├── 04-workflow.md
│   │   ├── 05-blueprint.md
│   │   ├── 06-rule.md
│   │   ├── 07-checklist.md
│   │   ├── 08-automation.md
│   │   ├── 09-navigation.md
│   │   ├── 10-documentation.md
│   │   ├── 11-mental-model.md
│   │   └── 12-evaluation.md
│   └── README.md
├── 01-agents/                # Persona-driven executors
├── 02-skills/                # Temporary capability containers
├── 03-tasks/                 # Atomic execution units
├── 04-workflows/             # Multi-agent coordination
├── 05-blueprints/            # Template generators (Python scripts)
├── 06-rules/                 # Behavioral constraints
├── 07-checklists/            # Quality gates and validation
├── 08-automation/            # Infrastructure scripts
│   ├── hooks/
│   │   ├── platform_compat.py     # Cross-platform encoding fix
│   │   ├── agent_system/
│   │   │   └── activate_agent.py
│   │   ├── entity_system/
│   │   │   └── build_entity_definitions.py
│   │   └── shortcut_system/
│   │       ├── build_shortcut_registry.py
│   │       ├── shortcut_resolver.py
│   │       ├── context_loader.py
│   │       └── help_generator.py
│   ├── scripts/
│   │   ├── mental_models/
│   │   └── skill_system/
│   └── tests/
├── 09-navigation/            # Maps, guides, wayfinding docs (EMPTY - gap)
├── 10-documentation/         # Guides and explanations
├── 11-mental-models/         # Cognitive frameworks (35 models)
└── 99-archive/               # Deprecated content
```

### Folder Number Mapping

| Number | Folder Name | Entity Type | Purpose | Category |
|--------|-------------|-------------|---------|----------|
| 00 | definitions | definition | Framework specs, schemas | reference |
| 01 | agents | agent | Persona-driven executors | executable |
| 02 | skills | skill | Temporary capability containers | executable |
| 03 | tasks | task | Atomic execution units | executable |
| 04 | workflows | workflow | Multi-agent coordination | executable |
| 05 | blueprints | blueprint | Template generators (Python) | generator |
| 06 | rules | rule | Behavioral constraints | constraint |
| 07 | checklists | checklist | Quality gates, validation | validation |
| 08 | automation | automation | Infrastructure scripts | infrastructure |
| 09 | navigation | navigation | Maps, guides, wayfinding | reference |
| 10 | documentation | documentation | Guides, explanations | reference |
| 11 | mental-models | mental-model | Cognitive frameworks | cognitive |
| 99 | archive | (deprecated) | Deprecated content | archive |

### Why This Numbering Convention?

1. **Sort Order**: Numbers ensure consistent directory listing across all systems
2. **Hierarchy**: Lower numbers = more foundational (definitions first, archive last)
3. **Consistency**: Same structure at ALL 4 levels (meta, system, domain, cross-domain)
4. **Progressive Disclosure**: Load by number order reflects dependency order
5. **Entity Type Mapping**: Each folder number corresponds to an entity type definition file

---

## 2. Entity Type Definitions - Complete Schema Patterns

All 12 entity types share a common frontmatter pattern with type-specific extensions.

### 2.1 Universal Frontmatter Fields

Every entity type definition contains these fields:

```yaml
---
# REQUIRED FIELDS
name: {entity-type-name}           # kebab-case identifier
description: {WHAT this entity type does}
when: {WHEN TO USE this entity type}

# FOLDER CONFIGURATION
folder_pattern: "{folder-number}-{folder-name}"  # e.g., "01-agents"
folder_purpose: "{what this folder contains}"
location_pattern: "*/folder-name/**/*.md"        # glob pattern for scanning

# SCANNING CONFIG
scanned: true|false               # Whether registry builder scans this folder

# CLASSIFICATION
category: executable|generator|constraint|validation|reference|infrastructure|cognitive

# METADATA
created: YYYY-MM-DD
updated: YYYY-MM-DD
author: "Human Name | agent-name"
version: X.Y.Z
---
```

### 2.2 Entity Type Categories

The `category` field groups entity types by behavior:

| Category | Entity Types | Behavior |
|----------|-------------|----------|
| **executable** | agent, skill, task, workflow | Can be invoked/executed |
| **generator** | blueprint | Produces output files |
| **constraint** | rule | Governs behavior |
| **validation** | checklist | Quality gates |
| **reference** | definition, navigation, documentation | Information/specs |
| **infrastructure** | automation | System operations |
| **cognitive** | mental-model | Reasoning frameworks |

### 2.3 The 12 Entity Types - Detailed Breakdown

#### Entity 00: Definition
```yaml
name: definition
description: Framework definitions and specifications
when: Need framework definitions, specifications, or architectural reference
folder_pattern: "00-definitions"
category: reference
special_scan: "entity-types/*.md scanned for metadata"
```
**Key Insight**: Self-referential - the definition entity defines what definitions ARE.

#### Entity 01: Agent
```yaml
name: agent
description: Persona-driven executors with specialized expertise
when: Need specialized expertise, autonomous execution, or persona-driven problem-solving
folder_pattern: "01-agents"
category: executable
scanned: true
```
**Unique Fields in Instances**:
- `activation_aliases: [MA, meta, architect]` - Natural language shortcuts
- `agent_scope: ["meta-orchestrator"]` - Which agents can access this agent's executables
- `persona: {description}` - Agent's identity
- `complexity: simple|moderate|complex|expert`

#### Entity 02: Skill
```yaml
name: skill
description: Initial container for capabilities - all info in ONE place before extraction
when: Prototyping new capabilities, understanding before formal extraction
folder_pattern: "02-skills"
category: executable
scanned: true
evolution_note: "Skills are TEMPORARY - extract components to parent structure, delete skill when done"
```
**Unique Fields in Instances**:
- `extraction_status: prototype|ready|extracted`
- `agent_scope: [agent-id-1, agent-id-2]` - OPTIONAL

**Lifecycle**: Create with structure -> Build components -> Extract to parent layer -> Delete

#### Entity 03: Task
```yaml
name: task
description: Single simple atomic units with minimal dependencies
when: Need simple, repeatable execution without complex coordination
folder_pattern: "03-tasks"
category: executable
scanned: true
```
**Unique Fields in Instances**:
- `validation: {success criteria}`
- `agent_scope: [agent-id-1, agent-id-2]` - OPTIONAL

**Structure Pattern**: Step 0 (Load Prerequisites) + Steps 1-N (Execution) + Validation

#### Entity 04: Workflow
```yaml
name: workflow
description: Multi-agent coordination with dependencies and quality gates
when: Need complex multi-step coordination, quality gates, or orchestrated execution
folder_pattern: "04-workflows"
category: executable
scanned: true
```
**Unique Fields in Instances**:
- `complexity: low|medium|high`
- `scope: meta|system|domain|cross-domain`
- `agent_scope: [agent-id-1, agent-id-2]` - OPTIONAL

**Structure Pattern**: Phases with Quality Gates + Transitions + Dependencies

#### Entity 05: Blueprint
```yaml
name: blueprint
description: Python scripts that generate markdown files with TODO templates
when: Need to generate structured output, create templates, or codify patterns
folder_pattern: "05-blueprints"
category: generator
scanned: false
```
**Key Insight**: Blueprints are NEVER executed directly - always called by tasks/workflows/skills.

**Smart Blueprint Pattern**:
```python
# Arguments control generation logic (compress if/else into script)
python agent-generator.py --type orchestrator --layer domain --output path
```

#### Entity 06: Rule
```yaml
name: rule
description: Behavioral constraints extracted from skill patterns
when: Need behavioral constraints, best practices enforcement
folder_pattern: "06-rules"
category: constraint
scanned: false
```
**Unique Fields in Instances**:
- `applies_to: [agents, tasks, workflows, all]`
- `enforcement: strict|recommended|guideline`
- `level: meta|system|domain|cross-domain`

**Loading Pattern**: Rules are ALWAYS hardcoded in executables - never loaded from registry.

**Three Loading Contexts**:
1. **Agent Activation Load**: `dependencies: [~rule:git-workflow]`
2. **Executable Load**: In task/workflow frontmatter
3. **Step-Level Load**: Referenced at specific execution steps

#### Entity 07: Checklist
```yaml
name: checklist
description: Quality gates and validation checklists for checkpoints
when: Need validation gates, quality checkpoints, or structured verification
folder_pattern: "07-checklists"
category: validation
scanned: false
```
**Two Types**:
1. **Manual Checklists** - Human-reviewed quality gates
2. **Evaluation Checklists** - Derived from executables for trace validation

**Unique Fields in Instances**:
- `type: manual|evaluation`
- `checkpoint: phase-transition|before-commit|activation|execution|completion`
- `source_entity: ~{type}:{id}` (for evaluation checklists)
- `derived_by: ~create-evaluation-checklist` (for evaluation checklists)

#### Entity 08: Automation
```yaml
name: automation
description: Infrastructure scripts and tools for system operations
when: Need infrastructure automation, hooks, validators, or system maintenance
folder_pattern: "08-automation"
category: infrastructure
scanned: false
```
**Three Types**:
1. **Hooks** (Event-Triggered): `hooks/` - Git hooks, file watchers, startup events
2. **Scripts** (Manual/On-Demand): `scripts/` - CLI tools, utilities
3. **Tests** (Validation): `tests/` - Test suites

**Docstring Pattern** (PREFERRED - Pattern B):
```python
#!/usr/bin/env python3
"""
---
description: Dynamic context loader - injects behavioral rules
when: Loading command context, injecting behavioral rules
---

Architech Dynamic Context Loader
Version: 1.0.0
"""
```

#### Entity 09: Navigation
```yaml
name: navigation
description: Maps, guides, and wayfinding documents
when: Need to orient, discover, navigate, or understand framework structure
folder_pattern: "09-navigation"
category: reference
scanned: false
```
**Six Navigation Types**:
1. `navigation` - Master framework maps
2. `reference` - Quick lookup materials
3. `index` - Catalogs and directories
4. `graph` - Relationship mapping
5. `map` - Domain/system-specific navigation
6. `hub` - Meta-navigation (navigation to other navigation)

#### Entity 10: Documentation
```yaml
name: documentation
description: Guides, explanations, and reference materials
when: Need how-to guides, concept explanations, or reference documentation
folder_pattern: "10-documentation"
category: reference
scanned: false
```
**Seven Documentation Types**:
1. `guide` - Step-by-step instructions
2. `tutorial` - Progressive learning experiences
3. `reference` - Quick lookup materials
4. `explanation` - Concept and theory
5. `overview` - Big picture summaries
6. `decision-record` - Architectural decisions
7. `visual` - Diagrams and flowcharts

#### Entity 11: Mental Model
```yaml
name: mental-model
description: Cognitive frameworks and problem-solving tools
when: Need cognitive frameworks, reasoning patterns, or structured problem-solving
folder_pattern: "11-mental-models"
category: cognitive
scanned: false
special_note: "Mental models exist at ALL levels - meta, system, domain, cross-domain"
```
**Smart Selection System (v3.0)**:
- **Tier Architecture**: Quick Mode (O(1) lookup) -> Full Mode (YAML parsing) -> Content Mode (full file read)
- **Situation-Based Selection**: 13 situations mapped to recommended models
- **Model Bundles**: Pre-validated combinations (strategic-planning, decision-making, problem-solving, etc.)

**Unique Fields in Instances**:
- `tier: 1|2` (1=core/frequent, 2=situational)
- `applies_to: [Strategy, Build, Process, Research]`
- `complexity: [Simple, Medium, Complex]`
- `triggers: ["phrase 1", "phrase 2"]`
- `anti_triggers: ["phrase to avoid"]`

#### Entity 12: Evaluation
```yaml
name: evaluation
description: Trace evaluation report schema for behavioral validation
when: Validating agent/skill/task execution via trace analysis
folder_pattern: (none - generated reports)
category: validation
```
**Schema Structure**:
```typescript
interface EvaluationReport {
  schema_version: "1.0";
  session_meta: { duration_minutes, event_count, executables, session_type };
  behavioral_validation: { phases: { activation, execution, completion }, overall_score, verdict };
  decision_chains: { chains: DecisionChain[], aggregate: { avg_quality_score, plan_first_rate } };
  content_analysis: { edits, bash, todos, reads, tool_usage, work_type };
  synthesis: { verdict, overall_score, summary, highlights, concerns, recommendations };
}
```

**Verdict Thresholds**:
| Score | Verdict | Criteria |
|-------|---------|----------|
| >= 95 | EXEMPLARY | No failures, all patterns present |
| >= 80 | COMPLIANT | No failures, minor warnings ok |
| >= 60 | MOSTLY_COMPLIANT | No critical failures |
| >= 40 | NEEDS_IMPROVEMENT | Has failures |
| < 40 | FAILED | Critical failures |

---

## 3. Behavioral Flags System

Entity instances use YAML frontmatter flags that trigger dynamic behavior injection.

### 3.1 Core Behavioral Flags

```yaml
---
# INTERACTIVITY FLAGS
interactive: true|false          # Enables user interaction mode
progressive: true|false          # Progressive disclosure pattern

# COGNITIVE FLAGS
cognitive_mode: systems-thinking|first-principles|ULTRATHINK|{model-name}
reasoning: true|false            # Enable extended reasoning
reasoning_modes: [systems-thinking, first-principles]  # Multi-model for workflows

# EXECUTION FLAGS
validation: {success criteria}   # Success/failure detection
enforcement: strict|recommended|guideline  # For rules

# SCOPING FLAGS
agent_scope: [agent-id-1, agent-id-2]  # Which agents can access
level: meta|system|domain|cross-domain  # Framework level

# COMPLEXITY FLAGS
complexity: simple|moderate|complex|expert
---
```

### 3.2 How Flags Drive Behavior

The `context_loader.py` automation reads frontmatter flags and injects behavioral rules dynamically:

```python
# From context_loader.py pattern
def inject_behavioral_rules(frontmatter: dict) -> str:
    """Inject behavioral rules based on frontmatter flags."""
    rules = []

    if frontmatter.get('interactive'):
        rules.append(INTERACTIVE_RULES)

    if frontmatter.get('progressive'):
        rules.append(PROGRESSIVE_DISCLOSURE_RULES)

    if cognitive_mode := frontmatter.get('cognitive_mode'):
        rules.append(load_mental_model(cognitive_mode))

    if frontmatter.get('reasoning'):
        rules.append(EXTENDED_REASONING_RULES)

    return "\n".join(rules)
```

### 3.3 Flag Combinations

| Use Case | Flags |
|----------|-------|
| Interactive Task | `interactive: true, progressive: true` |
| Deep Analysis | `cognitive_mode: ULTRATHINK, reasoning: true` |
| Domain Creation | `cognitive_mode: systems-thinking, interactive: true` |
| Strict Validation | `enforcement: strict, validation: {criteria}` |
| Multi-Model Workflow | `reasoning_modes: [systems-thinking, first-principles]` |

---

## 4. Entity Interrelationships

### 4.1 Dependency Graph

```
                    ┌─────────────────────────────────────────────┐
                    │              DEFINITIONS (00)                │
                    │   Foundation - defines all other types       │
                    └──────────────────┬──────────────────────────┘
                                       │ defines
                    ┌──────────────────┴──────────────────────────┐
                    │                                              │
        ┌───────────▼───────────┐              ┌───────────────────▼────────────┐
        │     AGENTS (01)        │              │         AUTOMATIONS (08)       │
        │  Persona executors     │◄─────────────│      Infrastructure scripts    │
        │  Load context, decide  │   activate   │   Registry, resolver, hooks    │
        └───────────┬───────────┘              └────────────────────────────────┘
                    │ orchestrate
        ┌───────────▼───────────┐
        │    WORKFLOWS (04)      │◄───────── RULES (06) constrain
        │  Multi-agent coord.    │           CHECKLISTS (07) validate gates
        └───────────┬───────────┘
                    │ execute
        ┌───────────▼───────────┐
        │     TASKS (03)         │◄───────── BLUEPRINTS (05) generate
        │   Atomic execution     │           (tasks CALL blueprints)
        └───────────┬───────────┘
                    │ evolve from
        ┌───────────▼───────────┐
        │     SKILLS (02)        │──────────► Extract to: Tasks, Rules, Blueprints
        │   Temp. prototypes     │            then DELETE
        └───────────────────────┘

        MENTAL MODELS (11) ─────► Enhance reasoning at any level
        NAVIGATION (09) ─────────► Orient and discover
        DOCUMENTATION (10) ──────► Explain and teach
        EVALUATION (12) ─────────► Validate execution traces
```

### 4.2 Loading Patterns

**Agent Activation Sequence**:
```bash
1. python build_shortcut_registry.py --agent {agent-id} --mode {plan|exec|discover}
2. python build_entity_definitions.py
3. Read agent file (meta-architect.md)
4. Load agent dependencies (~meta-map, etc.)
5. Display help menu
6. Stay in character until ~exit
```

**Task Execution Pattern**:
```markdown
Step 0: Load All Prerequisites (MANDATORY)
- Load entity definition (~entity:task)
- Load dependencies from frontmatter
- Verify context available

Steps 1-N: Execute
- Follow step-by-step instructions
- Call blueprints if generation needed
- Apply rules at decision points

Validation:
- Check success criteria
- Apply checklists at gates
```

**Workflow Phase Pattern**:
```markdown
Phase N: {Phase Name}
**Goal**: {objective}
**Agent**: {~agent-shortcut}  <- Specific agent executes
**Execution**:
1. Step (agent action)
2. Step (deliverable created)
**Quality Gate**:
- [ ] Criterion 1
- [ ] Criterion 2
**Transition**: PASS -> Phase N+1 | FAIL -> remediation
```

### 4.3 The Skill Evolution Path

Skills are TEMPORARY and follow this lifecycle:

```
┌─────────────────────────────────────────────────────────────────┐
│                  SKILL LIFECYCLE                                 │
└─────────────────────────────────────────────────────────────────┘

CREATION (via init_skill.py)
skill-name/
├── skill-name.md              # Entrypoint + workflow
├── 02-tasks/                  # Add execution tasks here
├── 04-blueprints/             # Add template generators here
├── 05-rules/                  # Add validation rules here
├── 06-checklists/             # Add quality gates here
├── 07-automation/             # Add scripts here
├── 09-documentation/          # Add reference docs here
└── assets/                    # Add output files here

      ↓ When components tested and ready

EXTRACTION (promote to parent layer)
{parent-layer}/
├── 02-tasks/component.md           # Promoted from skill
├── 04-blueprints/template.py       # Promoted from skill
├── 05-rules/validation.md          # Promoted from skill
├── 06-checklists/checklist.md      # Promoted from skill
├── 07-automation/script.py         # Promoted from skill
└── 09-documentation/guide.md       # Promoted from skill

      ↓ After successful promotion

DELETION
skill-name/ -> DELETED (purpose served)
```

---

## 5. Shortcut System - Entity Resolution

### 5.1 Shortcut Naming Conventions

```
~{name}                    # Unique executable (task, workflow, skill)
~entity:{type}             # Entity type definition
~rule:{name}               # Rule reference
~agent:{name}              # Agent reference
~{layer}:{category}:{name} # Disambiguation for collisions
```

### 5.2 Shortcut Registry Build Process

The `build_shortcut_registry.py` script:

1. **Scans** entity-type folders marked `scanned: true`
2. **Extracts** frontmatter: `name`, `description`, `when`, `agent_scope`
3. **Filters** by `--agent` flag (agent-centric architecture v3.0)
4. **Filters** by `--mode` flag (plan|exec|discover)
5. **Outputs** XML format for AI consumption:

```xml
<shortcuts>
  <shortcut>
    <name>create-agent</name>
    <description>Interactive agent creation wizard</description>
    <when>Adding new specialized expertise to the framework</when>
    <entity_type>task</entity_type>
    <path>architech/01-system/03-tasks/create-agent.md</path>
  </shortcut>
  ...
</shortcuts>
```

### 5.3 Mode System (Progressive Disclosure)

| Mode | Purpose | Loads | Context Reduction |
|------|---------|-------|-------------------|
| `plan` | Design, architect, validate | definitions, agents, skills, tasks, workflows, blueprints, rules, checklists, navigation, docs, mental-models | ~40-60% |
| `exec` | Execute work, run tasks | agents, skills, tasks, workflows, navigation only | ~60% |
| `discover` | Learn, explore, understand | definitions, rules, navigation, docs, mental-models | ~60% |

### 5.4 Agent-Centric Architecture (v3.0)

**Old Pattern (v2.x - deprecated)**:
```bash
--layer meta --domain software  # Layer/domain filtering
```

**New Pattern (v3.0)**:
```bash
--agent meta-architect --mode plan  # Agent-centric scoping
```

The agent's `agent_scope` field in frontmatter determines what gets loaded:
```yaml
# In agent frontmatter
agent_scope: [backend-engineer, frontend-developer]  # Only these can access
```

---

## 6. Instance Frontmatter - Complete Schema Reference

### 6.1 Agent Instance

```yaml
---
name: backend-engineer
description: Backend development specialist for APIs, databases, and server-side logic
when: Need backend implementation, API design, database optimization
persona: Pragmatic engineer focused on scalable, maintainable systems
expertise: [api-design, database-optimization, server-architecture, testing]
complexity: expert
activation_aliases: [BE, backend, server]  # Natural language shortcuts
agent_scope: [backend-engineer]            # Executables this agent can access
dependencies: [~task:create-api-endpoint, ~task:optimize-query, ~workflow:deploy-backend]
created: 2025-01-15
updated: 2025-11-20
author: "Dorian | meta-architect"
version: 2.0.0
---
```

### 6.2 Task Instance

```yaml
---
name: create-agent
description: Interactive agent creation wizard that generates complete agent definitions
when: Adding new specialized expertise to the framework
dependencies: [~entity:agent, ~rule:git-workflow]
complexity: moderate
validation: Agent file created, shortcut registered, frontmatter valid
agent_scope: []  # Empty = available to all agents
created: 2025-10-18
updated: 2025-10-24
author: "Dorian | meta-architect"
version: 1.1.0
---
```

### 6.3 Workflow Instance

```yaml
---
name: feature-development-workflow
description: Full feature lifecycle from ideation to deployment
when: Developing product features with cross-functional coordination
complexity: high
scope: domain
dependencies: [~git-workflow, ~ci-cd-pipeline, ~product-owner, ~architect, ~developer]
agent_scope: [product-manager, software-orchestrator]
created: 2025-01-13
updated: 2025-01-13
author: "Bene | product-orchestrator"
version: 1.0.0
---
```

### 6.4 Rule Instance

```yaml
---
name: git-workflow
description: Git collaboration pattern for all Architech work
when: Making any changes to context-store/
applies_to: all
enforcement: strict
level: system
created: 2025-01-14
updated: 2025-01-15
author: "Dorian | meta-architect"
version: 1.0.0
---
```

### 6.5 Skill Instance

```yaml
---
name: campaign-creation-skill
description: End-to-end marketing campaign creation with templates, validation, and automation
when: Launching product campaigns, seasonal promotions, email marketing initiatives
extraction_status: ready  # prototype|ready|extracted
dependencies: [~email-specialist, ~social-media-manager]
complexity: moderate
agent_scope: [content-writer, marketing-orchestrator]
created: 2025-08-15
updated: 2025-11-15
author: "Dorian | marketing-orchestrator"
---
```

### 6.6 Mental Model Instance

```yaml
---
name: first-principles-thinking
description: Break down problems to fundamental truths and rebuild solutions
tier: 1                                    # 1=core, 2=situational
applies_to: [Strategy, Build, Process, Research]
complexity: [Simple, Medium, Complex]
category: cognitive
level: universal
triggers:
  - "stuck on a problem"
  - "need fresh perspective"
  - "challenge assumptions"
anti_triggers:
  - "quick fix needed"
  - "routine task"
created: 2025-01-10
author: "Dorian | meta-architect"
---
```

---

## 7. Key Code Patterns

### 7.1 Cross-Platform Compatibility

Every automation script that outputs Unicode MUST import platform_compat.py:

```python
import sys
from pathlib import Path

# Platform compatibility - auto-fixes encoding on import
sys.path.insert(0, str(Path(__file__).parent.parent))
from platform_compat import *  # noqa: F401, F403
```

**Location**: `architech/01-system/08-automation/hooks/platform_compat.py`

### 7.2 Root Path Resolution Pattern

```python
@staticmethod
def _resolve_root_path(root_path: str) -> Path:
    """Intelligently resolve the root path by searching for 'architech' folder."""
    root = Path(root_path)

    # Strategy 1: Try provided path as-is
    if (root / "architech").exists():
        return root

    # Strategy 2: Check current directory
    cwd = Path.cwd()
    if (cwd / "architech").exists():
        return cwd

    # Strategy 3: Search upward (max 5 levels)
    current = cwd
    for _ in range(5):
        if (current / "architech").exists():
            return current
        parent = current.parent
        if parent == current:
            break
        current = parent

    return root
```

### 7.3 Frontmatter Extraction Pattern

```python
import yaml

def extract_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')

    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}
```

### 7.4 Entity Definition XML Generation

```python
def generate_entity_xml(entities: List[dict]) -> str:
    """Generate XML for entity definitions."""
    xml_parts = ['<entities>']

    for entity in sorted(entities, key=lambda x: x.get('name', '')):
        xml_parts.append(f'''
  <entity>
    <name>{entity['name']}</name>
    <description>{entity['description']}</description>
    <when>{entity.get('when', '')}</when>
    <purpose>{entity.get('folder_purpose', '')}</purpose>
    <location>{entity['location']}</location>
  </entity>''')

    xml_parts.append('\n</entities>')
    return '\n'.join(xml_parts)
```

---

## 8. Design Principles - Critical Insights

### 8.1 Observer vs Operator

**The Fundamental Question**: "Does this OBSERVE the system or OPERATE within it?"

- **OBSERVE** -> `00-meta/` (definitions, analysis, architectural observation)
- **OPERATE** -> `01-system/` (execution, runtime operations)

### 8.2 No Duplication Policy

**Core Principle**: NEVER duplicate distributed knowledge in centralized documents.

**Violations**:
- Copying entity type tables into documents
- Listing all 11 entity types inline
- Repeating folder structure explanations

**Correct Patterns**:
- Reference via shortcuts: `~entity:agent`
- Point to source: "See shortcut registry"
- Load on-demand: Use shortcuts

### 8.3 Progressive Disclosure

**How It Works**: Through scripts and YAML frontmatter containing metadata that gets pulled automatically.

**Bootstrap Bundle** (always loaded on activation):
1. Agent definition (meta-architect.md)
2. Entity metadata scan
3. Shortcut registry build
4. Navigation map (meta-map.md)

**Everything Else**: Loaded on-demand when needed.

### 8.4 Context is a Public Good

From Claude Skill System philosophy:
- Only add context that isn't already known
- Challenge each piece: "Does this really need to be documented?"
- Default assumption: Claude is already very smart
- Prefer concise examples over verbose explanations

---

## 9. Implementation Recommendations for Strategy Nexus

### 9.1 Core Entity Types to Implement First

1. **definition** - Foundation for all others
2. **agent** - Primary executors
3. **task** - Atomic execution units
4. **skill** - Prototyping containers

### 9.2 Simplified Folder Structure

```
03-skills/                 # Start with skills (temporary containers)
├── {skill-name}/
│   ├── SKILL.md          # Main entrypoint
│   ├── scripts/          # Automation (07-automation equivalent)
│   └── references/       # Documentation (10-documentation equivalent)
```

### 9.3 Essential Frontmatter Fields

For Strategy Nexus, start with:
```yaml
---
name: {kebab-case}
description: {what this does}
when: {when to use}
version: {X.Y.Z}
---
```

Add complexity gradually:
- `agent_scope` when agent isolation is needed
- `extraction_status` for skills
- `cognitive_mode` when mental model integration is desired

### 9.4 Key Automation Scripts to Port

1. `build_shortcut_registry.py` - Core discovery mechanism
2. `shortcut_resolver.py` - Dynamic resolution
3. `platform_compat.py` - Cross-platform encoding
4. `build_entity_definitions.py` - Entity catalog

---

## 10. Version History for Entity Definitions

| Entity | Current Version | Key Updates |
|--------|-----------------|-------------|
| definition | 2.1.0 | Multi-layer examples, self-referential clarity |
| agent | 4.1.0 | Simplified activation, natural language aliases |
| skill | 4.2.0 | Single-phase evolution, init_skill.py integration |
| task | 2.1.0 | Step 0 mandatory, agent_scope field |
| workflow | 2.1.0 | Phase structure, quality gates |
| blueprint | 2.0.0 | Python-only (no .yaml/.md templates), smart arguments |
| rule | 2.0.0 | Hardcoded loading pattern, enforcement levels |
| checklist | 2.1.0 | Evaluation checklist type for trace validation |
| automation | 3.2.0 | 6 docstring patterns, meta vs system distinction |
| navigation | 2.0.0 | 6 navigation types, frontmatter schema |
| documentation | 3.0.0 | 7 documentation types |
| mental-model | 3.0.0 | Smart selection, triggers, bundles |
| evaluation | 1.0.0 | Trace analysis schema |

---

**Extraction Complete**

This document provides the complete architecture of the 01-SYSTEM layer Entity System, including:
- All 12 numbered folders and their purposes
- Complete entity type definitions with frontmatter schemas
- Behavioral flags and their runtime injection
- Entity interrelationships and loading patterns
- Shortcut system and resolution
- Code patterns for implementation
- Design principles (Observer vs Operator, No Duplication, Progressive Disclosure)
- Implementation recommendations for Strategy Nexus

This extraction enables Project 15: Nexus Entity System Implementation.
