---
id: 01-optional-onboarding-system
name: Optional Onboarding System
status: COMPLETE
description: "Load when user mentions 'onboarding redesign', 'optional onboarding', 'smart defaults', 'B5 implementation', or 'onboarding to skills'"
created: 2025-12-10
completed: 2025-12-11
---

# Optional Onboarding System

## Purpose

Transform Nexus from forced 4-project onboarding to an optional, skill-based system that lets users start working immediately while preserving pedagogical value.

**Core Changes**:
1. **B5: Smart Defaults** - Auto-create minimal template files on first run so system works immediately
2. **B3: Onboarding-as-Skills** - Convert 4 forced projects to **5** optional skills users can trigger anytime
3. **Progressive Disclosure** - Intelligently suggest skills when contextually appropriate
4. **Modern Menu Design** - Replace ASCII art banner with clean, professional header

**Problem Solved**: New users currently must complete 35-50 minute onboarding before doing ANY work. This creates friction and drop-off for power users who know what they want.

---

## Success Criteria

**Must achieve**:
- [x] Fresh Nexus install shows menu on first run (NOT forced onboarding)
- [x] Smart defaults auto-created: goals.md, user-config.yaml, memory-map.md, core-learnings.md
- [x] Template detection works (smart_default: true flag)
- [x] 5 new skills created: setup-goals, setup-workspace, learn-projects, learn-skills, learn-nexus
- [x] Skills trigger via natural language ("setup goals", "learn projects", "learn skills", etc.)
- [x] All skills created via create-skill workflow (init_skill.py)
- [x] YAML v2.0 format used (name + description only)
- [x] Existing pedagogical content preserved in skill format
- [x] System works with zero personalization (degraded but functional)
- [x] Backward compatible with existing installations
- [x] Modern 3-line menu header replaces ASCII art banner

**Nice to have**:
- [x] Soft contextual prompts ("Notice your goals aren't set. Want help?") - via suggest_onboarding flag
- [x] Progress tracking via learning_tracker in user-config.yaml - schema implemented
- [ ] Express mode that runs essential setup quickly - DEFERRED
- [x] Suggestion frequency control (off/minimal/normal/proactive) - via suggestion_preference

---

## Context

**Background**:
- Current system has 4 onboarding projects (00-define-goals, 01-first-project, 02-first-skill, 03-system-mastery)
- nexus-loader.py forces Project 00 when goals.md doesn't exist
- skip-onboarding skill exists but requires validation gates
- Total onboarding time: 35-50 minutes

**Stakeholders**:
- New users (want guidance)
- Power users (want to skip and work immediately)
- System maintainers (want clean architecture)

**Constraints**:
- Must preserve CAVE pedagogical framework
- Must maintain close-session habit teaching
- Must not break existing installations
- Skills must work independently (soft dependencies only)

---

## Timeline

**Target**: Complete implementation in this session

**Milestones**:
1. B5 Smart Defaults implementation - Phase 1
2. B3 Skills conversion - Phase 2
3. Orchestrator updates - Phase 3
4. Testing & validation - Phase 4

---

## Implementation Summary

### B5: Smart Defaults

**Key Changes to nexus-loader.py**:
- Add `create_smart_defaults()` function
- Add `is_template_file()` detection (checks `smart_default: true`)
- Add `are_defaults_personalized()` check
- New state: `first_time_with_defaults` → shows menu, suggests onboarding
- Auto-create template files on first run

**Template Files**:
- goals.md (with `smart_default: true` flag)
- user-config.yaml (with defaults: English, onboarding: skipped)
- memory-map.md (static documentation)
- core-learnings.md (empty starter)

### B3: Onboarding-as-Skills

**5 New Skills** (all created via create-skill workflow):
| Skill | Triggers | Duration | Source |
|-------|----------|----------|--------|
| setup-goals | "setup goals", "define goals", "personalize nexus" | 8-10 min | Project 00 |
| setup-workspace | "setup workspace", "configure workspace" | 10-14 min | Project 01 (structure) |
| learn-projects | "learn projects", "understand projects", "project tutorial" | 8-10 min | Project 01 (concepts) |
| learn-skills | "learn skills", "skill tutorial", "create skill help" | 12-15 min | Project 02 |
| learn-nexus | "learn nexus", "system mastery", "AI collaboration" | 16-18 min | Project 03 |

**Skill Structure**:
```
00-system/skills/[skill-name]/
├── SKILL.md (YAML v2.0: name + description only)
└── references/ (teaching content)
```

### Progressive Disclosure

**Learning Tracker** (in user-config.yaml):
- Tracks skill completion, dismissals, last_suggested
- Configurable suggestion_preference (off/minimal/normal/proactive)
- Enables context-aware skill suggestions

**WHO updates WHAT**:
- nexus-loader.py → session_count
- Each skill → completed[skill]
- Orchestrator → dismissed, last_suggested
- close-session → workflow_patterns, common_mistakes

---

*See requirements.md for complete specification and steps.md for execution tasks*
