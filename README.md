# Nexus

A structured framework for Claude Code that turns beginners into power users with dramatically higher output.

## What It Does

Claude Code produces a lot. Files end up everywhere. Context gets lost between sessions. You re-explain the same things. The AI can't navigate your data. You get overwhelmed. Progress doesn't compound the way it should.

Nexus fixes this with:
- **10-minute integrations** — Connect Slack, HubSpot, Google, Airtable and more with guided setup
- **Structured projects (Builds)** — Interactive planning via discovery → plan → execute → ship
- **Context upload** — Drop in existing files, docs, or examples during onboarding and Claude learns from them
- **Persistent memory** — Goals, preferences, and learnings survive sessions
- **Organized workspace** — Claude knows where your files are
- **Reusable workflows (Skills)** — Automate repetitive tasks, compatible with open source skill libraries
- **Mental models built-in** — Pre-mortem, inversion, JTBD, Pareto and more applied to every plan
- **Cross-compaction continuity** — Resume-context files let Claude dynamically reload exactly what it needs after context resets

## Quick Example

```
You: "create build for LinkedIn content system"

Claude: [DISCOVERY]
        → Who's your target audience?
        → What topics position you as the expert?
        → What's your voice — educational, provocative, personal?
        → What does success look like — followers, DMs, leads?
        → Show me existing content or styles you like — I'll learn from them

        [CHECKS EXISTING WORK]
        → Found: post-templates in workspace
        → Found: audience-research from build-02

        [MENTAL MODEL REVIEW]
        → Jobs to Be Done: Audience hires content to signal expertise
        → Inversion: Fails if inconsistent or generic — adding hooks library
        → Pre-Mortem: Burnout risk at week 3 — adding batch creation

        [PLAN READY]
        → 12 requirements from discovery
        → 3 mental models applied
        → 5 steps defined
```

Next session:
```
You: "hi"

Claude: Resuming BUILD: linkedin-content | Step 1/5
        [Context restored from last session]

        Starting hook generation for your founder audience...
```

## Install

**macOS / Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.sh | bash
```

**Windows (PowerShell):**
```powershell
irm https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.ps1 | iex
```

**What gets installed:**
- Claude Code CLI
- VS Code + Claude extension
- uv (Python package manager for hooks)
- Nexus template files

**Then:** Open VS Code, click Claude icon in sidebar, say "hi".

<details>
<summary>Manual installation</summary>

1. Install [Claude Code](https://claude.ai/download)
2. Install [VS Code](https://code.visualstudio.com/download)
3. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
4. Install extension: `code --install-extension anthropic.claude-code`
5. Clone this repo and open in VS Code

</details>

**Requirements:** macOS 13+, Ubuntu 20.04+, or Windows 10+ | Claude API access

---

## Two Modes

### BUILD Mode
For projects with a beginning, middle, and end.

```
"create build for competitor analysis"
"continue build 2"
"archive linkedin-content"
```

**Build types:** Content systems, research projects, client deliverables, product features

### WORK Mode
For quick tasks and integrations.

```
"send slack message to #team"
"list my hubspot deals"
"generate an image of..."
```

**Rule of thumb:** Creating something new with multiple steps → BUILD. Running an existing workflow → WORK.

---

## Folder Structure

```
Nexus/
├── 00-system/          # Framework (don't edit)
│   ├── core/           # Engine and orchestrator
│   └── skills/         # Built-in skills
├── 01-memory/          # Your persistent context
│   ├── goals.md        # What you're trying to achieve
│   └── user-config.yaml
├── 02-builds/          # Your projects
│   ├── active/         # Work in progress
│   └── complete/       # Finished projects
├── 03-skills/          # Your custom skills
└── 04-workspace/       # Your files and outputs
```

**Your data** (`01-memory/`, `02-builds/`, `03-skills/`, `04-workspace/`) is never touched by updates.

---

## Built-in Integrations

| Service | What You Can Do |
|---------|-----------------|
| **Slack** | Send messages, search channels, upload files |
| **Google** | Gmail, Calendar, Drive, Sheets, Docs, Slides |
| **HubSpot** | Contacts, companies, deals, meetings, notes |
| **Airtable** | Query bases, manage records |
| **Langfuse** | Traces, datasets, prompts, evaluations |
| **NotebookLM** | Create notebooks, generate audio overviews |
| **HeyReach** | LinkedIn outreach campaigns |
| **Gemini** | AI image generation |

Connect any with `"connect [service]"`. Add new integrations with `"add integration"`.

---

## Common Commands

| Command | What It Does |
|---------|--------------|
| `hi` | Start session, see your builds |
| `create build` | Start new project with discovery |
| `continue` / `1` / `2` | Resume a build |
| `connect slack` | Set up an integration |
| `list skills` | See available skills |
| `close session` | Wrap up and save learnings |
| `update nexus` | Get framework updates |

---

## When Things Go Wrong

**Menu doesn't appear:** The session hook may have failed. Check that uv is installed (`uv --version`). If it persists, describe the issue to Claude — it can usually diagnose hook problems.

**Claude seems confused:** Say "let's reset" or start a new session. Context can get corrupted after long conversations.

**Build state seems wrong:** Check `02-builds/active/[build-name]/01-planning/resume-context.md` — this is what Claude reads to restore context.

---

## How It Works

Nexus uses Claude Code's hook system to inject context at session start. When you say "hi":

1. **SessionStart hook** runs, loading your goals, active builds, and skill catalog
2. **Orchestrator** decides what to show based on state
3. **You work** — builds track progress, skills execute workflows
4. **Context persists** — even when Claude's context window compacts, hooks reload the right files

The magic is in the file conventions. Markdown files are executable instructions for the AI. Your builds and skills are just structured folders that Claude knows how to navigate.

---

## Learn More

- [Product Overview](00-system/documentation/product-overview.md) — Problems Nexus solves
- [Framework Overview](00-system/documentation/framework-overview.md) — Technical architecture
- [UX Philosophy](00-system/documentation/ux-onboarding-philosophy.md) — Design principles

---

## Updates

```
"update nexus"
```

Updates only touch `00-system/`, `CLAUDE.md`, and `README.md`. Your memory, builds, skills, and workspace are preserved.

---

**Nexus** — Structure for Claude Code.
