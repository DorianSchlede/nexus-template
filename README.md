# Nexus

> **Quick Start:** [Use this template](https://github.com/DorianSchlede/nexus-template/generate) → Clone your repo → Open in VS Code → Start Claude Code → Say "hi"

---

## The Problem You Have Right Now

Every time you start a new Claude session:
- You re-explain who you are and what you do
- You re-describe your build and where you left off
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
    📦 BUILDS - None yet ▸ 'create build'
    🔧 SKILLS - 26 available

    💡 SUGGESTED: 'setup goals' to teach Nexus about you

You: "create build for launching v2.0 dashboard"

AI: [Creates build structure, guides planning]
    ✅ Build created: 01-dashboard-launch
```

**Next Session:**
```
You: "hi"

AI: Shows your context:
    🧠 MEMORY - Role: PM at SaaS | Goal: Launch v2.0
    📦 BUILDS - • dashboard-launch | IN_PROGRESS | 42%

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

### 2. Builds With Structure
Work happens in **Builds** — with planning documents, task lists, and progress tracking. Everything auto-saves.

### 3. Skills You Can Reuse
Capture workflows you repeat. Say "create skill" after doing something useful, and it becomes a one-command action forever.

---

## Quick Start

### One-Command Install

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.ps1 | iex
```

This installs:
- ✅ Claude Code (AI assistant CLI & VS Code extension)
- ✅ uv (Python package manager for Nexus hooks)
- ✅ Git (Windows only, includes Git Bash for hooks)
- ✅ Nexus template (cloned to your specified directory)
- ❓ VS Code (optional, asks during installation)

**After installation:**
1. Restart your terminal (for PATH updates)
2. `cd` to your Nexus directory
3. Open in VS Code: `code .`
4. Start Claude Code and say `hi`

> **System Requirements**: macOS 13.0+, Ubuntu 20.04+, or Windows 10 1809+ (Build 17763) | 4GB+ RAM | Internet connection

<details>
<summary>Manual Installation (if one-command fails)</summary>

### Prerequisites

#### Required Software

| Software | Official Site | Why Needed |
|----------|--------------|------------|
| **Claude Code** | [claude.com/download](https://claude.com/download) | The AI assistant |
| **Visual Studio Code** | [code.visualstudio.com](https://code.visualstudio.com/download) | IDE with Claude Code extension |
| **uv** | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) | Runs Nexus hooks (Python package manager) |
| **Git** *(Windows only)* | [git-scm.com](https://git-scm.com/download/win) | Required for hooks on Windows |

#### Individual Install Commands

**macOS / Linux / WSL:**
```bash
# Claude Code
curl -fsSL https://claude.ai/install.sh | bash

# uv (required for Nexus hooks)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows PowerShell:**
```powershell
# Claude Code
irm https://claude.ai/install.ps1 | iex

# uv (required for Nexus hooks)
irm https://astral.sh/uv/install.ps1 | iex

# Git for Windows (includes Git Bash)
winget install --id Git.Git
```

**VS Code Extension:**
```
ext install anthropic.claude-code
```
Or search "Claude Code" in VS Code Extensions marketplace.

> **Note:** After installing, restart your terminal/VS Code for PATH changes to take effect.

#### Details

<details>
<summary>Claude Code</summary>

> **Docs:** [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup) | **GitHub:** [anthropics/claude-code](https://github.com/anthropics/claude-code)

The commands above install both the CLI and enable the [VS Code Extension](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code).

</details>

<details>
<summary>uv</summary>

> **Docs:** [docs.astral.sh/uv](https://docs.astral.sh/uv/) | **GitHub:** [astral-sh/uv](https://github.com/astral-sh/uv)

uv is an extremely fast Python package manager. Nexus hooks use it to run Python scripts with automatic dependency management.

</details>

<details>
<summary>Git for Windows</summary>

> **Download:** [git-scm.com/download/win](https://git-scm.com/download/win) | **Project:** [gitforwindows.org](https://gitforwindows.org/)

Windows users need Git Bash for Claude Code hooks. Git for Windows includes it automatically.

</details>

</details>

### Step 1: Create Your Nexus (if not using one-command installer)

1. Click **[Use this template](https://github.com/DorianSchlede/nexus-template/generate)**
2. Name your repo (e.g., `my-nexus`), click **Create repository**
3. Clone and open:
   ```bash
   git clone https://github.com/YOUR-USERNAME/my-nexus.git
   cd my-nexus
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
| `"create build"` | Start a new build with guided planning |
| `"setup goals"` | Personalize Nexus with your role & goals |
| `"create folders"` | Organize your file folders |
| `"done"` | Save progress, end session |

### Optional: Learn the System

When you're ready, 6 optional learning skills teach you everything:

| Skill | Trigger | Time |
|-------|---------|------|
| **setup-goals** | "setup goals" | 8-10 min |
| **create-folders** | "create folders" | 5-8 min |
| **learn-integrations** | "learn integrations" | 10-12 min |
| **learn-builds** | "learn builds" | 8-10 min |
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

### Builds — Structured Work

Builds have a beginning, middle, and end:

```
02-builds/01-dashboard-launch/
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
│  → Shows your active Builds and Skills                     │
│  → Suggests next steps based on your state                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  WORK: "continue [build]" or "[skill trigger]"            │
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

Connect your tools with natural language:

| Integration | Trigger | What It Does |
|-------------|---------|--------------|
| **Notion** | "connect notion" | Query databases, create pages, manage content |
| **Airtable** | "connect airtable" | Query bases, manage records, batch operations |
| **Beam AI** | "connect beam" | Manage agents, create tasks, view analytics |
| **Any REST API** | "add integration" | Auto-discovers endpoints, creates implementation plan |

Guided setup walks you through API keys and configuration.

---

## Workspace Map

Your `04-workspace/` folder is documented in `workspace-map.md` — a living map of your file structure.

**Why it matters:**
- Nexus reads this to understand where your files are
- It can find and organize things without asking
- New files and folders are automatically understood

**Keep it in sync:**
```
You: "update workspace map"

AI: [Scans 04-workspace/, updates documentation]
    ✅ Workspace map updated. Found 3 new folders.
```

Run this occasionally after reorganizing your files.

---

## Requirements

**System:**
- macOS 13.0+ / Ubuntu 20.04+ / Debian 10+ / Windows 10+ (Git Bash or WSL)
- 4 GB+ RAM, Internet connection

**Required Software:**

| Software | Download | Docs |
|----------|----------|------|
| Claude Code | [claude.com/download](https://claude.com/download) | [code.claude.com/docs](https://code.claude.com/docs/en/setup) |
| VS Code | [code.visualstudio.com](https://code.visualstudio.com/download) | [docs](https://code.visualstudio.com/docs) |
| uv | [astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) | [docs.astral.sh/uv](https://docs.astral.sh/uv/) |
| Git *(Windows)* | [git-scm.com](https://git-scm.com/download/win) | [gitforwindows.org](https://gitforwindows.org/) |

**Optional:**
- MCP servers for integrations (Notion, Airtable, Linear)

**Windows Users:** Claude Code hooks require Git Bash (included with [Git for Windows](https://git-scm.com/download/win)). Native cmd/PowerShell is not supported for hooks.

---

## Troubleshooting

### Nexus menu doesn't appear on startup

**Cause:** The SessionStart hook didn't run (usually `uv` not found).

**Fix:**
1. Verify uv is installed: `uv --version`
2. If not installed, run the install command above
3. Restart VS Code completely
4. Type `/clear` in Claude Code to reload hooks

### "uv not found" error

**Cause:** uv isn't in your PATH.

**Fix (macOS/Linux):**
```bash
# Add to ~/.bashrc or ~/.zshrc
export PATH="$HOME/.local/bin:$PATH"
```

**Fix (Windows):** Restart your terminal after installing uv.

### Hooks work in terminal but not VS Code

**Cause:** VS Code uses a different shell environment.

**Fix:**
1. Open VS Code settings
2. Search for "terminal integrated shell"
3. Set to your shell that has uv in PATH
4. Restart VS Code

---

## Learn More

- **[Product Overview](00-system/documentation/product-overview.md)** — The problems Nexus solves
- **[Framework Overview](00-system/documentation/framework-overview.md)** — Technical deep dive

---

## Getting Nexus

### Option 1: Use as Template (Recommended)

1. Go to the [Nexus GitHub repository](https://github.com/DorianSchlede/nexus-template)
2. Click **"Use this template"** → **"Create a new repository"**
3. Name your repo, set visibility, click **"Create repository"**
4. Clone your new repo:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME
   code .
   ```

This gives you your own copy where you can commit personal data (goals, builds, skills).

### Option 2: Direct Clone (For Trying It Out)

```bash
git clone https://github.com/DorianSchlede/nexus-template.git
cd nexus-template
code .
```

Note: With direct clone, you can't push changes to the original repo.

---

## Getting Updates

Nexus receives regular system updates (new skills, improvements, fixes). Your personal data is **never touched** during updates.

### What Gets Updated

| Updated (from upstream) | Protected (your data) |
|------------------------|----------------------|
| `00-system/` | `01-memory/` |
| `CLAUDE.md` | `02-builds/` |
| `README.md` | `03-skills/` |
| | `04-workspace/` |
| | `.env`, `.claude/` |

### Automatic Update Checks

Updates are checked automatically on startup. When available, you'll see:
```
⚡ UPDATE AVAILABLE: v0.9.0 → v0.10.0
   Say 'update nexus' to get latest improvements
```

### How to Update

Just say:
```
You: "update nexus"

AI: UPDATE AVAILABLE: v0.9.0 → v0.10.0
    12 files will be updated

    Proceed? (yes/no)

You: "yes"

AI: ✅ Updated! Backup at: .sync-backup/2024-01-15/
```

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
│   │   ├── builds/            # Build management
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
├── 02-builds/                 # YOUR TEMPORAL WORK
│   └── {id}-{name}/             # Each build
│
├── 03-skills/                   # YOUR CUSTOM SKILLS
│   └── {skill-name}/            # Your reusable workflows
│
└── 04-workspace/                # YOUR FILES
    └── [Your organization]      # Documents, data, outputs
```

---

## Build Lifecycle

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
| `plan-build` | "create build" | Guided build setup |
| `create-skill` | "create skill" | Capture workflow for reuse |
| `execute-build` | "continue [name]" | Systematic build execution |
| `close-session` | "done" | Save progress, create report |

### Learning Skills
| Skill | Trigger | What It Does |
|-------|---------|--------------|
| `setup-goals` | "setup goals" | Personalize your goals |
| `create-folders` | "create folders" | Configure folder structure |
| `learn-integrations` | "learn integrations" | Connect external tools |
| `learn-builds` | "learn builds" | Build system tutorial |
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
| `"create build"` | Start guided build creation |
| `"create skill"` | Capture reusable workflow |
| `"continue [name]"` | Resume build |
| `"setup goals"` | Personalize your context |
| `"done"` | Save everything, end session |
| `"validate system"` | Check integrity |

---

**Nexus** — Work with AI optimally. Build once, reuse forever. Never start from scratch.
