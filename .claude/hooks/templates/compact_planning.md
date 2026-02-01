================================================================================
MANDATORY: BUILD PLANNING CONTINUATION
================================================================================

Build: {build_id}
Phase: PLANNING (Phase 1 incomplete)

STEP 1 - MANDATORY: Initialize TodoWrite
- Read 04-steps.md Phase 1 tasks
- Create todo list with all unchecked planning tasks
- Mark first unchecked task as in_progress

STEP 2 - MANDATORY: Follow plan-build skill
- Complete planning documents: overview → discovery → plan → steps
- Use mental models for key decisions (suggest if appropriate)
- Pause for user confirmation at each document

STEP 3 - MANDATORY: Update progress
- Mark tasks [x] as completed in 04-steps.md
- Update resume-context.md Progress Summary with planning accomplishments

STEP 4 - CRITICAL: Before ending session, update Progress Summary
Format for resume-context.md Progress Summary:
```
### Latest Session (YYYY-MM-DD)

**Completed this session:**
- [x] Completed 02-discovery.md

**Key decisions:**
- Approach chosen and why

**Next steps:**
1. Complete 03-plan.md
```

Fields auto-synced by hooks: session_ids, last_updated, total_tasks, current_phase
Fields YOU must update: files_to_load, Progress Summary

================================================================================
Current task: {current_task}
DO NOT start implementation until ALL Phase 1 tasks are [x] complete.
DO NOT display menu. START on current planning task immediately.
================================================================================
