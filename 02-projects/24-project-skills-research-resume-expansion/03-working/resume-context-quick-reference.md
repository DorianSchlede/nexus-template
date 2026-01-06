# Resume Context - Quick Reference

**Question**: What needs to go in resume-context.md and what needs to be loaded?

---

## What Goes IN resume-context.md

**Purpose**: LOADING MANIFEST + MINIMAL STATE (NOT a summary!)

### Required YAML Fields (10 total)

| Field | Type | Purpose | Example | When Updated |
|-------|------|---------|---------|--------------|
| **resume_schema_version** | string | Schema version tracking | `"1.0"` | Never (set at creation) |
| **last_updated** | timestamp | Last modification time | `"2026-01-04T19:45:00Z"` | Every update (auto) |
| **project_id** | string | Project identifier | `"24-project-skills"` | Never (set at creation) |
| **project_name** | string | Human-readable name | `"Project Skills Research"` | Never (set at creation) |
| **current_phase** | enum | Execution phase | `"execution"` | Phase transitions |
| **next_action** | string | Skill to execute | `"execute-project"` | Skill changes |
| **files_to_load** | array | Files to auto-load | `["01-planning/overview.md", ...]` | File additions |
| **current_section** | integer | Next section to work on | `4` | Section completion |
| **current_task** | integer | Next task to work on | `1` | Task/section completion |
| **total_tasks** | integer | Total task count | `40` | steps.md changes (rare) |
| **tasks_completed** | integer | Completed task count | `28` | Every bulk-complete |

### What NOT to Include

❌ **NO duplication** of content from other files
❌ **NO summaries** of work done
❌ **NO detailed progress notes**
❌ **NO session history**
❌ **NO validation gates** (removed in optimized version)

**Principle**: If it's already in overview.md, plan.md, or steps.md → DON'T repeat it here!

---

## What Gets LOADED on Resume

**Purpose**: SessionStart hook auto-loads files to restore complete context

### Auto-Loaded Files (from `files_to_load[]`)

**Minimum Set** (always):
```yaml
files_to_load:
  - "01-planning/overview.md"     # Project purpose, goals, success criteria
  - "01-planning/plan.md"          # Approach, decisions, dependencies
  - "01-planning/steps.md"         # Task checklist with progress
```

**Extended Set** (when research completed):
```yaml
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"
  - "01-planning/steps.md"
  - "01-planning/research.md"      # Research findings (if exists)
```

**Custom Set** (project-specific):
```yaml
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"
  - "01-planning/steps.md"
  - "01-planning/design.md"        # Architecture/design (if exists)
  - "02-resources/api-schema.json" # Critical reference (if needed)
```

### Loading Flow

**1. PreCompact Hook** (before compaction):
- Writes `precompact_state.json` with active project ID
- No context injection (returns `{}`)

**2. SessionStart Hook** (on resume):
- Reads `precompact_state.json` → gets project ID
- Loads `resume-context.md` from detected project
- Parses `files_to_load[]` array
- **Auto-loads all files** listed in array
- Injects MANDATORY instructions to AI
- AI continues from exact point automatically

**3. AI Receives**:
- All files from `files_to_load[]` (pre-loaded in context)
- Current section/task from resume-context.md
- Next action from resume-context.md
- Zero need for user to explain "continue from X"

---

## Information Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     RESUME-CONTEXT.MD                        │
│  (LOADING MANIFEST - tells SessionStart what to load)       │
│                                                              │
│  files_to_load:                                             │
│    - "01-planning/overview.md"   ┐                          │
│    - "01-planning/plan.md"       ├──> SessionStart Hook     │
│    - "01-planning/steps.md"      ┘    Auto-Loads These     │
│                                                              │
│  current_section: 4              ──> AI knows where to start│
│  current_task: 1                 ──> AI knows next task     │
│  next_action: "execute-project"  ──> AI knows what to do    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  AI RECEIVES IN CONTEXT                      │
│                                                              │
│  1. overview.md  → Purpose, goals, success criteria         │
│  2. plan.md      → Approach, decisions, dependencies        │
│  3. steps.md     → Full task list with [x] progress         │
│  4. resume state → Section 4, Task 1, execute-project       │
│                                                              │
│  AI: "I know exactly where we are. Continuing Section 4..." │
└─────────────────────────────────────────────────────────────┘
```

---

## Update Triggers

**When to Update resume-context.md**:

| After This... | Update These Fields | Command |
|--------------|---------------------|---------|
| **Section 3 complete** | `current_section=4`, `current_task=1`, `tasks_completed=28` | `--section 4 --completed 28` |
| **Tasks 10-15 complete** | `current_task=16`, `tasks_completed=15` | `--task 16 --completed 15` |
| **Phase change** | `current_phase="testing"` | `--phase testing` |
| **Add research.md** | `files_to_load` (manual edit) | N/A (edit YAML) |
| **Project done** | `current_phase="complete"`, `tasks_completed=40` | `--phase complete --completed 40` |

**Pattern**: Update IMMEDIATELY after every `bulk-complete-tasks.py` success.

---

## Example: Section 3 Completion

**Before bulk-complete**:
```yaml
current_section: 3      # Working on Section 3
current_task: 1         # Started at task 1
tasks_completed: 12     # 12 tasks done across all sections
```

**Execute work**:
```bash
# Work on Section 3 (tasks 13-28, 16 total tasks)
# ... execute tasks ...

# Bulk-complete Section 3
bulk-complete-tasks.py --project 05-lead-qualification --section 3
# Output: Successfully completed 16 tasks! 28/40 complete
```

**Update resume** (IMMEDIATELY after):
```bash
update_resume_context.py --project 05-lead-qualification --section 4 --completed 28
```

**After update**:
```yaml
current_section: 4      # NEXT section (not 3!)
current_task: 1         # Reset to 1 for new section
tasks_completed: 28     # New total (12 + 16)
last_updated: "2026-01-04T19:45:32Z"  # Auto-updated
```

**On next resume**:
- SessionStart loads overview.md, plan.md, steps.md
- AI sees current_section=4, current_task=1
- AI continues: "Section 4: Testing..."
- NO user trigger needed!

---

## Why This Design?

### Problem with Old Approach
❌ Summaries in resume file → duplication → stale data
❌ Manual triggers → user must say "continue project X"
❌ No auto-loading → AI must manually read files

### Solution with resume-context.md
✅ **Minimal manifest** → just loading instructions + state
✅ **Auto-loading** → files pre-loaded by SessionStart hook
✅ **Auto-continue** → AI knows what to do automatically
✅ **Always current** → updated after every bulk-complete

**Result**: Seamless continuation across 200k token compaction boundary!

---

## Quick Checklist

After every section completion:

- [ ] Bulk-complete section succeeds
- [ ] Update resume-context.md (section, task, completed)
- [ ] Verify update script output shows changes
- [ ] Continue to next section OR pause

**If pausing**:
- Resume state is current → next session auto-continues ✅

**If continuing**:
- Move to next section → repeat workflow ✅

---

**Key Insight**: resume-context.md is a **ROUTER**, not a **STORAGE**. It tells SessionStart **what to load** and **where to continue**, but doesn't store the actual content.
