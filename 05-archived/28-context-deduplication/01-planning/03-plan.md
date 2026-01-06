# Context Deduplication - Plan

**Last Updated**: 2026-01-05

---

## Problem Analysis

**Current Flow (Duplicated):**

```
SessionStart Hook
├── RESUME PATH (project detected):
│   └── build_resume_file_content() loads:
│       ├── orchestrator.md (FULL)        ← DUPLICATE
│       ├── system-map.md (FULL)          ← DUPLICATE
│       ├── workspace-map.md (FULL)       ← DUPLICATE
│       ├── project files (FULL)
│       └── skill file (FULL)
│
└── ALWAYS:
    └── load_full_startup_context() loads:
        ├── user_goals (FULL)
        ├── user_projects (minimal metadata)
        ├── orchestrator (extracted essentials)  ← STILL HAS FULL RULES
        ├── skills (tiered metadata)
        ├── workspace_map (FULL)           ← DUPLICATE
        ├── memory_map (FULL)              ← DUPLICATE
        ├── system_map (FULL)              ← DUPLICATE
        ├── state (flags)
        └── stats (counts)
```

**Waste per resume session:** ~12k+ tokens

---

## Approach

**Strategy**: Split responsibilities clearly - ONE source per content type

| Content Type | Source | What to Load |
|--------------|--------|--------------|
| System behavior rules | `nexus_data` (abbreviated) | Routing table, core skill triggers, never_do list |
| Full map files | Resume context ONLY (when needed) | orchestrator, system-map, workspace-map |
| User identity | `nexus_data` | user_goals (full) |
| Project metadata | `nexus_data` | Minimal: id, name, status, progress, current_task |
| Skill routing | `nexus_data` | Name + description only |
| Active project files | Resume context | Full content (overview, plan, steps) |
| Active skill file | Resume context | Full SKILL.md |

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Maps source | nexus_data ONLY | Remove from resume path to prevent duplication |
| Orchestrator | ABBREVIATED in nexus_data | Routing rules yes, full prose no |
| Resume file loading | Keep for project files | These ARE needed, just not system files |
| nexus_data maps | REMOVE full text | Replace with "see orchestrator" pointer |

---

## Dependencies & Links

**Files Impacted**:
- `00-system/core/nexus/loaders.py` - `load_full_startup_context()` to slim maps
- `.claude/hooks/session_start.py` - `build_resume_file_content()` to skip system files

**Related Projects**:
- Project 25 (Research Pipeline) - Created resume context system

---

## Implementation Strategy

**Phase 1: Slim nexus_data bundle**
- Create `extract_essential_orchestrator()` - routing table, core skills, never_do only
- Remove `workspace_map`, `memory_map`, `system_map` full text
- Add pointers: "For full content: Read 04-workspace/workspace-map.md"

**Phase 2: Clean up resume path**
- Remove orchestrator.md loading from `build_resume_file_content()`
- Remove system-map.md loading
- Remove workspace-map.md loading
- Keep only: project files + skill file

**Phase 3: Verify token savings**
- Measure before/after with actual sessions
- Target: >10k tokens saved per resume session

---

## Open Questions

- [x] Should we keep memory_map in nexus_data? → YES, it's small and useful
- [x] What's the minimum orchestrator content needed? → Routing table + core skill triggers + never_do list

---

*Next: Break down execution in 04-steps.md*
