# Nexus-v3 Template

> **Self-Guiding Work Organization System** - AI-powered project and workflow management through conversation

A Claude AI-powered system that remembers you across sessions, tracks projects, captures workflows, and maintains context—all through natural conversation.

---

## ✨ What is Nexus-v3?

Nexus-v3 is a **conversational work organization system** that helps you:

- **Track temporal work** with Projects (planning → execution → outputs)
- **Capture reusable workflows** with Skills
- **Preserve context** across AI sessions with persistent Memory
- **Auto-detect what to load** via YAML-driven metadata
- **Never start from scratch** - the system remembers everything

**No database. No web app. No coding required.**
Just markdown files + AI intelligence + optional Python scripts.

---

## 🚀 Quick Start

### 1. Clone or Download

```bash
git clone https://github.com/DorianSchlede/nexus-template.git
cd nexus-template
```

### 2. Set Up Environment (Optional MCP Integrations)

If you want to use MCP integrations (Airtable, Beam, Slack):

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your API keys
# AIRTABLE_API_KEY=your_key_here
# BEAM_API_TOKEN=your_token_here
# SLACK_BOT_TOKEN=your_token_here
# SLACK_TEAM_ID=your_team_id_here
```

### 3. Load in Claude

In Claude Desktop or Claude Code, load the entry file:

```
@c:/path/to/nexus-template/claude.md
```

### 4. Follow Onboarding

The system will:
1. Detect it's your first time
2. Guide you through 4 onboarding projects (8-10 min each)
3. Create your personalized workspace
4. Set up your memory system

**Total Onboarding**: 35-40 minutes → Fully operational!

---

## 🎯 Core Features

### 📁 Projects (Temporal Work)
Organize work with a beginning, middle, and end:
- `01-planning/` - Requirements, design, tasks
- `02-working/` - Work-in-progress files
- `03-outputs/` - Final deliverables
- Progress tracked via checkbox tasks
- Auto-updates through `close-session` skill

### 🔄 Skills (Reusable Workflows)
Capture repeatable workflows for common tasks:
- `SKILL.md` - Main workflow (< 500 lines recommended)
- `references/` - Optional detailed documentation
- `scripts/` - Optional automation code
- `assets/` - Optional files
- Auto-detected via trigger phrases in description

### 🧠 Memory (Context Persistence)
Never start from scratch:
- `goals.md` - Your objectives and success criteria
- `roadmap.md` - Short/long-term plans
- `core-learnings.md` - Patterns and insights
- `session-reports/` - Historical summaries
- Auto-updated by `close-session` skill

### 🗺️ Auto-Navigation
System generates navigation from metadata:
- 4 specialized maps (System, Memory, Project, Workspace)
- YAML-driven auto-detection
- Progressive disclosure (load minimum at start)
- Smart routing (skills → projects → general)

---

## 📂 Folder Structure

```
Nexus-v3/
│
├── claude.md                       # 🚀 LOAD THIS TO START!
│
├── 00-system/                      # SYSTEM FRAMEWORK
│   ├── system-map.md                   Master navigation hub
│   ├── core/
│   │   ├── orchestrator.md             AI decision logic (minimal)
│   │   ├── nexus-loader.py             Context loading + decision engine
│   │   └── init-memory.py              Memory initialization script
│   ├── skills/                         System skills (7 built-in)
│   │   ├── create-project/
│   │   ├── create-skill/
│   │   ├── add-integration/
│   │   ├── close-session/
│   │   ├── validate-system/
│   │   ├── archive-project/
│   │   └── update-tasks/
│   └── documentation/                  System documentation
│       ├── framework-overview.md       Complete guide
│       ├── structure.md                Complete structure docs
│       ├── ux-teaching-philosophy.md   Onboarding design
│       └── skill-file-format.md        .skill packaging spec
│
├── 01-memory/                      # CONTEXT PERSISTENCE
│   ├── memory-map.md                   Memory system navigation
│   ├── goals.md                        Your objectives
│   ├── roadmap.md                      Plans (3/6/12 month)
│   ├── user-config.yaml                Language & preferences
│   ├── core-learnings.md               Patterns & insights
│   └── session-reports/                Historical summaries
│
├── 02-projects/                    # TEMPORAL WORK
│   ├── project-map.md                  System state & current focus
│   ├── 00-define-goals/                Onboarding Project 00 (8-10 min)
│   ├── 01-first-project/               Onboarding Project 01 (10-12 min)
│   ├── 02-first-skill/                 Onboarding Project 02 (15 min)
│   ├── 03-system-mastery/              Onboarding Project 03 (10 min)
│   ├── 05-archived/                    Completed projects
│   └── {ID}-{name}/                    User projects
│       ├── 01-planning/
│       │   ├── overview.md             YAML metadata + description
│       │   ├── requirements.md
│       │   ├── design.md
│       │   └── tasks.md                Checkbox task list (state source)
│       ├── 02-working/             Work-in-progress files
│       └── 03-outputs/             Final deliverables
│
├── 03-skills/                      # USER SKILLS
│   └── {skill-name}/
│       ├── SKILL.md                    YAML metadata + workflow
│       ├── references/                 (optional) Detailed docs
│       ├── scripts/                    (optional) Automation
│       └── assets/                     (optional) Files
│
├── 04-workspace/                   # USER CONTENT
│   ├── workspace-map.md                Your custom folder guide
│   └── [Your folders]/                 Organize however you want
│
├── .mcp.json                       # MCP server configuration
├── .env.example                    # Environment variables template
└── .gitignore                      # Git ignore rules
```

---

## 🎓 Onboarding Journey (35-40 min)

### Project 00: Define Goals (8-10 min)
**Philosophy**: Concrete before abstract, experience before explanation

**What You'll Do**:
- Choose your language
- Capture YOUR goals (concrete)
- Create Memory system (action)
- Understand persistence (explanation)
- Practice close-session habit

**What Gets Created**:
- `01-memory/goals.md` - YOUR role, work pattern, goals
- `01-memory/roadmap.md` - YOUR milestones, metrics
- `01-memory/user-config.yaml` - YOUR language preference
- `02-projects/project-map.md` - Project tracking
- `01-memory/core-learnings.md` - Insight capture template
- `01-memory/session-reports/` - Session summary folder

---

### Project 01: First Project (10-12 min)
**Focus**: Workspace structure + Create first real project

**What You'll Do**:
- Create workspace structure using just-in-time organization
- Learn Projects vs Skills decision framework
- Use `create-project` skill to create first real project
- Apply project planning with AI guidance

**What Gets Created**:
- `04-workspace/` custom folder structure
- `04-workspace/workspace-map.md` with your organization
- Your first real project tailored to your goals

---

### Project 02: First Skill (15 min)
**Focus**: Skill creation + Workflow automation

**What You'll Do**:
- Learn what skills are (reusable workflows)
- Use `create-skill` skill to capture a workflow
- AI suggests skill name based on your description
- Practice executing your first skill

**What Gets Created**:
- Your first custom skill in `03-skills/`
- Understanding of workflow automation

---

### Project 03: System Mastery (10 min)
**Focus**: Review + AI collaboration awareness

**What You'll Do**:
- Review complete setup (goals, workspace, projects, skills)
- Learn 3 system pitfalls using YOUR actual entities
- Learn 2 AI behavioral patterns (False Progress 19%, Incomplete Reading)
- Practice detection exercises with YOUR projects
- Confirm two-layer mastery (system + AI collaboration)
- Graduate with AI awareness superpowers!

**Outcome**:
- Onboarding complete
- System mastery confirmed
- Ready for operational mode

---

## 🛠️ System Skills (7 Built-In)

| Skill | Purpose | Trigger |
|-------|---------|---------|
| **create-project** | Create new projects with AI-guided planning | "create project" |
| **create-skill** | Create reusable workflows for repetitive tasks | "create skill" |
| **add-integration** | Guide MCP server setup for external tools | "add integration" |
| **close-session** | End session, update memory, save progress | "done", "finish", "close" |
| **validate-system** | Check system integrity, auto-fix issues | "validate system" |
| **archive-project** | Move completed projects to 05-archived/ | "archive project" |
| **update-tasks** | Quick task updates without closing session | "update tasks" |

---

## 💡 Key Concepts

### Instruction-Driven Architecture
**Key Principle**: Python script (`nexus-loader.py`) is the MASTER CONTROLLER

**Three-Step Pattern** (every session):
1. **Run**: `python 00-system/core/nexus-loader.py --startup`
2. **Load**: All files from `files_to_load` array (parallel)
3. **Follow**: `instructions.action` exactly (no interpretation)

**Benefits**:
- ✅ Zero interpretation (AI doesn't guess, just executes)
- ✅ Zero manual state detection (script handles all edge cases)
- ✅ Deterministic behavior (same state = same instructions)
- ✅ Easy debugging (instructions are explicit and visible)

### YAML-Driven Auto-Detection
Everything has metadata describing when to load it:

```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update", "progress summary". Generate comprehensive weekly work summary.
---
```

AI matches user messages against descriptions → Context loads automatically

### Skill-First Execution
**Most Important Orchestration Principle**:

**Priority 1**: Check for matching skill (FIRST)
**Priority 2**: Check for project name match
**Priority 3**: General response (fallback - should be RARE)

User skills (03-skills/) have priority over system skills (00-system/skills/)

### Progressive Disclosure
Load minimum at start, more context just-in-time:
- **Session Start**: 5 core files + metadata (~7,000 tokens)
- **Skill Trigger**: SKILL.md + auto-load resources
- **Project Work**: Full planning files on-demand

---

## 🔌 MCP Integrations (Optional)

Nexus-v3 supports MCP (Model Context Protocol) integrations out of the box.

### Available Integrations

**Pre-configured in `.mcp.json`**:
- **Context7** - Access library documentation
- **Linear** - Project management and issue tracking
- **Airtable** - Database and spreadsheet integration
- **Beam Studio** - Knowledge base and documentation
- **Slack** - Team communication

### Setup Instructions

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Add your API keys to `.env`**:
   ```env
   AIRTABLE_API_KEY=your_key_here
   BEAM_API_TOKEN=your_token_here
   SLACK_BOT_TOKEN=xoxb-your-token-here
   SLACK_TEAM_ID=T-your-team-id-here
   ```

3. **Load environment variables**:
   The `.mcp.json` file references these environment variables automatically.

4. **Test integration**:
   Say "add integration" in Claude to get guided setup help.

### Security Note

**Never commit `.env` to version control!**
The `.gitignore` file is already configured to exclude it.

---

## 🎨 Design Philosophy

### 1. Concrete Before Abstract
Experience first, explanation after. Value delivery before feature teaching.

### 2. Instruction-Driven
Python script analyzes state and returns complete instructions. AI follows exactly.

### 3. YAML-Driven Auto-Detection
Everything has metadata. AI matches user messages against descriptions.

### 4. Skill-First Execution
Skills have priority over projects in routing. Encourages workflow capture.

### 5. Progressive Disclosure
Load minimum first, more context on-demand. Efficient token usage.

### 6. State in Data Files
Logic lives in data files (`project-map.md`), not code. Transparent and editable.

### 7. Context Preservation
Nothing is lost between sessions. All work saved automatically.

---

## 🚨 Troubleshooting

### System not loading?
Make sure you loaded `claude.md` (not other files directly).

### Navigation stale?
Say "validate system" to regenerate all navigation maps.

### Lost progress?
Check `01-memory/session-reports/` for historical summaries.

### Files missing?
Say "validate system" - it will detect and recreate templates.

### API keys not working?
Make sure your `.env` file exists and contains the correct keys.

### Need help?
The system self-guides! Just ask questions naturally.

---

## 📖 Documentation

### For Understanding the System
- **[Framework Overview](00-system/documentation/framework-overview.md)** - Complete system guide
- **[System Map](00-system/system-map.md)** - System structure and architecture
- **[Orchestrator](00-system/core/orchestrator.md)** - AI decision logic
- **[Structure Documentation](00-system/documentation/structure.md)** - Complete file/folder reference

### For Building Skills
- **[Skill File Format](00-system/documentation/skill-file-format.md)** - .skill packaging specification
- **create-skill skill** - Use the skill for guided creation with best practices

### For Development
- **[UX Teaching Philosophy](00-system/documentation/ux-teaching-philosophy.md)** - Onboarding design standards

---

## 📦 Distribution

This template can be shared as-is or customized for specific use cases.

### Customization Ideas
- Add domain-specific skills for your industry
- Pre-populate workspace structure for teams
- Include custom project templates
- Add organization-specific documentation
- Configure MCP integrations for your tools

### Sharing
1. Remove any sensitive data from `.env` (use `.env.example`)
2. Ensure `.gitignore` is properly configured
3. Update README with your customizations
4. Share via GitHub, zip file, or internal repository

---

## 🔄 Version

**Nexus-v3 Template** - November 2025
**Architecture Version**: 2.0
**Status**: Production Ready

**Key Features**:
- Instruction-driven architecture
- V2.0 YAML format (minimal metadata)
- 4-project onboarding (35-40 min)
- 7 system skills
- MCP integration support
- Progressive disclosure
- CAVE Framework (Concrete → Action → Value → Explanation)

---

## 📝 License

This template is provided as-is for personal and commercial use.
Customize freely to fit your needs!

---

**Ready to begin?** Load `claude.md` and let's get started! 🚀
