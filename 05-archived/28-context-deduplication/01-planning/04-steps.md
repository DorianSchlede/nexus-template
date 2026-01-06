# Context Deduplication - Execution Steps

**Last Updated**: 2026-01-05

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Planning

- [x] Complete 01-overview.md
- [x] Complete 03-plan.md
- [x] Complete 04-steps.md

---

## Phase 2: Slim nexus_data bundle

- [x] Check existing `extract_essential_orchestrator()` in loaders.py
- [x] Modify to return ONLY: routing table, core skill triggers, never_do list
- [x] Remove `workspace_map` full text from `load_full_startup_context()`
- [x] Remove `memory_map` full text from `load_full_startup_context()`
- [x] Remove `system_map` full text from `load_full_startup_context()`

---

## Phase 3: Clean up resume path

- [x] Modify `build_resume_file_content()` in session_start.py
- [x] Remove orchestrator.md loading (lines 358-370)
- [x] Remove system-map.md loading (lines 372-384)
- [x] Remove workspace-map.md loading (lines 386-398)
- [x] Keep project files + skill file loading
- [x] Update file count in header

---

## Phase 4: Testing & Verification

- [x] Test startup (non-resume) session
- [x] Test resume session
- [x] Test compact session
- [x] Verify all routing still works
- [x] Measure token savings

---

## Notes

**Target**: >10k tokens saved per resume session

---

*Mark tasks complete with [x] as you finish them*
