# Onboarding Redesign - Execution Steps

**Build Type**: Build
**Status**: Ready for Execution

---

## Context Requirements

**Build Location**: `02-builds/01-onboarding-redesign-contextual-micro-lessons/`

**Files to Load for Execution**:
- `01-planning/02-discovery.md` - Requirements
- `01-planning/03-plan.md` - Approach and decisions
- `ONBOARDING-REDESIGN-COMPLETE-PLAN.md` - Full implementation code

**Output Location**: Modified files in `.claude/hooks/`, `01-memory/`, `00-system/`

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Setup & Preparation

**Goal**: Verify environment and understand current state
**Context**: Load 02-discovery.md

- [ ] Read current `.claude/hooks/post_tool_use.py` to understand existing structure **[REQ-NF-2]**
- [ ] Read current `01-memory/user-config.yaml` to see existing sections **[REQ-1-6]**
- [ ] Read `00-system/core/nexus/templates/user-config.yaml` for template structure **[REQ-1-6]**
- [ ] **CHECKPOINT**: Confirm all files exist and are readable

---

## Phase 2: Core Implementation - PostToolUse Hook

**Goal**: Add micro-lesson detection and injection to post_tool_use.py
**Context**: Load 03-plan.md approach section, ONBOARDING-REDESIGN-COMPLETE-PLAN.md Section 4A

### 2.1 Add Micro-Lessons Configuration **[REQ-1 through REQ-5]**

- [ ] Add `MICRO_LESSONS` dictionary with all 5 lessons:
  - `build_created` - trigger on Write to `02-builds/*/01-planning/*`
  - `skill_loaded` - trigger on Read of `SKILL.md` in skills folders
  - `workspace_used` - trigger on Write to `04-workspace/*`
  - `memory_updated` - trigger on Write to `01-memory/goals.md` or `core-learnings.md`
  - `close_session_used` - trigger on Read of `close-session/SKILL.md`
- [ ] Add each lesson's content (box-drawn format, 6 lines max)

### 2.2 Add Anti-Pattern Detection **[REQ-6]**

- [ ] Add `ANTI_PATTERNS` dictionary with:
  - `repeated_build_pattern` - regex for `-\d+$`, month names, week patterns, version numbers
  - Warning message template with `{name}` placeholder

### 2.3 Add State Management Functions **[Property 2, Property 4]**

- [ ] Add `get_first_encounters(config_path)` - read flags from user-config.yaml using regex
- [ ] Add `get_anti_patterns_warned(config_path)` - read warning flags using regex
- [ ] Add `update_config_flag(config_path, section, flag, value)` - update YAML with regex

### 2.4 Add Detection Functions **[REQ-1 through REQ-6]**

- [ ] Add `check_micro_lesson(tool_name, tool_input, config_path)` - returns lesson or None
- [ ] Add `check_anti_pattern(tool_name, tool_input, config_path)` - returns warning or None

### 2.5 Update main() Function **[All REQs]**

- [ ] After existing session_id and logging logic, add:
  - Get config_path as `Path('01-memory/user-config.yaml')`
  - Call `check_micro_lesson()`, if result, output JSON and exit
  - Call `check_anti_pattern()`, if result, output JSON and exit
  - Exit cleanly if no lesson/warning

- [ ] **CHECKPOINT**: Hook code complete, verify syntax with `python -m py_compile`

---

## Phase 3: Configuration Updates

**Goal**: Add required sections to user-config.yaml files
**Context**: Template structure from discovery

### 3.1 Update User Config Template **[REQ-1 through REQ-6]**

- [ ] Add to `00-system/core/nexus/templates/user-config.yaml`:
```yaml
first_encounters:
  build_created: false
  skill_loaded: false
  workspace_used: false
  memory_updated: false
  close_session_used: false

anti_patterns_warned:
  repeated_build_pattern: false
```

### 3.2 Update Current User Config **[REQ-1 through REQ-6]**

- [ ] Add same sections to `01-memory/user-config.yaml`
- [ ] **CHECKPOINT**: Both config files have new sections

---

## Phase 4: Documentation Update

**Goal**: Document how contextual teaching works
**Context**: Orchestrator section from plan

### 4.1 Update Orchestrator **[Documentation]**

- [ ] Add `<section id="contextual-teaching">` to `00-system/core/orchestrator.md`
- [ ] Include: How it works, when lessons appear, Claude's role, anti-pattern detection table

---

## Phase 5: Validation

**Goal**: Verify against requirements and properties
**Context**: Implementation complete

### 5.1 Syntax Validation **[REQ-NF-2]**

- [ ] Run `python -m py_compile .claude/hooks/post_tool_use.py`
- [ ] Verify no syntax errors

### 5.2 Unit Test Triggers **[REQ-1 through REQ-6]**

- [ ] Test build_created trigger matches `02-builds/01-test/01-planning/overview.md`
- [ ] Test skill_loaded trigger matches `00-system/skills/builds/plan-build/SKILL.md`
- [ ] Test workspace_used trigger matches `04-workspace/notes/test.md`
- [ ] Test memory_updated trigger matches `01-memory/goals.md`
- [ ] Test close_session_used trigger matches `00-system/skills/system/close-session/SKILL.md`
- [ ] Test anti-pattern matches `02-builds/01-report-january/overview.md`
- [ ] Test anti-pattern does NOT match `02-builds/01-career-plan/overview.md`

### 5.3 Integration Test **[Property 1, Property 2]**

- [ ] Create test build, verify lesson output in stdout
- [ ] Check user-config.yaml, verify flag set to true
- [ ] Create second build, verify NO lesson output
- [ ] **CHECKPOINT**: All tests pass

---

## Phase 6: Finalization

**Goal**: Complete build and update state
**Context**: All validation passed

- [ ] Update `resume-context.md`: current_phase: "complete"
- [ ] Update `01-overview.md` success criteria checkboxes
- [ ] Move `ONBOARDING-REDESIGN-COMPLETE-PLAN.md` to `02-resources/` (reference material)

---

## Summary

| Phase | Tasks | Optional | Checkpoints |
|-------|-------|----------|-------------|
| Phase 1 | 4 | 0 | 1 |
| Phase 2 | 7 | 0 | 1 |
| Phase 3 | 3 | 0 | 1 |
| Phase 4 | 2 | 0 | 0 |
| Phase 5 | 10 | 0 | 1 |
| Phase 6 | 3 | 0 | 0 |
| **Total** | **29** | **0** | **4** |

---

## Quick Reference: Micro-Lesson Triggers

| Lesson ID | Tool | Path Pattern | Shows Once |
|-----------|------|--------------|------------|
| build_created | Write | `02-builds/*/01-planning/*` | Yes |
| skill_loaded | Read | `*/SKILL.md` in skills | Yes |
| workspace_used | Write | `04-workspace/*` | Yes |
| memory_updated | Write | `01-memory/goals.md` or `core-learnings.md` | Yes |
| close_session_used | Read | `close-session/SKILL.md` | Yes |
| repeated_build_pattern | Write | `02-builds/XX-{pattern}/` | Yes (warning) |

---

*Mark tasks complete with [x] as you finish them*
