# Extraction 4: Resume/Handoff Schema Patterns

**Source**: `mutagent-obsidian/architech/00-meta/01-agents/meta-architect/memory/`
**Extracted**: 2026-01-01
**Spawns**: Project 17 (Hook Pattern Research)

---

## 1. Memory Folder Structure

### 1.1 Directory Architecture

The meta-architect agent maintains a sophisticated memory system at:
`architech/00-meta/01-agents/meta-architect/memory/`

```
memory/
├── compaction-log.yaml        # History of knowledge compression operations
├── dependency-map.v3.yaml     # Blueprint and system dependency graph
├── framework-evolution.md     # Log of framework-level changes
├── global-learnings.md        # Cross-session pattern repository
├── quick-reference-meta-architect.md  # FAST ACCESS critical context
├── vacuum-state.md            # Current state of knowledge extraction system
│
├── extraction-logs/           # Raw extraction outputs
│   ├── self-evolution-violation-2025-01-27.md
│   └── system-patterns/
│       ├── architech-dependency-analysis.md
│       ├── genesis-extraction.md
│       └── template-completeness-analysis.md
│
├── pattern-analysis/          # Pattern recognition outputs
│   ├── agent-patterns.md
│   ├── behavioral-patterns-phase1-integration-complete.md
│   ├── context-patterns.md
│   ├── file-placement-failure-ultrathink.md
│   ├── file-placement-validation-implementation-plan.md
│   ├── orchestration-rules-analysis.md
│   └── production-agent-patterns-extraction.md
│
├── simulation-results/        # Agent behavior simulation outputs
│   ├── example-simulation-configuration.md
│   └── evaluation-checklists/
│       ├── agent-simulation-checklist.md
│       └── infrastructure-readiness-checklist.md
│
└── synthesis/                 # Compacted, synthesized knowledge
    ├── compacted-learnings/
    │   └── compact-learnings-v2.0.md  # 15:1 compression ratio
    ├── nexus-behavioral-patterns-deep-dive.md
    ├── nexus-behavioral-patterns-integration.md
    ├── ultrathink-nexus-deep-patterns.md
    └── pattern-library/
        └── architech-patterns-v1.yaml  # 15 patterns catalogued
```

### 1.2 File Purposes

| File | Purpose | Load Priority |
|------|---------|---------------|
| `quick-reference-meta-architect.md` | FAST ACCESS - Critical files, shortcuts, decision trees | MANDATORY FIRST |
| `vacuum-state.md` | Current extraction status, metrics, health check | Startup |
| `global-learnings.md` | Cross-session patterns, critical learnings | Startup |
| `compaction-log.yaml` | History of compression operations | On-demand |
| `dependency-map.v3.yaml` | Blueprint dependency graph | On-demand |
| `framework-evolution.md` | Framework change history | On-demand |

---

## 2. Handoff Protocol Patterns

### 2.1 Warm Handoff Protocol (P008)

**Core Pattern**: Context-preserving agent transitions

```yaml
handoff_protocol:
  format: 'Work complete: {context_path}'
  validation: Required before handoff
  memory_update: Triggered after handoff

  steps:
    1. Complete current work
    2. Identify context location (explicit path)
    3. Validate work against quality gates
    4. Transfer state to receiving agent
    5. Trigger memory update

  handoff_templates:
    to_pm: 'Requirements ready at {path}'
    to_architect: 'Design needed for {path}'
    to_dev: 'Implementation ready at {path}'
    to_qa: 'Testing required for {path}'
```

### 2.2 Context Flow Paths

```yaml
flow_paths:
  vertical_flows:
    - META -> TOP_LEVEL -> REPOSITORY -> FEATURE
    - FEATURE -> REPOSITORY -> TOP_LEVEL -> META (feedback)

  horizontal_flows:
    - AGENT -> AGENT (warm handoffs)
    - REPOSITORY -> REPOSITORY (cross-repo sync)

  bidirectional_flows:
    - TOP_DOWN: Rules and constraints
    - BOTTOM_UP: Learnings and wisdom
```

### 2.3 Session Close Protocol

**Source**: `close-session workflow`

**10-Step Closure Sequence**:
1. Initialize TodoList with all workflow steps
2. Read Active Project State & Auto-Complete if Done
3. Review Task Completion (Interactive)
4. Update Maps (scan Projects/ and Skills/)
5. Get Fresh Timestamp
6. Update Memory Files
7. Clean Up Temporary Files
8. Create Session Report
9. Display Summary
10. **CRITICAL**: Instruct User to Start Fresh Session

**Session Report Template**:
```markdown
# Session Report - YYYY-MM-DD

**Duration**: [start time estimate] - [end time]
**Focus**: [project name or "General work"]

## Work Completed
- [Completed tasks from tasks.md]

## Progress Made
**Before**: X/Y tasks complete
**After**: Z/Y tasks complete
**Status**: [status before] -> [status after]

## Decisions Made
- [Decision 1]
- [Decision 2]

## Patterns Observed
- [Pattern 1]
- [Pattern 2]

## Context Notes
[Relevant context for next session]

## Next Steps
- Continue: [next task in current project]
```

---

## 3. State Machine Transitions

### 3.1 Project State Machine

```yaml
project_states:
  PLANNING:
    threshold: 0-9% complete
    allowed_transitions: [IN_PROGRESS]

  IN_PROGRESS:
    threshold: 10-99% complete
    allowed_transitions: [PLANNING, COMPLETE]

  COMPLETE:
    threshold: 100% complete
    allowed_transitions: [IN_PROGRESS] # Can be reopened
```

### 3.2 System State Classification

**Source**: `architech-loader.py`

```yaml
system_states:
  operational_with_active_projects:
    condition: active_projects > 0
    action: display_menu
    message: "Welcome! You have {N} active project(s)"

  projects_in_planning:
    condition: planning_projects > 0 AND active_projects == 0
    action: display_menu
    message: "You have {N} project(s) in planning"

  operational:
    condition: no active or planning projects
    action: display_menu
    message: "No active projects - ready to create new work"
```

### 3.3 Agent Power Hierarchy (State Authority)

```yaml
power_hierarchy:
  L10: [meta-architect]        # Observer/Creator - can modify framework
  L9:  [orchestrator, master]  # System Coordinators - can invoke all agents
  L8:  [architect, product-manager]  # Strategy/Design
  L7:  [developer, qa, product-owner, llm-whisperer]  # Builders
  L6:  [analyst, ux-expert]    # Research/Design
  L5:  [scrum-master]          # Facilitation
```

---

## 4. Required Sections in Resume Files

### 4.1 Project Overview (overview.md)

```yaml
required_frontmatter:
  id: "XX-project-name"
  name: "Human readable name"
  status: PLANNING|IN_PROGRESS|COMPLETE
  description: "Load trigger description"
  created: YYYY-MM-DD
  updated: YYYY-MM-DD  # Optional

required_sections:
  - Purpose (problem solved, value created)
  - Context (background, stakeholders)
  - Success Criteria (must achieve, nice to have)
  - Timeline (target completion, milestones)
  - Notes (additional context)
```

### 4.2 Tasks File (tasks.md)

```yaml
required_structure:
  header:
    - title: "{Project Name} - Tasks"
    - last_updated: YYYY-MM-DD

  phases:
    - "Phase 1: Setup & Planning"
    - "Phase 2: Foundation"
    - "Phase 3: Core Features"
    - "Phase 4: Integration"
    - "Phase 5: Testing & Refinement"
    - "Phase 6: Deployment"
    - "Phase 7: Retrospective (MANDATORY)"

  task_format:
    unchecked: "- [ ] Task description"
    checked: "- [x] Task description"

  footer:
    - Task Management instructions
    - Current blockers
    - Dependencies
```

### 4.3 Quick Reference (quick-reference-{agent}.md)

**This is the CRITICAL RESUME FILE for agents**

```yaml
required_sections:
  critical_files_to_always_load:
    - path, shortcut, purpose

  key_framework_documents:
    - domain creation references
    - quality standards references

  entity_classification_quick_rules:
    - checklist for entity typing

  analysis_patterns:
    - ULTRATHINK checklist
    - BLACK HOLE vacuum process

  self_improvement_protocol:
    - when to evolve
    - how to evolve
    - recent evolutions

  common_questions_and_answers:
    - Q&A pairs for frequent decisions

  behavioral_safeguards:
    - AI failure prevention patterns
    - before_task / after_task checklists

  quick_actions:
    - command sequences for common tasks

  version_history:
    - changelog
```

---

## 5. MANDATORY LOAD Pattern

### 5.1 Startup Sequence

**Source**: `CLAUDE.md` and `architech-loader.py`

```yaml
mandatory_load_sequence:
  step_1:
    action: "Execute architech-loader.py --startup"
    returns:
      - system_state classification
      - files_to_load array
      - instructions (action, message, steps)
      - metadata (projects, skills)
      - stats

  step_2:
    action: "Load MANDATORY_MAPS"
    files:
      - "architech/00-meta/09-navigation/meta-map.md"

  step_3:
    action: "Adopt persona from agent file"
    sequence:
      - Read entire agent file
      - Adopt persona
      - Load context-map
      - Greet and halt
```

### 5.2 Critical Files (from quick-reference)

```yaml
architectural_foundation:
  load_first:
    - path: "00-meta/00-definitions/framework-maps/structure-map.yaml"
      shortcut: "~structure-map"
      purpose: "WHERE things live (four-level architecture)"

    - path: "00-meta/00-definitions/framework-maps/memory-map.yaml"
      shortcut: "~memory-map"
      purpose: "HOW context flows (memory hierarchy)"

    - path: "01-system/rules/architech-orchestration-rules.md"
      shortcut: "~architech-orchestration"
      purpose: "WHICH entities exist, WHEN to use"

    - path: "01-system/rules/core-context-loading.md"
      shortcut: "~core-context-loading"
      purpose: "WHAT must be loaded"
```

### 5.3 Pre-Operation Checks

**Source**: `framework-evolution-protocols.md`

```yaml
before_any_operation:
  1_read: "structures.md to understand current template system"
  2_read: "3-5 existing templates in same category for patterns"
  3_extract: "common patterns and required sections"
  4_identify: "versioning and metadata standards"
  5_apply: "patterns to new creation"
  6_validate: "against framework compliance"

violation_prevention:
  - "If unsure about format, read structures.md first"
  - "If creating new template type, study closest existing type"
  - "If modifying framework, check impact on existing components"
  - "If missing versioning, STOP and add proper 3-line header"
```

---

## 6. Context Preservation

### 6.1 What Gets Saved

```yaml
preserved_context:
  project_state:
    - overview.md (purpose, goals, status)
    - tasks.md (progress, checkboxes)
    - requirements.md (what to build)
    - design.md (how to build)

  agent_memory:
    - global-learnings.md (cross-session patterns)
    - quick-reference-{agent}.md (critical context)
    - extraction-logs/ (raw extractions)
    - synthesis/ (compacted knowledge)

  session_reports:
    - session-reports/YYYY-MM-DD-session.md

  patterns:
    - pattern-analysis/*.md
    - synthesis/pattern-library/*.yaml
```

### 6.2 What Gets Lost

```yaml
lost_context:
  ephemeral:
    - In-conversation reasoning
    - Temporary calculations
    - Uncommitted file changes

  session_specific:
    - Current working memory
    - Tool call history
    - Intermediate states

  not_persisted:
    - User preferences not documented
    - Implicit decisions not recorded
    - Mental models not loaded
```

### 6.3 Context Preservation Mechanisms

```yaml
mechanisms:
  hierarchical_memory:
    type: structural
    quality: PERFECT
    coverage: 100%

  engineering_rules:
    type: governance
    quality: EXCELLENT
    coverage: all_operations

  warm_handoffs:
    type: operational
    quality: PERFECT
    coverage: all_transitions
    format: "Work complete: {context_path}"

  template_generation:
    type: genetic
    quality: PERFECT
    coverage: all_components
    source: 44_YAML_templates

  quality_gates:
    type: validation
    quality: EXCELLENT
    coverage: all_decisions
    framework: PASS/CONCERNS/FAIL/WAIVED
```

---

## 7. Evolution/Versioning System

### 7.1 Agent Version Structure

```
evolution/
├── v1.0.0/
│   └── meta-architect.md
├── v1.1.0/
│   └── meta-architect.md
├── v1.2.0/
│   └── meta-architect.md
├── v1.3.0/
│   └── meta-architect.md
└── v1.4.0/
    └── meta-architect.md
```

### 7.2 Self-Evolution Protocol

**Source**: `self-evolution-violation-2025-01-27.md`

```yaml
meta_architect_edit_protocol:
  before_any_edit:
    - question: "Is this file meta-architect.md?"
    - if_yes:
        - STOP
        - Check .meta/meta-architect/evolution/
        - Determine next version number
        - Plan evolution properly

  required_actions:
    1: "CHECK .meta/meta-architect/ directory"
    2: "CREATE new version directory"
    3: "UPDATE evolution-log.md"
    4: "COPY to evolution/v{x.y.z}/"
    5: "UPDATE current/"
    6: "SYNC with .architech/agents/"

  validation:
    - Version must increment
    - Evolution log must document
    - Learning must be extracted
```

### 7.3 Knowledge Compaction

**Source**: `compaction-log.yaml`

```yaml
compaction_operations:
  trigger_conditions:
    pattern_threshold: 20_new_patterns
    time_threshold: 30_days
    size_threshold: 100kb
    user_request: immediate

  process:
    input_metrics:
      - total_files
      - total_size_kb
      - total_lines
      - redundancy_detected

    processing:
      - analysis_depth: MAXIMUM
      - pattern_extraction: COMPLETE
      - knowledge_synthesis: ULTRA_COMPRESSED
      - obsolete_removal: AGGRESSIVE

    output_metrics:
      - compacted_file: compact-learnings-v{x}.md
      - compression_ratio: 15:1 (achieved)
      - knowledge_retention: 100%
```

---

## 8. Behavioral Safeguards (AI Failure Prevention)

### 8.1 Critical Patterns

**Source**: `quick-reference-meta-architect.md`

```yaml
behavioral_safeguards:
  execution_documentation_paradox:
    prevention: 35%
    before: "Am I about to EXECUTE or DOCUMENT?"
    commitment: Execute first, document second
    evidence: Proof required for all completion claims

  false_completion_syndrome:
    prevention: 19%
    before: "What proof validates completion?"
    strategy: Prepare evidence collection plan
    validation: Independent verification must be possible

  basic_operations_failure:
    prevention: 21%
    before: "Can I correctly execute fundamentals?"
    validation: File paths, sequences, procedures verified
    foundation: Basic competency confirmed before complex work

  systematic_success_reinforcement:
    type: preventive
    before: "What successful patterns can I apply?"
    leverage: Use proven approaches
    reference: quick-reference-meta-architect.md
```

### 8.2 Application Pattern

```yaml
before_task:
  - Check: "Execute or document?" -> Choose EXECUTE
  - Plan: "What proof validates this?" -> Define evidence
  - Verify: "Can I do basics?" -> Validate foundation
  - Apply: "What patterns work?" -> Reference quick-reference

after_task:
  - Verify: Evidence collected
  - Check: Independent verification possible
  - Validate: Filesystem matches claims
  - Capture: Document success patterns
```

---

## 9. Key Insights for Strategy Nexus

### 9.1 Patterns to Adopt

1. **MANDATORY LOAD Pattern**: Always read context files before proceeding
2. **Quick Reference Files**: Create fast-access critical context for each agent/project
3. **Warm Handoff Protocol**: Explicit context paths with validation
4. **Session Reports**: Persistent record of each work session
5. **Compaction System**: Compress learnings over time (15:1 ratio possible)
6. **Behavioral Safeguards**: Pre/post task checklists for AI failure prevention

### 9.2 Structure to Mirror

```yaml
nexus_resume_structure:
  per_project:
    - _resume.md (equivalent to quick-reference)
    - steps.md (equivalent to tasks.md)
    - overview.md (in 01-planning/)

  per_agent:
    - memory/ folder with:
      - global-learnings.md
      - quick-reference-{agent}.md
      - synthesis/ (compacted knowledge)

  system_level:
    - context_startup.json (from nexus-loader)
    - session-reports/ (historical records)
```

### 9.3 Critical Differences

| Architech | Strategy Nexus | Adaptation Needed |
|-----------|----------------|-------------------|
| YAML frontmatter | JSON configs | Keep consistency |
| 7-phase tasks | Flexible phases | Add retrospective phase |
| ~shortcut syntax | Plain paths | Consider shortcuts |
| .md everything | Mixed formats | Standardize |
| evolution/ folders | _resume.md only | Add versioning? |

---

## 10. Spawned Project: Hook Pattern Research (Project 17)

This extraction reveals sophisticated patterns that require deeper research:

1. **Pre/Post Hook Architecture**: How to inject behavior before/after operations
2. **Mandatory Load Enforcement**: Blocking patterns for context loading
3. **State Machine Validation**: Transitions with quality gates
4. **Compaction Triggers**: When and how to compress knowledge
5. **Evolution Protocol**: Self-modifying systems with version control

**Recommended Project 17 Tasks**:
- [ ] Research Claude Code hook system capabilities
- [ ] Design mandatory load hook pattern
- [ ] Implement session close hook
- [ ] Create compaction trigger system
- [ ] Build evolution/versioning for agents

---

**Extraction Complete**

*Hyperdetailed extraction of Resume/Handoff schema patterns from Architech framework*
*Ready for absorption into Strategy Nexus system*
