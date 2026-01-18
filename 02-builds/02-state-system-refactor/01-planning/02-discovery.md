# State System Refactor - Discovery

**Build Type**: Build
**Purpose**: Clean up chaotic state detection logic, establish single source of truth

---

## Problem Statement

The onboarding state detection is broken and spread across multiple files with conflicting logic:

1. **Menu shows wrong state** - "✓ Organized" when `create_folders: false`
2. **Multiple detection methods** - Template checks vs learning_tracker
3. **Logic distributed** across 4+ files with no clear ownership

---

## Requirements (EARS Format)

### Functional Requirements

**REQ-1**: THE state detection system SHALL derive all onboarding completion state from `learning_tracker.completed` in `01-memory/user-config.yaml`.

**REQ-2**: WHEN displaying folder status in menu, THE system SHALL show "✓ Organized" only IF `learning_tracker.completed.create_folders` equals `true`.

**REQ-3**: THE system SHALL NOT use `is_template_file()` to determine onboarding skill completion state.

**REQ-4**: WHEN the `create-folders` skill completes, THE skill SHALL set `learning_tracker.completed.create_folders` to `true` in user-config.yaml.

**REQ-5**: THE system SHALL use consistent naming: `create_folders` (underscore) for config keys, `create-folders` (hyphen) for skill/folder names.

### Non-Functional Requirements

**REQ-NF-1**: THE state detection code SHALL exist in a single file (`state.py`) with no duplication in other modules.

**REQ-NF-2**: THE state detection SHALL complete within 50ms to not impact hook performance.

### Quality Checklist (INCOSE)

- [x] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [x] No vague terms (quickly, adequate, reasonable, user-friendly)
- [x] No pronouns (it, them, they) - specific names used
- [x] Each requirement independently testable
- [x] Active voice throughout
- [x] No escape clauses (where possible, if feasible)
- [x] Solution-free (what, not how)

---

## Dependencies

### Files to Modify

| File | Changes Needed |
|------|----------------|
| `00-system/core/nexus/state.py` | Remove `check_workspace_configured()`, `check_goals_personalized()` - use learning_tracker instead |
| `.claude/hooks/session_start.py` | Simplify state detection to use only learning_tracker |
| `00-system/core/nexus/loaders.py` | Update `_template_onboarding_incomplete()` to use learning_tracker |
| `00-system/skills/learning/create-folders/SKILL.md` | Ensure skill sets learning_tracker on completion |

### Files to Create

None - this is a refactor, not new functionality.

### External Systems

None - purely internal state management.

---

## Existing Patterns

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| `extract_learning_completed()` | state.py:360-398 | This is correct - expand usage |
| `build_pending_onboarding()` | state.py:335-356 | Keep as-is, it already uses learning_tracker |
| YAML parsing | utils.py | Reuse existing parsers |

---

## Current Code Analysis

### state.py - What to Change

```python
# DELETE these functions (lines 434-458):
def check_workspace_configured(base_path: Path) -> bool:
    """Uses is_template_file() - WRONG approach"""

def check_goals_personalized(goals_path: Path) -> bool:
    """Uses is_template_file() - WRONG approach"""

# KEEP and expand usage of:
def extract_learning_completed(config_path: Path) -> Dict[str, bool]:
    """Reads user-config.yaml - CORRECT approach"""
```

### session_start.py - What to Change

Lines 552-567 currently do:
```python
goals_is_template = is_template_file(str(goals_path))
goals_personalized = check_goals_personalized(goals_path)

workspace_is_template = is_template_file(str(workspace_map_path))
workspace_configured = check_workspace_configured(base_path)
```

**Change to:**
```python
learning_completed = extract_learning_completed(config_path)

goals_personalized = learning_completed.get("setup_memory", False)
workspace_configured = learning_completed.get("create_folders", False)

# Keep is_template checks for VALIDATION LOGGING ONLY
goals_is_template = is_template_file(str(goals_path))
workspace_is_template = is_template_file(str(workspace_map_path))
```

### loaders.py - What to Change

`_template_onboarding_incomplete()` at ~line 1376 uses `context.get("workspace_configured")`.
This already works IF session_start.py sets it correctly from learning_tracker.

**No change needed** - loaders.py consumes state, doesn't produce it.

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Existing users have old config without create_folders key | High | Low | extract_learning_completed() already has defaults |
| Skills not setting learning_tracker on completion | Medium | High | Audit all onboarding skills, add update step |
| Template detection still needed for first-run detection | Low | Low | Keep is_template_file() but only for initial file creation |

### Open Questions

- [x] Is the issue stale session context or actual bug? → Both. The rename fixed config, but logic is still messy.
- [x] Should we remove is_template_file() entirely? → No, keep for validation/logging, not for state.

---

## Mental Model Applied: First Principles

**What is the fundamental truth here?**
- A skill is "complete" when the user has done it
- The only reliable record of "user did X" is an explicit flag set by the skill
- File existence/content is unreliable (user might manually edit, templates copied, etc.)

**Therefore:**
- `learning_tracker.completed.{skill}` is the ONLY valid source
- All other detection methods are heuristics at best, bugs at worst

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
