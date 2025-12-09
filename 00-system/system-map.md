# Nexus-v3 System Map

<!-- AI CONTEXT FILE -->
<!-- Purpose: Core system navigation and structure reference -->
<!-- Updated by: System (static framework documentation) -->

**Primary navigation hub for the Nexus-v3 work organization system.**

> **Purpose**: Help AI understand Nexus-v3 system structure and navigation
>
> **Audience**: AI (loaded every session via --startup)
>
> **Maintenance**: Static (part of system framework)

> 📖 **Need more detail?** See [Framework Overview](documentation/framework-overview.md) (optional, load if needed)

---

## 🗺️ Navigation Hub

### Essential Documents

- **📊 [Orchestrator](core/orchestrator.md)** - AI loading sequence and decision logic
- **📖 [Framework Overview](documentation/framework-overview.md)** - Complete system guide (optional, load if needed)

### Navigation Maps

- **🧠 [Memory Map](../01-memory/memory-map.md)** - Context persistence system
- **️ [Workspace Map](../04-workspace/workspace-map.md)** - User's custom folder structure
- **🎯 [Goals](../01-memory/goals.md)** - User objectives and success criteria

---

## 🎯 Overview

Nexus-v3 is a self-guiding work organization system that runs entirely through conversation with Claude AI.

### Core Capabilities

- **📁 Projects**: Temporal work units with planning → execution → outputs
- **🔄 Skills**: Reusable workflows (skill-first execution)
- **🧠 Memory**: Context preservation across AI sessions
- **🤖 Instruction-Driven**: Python script returns complete instructions (no AI interpretation)
- **🎯 Auto-Detection**: YAML-driven project/skill matching

---

## 📁 System Structure

```
Nexus-v3/
│
├── claude.md                       # 🚀 LOAD THIS TO START!
│
├── 00-system/                      # SYSTEM FRAMEWORK
│   ├── system-map.md               # THIS FILE - Navigation hub
│   ├── core/
│   │   ├── orchestrator.md         # AI decision logic
│   │   ├── nexus-loader.py         # Context loading + decision engine
│   │   └── init-memory.py          # Memory initialization script
│   ├── mental-models/              # ⭐ Thinking frameworks (system-level)
│   │   ├── mental-models.md        # Main catalog (on-demand)
│   │   └── references/             # Detailed model guides
│   ├── skills/                     # System skills (10 built-in)
│   │   ├── create-project/
│   │   ├── execute-project/
│   │   ├── create-skill/
│   │   ├── add-integration/
│   │   ├── close-session/
│   │   ├── bulk-complete/
│   │   ├── validate-system/
│   │   ├── archive-project/
│   │   ├── skip-onboarding/
│   │   └── validate-workspace-map/
│   └── documentation/
│       ├── framework-overview.md       # Complete system guide
│       ├── product-overview.md         # Product introduction
│       ├── structure.md                # System structure details
│       ├── skill-file-format.md        # Skill creation guide
│       ├── ux-expert-philosophy.md     # UX design principles
│       ├── ux-onboarding-philosophy.md # Onboarding design
│       └── presentation-materials/     # Business presentations
│
├── 01-memory/                      # CONTEXT PERSISTENCE
│   ├── memory-map.md
│   ├── goals.md
│   ├── roadmap.md
│   ├── user-config.yaml
│   ├── core-learnings.md
│   └── session-reports/
│
├── 02-projects/                    # TEMPORAL WORK
│   ├── 00-onboarding/              # Onboarding projects
│   │   ├── 00-define-goals/
│   │   ├── 01-first-project/
│   │   ├── 02-first-skill/
│   │   └── 03-system-mastery/
│   ├── 05-archived/                # Completed projects
│   └── {ID}-{name}/                # User projects
│       ├── 01-planning/
│       │   ├── overview.md         # YAML metadata
│       │   ├── plan.md
│       │   └── steps.md            # Checkbox list (state source)
│       ├── 02-resources/           # Reference materials
│       ├── 03-working/             # Work-in-progress files
│       └── 04-outputs/             # Final deliverables
│
├── 03-skills/                      # USER SKILLS
│   └── {skill-name}/
│       ├── SKILL.md                # YAML metadata + workflow
│       ├── references/             # (optional)
│       ├── scripts/                # (optional)
│       └── assets/                 # (optional)
│
└── 04-workspace/                   # USER CONTENT
    ├── workspace-map.md
    └── [Your folders]/
```

---

## 🚀 Quick Start (AI Agents)

**Three-Step Pattern** (every session):

1. **Run**: `python 00-system/core/nexus-loader.py --startup`
2. **Load**: All files from `files_to_load` array (parallel)
3. **Follow**: `instructions.action` exactly (no interpretation)

---

## 🏗️ Core Entities

### Projects
- **Purpose**: Temporal work with beginning, middle, end
- **Location**: `02-projects/{ID}-{name}/`
- **Structure**: 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/)
- **State**: Checkbox tasks in `steps.md`
- **Lifecycle**: PLANNING → IN_PROGRESS → COMPLETE → ARCHIVED

### Skills
- **Purpose**: Reusable workflows for repetitive tasks
- **Location**: `03-skills/{skill-name}/`
- **Priority**: User skills > system skills
- **Routing**: Skills-first execution (most important principle)

### Memory
- **Purpose**: Context preservation across sessions
- **Location**: `01-memory/`
- **Updates**: Auto-updated by close-session skill

---

## 📜 Core Infrastructure

### nexus-loader.py
**Purpose**: Context loading + decision engine (MASTER CONTROLLER)

**Commands**:
- `--startup` - Load session context + return instructions
- `--project {ID}` - Load specific project
- `--skill {name}` - Load specific skill

**Output**: JSON with `system_state`, `files_to_load`, `instructions`, `metadata`

### orchestrator.md
**Purpose**: AI decision logic (minimal, instruction-driven)

**Key**: Python script is master controller. AI just follows instructions.

---

## 🗂️ YAML Metadata

### Project YAML (overview.md)
```yaml
---
id: 10-website-redesign
name: Website Redesign
status: IN_PROGRESS
description: Load when user mentions "website", "redesign", "site update"
created: 2025-11-01
last_worked: 2025-11-04
tags: [web, design]
---
```

**Note**: `tasks_total`, `tasks_completed`, `progress` auto-calculated from steps.md

### Skill YAML (SKILL.md)
```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update", "progress summary". Generate comprehensive weekly work summary.
---
```

**V2.0 Format**: Only `name` + `description` (minimal metadata, progressive disclosure)

---

## 📂 File Naming

**Projects**: `{ID}-{name}`
- ID: Zero-padded numeric (00, 01, 10, 11)
- Name: lowercase-with-hyphens
- Example: `10-website-redesign`

**Skills**: `{skill-name}`
- Name: lowercase-with-hyphens
- Prefer verb-based: `generate-report`, `analyze-data`
- Example: `weekly-status-report`

**Memory Files**: Fixed names
- `goals.md`, `roadmap.md`, `user-config.yaml`, `core-learnings.md`, `memory-map.md`

---

## 🔄 Instruction-Driven Architecture

**Key Principle**: Python script analyzes state and returns complete instructions. AI follows exactly.

**Benefits**:
- ✅ Zero interpretation
- ✅ Zero manual state detection
- ✅ Deterministic behavior
- ✅ Easy debugging

**Metadata Scanning**: Every `--startup` scans YAML from all projects/skills

**Token Budget**: Warns if metadata >7,000 tokens (3.5% of context window)

---

**Nexus-v3** - Self-guiding work organization through AI conversation and instruction-driven automation.

---

**Version**: 2.1
**Last Updated**: 2025-11-24
**Status**: Production Ready
