================================================================================
MANDATORY: BUILD PLANNING CONTINUATION
================================================================================

Build: {build_id}
Phase: Planning (discovery/design incomplete)

NOTE: "Phase" is workflow stage. Build status field uses: PLANNING, IN_PROGRESS, ACTIVE, COMPLETE, ARCHIVED

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

STEP 4 - CRITICAL: Before ending session
1. Update `continue_at` with specific pointer (e.g., "02-discovery.md Q3")
2. Add any `blockers`
3. Write decisions to files → Add to `files_to_load`
   - Made decision? → Write to `02-resources/decisions.md` → Add to list
   - Found gotcha? → Write to `03-working/session-notes.md` → Add to list
4. Update "Context for Next Agent" prose to POINT to files

Fields auto-synced by hooks: session_ids, last_updated, total_tasks, current_phase
Fields YOU must update: continue_at, blockers, files_to_load (with # reason comments)

> Philosophy: Don't capture context in prose. Write to FILES, add to files_to_load.

================================================================================
Current task: {current_task}
DO NOT start implementation until ALL Phase 1 tasks are [x] complete.
DO NOT display menu. START on current planning task immediately.
================================================================================
