---
name: how-nexus-works
description: "Learn how Nexus works - the system tour. ~7 min."
onboarding: false
priority: high
duration: "7 min"
---

# How Nexus Works

Quick 7-minute tour of Nexus concepts and workflows.

## Purpose

Help users understand the core architecture of Nexus: what BUILDs and SKILLs are, how memory and workspace work, and how to use the system effectively.

**Time Estimate**: 7 minutes

---

## Workflow

### Part 1: BUILDs (2 min)

**Display**:
```
----------------------------------------------------
🏗️  PART 1: BUILDs
----------------------------------------------------

A BUILD is finite work with a clear beginning, middle, and end.

**Examples**:
[OK] Research competitor landscape → Report
[OK] Design brand strategy → Framework
[OK] Create onboarding docs → Documentation
[OK] Plan marketing campaign → Strategy

**NOT a BUILD**:
[FAIL] Weekly status reports (repeating task)
[FAIL] Daily standup notes (ongoing workflow)
[FAIL] Code formatting (repeating automation)

**Rule**: If it ENDS, it's a BUILD. If it REPEATS, it's a SKILL.

**BUILD Structure**:
02-builds/ID-name/
├── 01-planning/        # Think before you execute
├── 02-resources/       # Research & materials
├── 03-work-in-progress/# Drafts & iterations
└── 04-outputs/         # Final deliverables

**Lifecycle**:
1. 'plan build' → Define what you want
2. Planning phase → Answer discovery questions
3. 'execute build' → Work through phases
4. Completion → Deliverables in 04-outputs/
5. Archive → Moves to 02-builds/complete/

**Example**: "Research Competitors"

When you say "build competitor research", Nexus:
1. Asks: Who are your competitors? What do you want to know?
2. Creates: Planning document with research questions
3. Executes: Searches, analyzes, compiles findings
4. Delivers: competitor-analysis.md in 04-outputs/
5. Archives: Project moves to 02-builds/complete/ when done
```

**Ask**: "Do you have any questions about BUILDs so far?"

Wait for response. If user asks questions, answer them. If not, continue.

---

### Part 2: SKILLs (2 min)

**Display**:
```
----------------------------------------------------
⚡ PART 2: SKILLs
----------------------------------------------------

A SKILL is a repeatable workflow you can execute anytime.

**Examples**:
[OK] 'close session' → Save progress, create report
[OK] 'list skills' → Show available workflows
[OK] 'mental models' → Apply thinking frameworks
[OK] Integration skills (if you add Slack, Airtable, etc.)

**When to create a SKILL**:
- You'll do this task more than once
- It's a standardized workflow
- Others might reuse it

**When to create a BUILD**:
- It's one-off work with deliverables
- You want structured planning & outputs
- It has a clear completion point

**Decision Tree**:
┌─ Does it repeat?
│  ├─ YES → SKILL
│  └─ NO ┐
│        └─ Does it have deliverables?
│           ├─ YES → BUILD
│           └─ NO → Just do it (no structure needed)

**How to load skills**:
- Type the skill name: 'close session', 'mental models'
- Or browse: 'list skills'

Nexus has 50+ built-in skills, and you can create your own.
```

**Ask**: "Does the BUILD vs SKILL distinction make sense?"

Wait for response. If unclear, clarify. If clear, continue.

---

### Part 3: Memory (1 min)

**Display**:
```
----------------------------------------------------
🧠 PART 3: Memory
----------------------------------------------------

Nexus remembers you across sessions.

**Key file**: 01-memory/goals.md

Contains:
- Your role & expertise
- Short-term goals (3 months)
- Long-term vision (1-3 years)
- Work style & preferences

**How it works**:
- Set during onboarding (quick-start)
- Loaded every session automatically
- I always know your context

**Why this matters**:
Instead of:
  "I'm a PM at a B2B SaaS company building a new feature..."

You just say:
  "Help me plan the Q2 roadmap"

And I already know your role, company type, goals, and style.

**Other memory files**:
- core-learnings.md → Insights from past work
- session-reports/ → History of what we've built
- user-config.yaml → Preferences & settings
```

**Ask**: "Have you completed the quick-start onboarding?"

If NO → "I recommend completing onboarding to set up your goals and workspace"
If YES → "Great! That's why I understand your context."

---

### Part 4: Workspace (1 min)

**Display**:
```
----------------------------------------------------
[DIR] PART 4: Workspace
----------------------------------------------------

Your persistent file storage.

**Location**: 04-workspace/

This is YOUR space for:
- Documents you want me to access
- Templates & frameworks
- Project archives
- Any persistent content

**Structure**:
04-workspace/
├── input/              # Drop files here for analysis
├── templates/          # Reusable frameworks
├── projects/           # Organized work
└── workspace-map.md    # Navigation guide for AI

**workspace-map.md**:
Documents your folder structure so I can navigate efficiently.

**Example**:
```yaml
04-workspace/
├── brand-strategy/
│   ├── canvas-template.md
│   └── positioning-framework.md
├── client-projects/
│   └── acme-corp/
└── research/
    └── competitor-intel/
```

When you say "use my brand canvas template", I know exactly where to find it.

**Setup**: Workspace is configured during quick-start onboarding.
```

---

### Part 5: Sessions (1 min)

**Display**:
```
----------------------------------------------------
[SYNC] PART 5: Sessions
----------------------------------------------------

Work persists automatically. No saving required.

**How it works**:

1. **Start session**: Type 'Hi'
   → Shows menu with current work & options

2. **Do work**: Build, execute skills, chat
   → Progress auto-saves continuously

3. **Close session**: Type 'close session'
   → Creates session report
   → Captures learnings
   → Everything ready for next time

4. **Next session**: Type 'Hi'
   → Resume exactly where you left off
   → Or start new work

**Context continuity**:
- Active BUILDs → Always visible in menu
- Memory → Loaded automatically
- Workspace → Always accessible
- State → Tracked in user-config.yaml

**Example flow**:
Monday: "Build competitor research" → Plan phase → Close
Tuesday: "Hi" → Menu shows "Continue Competitor Research (40% done)" → Resume
Wednesday: Complete → Deliverables in 04-outputs/ → Archive
```

**Display**:
```
----------------------------------------------------
[OK] TOUR COMPLETE!
----------------------------------------------------

You now understand:
[OK] BUILDs → Finite work with deliverables
[OK] SKILLs → Repeatable workflows
[OK] Memory → Your persistent context (goals.md)
[OK] Workspace → Your file storage (04-workspace/)
[OK] Sessions → Work persists automatically

**Quick Reference**:
- New work with deliverables → "build [name]"
- Repeating task → "create skill [name]" or use existing
- See options → "list skills"
- Start session → "Hi"
- End session → "close session"

**Recommended next steps**:
1. Start your first BUILD: "build [what you want to create]"
2. Explore skills: "list skills"

Type 'Hi' to see the menu, or tell me what you want to work on.
```

---

## Post-Completion Actions

**Update Config**:
```python
from nexus.state_writer import update_yaml_path

config_path = "00-system/core/nexus/templates/user-config.yaml"
update_yaml_path(config_path, "learning_tracker.completed.how_nexus_works", True)
```

**Return to menu or user request**.

---

## Implementation Notes

**Tone**: Conversational, explain through examples, use visuals (trees, flows)
**Pacing**: Pause for questions between parts
**Depth**: Overview level, not deep implementation details
**Goal**: User understands the mental model of Nexus
