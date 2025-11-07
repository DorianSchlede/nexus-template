# close-session Complete Workflow

Complete step-by-step workflow for saving progress, updating memory, regenerating navigation, and ensuring system integrity.

---

## Table of Contents

- [Step 1: Initialize TodoList](#step-1-initialize-todolist)
- [Step 2: Read Active Project State](#step-2-read-active-project-state)
- [Step 2.5: Review Task Completion (Interactive)](#step-25-review-task-completion-new---interactive)
- [Step 3: Update Maps](#step-3-update-maps-replaces-build-maps-skill)
  - [3a. Scan Projects/ Folder](#3a-scan-projects-folder)
  - [3b. Scan Skills/ Folder](#3b-scan-skills-folder)
  - [3c. Update project-map.md](#3c-update-02-projectsproject-mapmd)
  - [3d. Update skill-map.md](#3d-update-skill-mapmd-root)
  - [3e. Validate Integrity](#3e-validate-integrity)
- [Step 4: Get Fresh Timestamp](#step-4-get-fresh-timestamp)
- [Step 5: Update Memory Files](#step-5-update-memory-files)
  - [5a. Update project-map.md](#5a-update-02-projectsproject-mapmd-if-not-done-in-step-3c)
  - [5b. Check for Patterns](#4b-check-for-patterns)
- [Step 6: Clean Up Temporary Files](#step-6-clean-up-temporary-files)
  - [6a. Scan Root Folder](#5a-scan-root-folder)
  - [6b. Process Each Temp File](#5b-process-each-temp-file)
  - [6c. Report Cleanup Summary](#5c-report-cleanup-summary)
- [Step 7: Create Session Report](#step-7-create-session-report)
- [Step 7.5: Skill Execution Review](#step-75-skill-execution-review-for-create-project)
- [Step 8: Display Summary](#step-8-display-summary)
- [Step 9: Mark TodoWrite Complete](#step-9-mark-todowrite-complete)
- [Step 10: Instruct User to Start Fresh Session](#step-10-instruct-user-to-start-fresh-session)

---

## Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Read project state
- [ ] Review task completion (interactive)
- [ ] Update maps (scan Projects/ and Skills/)
- [ ] Update memory files
- [ ] Clean temp files (interactive)
- [ ] Create session report
- [ ] Display summary
- [ ] Instruct user to start fresh session
```

This creates transparency and allows progress tracking during session closure.

**Mark tasks complete as you finish each step throughout this workflow.**

---

## Step 2: Read Active Project State & Auto-Complete if Done

⚠️ **CRITICAL WARNING - COMMON MISTAKE**:
**DO NOT** skip task completion because you think tasks.md is "just documentation"!
**EVERY tasks.md file contains ACTUAL CHECKBOXES** that must be marked complete!
Even onboarding projects (00-define-goals, 01-first-project, etc.) have REAL tasks!

**Load 02-projects/project-map.md**:
- Identify current focus project from "Current Focus" section
- Extract project ID and name

**IF current focus exists**:
- Load `Projects/{ID}-{name}/planning/tasks.md`
- **CRITICAL**: This file contains REAL checkboxes, not just documentation!
- Count total tasks (all checkboxes: `- [ ]` and `- [x]`)
- Count completed tasks (only `- [x]` or `- [X]`)
- Calculate progress: `X/Y` format
- Identify first unchecked task (current task)
- Determine status change:
  - **PLANNING**: 0-9% complete
  - **IN_PROGRESS**: 10-99% complete
  - **COMPLETE**: 100% complete

**AUTOMATIC BULK-COMPLETION CHECK** (NEW - MANDATORY):

**IF** project work was done this session **AND** work appears complete:
- Check if there are many unchecked tasks remaining (>10)
- Check if session context indicates "project finished", "all done", "completed everything", etc.

**IF BOTH conditions true**:
```
🎉 Detected completed project work!

Project: [project-name]
Status: All work complete, but [N] tasks unchecked

Automatically marking all tasks as complete...
```

**Execute**:
- Run: `python 00-system/skills/close-session/scripts/bulk-complete-tasks.py --project [project-id] --all --no-confirm`
- Script marks ALL unchecked tasks as `[x]` without confirmation prompt
- Script validates by re-reading file
- Recalculate progress (should now be 100%)
- Display script output showing: "✅ VALIDATED: Re-read file shows 0 uncompleted, [N] completed"
- Display: "✅ Marked [N] tasks as complete! Progress: 100%"

**THEN** continue to Step 2.5 (will skip interactive review since all tasks done)

**IF no current focus**:
- Note: "No active project this session"
- Continue with general session closure

---

## Step 2.5: Review Task Completion (INTERACTIVE - only if auto-complete didn't run)

**IF bulk-complete already ran in Step 2**:
- Skip this entire step (all tasks already complete)
- Continue to Step 3

**IF current focus project still has unchecked tasks**:

### 1. Display context
```
Let's update your task list for [project-name].

You've been working on: [current task from tasks.md]
```

### 2. Check if project appears complete but wasn't auto-detected

**IF project seems complete but wasn't caught in Step 2**:

```
This project appears to be complete!

However, I see [N] unchecked tasks in tasks.md. Would you like to:

a) "bulk complete" - Mark all remaining tasks as complete (fast, for finished projects)
b) "review" - Review tasks individually to select which to check off
c) "skip" - Leave tasks as-is

What would you like to do?
```

**IF user says "bulk complete" or "bulk"**:
- Run: `python 00-system/skills/close-session/scripts/bulk-complete-tasks.py --project [project-id] --all --no-confirm`
- Script will mark ALL unchecked tasks as `[x]` without confirmation
- Script validates by re-reading file
- Display script output: "✅ VALIDATED: Re-read file shows 0 uncompleted, [N] completed"
- Display: "✅ Marked [N] tasks as complete!"
- Recalculate progress (should now be 100%)
- **Skip to Step 3** (project is now complete)

**IF user says "review"**:
- Continue to Step 3 below (interactive selection)

**IF user says "skip"**:
- Skip to Step 3 (leave tasks as-is)

### 3. Get first 10 unchecked tasks (only if reviewing individually)
- Read tasks.md
- Extract first 10 unchecked tasks (with line context)
- Number them 1-10

### 4. Ask user
```
Which tasks did you complete today? (You can say task numbers, "none", or "all")

Unchecked tasks:
1. [ ] Create root Nexus-v3/ folder
2. [ ] Create 00-system/ folder
3. [ ] Create 00-system/agents/ folder
4. [ ] Create 00-system/skills/ folder
5. [ ] Create Projects/ folder
[... up to 10]

Say: "1, 3, 5" or "none" or "all"
```

### 5. Process response
- **"none"**: Skip to next step
- **"all"**: Check off all 10 shown tasks
- **Numbers** (e.g., "1, 3, 5"): Check off specific tasks
- **Task description**: Match and check off
- **"bulk complete"** or **"bulk"**: Offer bulk-completion option (see Step 2 above)

### 6. Update tasks.md
- For each selected task, change `- [ ]` to `- [x]`
- Preserve exact formatting and indentation
- Use Edit tool with exact string replacement

### 7. Recalculate progress
- Count new totals (completed / total)
- Update progress percentage
- Store for later update

### 8. Confirm to user
```
✓ Checked off 3 tasks
New progress: 5/624 tasks (0.8%)
```

**IF all tasks shown are now complete AND more unchecked tasks remain**:
- Repeat Steps 3-8 with next 10 tasks
- Continue until user says "none" or all tasks complete

**IF 100% complete**:
- Celebrate: "🎉 All tasks complete!"
- Suggest archival: "Run 'archive project [name]' to move to archived/"

---

## Step 3: Update Maps (REPLACES build-maps skill!)

This is the core navigation regeneration step.

### 3a. Scan Projects/ Folder

```
For each folder in Projects/:
  1. Identify {ID}-{name} format
  2. Load planning/tasks.md
  3. Count total tasks (checkboxes)
  4. Count completed tasks ([x] or [X])
  5. Calculate progress (X/Y)
  6. Determine status:
     - PLANNING: 0-9% complete
     - IN_PROGRESS: 10-99% complete
     - COMPLETE: 100% complete
  7. Identify first unchecked task (current task)
  8. Get last modified timestamp of tasks.md
  9. Build project data structure
```

### 3b. Scan Skills/ Folder

```
For each folder in Skills/:
  1. Identify {skill-name}
  2. Load SKILL.md
  3. Extract first line after title (one-line purpose)
  4. Check for subfolders:
     - /scripts exists?
     - /references exists?
     - /assets exists?
  5. For each subfolder, identify when resources should load
  6. Build skill data structure
```

### 3c. Update 02-projects/project-map.md

Update the comprehensive project map:

```markdown
# Project Map

**Last Updated**: YYYY-MM-DD HH:MM:SS

## System State

IF goals.md missing OR empty:
  → System uninitialized
  → Load Projects/00-setup-memory/
  → Guide through memory initialization

IF onboarding projects (00-04) not all complete:
  → Load current onboarding project (from Active Projects below)
  → Display guidance from project planning files

IF all onboarding complete:
  → System operational
  → Display active projects and skills

## Active Projects

### 00-setup-memory
**Status**: COMPLETE
**Progress**: 15/15 tasks complete
**Last Updated**: YYYY-MM-DD HH:MM:SS
**Location**: Projects/00-setup-memory/

### 05-website-development
**Status**: IN_PROGRESS
**Progress**: 3/8 tasks complete
**Last Updated**: YYYY-MM-DD HH:MM:SS
**Current Task**: Design homepage mockup
**Location**: Projects/05-website-development/

[Repeat for each project found in scan]

## Current Focus
05-website-development - Building consulting website
Last session: YYYY-MM-DD HH:MM:SS

## Recent Decisions
- Decided to use Tailwind CSS for styling
- Will deploy to Vercel for hosting
[Max 10, newest first - add new decision if any from this session]
```

**Key Updates**:
- Update all project entries with current status
- Update timestamps to current session time
- Update "Last Updated" for modified projects
- Update "Current Task" based on checkbox scan
- Add new decision if captured during session
- Keep Recent Decisions to max 10 (remove oldest)

### 3d. Update skill-map.md (root)

Regenerate user skills map:

```markdown
# Skill Map

**Last Updated**: YYYY-MM-DD HH:MM:SS

## User Skills

### weekly-status-report
**Purpose**: Generate weekly status report from project progress
**Location**: Skills/weekly-status-report/
**Load /references/template.md**: When user starts skill execution
**Load /scripts/format.py**: When generating final output

### client-proposal-generator
**Purpose**: Create client proposal from discovery notes
**Location**: Skills/client-proposal-generator/
**Load /references/proposal-template.md**: When filling proposal sections
**Load /assets/logo.png**: When generating final PDF

[Repeat for each skill found in scan]

---

No user skills yet? Run `create-skill` to add one!

**Note**: System skills are defined in `00-system/framework-map.md`
```

**IF Skills/ folder is empty**:
```markdown
# Skill Map

**Last Updated**: YYYY-MM-DD HH:MM:SS

## User Skills

> No user skills yet. Run `create-skill` to add one!
>
> System skills are defined in `00-system/framework-map.md`

---

**Note**: This file is auto-generated by the `close-session` skill.
It scans the `Skills/` folder and lists all user-created skills.
```

### 3e. Validate Integrity

Check for issues:
- [ ] All projects in Projects/ are listed in 02-projects/project-map.md
- [ ] All skills in Skills/ are listed in skill-map.md
- [ ] No dead links in navigation
- [ ] Timestamps are current
- [ ] All required files exist (tasks.md for projects, SKILL.md for skills)

**IF issues found**:
- Report in session summary (Step 8)
- Suggest "Run validate-system for detailed check"

---

## Step 4: Get Fresh Timestamp

**CRITICAL**: Get current timestamp NOW (not from session start):
- Execute: `powershell -Command "Get-Date -Format 'yyyy-MM-DD HH:mm:ss'"`
- Or equivalent for your system
- Store as `current_timestamp` variable
- This ensures "Last Updated" fields reflect actual update time

**Why this matters**: Using session start timestamp creates staleness (20+ min old timestamps).

---

## Step 5: Update Memory Files

### 5a. Update 02-projects/project-map.md (if not done in Step 3c)

If current focus project exists:
- Update progress count (X/Y)
- Update status (if changed)
- Update "Last Updated" timestamp
- Update "Current Task" (first unchecked)
- Update "Current Focus" section with timestamp

### 5b. Validate workspace-map.md (NEW - AUTO-VALIDATE)

**Purpose**: Ensure workspace-map.md stays synchronized with actual 04-workspace/ structure

**Step 1: List actual folders**
- Execute: List all top-level folders in 04-workspace/
- Store: ACTUAL_FOLDERS = ["Clients/", "Templates/", "Research/"]
- Exclude: Hidden folders, .git, etc.

**Step 2: Read workspace-map.md**
- Read: 04-workspace/workspace-map.md
- Parse: Extract folder names mentioned in descriptions
- Store: MAPPED_FOLDERS = ["Clients/", "Templates/", "Research/"]

**Step 3: Compare structures**
- Compare: ACTUAL_FOLDERS vs MAPPED_FOLDERS
- Identify mismatches:
  - Missing from map: Folders that exist but not documented
  - Extra in map: Folders documented but don't exist (stale)

**Step 4: Handle results**

**IF perfect match** (ACTUAL == MAPPED):
- Continue silently (no output needed)
- workspace-map is accurate

**IF mismatches found**:
```
⚠️ workspace-map.md needs updating

Discrepancies found:
- Missing from map (exist but not documented): Projects/, Notes/
- Extra in map (documented but don't exist): OldClients/

Would you like me to help update workspace-map.md now?
Reply: "yes" / "no" / "later"
```

**IF user says "yes"**:
- For each missing folder:
  ```
  I see you have a "Projects/" folder in workspace.
  What should I note about this folder? (1-2 sentences)
  ```
- For each extra folder:
  ```
  "OldClients/" is in the map but doesn't exist anymore.
  I'll remove it from the map.
  ```
- Update workspace-map.md with new descriptions
- Read file again to validate
- Display: "✅ workspace-map.md updated and validated"

**IF user says "no" or "later"**:
- Display: "Note: Please update workspace-map.md when you have time"
- Display: "It helps me navigate your workspace correctly"
- Continue to next step

**Time**: 30-60 seconds if mismatches found, 0 seconds if perfect match

### 5c. Check for Patterns

Analyze this session's work:

**IF repeatable workflow emerged**:
- Note: "Detected repeatable workflow: [description]"
- Suggest: "Consider creating a skill with 'create-skill'"
- Add suggestion to display summary

**IF new insight gained**:
- Update 01-memory/core-learnings.md
- Add to "Patterns Discovered" section:
  ```markdown
  ### [Pattern Name]
  **Observed**: YYYY-MM-DD
  **Context**: [when this pattern emerged]
  **Insight**: [what was learned]
  ```

**IF system preference detected**:
- Update 01-memory/core-learnings.md
- Add to "System Preferences" section

---

## Step 6: Clean Up Temporary Files

This ensures a clean workspace.

### 5a. Scan Root Folder

Look for temporary files:
- `*.tmp`
- `*.temp`
- `*.log`
- Unnamed files: `file-1.md`, `untitled.md`, `unnamed-*.md`
- Tool output files not in project outputs/
- Draft files not intentionally saved

**Exclude from scan**:
- `claude.md` (root file)
- `README.md` (documentation)
- `skill-map.md` (navigation)
- Any file in 00-system/, Projects/, Skills/, Memory/, User-Folders/

### 5b. Process Each Temp File

For each temp file found:

#### 1. Display file info
```
Found temporary file: file-1.md (12 KB)
Preview: [first 2 lines of content]
```

#### 2. Ask user
```
What should I do with this file?

Options:
- "keep" or "preserve" → Ask which project outputs/ to move to
- "delete" or "remove" → Delete permanently
- "skip" → Leave it for now
```

#### 3. If user says "keep" or "preserve"
```
Which project should this go in?

Active projects:
- 05-website-development
- 06-client-outreach

Or say "skip" to leave it.
```

**Then**:
- Move file to `Projects/{ID}-{name}/outputs/`
- Rename if needed to avoid conflicts
- Confirm: "Moved to Projects/{ID}-{name}/outputs/{filename}"

#### 4. If user says "delete" or "remove"
- Delete file
- Confirm: "Deleted {filename}"

#### 5. If user says "skip"
- Leave file in place
- Note: "Left {filename} in place"

### 5c. Report Cleanup Summary

Count actions:
- Files preserved: X
- Files deleted: Y
- Files skipped: Z

Include in session summary (Step 8).

---

## Step 7: Create Session Report

Generate historical record in 01-memory/session-reports/.

**File**: `01-memory/session-reports/YYYY-MM-DD-session.md`

**IF file exists** (multiple sessions in one day):
- Append with session number: `YYYY-MM-DD-session-2.md`

**Content**:
```markdown
# Session Report - YYYY-MM-DD

**Duration**: [start time estimate] - [end time]
**Focus**: [project name or "General work" or "System setup"]

## Work Completed

[IF project work:]
- [Completed task 1 from tasks.md]
- [Completed task 2 from tasks.md]

[IF no project work:]
- [Summary of what was done this session]

## Progress Made

[IF project work:]
**Before**: X/Y tasks complete
**After**: Z/Y tasks complete
**Status**: [status before] → [status after]

[IF no project work:]
General session: [brief description]

## Decisions Made

[IF decisions captured:]
- [Decision 1]
- [Decision 2]

[IF no decisions:]
No major decisions this session.

## Patterns Observed

[IF patterns detected:]
- [Pattern 1]
- [Pattern 2]

[IF no patterns:]
No new patterns detected.

## Maps Updated

- project-map.md: Updated [Y] projects
- skill-map.md: Updated [Z] skills

## Cleanup

- Temporary files: [X preserved, Y deleted, Z skipped]

## Next Steps

[Recommendations based on current state:]
- Continue: [next task in current project]
- Or: [alternative actions]

## Context Notes

[Any relevant context for next session:]
- [Note 1]
- [Note 2]
```

**Estimation for duration**:
- If timestamps available: calculate from session start
- If not: estimate as "~[N] minutes" based on work done

---

## Step 7.5: Skill Execution Review (For create-project)

**IF `create-project` skill was used this session:**

Check session history/context to determine if create-project was executed. If yes, ask user:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Quick Execution Review
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

I want to make sure I followed the create-project workflow correctly.

Did I:
✅ Use TodoWrite at the beginning?
✅ Pause after each document for your review?
✅ Wait for your confirmation before proceeding?
✅ Collaborate with you instead of just generating?

If I skipped any of these steps, please let me know so I can
improve for next time. This helps me follow the system's
collaborative design philosophy better.

Reply: "yes, you did great" / "you skipped [step]" / "let's not worry about it"
```

**Process Response**:
- **"yes, you did great"** / **"looks good"** / **"all good"** → Continue to Step 8
- **"you skipped [X]"** / **"you didn't [Y]"** →
  - Acknowledge: "Thank you for the feedback! I'll be more careful about [X] next time."
  - Log to 01-memory/core-learnings.md under "AI Behavior Patterns"
  - Continue to Step 8
- **"let's not worry about it"** / **"skip"** → Continue to Step 8

**Why this matters**: AI agents tend to optimize for speed, sometimes skipping collaborative steps. This review helps the system learn and improve adherence to the collaborative workflow philosophy.

---

## Step 8: Display Summary

Show comprehensive session summary to user:

```
Session saved! ✅

Progress:
- Project: [project name or "General work"]
- Completed: [X tasks or "N/A"]
- Status: [current status or "N/A"]

Maps Updated:
- project-map: [Y projects]
- skill-map: [Z skills]
- workspace-map: [✅ Accurate or ⚠️ Needs update]

Cleanup:
- Temporary files: [X preserved, Y deleted, Z skipped]

[IF patterns detected:]
Patterns Detected:
- [Pattern 1]
- [Pattern 2]

[IF repeatable workflow detected:]
💡 Suggestion: Consider creating a skill for "[workflow name]"
   Say "create skill" to capture this workflow!

Next Session:
[IF current focus project:]
- Continue: [project name]
- Next task: [first unchecked task description]

[IF no current focus:]
- Start new work, or
- Say "create project" to begin something new

[IF issues found in validation:]
⚠️ Issues detected: [count]
  Run "validate system" for detailed check and auto-fix.

See you next time! 🚀
```

---

## Step 9: Mark TodoWrite Complete

Mark all TodoWrite tasks as complete.

**Workflow complete!**

---

## Step 10: Instruct User to Start Fresh Session

**CRITICAL - FINAL STEP**: After completing all close-session steps, instruct the user to start a new conversation for proper memory boundaries:

```
✅ Session closed successfully!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔄 IMPORTANT: Start a Fresh Session
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

To ensure proper context loading and memory boundaries:

Please either:
1. **Close this chat** and start a new one, OR
2. Use the **/clear conversation** command

This ensures:
✓ Clean context for next session
✓ Fresh loading of updated project state
✓ Proper memory boundaries
✓ No context pollution from previous session

When you return, I'll automatically load your updated progress
and pick up right where we left off!

See you next time! 🚀
```

**Why this matters**:
- Prevents context pollution from previous session
- Ensures nexus-loader.py runs fresh with updated state
- Proper separation between sessions (planning principle)
- Avoids AI confusion from stale context

**DO NOT skip this step** - it's critical for system integrity!

---

**END OF WORKFLOW**
