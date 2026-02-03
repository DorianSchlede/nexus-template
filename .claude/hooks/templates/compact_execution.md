================================================================================
MANDATORY: BUILD EXECUTION CONTINUATION
================================================================================

Build: {build_id}
Phase: Execution (planning done, now implementing)

NOTE: "Phase" here is workflow stage, NOT the build "status" field.
Valid status values: PLANNING, IN_PROGRESS, ACTIVE, COMPLETE, ARCHIVED
Do NOT write "EXECUTION" to the status field.

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

STEP 4 - CRITICAL: Before ending session
1. Update `continue_at` with specific pointer (e.g., "api.py:142")
2. Add any `blockers`
3. Write decisions to files → Add to `files_to_load`
   - Made decision? → Write to `02-resources/decisions.md` → Add to list
   - Found gotcha? → Write to `03-working/session-notes.md` → Add to list
4. Update "Context for Next Agent" prose to POINT to files

Fields auto-synced by hooks: session_ids, last_updated, tasks_completed, current_section
Fields YOU must update: continue_at, blockers, files_to_load (with # reason comments)

> Philosophy: Don't capture context in prose. Write to FILES, add to files_to_load.

================================================================================
Current task: {current_task}
DO NOT display menu. START on this task immediately.
================================================================================
