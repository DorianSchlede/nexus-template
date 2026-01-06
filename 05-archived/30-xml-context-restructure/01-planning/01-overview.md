---
id: 30-xml-context-restructure
name: XML Context Restructure
status: IN_PROGRESS
description: "Load when user mentions 'XML context', 'context injection', 'SessionStart hook', 'startup context', 'compact context', or 'context structure'"
created: 2026-01-05
---

# XML Context Restructure

## Purpose

Replace JSON/markdown context injection with semantic XML structure for Claude Code operating inside the NEXUS system. This is the HYPER IMPORTANT primary working mode that controls ALL routing, skill loading, and project management.

**Problem**: Current context injection uses a mix of JSON and markdown that:
- Duplicates content between startup and compact modes
- Lacks clear semantic structure for AI parsing
- Has inconsistent routing priority
- Doesn't properly guide AI toward project-first workflow

**Solution**: Unified XML context structure with:
- Clear semantic tags for each context section
- Separate modes: STARTUP (fresh) vs COMPACT (project resume)
- Dynamic skill loading triggers
- Project-first workflow enforcement

---

## Success Criteria

**Must achieve**:
- [ ] XML structure defined for STARTUP mode (fresh sessions)
- [ ] XML structure defined for COMPACT mode (project continuation)
- [ ] Transcript parsing to detect project work in previous session
- [ ] Dynamic skill section construction from filesystem
- [ ] Core routing with project-first priority
- [ ] Auto-load skill files when suggesting plan-project/execute-project
- [ ] Implementation in session_start.py and loaders.py
- [ ] Zero duplication between modes

**Nice to have**:
- [ ] Token count estimation in output
- [ ] Validation of XML structure integrity

---

## Context

**Background**:
- SessionStart hook injects context via additionalContext field
- Current system uses JSON (nexus_data) + markdown (file contents)
- Compact/resume sessions duplicate content from startup
- ~10-12K tokens wasted per session on duplication

**Stakeholders**:
- All Nexus users (better AI behavior, less confusion)
- System maintainers (clearer structure to modify)

**Constraints**:
- Must work within Claude Code hook system
- additionalContext is a string field (XML works fine)
- Must maintain backward compatibility during transition
- Performance: hook must complete in <200ms

---

## Timeline

**Target**: Complete in 1-2 sessions

**Milestones**:
- Phase 1: Complete XML design specification
- Phase 2: Implement STARTUP mode
- Phase 3: Implement COMPACT mode with transcript detection
- Phase 4: Testing and validation

---

*Next: See 03-plan.md for complete XML specification*
