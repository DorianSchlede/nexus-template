<div align="center">

# Nexus

**Build yourself the AI copilot system you couldn't dream of.**

Experience efficiency on another level, let AI perfectly navigate your context and interactively plan to get exactly what you want.
<br/>
Optimized onboarding experience including context import and roadmap building.

Made for users of ChatGPT, Gemini Claude Code, Cursor, Antigravity, Cowork — and anyone who wants to maximize AI efficiency.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude-Code-orange.svg)](https://claude.ai/download)
[![Cursor](https://img.shields.io/badge/Cursor-AI-blue.svg)](https://cursor.com)
[![GitHub stars](https://img.shields.io/github/stars/DorianSchlede/nexus-template?style=social)](https://github.com/DorianSchlede/nexus-template)

[Get Started](#install) · [Documentation](#learn-more) · [Contributing](#contributing)

</div>

---

## Who This Is For

**Using ChatGPT, Gemini, or Claude chat?**
You're copy-pasting and repeating yourself. 
AI coding tools let you *execute* — write files, run code, integrate with your stack. They seem intimidating, but Nexus creates easy access and power with structure from day one.

**Using Claude Code or Cursor?**
You have execution power but no organization, your AI agent sometimes gets lost. Files scatter, context dies between sessions, you re-explain the same things. You don't get exactly what you want. Nexus adds memory, projects, and workflows that build on each other.

**Using Claude Cowork?**
You have file access and skills, but no structured project management, no cross-session memory, no guided setup. Nexus fills those gaps.

**Using Antigravity or other frameworks?**
Nexus differentiates with interactive planning (discovery → mental models → steps), 10-minute integrations for any API, and resume context that survives compaction.

**The key difference:** You can build complete systems — automations, workflows, integrations — because AI always has your full context: files, goals, and work-in-progress. You describe what you want, Nexus helps you ship it.

---

## The Gap

| | Chat | Cowork | Claude Code | Cursor | **Nexus** |
|:--|:--:|:--:|:--:|:--:|:--:|
| Execute code | — | ✓ | ✓ | ✓ | ✓ |
| Read/write files | — | ✓ | ✓ | ✓ | ✓ |
| **AI navigates your files** | — | Folder | Project | Project | **Full map** |
| **Guided onboarding** | — | — | — | — | ✓ |
| **Context import** | — | — | — | — | ✓ |
| **Roadmapping** | — | — | — | — | ✓ |
| **Interactive planning** | — | — | — | — | ✓ |
| **Structured projects** | — | — | — | — | ✓ |
| Software integrations | — | Plugins | Manual | Manual | **Any API, 10 min** |
| Session context | Memory | Limited | Summary | Summary | **Full restore** |
| Reusable workflows | — | Skills | Skills | — | **Skills + library** |

---

## What Changes

### Before: Chat
```
You: Write me a LinkedIn content strategy
AI: Here's a strategy... [2000 words]
You: [copies to a doc somewhere, forgets about it, asks the same thing next month]
```

### Before: Claude Code / Cursor
```
You: Write me a LinkedIn content strategy
AI: [creates strategy.md, templates.md, schedule.md in random places]

[next session]
You: Continue the linkedin work
AI: I don't have context on that project. Can you explain what you were working on?
```

### Before: Cowork
```
You: Write me a LinkedIn content strategy
Cowork: [creates files in your designated folder, uses skills]

[next session]
You: Continue the linkedin work
Cowork: [starts fresh, no memory of previous session structure]
```

### After: Nexus
```
You: create build for linkedin content strategy

Nexus: [DISCOVERY]
       → Who's your target audience?
       → What topics position you as expert?
       → Show me content you like — I'll learn the style

       [MENTAL MODELS]
       → Pre-mortem: What kills this at week 3? → Adding batch creation
       → Inversion: What makes content fail? → Generic + inconsistent
       → JTBD: What job does your content do? → Signal expertise to buyers

       [PLAN]
       → 5 steps defined
       → Progress tracked
       → Outputs organized

[next session]
You: hi

Nexus: Welcome back.

       Active: BUILD #5 linkedin-content | Step 3/5
       Last session: Completed hook templates
       Next: Post scheduling system

       Continue?
```

---

## Install

<div align="center">

[![Use this template](https://img.shields.io/badge/Use_this_template-238636?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DorianSchlede/nexus-template/generate)

</div>

Click the button, clone your new repo, open in your editor with AI enabled.

**Works with:**
- Claude Code (VS Code extension or CLI)
- Cursor (`.cursor/rules/` included)
- Any tool that reads project instructions

**Or run the installer:**

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.ps1 | iex
```

<details>
<summary><strong>Manual setup</strong></summary>

1. Install [Claude Code](https://claude.ai/download) or [Cursor](https://cursor.com)
2. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Clone this repo and open in your editor
4. Say "hi" to start

</details>

---

## Core Concepts

| Concept | What It Is | Example |
|---------|------------|---------|
| **Builds** | Projects with discovery, planning, execution, and delivery | `"create build for competitor analysis"` |
| **Skills** | Reusable workflows that run the same way every time | `"send slack message to #team"` |
| **Memory** | Goals, preferences, and learnings that persist across sessions | `01-memory/goals.md` |
| **Roadmap** | Plan what to build next — prioritized, goal-aligned, informed by context | `"create roadmap"` |
| **Context Import** | Upload any files — Nexus analyzes them and learns your domain | `"analyze context"` |

---

## Context Import

Jumpstart any Nexus instance with your existing knowledge.

**Upload anything:**
- PDFs, Word docs, text files
- ChatGPT/Claude export files
- Code, configs, documentation
- Screenshots, images

**What happens:**
1. Drop files into `01-memory/input/`
2. Nexus spawns parallel SubAgents to analyze everything
3. Extracts: themes, tools mentioned, build ideas, domain patterns
4. Saves structured insights (not dumped into chat)
5. Informs your goals, workspace, and first build

```
You: analyze context

Nexus: Found 23 files. Analyzing in 5 parallel batches...

       Themes discovered:
       → SaaS onboarding flows
       → Product-led growth metrics
       → Customer interview transcripts

       BUILD ideas from your files:
       → Onboarding audit framework
       → PLG metrics dashboard
       → Interview synthesis system

       Saved to: 01-memory/input/_analysis/
```

Works during onboarding or anytime later.

---

## Integrations

**Built-in** (ready to connect):

| Service | What You Get |
|---------|-------------|
| **Slack** | Messages, channels, file uploads |
| **Google** | Gmail, Calendar, Drive, Sheets, Docs, Slides |
| **HubSpot** | Contacts, companies, deals, full pipeline |
| **Airtable** | Query and manage any base |
| **Langfuse** | LLM tracing, datasets, evaluations |
| **NotebookLM** | Notebooks, audio overviews |
| **HeyReach** | LinkedIn outreach campaigns |
| **Gemini** | Image generation |

**Any API** — Add new integrations in ~10 minutes with guided setup:
```
"add integration"
"connect [service name]"
```

Nexus walks you through API keys, authentication, and creates the skill structure automatically.

---

## For Power Users

<details>
<summary><strong>Claude Code / Cursor users</strong></summary>

What Nexus adds to your existing workflow:

- **SessionStart hooks** — Context injected automatically. Goals, builds, skills load without you asking.
- **Compaction survival** — `resume-context.md` in each build means you don't lose state when context resets.
- **Folder conventions** — `02-builds/` for projects, `03-skills/` for automations. AI knows where things go.
- **Mental models** — Pre-mortem, inversion, JTBD applied during planning. Better plans, less rework.
- **Skill library** — Standard format means you can export skills, import others', build a collection.

</details>

<details>
<summary><strong>Cowork users</strong></summary>

What Nexus adds beyond Cowork's capabilities:

- **Structured projects** — Builds have phases: discovery, planning, execution, delivery. Not just "do this task."
- **Cross-session memory** — Goals and learnings persist. Cowork's Knowledge Bases are coming; Nexus has this now.
- **Guided onboarding** — Setup wizard, not "figure it out yourself."
- **Integration architecture** — Master skills + operation skills pattern. Connect once, get dozens of operations.

</details>

<details>
<summary><strong>Framework users (Antigravity, etc.)</strong></summary>

Key Nexus differentiators:

- **Interactive planning** — Discovery questions, mental models, step generation. Not just task lists.
- **Resume context** — Each build auto-updates `resume-context.md`. Cross-session continuity without manual notes.
- **Smart routing** — "Continue the linkedin thing" finds the right build. No exact command syntax.
- **10-minute integrations** — Guided flow for any API. Not just pre-built connectors.
- **Context import** — Bulk upload files to jumpstart any instance. SubAgent analysis extracts structure.

</details>

---

## Project Structure

```
Nexus/
├── 00-system/          # Framework core (don't edit)
│   ├── core/           # Orchestrator, hooks, engine
│   └── skills/         # Built-in skills
├── 01-memory/          # Your persistent context
│   └── input/          # Context import staging area
├── 02-builds/          # Your projects
│   ├── active/
│   └── complete/
├── 03-skills/          # Your custom skills
├── 04-workspace/       # Your files and outputs
├── .cursor/rules/      # Cursor AI configuration
├── CLAUDE.md           # Claude Code configuration
└── AGENTS.md           # Generic agent configuration
```

> Your data (`01-04`) is never touched by framework updates.

---

## Commands

| Say This | What Happens |
|----------|--------------|
| `hi` | Start session, see active builds |
| `create build [name]` | New project with discovery + planning |
| `continue` / `1` / `2` | Resume a build by number |
| `create roadmap` | Plan what to build, prioritized by your goals |
| `analyze context` | Import and analyze uploaded files |
| `connect [service]` | Set up an integration |
| `add integration` | Add any new API |
| `list skills` | See available workflows |
| `close session` | Save learnings, wrap up |
| `update nexus` | Get framework updates |

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Menu doesn't appear | Check uv: `uv --version`. Hooks need it. |
| AI seems lost | Say "let's reset" or start fresh session |
| Wrong build state | Check `02-builds/active/[name]/01-planning/resume-context.md` |
| Cursor not reading rules | Ensure `.cursor/rules/nexus.mdc` exists |

---

## Learn More

- [Product Overview](00-system/documentation/product-overview.md) — What problems Nexus solves
- [Framework Overview](00-system/documentation/framework-overview.md) — Technical architecture
- [UX Philosophy](00-system/documentation/ux-onboarding-philosophy.md) — Design principles

---

## Contributing

Contributions welcome:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Open a Pull Request

For bugs and requests: [open an issue](https://github.com/DorianSchlede/nexus-template/issues)

---

## Updates

```
"update nexus"
```

Updates only touch `00-system/`. Your memory, builds, skills, and workspace stay intact.

---

<div align="center">

**Nexus** — Stop re-explaining. Start compounding.

[Get Started](#install) · [Star this repo](https://github.com/DorianSchlede/nexus-template)

</div>
