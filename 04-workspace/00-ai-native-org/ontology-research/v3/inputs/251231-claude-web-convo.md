# Claude Code Native Organization: Core Learnings

## Context

Dorian is building a Claude Code native organization—a company where Claude Code is the primary operational tool and AI agents handle baseline operations while humans provide strategic oversight.

Key projects:
- **Mutagent**: AI agent optimization startup (launching 2026, targeting YC)
- **UDWO**: Unified Digital Work Ontology framework
- **Nexus AI OS**: Memory/Projects/Skills/Workspace system

Dorian's profile: Red-Yellow (DISC). Driver who wants to win and be seen winning. Builds impressive frameworks, but the frameworks are artifacts for influence—not perfectionism. Trap: excited by vision, bored by grind.

---

## Core Insight

A Claude Code native org doesn't model domains for *understanding*. It models domains for *action*.

Traditional ontology: "What is this thing and how does it relate?"
Claude Code ontology: "What can I do here, what do I need, what do I produce?"

---

## Domain Modeling for Claude Code

### Every domain needs three things:

1. **State** — What exists (files, data, status)
2. **Operations** — What actions can be performed
3. **Transitions** — What triggers what, what flows where

### Domain schema:

```
Domain: [Name]

Purpose: [One sentence]

State:
  - [Entity]: [Location] — [Contents]

Operations:
  - [Action]: [Input] → [Output]

Triggers:
  - When [condition] → [operation]

Handoffs:
  - Produces [thing] → consumed by [domain]
  - Receives [thing] → from [domain]

Human gates:
  - [Decisions requiring human approval]

Context files:
  - [Files Claude needs to operate]
```

---

## Knowledge Representation Principles

Claude reads sequentially, has limited context, can't see everything at once.

### Principle 1: Every folder has INDEX.md
- What this folder is
- What files are here
- What to read first
- What operations are possible

### Principle 2: Every file has frontmatter
```yaml
---
type: audience
domain: marketing
status: active
updated: 2025-01-15
related: [file1.md, file2.md]
---
```

### Principle 3: Structured entity files
Not prose. Parseable fields Claude can read and update.

### Principle 4: Explicit links
Bad: "See the messaging doc"
Good: "/domains/marketing/messages.md#flying-blind"

### Principle 5: Operation specs in DOMAIN.md
Full specification: purpose, inputs, outputs, steps, logging requirement.

---

## Task Representation

Tasks must be: parseable, stateful, atomic.

```yaml
---
id: task-2025-01-15-001
type: task
domain: marketing
status: pending | in-progress | blocked | done | failed
assigned: claude
priority: high
depends-on: []
---

# Task: [Title]

## Objective
[What to do]

## Inputs
[File paths]

## Outputs
[Where to save]

## Acceptance criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Log
[Claude appends here]
```

---

## Action Tracking

Every action logged. Non-negotiable.

```markdown
## 2025-01-15T09:34:22Z

- action: draft_post
- domain: marketing
- task: task-2025-01-15-001
- inputs: [list]
- outputs: [list]
- status: success
- duration: 45s
- notes: none
```

Recommendation: One file per action, not append-only log (reduces corruption).

---

## Critical Realities About Claude Code

Claude is not a reliable worker. It's a brilliant improviser with amnesia.

| Assumption | Reality |
|------------|---------|
| Claude follows protocols | ~70% of the time |
| Claude logs consistently | Will forget, format wrong |
| Claude navigates correctly | Will hallucinate paths |
| Claude manages its own queue | Will forget to move files |

### Implications:
- Put PROTOCOL.md in system prompt, not just file system
- One file per action (not append)
- External orchestration or audit mechanisms
- Error recovery procedures needed
- Context window management required

---

## Speed at Scale

### Three levers:
1. Reduce Claude's decision surface
2. Reduce your review burden
3. Parallelize what can be parallel

### Reduce decisions:
- Templates with blanks, not open generation
- Enums for all categorical fields
- Pre-computed CONTEXT.md per domain

### Reduce review:
- Tier tasks: None / Async / Sync
- Spot-check 20-30%, don't review all
- Auto-approve after timeout

### Parallelize:
- Batch similar tasks
- Daily pipelines, not ad-hoc
- Prompt library for tested operations

---

## The Five Improvement Loops

### Loop 1: Task (Every Execution)
Capture: execution data + Claude self-assessment
```
- instruction_clarity (1-5)
- context_sufficiency (1-5)
- output_confidence (1-5)
- noted_issues
```

### Loop 2: Batch (End of Batch)
Claude synthesizes patterns across similar tasks.
Output: common issues, anomalies, suggested improvements.

### Loop 3: Daily (End of Day)
Aggregate batches + connect to human review decisions.
Key: identify discrepancies (Claude confident but human rejected, vice versa).

### Loop 4: Weekly (End of Week)
Strategic analysis: trends, persistent issues, outcome attribution.
Make 1-2 system changes based on evidence.

### Loop 5: Monthly (End of Month)
Zoom out: Is the system working? What's the trajectory?
Strategic decisions about scaling, new domains, automation.

---

## Minimum Viable System

Start with 5 files only:

```
/company/context.md          — One paragraph
/domains/marketing/DOMAIN.md — One operation
/tasks/current.md            — One task
/logs/actions.md             — Empty
/system/PROTOCOL.md          — 10 lines max
```

### PROTOCOL.md (complete):
```
1. Read /tasks/current.md
2. Read DOMAIN.md for relevant domain
3. Execute operation specified
4. Save output to location specified
5. Log what you did to /logs/actions.md
6. Update task status to done
```

Then: run tasks, watch failures, fix only what breaks.

---

## Minimum Viable Improvement Loop

**Per-task:** Self-assessment appended to every action log.

**Daily (5 min):** Claude summarizes logs, identifies top 3 issues.

**Weekly (30 min):** Review synthesis. Make 1-2 changes. Log changes.

---

## The Improvement Hierarchy

Change at highest layer that solves the problem:

| Layer | Change Frequency |
|-------|------------------|
| Prompts/templates | Weekly |
| Context files | Weekly |
| Examples | Weekly |
| Operation specs | Bi-weekly |
| Domain structure | Monthly |
| Protocol | Quarterly |

Bad output? Fix prompt first. Don't restructure the domain.

---

## File Structure (Evolved)

```
/
├── .claude/
│   ├── PROTOCOL.md          — Operating instructions
│   ├── SCHEMAS.md           — File templates
│   ├── ERRORS.md            — Error recovery
│   └── CONTEXT.md           — What to load per operation
│
├── company/
│   ├── context.md
│   ├── voice.md
│   └── positioning.md
│
├── domains/
│   └── {domain}/
│       ├── INDEX.md
│       ├── DOMAIN.md
│       ├── CONTEXT.md       — Pre-computed context
│       ├── inbox/           — Incoming handoffs
│       └── review/          — Pending human approval
│
├── tasks/
│   ├── queue.md             — Single source of truth
│   └── archive/
│
├── logs/
│   ├── actions/             — One file per action
│   ├── batches/
│   ├── daily/
│   ├── weekly/
│   └── outcomes/
│
├── prompts/                  — Versioned, tested prompts
│
└── review/
    ├── pending/
    └── decisions/
```

---

## Knowledge Engineering Reading Path

### Phase 1: Foundations
- *Thinking in Systems* — Donella Meadows
- *Women, Fire, and Dangerous Things* — George Lakoff

### Phase 2: Practical Modeling
- *Data and Reality* — William Kent (most important)
- *Domain-Driven Design* — Eric Evans

### Phase 3: Deeper (optional)
- *The Knowledge Graph Cookbook* — Blumauer
- *Analysis Patterns* — Martin Fowler

### Non-book learning:
- Model 10 different domains
- Rebuild same domain 3 times
- Explain model to someone
- Use model in code/tooling
- Study existing schemas (schema.org, FHIR)

---

## Key Terminology

| Term | Definition |
|------|------------|
| Taxonomy | Classification into categories (tree) |
| Ontology | Categories + relationships (graph) |
| Schema | Template defining what properties something has |
| Entity | A distinct thing in your system |
| Attribute | A property of an entity |
| Relation | How entities connect |
| Knowledge Graph | Facts + relationships you can query |
| Domain | Bounded area of knowledge/business |
| Ubiquitous Language | Agreed meanings for terms within a domain |
| Bounded Context | Where a particular domain model applies |

---

## Common Traps

| Trap | Fix |
|------|-----|
| Building full structure before testing | Start with 5 files, run tasks, fix what breaks |
| Optimizing based on execution only | Track quality + outcomes, not just completion |
| Claude improving "itself" | Claude executes → System captures → Analysis → Human approves → System updates |
| Append-only logs | One file per action |
| Reviewing everything | Tier + spot-check + auto-approve |
| Changing too much at once | One change per cycle, attribute effects |

---

## The Meta-Rule

```
Don't add structure until you feel the pain of not having it.
```

Every file created before needed is debt. The system emerges from reps, not architecture.

---

## What Success Looks Like

```
Morning:
- Open /today.md
- Lists batches to run
- Claude executes
- Outputs land in /review

Evening:
- Scan /review (5 min)
- Approve/reject
- Claude processes
- Done
```

You touch the system twice a day. Claude does the rest.