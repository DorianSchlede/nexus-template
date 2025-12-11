# Nexus

> **Quick Start:** Clone repo → Open in VS Code → Start Claude Code → Say "hi" → Start working immediately
>
> ```bash
> git clone https://github.com/DorianSchlede/nexus-template.git
> ```

---

## The Problem You Have Right Now

Every time you start a new Claude session:
- You re-explain who you are and what you do
- You re-describe your project and where you left off
- You rebuild the same workflows from scratch
- You lose context, insights, and momentum

**What if Claude remembered everything?**

---

## See It Work (2 minutes)

**First Time:**
```
You: "hi"

AI: Shows Nexus menu with:
    🧠 MEMORY - Not configured ▸ 'setup goals'
    📦 PROJECTS - None yet ▸ 'create project'
    🔧 SKILLS - 26 available

    💡 SUGGESTED: 'setup goals' to teach Nexus about you

You: "create project for launching v2.0 dashboard"

AI: [Creates project structure, guides planning]
    ✅ Project created: 01-dashboard-launch
```

**Next Session:**
```
You: "hi"

AI: Shows your context:
    🧠 MEMORY - Role: PM at SaaS | Goal: Launch v2.0
    📦 PROJECTS - • dashboard-launch | IN_PROGRESS | 42%

    💡 SUGGESTED: 'continue dashboard-launch' - resume at 42%

You: "continue dashboard-launch"

AI: [Loads all context, shows exactly where you left off]
    "You're on Phase 2: Design. Next task: Review wireframes."
```

**That's the magic.** No re-explaining. Ever.

---

## What Makes This Possible

Nexus gives you three things:

### 1. Memory That Persists
Your role, goals, and learnings are saved in files. Every session, Claude loads them automatically. You never start from zero.

### 2. Projects With Structure
Work happens in **Projects** — with planning documents, task lists, and progress tracking. Everything auto-saves.

### 3. Skills You Can Reuse
Capture workflows you repeat. Say "create skill" after doing something useful, and it becomes a one-command action forever.

---

## Quick Start

### Prerequisites

- [ ] **Claude Code Account** — [Sign up here](https://claude.ai)
- [ ] **Visual Studio Code** — [Download](https://code.visualstudio.com/)
- [ ] **Claude Code VS Code Extension** — Install from VS Code marketplace
- [ ] **Python 3.x** — [Download](https://python.org)

### Step 1: Clone & Open

```bash
git clone https://github.com/DorianSchlede/nexus-template.git
cd nexus-template
code .
```

### Step 2: Start Claude Code

1. **Open Claude Chat** via the Claude Code extension (click the Claude icon in sidebar)
2. **Say:** `hi`

The system activates automatically and shows the menu.

### Step 3: Start Working

You can start working **immediately** — no setup required!

| You Say | What Happens |
|---------|--------------|
| `"create project"` | Start a new project with guided planning |
| `"setup goals"` | Personalize Nexus with your role & goals |
| `"setup workspace"` | Organize your file folders |
| `"done"` | Save progress, end session |

### Optional: Learn the System

When you're ready, 5 optional learning skills teach you everything:

| Skill | Trigger | Time |
|-------|---------|------|
| **setup-goals** | "setup goals" | 8-10 min |
| **setup-workspace** | "setup workspace" | 5-8 min |
| **learn-projects** | "learn projects" | 8-10 min |
| **learn-skills** | "learn skills" | 10-12 min |
| **learn-nexus** | "learn nexus" | 15-18 min |

---

## The Three Core Concepts

### Memory — Your Persistent Context

The `01-memory/` folder stores who you are (auto-created on first run):

```
01-memory/
├── goals.md           ← YOUR role, objectives, success metrics
├── user-config.yaml   ← Language & preferences
├── core-learnings.md  ← Patterns that grow over time
└── session-reports/   ← Auto-generated session history
```

Every session, Claude loads these files first. It knows your context before you say anything.

### Projects — Structured Work

Projects have a beginning, middle, and end:

```
02-projects/01-dashboard-launch/
├── 01-planning/       ← overview.md, plan.md, steps.md
├── 02-resources/      ← Reference materials
├── 03-working/        ← Work in progress
└── 04-outputs/        ← Final deliverables
```

### Skills — Reusable Workflows

Skills capture actions you repeat:

```
You: "generate status report"

AI: [Loads skill → Follows exact steps → Produces report]
```

Create your own with `"create skill"` after doing something useful.

---

## How Sessions Work

```
┌─────────────────────────────────────────────────────────────┐
│  START: "hi"                                                 │
│  → System loads your Memory                                  │
│  → Shows your active Projects and Skills                     │
│  → Suggests next steps based on your state                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  WORK: "continue [project]" or "[skill trigger]"            │
│  → Loads relevant context                                    │
│  → Executes systematically                                   │
│  → Tracks progress                                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  END: "done"                                                 │
│  → Saves all progress                                        │
│  → Updates Memory with learnings                             │
│  → Creates session report                                    │
│  → Ready to resume next time                                 │
└─────────────────────────────────────────────────────────────┘
```

---

## Integrations

Nexus includes master skills for connecting to external tools:

| Integration | Skill | What It Does |
|-------------|-------|--------------|
| **Notion** | `notion-master` | Connect databases, sync pages, search |
| **Airtable** | `airtable-master` | Connect bases, query records, manage data |

Say "connect notion" or "connect airtable" to get started.

---

## Requirements

**Required:**
- Claude Code Account ([sign up](https://claude.ai))
- Visual Studio Code ([download](https://code.visualstudio.com/))
- Claude Code VS Code Extension (install from marketplace)
- Python 3.x ([download](https://python.org))

**Optional:**
- MCP servers for integrations (Notion, Airtable, Linear)
- Git for version control

---

## Learn More

- **[Product Overview](00-system/documentation/product-overview.md)** — The problems Nexus solves
- **[Framework Overview](00-system/documentation/framework-overview.md)** — Technical deep dive

---

# Technical Reference

*The sections below are for users who want deeper understanding.*

---

## Folder Structure

```
Nexus/
│
├── CLAUDE.md                    # Entry point - loads on startup
│
├── 00-system/                   # FRAMEWORK (don't modify)
│   ├── core/                    # Engine scripts
│   │   ├── orchestrator.md      # AI decision logic
│   │   └── nexus-loader.py      # Context loader + state machine
│   ├── skills/                  # Built-in system skills (26+)
│   │   ├── learning/            # Onboarding skills
│   │   ├── projects/            # Project management
│   │   ├── skill-dev/           # Skill creation
│   │   ├── system/              # System utilities
│   │   ├── notion/              # Notion integration
│   │   ├── airtable/            # Airtable integration
│   │   └── tools/               # Mental models, generators
│   └── documentation/           # Framework guides
│
├── 01-memory/                   # YOUR PERSISTENT CONTEXT
│   ├── goals.md                 # Role, objectives (auto-created)
│   ├── user-config.yaml         # Preferences + learning tracker
│   ├── core-learnings.md        # Patterns (grows over time)
│   └── session-reports/         # Auto-generated summaries
│
├── 02-projects/                 # YOUR TEMPORAL WORK
│   └── {id}-{name}/             # Each project
│
├── 03-skills/                   # YOUR CUSTOM SKILLS
│   └── {skill-name}/            # Your reusable workflows
│
└── 04-workspace/                # YOUR FILES
    └── [Your organization]      # Documents, data, outputs
```

---

## Project Lifecycle

| Status | Meaning |
|--------|---------|
| `PLANNING` | Being designed |
| `IN_PROGRESS` | Active work |
| `COMPLETE` | All tasks done |
| `ARCHIVED` | Moved to archive |

---

## Built-in System Skills

### Core Skills
| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `create-project` | "create project" | Guided project setup |
| `create-skill` | "create skill" | Capture workflow for reuse |
| `execute-project` | "continue [name]" | Systematic project execution |
| `close-session` | "done" | Save progress, create report |

### Learning Skills
| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `setup-goals` | "setup goals" | Personalize your goals |
| `setup-workspace` | "setup workspace" | Configure folder structure |
| `learn-projects` | "learn projects" | Project system tutorial |
| `learn-skills` | "learn skills" | Skill system tutorial |
| `learn-nexus` | "learn nexus" | System mastery |

### Integration Skills
| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `notion-master` | "connect notion" | Notion database integration |
| `airtable-master` | "connect airtable" | Airtable base integration |
| `add-integration` | "add integration" | MCP server setup guide |

---

## Key Commands Reference

| Command | What Happens |
|---------|--------------|
| `"hi"` | Load system, show menu |
| `"create project"` | Start guided project creation |
| `"create skill"` | Capture reusable workflow |
| `"continue [name]"` | Resume project |
| `"setup goals"` | Personalize your context |
| `"done"` | Save everything, end session |
| `"validate system"` | Check integrity |

---

**Nexus** — Work with AI optimally. Build once, reuse forever. Never start from scratch.
