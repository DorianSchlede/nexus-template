# Architecture v2: Mandatory Router + Template-First + Discovery-First

**Date**: 2026-01-07
**Version**: 2.2 (EARS/INCOSE integration)
**Status**: IN REVIEW
**Supersedes**: architecture-decision.md, revised-architecture.md, mental-models-analysis.md, template-system-design.md

---

## Executive Summary

plan-project becomes the **mandatory router** for all project creation. Templates define types. Discovery happens **before** mental models. **Steps enforce sequence** to prevent context loss.

**Critical Insight**: The AI WILL forget to return from sub-skills. Steps are the ONLY enforcement mechanism.

---

## Core Principles

1. **Router is MANDATORY** - All project creation goes through plan-project
2. **Templates define types** - Add a type by adding a folder (no code changes)
3. **Discovery BEFORE mental models** - Can't stress-test what you don't understand
4. **Steps enforce sequence** - AI forgets; steps don't. Steps are the core leverage.
5. **Discovery outputs to 02-discovery.md** - MANDATORY file, preserves intelligence across compaction
6. **Resume-context.md is dynamic** - Updated every phase, enables proper reload
7. **Mental models loaded dynamically** - Via mental-models skill, not hardcoded
8. **Sub-skills loaded via bash** - Explicit `nexus-loader.py --skill X` commands
9. **No keyword triggers** - AI semantically matches from type description
10. **AI scales naturally** - No sub-types or scope parameters, AI judges depth

---

## The Sequence (CRITICAL)

### Wrong (Old)
```
Type → Mental Models → Discovery → Plan
       ↑
       "What could go wrong?" (but we don't know what we're building!)
```

### Correct (New)
```
Type → Discovery → Mental Models → Re-Discovery? → Plan
                   ↑
                   "Given what we found, what could go wrong?"
```

### The Loop

```
┌─────────────────────────────────────────┐
│                                         │
│   DISCOVER ──────► THINK ──────►        │
│       ▲              │                  │
│       │              │                  │
│       └──────────────┘                  │
│         (if gaps found)                 │
│                                         │
│              │                          │
│              ▼                          │
│           FINALIZE                      │
│                                         │
└─────────────────────────────────────────┘

Max 2 re-discovery rounds. After that, note unknowns and proceed.
```

---

## Full Flow (STEPS-DRIVEN)

**Critical**: Each phase has explicit steps that MUST be embedded in the project's `04-steps.md`.
The steps file is the enforcement mechanism that survives compaction.

```
plan-project (MANDATORY ROUTER)
    │
    │ ══════════════════════════════════════
    │ PHASE 1: SETUP
    │ ══════════════════════════════════════
    │
    ├── Step 1.1: Type Detection
    │   └── AI semantically matches user input against _type.yaml descriptions
    │   └── OR ask user to select type (show descriptions)
    │   └── NO keyword matching - descriptions are sufficient
    │
    ├── Step 1.2: Create Project Structure
    │   └── Run: python 00-system/skills/projects/plan-project/scripts/init_project.py --type {type}
    │   └── Creates: 01-planning/, 02-resources/, 03-working/, 04-outputs/
    │
    ├── Step 1.3: Load ALL Templates
    │   └── Copy overview.md template → project/01-planning/01-overview.md
    │   └── Copy discovery.md template → project/01-planning/02-discovery.md (MANDATORY)
    │   └── Copy plan.md template → project/01-planning/03-plan.md
    │   └── Copy steps.md template → project/01-planning/04-steps.md
    │   └── Create resume-context.md with initial state
    │
    ├── Step 1.4: Initialize Resume Context
    │   └── Write project_id, project_name, current_phase: "planning"
    │   └── Write files_to_load: [all planning files]
    │   └── This enables proper reload after compaction
    │
    │ ══════════════════════════════════════
    │ PHASE 2: DISCOVERY (First Pass)
    │ ══════════════════════════════════════
    │
    ├── Step 2.1: Check _type.yaml for discovery.skill
    │   │
    │   ├── HAS SKILL (integration, research, skill)
    │   │   │
    │   │   ├── Step 2.1a: Update resume-context.md
    │   │   │   └── Add sub_skill: "{skill-name}"
    │   │   │   └── Add sub_skill_step: "discovery"
    │   │   │
    │   │   ├── Step 2.1b: Load Sub-Skill via Bash
    │   │   │   └── python 00-system/core/nexus-loader.py --skill {skill-name}
    │   │   │   └── Pass: entry_mode: "from_router", project_path: "02-projects/XX-name/"
    │   │   │
    │   │   ├── Step 2.1c: Execute Sub-Skill Discovery
    │   │   │   └── Sub-skill performs discovery (WebSearch, paper-search, etc.)
    │   │   │   └── Sub-skill writes findings to 02-discovery.md in project
    │   │   │
    │   │   └── Step 2.1d: Clear Sub-Skill from Resume
    │   │       └── Remove sub_skill, sub_skill_step from resume-context.md
    │   │
    │   └── NO SKILL (build, content, strategy, process, generic)
    │       └── Use discovery.md template questions
    │       └── Ask questions inline
    │       └── Write answers to 02-discovery.md (MANDATORY)
    │
    ├── Step 2.2: Verify Discovery Output Exists
    │   └── Confirm 02-discovery.md has content
    │   └── If empty, discovery failed - do not proceed
    │
    │ ══════════════════════════════════════
    │ PHASE 3: MENTAL MODELS (Informed by Discovery)
    │ ══════════════════════════════════════
    │
    ├── Step 3.1: Load Mental Models Dynamically
    │   └── Run: python 00-system/mental-models/scripts/select_mental_models.py --format brief
    │   └── AI selects 2-3 relevant models based on discovery findings
    │   └── Present options to user
    │
    ├── Step 3.2: Load Selected Model Files
    │   └── Read: 00-system/mental-models/models/{category}/{model-slug}.md
    │   └── Apply model questions to discovery findings
    │
    ├── Step 3.3: Apply Mental Models to Discovery
    │   │
    │   ├── Questions are INFORMED by discovery:
    │   │   └── "Given what we found about [X], what's truly essential?"
    │   │   └── "Given these constraints [from discovery], what could break?"
    │   │   └── "Given this plan [from discovery], imagine it failed. Why?"
    │   │
    │   └── Capture outputs:
    │       └── success_criteria: []
    │       └── risks: []
    │       └── gaps: []
    │
    ├── Step 3.4: Update Plan with Mental Model Outputs
    │   └── Write success criteria to 03-plan.md
    │   └── Write risks to 03-plan.md
    │   └── Write gaps as open questions
    │
    │ ══════════════════════════════════════
    │ PHASE 4: RE-DISCOVERY (If Needed)
    │ ══════════════════════════════════════
    │
    ├── IF gaps exist AND iteration < 2:
    │   │
    │   ├── Step 4.1: Update Resume Context
    │   │   └── Set rediscovery_round: 1 (or 2)
    │   │
    │   ├── Step 4.2: Route to Discovery
    │   │   └── Same as Phase 2, but targeted at gaps
    │   │
    │   └── Step 4.3: Return to Phase 3
    │       └── Re-apply mental models with new info
    │
    ├── ELSE IF gaps exist AND iteration >= 2:
    │   └── Log unknowns in 03-plan.md "Open Questions" section
    │   └── Note: "Proceeding with known unknowns after 2 discovery rounds"
    │   └── Proceed to finalization
    │
    │ ══════════════════════════════════════
    │ PHASE 5: FINALIZATION
    │ ══════════════════════════════════════
    │
    ├── Step 5.1: Merge All Into 03-plan.md
    │   └── Discovery findings (from 02-discovery.md)
    │   └── Mental model outputs (success criteria, risks)
    │   └── Open questions / unknowns
    │   └── Add context loading section at top
    │
    ├── Step 5.2: Finalize 04-steps.md
    │   └── Use steps.md template as base
    │   └── Fill in concrete tasks from discovery
    │   └── Each phase must have "Context to Load" header
    │   └── Each phase must have "Update Resume" step
    │
    ├── Step 5.3: Update Resume Context
    │   └── Set current_phase: "execution"
    │   └── Update files_to_load with all relevant resources
    │   └── Set next_action: "execute-project"
    │
    └── Step 5.4: Project Ready for Execution
        └── All 4 planning files complete
        └── Resume context enables reload
        └── Steps enforce execution sequence
```

---

## Directory Structure

```
plan-project/
├── SKILL.md                      # Router logic (simplified)
├── scripts/
│   └── init_project.py           # Project scaffolding
│
├── templates/
│   └── types/                    # ONE FOLDER PER TYPE
│       │
│       ├── build/
│       │   ├── _type.yaml        # Type config
│       │   ├── plan.md           # Plan template with placeholders
│       │   ├── steps.md          # Steps template
│       │   └── discovery.md      # Inline discovery questions
│       │
│       ├── integration/
│       │   ├── _type.yaml        # Routes to add-integration
│       │   ├── plan.md
│       │   ├── steps.md
│       │   └── discovery.md      # Fallback if skill unavailable
│       │
│       ├── research/
│       │   ├── _type.yaml        # Routes to create-research-project
│       │   ├── plan.md
│       │   ├── steps.md
│       │   └── discovery.md
│       │
│       ├── strategy/
│       │   ├── _type.yaml
│       │   ├── plan.md
│       │   ├── steps.md
│       │   └── discovery.md
│       │
│       ├── content/
│       │   └── ...
│       │
│       ├── process/
│       │   └── ...
│       │
│       └── generic/
│           └── ...
│
└── references/
    ├── routing-logic.md          # How the router works
    └── type-detection.md         # Auto-generated keyword → type mapping
```

---

## _type.yaml Schema

```yaml
# Required
name: string                      # Display name (e.g., "Integration")
description: string               # When to use this type - AI matches semantically

# Discovery configuration
discovery:
  skill: string                   # Skill to route to (optional)
  skill_load_command: string      # Exact bash command to load skill
  entry_mode: from_router         # Always "from_router" when skill specified
  inline: boolean                 # Use discovery.md template (default if no skill)

# Output configuration
outputs:
  discovery_file: string          # Always "02-discovery.md" - MANDATORY
  versioned_resources: boolean    # Whether to version resources (default: true)

# Mental models - loaded dynamically, not hardcoded
mental_models:
  dynamic: true                   # Always true - use mental-models skill
  load_command: string            # Command to list available models
  max_rediscovery_rounds: number  # Default: 2
```

**Note**: No `keywords` field. AI semantically matches from `description`.

### Example: integration/_type.yaml

```yaml
name: Integration
description: |
  Connect external APIs and services to Nexus.
  Use when: adding webhooks, OAuth flows, API clients, third-party service connections.

discovery:
  skill: add-integration
  skill_load_command: "python 00-system/core/nexus-loader.py --skill add-integration"
  entry_mode: from_router

outputs:
  discovery_file: "02-discovery.md"
  versioned_resources: true

mental_models:
  dynamic: true
  load_command: "python 00-system/mental-models/scripts/select_mental_models.py --format brief"
  max_rediscovery_rounds: 2
```

### Example: build/_type.yaml

```yaml
name: Build
description: |
  Create new software, features, or systems.
  Use when: implementing functionality, coding solutions, building tools.

discovery:
  inline: true

outputs:
  discovery_file: "02-discovery.md"
  versioned_resources: true

mental_models:
  dynamic: true
  load_command: "python 00-system/mental-models/scripts/select_mental_models.py --format brief"
  max_rediscovery_rounds: 1
```

### Example: skill/_type.yaml (NEW)

```yaml
name: Skill
description: |
  Create new Nexus skills or automation capabilities.
  Use when: building reusable workflows, automation, new commands.

discovery:
  skill: create-skill
  skill_load_command: "python 00-system/core/nexus-loader.py --skill create-skill"
  entry_mode: from_router

outputs:
  discovery_file: "02-discovery.md"
  versioned_resources: true

mental_models:
  dynamic: true
  load_command: "python 00-system/mental-models/scripts/select_mental_models.py --format brief"
  max_rediscovery_rounds: 1
```

---

## What Skills Return

Skills are **discovery engines**. They return structured data, not prose.

### add-integration returns:

```yaml
discovery_output:
  service_name: "HubSpot"
  service_slug: "hubspot"
  base_url: "https://api.hubapi.com"
  auth_type: "oauth2"
  env_key: "HUBSPOT_API_KEY"
  rate_limits: "100 requests / 10 seconds"
  endpoints:
    - name: "List Contacts"
      method: "GET"
      path: "/crm/v3/objects/contacts"
      selected: true
    - name: "Create Contact"
      method: "POST"
      path: "/crm/v3/objects/contacts"
      selected: true
  config_path: "02-resources/integration-config.json"
```

### create-research-project returns:

```yaml
discovery_output:
  research_question: "How do foundational ontologies compare..."
  research_purpose: "Inform ontology selection for knowledge graph"
  extraction_schema:
    - field: "ontology_name"
      description: "Name of the ontology"
      priority: high
    - field: "core_concepts"
      description: "Main concepts/classes"
      priority: high
  papers_found: 45
  papers_selected: 15
  papers_downloaded: 12
  papers_failed: 3
  briefing_path: "02-resources/_briefing.md"
  analysis_kit_path: "02-resources/_analysis_kit.md"
```

### create-skill returns:

```yaml
discovery_output:
  skill_name: "slack-power"
  skill_slug: "slack-power"
  skill_purpose: "Extract meeting notes and action items from Slack channels"
  triggers:
    - "extract slack meetings"
    - "slack meeting notes"
    - "summarize slack channel"
  skill_type: "workflow"  # workflow | tool | integration
  resources_needed:
    scripts: true
    references: true
    assets: false
  complexity: "medium"  # simple | medium | complex
  dependencies:
    - "Slack API access"
    - "MCP server configured"
  skill_path: "03-skills/slack-power/"
```

---

## Template Placeholders

Templates use placeholders that get filled by discovery and mental models.

### plan.md template example:

```markdown
# {{project_name}} - Plan

## Purpose
{{mental_models.purpose}}

## Success Criteria
{{#each mental_models.success_criteria}}
- [ ] {{this}}
{{/each}}

## Discovery Summary

### What We Found
{{discovery_output.summary}}

### Key Constraints
{{#each discovery_output.constraints}}
- {{this}}
{{/each}}

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
{{#each mental_models.risks}}
| {{name}} | {{likelihood}} | {{impact}} | {{mitigation}} |
{{/each}}

## Open Questions
{{#each mental_models.unknowns}}
- [ ] {{this}}
{{/each}}

---
*Generated by plan-project router*
```

---

## Specialized Skill Contract

When router calls a skill:

```yaml
# Router passes to skill
entry_mode: from_router
project_path: "02-projects/31-hubspot-integration/"
```

Skill MUST:
1. Check `entry_mode` at workflow start
2. Skip project creation steps if `entry_mode == from_router`
3. Use provided `project_path` for all file operations
4. Return `discovery_output` as structured YAML/JSON
5. NOT generate prose - router handles plan.md population

Skill returns:
```yaml
discovery_output:
  # Structured data specific to skill type
  ...
```

---

## Type Spectrum

| Type | Discovery Method | Why |
|------|------------------|-----|
| **build** | Inline (discovery.md) | Just questions about requirements |
| **integration** | Skill (add-integration) | Needs WebSearch, API parsing |
| **research** | Skill (create-research-project) | Needs paper-search, downloads |
| **strategy** | Inline (discovery.md) | Decision framework questions |
| **content** | Inline (discovery.md) | Creative brief questions |
| **process** | Inline (discovery.md) | Current/future state questions |
| **skill** | Skill (create-skill) | Needs skill scaffolding, triggers |
| **generic** | Inline (discovery.md) | Minimal questions |

**Integration, research, and skill need external skills because they fetch data or scaffold structures.**
**Other types just need good discovery questions.**

---

## Resume Context Schema (CRITICAL)

Resume context enables proper reload after compaction. **Must be updated at every phase transition.**

```yaml
# resume-context.md frontmatter
---
session_ids: ["uuid-1", "uuid-2"]         # Track all sessions
resume_schema_version: "2.0"
last_updated: "2026-01-07T10:00:00Z"

# PROJECT
project_id: "30-project-name"
project_name: "Human Readable Name"
current_phase: "planning|execution"

# LOADING - Updated dynamically
next_action: "plan-project|execute-project"
files_to_load:
  - "01-planning/01-overview.md"
  - "01-planning/02-discovery.md"          # MANDATORY
  - "01-planning/03-plan.md"
  - "01-planning/04-steps.md"
  - "02-resources/integration-config.json"  # Type-specific resources

# SUB-SKILL TRACKING (when routing to another skill)
sub_skill: "add-integration"               # Current sub-skill (if any)
sub_skill_step: "discovery"                # What the sub-skill is doing
sub_skill_project_path: "02-projects/30-x/" # Where sub-skill writes

# DISCOVERY STATE
rediscovery_round: 0                       # 0, 1, or 2
discovery_complete: false

# PROGRESS
current_section: 2
current_task: 3
total_tasks: 24
tasks_completed: 8
---
```

### Resume Context Update Rules

1. **On Phase Transition**: Update `current_phase`, `files_to_load`
2. **On Sub-Skill Entry**: Add `sub_skill`, `sub_skill_step`, `sub_skill_project_path`
3. **On Sub-Skill Exit**: Remove sub-skill fields, verify `02-discovery.md` has content
4. **On Re-Discovery**: Increment `rediscovery_round`
5. **On Task Completion**: Update progress counters

### SessionStart Hook Integration

The SessionStart hook reads `resume-context.md` to determine what to load:

```python
# Simplified hook logic
if resume_context.sub_skill:
    # We were in a sub-skill, reload it
    inject_context(resume_context.sub_skill)
    inject_instruction(f"Continue {resume_context.sub_skill_step}")
else:
    # Normal project resume
    inject_files(resume_context.files_to_load)
    inject_instruction(f"Continue from {resume_context.current_phase}")
```

---

## Steps Template (ENFORCEMENT MECHANISM)

Steps are the core leverage for making this system work. They survive compaction and enforce sequence.

### Required Sections in Every Steps Template

```markdown
# {Project Name} - Execution Steps

**Context to Load**:
- `01-planning/03-plan.md`
- `01-planning/02-discovery.md`
- `02-resources/{type-specific-files}`

---

## Phase 1: Setup
**Update Resume**: Set current_phase: "planning", current_section: 1

- [ ] Detect project type
- [ ] Create project structure
- [ ] Load all templates (overview, discovery, plan, steps)
- [ ] Initialize resume-context.md

---

## Phase 2: Discovery
**Context to Load**: `_type.yaml` for discovery configuration
**Update Resume**: Set current_section: 2

### IF skill-based discovery:
- [ ] Update resume-context.md with sub_skill
- [ ] Load sub-skill: `python 00-system/core/nexus-loader.py --skill {skill}`
- [ ] Execute discovery (sub-skill handles this)
- [ ] Verify 02-discovery.md has content
- [ ] Clear sub_skill from resume-context.md

### IF inline discovery:
- [ ] Read discovery.md template questions
- [ ] Ask discovery questions
- [ ] Write answers to 02-discovery.md

---

## Phase 3: Mental Models
**Context to Load**: `02-discovery.md`
**Update Resume**: Set current_section: 3

- [ ] Load mental models: `python 00-system/mental-models/scripts/select_mental_models.py --format brief`
- [ ] Select 2-3 relevant models
- [ ] Apply models to discovery findings
- [ ] Capture: success_criteria, risks, gaps
- [ ] Update 03-plan.md with outputs
- [ ] IF gaps exist AND round < 2: Go to Phase 4
- [ ] ELSE: Go to Phase 5

---

## Phase 4: Re-Discovery (if needed)
**Update Resume**: Increment rediscovery_round

- [ ] Focus on identified gaps
- [ ] Repeat Phase 2 steps for gaps only
- [ ] Return to Phase 3

---

## Phase 5: Finalization
**Update Resume**: Set current_phase: "execution"

- [ ] Merge all into 03-plan.md
- [ ] Finalize 04-steps.md with concrete tasks
- [ ] Update resume-context.md files_to_load
- [ ] Set next_action: "execute-project"
```

### Key Enforcement Patterns

1. **Every phase has "Update Resume" instruction** - Non-negotiable
2. **Context to Load is explicit** - No guessing what files are needed
3. **Sub-skill tracking in steps** - Add/remove from resume is a step
4. **Verification steps** - "Verify 02-discovery.md has content"
5. **Conditional flow in steps** - IF/ELSE embedded in step list

---

## EARS Requirements Patterns (Build/Skill Types)

For Build and Skill project types, requirements in 02-discovery.md MUST follow EARS patterns.
Battle-tested at Amazon scale via Kiro.

### The Six EARS Patterns

Every requirement MUST follow exactly ONE pattern:

| Pattern | Template | Example |
|---------|----------|---------|
| **Ubiquitous** | THE `<system>` SHALL `<response>` | THE API SHALL return JSON responses |
| **Event-driven** | WHEN `<trigger>`, THE `<system>` SHALL `<response>` | WHEN user clicks submit, THE form SHALL validate inputs |
| **State-driven** | WHILE `<condition>`, THE `<system>` SHALL `<response>` | WHILE connection is active, THE client SHALL send heartbeats |
| **Unwanted** | IF `<condition>`, THEN THE `<system>` SHALL `<response>` | IF rate limit exceeded, THEN THE API SHALL return 429 |
| **Optional** | WHERE `<option>`, THE `<system>` SHALL `<response>` | WHERE caching enabled, THE service SHALL store responses |
| **Complex** | [WHERE] [WHILE] [WHEN/IF] THE `<system>` SHALL `<response>` | WHERE admin, WHEN delete requested, THE system SHALL require confirmation |

### INCOSE Quality Rules

Every requirement MUST comply with these rules:

**Clarity and Precision**
- Active voice: Clearly state who does what
- No vague terms: Avoid "quickly", "adequate", "reasonable", "user-friendly"
- No pronouns: Don't use "it", "them", "they" - use specific names
- Consistent terminology: Use defined terms consistently

**Testability**
- Explicit conditions: All conditions must be measurable or verifiable
- Measurable criteria: Use specific, quantifiable criteria
- One thought per requirement: Each requirement tests one thing

**Completeness**
- No escape clauses: Avoid "where possible", "if feasible"
- No absolutes: Avoid "never", "always", "100%" unless truly absolute
- Solution-free: Focus on what, not how

### Requirements in 02-discovery.md (Build/Skill)

```markdown
## Requirements

### Functional Requirements

**REQ-1**: WHEN user invokes the skill, THE system SHALL display available options
**REQ-2**: THE system SHALL validate all inputs before processing
**REQ-3**: IF validation fails, THEN THE system SHALL return descriptive error message
**REQ-4**: WHILE processing, THE system SHALL update progress in resume-context.md

### Non-Functional Requirements

**REQ-NF-1**: THE system SHALL respond within 2 seconds for all operations
**REQ-NF-2**: THE system SHALL handle up to 100 concurrent requests

### Quality Checklist
- [ ] All requirements use EARS patterns
- [ ] No vague terms (quickly, adequate, etc.)
- [ ] No pronouns (it, them, they)
- [ ] Each requirement is independently testable
- [ ] No implementation details (focus on what, not how)
```

---

## Correctness Properties (Build/Skill Types)

For Build and Skill types, 03-plan.md includes Correctness Properties for property-based testing.

### What Are Correctness Properties?

Universal quantifications that must hold for ALL valid inputs - not just specific test cases.

### Property Format

```markdown
## Correctness Properties

**Property 1: Input Validation Completeness**
For all user inputs, the system either accepts valid input OR returns a descriptive error.
**Validates**: REQ-2, REQ-3

**Property 2: State Consistency**
For any sequence of operations, resume-context.md reflects the actual system state.
**Validates**: REQ-4

**Property 3: Idempotency**
For all read operations, repeated calls with same input return same output.
**Validates**: REQ-1
```

### Property Requirements

- Each property contains explicit "for all" or "for any" statement
- Each property references the requirement(s) it validates
- Properties enable property-based testing (not just example-based)

---

## Task Patterns (ALL Types)

### Checkpoint Tasks

Insert verification points every 3-5 tasks:

```markdown
- [ ] Implement user input validation
- [ ] Add error handling for edge cases
- [ ] **CHECKPOINT**: Verify validation works, ask user if questions arise
- [ ] Implement core processing logic
- [ ] Add logging for debugging
- [ ] **CHECKPOINT**: Test core flow end-to-end
```

### Optional Task Marking

Tasks that can be skipped are marked with `*` postfix:

```markdown
- [ ] Implement core feature
- [ ]* Write unit tests for core feature (optional)
- [ ]* Add integration tests (optional)
- [ ] Wire up to main system
- [ ]* Add performance benchmarks (optional)
```

**Rules:**
- Only sub-tasks can have `*` postfix
- Top-level tasks MUST NOT be optional
- Core implementation tasks are NEVER optional
- Test tasks are typically optional (user chooses)

### Task Reference Format

Each task references requirements/decisions:

```markdown
- [ ] Implement input validation **[REQ-2]**
- [ ] Add error messages **[REQ-3]**
- [ ]* Write property tests for validation **[Property 1]** (optional)
```

### No Standalone Test Tasks

Tests are SUB-TASKS of implementation, not separate phases:

```markdown
## BAD - Standalone test phase
- [ ] Implement feature A
- [ ] Implement feature B
- [ ] Write all tests  ← NO!

## GOOD - Tests as sub-tasks
- [ ] Implement feature A
  - [ ]* Unit tests for A (optional)
- [ ] Implement feature B
  - [ ]* Unit tests for B (optional)
- [ ] **CHECKPOINT**: Verify A and B work together
```

---

## Adding a New Type

To add a new type (e.g., "automation"):

1. Create folder: `templates/types/automation/`

2. Create `_type.yaml`:
```yaml
name: Automation
description: Automate repetitive workflows
keywords:
  - automate
  - automation
  - workflow
  - schedule
  - cron

discovery:
  inline: true

mental_models:
  after_discovery: true
  models:
    - first-principles
    - pre-mortem
  max_rediscovery_rounds: 1
```

3. Create `plan.md` template with automation-specific sections

4. Create `steps.md` template with automation phases

5. Create `discovery.md` with questions:
```markdown
## Automation Discovery

### Current State
- What process are you automating?
- How is it done manually today?
- How often does it run?

### Trigger
- What triggers this automation?
- Time-based? Event-based? Manual?

### Inputs/Outputs
- What data goes in?
- What should come out?

### Error Handling
- What happens if it fails?
- Who should be notified?
```

**That's it. Router auto-discovers from folder structure.**

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Router | **MANDATORY** | Single entry point, consistent quality |
| Direct skill invocation | **DEPRECATED** | Forces mental models, prevents shortcuts |
| Template structure | **types/{type}/ folder** | Self-contained, auto-discoverable |
| Discovery timing | **BEFORE mental models** | Can't stress-test what you don't understand |
| Mental model timing | **AFTER discovery** | Informed questioning, not abstract |
| Mental model loading | **DYNAMIC via skill** | Not hardcoded in _type.yaml |
| Re-discovery | **Max 2 rounds** | Prevent over-planning, note unknowns |
| Scope handling | **AI judges naturally** | No sub-types, trust AI judgment |
| Naming | **Keep "Project"** | Distinct enough from Claude/ChatGPT |
| Type detection | **SEMANTIC from description** | No keyword triggers needed |
| Discovery output | **02-discovery.md MANDATORY** | Preserves intelligence across compaction |
| Resume context | **DYNAMIC updates every phase** | Enables proper reload |
| Sub-skill loading | **EXPLICIT bash commands** | `nexus-loader.py --skill X` |
| Steps | **ENFORCEMENT MECHANISM** | AI forgets; steps don't |
| Process vs Skill | **KEEP SEPARATE** | Process=workflow, Skill=new capability |
| Requirements format | **EARS patterns (Build/Skill)** | Battle-tested at Amazon scale |
| Quality rules | **INCOSE (Build/Skill)** | Industry standard for requirement quality |
| Task checkpoints | **ALL types** | Verification points every 3-5 tasks |
| Optional tasks | **`*` postfix marking** | Allow skipping non-critical tasks |

---

## Migration: Existing Skills

### add-integration

**Current behavior**: 7 steps, creates project, scaffolds integration

**New behavior**:
- Add `entry_mode` check at start
- When `entry_mode == from_router`:
  - Skip Step 1 (project creation) - router did this
  - Skip Step 6 (project setup) - router did this
  - Return `discovery_output` instead of continuing to scaffold
- Direct invocation: Show deprecation notice

### create-research-project

**Current behavior**: 13 steps, creates project, downloads papers, generates kits

**New behavior**:
- Add `entry_mode` check at start
- When `entry_mode == from_router`:
  - Skip Step 1 (project creation) - router did this
  - Continue through Step 13 (research needs all steps)
  - Return `discovery_output` with briefing/kit paths
- Direct invocation: Show deprecation notice

---

## Example Flows

### Integration Flow

```
User: "integrate hubspot"

Router:
  1. Type detection → "integration"
  2. Create project structure
  3. Route to add-integration skill

add-integration:
  - WebSearch "HubSpot API documentation"
  - Parse API docs
  - Present endpoints to user
  - User selects: contacts, deals
  - Return discovery_output

Router:
  4. Apply mental models:
     - "Given HubSpot's rate limits, what could break?"
     - "Do we need retry logic?"
     - Gap: "What about pagination?"

  5. Re-discovery:
     - "Check HubSpot pagination support"
     - Update discovery_output

  6. Finalize:
     - Populate plan.md
     - Generate steps.md
     - Ready for execution
```

### Build Flow

```
User: "build a notification system"

Router:
  1. Type detection → "build"
  2. Create project structure
  3. Inline discovery (from discovery.md):
     - "What triggers notifications?"
     - "What channels? (email, slack, push)"
     - "Who receives them?"
     - Capture as discovery_output

  4. Apply mental models:
     - "What's the minimum viable notification?"
     - "What if email service is down?"
     - "What about notification fatigue?"

  5. No re-discovery needed

  6. Finalize:
     - Populate plan.md
     - Generate steps.md
     - Ready for execution
```

---

## Implementation Phases

### Phase 1: Create Template Structure (~1 hr)
- Create `templates/types/` directory
- Create all 7 type folders with _type.yaml + templates
- Write discovery.md for inline types

### Phase 2: Update plan-project SKILL.md (~30 min)
- Simplify to router logic
- Add type detection from _type.yaml
- Add discovery → mental models → re-discovery loop
- Add template merging logic

### Phase 3: Update Specialized Skills (~30 min)
- add-integration: Add entry_mode, return discovery_output
- create-research-project: Add entry_mode, return discovery_output
- Add deprecation notices for direct invocation

### Phase 4: Testing (~30 min)
- Test router → integration → mental models → finalize
- Test router → research → mental models → finalize
- Test router → build (inline) → mental models → finalize
- Test re-discovery loop triggers correctly
- Test deprecation notices show

**Total: ~2.5 hours AI time**

---

## Open Questions (For Future)

- [ ] Should re-discovery use the same skill or a lighter "check" mode?
- [ ] How to persist discovery_output format across sessions?
- [ ] Should mental model outputs feed into steps.md task descriptions?

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1 | 2026-01-07 | Initial router pattern |
| v2 | 2026-01-07 | Discovery-first, mental models after, re-discovery loop |
| v2.1 | 2026-01-07 | **Major revision**: Steps as enforcement mechanism, mandatory 02-discovery.md, dynamic resume-context.md, dynamic mental model loading, semantic type matching (no keywords), explicit bash commands for sub-skills, added "skill" type, process vs skill separation |
| v2.2 | 2026-01-07 | **EARS/INCOSE integration**: Added EARS requirement patterns for Build/Skill types, INCOSE quality rules, Correctness Properties for property-based testing, Checkpoint tasks for all types, Optional task marking with `*` postfix, Task reference format linking to requirements |

---

## Open Questions (For Future)

- [ ] Should create-skill skill exist or can skill creation be template-only?
- [ ] How to handle SessionStart hook changes for sub-skill tracking?
- [ ] Should discovery.md template have required vs optional questions?
- [ ] Version control strategy for resources (v1, v2, etc.)?

---

*This document is the single source of truth for plan-project architecture.*
