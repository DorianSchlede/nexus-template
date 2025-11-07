---
name: close-session
description: Load when user says "done", "finish", "complete", "close", "wrap up", "end session", or any system skill/project completes
---

# Close Session

Save progress, update memory, regenerate navigation, and ensure system integrity.

## Purpose

The `close-session` skill is the most critical system skill. It ensures nothing is ever lost by:
- Reading and updating project progress from tasks.md checkboxes
- Regenerating navigation maps (project-map.md and skill-map.md)
- Validating workspace-map.md accuracy (auto-detect mismatches)
- Updating memory with decisions and patterns
- Cleaning temporary files from root folder
- Creating historical session reports
- Displaying comprehensive summary

**CRITICAL**: This skill is AUTO-TRIGGERED by all other skills and projects (not user-dependent!).

---

## Quick Start (MANDATORY EXECUTION SEQUENCE)

**⚠️ CRITICAL: This skill MUST follow this exact sequence - no shortcuts!**

### Step 1: Initialize TodoWrite
Create TodoList with all 9 workflow steps from workflow.md

### Step 2: STOP AND LOAD WORKFLOW (MANDATORY!)
**BEFORE CONTINUING**: Load [workflow.md](references/workflow.md) and read ALL 9 steps

### Step 3: Execute Workflow Steps Sequentially
Follow workflow.md exactly, marking each step complete in TodoList as you go

### Step 4: Handle Errors
Use [error-handling.md](references/error-handling.md) for any issues

---

## ENFORCEMENT RULES (Why This Matters)

### Rule 1: TodoWrite is MANDATORY
**Problem**: Without TodoWrite, steps get skipped or forgotten
**Solution**: Initialize TodoWrite with all 9 steps at the start

### Rule 2: workflow.md is MANDATORY
**Problem**: Line 27 says "CRITICAL STOP AND LOAD" but gets ignored
**Solution**: IMMEDIATELY load workflow.md after TodoWrite initialization

### Rule 3: bulk-complete-tasks.py is MANDATORY for complete projects
**Problem**: Project status says "COMPLETE" but tasks.md shows 0/64 complete
**Solution**: Step 2 AUTOMATICALLY runs bulk-complete-tasks.py when project work completed
**Fallback**: Step 2.5 offers manual bulk-complete if auto-detection missed it
**Location**: `scripts/bulk-complete-tasks.py` (integrated into workflow)

⚠️ **CRITICAL - COMMON MISTAKE TO AVOID**:
**NEVER** assume tasks.md is "just documentation"!
**EVERY** project's tasks.md contains REAL checkboxes that MUST be checked off!
This includes onboarding projects (00-define-goals has 40+ real tasks!).
If project work is complete, ALL tasks must be marked `[x]`!

### Rule 4: All 9 Steps Must Execute
**Problem**: Partial execution means memory doesn't persist correctly
**Solution**: Mark each step in TodoList as you complete it - ensures nothing skipped

### Why These Rules Exist:
- **Context Preservation**: This is THE ONLY mechanism for memory persistence
- **Data Integrity**: Task counts must match project status
- **System Reliability**: Skipping steps breaks the entire memory system

**Without this skill running completely, Nexus loses its memory!**

---

## Key Features

### Automatic & Interactive Task Completion
Smart task completion with automatic detection:
- **Automatic Bulk Complete**: If project work completed this session, auto-marks all tasks
- **Manual Bulk Option**: If auto-detect missed it, offers bulk-complete during review
- **Interactive Review**: Shows first 10 unchecked tasks for manual selection
- User selects by number ("1, 3, 5"), "all", "bulk complete", or "none"
- Updates tasks.md automatically (via Edit tool or bulk-complete script)
- Recalculates progress after any changes

### Navigation Regeneration
Auto-scans and rebuilds navigation maps:
- Scans `Projects/` folder for all projects
- Scans `Skills/` folder for all skills
- Updates 02-projects/project-map.md
- Regenerates skill-map.md (root)
- Validates integrity

### Temp File Cleanup
Interactive cleanup with user choices:
- Scans root folder for temp files
- Asks what to do with each: keep, delete, or skip
- Moves preserved files to project outputs/
- Reports cleanup summary

### Session Reporting
Creates historical record:
- Generates session report in 01-memory/session-reports/
- Includes work completed, progress, decisions, patterns
- Provides context for next session

### Progress Tracking
Auto-calculates from checkboxes:
- Counts total tasks (all `- [ ]` and `- [x]`)
- Counts completed tasks (only `- [x]`)
- Determines status (PLANNING/IN_PROGRESS/COMPLETE)
- Identifies next task

### Auto-Trigger Support
Called automatically by other skills:
- create-project
- validate-system
- Any skill completion

### Memory Preservation
THE critical persistence mechanism:
- Updates 02-projects/project-map.md
- Regenerates skill-map.md
- Creates session reports
- Cleans temp files

**Without this skill, context does NOT persist across sessions!**

---

## Workflow Overview

Complete workflow with all 9 steps: See [workflow.md](references/workflow.md)

### High-Level Steps:

1. **Initialize TodoList** - Create comprehensive task tracking
2. **Read Project State & Auto-Complete** - Load current focus, auto-mark tasks if project done
3. **Interactive Task Completion** - Ask user which tasks done (if not auto-completed)
4. **Update Maps** - Scan Projects/ and Skills/, regenerate navigation
5. **Get Fresh Timestamp** - Ensure accurate "Last Updated" times
6. **Update Memory Files** - Save progress, validate workspace-map.md, check for patterns
7. **Clean Temp Files** - Interactive cleanup with user choices
8. **Create Session Report** - Historical record for reference
9. **Display Summary** - Comprehensive session summary

**Total Execution Time**: 2-5 minutes (depending on interaction)

---

## Integration

### Auto-Trigger Format

When called by other skills:

```
Auto-triggering close-session skill...

[Full workflow executes]

Session saved! ✅
[Summary displays]
```

### User-Trigger Format

When user says "done for now":

```
Closing your session...

[Full workflow executes]

Session saved! ✅
[Summary displays]
```

### All Skills Must End With

Every skill and project workflow should conclude with:

```markdown
### Final Step: Close Session
Auto-trigger close-session skill to save progress
```

This ensures:
- Progress is saved
- Maps are updated
- Session is recorded
- Nothing is lost

---

## Error Handling

For complete error scenarios and solutions, see [error-handling.md](references/error-handling.md)

### Common Scenarios:

**No active project** → Skip project steps, continue with maps and cleanup

**Missing tasks.md** → Report in summary, suggest validate-system

**Corrupted memory** → Rebuild from scan, report issue

**Map generation fails** → Keep old maps, report error, suggest retry

**User doesn't respond** → Default to "skip" for temp files

---

## Critical Notes

### Memory Preservation

This skill is the **ONLY** way to:
- Update 02-projects/project-map.md with current progress
- Regenerate skill-map.md from Skills/ folder scan
- Create historical session reports
- Clean temporary files from workspace

### Context Persistence

**Without this skill running at session end:**
- Progress updates are lost
- Navigation maps become stale
- No historical record is created
- Temp files accumulate

**Never skip this skill** - it's the foundation of context preservation!

### Workflow Philosophy

This skill embodies the Nexus philosophy:
- **Memory preservation**: Nothing is ever lost
- **Context awareness**: Full system state captured
- **Progressive disclosure**: Load what you need, when you need it
- **User collaboration**: Interactive choices for important decisions

---

## Resources

### references/
- **workflow.md**: Complete 9-step workflow (with TOC)
- **error-handling.md**: All error scenarios and solutions

### scripts/
- **bulk-complete-tasks.py**: Bulk-complete all tasks in a project when work is done
  - Used in Step 2 (auto) and Step 2.5 (manual) when project is complete
  - Marks all unchecked tasks as `[x]` in one operation
  - **MANDATORY** when project status should be COMPLETE
  - Much faster than checking off 50+ tasks individually
  - Usage: `python bulk-complete-tasks.py --project [ID] --all --no-confirm`
  - The `--no-confirm` flag bypasses user confirmation for AI automation
  - Script validates by re-reading file and displays evidence of completion

---

**Remember**: This is THE most important system skill. Every session MUST end with close-session to preserve context!
