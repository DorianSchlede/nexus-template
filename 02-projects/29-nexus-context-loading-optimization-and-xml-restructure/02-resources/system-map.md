# System Map - Nexus Structure

**Purpose**: Quick navigation and understanding of the Nexus system

---

## 📁 File Structure

```
nexus/
├── 00-system/
│   ├── core/
│   │   ├── orchestrator.md        # AI behavior rules
│   │   └── nexus-loader.py        # Context injection
│   └── skills/                    # Core workflows (plan-project, execute-project)
│
├── 01-memory/
│   ├── goals.md                   # User identity
│   └── session-reports/           # History
│
├── 02-projects/                   # BUILD mode
│   └── {ID}-{name}/
│       ├── 01-planning/           # 4 phases
│       ├── 02-resources/
│       ├── 03-working/
│       └── 04-outputs/
│
├── 03-skills/                     # EXECUTE mode
│   └── {skill-name}/
│       └── SKILL.md
│
└── 04-workspace/                  # User content
    └── workspace-map.md
```

---

## 🔄 How It Works

```
User Opens Session
        ↓
Hook Runs (<200ms)
        ↓
Loads Context:
- orchestrator.md (what to do)
- skills catalog (what's available)
- active projects (current work)
- user goals (who you are)
        ↓
Generates Dynamic Instruction
(based on current state)
        ↓
Claude Executes
```

---

## 🎯 Routing Logic

| User Says | Claude Does |
|-----------|-------------|
| "Build X" / "Create X" | Load plan-project |
| "Continue project 29" | Load execute-project |
| "Send message" | Load skill |
| "What can you do?" | Display menu |

**Priority**: System skills (P1) → User skills (P2) → Projects (P3+)

---

## 📂 File Paths Quick Reference

| Need | Path |
|------|------|
| Behavior rules | `00-system/core/orchestrator.md` |
| Context loader | `00-system/core/nexus-loader.py` |
| User identity | `01-memory/goals.md` |
| Build work | `02-projects/{ID}-{name}/` |
| Execute work | `03-skills/{name}/SKILL.md` |
| User files | `04-workspace/` |

---

## 🔧 Common CLI Commands

```bash
# Load project
python 00-system/core/nexus-loader.py --project {ID}

# Load skill
python 00-system/core/nexus-loader.py --skill {name}

# Discover skills
load-skill {category} --help
```

---

## 📊 Two Modes

### BUILD Mode (Projects)
**When**: Want to BUILD something with beginning/middle/end
**Skills**: plan-project → execute-project
**Structure**: 02-projects/{ID}-{name}/

### EXECUTE Mode (Skills)
**When**: Want to EXECUTE a task or workflow
**Skills**: Any skill in 00-system/skills/ or 03-skills/
**Structure**: Direct execution, no project overhead

---

## 🎨 Visual Flow Diagram

```
┌─────────────────────────────────────────────────────┐
│ Build Something?                                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│  User: "Build API integration"                      │
│         ↓                                            │
│  plan-project (Planning Phase)                      │
│    - Create 02-projects/{ID}-api-integration/       │
│    - Fill: overview, plan, steps                    │
│    - Close session                                  │
│         ↓                                            │
│  [New Session]                                       │
│         ↓                                            │
│  User: "Continue project 29"                        │
│         ↓                                            │
│  execute-project (Execution Phase)                  │
│    - Read steps.md                                  │
│    - Execute tasks                                  │
│    - Mark [x] complete                              │
│    - Update progress                                │
│         ↓                                            │
│  Project COMPLETE                                   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

```
┌─────────────────────────────────────────────────────┐
│ Execute Something?                                   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  User: "Send slack message"                         │
│         ↓                                            │
│  Load slack-send-message skill                      │
│         ↓                                            │
│  Execute workflow                                   │
│         ↓                                            │
│  Done (no project needed)                           │
│                                                      │
└─────────────────────────────────────────────────────┘
```

---

## 📍 Where Files Live

**System Files** (never modified by user):
```
00-system/
├── core/orchestrator.md              # Routing rules
├── core/nexus-loader.py              # Hook logic
├── skills/plan-project/              # Project planning
├── skills/execute-project/           # Project execution
└── skills/close-session/             # Save state
```

**User Files** (created/modified during work):
```
01-memory/goals.md                    # Your identity
02-projects/{ID}-{name}/              # Your build work
03-skills/{custom-skill}/             # Your workflows
04-workspace/{your-folders}/          # Your content
```

---

**That's it.** Everything else loads on-demand.
