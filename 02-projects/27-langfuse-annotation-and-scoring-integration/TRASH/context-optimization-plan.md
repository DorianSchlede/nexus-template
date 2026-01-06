# Context Optimization Plan: Resume State

**Date**: 2026-01-05
**Purpose**: Optimize `session_start.py` to avoid redundant context loading during resume/compact

---

## Problem Statement

When resuming a project, the current hook loads **BOTH**:
1. **Project files** via `auto_load_project_files()` - ~15-20K tokens
   - 4 project files (overview, discovery, plan, steps)
   - 1 skill file (plan-project or execute-project SKILL.md)

2. **nexus_data JSON blob** via `load_full_startup_context()` - ~8-12K tokens
   - user_goals
   - user_projects
   - orchestrator (rules)
   - skills (tiered)
   - stats
   - state

**Result**: ~25-30K tokens of context, with significant duplication.

---

## Desired Behavior

### For `source=resume` or `source=compact` WITH active project:

**KEEP** (project-specific context):
- All 4 project files (overview.md, discovery.md, plan.md, steps.md)
- Skill file (SKILL.md for plan-project or execute-project)
- Resume header with phase detection

**REMOVE** (redundant):
- Full `nexus_data` JSON blob

**ADD** (minimal routing only):
- Compact routing reminder (50 tokens)
- Skill priority reminder

### For `source=startup` or `source=clear`:

**KEEP** (full startup context):
- Full `nexus_data` JSON blob
- Display menu instruction

---

## Implementation Plan

### File: `.claude/hooks/session_start.py`

#### Change 1: Conditional nexus_data loading (lines ~791-808)

**Current** (always loads):
```python
# 5. Load full MVC context (optimized)
try:
    nexus_core = Path(project_dir) / "00-system" / "core"
    # ... load full_context
    context["nexus_data"] = full_context
except Exception as e:
    # ... fallback
```

**Proposed** (conditional):
```python
# 5. Load full MVC context - SKIP for resume with project loaded
skip_nexus_data = should_resume and resume_instructions is not None

if skip_nexus_data:
    logging.info("Skipping nexus_data for resume (project context already loaded)")
    context["nexus_data"] = {
        "skipped": True,
        "reason": "project_context_loaded",
        "routing_reminder": "skill → integration → project → natural",
        "skill_priority": "00-system/skills/ > 03-skills/"
    }
else:
    # ... existing full load
```

#### Change 2: Update logging (line ~861)

Add token savings estimate to log:
```python
f.write(f"Nexus Data: {'Skipped (project context loaded)' if skip_nexus_data else 'Full'}\n")
```

---

## Token Budget Analysis

### Before Optimization (resume with project):

| Component | Tokens |
|-----------|--------|
| Resume header | ~200 |
| Project files (4) | ~12,000 |
| Skill file | ~3,000 |
| nexus_data JSON | ~10,000 |
| **Total** | **~25,000** |

### After Optimization (resume with project):

| Component | Tokens |
|-----------|--------|
| Resume header | ~200 |
| Project files (4) | ~12,000 |
| Skill file | ~3,000 |
| Routing reminder | ~50 |
| **Total** | **~15,250** |

**Savings**: ~10,000 tokens per resume session (40% reduction)

---

## Validation Checklist

- [ ] Resume with active project: nexus_data skipped
- [ ] Startup fresh: nexus_data loaded (full menu)
- [ ] Clear command: nexus_data loaded (full menu)
- [ ] Resume without project: nexus_data loaded (fallback)
- [ ] Compact with project: nexus_data skipped
- [ ] Token savings visible in log

---

## Rollback Plan

If issues arise:
1. Comment out the conditional check
2. Always load full nexus_data
3. Document the issue for investigation

---

## Related Files

- `.claude/hooks/session_start.py` - Main hook to modify
- `00-system/core/nexus/loaders.py` - `load_full_startup_context()` function
- `00-system/.cache/session_start_tokens.txt` - Token analysis output

---

*This plan optimizes resume context to ~15K tokens while maintaining full startup capability.*
