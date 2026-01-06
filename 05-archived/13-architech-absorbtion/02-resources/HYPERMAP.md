# ARCHITECH ULTRA-DETAILED HYPERMAP

**Generated**: 2025-12-31
**Purpose**: Complete cross-referenced documentation of the Architech framework
**Coverage**: All entity types, agents, skills, automation, mental models, domains

---

## TABLE OF CONTENTS

1. [Framework Architecture](#1-framework-architecture)
2. [Entity Type System (12 Types)](#2-entity-type-system-12-types)
3. [Agent Registry](#3-agent-registry)
4. [Skill Registry](#4-skill-registry)
5. [Automation System](#5-automation-system)
6. [Mental Model System](#6-mental-model-system)
7. [Domain Layer Status](#7-domain-layer-status)
8. [Dependency Graph](#8-dependency-graph)
9. [Cross-Reference Index](#9-cross-reference-index)

---

## 1. FRAMEWORK ARCHITECTURE

### 1.1 Four-Layer Hierarchy

```
architech/
├── 00-meta/           # OBSERVER LAYER - Framework-about-framework
│   ├── 01-agents/     # Meta agents (meta-architect, trace-analyst, etc.)
│   ├── 02-skills/     # Meta skills (create-project, create-skill, etc.)
│   ├── 09-navigation/ # Framework maps (meta-map, architecture-map)
│   └── 20-project-management/  # Framework evolution projects
│
├── 01-system/         # OPERATOR LAYER - Universal building blocks
│   ├── 00-definitions/    # Entity type definitions (12 types)
│   ├── 02-skills/         # System skills (diagnose-trace)
│   ├── 03-tasks/          # System tasks
│   ├── 08-automation/     # All Python automation (27+ scripts)
│   ├── 10-documentation/  # System documentation
│   └── 11-mental-models/  # Universal mental models (30+)
│
├── 02-domains/        # DOMAIN LAYER - Business domain frameworks
│   ├── 01-strategy/
│   ├── 02-product/
│   ├── 03-software/   # Only populated domain (73 entities)
│   ├── 04-finance/
│   ├── 05-marketing/
│   ├── 06-operations/
│   └── 07-sales/
│
└── 03-cross-domain/   # CROSS-DOMAIN LAYER - Shared systems
    └── 10-project-management/
```

### 1.2 Core Philosophy

- **Progressive Disclosure**: Load context only when needed
- **Entity-Driven**: Everything is an entity with frontmatter metadata
- **Shortcut-Based**: `~shortcut` navigation system
- **Agent-Centric**: v3.0 architecture with `--agent {id} --mode {plan|exec|discover}`
- **Self-Evolving**: Framework observes and improves itself

---

## 2. ENTITY TYPE SYSTEM (12 Types)

### 2.1 Entity Type Overview Table

| # | Entity | Folder | Purpose | Category | Version | Status |
|---|--------|--------|---------|----------|---------|--------|
| 00 | [Definition](#definition) | `00-definitions/` | Framework specifications | reference | v2.1.0 | ✅ 95% |
| 01 | [Agent](#agent) | `01-agents/` | Persona-driven executors | executable | v4.1.0 | ✅ 90% |
| 02 | [Skill](#skill) | `02-skills/` | Temporary capability containers | executable | v4.2.0 | ✅ 85% |
| 03 | [Task](#task) | `03-tasks/` | Atomic execution units | executable | v2.1.0 | ✅ 85% |
| 04 | [Workflow](#workflow) | `04-workflows/` | Multi-agent coordination | executable | v2.1.0 | ⚠️ 80% |
| 05 | [Blueprint](#blueprint) | `05-blueprints/` | Python template generators | generator | v2.0.0 | ⚠️ 75% |
| 06 | [Rule](#rule) | `06-rules/` | Behavioral constraints | constraint | v2.0.0 | ✅ 85% |
| 07 | [Checklist](#checklist) | `07-checklists/` | Quality gates | validation | v2.1.0 | ✅ 85% |
| 08 | [Automation](#automation) | `08-automation/` | Infrastructure scripts | infrastructure | v3.2.0 | ✅ 90% |
| 09 | [Navigation](#navigation) | `09-navigation/` | Maps and wayfinding | reference | v2.0.0 | ⚠️ 70% |
| 10 | [Documentation](#documentation) | `10-documentation/` | Guides and references | reference | v3.0.0 | ⚠️ 70% |
| 11 | [Mental Model](#mental-model) | `11-mental-models/` | Cognitive frameworks | cognitive | v3.0.0 | ✅ 90% |
| 12 | [Evaluation](#evaluation) | `07-checklists/evaluation/` | Trace analysis reports | validation | v1.0.0 | 🆕 New |

---

### 2.2 Entity Type Deep Dive

#### DEFINITION
**Location**: [architech/01-system/00-definitions/entity-types/00-definition.md](architech/01-system/00-definitions/entity-types/00-definition.md)
**Shortcut**: `~entity:definition`
**Purpose**: Framework specifications and architectural reference documents
**Key Insight**: Self-referential "bootstrap" entity - defines what definitions ARE
**Scanned**: Yes (for metadata)
**Multi-Layer**: Exists at meta, system, domain, AND cross-domain levels

**When to Use**:
- ✅ Defining framework structure or patterns
- ✅ Creating entity type specifications
- ✅ Establishing architectural standards
- ❌ NOT for how-to guides (use Documentation)
- ❌ NOT for behavioral constraints (use Rule)

---

#### AGENT
**Location**: [architech/01-system/00-definitions/entity-types/01-agent.md](architech/01-system/00-definitions/entity-types/01-agent.md)
**Shortcut**: `~entity:agent`
**Purpose**: Persona-driven executors with specialized expertise
**Activation**: Natural language via aliases (e.g., "MA" → meta-architect)
**Modes**: `plan` | `exec` | `discover`

**Agent Types**:
| Type | Description | Example |
|------|-------------|---------|
| Orchestrator | Coordinates multiple agents | meta-architect, domain-orchestrator |
| Specialized | Deep expertise in single area | backend-engineer, content-writer |
| Meta | Framework observation | trace-analyst, trace-aggregator |

**Frontmatter Fields**:
```yaml
name: {kebab-case}
description: {role + expertise}
when: {trigger scenarios}
scope_type: orchestrator|specialized|utility
activation_aliases: [MA, meta, architect]
complexity: simple|moderate|expert
color: purple|blue|green|orange|cyan
```

---

#### SKILL
**Location**: [architech/01-system/00-definitions/entity-types/02-skill.md](architech/01-system/00-definitions/entity-types/02-skill.md)
**Shortcut**: `~entity:skill`
**Purpose**: Temporary capability containers with numbered folders
**Philosophy**: "The context window is a public good" (Claude Skill System)

**Lifecycle**:
```
CREATION (init_skill.py)
    ↓
skill-name/
├── skill-name.md      # Entrypoint
├── 02-tasks/          # Execution procedures
├── 04-blueprints/     # Template generators
├── 05-rules/          # Behavioral constraints
├── 06-checklists/     # Quality gates
├── 07-automation/     # Infrastructure scripts
├── 09-documentation/  # Reference docs
└── assets/            # Output files
    ↓
EXTRACTION (to parent layer)
    ↓
DELETION (purpose served)
```

**Extraction Status**: `prototype` → `ready` → `extracted`

---

#### TASK
**Location**: [architech/01-system/00-definitions/entity-types/03-task.md](architech/01-system/00-definitions/entity-types/03-task.md)
**Shortcut**: `~entity:task`
**Purpose**: Single, simple, atomic units of execution

**Characteristics**:
- ✅ Atomic - One clear purpose
- ✅ Simple - Straightforward execution
- ✅ Repeatable - Consistent results
- ✅ Minimal Dependencies

**Task vs Other Entities**:
| Use Task | Don't Use Task |
|----------|---------------|
| Clear steps | Complex decisions (→ Agent) |
| Single executor | Multi-agent (→ Workflow) |
| Proven approach | Experimental (→ Skill) |
| Execution | Template generation (→ Blueprint) |

---

#### WORKFLOW
**Location**: [architech/01-system/00-definitions/entity-types/04-workflow.md](architech/01-system/00-definitions/entity-types/04-workflow.md)
**Shortcut**: `~entity:workflow`
**Purpose**: Multi-agent coordination with phases and quality gates

**Structure**:
```
Phase 1 → Quality Gate → Phase 2 → Quality Gate → Phase N
   ↓           ↓            ↓           ↓           ↓
 Agent A    Validate     Agent B    Validate    Complete
```

**Key Fields**:
```yaml
complexity: low|medium|high
scope: meta|system|domain|cross-domain
agent_scope: [agent-1, agent-2]  # Which agents can access
```

---

#### BLUEPRINT
**Location**: [architech/01-system/00-definitions/entity-types/05-blueprint.md](architech/01-system/00-definitions/entity-types/05-blueprint.md)
**Shortcut**: `~entity:blueprint`
**Purpose**: Python scripts that generate markdown files with TODO templates

**Critical Pattern**: Blueprints are NEVER executed directly - always wrapped by tasks
```bash
# WRONG
python agent-generator.py --output path/to/agent.md

# CORRECT (via task)
*create-agent → calls agent-generator.py → provides editing guidance
```

**Blueprint Types**:
| Type | Output | Example |
|------|--------|---------|
| Single File | One .md file | agent-generator.py |
| Multi-File | Entire folder structure | domain-generator.py, project-generator.py |

---

#### RULE
**Location**: [architech/01-system/00-definitions/entity-types/06-rule.md](architech/01-system/00-definitions/entity-types/06-rule.md)
**Shortcut**: `~entity:rule`
**Purpose**: Behavioral constraints that define how to behave, not what to execute

**Loading Patterns**:
| Context | Where | When |
|---------|-------|------|
| Agent Activation | `dependencies: [~rule:git-workflow]` | ALL agent operations |
| Executable Load | Task/workflow frontmatter | Entire executable |
| Step-Level | Specific step reference | Just that step |

**Enforcement Levels**:
| Level | Meaning | Example |
|-------|---------|---------|
| `strict` | MUST comply, blocks if violated | git-workflow |
| `recommended` | SHOULD comply, warns | semantic-versioning |
| `guideline` | MAY comply, suggests | documentation-style |

---

#### CHECKLIST
**Location**: [architech/01-system/00-definitions/entity-types/07-checklist.md](architech/01-system/00-definitions/entity-types/07-checklist.md)
**Shortcut**: `~entity:checklist`
**Purpose**: Quality gates and validation at specific checkpoints

**Two Types**:
| Type | Created By | Used For |
|------|-----------|----------|
| Manual | Human authoring | Pre-commit, releases |
| Evaluation | `~create-evaluation-checklist` | Trace validation |

**Evaluation Checklist Pipeline**:
```
Executable (agent/skill/task/workflow)
    ↓ ~create-evaluation-checklist
Evaluation Checklist (.md)
    ↓ ~diagnose-trace (loads sequentially)
Validation Report
```

---

#### AUTOMATION
**Location**: [architech/01-system/00-definitions/entity-types/08-automation.md](architech/01-system/00-definitions/entity-types/08-automation.md)
**Shortcut**: `~entity:automation`
**Purpose**: Infrastructure scripts and tools (Python/Shell)

**Types**:
| Type | Location | Trigger |
|------|----------|---------|
| Hooks | `08-automation/hooks/` | Event-triggered |
| Scripts | `08-automation/scripts/` | Manual/on-demand |
| Tests | `08-automation/tests/` | Validation |

**Current Stats**: 27 Python files, 150+ tests, 8,000+ LOC

---

#### NAVIGATION
**Location**: [architech/01-system/00-definitions/entity-types/09-navigation.md](architech/01-system/00-definitions/entity-types/09-navigation.md)
**Shortcut**: `~entity:navigation`
**Purpose**: Maps, guides, and wayfinding documents

**Navigation Types**:
| Type | Purpose | Example |
|------|---------|---------|
| `navigation` | Master framework maps | meta-map.md |
| `reference` | Quick lookup | architecture-map.md |
| `index` | Entity catalogs | entity-type-index |
| `graph` | Relationship mapping | workflow-dependency-map |
| `map` | Domain-specific | software-domain-map |
| `hub` | Meta-navigation | framework-map.md |

---

#### DOCUMENTATION
**Location**: [architech/01-system/00-definitions/entity-types/10-documentation.md](architech/01-system/00-definitions/entity-types/10-documentation.md)
**Shortcut**: `~entity:documentation`
**Purpose**: Guides, explanations, and reference materials

**Types**:
- `guide` - Step-by-step instructions
- `tutorial` - Progressive learning
- `reference` - Quick lookup
- `explanation` - Concept deep dives
- `overview` - Big picture summaries
- `decision-record` - ADRs
- `visual` - Diagrams, flowcharts

---

#### MENTAL MODEL
**Location**: [architech/01-system/00-definitions/entity-types/11-mental-model.md](architech/01-system/00-definitions/entity-types/11-mental-model.md)
**Shortcut**: `~entity:mental-model`
**Purpose**: Cognitive frameworks with smart selection

**Smart Selection System**:
```
User Query
    ↓
QUICK MODE (O(1) lookup via SITUATION_MODELS)
    ↓
FULL MODE (YAML parsing, trigger matching)
    ↓
CONTENT MODE (Full file read on demand)
```

**8 Categories**: cognitive, strategic, creative, diagnostic, validation, collaborative, meta-cognitive, ai-reasoning

**30+ Models**: first-principles, systems-thinking, design-thinking, pre-mortem, SCAMPER, etc.

---

#### EVALUATION
**Location**: [architech/01-system/00-definitions/entity-types/12-evaluation.md](architech/01-system/00-definitions/entity-types/12-evaluation.md)
**Shortcut**: `~entity:evaluation`
**Purpose**: Trace analysis report schema

**Schema Components**:
- `behavioral_validation` - From trace-behavioral-validator
- `decision_chains` - From trace-decision-analyzer
- `content_analysis` - From trace-content-analyzer
- `synthesis` - Orchestrator verdict

**Scoring Formula**:
```
Overall = (Activation × 0.30) + (Execution × 0.40) + (Completion × 0.30)
```

**Verdicts**: EXEMPLARY (≥95) | COMPLIANT (≥80) | MOSTLY_COMPLIANT (≥60) | NEEDS_IMPROVEMENT (≥40) | FAILED (<40)

---

## 3. AGENT REGISTRY

### 3.1 Active Agents Overview

| Agent | Version | Status | Aliases | Scope |
|-------|---------|--------|---------|-------|
| [meta-architect](#meta-architect) | v2.8.0 | ✅ PROD | MA, meta, architect, hi, hello | orchestrator |
| [trace-analyst](#trace-analyst) | v3.1.0 | ✅ PROD | analyze-trace, analyze, diagnose | utility |
| [trace-aggregator](#trace-aggregator) | v1.0.0 | ✅ PROD | aggregate-traces, agent-health | utility |
| [bootstrap](#bootstrap) | designed | 🔧 Design | bootstrap | meta |

---

### 3.2 Agent Deep Dive

#### META-ARCHITECT
**Location**: [architech/00-meta/01-agents/meta-architect/current/meta-architect.md](architech/00-meta/01-agents/meta-architect/current/meta-architect.md)
**Shortcut**: `~meta-architect` or `~agent:meta-architect`
**Icon**: 🏛️🔬🌌
**Color**: Purple
**Role**: Meta-Level System Architect & Knowledge Vacuum

**Core Principles**:
1. CONTEXT IS EVERYTHING
2. OBSERVER ONLY - Never modify existing components
3. BLACK HOLE VACUUM - Extract every pattern
4. SOCRATIC GUIDANCE - Lead with questions
5. DEVIL'S ADVOCATE - Pushback on harmful changes
6. SELF-EVOLUTION - Continuously improve

**Activation**:
```bash
python build_shortcut_registry.py --agent meta-architect --mode plan
python build_entity_definitions.py
echo "meta-architect" > .claude/current_agent.txt
# Then: Load ~meta-map, display ~help
```

**Memory Structure**:
```
meta-architect/
├── current/meta-architect.md    # Active version
├── evolution/                   # Version history (v1.0-v1.4)
├── evolution-log.md             # Change tracking
├── memory/
│   ├── extraction-logs/         # Pattern extractions
│   ├── pattern-analysis/        # Behavioral patterns
│   ├── synthesis/               # Compacted learnings
│   ├── framework-evolution.md
│   ├── global-learnings.md
│   └── vacuum-state.md
└── suggestions/                 # Improvement ideas
```

---

#### TRACE-ANALYST
**Location**: [architech/00-meta/01-agents/trace-analyst/trace-analyst.md](architech/00-meta/01-agents/trace-analyst/trace-analyst.md)
**Shortcut**: `~trace-analyst`
**Icon**: 🔍
**Color**: Cyan
**Role**: Multi-agent trace analysis orchestrator

**Core Insight**: "The reports are not for humans. They are for AI."

**Subagent Architecture**:
```
trace-analyst (orchestrator)
    ├── trace-behavioral-validator  # Phase validation
    ├── trace-decision-analyzer     # Reasoning flow analysis
    └── trace-content-analyzer      # Deep content examination
```

**Skills**:
- [export-trace](architech/00-meta/01-agents/trace-analyst/02-skills/export-trace/export-trace.md)
- [detect-executable](architech/00-meta/01-agents/trace-analyst/02-skills/detect-executable/detect-executable.md)
- [resolve-checklist](architech/00-meta/01-agents/trace-analyst/02-skills/resolve-checklist/resolve-checklist.md)
- [validate-against-checklist](architech/00-meta/01-agents/trace-analyst/02-skills/validate-against-checklist/validate-against-checklist.md)
- [generate-report](architech/00-meta/01-agents/trace-analyst/02-skills/generate-report/generate-report.md)

---

#### TRACE-AGGREGATOR
**Location**: [architech/00-meta/01-agents/trace-aggregator/trace-aggregator.md](architech/00-meta/01-agents/trace-aggregator/trace-aggregator.md)
**Shortcut**: `~trace-aggregator`
**Icon**: 📊
**Color**: Orange
**Role**: Cross-session pattern discovery

**Pipeline**:
```
Query Evaluations → Aggregate Metrics → Analyze Patterns → Generate Health Report
```

**Skills**:
- [query-evaluations](architech/00-meta/01-agents/trace-aggregator/02-skills/query-evaluations/query-evaluations.md)
- [aggregate-metrics](architech/00-meta/01-agents/trace-aggregator/02-skills/aggregate-metrics/aggregate-metrics.md)
- [generate-health-report](architech/00-meta/01-agents/trace-aggregator/02-skills/generate-health-report/generate-health-report.md)

---

## 4. SKILL REGISTRY

### 4.1 Meta-Layer Skills

| Skill | Status | Automation | Location |
|-------|--------|------------|----------|
| [create-project](architech/00-meta/02-skills/create-project/create-project.md) | ✅ Ready | `init_project.py` | 00-meta/02-skills/ |
| [create-skill](architech/00-meta/02-skills/create-skill/create-skill.md) | ✅ Ready | `init_skill.py` | 00-meta/02-skills/ |
| [execute-project](architech/00-meta/02-skills/execute-project/execute-project.md) | ✅ Ready | Manual | 00-meta/02-skills/ |
| [mental-models](architech/00-meta/02-skills/mental-models/mental-models.md) | ✅ Ready | `select_mental_models.py` | 00-meta/02-skills/ |
| [bulk-complete](architech/00-meta/02-skills/bulk-complete/bulk-complete.md) | ✅ Ready | Manual | 00-meta/02-skills/ |
| [archive-project](architech/00-meta/02-skills/archive-project/archive-project.md) | ⚠️ Prototype | Manual | 00-meta/02-skills/ |
| [validate-system](architech/00-meta/02-skills/validate-system/validate-system.md) | ⚠️ Prototype | Manual | 00-meta/02-skills/ |
| [validate-docs-implementation](architech/00-meta/02-skills/validate-docs-implementation/validate-docs-implementation.md) | ⚠️ Prototype | Manual | 00-meta/02-skills/ |
| [validate-workspace-map](architech/00-meta/02-skills/validate-workspace-map/validate-workspace-map.md) | ⚠️ Prototype | Manual | 00-meta/02-skills/ |
| [migrate-nexus](architech/00-meta/02-skills/migrate-nexus/migrate-nexus.md) | ✅ Ready | Manual | 00-meta/02-skills/ |
| [skip-onboarding](architech/00-meta/02-skills/skip-onboarding/skip-onboarding.md) | ✅ Ready | Manual | 00-meta/02-skills/ |
| [bridge-to-agent-tracer](architech/00-meta/02-skills/bridge-to-agent-tracer/bridge-to-agent-tracer.md) | 🆕 New | Manual | 00-meta/02-skills/ |

### 4.2 System-Layer Skills

| Skill | Status | Location |
|-------|--------|----------|
| [diagnose-trace](architech/01-system/02-skills/diagnose-trace) | ✅ Ready | 01-system/02-skills/ |

---

## 5. AUTOMATION SYSTEM

### 5.1 Automation Overview

**Total Files**: 27 Python scripts
**Test Coverage**: 150+ test cases
**Subsystems**: 5 major subsystems

### 5.2 Subsystem Map

#### SHORTCUT SYSTEM (`hooks/shortcut_system/`)
The core navigation system for Architech.

| Script | Lines | Purpose |
|--------|-------|---------|
| [build_shortcut_registry.py](architech/01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py) | ~1,000 | Builds registry from frontmatter |
| [shortcut_resolver.py](architech/01-system/08-automation/hooks/shortcut_system/shortcut_resolver.py) | ~800 | Resolves `~shortcut` to file paths |
| [context_loader.py](architech/01-system/08-automation/hooks/shortcut_system/context_loader.py) | ~200 | Dynamic context injection |
| [help_generator.py](architech/01-system/08-automation/hooks/shortcut_system/help_generator.py) | ~150 | Generates help menus |

**Key Feature**: 2-tier cascade architecture
- Base registry: `00-architech` (loaded at session start)
- Domain registries: Loaded on-demand

#### AGENT SYSTEM (`hooks/agent_system/`)

| Script | Purpose |
|--------|---------|
| [activate_agent.py](architech/01-system/08-automation/hooks/agent_system/activate_agent.py) | Agent activation via alias resolution |

#### ENTITY SYSTEM (`hooks/entity_system/`)

| Script | Purpose |
|--------|---------|
| [build_entity_definitions.py](architech/01-system/08-automation/hooks/entity_system/build_entity_definitions.py) | XML entity definitions builder |

#### MENTAL MODELS (`scripts/mental_models/`)

| Script | Lines | Purpose |
|--------|-------|---------|
| [select_mental_models.py](architech/01-system/08-automation/scripts/mental_models/select_mental_models.py) | ~500 | Situation-aware model selection |
| [mental_model_loader.py](architech/01-system/08-automation/scripts/mental_models/mental_model_loader.py) | ~300 | Bundle loading, recommendations |

#### SKILL SYSTEM (`scripts/skill_system/`)

| Script | Purpose |
|--------|---------|
| [init_skill.py](architech/01-system/08-automation/scripts/skill_system/init_skill.py) | Creates skill folder structure |

#### PROJECT SYSTEM (`scripts/project_system/`)

| Script | Purpose |
|--------|---------|
| [track_progress.py](architech/01-system/08-automation/scripts/project_system/track_progress.py) | Project progress tracking |

#### VALIDATORS (`scripts/`)

| Script | Purpose |
|--------|---------|
| [validate_frontmatter.py](architech/01-system/08-automation/scripts/validate_frontmatter.py) | YAML frontmatter validation |
| [validate_registry_integrity.py](architech/01-system/08-automation/scripts/validate_registry_integrity.py) | Registry consistency checks |
| [validate_wikilinks.py](architech/01-system/08-automation/scripts/validate_wikilinks.py) | Wikilink resolution validation |
| [context_bundler.py](architech/01-system/08-automation/scripts/context_bundler.py) | Context bundle generation |

#### INFRASTRUCTURE (`hooks/`)

| Script | Purpose |
|--------|---------|
| [platform_compat.py](architech/01-system/08-automation/hooks/platform_compat.py) | Cross-platform encoding fix (Unicode) |
| [git_commit_tracker.py](architech/01-system/08-automation/hooks/git_commit_tracker.py) | Git commit tracking |

### 5.3 Test Suite

| Test File | Tests | Coverage |
|-----------|-------|----------|
| test_build_shortcut_registry.py | 25+ | ~70% |
| test_select_mental_models.py | 15+ | ~80% |
| test_entity_definitions.py | 10+ | ~75% |
| test_architech_loader.py | 10+ | ~70% |
| hooks/test_*.py | 50+ | Various |

**Test Runner**: [run_all_tests.py](architech/01-system/08-automation/tests/run_all_tests.py)

---

## 6. MENTAL MODEL SYSTEM

### 6.1 Overview

**Total Models**: 30+
**Categories**: 8
**Selection Scripts**: 2 (`select_mental_models.py`, `mental_model_loader.py`)

### 6.2 Categories & Models

#### COGNITIVE (4 models)
- [first-principles](architech/01-system/11-mental-models/first-principles.md)
- [systems-thinking](architech/01-system/11-mental-models/systems-thinking.md)
- [analogical-reasoning](architech/01-system/11-mental-models/analogical-reasoning.md)
- [lateral-thinking](architech/01-system/11-mental-models/lateral-thinking.md)

#### STRATEGIC (5 models)
- [scenario-planning](architech/01-system/11-mental-models/scenario-planning.md)
- [ooda-loop](architech/01-system/11-mental-models/ooda-loop.md)
- [jobs-to-be-done](architech/01-system/11-mental-models/jobs-to-be-done.md)
- [working-backwards](architech/01-system/11-mental-models/working-backwards.md)
- [second-order-thinking](architech/01-system/11-mental-models/second-order-thinking.md)

#### CREATIVE (3 models)
- [design-thinking](architech/01-system/11-mental-models/design-thinking.md)
- [scamper](architech/01-system/11-mental-models/scamper.md)
- [lateral-thinking](architech/01-system/11-mental-models/lateral-thinking.md)

#### DIAGNOSTIC (3 models)
- [root-cause-analysis](architech/01-system/11-mental-models/root-cause-analysis.md)
- [pre-mortem](architech/01-system/11-mental-models/pre-mortem.md)
- [after-action-review](architech/01-system/11-mental-models/after-action-review.md)

#### VALIDATION (3 models)
- [hypothesis-testing](architech/01-system/11-mental-models/hypothesis-testing.md)
- [confidence-calibration](architech/01-system/11-mental-models/confidence-calibration.md)
- [cognitive-biases](architech/01-system/11-mental-models/cognitive-biases.md)

#### COLLABORATIVE (3 models)
- [six-thinking-hats](architech/01-system/11-mental-models/six-thinking-hats.md)
- [devils-advocate](architech/01-system/11-mental-models/devils-advocate.md)
- [steel-man](architech/01-system/11-mental-models/steel-man.md)
- [stakeholder-mapping](architech/01-system/11-mental-models/stakeholder-mapping.md)

#### OPERATIONAL (4 models)
- [task-decomposition](architech/01-system/11-mental-models/task-decomposition.md)
- [eisenhower-matrix](architech/01-system/11-mental-models/eisenhower-matrix.md)
- [constraint-analysis](architech/01-system/11-mental-models/constraint-analysis.md)
- [inversion](architech/01-system/11-mental-models/inversion.md)

#### META-COGNITIVE (3 models)
- [decision-matrix](architech/01-system/11-mental-models/decision-matrix.md)
- [opportunity-cost](architech/01-system/11-mental-models/opportunity-cost.md)
- [expected-value-thinking](architech/01-system/11-mental-models/expected-value-thinking.md)

### 6.3 Situation Mapping

| Situation | Recommended Models |
|-----------|-------------------|
| `starting` | Jobs to Be Done, First Principles, Stakeholder Mapping |
| `stuck` | Lateral Thinking, Inversion, Constraint Analysis |
| `deciding` | Expected Value, Opportunity Cost, Decision Matrix |
| `disagreement` | Six Thinking Hats, Steel Man, Socratic |
| `failure` | Root Cause Analysis, After-Action Review |
| `improving` | SCAMPER, Systems Thinking, Pareto |
| `creative` | Design Thinking, SCAMPER, Lateral, Analogical |
| `debugging` | Root Cause, Hypothesis Testing, Task Decomposition |
| `risk` | Pre-Mortem, Inversion, Devil's Advocate |

### 6.4 Model Bundles

| Bundle | Use Case | Models |
|--------|----------|--------|
| `strategic-planning` | Major decisions | First Principles → Jobs to Be Done → Pre-Mortem → Second-Order |
| `decision-making` | Choosing options | Decision Matrix → Expected Value → Inversion → Opportunity Cost |
| `problem-solving` | Stuck/breakthrough | Root Cause → Constraint Analysis → Lateral Thinking |
| `risk-assessment` | High-stakes | Pre-Mortem → Inversion → Scenario Planning |
| `innovation` | Creating new | Jobs to Be Done → SCAMPER → Analogical |
| `team-alignment` | Multiple stakeholders | Stakeholder Mapping → Six Hats → Steel Man |
| `ultrathink` | Deep analysis | First Principles → Systems Thinking → Inversion → Model Combinations |

---

## 7. DOMAIN LAYER STATUS

### 7.1 Domain Overview

| Domain | Path | Status | Entities |
|--------|------|--------|----------|
| 01-strategy | `02-domains/01-strategy/` | 🔴 Scaffold only | 0 |
| 02-product | `02-domains/02-product/` | 🔴 Scaffold only | 0 |
| **03-software** | `02-domains/03-software/` | ✅ **Active** | **73** |
| 04-finance | `02-domains/04-finance/` | 🔴 Scaffold only | 0 |
| 05-marketing | `02-domains/05-marketing/` | 🔴 Scaffold only | 0 |
| 06-operations | `02-domains/06-operations/` | 🔴 Scaffold only | 0 |
| 07-sales | `02-domains/07-sales/` | 🔴 Scaffold only | 0 |

### 7.2 Software Domain (Only Populated)

**Location**: `architech/02-domains/03-software/`
**Entity Count**: 73
**Status**: Active with real content

**Structure**:
```
03-software/
├── 00-definitions/     # Domain-specific definitions
├── 01-agents/          # Software agents
├── 02-skills/          # Software skills
├── 03-tasks/           # Software tasks
├── 04-workflows/       # Development workflows
├── 11-mental-models/   # Software-specific models
└── README.md
```

---

## 8. DEPENDENCY GRAPH

### 8.1 Activation Flow

```
User Input ("load MA" / "hi")
    ↓
Alias Resolution (activation_aliases)
    ↓
Agent File Load (~meta-architect)
    ↓
Activation Hooks:
    ├─ build_shortcut_registry.py --agent meta-architect --mode plan
    ├─ build_entity_definitions.py
    └─ echo "{name}" > .claude/current_agent.txt
    ↓
Context Load (~meta-map, dependencies)
    ↓
Help Display (~help)
```

### 8.2 Entity Creation Flow

```
User: "create new agent"
    ↓
Skill: ~create-agent
    ↓
Blueprint: agent-generator.py (generates .md with TODOs)
    ↓
Task Guidance: Complete TODOs
    ↓
Validation: ~entity:agent compliance
    ↓
Integration: Shortcut registry update
```

### 8.3 Trace Analysis Flow

```
Session Complete
    ↓
~trace-analyst activation
    ↓
Phase 1: PREPARE (export trace)
    ↓
Phase 2: DISPATCH (3 parallel subagents)
    ├─ trace-behavioral-validator
    ├─ trace-decision-analyzer
    └─ trace-content-analyzer
    ↓
Phase 3: AGGREGATE (merge JSON)
    ↓
Phase 4: PERSIST (store to backend)
    ↓
~trace-aggregator (cross-session patterns)
```

### 8.4 Core Dependencies

| Component | Depends On |
|-----------|-----------|
| meta-architect | ~meta-map, shortcut_registry, entity_definitions |
| trace-analyst | ~entity:checklist, trace subagents |
| create-skill | init_skill.py, ~entity:skill |
| mental-models | select_mental_models.py, 30+ model files |
| shortcut system | frontmatter parsing, path resolution |

---

## 9. CROSS-REFERENCE INDEX

### 9.1 By File Type

#### Python Scripts (.py)
| Path | Purpose |
|------|---------|
| [hooks/shortcut_system/build_shortcut_registry.py](architech/01-system/08-automation/hooks/shortcut_system/build_shortcut_registry.py) | Registry builder |
| [hooks/shortcut_system/shortcut_resolver.py](architech/01-system/08-automation/hooks/shortcut_system/shortcut_resolver.py) | Shortcut resolver |
| [hooks/shortcut_system/context_loader.py](architech/01-system/08-automation/hooks/shortcut_system/context_loader.py) | Context injection |
| [hooks/agent_system/activate_agent.py](architech/01-system/08-automation/hooks/agent_system/activate_agent.py) | Agent activation |
| [hooks/entity_system/build_entity_definitions.py](architech/01-system/08-automation/hooks/entity_system/build_entity_definitions.py) | Entity XML builder |
| [scripts/mental_models/select_mental_models.py](architech/01-system/08-automation/scripts/mental_models/select_mental_models.py) | Model selector |
| [scripts/skill_system/init_skill.py](architech/01-system/08-automation/scripts/skill_system/init_skill.py) | Skill initializer |

#### Entity Definitions (.md)
| Path | Entity Type |
|------|-------------|
| [00-definition.md](architech/01-system/00-definitions/entity-types/00-definition.md) | Definition |
| [01-agent.md](architech/01-system/00-definitions/entity-types/01-agent.md) | Agent |
| [02-skill.md](architech/01-system/00-definitions/entity-types/02-skill.md) | Skill |
| [03-task.md](architech/01-system/00-definitions/entity-types/03-task.md) | Task |
| [04-workflow.md](architech/01-system/00-definitions/entity-types/04-workflow.md) | Workflow |
| [05-blueprint.md](architech/01-system/00-definitions/entity-types/05-blueprint.md) | Blueprint |
| [06-rule.md](architech/01-system/00-definitions/entity-types/06-rule.md) | Rule |
| [07-checklist.md](architech/01-system/00-definitions/entity-types/07-checklist.md) | Checklist |
| [08-automation.md](architech/01-system/00-definitions/entity-types/08-automation.md) | Automation |
| [09-navigation.md](architech/01-system/00-definitions/entity-types/09-navigation.md) | Navigation |
| [10-documentation.md](architech/01-system/00-definitions/entity-types/10-documentation.md) | Documentation |
| [11-mental-model.md](architech/01-system/00-definitions/entity-types/11-mental-model.md) | Mental Model |
| [12-evaluation.md](architech/01-system/00-definitions/entity-types/12-evaluation.md) | Evaluation |

#### Agents (.md)
| Path | Agent |
|------|-------|
| [meta-architect/current/meta-architect.md](architech/00-meta/01-agents/meta-architect/current/meta-architect.md) | Meta Architect |
| [trace-analyst/trace-analyst.md](architech/00-meta/01-agents/trace-analyst/trace-analyst.md) | Trace Analyst |
| [trace-aggregator/trace-aggregator.md](architech/00-meta/01-agents/trace-aggregator/trace-aggregator.md) | Trace Aggregator |
| [bootstrap/bootstrap.md](architech/00-meta/01-agents/bootstrap/bootstrap.md) | Bootstrap |

### 9.2 By Shortcut

| Shortcut | Resolves To |
|----------|------------|
| `~meta-architect` | 00-meta/01-agents/meta-architect/current/meta-architect.md |
| `~trace-analyst` | 00-meta/01-agents/trace-analyst/trace-analyst.md |
| `~trace-aggregator` | 00-meta/01-agents/trace-aggregator/trace-aggregator.md |
| `~meta-map` | 00-meta/09-navigation/meta-map.md |
| `~entity:definition` | 01-system/00-definitions/entity-types/00-definition.md |
| `~entity:agent` | 01-system/00-definitions/entity-types/01-agent.md |
| `~entity:skill` | 01-system/00-definitions/entity-types/02-skill.md |
| `~entity:task` | 01-system/00-definitions/entity-types/03-task.md |
| `~entity:workflow` | 01-system/00-definitions/entity-types/04-workflow.md |
| `~entity:blueprint` | 01-system/00-definitions/entity-types/05-blueprint.md |
| `~entity:rule` | 01-system/00-definitions/entity-types/06-rule.md |
| `~entity:checklist` | 01-system/00-definitions/entity-types/07-checklist.md |
| `~entity:automation` | 01-system/00-definitions/entity-types/08-automation.md |
| `~entity:navigation` | 01-system/00-definitions/entity-types/09-navigation.md |
| `~entity:documentation` | 01-system/00-definitions/entity-types/10-documentation.md |
| `~entity:mental-model` | 01-system/00-definitions/entity-types/11-mental-model.md |
| `~create-project` | 00-meta/02-skills/create-project/create-project.md |
| `~create-skill` | 00-meta/02-skills/create-skill/create-skill.md |
| `~mental-models` | 00-meta/02-skills/mental-models/mental-models.md |

---

## STATISTICS SUMMARY

| Metric | Count |
|--------|-------|
| Entity Types | 12 |
| Active Agents | 3 (+ 1 designed) |
| Meta Skills | 12 |
| System Skills | 1 |
| Python Scripts | 27 |
| Test Cases | 150+ |
| Mental Models | 30+ |
| Lines of Code | 8,000+ |
| Populated Domains | 1 (software) |
| Total Entities (software) | 73 |

---

**Document Version**: 1.0.0
**Generated**: 2025-12-31
**Generator**: Meta Architect (Claude Opus 4.5)
