# Architecture v2: Mandatory Router + Template-First + Discovery-First

**Date**: 2026-01-07
**Status**: APPROVED
**Supersedes**: architecture-decision.md, revised-architecture.md, mental-models-analysis.md, template-system-design.md

---

## Executive Summary

plan-project becomes the **mandatory router** for all project creation. Templates define types. Discovery happens **before** mental models. Skills are discovery engines that return structured data.

---

## Core Principles

1. **Router is MANDATORY** - All project creation goes through plan-project
2. **Templates define types** - Add a type by adding a folder (no code changes)
3. **Discovery BEFORE mental models** - Can't stress-test what you don't understand
4. **Skills are discovery engines** - They return structured data, not finished plans
5. **Discovery ↔ Think loop** - Mental models may trigger re-discovery
6. **AI scales naturally** - No sub-types or scope parameters, AI judges depth

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

## Full Flow

```
plan-project (MANDATORY ROUTER)
    │
    │ ══════════════════════════════════════
    │ PHASE 1: SETUP
    │ ══════════════════════════════════════
    │
    ├── Step 1.1: Type Detection
    │   └── Match user input against templates/types/*/_type.yaml keywords
    │   └── OR ask user to select type
    │
    ├── Step 1.2: Create Project Structure
    │   └── Run init_project.py --type {type}
    │   └── Creates: 01-planning/, 02-resources/, 03-working/, 04-outputs/
    │
    ├── Step 1.3: Load Templates
    │   └── Copy plan.md template → project/01-planning/03-plan.md
    │   └── Copy steps.md template → project/01-planning/04-steps.md
    │
    │ ══════════════════════════════════════
    │ PHASE 2: DISCOVERY (First Pass)
    │ ══════════════════════════════════════
    │
    ├── Step 2.1: Check _type.yaml for discovery.skill
    │   │
    │   ├── HAS SKILL (integration, research)
    │   │   └── Route to skill with:
    │   │       - entry_mode: "from_router"
    │   │       - project_path: "02-projects/XX-name/"
    │   │   └── Skill performs discovery (WebSearch, paper-search, etc.)
    │   │   └── Skill returns: discovery_output (structured YAML/JSON)
    │   │
    │   └── NO SKILL (build, content, strategy, process, generic)
    │       └── Use discovery.md template
    │       └── Ask questions inline
    │       └── Capture answers as discovery_output
    │
    ├── Step 2.2: Populate Discovery Section
    │   └── Write discovery_output to plan.md "Discovery" section
    │
    │ ══════════════════════════════════════
    │ PHASE 3: MENTAL MODELS (Informed by Discovery)
    │ ══════════════════════════════════════
    │
    ├── Step 3.1: Load Mental Models for Type
    │   └── Read mental_models from _type.yaml
    │   └── Offer 2-3 relevant models to user
    │
    ├── Step 3.2: Apply Mental Models to Discovery
    │   │
    │   ├── First Principles
    │   │   └── "Given what we found, what's truly essential?"
    │   │   └── "Are we overcomplicating this?"
    │   │
    │   ├── Devil's Advocate
    │   │   └── "Given these constraints, what could break?"
    │   │   └── "What are we not considering?"
    │   │
    │   ├── Pre-Mortem
    │   │   └── "Given this plan, imagine it failed. Why?"
    │   │   └── "What early warning signs would we see?"
    │   │
    │   └── Success Criteria
    │       └── "How will we know this worked?"
    │       └── "What's the minimum viable outcome?"
    │
    ├── Step 3.3: Identify Gaps
    │   └── "Do we need more information about X?"
    │   └── gaps = list of unknowns
    │
    │ ══════════════════════════════════════
    │ PHASE 4: RE-DISCOVERY (If Needed)
    │ ══════════════════════════════════════
    │
    ├── IF gaps exist AND iteration < 2:
    │   └── Route back to skill OR ask inline questions
    │   └── Update discovery_output
    │   └── Return to Phase 3
    │
    ├── ELSE IF gaps exist AND iteration >= 2:
    │   └── Log unknowns in plan.md "Open Questions" section
    │   └── Proceed to finalization
    │
    │ ══════════════════════════════════════
    │ PHASE 5: FINALIZATION
    │ ══════════════════════════════════════
    │
    ├── Step 5.1: Merge All Into plan.md
    │   └── Discovery findings
    │   └── Mental model outputs (success criteria, risks)
    │   └── Open questions / unknowns
    │
    ├── Step 5.2: Generate steps.md
    │   └── Use steps.md template
    │   └── Fill in concrete tasks from discovery
    │
    └── Step 5.3: Project Ready for Execution
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
description: string               # When to use this type
keywords: string[]                # Trigger words for auto-detection

# Discovery configuration
discovery:
  skill: string                   # Skill to route to (optional)
  entry_mode: from_router         # Required if skill specified
  skip_steps: number[]            # Steps to skip in target skill
  inline: boolean                 # Use discovery.md (default if no skill)

# Mental models configuration
mental_models:
  after_discovery: true           # Always true in v2
  models: string[]                # Which models to offer
  max_rediscovery_rounds: number  # Default: 2
```

### Example: integration/_type.yaml

```yaml
name: Integration
description: Connect external APIs and services to Nexus
keywords:
  - integrate
  - integration
  - API
  - connect
  - webhook
  - oauth

discovery:
  skill: add-integration
  entry_mode: from_router
  skip_steps: [1, 6]

mental_models:
  after_discovery: true
  models:
    - first-principles
    - devils-advocate
    - pre-mortem
  max_rediscovery_rounds: 2
```

### Example: build/_type.yaml

```yaml
name: Build
description: Create new software, features, or systems
keywords:
  - build
  - create
  - implement
  - develop
  - feature

discovery:
  inline: true

mental_models:
  after_discovery: true
  models:
    - first-principles
    - stakeholder-mapping
    - pre-mortem
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
| **integration** | Skill (add-integration) | Needs WebSearch, API parsing |
| **research** | Skill (create-research-project) | Needs paper-search, downloads |
| **build** | Inline (discovery.md) | Just questions about requirements |
| **strategy** | Inline (discovery.md) | Decision framework questions |
| **content** | Inline (discovery.md) | Creative brief questions |
| **process** | Inline (discovery.md) | Current/future state questions |
| **generic** | Inline (discovery.md) | Minimal questions |

**Integration and research need skills because they fetch external data.**
**Other types just need good questions.**

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
| Re-discovery | **Max 2 rounds** | Prevent over-planning, note unknowns |
| Scope handling | **AI judges naturally** | No sub-types, trust AI judgment |
| Naming | **Keep "Project"** | Distinct enough from Claude/ChatGPT |
| Skills return | **Structured data** | Router handles prose generation |

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

---

*This document is the single source of truth for plan-project architecture.*
