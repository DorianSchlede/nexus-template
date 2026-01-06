# System Map - Core Essentials

**Purpose**: Navigate Nexus structure and understand execution flow

---

## 📁 Core Structure

```
Nexus/
├── 00-system/
│   ├── core/
│   │   ├── orchestrator.md         # Behavior rules, routing
│   │   └── nexus-loader.py         # Context injection
│   └── skills/                     # System workflows
│
├── 01-memory/
│   ├── goals.md                    # User identity
│   └── session-reports/            # History
│
├── 02-projects/                    # BUILD mode work
│   └── {ID}-{name}/
│       ├── 01-planning/            # 4 phases
│       └── 04-outputs/             # Deliverables
│
├── 03-skills/                      # EXECUTE mode work
│   └── {skill-name}/SKILL.md       # Workflows
│
└── 04-workspace/                   # User content
    └── workspace-map.md            # Structure doc
```

---

## 🔄 Execution Flow

```
Session Starts
     ↓
Hook Injects Context (<200ms)
- orchestrator.md (behavior)
- skills catalog (what's available)
- active projects (current work)
- user goals (identity)
- dynamic instructions (what to do next)
     ↓
Claude Executes
- If BUILD work → plan-project or execute-project
- If EXECUTE work → load skill
- If unclear → display menu
```

---

## 🎯 Quick Decisions

| User Says | You Do |
|-----------|--------|
| "Build X" / "Create X" | plan-project |
| "Continue project 29" | execute-project |
| "Send slack message" | Load skill |
| "What can you do?" | Display menu |

---

## 📂 File Locations

| Need | Path |
|------|------|
| Behavior rules | `00-system/core/orchestrator.md` |
| User identity | `01-memory/goals.md` |
| Project work | `02-projects/{ID}-{name}/` |
| Workflows | `03-skills/{name}/SKILL.md` |
| User content | `04-workspace/` |

---

## 🔧 CLI Commands

```bash
# Load project context
python 00-system/core/nexus-loader.py --project {ID}

# Load skill
python 00-system/core/nexus-loader.py --skill {name}

# Discover skills in category
load-skill {category} --help
```

---

**That's it. Everything else is progressive disclosure.**
