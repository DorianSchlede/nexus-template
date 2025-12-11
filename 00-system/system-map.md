# Nexus System Map

<!-- AI CONTEXT FILE -->
<!-- Purpose: System structure reference (NOT behavior rules) -->
<!-- For AI behavior/routing: See orchestrator.md -->

**System structure reference for Nexus-v4.**

> **Purpose**: Help AI navigate system structure and file locations
>
> **For AI behavior rules**: See [orchestrator.md](core/orchestrator.md)
>
> **Maintenance**: Static (part of system framework)

---

## 🗺️ Navigation Hub

| Document | Purpose |
|----------|---------|
| **[Orchestrator](core/orchestrator.md)** | AI behavior rules, routing, menu display |
| **[Framework Overview](documentation/framework-overview.md)** | Complete system guide (detailed) |
| **[Memory Map](../01-memory/memory-map.md)** | Context persistence system |
| **[Workspace Map](../04-workspace/workspace-map.md)** | User's custom folders |

---

## 📁 System Structure

```
Nexus-v4/
│
├── CLAUDE.md                       # 🚀 Entry point (loads orchestrator)
│
├── 00-system/                      # SYSTEM FRAMEWORK
│   ├── system-map.md               # THIS FILE
│   ├── core/
│   │   ├── orchestrator.md         # AI behavior rules
│   │   └── nexus-loader.py         # Master controller script
│   ├── skills/                     # System skills
│   │   ├── create-project/
│   │   ├── execute-project/
│   │   ├── create-skill/
│   │   ├── setup-goals/
│   │   ├── setup-workspace/
│   │   ├── learn-projects/
│   │   ├── learn-skills/
│   │   ├── learn-nexus/
│   │   ├── close-session/
│   │   └── ...more
│   └── documentation/
│       ├── framework-overview.md
│       └── product-overview.md
│
├── 01-memory/                      # CONTEXT PERSISTENCE
│   ├── goals.md                    # User objectives
│   ├── user-config.yaml            # Preferences
│   ├── core-learnings.md           # Accumulated insights
│   └── session-reports/            # Historical sessions
│
├── 02-projects/                    # TEMPORAL WORK
│   ├── 00-onboarding/              # Legacy onboarding projects
│   └── {ID}-{name}/                # User projects
│       ├── 01-planning/
│       │   ├── overview.md         # YAML metadata
│       │   └── steps.md            # Task checkboxes
│       ├── 02-resources/
│       ├── 03-working/
│       └── 04-outputs/
│
├── 03-skills/                      # USER SKILLS (priority over system)
│   └── {skill-name}/
│       ├── SKILL.md                # YAML + workflow
│       ├── references/
│       └── scripts/
│
└── 04-workspace/                   # USER CONTENT
    ├── workspace-map.md            # Folder structure documentation
    └── [Your folders]/
```

---

## 🗂️ YAML Metadata

### Project YAML (overview.md)
```yaml
---
id: 10-website-redesign
name: Website Redesign
status: IN_PROGRESS
description: Load when user mentions "website", "redesign"
created: 2025-11-01
---
```
**Note**: `tasks_total`, `tasks_completed`, `progress` auto-calculated from steps.md

### Skill YAML (SKILL.md)
```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update"
---
```

---

## 📂 File Naming

| Type | Format | Example |
|------|--------|---------|
| Projects | `{ID}-{name}` | `10-website-redesign` |
| Skills | `{skill-name}` | `weekly-status-report` |
| Memory | Fixed names | `goals.md`, `user-config.yaml` |

**Naming rules**: lowercase-with-hyphens, verb-based for skills

---

## 🔧 CLI Reference

```bash
python 00-system/core/nexus-loader.py --startup    # Load session context
python 00-system/core/nexus-loader.py --project ID # Load specific project
python 00-system/core/nexus-loader.py --skill name # Load specific skill
```

**Output**: JSON with `system_state`, `memory_content`, `instructions`, `metadata`

---

**Version**: 4.0 | **Updated**: 2025-12-11
