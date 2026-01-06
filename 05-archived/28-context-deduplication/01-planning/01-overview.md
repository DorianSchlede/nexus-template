---
id: 28-context-deduplication
name: Context Deduplication
status: COMPLETE
description: "Load when user mentions 'context duplication', 'token waste', 'duplicate files', 'nexus_data redundancy', or 'fix context loading'"
created: 2026-01-05
completed: 2026-01-05
archived: 2026-01-05
---

# Context Deduplication

## Purpose

Eliminate duplicate context injection in SessionStart hook that wastes ~12k+ tokens per session.

## Problem Analysis

**Current duplication sources:**

| Content | Source 1 | Source 2 | Waste |
|---------|----------|----------|-------|
| orchestrator.md | SessionStart (full) | nexus_data.orchestrator | ~4k tokens |
| workspace-map.md | SessionStart (full) | nexus_data.workspace_map | ~1k tokens |
| system-map.md | SessionStart (full) | nexus_data.system_map | ~1k tokens |
| memory-map.md | SessionStart (full) | nexus_data.memory_map | ~1k tokens |
| Project planning files | SessionStart (resume) | system-reminders (on modify) | ~6k tokens |

**Root causes:**
1. `nexus_data` JSON contains full file contents of maps AND SessionStart loads them again
2. Project files loaded for resume get re-injected via system-reminders when modified
3. No coordination between resume file loading and nexus_data bundle

---

## Success Criteria

**Must achieve**:
- [x] Eliminate duplicate orchestrator/map loading (choose ONE source)
- [x] Reduce nexus_data bundle size by removing redundant full-text fields
- [x] Total context savings: >10k tokens per session
- [x] No loss of functionality (routing, project resume, skill matching still work)

**Nice to have**:
- [x] Document which source handles which content type
- [ ] Add token estimation to nexus-loader output

---

## Context

**Background**: SessionStart hook loads full context via nexus-loader.py, which returns a JSON bundle containing full file contents. When resuming projects, additional files are loaded. System-reminders then re-inject files when they're modified, causing duplication.

**Stakeholders**: All Nexus users (context window efficiency)

**Constraints**:
- Must maintain backward compatibility with existing hooks
- Must not break resume/compact functionality
- Changes primarily in `nexus-loader.py` and `session_start.py`

---

## Timeline

**Target**: Complete in this session

**Milestones**:
- Phase 1: Analyze current context loading flow
- Phase 2: Design deduplicated architecture
- Phase 3: Implement changes
- Phase 4: Verify token savings

---

*Next: Fill in 02-discovery.md*
