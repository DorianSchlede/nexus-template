# Nexus-v3 Product Overview

**The Claude Code Operating System**

---

## What is Nexus?

Nexus transforms Claude from a stateless tool into a **persistent, organized operating system** for knowledge work.

### The Core Problem

**Without Nexus:**
- AI forgets everything every session
- Files scattered randomly everywhere
- Every workflow different and unpredictable
- Build same thing repeatedly
- Context overload, slow responses

**With Nexus:**
- AI remembers your context permanently
- Clear structure, organized files
- Consistent, reusable workflows
- Build once, use forever
- Fast, scalable system

---

## The 7 Core Problems Solved

### **1. AI Amnesia**

**Problem:**  
AI forgets everything every session. You re-explain the same context repeatedly.

**Nexus Solution:**  
`01-memory/goals.md` stores your role, criteria, and patterns. Auto-loaded every session. Zero re-explaining.

---

### **2. File Chaos**

**Problem:**  
When you just do stuff with Agentic Coding, the AI just generates files all over the place. Files scattered randomly. Can't find anything. AI can't find anything.

**Nexus Solution:**  
5-folder system with clear boundaries. `workspace-map.md` tracks everything. AI knows where to look.

---

### **3. Inconsistent Results**

**Problem:**  
AI improvises to complete tasks differently every time if you don't provide clear instructions and repeated context blocks. This leads to inconsistent results.

**Nexus Solution:**  
Skills = saved workflows with exact steps. AI executes, doesn't interpret. 95%+ quality.

---

### **4. Repeated Work**

**Problem:**  
Build same workflow multiple times. No reuse. Time wasted.

**Nexus Solution:**  
Create skill once, trigger with keywords, reuse forever. 50% time savings.

---

### **5. Context Overload**

**Problem:**  
Loading everything at once. Slow startup, degraded quality. Can't scale.

**Nexus Solution:**  
Progressive loading: Metadata at startup, full content on-demand. 80% faster, scales to 100+ skills.

---

### **6. Hard to Learn**

**Problem:**  
Steep learning curve. No clear path. Overwhelming complexity.

**Nexus Solution:**  
Pedagogically-guided 1-hour onboarding. Experience-first learning. Clear mental models.

---

### **7. Immediate Execution Without Planning**

**Problem:**  
AI always wants to execute immediately unless you put it into a clear planning framework. This leads to:
- Rushed implementations without proper requirements
- Missing edge cases and design considerations
- Rework and wasted time
- Surface-level solutions that don't address root problems

**Nexus Solution:**  
**Interactive project planning mode** enables you to express exactly what you want and get the best out of AI:

- **Planning Session (20 mins - 4 hours):** Collaborate with AI to define requirements, design, and tasks
- **Review artifacts:** Read all planning documents to ensure completeness
- **Trust the implementation:** AI executes autonomously for 20 minutes with crystal-clear requirements
- **Result:** 95%+ quality implementations that solve the real problem

**The Pattern:**
```
Session 1 (Planning - 20-30 min):
- Create project structure (init_project.py)
- Collaboratively fill overview.md (purpose, success criteria, context)
- Define plan.md with AI-guided mental models:
  * Socratic questioning to surface assumptions
  * Devil's Advocate to identify risks
  * Dependency research to find related files/systems
- Break down steps.md (execution checklist)
- NO IMPLEMENTATION

Session 2 (Implementation):
- Load planning files (crystal-clear requirements)
- Execute end-to-end
- Runs autonomously 20+ minutes
- Minimal intervention needed
```

**Benefit:** Planning optimized for deep thinking. Implementation optimized for execution. Mental models ensure quality. No context pollution.

---

### The 5-Folder Operating System

```
Nexus-v3/
│
├── 00-system/                    ← KERNEL (AI manages this)
│   ├── core/
│   │   ├── nexus-loader.py      ← Bootloader (loads context)
│   │   ├── orchestrator.md      ← Kernel instructions
│   │   └── init-memory.py       ← Memory initialization
│   ├── skills/                   ← System skills
│   │   ├── create-project/
│   │   ├── create-skill/
│   │   ├── close-session/
│   │   └── validate-system/
│   └── documentation/
│
├── 01-memory/                    ← LONG-TERM MEMORY (Hard Drive)
│   ├── goals.md                 ← Your role & objectives
│   ├── roadmap.md               ← Strategic plans
│   ├── core-learnings.md        ← Patterns discovered
│   └── session-reports/         ← Session logs
│
├── 02-projects/                  ← BOUNDED CONTEXTS (Active Processes)
│   └── {ID}-{name}/
│       ├── 01-planning/         ← Purpose, plan, execution steps
│       ├── 02-resources/        ← Reference materials
│       ├── 03-working/          ← Work-in-progress files
│       └── 04-outputs/          ← Final deliverables
│
├── 03-skills/                    ← APPLICATIONS (Executables)
│   └── {skill-name}/
│       └── SKILL.md             ← Workflow definition
│
└── 04-workspace/                 ← USER SPACE (Home Directory)
    ├── workspace-map.md         ← Your folder guide
    └── [Your folders]/          ← Organize as you want
```

---

## Core Concepts

### **Projects**

**What:** Temporal work with beginning, middle, end  
**When:** Building something specific (workflow, analysis, deliverable)  
**Structure:** 4 folders (planning → resources → working → outputs)  
**Lifecycle:** PLANNING → IN_PROGRESS → COMPLETE → ARCHIVED

**Example:**
```
02-projects/01-lead-qualification/
  ├── 01-planning/
  │   ├── overview.md       # Purpose, success criteria, context, timeline
  │   ├── plan.md           # Approach, decisions, dependencies, mental models
  │   └── steps.md          # Execution checklist with phases (state tracking)
  ├── 02-resources/         # Reference materials
  ├── 03-working/           # Work-in-progress files
  └── 04-outputs/           # Final deliverables
```

---

### **Skills**

**What:** Reusable workflows triggered by keywords  
**When:** Doing something repeatedly (reports, analysis, workflows)  
**Format:** SKILL.md with exact steps  
**Trigger:** Natural language keywords

**Example:**
```markdown
# Weekly Status Report Skill

## Trigger
"status report", "weekly update", "progress summary"

## Workflow
1. Load goals.md for current objectives
2. Scan session-reports/ from last 7 days
3. Extract completed tasks from projects
4. Generate summary with metrics
5. Save to workspace/reports/
```

**Usage:**
```
You: "Generate status report"
AI: [Loads skill, follows exact steps, produces report]
```

---

### **Memory**

**What:** Context that persists across sessions  
**Where:** `01-memory/` folder  
**Auto-loaded:** Every session via `nexus-loader.py --startup`

**Key Files:**
- **goals.md**: Your role, objectives, work patterns
- **roadmap.md**: Strategic plans, milestones
- **core-learnings.md**: Insights accumulated over time
- **session-reports/**: Auto-generated session summaries

**Benefit:** AI remembers you. No re-explaining.

---

## How Nexus Works

### The 3-Step Session Pattern

**Step 1: AI Loads Your Context** (2 seconds)
```
When you start:
1. AI runs: nexus-loader.py --startup
2. Loads: goals.md, roadmap.md, workspace-map.md
3. Scans: All project metadata, all skill metadata
4. AI knows: Who you are, what exists, what's available
```

**Step 2: You Work Together**
```
You: "Work on lead qualification"
AI: [Loads project planning files]
AI: "I see you're 48% complete (12/25 tasks). Let's continue..."
You: Build, create, analyze
AI: Saves work to appropriate folders
```

**Step 3: AI Saves Everything** (30 seconds)
```
You: "Done"
AI: [Runs close-session skill]
    - Updates task completion
    - Validates workspace-map.md
    - Creates session report
    - Cleans temp files
```

**Next Session:**
```
AI: [Loads everything automatically]
AI: "Welcome back. Yesterday you completed tasks 1-5.
     You decided to use Python. Let's continue with task 6."
```

---

## Navigating Nexus

### **Starting a Session**

Every session begins the same way:
1. AI loads `orchestrator.md`
2. AI runs `nexus-loader.py --startup`
3. AI displays menu with:
   - Your goals
   - Active projects
   - Available skills
   - Suggested next steps

### **Working with Projects**

**Create a project:**
```
You: "Create a project for [goal]"
AI: [Runs create-project skill]
    - Offers project type (Build, Research, Strategy, Content, Process)
    - Runs init_project.py (auto-assigns ID, creates structure)
    - Guides collaborative planning:
      * overview.md (purpose, success criteria, context)
      * plan.md (approach + mental models: Socratic, Devil's Advocate, dependency research)
      * steps.md (execution checklist)
    - Saves for separate execution session
```

**Work on a project:**
```
You: "Work on [project name]"
AI: [Loads project planning files]
    - Shows current status
    - Shows next task
    - Continues where you left off
```

**Complete a project:**
```
You: "Finalize [project]"
AI: - Moves files to outputs/
    - Marks all tasks complete
    - Creates final documentation
```

### **Working with Skills**

**Create a skill:**
```
You: "Create a skill for [workflow]"
AI: [Runs create-skill skill]
    - Extracts workflow steps
    - Defines trigger keywords
    - Saves to 03-skills/
    - Immediately available next session
```

**Use a skill:**
```
You: [Say trigger keyword]
AI: [Loads skill, executes workflow]
    - Follows exact steps
    - Same result every time
    - Saves output appropriately
```

### **Ending a Session**

**Always end with:**
```
You: "Done"
AI: [Runs close-session]
    - "Which tasks did you complete?"
    - "Any important decisions?"
    - Saves everything
    - Creates session report
```

**Why it matters:**
- Progress saved
- Memory updated
- Context preserved for next session
- Workspace validated

---

## Key Innovations

### **1. Instruction-Driven Architecture**

**Traditional AI:**
```
You: "Create a project"
AI: [Interprets, improvises, inconsistent]
```

**Nexus:**
```
You: "Create a project"
AI: [Loads create-project/SKILL.md, executes exactly]
Result: 100% consistent
```

### **2. Progressive Loading**

**At Startup:** Load metadata only (~1,000 words)  
**When Triggered:** Load full content (~500 words per skill)  
**On-Demand:** Load helper files (as needed)

**Benefit:** Fast startup, efficient memory, scales to 100+ skills

### **3. Script-First Automation**

**Traditional:**
```
AI generates folders manually (5 min, variable quality)
```

**Nexus:**
```
Python script creates structure (5 sec, consistent quality)
```

### **4. Context Preservation**

**close-session workflow:**
1. Update tasks (which completed?)
2. Validate workspace (folders match map?)
3. Save decisions (what did you decide?)
4. Create report (session summary)
5. Clean up (move files, remove temp)

**Next session:** AI loads everything, continues seamlessly

---

## Common Workflows

### **Daily Work Pattern**

```
Morning:
1. Start session (AI loads context)
2. Review suggested next steps
3. Continue active project or start new one

During Work:
4. Use skills for repeated tasks
5. Create new skills when patterns emerge
6. AI saves work continuously

End of Day:
7. Say "done"
8. AI runs close-session
9. Everything saved for tomorrow
```

### **Weekly Pattern**

```
Monday-Thursday: Execute projects
Friday: Create skills from patterns discovered
Monthly: Review core-learnings.md, update roadmap.md
```

---

## Best Practices

### **Do:**
✅ Always end sessions with "done" (run close-session)  
✅ Create skills for anything you do twice  
✅ Fill in planning files before building  
✅ Use natural language (AI routes to correct skill/project)  
✅ Update goals.md as objectives evolve

### **Don't:**
❌ Skip close-session (progress won't save)  
❌ Create projects without planning first  
❌ Manually organize files (let AI follow structure)  
❌ Re-explain context (it's in goals.md)

---

## Getting Help

### **Understanding the System**

- **This file**: High-level overview
- **framework-overview.md**: Complete technical guide
- **system-map.md**: Navigation and structure reference

### **Learning to Use It**

- **Onboarding**: 4 projects, 1 hour, full mastery
- **Skills**: create-project, create-skill, close-session
- **Menu**: Shows suggested next steps every session

### **Troubleshooting**

```
You: "Validate system"
AI: [Runs validate-system skill]
    - Checks folder structure
    - Validates workspace-map.md
    - Confirms all files present
    - Reports any issues
```

---

## Summary

**Nexus in 3 Sentences:**

1. **Nexus gives AI memory** - Remembers your role, workflows, and decisions permanently
2. **Nexus provides structure** - Clear 5-folder system, consistent project templates, organized files
3. **Nexus enables reuse** - Save workflows as skills, trigger with keywords, use forever

**Time to Value:** 1 hour onboarding → Immediate productivity

**ROI:** 12 hours/week saved per person | 95% quality | Infinite scalability

**Bottom Line:** Turns Claude from a powerful tool into a systematic operating system for knowledge work.

---

**Ready to start?** Say "create project" to start working, or "setup goals" to personalize first. AI will guide you.
