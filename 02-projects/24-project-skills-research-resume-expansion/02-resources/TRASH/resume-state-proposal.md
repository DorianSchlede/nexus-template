# Resume State Proposal

**Purpose**: Enable robust session continuation after context compaction (200k token limit)

---

## Problem Statement

### Current Behavior
- After ~200k tokens, Claude compacts the conversation (summarizes and continues)
- Current `--resume` mode only changes menu action to "continue_working"
- No structured state is preserved about:
  - Where user was in project workflow
  - What section/task was active
  - What critical context is needed
  - What decisions were made

### Impact
- AI loses detailed context after compaction
- User must re-explain where they were
- Risk of repeating completed work
- Loss of decision rationale

---

## Solution: Structured Resume State

### Core Concept
Create a `_resume.md` file in each project that acts as a "save point" for session continuation.

**Location**: `02-projects/{project-id}/01-planning/_resume.md`

**Updated**:
- Before close-session
- After major phase transitions
- On manual trigger ("save progress")
- When approaching token limit (future: auto-detect)

---

## Resume State Structure

```yaml
---
# Resume State Metadata
resume_version: 1.0
last_updated: 2026-01-03T15:30:00
compaction_count: 0  # How many times conversation was compacted
total_tokens_approx: 45000  # Approximate tokens used this session
session_count: 2  # Number of sessions on this project

# Project Context
project_id: 24-project-skills-research-resume-expansion
project_name: Project Skills Research & Resume Expansion
project_status: IN_PROGRESS  # RESEARCH | PLANNING | IN_PROGRESS | COMPLETE

# Current Location
current_phase: execution  # research | planning | execution | testing | deployment
current_skill: execute-project  # Which skill is active
current_workflow_step: 4  # Which step in skill workflow

# Execution State (for execute-project)
current_section: 2
current_section_name: Implementation
next_task_number: 15
next_task_description: Implement scoring logic
progress_tasks_completed: 14
progress_tasks_total: 40
progress_percentage: 35

# Planning State (for create-project)
planning_completed:
  - research: true
  - overview: true
  - plan: true
  - steps: false
---

# Resume State: {Project Name}

> **Last Session**: 2026-01-03 at 15:30
> **Current Phase**: Execution (Section 2: Implementation)
> **Next Action**: Continue Task 15 - "Implement scoring logic"

---

## Quick Context

**What We're Building**:
{1-2 sentence summary from overview.md purpose}

**Current Goal**:
{What the current phase/section is trying to achieve}

**Progress Summary**:
- ✅ Research phase: Complete
- ✅ Planning (overview, plan): Complete
- 🔄 Execution: Section 1 complete, Section 2 in progress (14/40 tasks)
- ⬜ Testing: Not started
- ⬜ Deployment: Not started

---

## Session History

### Session 1: Project Creation (2026-01-02)
- Created project structure
- Completed research phase
- Findings documented in `02-resources/research.md`
- Identified 3 key dependencies

### Session 2: Planning (2026-01-03)
- Completed overview.md
- Completed plan.md with First Principles + Pre-Mortem models
- Started execution phase
- Completed Section 1: Setup (8 tasks)
- Started Section 2: Implementation (6/16 tasks complete)

### Session 3 (Current): Execution Continues
- Resumed at Task 15
- Need to: [current task description]

---

## Critical Context to Remember

**Key Decisions Made**:
1. {Decision 1 and rationale}
2. {Decision 2 and rationale}

**Important Assumptions**:
- {Assumption 1}
- {Assumption 2}

**Blockers/Risks Identified**:
- [ ] {Blocker 1 - status}
- [x] {Blocker 2 - resolved how}

**Mental Models Applied**:
- First Principles: {Key insights from this model}
- Pre-Mortem: {Key risks identified}

---

## Files Modified This Project

**Created**:
- `02-resources/research.md`
- `03-working/draft-implementation.py`

**Modified**:
- `00-system/skills/project-create/SKILL.md`
- `00-system/core/nexus-loader.py`

**Pending**:
- `00-system/skills/execute-project/SKILL.md` - needs resume integration

---

## Loading Sequence for Resume

**When resuming this project**, load files in this order:

1. **THIS FILE FIRST** (`_resume.md`) - Get current state
2. **Core Planning Files**:
   - `overview.md` - Remember purpose and goals
   - `plan.md` - Recall approach and decisions
3. **Current Phase Files**:
   - `steps.md` - See all tasks and progress
   - `02-resources/research.md` - Research findings
4. **Work in Progress**:
   - `03-working/draft-implementation.py` - Current code
5. **Reference as Needed**:
   - Files listed in "Files Modified" section above

---

## Quick Start Commands

```bash
# Resume this project
python 00-system/core/nexus-loader.py --resume --project 24

# The loader will:
# 1. Detect _resume.md exists
# 2. Return resume-specific instructions
# 3. Point AI to this file first
# 4. Provide loading sequence above
```

---

## Compaction Detection

**Token Tracking** (for future auto-save):
- Current session: ~45,000 tokens
- Warning threshold: 180,000 tokens (90% of 200k)
- Critical threshold: 195,000 tokens (trigger auto-save)

**Manual Save Triggers**:
- User says "save progress"
- User says "done for today" (close-session)
- After completing major phase (bulk-complete section)

---

## Resume State Update Checklist

**After each session**:
- [ ] Update last_updated timestamp
- [ ] Update session_count
- [ ] Update current location (phase, section, task)
- [ ] Update progress metrics
- [ ] Add session summary to Session History
- [ ] Update Critical Context if decisions made
- [ ] Update Files Modified list

---

## Integration Points

### execute-project Skill
1. Check for `_resume.md` on project load
2. If exists: Display quick context from resume state
3. Offer to continue from saved position
4. Update resume state after bulk-complete
5. Update resume state before close-session

### create-project Skill
1. Create initial `_resume.md` when project initialized
2. Update planning_completed flags as each step finishes
3. Transition to execution phase updates current_phase

### nexus-loader.py
1. Add `--resume --project [ID]` combined mode
2. Check for `_resume.md` in project directory
3. Return resume-specific loading instructions
4. Include resume state in response

### close-session Skill
1. Always update `_resume.md` before closing
2. Prompt user if critical decisions not captured
3. Verify Files Modified list is current

---

## Example Resume Flow

**User**: "Continue project 24"

**AI Loads**:
1. Runs: `python nexus-loader.py --project 24`
2. Loader detects `_resume.md` exists
3. Returns: `recommended_reads: ["01-planning/_resume.md", "01-planning/overview.md", ...]`

**AI Reads Resume**:
```
Quick Context shows:
- Last session: 2026-01-03 at 15:30
- Current: Section 2 Implementation, Task 15
- Progress: 14/40 tasks (35%)
```

**AI Responds**:
```markdown
Welcome back! Picking up where we left off:

📍 CURRENT STATE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Project: Project Skills Research & Resume Expansion
Last Session: Yesterday at 15:30
Progress: 14/40 tasks (35%)

Current Location:
  Section 2: Implementation
  Next Task: #15 - "Implement scoring logic"

Recent Progress:
  ✅ Completed Section 1: Setup (8 tasks)
  🔄 Section 2: 6/16 tasks complete

Key Context:
  - Using First Principles + Pre-Mortem models
  - Decision: [Key decision from Critical Context]
  - Blocker: [Active blocker if any]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to continue Task 15, or would you like to:
1. Review completed work first
2. Jump to different section
3. Update the plan based on learnings
```

---

## Benefits

1. **Seamless Continuation**: Resume exactly where you left off
2. **Context Preservation**: Critical decisions and rationale saved
3. **Progress Visibility**: Always know where you are
4. **Compaction Resilience**: Survive 200k token compaction
5. **Session Transparency**: Clear history of what happened when

---

## Implementation Phases

### Phase 1: Basic Resume State
- Create `_resume.md` template
- Update execute-project to write resume state
- Update nexus-loader.py to read resume state
- Basic resume flow working

### Phase 2: Auto-Update Integration
- Hook into bulk-complete to auto-update progress
- Hook into close-session to save state
- Add manual "save progress" trigger

### Phase 3: Compaction Detection (Future)
- Track token usage per session
- Warn at 180k tokens
- Auto-trigger save at 195k tokens
- Suggest natural stopping points

---

**Status**: Proposal
**Next**: Review with stakeholder, refine template, implement Phase 1
