# Nexus

> **Stop prompting. Start building.**

The operating system for Claude Code that turns chaos into systems.

**ChatGPT/Gemini user?** This is your gateway to real AI power.
**Claude Code user?** This is how you 10x.

## The Problem

Claude Code is incredibly powerful. It produces *so much* — but you lose track. Files end up everywhere. The AI can't navigate your content. Context between sessions gets lost.

Sometimes Claude doesn't build exactly what you want. You spend hours cleaning up, re-explaining, starting over.

You spend more time managing Claude than using it.

## The Secret

**In Nexus, AI helps you get the most out of yourself.**

Plan for 10 minutes. Get exactly what you want. With Nexus, the chaos stops.

**How?** Through structured, guided planning that ensures Claude understands:

- **A) What you want exactly** — Intelligent questioning extracts your real requirements
- **B) What already exists** — Connects new work to your existing files and builds
- **C) What research says** — Pulls in context from the internet when needed

Most importantly: **Nexus lets AI navigate your files and context.** It knows where things are, what you've built, and how everything connects.

Built to transition curious GPT/Gemini users to the most powerful AI coding tool, and to help existing Claude Code users achieve even more.

```
You: "create build for LinkedIn content system"

Claude: [DISCOVERY - asks exactly the right questions]
        → Who's your audience?
        → What topics position you as an expert?
        → What does success look like?

        [CHECKS YOUR EXISTING WORK]
        → Found: post-templates in workspace
        → Found: audience-research in build-02
        → Build on these?

        [IDENTIFIES RISKS]
        → Risk: Content without clear CTA
        → Adding: CTA templates to deliverables

        [PLAN READY]
        ✓ 12 requirements from your answers
        ✓ 3 risks identified
        ✓ 5 concrete steps

        Ready. Say "hi" next session to execute.
```

**Then executes perfectly** — because Claude knows exactly what you want:

```
Next session:

You: "hi"

Claude: 📦 BUILD: linkedin-content | Step 1/5

        [Remembers your audience, topics, constraints]

        Here are 50 hooks tailored to founders interested in AI:
        - "Most founders waste 10 hours/week on content..."
        - "Last month I automated my entire posting..."

        ✓ Step 1 complete. Progress saved.
```

**Plan well → Execute perfectly.** Context compounds forever. You never re-explain.

---

## Your Dashboard

Every session starts here — your builds, skills, and progress at a glance:

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝


  BUILD ─────────────────────────────── Create & finish projects
  Start something new, or continue where you left off.

    1. linkedin-content     [Step 3/5]  Writing hooks
    2. competitor-research  [Step 1/4]  Starting analysis
    3. email-templates      [PLANNING]  Ready to execute

    "plan" → new build    "1" → continue build 1    "manage" → all builds


  WORK ──────────────────────────────── Run your automations
  Skills are reusable workflows you build once and run anytime.

    YOUR SKILLS (03-skills/)
    weekly-report       client-onboard      competitor-scan

    SYSTEM SKILLS (150+ built-in)
    slack    google    hubspot    airtable    langfuse    gemini

    "connect slack" → setup    "list skills" → browse all    "create skill" → new


  CHAT ─────────────────────────────────────── Just talk
  No structure needed. Ask anything, I'll help directly.

```

Say a number to continue a build. Say a skill name to run it. Or just chat.

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

This installs everything:
- ✅ Claude Code
- ✅ VS Code + Claude extension
- ✅ uv (for Nexus hooks)
- ✅ Nexus template

**Then:**
1. VS Code opens automatically
2. Click the **Claude icon** in the sidebar
3. Say **"hi"**
4. Follow the 10-15 minute quick-start

> **Requirements:** macOS 13+, Ubuntu 20.04+, or Windows 10 1809+ | 4GB+ RAM

<details>
<summary>Manual Installation</summary>

| Software | Install |
|----------|---------|
| **Claude Code** | `curl -fsSL https://claude.ai/install.sh \| bash` |
| **VS Code** | [code.visualstudio.com](https://code.visualstudio.com/download) |
| **uv** | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **Claude Extension** | `code --install-extension anthropic.claude-code` |

Then clone or download Nexus and open in VS Code.

</details>

---

## Features

| | What You Get |
|---|---|
| **Interactive Planning** | Claude asks exactly the right questions. Reviews dependencies. Plans emerge from dialogue. Perfect execution in one shot. |
| **Persistent Context** | Your goals, progress, and learnings survive across sessions. When context compacts, Nexus reloads the right files automatically. |
| **Smart Workspace** | Your folders become Claude's workspace. It knows where things are, saves outputs in the right places. No more scattered files. |
| **Live Dashboard** | See all your builds and skills at a glance. Resume any build instantly. Your toolkit grows with you. |
| **10-Minute Integrations** | Connect Slack, HubSpot, Airtable, Google, and more. Guided setup with API discovery built in. |
| **Portable Skills** | 150+ built-in skills. Drop any open source skill into `03-skills/` and use it immediately. |

---

## Two Modes

### BUILD — Building Out Your System
For creating the pieces of your system. Has a beginning, middle, and end.

| Type | Examples |
|------|----------|
| **Content** | LinkedIn machine, newsletter pipeline, content calendar |
| **Client** | Onboarding process, project templates, deliverables |
| **Research** | Competitor analysis, market research, synthesis |
| **Product** | Feature specs, documentation, release workflows |

Each build: **discover → plan → execute → ship**

### WORK — Using Your System
For running your system day-to-day. Quick actions and integrations.

```
"send slack message to #team"
"analyze this competitor"
"draft a response to this email"
"generate this week's posts"
```

**Rule:** Creating something new → BUILD. Using what you built → WORK.

---

## The Four Primitives

### 1. Memory
Your persistent context. Loaded every session.

```
01-memory/
├── goals.md           ← Your purpose and success metrics
├── user-config.yaml   ← Preferences and state
└── roadmap.md         ← What you're building (optional)
```

### 2. Builds
Structured projects with clear phases.

```
02-builds/active/01-content-system/
├── 01-planning/       ← Discovery, plan, steps
├── 02-resources/      ← Reference materials
├── 03-working/        ← Drafts in progress
└── 04-outputs/        ← Final deliverables
```

### 3. Skills
Workflows triggered by a phrase. 150+ built-in.

```
"connect slack"   → Integration setup
"create build"    → Build planning
"learn nexus"     → System tutorial
```

Create your own or drop in any open source skill.

### 4. Workspace
Your output folder. Organized your way.

```
04-workspace/
├── content/           ← Posts, drafts
├── templates/         ← Reusable formats
└── workspace-map.md   ← Structure doc
```

Claude reads `workspace-map.md` to navigate your files.

---

## Integrations

8 built-in, unlimited via `add integration`:

| Service | Trigger | Capabilities |
|---------|---------|--------------|
| **Slack** | "connect slack" | Messages, channels, search |
| **Google** | "connect google" | Drive, Calendar, Gmail, Sheets, Docs |
| **HubSpot** | "connect hubspot" | Contacts, companies, deals, meetings |
| **Langfuse** | "connect langfuse" | Traces, datasets, prompts, scores |
| **Airtable** | "connect airtable" | Query bases, manage records |
| **NotebookLM** | "connect notebooklm" | AI notebooks, audio overviews |
| **HeyReach** | "connect heyreach" | LinkedIn outreach |
| **Gemini Image** | "generate image" | AI image generation |

---

## Key Commands

| You Say | What Happens |
|---------|--------------|
| `"hi"` | Load Nexus, see your builds |
| `"create build"` | Start new build with discovery |
| `"continue"` | Resume current build |
| `"1"` or `"2"` | Quick-select build by number |
| `"connect [service]"` | Set up integration |
| `"update nexus"` | Get latest updates |

---

## Updates

Your data is never touched:

| Updated (system) | Protected (yours) |
|------------------|-------------------|
| `00-system/` | `01-memory/` |
| `CLAUDE.md` | `02-builds/` |
| `README.md` | `03-skills/`, `04-workspace/` |

```
You: "update nexus"

Claude: UPDATE AVAILABLE: v0.9.0 → v0.10.0
        12 files will be updated
        Proceed? (yes/no)
```

---

## Troubleshooting

**Menu doesn't appear?** Ask: *"The menu didn't show up, can you help?"*

**Something broken?** Describe the problem. Claude diagnoses and fixes most issues automatically.

---

## Learn More

- [Product Overview](00-system/documentation/product-overview.md) — The problems Nexus solves
- [Framework Overview](00-system/documentation/framework-overview.md) — Technical deep dive

---

# Technical Reference

## Folder Structure

```
Nexus/
├── CLAUDE.md                    # Entry point
├── 00-system/                   # Framework (don't modify)
│   ├── core/                    # Engine
│   ├── skills/                  # 150+ built-in skills
│   └── documentation/           # Guides
├── 01-memory/                   # Your context
├── 02-builds/                   # Your projects
│   ├── active/
│   └── complete/
├── 03-skills/                   # Your custom skills
└── 04-workspace/                # Your files
```

## Build Lifecycle

| Status | Meaning |
|--------|---------|
| `PLANNING` | Being designed |
| `IN_PROGRESS` | Active work |
| `COMPLETE` | Done |
| `ARCHIVED` | Moved to archive |

## Built-in Skills

### Build Management
| Skill | Trigger |
|-------|---------|
| `plan-build` | "create build" |
| `execute-build` | "continue [name]" |
| `archive-build` | "archive [name]" |

### Learning
| Skill | Time |
|-------|------|
| `quick-start` | 10-15 min |
| `learn-builds` | 8-10 min |
| `learn-skills` | 10-12 min |
| `learn-nexus` | 15-18 min |

### Integrations (100+ skills)
| Service | Skills |
|---------|--------|
| Slack | 5 |
| Google | 12 |
| HubSpot | 20+ |
| Langfuse | 50+ |
| Airtable, NotebookLM, HeyReach, Gemini | 3 each |

## Glossary

| Term | Meaning |
|------|---------|
| **Build** | Structured project: discover → plan → execute → ship |
| **Skill** | Reusable workflow triggered by phrase |
| **Memory** | Persistent context loaded every session |
| **Workspace** | Your output folder, AI-navigable |
| **Compaction** | When Claude summarizes context; Nexus reloads right files |
| **Discovery** | Interactive Q&A that shapes what gets built |

---

**Nexus** — Build any system in no time.
