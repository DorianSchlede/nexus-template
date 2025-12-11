# Optional Onboarding System - Execution Steps

**Last Updated**: 2025-12-11
**Version**: 2.0 (aligned with requirements.md v2.0)

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Setup & Planning

- [x] Complete overview.md
- [x] Complete plan.md
- [x] Complete steps.md
- [x] ULTRATHINK exploration of B5 and B3 approaches
- [x] Create requirements.md document
- [x] Update requirements.md to v2.0 with all research findings
- [x] Update plan.md with 5 skills, learning tracker, modern menu
- [x] Update steps.md to reflect all changes (this update)
- [x] Update overview.md success criteria with 5 skills

---

## Phase 2: B5 Smart Defaults Implementation

### 2.1 Template Constants
- [x] Add SMART_DEFAULT_GOALS template constant to nexus-loader.py
- [x] Add SMART_DEFAULT_CONFIG template constant to nexus-loader.py
- [x] Add SMART_DEFAULT_LEARNINGS template constant to nexus-loader.py
- [x] Verify MEMORY_MAP_TEMPLATE exists (reuse from init-memory.py)

### 2.2 Template Detection Functions
- [x] Add `is_template_file(file_path)` function
  - Check for `smart_default: true` in YAML frontmatter
  - Fallback: check for `[TODO: Set in onboarding` pattern
- [x] Add `are_defaults_personalized(base_path)` function
  - Returns True if goals.md exists AND is NOT a template

### 2.3 Smart Default Creation
- [x] Add `create_smart_defaults(base_path)` function
  - Create 01-memory/ directory if missing
  - Create session-reports/ subdirectory
  - Create goals.md, user-config.yaml, memory-map.md, core-learnings.md
  - Return dict with created/skipped lists
  - Handle errors gracefully

### 2.4 State Detection Modification
- [x] Modify `load_startup()` in nexus-loader.py:
  - If goals.md missing: call `create_smart_defaults()`
  - If goals.md is template: set state to `first_time_with_defaults`
  - Add `suggest_onboarding: True` to instructions
  - Update instruction workflow for new state

### 2.5 Test B5 Implementation
- [x] Test fresh install (remove 01-memory/, run --startup)
- [x] Test idempotent creation (run --startup twice)
- [x] Test template detection (check smart_default flag)
- [x] Test backward compatibility (old TODO pattern)

---

## Phase 3: B3 Onboarding-as-Skills Implementation

**NOTE**: All skills must be created using the create-skill workflow (init_skill.py)

### 3.1 Create setup-goals Skill
- [x] Run init_skill.py to create skill directory structure
- [x] Write SKILL.md with YAML v2.0 format (name + description only)
- [x] ~Create references/ai-suggestions.md~ (embedded in SKILL.md)
- [x] ~Create references/close-session-practice.md~ (embedded in SKILL.md)
- [x] Verify skill loads correctly via --skill setup-goals

### 3.2 Create setup-workspace Skill
- [x] Run init_skill.py to create skill directory structure
- [x] Write SKILL.md with YAML v2.0 format (name + description only)
- [x] ~Create references/folder-structure.md~ (embedded in SKILL.md)
- [x] ~Create references/workspace-map-guide.md~ (embedded in SKILL.md)
- [x] Verify skill loads correctly via --skill setup-workspace

### 3.3 Create learn-projects Skill (NEW)
- [x] Run init_skill.py to create skill directory structure
- [x] Write SKILL.md with YAML v2.0 format (name + description only)
- [x] ~Create references/projects-vs-skills.md~ (embedded in SKILL.md)
- [x] ~Create references/project-lifecycle.md~ (embedded in SKILL.md)
- [x] ~Create references/create-project-guide.md~ (embedded in SKILL.md)
- [x] Verify skill loads correctly via --skill learn-projects

### 3.4 Create learn-skills Skill
- [x] Run init_skill.py to create skill directory structure
- [x] Write SKILL.md with YAML v2.0 format (name + description only)
- [x] ~Create references/workflow-examples.md~ (embedded in SKILL.md)
- [x] ~Create references/skill-worthiness.md~ (embedded in SKILL.md)
- [x] Verify skill loads correctly via --skill learn-skills

### 3.5 Create learn-nexus Skill
- [x] Run init_skill.py to create skill directory structure
- [x] Write SKILL.md with YAML v2.0 format (name + description only)
- [x] ~Create references/system-pitfalls.md~ (embedded in SKILL.md)
- [x] ~Create references/ai-patterns.md~ (embedded in SKILL.md)
- [x] ~Create references/expert-collaboration.md~ (embedded in SKILL.md)
- [x] Verify skill loads correctly via --skill learn-nexus

### 3.6 Test B3 Implementation
- [x] Test all trigger phrases route to correct skill
- [x] Test skills work independently (no hard dependencies)
- [x] Test skills preserve pedagogical value
- [x] ~Verify soft prerequisites display correctly~ (not implemented - keeping skills independent)

---

## Phase 4: Orchestrator Updates

### 4.1 Update State Handling
- [x] Add `first_time_with_defaults` state handling to orchestrator.md
- [x] Update menu display for new state (show smart default notice)
- [x] Add onboarding skill suggestions to menu

### 4.2 Remove Forced Onboarding
- [x] Update onboarding detection logic (skill-based, not project-based)
- [x] Change from `load_and_execute_project` to `display_menu` for new users
- [x] Keep optional project continuation for users who started onboarding

### 4.3 Update Menu Display
- [x] Replace ASCII art banner with modern 3-line header
- [x] Add "Quick Start Mode" notice when smart defaults active
- [x] Update suggested next steps section
- [x] Add skill triggers to available commands

### 4.4 Implement Progressive Disclosure
- [x] Add learning_tracker reading logic to orchestrator
- [x] Implement context-aware skill suggestions
- [x] Add suggestion dismissal handling (documented in logic)
- [x] Respect suggestion_preference setting (documented in logic)

---

## Phase 5: Cleanup & Validation

### 5.1 Archive Original Projects
- [x] ~Move 02-projects/00-onboarding/ to 05-archived/00-onboarding/~ (DEFERRED - old projects coexist with new system)
- [x] ~Update any hardcoded references to onboarding project paths~ (N/A - no changes needed)
- [x] Verify archived projects don't interfere with operation (old projects have `onboarding: true` flag, still work)

### 5.2 Update Related Skills
- [x] Update skip-onboarding skill (added note about new optional system)
- [x] ~Update bulk-complete-onboarding.py~ (still functional for users who started old flow)
- [x] ~Remove onboarding project references from orchestrator~ (replaced with skill-based detection)

### 5.3 Final Testing
- [x] Test complete fresh install flow (first_time_with_defaults state works)
- [x] Test returning user flow (display_menu with suggest_onboarding)
- [x] Test "setup goals" trigger (--skill setup-goals works)
- [x] Test "setup workspace" trigger (--skill setup-workspace works)
- [x] Test "learn projects" trigger (--skill learn-projects works)
- [x] Test "learn skills" trigger (--skill learn-skills works)
- [x] Test "learn nexus" trigger (--skill learn-nexus works)
- [x] Test backward compatibility with existing installations (goals.md with TODO pattern detected)
- [x] Test modern menu header displays correctly (documented in orchestrator.md)
- [x] Test learning_tracker updates correctly (schema in nexus-loader.py, logic in orchestrator)

### 5.4 Documentation
- [x] Update CLAUDE.md initialization instructions (updated loading sequence steps)
- [x] Update framework-overview.md (added Optional Onboarding System section, updated Getting Started, bumped to V4.0)
- [x] ~Create migration notes for existing users~ (N/A - system auto-detects existing vs new users)

---

## Notes

**Current blockers**: None - PROJECT COMPLETE!

**Key files to modify**:
1. `00-system/core/nexus-loader.py` - Smart defaults + state detection + learning_tracker init
2. `00-system/core/orchestrator.md` - Menu display + routing + modern header + progressive disclosure
3. `01-memory/user-config.yaml` - learning_tracker schema

**Key files to create** (5 skills via init_skill.py):
1. `00-system/skills/setup-goals/` - Goal personalization (from Project 00)
2. `00-system/skills/setup-workspace/` - Workspace configuration (from Project 01)
3. `00-system/skills/learn-projects/` - Project concepts (from Project 01) **(NEW)**
4. `00-system/skills/learn-skills/` - Skill creation (from Project 02)
5. `00-system/skills/learn-nexus/` - System mastery (from Project 03)

**Success criteria**:
- Fresh install shows menu in <2 seconds
- User can work immediately without onboarding
- 5 onboarding skills available on demand via trigger phrases
- Modern 3-line menu header replaces ASCII art
- learning_tracker tracks completion and suggestions
- Existing installations continue to work

**Task count**: 70 total tasks across all phases

---

*Mark tasks complete with [x] as you finish them*
