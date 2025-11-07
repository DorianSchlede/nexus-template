# Nexus-v3 Framework Overview

**The complete guide to understanding how Nexus-v3 works.**

> **Start Here**: If you're new to Nexus-v3, this document explains the entire system and how all pieces fit together.

---

## 🧬 Living Knowledge Organism

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║  ALL FILES IN THIS SYSTEM ARE EXECUTABLE — NOT DOCUMENTATION!         ║
║                                                                       ║
║  Every .md file, .yaml config, and planning document is designed     ║
║  to be READ, LOADED, and EXECUTED by AI in conversation.             ║
║                                                                       ║
║  This is not a static knowledge base. It's a living, breathing       ║
║  organism that guides you through work, adapts to your context,      ║
║  and evolves with every interaction.                                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

---

## 🎯 What is Nexus-v3?

**Nexus-v3 is a self-guiding work organization system** that runs entirely through conversation with Claude AI. It helps you:

- **Track temporal work** with projects (planning → execution → outputs)
- **Capture reusable workflows** with skills
- **Preserve context** across AI sessions with memory
- **Auto-detect what to load** via YAML-driven metadata
- **Never start from scratch** - the system remembers everything

### Core Philosophy

1. **Instruction-Driven**: Python script analyzes state and returns complete instructions (no AI interpretation)
2. **YAML-Driven**: Everything has metadata that describes when to load it
3. **Progressive Disclosure**: Load minimum at start, more context just-in-time
4. **State in Data**: Logic lives in data files, not code
5. **Context Preservation**: All context is saved, nothing is lost between sessions
6. **Self-Documenting**: System generates navigation from file metadata
7. **Skill-First Execution**: Skills have priority over projects in routing

---

## 🗺️ The Four Navigation Maps

Nexus-v3 has **4 specialized maps** that guide you through different aspects of the system:

### 1. [System Map](../system-map.md) 📊

**What it covers**: System framework and structure

**Use it for**:
- Understanding the folder structure
- Finding system skills (create-project, create-skill, etc.)
- Learning how the loader and orchestrator work
- Seeing the complete system architecture

**Key sections**:
- System structure diagram
- Core infrastructure (loader, orchestrator)
- System skills reference (6 built-in skills)
- YAML metadata formats
- Startup loading sequence

---

### 2. [Memory Map](../../01-memory/memory-map.md) 🧠

**What it covers**: Context persistence system

**Use it for**:
- Understanding how memory works
- Finding your goals, roadmap, and learnings
- Locating session reports
- Understanding what gets saved automatically

**Key files**:
- `goals.md` - Your objectives and success criteria
- `roadmap.md` - Short/long-term plans
- `core-learnings.md` - Patterns and insights
- `session-reports/` - Historical work summaries

---

### 3. [Project Map](../../02-projects/project-map.md) 📋

**What it covers**: System state and current focus

**Use it for**:
- Checking system initialization status
- Finding your current focus (what you were working on)
- Seeing recent decisions
- Understanding project lifecycle

**Key information**:
- System state (first_time_setup, operational, etc.)
- Onboarding status and current project
- Current focus (active project + next task)
- Recent decisions log
- Project status tracking

---

### 4. [Workspace Map](../../04-workspace/workspace-map.md) 🗺️

**What it covers**: Your custom folder structure

**Use it for**:
- Navigating your personal workspace
- Understanding your custom folder organization
- Finding client folders, research, templates, etc.

**Created during**: Project 01 (First Project) during onboarding

---

## 📁 System Structure

```
Nexus-v3/
│
├── claude.md                   🚀 LOAD THIS TO START!
│
├── 00-system/                  📊 SYSTEM FRAMEWORK
│   ├── system-map.md               Master system navigation
│   ├── core/                       Core infrastructure
│   │   ├── orchestrator.md             AI decision logic (minimal)
│   │   ├── nexus-loader.py             Context loading + decision engine
│   │   └── init-memory.py              Memory initialization script
│   ├── skills/                     System skills (6 built-in)
│   │   ├── create-project/             Project creation wizard
│   │   ├── create-skill/               Skill creation wizard
│   │   ├── add-integration/            MCP integration guide
│   │   ├── close-session/              Session cleanup & memory update
│   │   ├── validate-system/            System integrity checker
│   │   └── archive-project/            Archive completed projects
│   └── documentation/              System documentation
│       ├── framework-overview.md (THIS FILE)
│       ├── yaml-quick-reference.md
│       └── skill-file-format.md
│
├── 01-memory/                  🧠 CONTEXT PERSISTENCE
│   ├── memory-map.md               Memory system navigation
│   ├── goals.md                    Your objectives
│   ├── roadmap.md                  Plans (3/6/12 month)
│   ├── user-config.yaml            Language & preferences
│   ├── core-learnings.md           Patterns & insights
│   └── session-reports/            Historical summaries
│
├── 02-projects/                📋 TEMPORAL WORK
│   ├── project-map.md              System state & current focus
│   ├── 00-define-goals/            Onboarding Project 00 (8-10 min)
│   ├── 01-first-project/           Onboarding Project 01 (10-12 min)
│   ├── 02-first-skill/             Onboarding Project 02 (15 min)
│   ├── 03-system-mastery/          Onboarding Project 03 (10 min)
│   ├── 05-archived/                Completed projects (archive-project skill)
│   └── {ID}-{name}/                Individual user projects
│       ├── 01-planning/
│       │   ├── overview.md             YAML metadata + description
│       │   ├── requirements.md
│       │   ├── design.md
│       │   └── tasks.md                Checkbox task list (state source)
│       ├── 02-working/             Work-in-progress files
│       └── 03-outputs/             Final deliverables
│
├── 03-skills/                  🔄 USER SKILLS (custom workflows)
│   └── {skill-name}/
│       ├── SKILL.md                YAML metadata + workflow
│       ├── references/             (optional) Detailed docs
│       ├── scripts/                (optional) Automation
│       └── assets/                 (optional) Files
│
└── 04-workspace/               🗺️ USER CONTENT
    ├── workspace-map.md            Your custom folder guide
    └── [Your folders]/             Clients, research, templates, etc.
```

---

## 🚀 Instruction-Driven Architecture (Critical)

### The Master Controller Pattern

**Key Principle**: The Python script (`nexus-loader.py`) is the MASTER CONTROLLER. All orchestration logic lives there.

The script doesn't just return file lists - it returns **COMPLETE INSTRUCTIONS**:

```json
{
  "system_state": "first_time_setup",
  "files_to_load": [
    "00-system/system-map.md",
    "02-projects/project-map.md",
    "04-workspace/workspace-map.md"
  ],
  "instructions": {
    "action": "load_and_execute_project",
    "project_id": "00-define-goals",
    "execution_mode": "immediate",
    "message": "Welcome to Nexus! Starting onboarding...",
    "reason": "First time setup - goals.md not initialized",
    "workflow": [
      "Load Project 00: Define Goals",
      "Execute tasks.md in sequence",
      "Create goals.md, roadmap.md, and memory system"
    ]
  },
  "metadata": {
    "projects": [...],
    "skills": [...]
  }
}
```

### Why This Matters

**Traditional Approach** (Error-Prone):
```
AI → Detect state → Guess what to do → Load files → Execute
```

**Nexus Approach** (Bulletproof):
```
Script → Analyze state → Return instructions → AI follows exactly
```

**Benefits**:
- ✅ **Zero interpretation** - AI doesn't guess, just executes
- ✅ **Zero manual state detection** - Script handles all edge cases
- ✅ **Deterministic behavior** - Same state = Same instructions
- ✅ **Easy debugging** - Instructions are explicit and visible
- ✅ **Simple orchestrator.md** - Just "follow the instructions"

---

## 🔄 The Three-Step Startup Pattern

**EVERY session follows this bulletproof pattern:**

### Step 1: Run Startup Script

```bash
python 00-system/core/nexus-loader.py --startup
```

The script analyzes system state and returns:
- `system_state` - Current state (first_time_setup, operational, etc.)
- `files_to_load` - Array of files that exist and should be loaded
- `instructions` - Complete instructions for what to do next
- `metadata` - Projects and skills metadata (YAML scan)
- `stats` - System statistics and token counts

---

### Step 2: Load Files

Load ALL files from `files_to_load` array using Read tool (parallel):

```python
for file_path in startup['files_to_load']:
    Read(file_path)
```

**Result**: Zero "file not found" errors (script only lists files that exist)

---

### Step 3: Follow Instructions

Read `instructions.action` and execute exactly as specified:

#### Action: `load_and_execute_project`

```python
project_id = startup['instructions']['project_id']
mode = startup['instructions']['execution_mode']

# Display message
print(startup['instructions']['message'])

# Load project files
python nexus-loader.py --project {project_id}

# Read all planning files in parallel
Read: {project}/01-planning/overview.md
Read: {project}/01-planning/design.md
Read: {project}/01-planning/tasks.md

# Execute based on mode
if mode == 'immediate':
    begin_executing_tasks()
else:
    display_context_and_wait_for_user()
```

#### Action: `display_menu`

```python
display_nexus_banner()
show_goals()
show_projects()
show_skills()
wait_for_user_input()
```

#### Action: `resume_project`

```python
project_id = startup['instructions']['project_id']
load_project_and_find_next_task()
continue_from_checkpoint()
```

**That's it!** The script tells you exactly what to do. No guessing, no interpretation.

---

## 🎓 The Onboarding Journey (4 Projects, 35-40 min)

Nexus-v3 features a **pedagogically-designed onboarding** that teaches through experience, not explanation.

### Project 00: Define Goals (8-10 min) - V2.0 Redesign

**Status**: First onboarding project
**Philosophy**: **CONCRETE BEFORE ABSTRACT**

#### V2.0 Improvements

| Metric | V1.0 (Old) | V2.0 (New) | Impact |
|--------|-----------|-----------|--------|
| **Time** | 12-15 min | 8-10 min | 33% faster |
| **Vocabulary** | 15+ terms | 4 terms | 73% reduction |
| **Tasks** | 40 | 16 | 60% fewer |
| **Structure** | Abstract→Concrete | Concrete→Abstract | Grounded learning |
| **Time to value** | 12 min | 5 min | 58% faster |
| **Drop-off risk** | 35-45% | <15% | 70% improvement |

#### The Journey

**Section 0: Welcome + Language (30 seconds)**
- Simple welcome
- Language selection (enforced for ALL subsequent interactions)
- NO system complexity before context exists

**Section 1: Your Goals (5 minutes) - CONCRETE FIRST**
- What do you do? (role + work pattern)
- 3-month goal + AI suggests metrics
- 6-12 month vision + AI suggests milestones
- Confirm understanding
- **AI Suggestion Framework**: Suggest, don't prescribe. Always allow refinement.

**Section 2: Optional Context (15 seconds) - FYI ONLY**
- Brief mention of `00-input/` folder
- NO stopping, NO checking, NO pressure

**Section 3: Create Your Workspace (2 minutes) - ACTION**
- Execute `init-memory.py` with user's actual content
- Show file tree (visual confirmation)
- Brief explanations of each file
- **Experience before explanation**

**Section 4: Understanding Memory (2 minutes) - EXPLANATION**
- Explain what just happened (grounded in experience)
- Show the value (tomorrow's persistence)
- Connect to user's goal
- Introduce 4 terms: Memory, Goals, Sessions, close-session

**Section 5: Close-Session Habit (2 minutes) - CRITICAL**
- Introduce the most important habit
- Explain what close-session does
- Practice it RIGHT NOW (immediate practice)
- Execute and show it working

**Section 6: What's Next (1 minute)**
- Preview the 3 remaining sessions
- Show progress made today
- Clear next step

#### What Gets Created

By the end of Project 00:
- ✅ `01-memory/goals.md` - YOUR role, work pattern, goals
- ✅ `01-memory/roadmap.md` - YOUR milestones, metrics, priorities
- ✅ `01-memory/user-config.yaml` - YOUR language and preferences
- ✅ `02-projects/project-map.md` - Project tracking
- ✅ `01-memory/core-learnings.md` - Insight capture template
- ✅ `01-memory/session-reports/` - Session summary folder

**All files contain YOUR actual content—no placeholders!**

#### Design Principles Applied

**Learning Science**:
- **Bloom's Taxonomy**: Start at "Knowledge" level (your goals), not "Analysis" (system architecture)
- **Constructivist Learning**: Experience before explanation (grounded learning)
- **Problem-Based Learning**: Need (your goals) drives solution discovery
- **Cognitive Load Theory**: 4 terms total respects working memory limits (Miller's Law)
- **Ebbinghaus Forgetting Curve**: Experience + immediate practice = 80% retention
- **Peak-End Rule**: Peak = goals captured in 5 min, End = close-session works perfectly

---

### Project 01: First Project (10-12 min)

**Status**: Second onboarding project
**Focus**: Workspace structure + Create first real project

**What You'll Do**:
- Create workspace structure using just-in-time organization
- Learn Projects vs Skills decision framework
- Use `create-project` skill to create first real project
- Apply project planning with AI guidance

**What Gets Created**:
- ✅ `04-workspace/` custom folder structure
- ✅ `04-workspace/workspace-map.md` with your organization
- ✅ Your first real project tailored to your goals

---

### Project 02: First Skill (15 min)

**Status**: Third onboarding project (was Project 03 before consolidation)
**Focus**: Skill creation + Workflow automation

**What You'll Do**:
- Learn what skills are (reusable workflows)
- Use `create-skill` skill to capture a workflow
- AI suggests skill name based on your description
- Practice executing your first skill

**What Gets Created**:
- ✅ Your first custom skill in `03-skills/`
- ✅ Understanding of workflow automation

---

### Project 03: System Mastery (10 min)

**Status**: Fourth and final onboarding project
**Focus**: Review + AI collaboration awareness

**What You'll Do**:
- Review complete setup (goals, workspace, projects, skills)
- Learn 3 system pitfalls using YOUR actual entities
- Learn 2 AI behavioral patterns (False Progress 19%, Incomplete Reading)
- Practice detection exercises with YOUR projects
- Confirm two-layer mastery (system + AI collaboration)
- Graduate with AI awareness superpowers!

**Outcome**:
- ✅ Onboarding complete
- ✅ System mastery confirmed
- ✅ AI collaboration awareness established
- ✅ Ready for operational mode

---

## 🔄 How It All Works Together

### Session Start (Instruction-Driven)

```
1. Run: python nexus-loader.py --startup
   ↓
2. Script analyzes system state:
   - Check if goals.md exists
   - Check if onboarding complete
   - Check for current focus
   - Detect system state
   ↓
3. Script returns instructions:
   {
     "system_state": "operational",
     "files_to_load": [
       "system-map.md",
       "memory-map.md",
       "project-map.md",
       "goals.md",
       "workspace-map.md"
     ],
     "instructions": {
       "action": "display_menu"
     },
     "metadata": {
       "projects": [...],
       "skills": [...]
     }
   }
   ↓
4. AI loads all files in parallel
   ↓
5. AI follows instructions (display_menu):
   - Show Nexus banner
   - Show your goals
   - Show active projects
   - Show available skills
   - Wait for user input
```

### During Work (Skill-First Execution)

**Priority 1: Check for matching skill** (MOST IMPORTANT)

```
User: "generate status report"
  ↓
AI scans metadata.skills:
  - Match "status report" → weekly-status-report skill
  ↓
Load skill:
  python nexus-loader.py --skill weekly-status-report
  ↓
Read: 03-skills/weekly-status-report/SKILL.md
  ↓
Execute workflow in SKILL.md
```

**Priority 2: Check for project name match**

```
User: "continue working on website"
  ↓
AI scans metadata.projects:
  - Match "website" → 05-website-development
  ↓
Load project:
  python nexus-loader.py --project 05-website-development
  ↓
Read in parallel:
  - 02-projects/05-website-development/01-planning/overview.md
  - 02-projects/05-website-development/01-planning/requirements.md
  - 02-projects/05-website-development/01-planning/design.md
  - 02-projects/05-website-development/01-planning/tasks.md
  ↓
Show: Next unchecked task
  ↓
User works on task
  ↓
Context flows to project files
```

**Priority 3: General response** (Fallback - should be RARE)

```
User: "What's the weather like?"
  ↓
No skill match, no project match
  ↓
Respond naturally + suggest creating project/skill if needed
```

**This priority order is THE most important orchestration principle in Nexus.**

### Session End (close-session skill)

```
User: "done for now"
  ↓
AI triggers: close-session skill
  ↓
Skill workflow:
  1. Update project-map.md:
     - Set current focus
     - Log recent decisions
  ↓
  2. Update task progress:
     - Mark completed tasks with [x]
     - Calculate progress percentage
  ↓
  3. Create session report:
     - 01-memory/session-reports/{date}.md
     - Summary of work done
     - Decisions made
     - Next steps
  ↓
  4. Clean temp files (if any)
  ↓
  5. Confirm: "Session closed. Progress saved!"
  ↓
All context preserved for next session
```

---

## 🎯 Key Concepts

### 1. Projects (Temporal Work)

**Purpose**: Organize work with a beginning, middle, and end

**Structure**:
- `01-planning/` - What you're building (requirements, design, tasks)
- `02-working/` - Work-in-progress files
- `03-outputs/` - Final deliverables

**Lifecycle**: PLANNING → IN_PROGRESS → COMPLETING → COMPLETE → ARCHIVED

**State Source**: Checkbox list in `tasks.md`

**YAML Metadata** (in overview.md):
```yaml
---
id: 05-website-development
name: Website Development
status: IN_PROGRESS
description: Load when user mentions "website", "web dev", "homepage"
created: 2025-11-01
last_worked: 2025-11-04
tags: [web, design]
---
```

**Note**: `tasks_total`, `tasks_completed`, and `progress` are **calculated automatically** by nexus-loader from tasks.md checkboxes. **Do NOT store in YAML**.

---

### 2. Skills (Reusable Workflows)

**Purpose**: Capture repeatable workflows for common tasks

**Structure**:
- `SKILL.md` - Main workflow (<500 lines)
- `references/` - Detailed documentation
- `scripts/` - Automation code
- `assets/` - Files needed by skill

**V2.0 YAML Format** (minimal metadata):
```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update", "progress summary". Generate comprehensive weekly work summary with completed tasks, decisions made, and next steps.
---
```

**Progressive Disclosure**:
1. **Metadata** (always loaded) - name + description (~50 tokens)
2. **SKILL.md** (loaded when triggered) - main workflow
3. **References** (loaded on-demand) - detailed docs

**Priority**: User skills (03-skills/) have priority over system skills (00-system/skills/)

---

### 3. Memory (Context Persistence)

**Purpose**: Never start from scratch - preserve all context

**What gets saved**:
- **Goals**: Your objectives and success criteria
- **Roadmap**: Short/long-term plans
- **Learnings**: Patterns, insights, best practices
- **Session Reports**: Historical work summaries
- **Project State**: What you were working on
- **User Config**: Language and preferences

**Auto-Updated By**: close-session skill at end of each session

**Key Principle**: Context is cumulative - builds over time

---

### 4. Auto-Detection (YAML-Driven)

**How it works**:

1. **Everything has metadata** (YAML frontmatter)
2. **Description field** contains trigger phrases
3. **AI matches** user message against descriptions
4. **Loads context** when match found

**Example**:

```yaml
# In 02-projects/05-website-development/01-planning/overview.md
---
description: Load when user mentions "website", "web dev", "homepage", "site"
---
```

```
User: "let's work on the homepage"
  ↓
AI matches "homepage" → Loads website project
```

---

## 🔧 Core Infrastructure

### nexus-loader.py

**Location**: `00-system/core/nexus-loader.py`

**What it does**:
- Analyzes system state
- Returns complete instructions (instruction-driven architecture)
- Loads core files at session start
- Scans all projects and skills for metadata
- Provides context loading on-demand
- Monitors token budget
- Returns structured JSON

**Commands**:
```bash
python nexus-loader.py --startup          # Load session context + return instructions
python nexus-loader.py --list-projects    # Scan project metadata
python nexus-loader.py --list-skills      # Scan skill metadata
python nexus-loader.py --project 05       # Load specific project
python nexus-loader.py --skill close-session  # Load specific skill
python nexus-loader.py --show-tokens      # Display token costs
```

**Output Structure**:
```json
{
  "loaded_at": "2025-11-05T01:05:54",
  "bundle": "startup",
  "system_state": "operational",
  "files_to_load": ["...", "...", "..."],
  "instructions": {
    "action": "display_menu",
    "message": "...",
    "reason": "..."
  },
  "metadata": {
    "projects": [...],
    "skills": [...]
  },
  "stats": {
    "files_found": 3,
    "total_projects": 8,
    "total_skills": 12
  }
}
```

---

### orchestrator.md

**Location**: `00-system/core/orchestrator.md`

**What it does**:
- Documents AI decision logic (minimal)
- Explains three-step startup sequence
- Describes skill-first execution priority
- Shows project/skill loading patterns
- Provides response formatting guidelines
- Emphasizes menu display format

**Design Principle**: Ultra-simple. State lives in data files, not code. Python script is master controller.

**Key Sections**:
- Startup Sequence (3 steps)
- Language Preference Enforcement
- Project Loading Pattern (two-step)
- Skill Loading Pattern (two-step)
- Smart Routing (skill-first execution)
- Menu Display Format

---

### init-memory.py

**Location**: `00-system/core/init-memory.py`

**What it does**:
- Initializes memory system during Project 00
- Creates all 6 memory files with user's actual content
- Populates goals.md with user's role, work pattern, goals
- Populates roadmap.md with user's milestones, metrics
- Creates user-config.yaml with language preference
- Initializes project-map.md with onboarding state
- Creates core-learnings.md template
- Creates session-reports/ folder

**Input**: USER_LANGUAGE, USER_ROLE, SHORT_TERM_GOAL, LONG_TERM_GOAL

**Output**: Complete memory system (no placeholders!)

---

## 🤖 System Skills (6 Built-In)

**Location**: `00-system/skills/` (NOT in 03-skills/)

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **create-project** | Create new projects with AI-guided planning | "create project" |
| **create-skill** | Create reusable workflows for repetitive tasks | "create skill" |
| **add-integration** | Guide MCP server setup for external tools | "add integration" |
| **close-session** | End session, update memory, save progress | "done", "finish", "close" |
| **validate-system** | Check system integrity, auto-fix issues | "validate system" |
| **archive-project** | Move completed projects to 05-archived/ | "archive project" |

**Note**: All skills use V2.0 format (name + description only)

---

## 📖 Documentation Reference

### For Understanding the System

- **[Framework Overview](framework-overview.md)** (THIS FILE) - Complete system guide
- **[System Map](../system-map.md)** - System structure and architecture
- **[Orchestrator](../core/orchestrator.md)** - AI decision logic (minimal, instruction-driven)
- **[Memory Map](../../01-memory/memory-map.md)** - Context persistence
- **[Project Map](../../02-projects/project-map.md)** - Current state

### For Building Skills

- **[YAML Quick Reference](yaml-quick-reference.md)** - V2.0 skill YAML format cheat sheet
- **[Skill File Format](skill-file-format.md)** - .skill packaging specification
- **create-skill skill** - Use the create-skill skill for guided skill creation with built-in best practices

### For Development

- **Project Schema**: `../skills/create-project/project-schema.yaml`
- **Onboarding Projects**: Check `02-projects/00-define-goals/` through `03-system-mastery/` for complete designs

---

## 💡 Design Principles

### 1. Instruction-Driven Architecture

**Principle**: Python script analyzes state and returns complete instructions. AI follows exactly.

**Why**: Zero interpretation, zero ambiguity, deterministic behavior, easy debugging.

**Example**: Script returns `"action": "load_and_execute_project"` with complete workflow steps.

---

### 2. YAML-Driven Auto-Detection

**Principle**: Everything has metadata describing when to load it. AI matches user messages against descriptions.

**Why**: Context loads automatically. No manual routing. Self-documenting.

**Example**: Project description "Load when user mentions 'website'" → User says "website" → Project loads.

---

### 3. Skill-First Execution

**Principle**: Skills have priority over projects in routing. User skills have priority over system skills.

**Why**: Reusable workflows are more valuable than one-off project work. Encourages workflow capture.

**Example**: "status report" matches skill → Executes skill (doesn't search projects first).

---

### 4. Progressive Disclosure

**Principle**: Load minimum at start (just metadata), more context just-in-time (when needed).

**Why**: Efficient token usage. Fast startup. Context loads when relevant.

**Example**: Metadata (~50 tokens) always loaded. SKILL.md (~2000 tokens) loaded when triggered.

---

### 5. State in Data Files

**Principle**: project-map.md contains system state. tasks.md contains task progress. No logic in code.

**Why**: Transparent. Inspectable. Debuggable. AI can read state directly.

**Example**: Current focus stored in project-map.md, not in Python variables.

---

### 6. Context Preservation

**Principle**: Nothing is lost between sessions. All work saved automatically. Session reports build historical record.

**Why**: Never start from scratch. Cumulative learning. Historical awareness.

**Example**: close-session updates memory, saves progress, creates session report.

---

### 7. Concrete Before Abstract (Onboarding)

**Principle**: Experience first, explanation after. Value delivery before feature teaching.

**Why**: Grounded learning. Higher retention. Lower cognitive load. Better engagement.

**Example**: Project 00 captures goals (5 min) BEFORE explaining system architecture.

---

## 🎓 Key Terminology

| Term | Definition |
|------|------------|
| **Project** | Temporal work with beginning, middle, end (e.g., client website) |
| **Skill** | Reusable workflow for repetitive tasks (e.g., weekly report) |
| **Memory** | Context persistence system (goals, learnings, session reports) |
| **YAML Frontmatter** | Metadata at top of files (between `---` markers) |
| **Auto-Detection** | System automatically loads context based on YAML descriptions |
| **Progressive Disclosure** | Load minimum first, more context on-demand |
| **Session** | Single conversation with AI (start → work → close) |
| **Context** | All information relevant to current work |
| **Instruction-Driven** | Script returns complete instructions, AI follows exactly |
| **Skill-First** | Skills have priority over projects in routing |
| **Onboarding** | 4-project journey (00-03) to learn system (35-40 min) |

---

## 🔄 System Workflows

### Creating a Project

```
User: "I want to create a project"
  ↓
AI triggers: create-project skill
  ↓
Interactive wizard:
  1. Project purpose
  2. Requirements
  3. Design approach
  4. Task breakdown
  ↓
Creates:
  └── 02-projects/{ID}-{name}/
      ├── 01-planning/
      │   ├── overview.md (YAML metadata)
      │   ├── requirements.md
      │   ├── design.md
      │   └── tasks.md
      ├── 02-working/
      └── 03-outputs/
  ↓
Updates: project-map.md with new project
```

### Creating a Skill

```
User: "I want to create a skill"
  ↓
AI triggers: create-skill skill
  ↓
Interactive wizard:
  1. Skill purpose
  2. AI suggests skill name
  3. Workflow steps
  4. Optional: references, scripts, assets
  ↓
Creates:
  └── 03-skills/{skill-name}/
      ├── SKILL.md (V2.0 YAML + workflow)
      ├── references/ (if needed)
      ├── scripts/ (if needed)
      └── assets/ (if needed)
  ↓
Auto-detected: Next session, skill available in metadata
```

### Working on a Project

```
User: "continue working on website"
  ↓
AI matches "website" against project descriptions
  ↓
Loads: python nexus-loader.py --project 05-website-development
  ↓
Reads in parallel:
  ├── overview.md
  ├── requirements.md
  ├── design.md
  └── tasks.md
  ↓
Shows: Next unchecked task
  ↓
User completes work
  ↓
Context saved to project files
```

### Ending a Session

```
User: "done for now"
  ↓
AI triggers: close-session skill
  ↓
Skill workflow:
  1. Update project-map.md (current focus, decisions)
  2. Update tasks.md (mark completed with [x])
  3. Create session report (session-reports/{date}.md)
  4. Clean temp files
  5. Confirm completion
  ↓
Session complete - all context preserved
```

---

## 🌟 Why Nexus-v3?

### Problems It Solves

❌ **Without Nexus-v3**:
- Start every AI session from scratch
- Repeat context manually
- Lose track of progress
- Forget what you were working on
- No reusable workflows
- Manual project management overhead

✅ **With Nexus-v3**:
- Resume exactly where you left off
- Context loads automatically (instruction-driven)
- Progress tracked automatically (tasks.md)
- Always know current focus (project-map.md)
- Capture and reuse workflows (skills)
- Zero-overhead organization (YAML-driven)

### Key Benefits

1. **Never Repeat Context** - System remembers everything (memory files)
2. **Instruction-Driven** - Script tells AI exactly what to do (zero ambiguity)
3. **Auto-Detection** - Right context loads automatically (YAML descriptions)
4. **Skill-First** - Reusable workflows prioritized over one-off work
5. **Progress Tracking** - Always know what's done/next (checkbox tasks)
6. **Workflow Capture** - Reuse successful patterns (skills)
7. **Historical Record** - Session reports build over time
8. **Pedagogical Onboarding** - Learn through experience, not explanation (35-40 min)

---

## 🚀 Getting Started

### First-Time User Journey

**Step 1: Load claude.md**
```
In Claude Desktop or Claude Code:
Load: Nexus-v3/claude.md
```

**Step 2: System Auto-Detects First Time**
```
Script returns: "system_state": "first_time_setup"
Instructions: Load and execute Project 00 (immediate)
```

**Step 3: Complete Onboarding** (35-40 min total)
- **Project 00** (8-10 min): Define goals, create memory
- **Project 01** (10-12 min): Create workspace, first project
- **Project 02** (15 min): Create first skill
- **Project 03** (10 min): System mastery review + graduation

**Step 4: Operational!**
```
Next session:
Script returns: "system_state": "operational"
Instructions: Display menu
AI shows: Goals, projects, skills, current focus
User: Work naturally with full context preservation
```

### Typical Operational Session

```
1. AI runs: python nexus-loader.py --startup
2. AI loads: 5 core files + metadata
3. AI displays: Goals, projects, skills, current focus
4. User says: "work on website"
5. AI matches: website project → Loads context
6. User works: AI assists with full context
7. User says: "done"
8. AI triggers: close-session → Saves everything
9. Next session: Resume exactly where you left off
```

---

## 📞 Need Help?

### Navigation

- Lost? Check the [System Map](../system-map.md)
- Need context? Check the [Memory Map](../../01-memory/memory-map.md)
- Want to know what's next? Check the [Project Map](../../02-projects/project-map.md)
- How does orchestration work? Check the [Orchestrator](../core/orchestrator.md)

### Building

- Creating skills? Use the **create-skill** skill for guided workflow with built-in best practices
- Quick YAML reference? See [YAML Quick Reference](yaml-quick-reference.md)
- Packaging skills? See [Skill File Format](skill-file-format.md)

### Understanding

- How does it work? Read this document (you're here!)
- How do I start? See "Getting Started" section above
- What's the philosophy? See "Design Principles" section above
- What's the onboarding like? See "The Onboarding Journey" section above

---

## 🔮 Advanced Topics

### Language-First Architecture

Language selection happens in first 30 seconds of Project 00 and is enforced for ALL subsequent interactions. Stored in `01-memory/user-config.yaml`.

Supported: English, Deutsch, Español, Français, 中文, 日本語, Português, Italiano, and more.

### AI Suggestion Framework

5-step collaborative pattern used in onboarding:
1. User provides context
2. AI synthesizes and suggests 2-3 options
3. Ask for resonance ("What resonates with you?")
4. User refines
5. Capture refined version (NOT AI's suggestion)

**Philosophy**: Invitation, not instruction. Collaborative, not prescriptive.

### Token Budget Management

nexus-loader.py monitors total metadata tokens and warns if >7,000 (3.5% of context window).

Progressive disclosure keeps startup lean:
- Metadata: ~50 tokens per skill/project
- SKILL.md: ~2000 tokens (loaded when triggered)
- References: Variable (loaded on-demand)

### Archiving Completed Projects

Use `archive-project` skill to move completed projects to `02-projects/05-archived/`.

Benefits:
- Cleaner project list
- Historical record preserved
- Can unarchive if needed

---

**Nexus-v3** - Self-guiding work organization through AI conversation and instruction-driven automation.

**Never start from scratch. Always resume where you left off. Let the system remember for you.**

---

**Version**: 2.0
**Last Updated**: 2025-11-05
**Status**: Production Ready
**Major Changes**:
- Added instruction-driven architecture documentation
- Documented three-step startup pattern
- Comprehensive onboarding journey (Project 00 V2.0 redesign)
- Skill-first execution principle
- Updated system skills count (5 → 6)
- Living knowledge organism philosophy
