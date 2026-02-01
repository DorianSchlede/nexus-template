================================================================================
MANDATORY: BUILD EXECUTION CONTINUATION
================================================================================

Build: {build_id}
Phase: EXECUTION (Phase 1 complete, implementing)

STEP 1 - MANDATORY: Initialize TodoWrite
- Read 04-steps.md for current execution phase
- Find first unchecked [ ] task
- Create todo list with remaining tasks
- Mark current task as in_progress

STEP 2 - MANDATORY: Follow execute-build skill
- Work on ONE task at a time
- Mark [x] complete immediately when done
- Move to next unchecked task

STEP 3 - MANDATORY: Track progress
- Update 04-steps.md checkboxes as you complete
- Update resume-context.md Progress Summary after significant progress

STEP 4 - CRITICAL: Before ending session, update Progress Summary
Format for resume-context.md Progress Summary:
```
### Latest Session (YYYY-MM-DD)

**Completed this session:**
- [x] Task description

**Key decisions:**
- Decision and why

**Next steps:**
1. Next task
```

Fields auto-synced by hooks: session_ids, last_updated, tasks_completed, current_section
Fields YOU must update: files_to_load (add working files), Progress Summary

================================================================================
Current task: {current_task}
DO NOT display menu. START on this task immediately.
================================================================================
