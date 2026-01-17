---
id: 01-onboarding-redesign-contextual-micro-lessons
name: Onboarding Redesign - Contextual Micro-Lessons
status: COMPLETE
description: "Implement 'Teach Through Doing' onboarding via PostToolUse hook micro-lessons"
created: 2026-01-17
completed: 2026-01-17
build_path: 02-builds/01-onboarding-redesign-contextual-micro-lessons/
---

# Onboarding Redesign - Contextual Micro-Lessons

## Build Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

Replace the current onboarding approach (concept overload upfront) with contextual "micro-lessons" that teach users concepts at the moment they first encounter them.

**Core Philosophy (The Golden Rule):**
> *"Du willst halt die Leute machen einfach was... und nachdem es passiert ist, sagst du ihm, was gerade passiert ist"*
> Let users DO something, then explain what just happened.

---

## Success Criteria

**Must achieve**:
- [x] PostToolUse hook injects micro-lessons on first encounter with builds, skills, workspace, memory, close-session
- [x] Each micro-lesson shows only ONCE (tracked via user-config.yaml flags)
- [x] Anti-pattern detection warns when user creates repeated naming patterns (report-jan, task-1)
- [x] Lessons are 15 seconds max - quick tip then back to work
- [x] All existing hook functionality preserved (session_id injection, logging)

**Nice to have**:
- [ ] Integration lesson on first connect (deferred to future)
- [ ] Startup flow asks "What do you want to work on?" instead of showing menu (deferred to future)

---

## Context

**Background**:
Real onboarding session (Sascha-Dorian, 2+ hours) revealed critical pain points:
- User overwhelmed by Skills, Builds, Workspace, Memory concepts thrown at once
- Explaining before doing - user didn't understand concepts without context
- No tangible value after 2 hours of onboarding
- Quote: *"du gibst mir jetzt hier ganz viele Konzepte... führe mich mal bitte Stück für Stück durchs Onboarding"*

**Stakeholders**:
- New Nexus users (primary)
- Existing users who skipped onboarding

**Constraints**:
- Must use existing hook infrastructure (PostToolUse)
- Must not break existing post_tool_use.py functionality
- Must work with current user-config.yaml structure
- Lessons must be brief (15 seconds max reading time)

---

## Reference Document

Complete implementation details preserved in:
`02-resources/ONBOARDING-REDESIGN-COMPLETE-PLAN.md`

---

## Completion Summary

**Implemented**:
- 5 micro-lessons (build_created, skill_loaded, workspace_used, memory_updated, close_session_used)
- Anti-pattern detection for repeated naming patterns
- State persistence in user-config.yaml (first_encounters, anti_patterns_warned)
- JSON output format with additionalContext injection

**Files Modified**:
- `.claude/hooks/post_tool_use.py` - Added 280+ lines of micro-lesson logic
- `01-memory/user-config.yaml` - Added tracking sections
- `00-system/core/nexus/templates/user-config.yaml` - Added template sections
- `00-system/core/orchestrator.md` - Added contextual-teaching documentation

**All Tests Passed**: Triggers, anti-patterns, JSON format, flag persistence
