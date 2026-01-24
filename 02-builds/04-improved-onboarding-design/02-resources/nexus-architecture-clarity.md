# Nexus Architecture Clarity

**Purpose**: Document fundamental architectural insights discovered during contextual learning planning.

---

## Core Definitions

### SKILL = Execute Work
**Skills are executable capabilities** - the tools that DO the work.

```
Examples:
- weekly-report SKILL → Generates report (execution)
- qualify-lead SKILL → Processes lead (execution)
- format-doc SKILL → Formats document (execution)
```

**Skills execute on workspace materials** to produce outputs.

### BUILD = Build Your System
**Builds are the PROCESS of creating capabilities** for your system.

```
Examples:
- BUILD a skill → Create reusable workflow
- BUILD an integration → Connect external service
- BUILD content → Create deliverable
- BUILD research → Conduct analysis
```

**"Let's start building"** - not "let's create builds"

---

## The Fundamental Insight

**OLD FRAMING** (Confusing):
```
Builds vs Skills
(Implies they're opposites or alternatives)
```

**NEW FRAMING** (Clear):
```
BUILD system capabilities
  ├─ Type: skill (executable workflow) ⭐ MOST IMPORTANT
  ├─ Type: integration (API connection)
  ├─ Type: research (analysis)
  ├─ Type: strategy (business planning)
  ├─ Type: content (creative deliverable)
  ├─ Type: process (workflow optimization)
  ├─ Type: build (software/features)
  └─ Type: generic (other)
```

**Skills are ONE type of build** - the most important one for recurring work.

---

## User Journey Examples

### Example 1: Weekly Reports

**User says**: "Ich brauche jeden Montag einen Report"

**System thinks**: "Let's BUILD that capability"

```
plan-build → Type: skill
    ↓
BUILD PROCESS:
  - Define workflow steps
  - Create template
  - Set up triggers
  - Document execution
    ↓
OUTPUT: weekly-report SKILL (in 03-skills/)
    ↓
NEXT MONDAY: Execute skill
  - Read from 04-workspace/ (data)
  - Generate report
  - Write to 04-workspace/ (output)
```

### Example 2: Recipe Book

**User says**: "Hilf mir mit meinem Rezeptbuch"

**System thinks**: "Let's BUILD that"

```
plan-build → Type: content
    ↓
BUILD PROCESS:
  - Define structure
  - Plan sections
  - Set milestones
    ↓
OUTPUT: Completed recipe book (in 04-workspace/)
```

---

## The 5-Folder Architecture

```
NEXUS:
├─ 00-system/         → Nexus core (skills, hooks, templates)
├─ 01-memory/         → System state (goals, learnings, config)
├─ 02-builds/         → BUILD PROCESSES (creating capabilities)
│  └─ Each build has planning, resources, working, outputs
├─ 03-skills/         → EXECUTABLE CAPABILITIES (you built these)
│  └─ Each skill ready to execute on workspace materials
└─ 04-workspace/      → YOUR STUFF
   ├─ Context store (files, notes, research)
   ├─ Build area (where things are created)
   └─ Material for skills (input/output for execution)
```

---

## Workspace Role

**WORKSPACE = Multi-Purpose Space**

1. **Context Store**
   - Your files, notes, research
   - Project materials
   - References

2. **Build Area**
   - Where content is created
   - Where outputs are generated
   - Work-in-progress files

3. **Material for Skills**
   - INPUT: Skills read from workspace (data, templates)
   - OUTPUT: Skills write to workspace (reports, documents)

**Example Flow**:
```
04-workspace/data/sales-2024.csv  (input)
    ↓
Execute: weekly-report SKILL
    ↓
04-workspace/reports/week-51.md   (output)
```

---

## plan-build = Core Workflow

**plan-build is the GATEWAY for everything** you want to build.

**User NEVER says**:
- "Erstelle einen Skill"
- "Mache ein Build"
- "Create Type X"

**User says naturally**:
- "Ich brauche jeden Montag einen Report"
- "Hilf mir mit meinem Rezeptbuch"
- "Verbinde Slack"
- "Analysiere Competitors"

**Nexus routing detects intent** → Always loads plan-build → plan-build detects TYPE → Guides through appropriate build process.

---

## Why Skills are Special

**Skills = Repeating Executable Work**

Skills are the MOST IMPORTANT build type because:
- They compound over time (build once, use forever)
- They eliminate repeated manual work
- They capture institutional knowledge
- They ensure consistency

**3-Criteria Framework** (when to build a skill):
1. **FREQUENCY**: 2+ times per month?
2. **REPEATABILITY**: Steps mostly the same?
3. **VALUE**: Saves >5 minutes per execution?

ALL 3 YES = Build a skill!

---

## Language Matters

**DON'T SAY**:
- "Create a build" (confusing noun)
- "Builds vs Skills" (false dichotomy)
- "Load builds lesson" (unclear)

**DO SAY**:
- "Let's start building" (action)
- "What are you building?" (process)
- "Building capabilities" (system development)
- "Skills are executable workflows you build" (clarity)

---

## Gateway Lesson Implications

The first-time learning experience should teach:

1. **Nexus = Building System** (for work capabilities)
2. **8 Types of Builds** (what you can build)
3. **Skills = Most Important** (recurring executable work)
4. **plan-build Guides You** (structured process)
5. **Workspace = Your Materials** (input/output for everything)

**NOT "Builds vs Skills"** - that framing creates confusion.

**YES "Building your system, especially skills"** - that's clear.

---

## Summary

```
BUILD = Process (creating capabilities)
SKILL = Capability (executing work)
WORKSPACE = Materials (context + work area)
plan-build = Guide (structured building process)
```

**Nexus helps you BUILD a personalized work system, where SKILLS are the most valuable capabilities because they execute repeatedly on your WORKSPACE materials.**
