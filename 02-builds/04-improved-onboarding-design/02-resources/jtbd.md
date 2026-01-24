# Framework 2: Jobs to Be Done (JTBD) v2

**Project**: 02-nexus-ui-wireframing
**Framework**: User Motivation Analysis
**Version**: 2.0 - Updated for Build vs Work model
**Status**: CONFIRMED

---

## Core Question

> What does the user want to ACHIEVE (not: what do they want to DO)?

---

## The User Evolution (v2)

```
BEFORE NEXUS:    100% Manual Work (doing everything yourself)
                 ↓
WITH NEXUS:      Build systems that do work FOR you
                 ↓
GOAL:            User becomes SYSTEM BUILDER, not worker

                 BUILD creates → WORK uses
```

**Key Insight**: Users don't just want AI help - they want to BUILD a system that multiplies their output.

---

## The Two Primary Jobs (v2)

### BUILD: Create Something New

**Statement**: "I want to create X with AI helping me think through it"

| Aspect | Details |
|--------|---------|
| **Type** | Finite, has clear end |
| **Difficulty** | HARD (requires thinking) |
| **Output** | Artifacts (docs, frameworks, systems) |
| **UI** | 🔨 Build tab |

### WORK: Use What Was Built

**Statement**: "Execute a skill or get help from my system"

| Aspect | Details |
|--------|---------|
| **Type** | Ongoing, repeatable |
| **Difficulty** | Easy (system does the work) |
| **Output** | Outcomes (emails sent, analyses done) |
| **UI** | 💼 Work tab |

---

## Job Categories (v2)

### Category 1: ONE-TIME SETUP JOBS

These happen during the 8-step onboarding:

| Step | Job | What's Created |
|------|-----|----------------|
| 1-3 | **Setup Memory** | goals.md, context.md |
| 4 | **Setup Workspace** | Folder structure |
| 5 | **Plan Roadmap** | Kanban with items |
| 6-7 | **First Build** | Complete Build cycle |
| 8 | **First Work** | Learn Work mode |

---

#### Job 1.1: SETUP MEMORY (Steps 1-3)

**Statement**: "Tell the system who I am and what I want to achieve"

| Aspect | Details |
|--------|---------|
| **Type** | Onboarding (chat + file drop) |
| **Difficulty** | Easy (guided conversation) |
| **Steps** | Context dump → Goals → More context |

**UI**: Onboarding-specific screens (not product UI yet)

---

#### Job 1.2: SETUP WORKSPACE (Step 4)

**Statement**: "Organize my files so AI can navigate them"

| Aspect | Details |
|--------|---------|
| **Type** | Onboarding (REAL Workspace UI) |
| **Difficulty** | Easy (AI suggests, user confirms) |
| **Output** | Folder structure familiar to business users |

**UI**: Actual 📁 Workspace tab during onboarding

---

#### Job 1.3: PLAN ROADMAP (Step 5)

**Statement**: "Define what I want to build"

| Aspect | Details |
|--------|---------|
| **Type** | Onboarding (REAL Roadmap UI) |
| **Difficulty** | Medium (thinking about priorities) |
| **Output** | Kanban board with items |

**UI**: Actual 🗺️ Roadmap tab during onboarding

---

#### Job 1.4: FIRST BUILD (Steps 6-7)

**Statement**: "Experience the full Build cycle with AI"

| Aspect | Details |
|--------|---------|
| **Type** | Onboarding (REAL Build UI) |
| **Difficulty** | Medium (learning 4-document structure) |
| **Output** | First deliverable + understanding of Build |

**UI**: Actual 🔨 Build tab (Planning → Building phases)

---

#### Job 1.5: FIRST WORK (Step 8)

**Statement**: "Use what I just built"

| Aspect | Details |
|--------|---------|
| **Type** | Onboarding (REAL Work UI) |
| **Difficulty** | Easy |
| **Output** | Understanding of Build → Work flow |

**UI**: Actual 💼 Work tab

---

### Category 2: ONGOING JOBS

These are the regular jobs users do after onboarding:

---

#### Job 2.1: ORIENT MYSELF

**Statement**: "Where am I? What's the status? What should I do next?"

| Aspect | Details |
|--------|---------|
| **Type** | Every session |
| **Difficulty** | Easy |
| **UI** | 🗺️ Roadmap tab (fixed, always available) |

**What user sees**:
- Kanban board with all Builds
- Status at a glance (IDEAS → TO-DO → PLANNING → BUILDING → DONE)
- Open Build tabs for active work

---

#### Job 2.2: BUILD SOMETHING (HARDEST JOB)

**Statement**: "I want to create X with AI helping me think through it"

| Aspect | Details |
|--------|---------|
| **Type** | Finite project work |
| **Difficulty** | HARD |
| **Frequency** | When creating something new |

**Why it's hard:**
- Requires thinking through what you actually need
- Must collaborate with AI on 4 documents
- Reading and reviewing is necessary
- Not passive - you're designing with AI

**The 4-Document Structure**:

| Document | Job within Build |
|----------|------------------|
| **01-overview.md** | Define what and why |
| **02-discovery.md** | Gather information and resources |
| **03-plan.md** | Decide approach and methodology |
| **04-steps.md** | Create task checklist for AI |

**UI**: 🔨 Build tab with document tabs + chat

---

#### Job 2.3: WORK (USE WHAT WAS BUILT)

**Statement**: "Execute skills or get copilot help"

| Aspect | Details |
|--------|---------|
| **Type** | Ongoing, repeatable |
| **Difficulty** | Easy |
| **Frequency** | Daily |

**Two modes within Work**:

1. **Skill Execution**: Trigger reusable automations
   - "Send follow-up email"
   - "Generate meeting notes"
   - Input → Execute → Output

2. **Copilot**: Ad-hoc assistance
   - "Help me analyze this interview"
   - Uses context from Memory + Workspace
   - Conversational

**UI**: 💼 Work tab with Quick Actions + chat

---

#### Job 2.4: FIND INFORMATION

**Statement**: "Locate file or fact quickly in my workspace"

| Aspect | Details |
|--------|---------|
| **Type** | Ad-hoc navigation |
| **Difficulty** | Easy |
| **UI** | 📁 Workspace tab + Quick search (⌘+K) |

---

#### Job 2.5: REVIEW NOTIFICATIONS

**Statement**: "See what happened and what needs attention"

| Aspect | Details |
|--------|---------|
| **Type** | Passive monitoring |
| **Difficulty** | Easy |
| **UI** | 📥 Inbox tab |

**What's in Inbox**:
- Build completion notifications
- AI suggestions ("Create skill from this pattern?")
- External inputs (emails, messages)

---

#### Job 2.6: UPDATE MEMORY

**Statement**: "My goals or preferences changed"

| Aspect | Details |
|--------|---------|
| **Type** | Configuration |
| **Difficulty** | Easy |
| **UI** | ⚙️ Settings |

---

## Jobs Summary (v2)

### Setup Jobs (Onboarding)

| Job | Statement | Step | UI |
|-----|-----------|------|-----|
| Setup Memory | Tell system who I am | 1-3 | Onboarding |
| Setup Workspace | Organize files | 4 | Real Workspace tab |
| Plan Roadmap | Define what to build | 5 | Real Roadmap tab |
| First Build | Create first thing | 6-7 | Real Build tab |
| First Work | Use what was built | 8 | Real Work tab |

### Ongoing Jobs

| Job | Statement | Difficulty | UI |
|-----|-----------|------------|-----|
| Orient Myself | Where am I? | Easy | 🗺️ Roadmap |
| **Build Something** | Create X | **HARD** | 🔨 Build |
| **Work** | Use/Execute | **Easy** | 💼 Work |
| Find Information | Locate file | Easy | 📁 Workspace |
| Review Notifications | What happened | Easy | 📥 Inbox |
| Update Memory | Change goals | Easy | ⚙️ Settings |

---

## Build vs Work Competitive Analysis

| Job | ChatGPT | Claude Projects | Notion AI | Nexus |
|-----|---------|-----------------|-----------|-------|
| **Build Something** | ⚠️ Chat only | ⚠️ Files + chat | ⚠️ AI assists | ✅ 4-doc structure |
| **Work/Execute** | ⚠️ Copy prompts | ⚠️ Manual repeat | ⚠️ Limited | ✅ Skills + Copilot |
| **Progress Tracking** | ❌ None | ❌ None | ⚠️ Manual | ✅ Kanban + % |
| **Reusable Automation** | ❌ None | ⚠️ Custom instructions | ⚠️ Templates | ✅ Skills |

**Key Insight**: Competitors help with individual tasks. Nexus helps BUILD SYSTEMS.

---

## Key UI Implications (v2)

### For Build Jobs:
- **4-document structure visible** - tabs for Overview, Discovery, Plan, Steps
- **Chat + Document split** - conversation alongside artifact
- **Progress clear** - which doc, which phase (PLANNING/BUILDING/DONE)
- **Feedback mechanism** - comment on document sections

### For Work Jobs:
- **Quick Actions prominent** - skills easily accessible
- **Context loaded** - Memory + Build context ready
- **Output focused** - results of skill execution clear
- **Session persistence** - can continue later

### For Navigation:
- **Fixed tabs for overview** - Roadmap, Workspace, Inbox always there
- **Multiple tabs for depth** - Open several Builds or Work sessions
- **Tab management** - Close, rename, reorder

---

## Key Changes from v1

| Aspect | v1 | v2 |
|--------|----|----|
| Primary modes | Planning vs Execution | **Build vs Work** |
| Skill access | Separate mode | Part of Work tab |
| Onboarding | Generic wizard | **8 steps with real UI** |
| Build structure | 2 phases | **3 phases + 4 documents** |
| Tab model | Mode switching | **Fixed + Multiple tabs** |

---

*JTBD Framework v2 - Updated 2026-01-13 for Build vs Work model*
