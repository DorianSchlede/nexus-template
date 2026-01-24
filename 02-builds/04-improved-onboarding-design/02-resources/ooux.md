# Framework 1: Object-Oriented UX (OOUX) v2

**Project**: 02-nexus-ui-wireframing
**Framework**: Information Architecture
**Version**: 2.0 - Updated for Build vs Work model
**Status**: CONFIRMED

---

## Core Question

> What are the OBJECTS in the system and how do they relate?

---

## The Four Pillars (Updated v2)

```
+---------------------------------------------------------------------+
|                      NEXUS: THE FOUR PILLARS                         |
|                                                                      |
|  +---------------+     +---------------+                             |
|  |  01-MEMORY    |     |  02-BUILDS    |                             |
|  |   (Brain)     |     |  (Workshop)   |                             |
|  |               |     |               |                             |
|  |  Goals        |     |  Projects     |                             |
|  |  Context      |     |  4 Documents: |                             |
|  |  Preferences  |     |  - Overview   |                             |
|  |               |     |  - Discovery  |                             |
|  |               |     |  - Plan       |                             |
|  |               |     |  - Steps      |                             |
|  +---------------+     +---------------+                             |
|                                                                      |
|  +---------------+     +---------------+                             |
|  |  03-SKILLS    |     | 04-WORKSPACE  |                             |
|  |  (Workforce)  |     | (Your Files)  |                             |
|  |               |     |               |                             |
|  |  Automations  |     |  By domain    |                             |
|  |  Integrations |     |  Your docs    |                             |
|  |  Quick Actions|     |  Build outputs|                             |
|  +---------------+     +---------------+                             |
|                                                                      |
+---------------------------------------------------------------------+
```

---

## Build vs Work: The Core Mental Model

**v2 Key Insight**: The system has two primary modes of operation:

| Build | Work |
|-------|------|
| Create something NEW | USE what was built |
| Finite (has end) | Ongoing (repeatable) |
| Plan → Build → Done | Trigger → Execute → Result |
| Output: Artifacts | Output: Outcomes |
| Tab: 🔨 Build | Tab: 💼 Work |

---

## Object Definitions (v2)

### 1. MEMORY (`01-memory/`)

**What**: Your extended brain - persistent knowledge about YOU.

| Attribute | Description |
|-----------|-------------|
| `goals.md` | Role, objectives, work style |
| `context.md` | Who you are, what you're working on |
| `user-config.yaml` | Preferences, system state |

**Actions**: Read (always), Update (via Settings or chat)

**UI Representation**:
- Settings panel
- Onboarding steps 1-3 create this
- Always loaded as AI context

---

### 2. BUILD (`02-builds/`)

**What**: Your workshop - projects with clear lifecycle and 4-document structure.

**v2 Update**: Every Build creates exactly 4 documents:

| Document | Purpose |
|----------|---------|
| `01-overview.md` | What and why (purpose, scope, success criteria) |
| `02-discovery.md` | Information gathering (resources, research, context) |
| `03-plan.md` | How to approach (methodology, decisions) |
| `04-steps.md` | Execution checklist (tasks for AI to execute) |

**Lifecycle**:
```
PLANNING 🔵 → BUILDING 🟡 → DONE ✅
```

**Actions**: Create, Plan (4 docs), Build (AI executes), Complete, Archive

**UI Representation**:
- 🔨 Build tab (multiple allowed)
- Roadmap Kanban cards
- 4-document tab navigation during Planning

---

### 3. SKILL (`03-skills/`)

**What**: Your AI workforce - reusable automations triggered in Work mode.

| Attribute | Description |
|-----------|-------------|
| `SKILL.md` | Instructions, workflow |
| `triggers[]` | Natural language phrases |
| Inputs/Outputs | What it needs, what it produces |

**Actions**: Trigger (in Work tab), Create (via Build)

**UI Representation**:
- Quick Actions in Work tab
- Skill execution flow
- Part of Work mode, not separate tab

---

### 4. WORKSPACE (`04-workspace/`)

**What**: Your files - organized like Google Drive/Dropbox (familiar pattern).

| Attribute | Description |
|-----------|-------------|
| Domain folders | Organized by your business domains |
| Build outputs | Deliverables from completed Builds |
| Knowledge | Research, templates, reference |

**Actions**: Browse, Search, Create, Organize

**UI Representation**:
- 📁 Workspace tab (fixed, singleton)
- Familiar folder/file browser
- Quick search (⌘+K)

---

## Tab Types as Objects (v2 NEW)

The UI is organized around **tabs**, which are the primary navigation:

### Fixed Tabs (Singletons)

| Tab | Object | Purpose |
|-----|--------|---------|
| 🗺️ Roadmap | Builds (overview) | Kanban board of all Builds |
| 📁 Workspace | Files | Browse and manage files |
| 📥 Inbox | Notifications | External inputs, alerts |

### Multiple Tabs (User-created)

| Tab | Object | Purpose |
|-----|--------|---------|
| 🔨 Build | Single Build | Work on one project |
| 💼 Work | Session | Execute skills, copilot |

---

## Object Relationships (v2)

```
MEMORY ──informs──▶ All (context for everything)

BUILD ──creates──▶ WORKSPACE outputs (deliverables)
BUILD ──uses──▶ SKILL (during Work phase)
BUILD ──reads──▶ WORKSPACE (reference materials)

SKILL ──executes-in──▶ WORK tab
SKILL ──reads/writes──▶ WORKSPACE (inputs/outputs)

ROADMAP ──contains──▶ BUILD cards (status overview)

WORK ──uses──▶ SKILL (quick actions)
WORK ──uses──▶ BUILD context (tasks from completed builds)
```

---

## UI Mapping (v2)

Each pillar maps to UI components:

```
+-------------------------------------------------------------------+
|  [NEXUS]  YOUR SYSTEM IS 45% BUILT       [🎤] [🔍] [⚙️] [?]       |
+-------------------------------------------------------------------+
|  FIXED TABS               │  MULTIPLE TABS                         |
|  [🗺️ Roadmap]             │  [🔨 ICP Build ×] [💼 Work ×] [+]      |
|  [📁 Workspace]           │                                        |
|  [📥 Inbox]               │                                        |
+-------------------------------------------------------------------+
|                                                                    |
|              (Active tab content)                                  |
|                                                                    |
|  MEMORY: Loaded as context (not a tab)                            |
|  SKILLS: Accessed via Work tab (not separate)                     |
|                                                                    |
+-------------------------------------------------------------------+
```

---

## Pillar → Tab Mapping

| Pillar | Primary UI | Access Pattern |
|--------|------------|----------------|
| **MEMORY** | Settings + Onboarding | Always loaded, edit via ⚙️ |
| **BUILD** | 🗺️ Roadmap + 🔨 Build tabs | Overview → Detail |
| **SKILL** | 💼 Work tab (Quick Actions) | Part of Work mode |
| **WORKSPACE** | 📁 Workspace tab | Always accessible |

---

## Four Pillars in Onboarding

During the 8-step onboarding, pillars are introduced progressively:

| Step | Pillar Introduced | What's Created |
|------|-------------------|----------------|
| 1-3 | MEMORY | goals.md, context.md |
| 4 | WORKSPACE | Folder structure |
| 5 | BUILD (overview) | Roadmap with items |
| 6-7 | BUILD (detail) | First Build (4 docs + outputs) |
| 8 | SKILL (via Work) | First Work session |

---

## Key Changes from v1

| Aspect | v1 | v2 |
|--------|----|----|
| Build structure | Planning → Execution | 4 documents (Overview, Discovery, Plan, Steps) |
| Skill access | Separate mode/tab | Via Work tab (Quick Actions) |
| Navigation | Mode switching | Tab-based (fixed + multiple) |
| Workspace | Domain folders | Familiar file browser (Google Drive pattern) |
| Lifecycle | Plan → Execute → Complete | PLANNING 🔵 → BUILDING 🟡 → DONE ✅ |

---

*OOUX Framework v2 - Updated 2026-01-13 for Build vs Work model*
