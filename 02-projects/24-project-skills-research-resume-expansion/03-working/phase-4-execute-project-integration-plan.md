# Phase 4: execute-project Resume Integration Plan

**Created**: 2026-01-04
**Status**: Planning
**Estimated Time**: 2-3 hours

---

## Goal

Integrate resume-context.md auto-updates into the execute-project workflow to ensure:
1. Resume state stays current during project execution
2. Resume template is optimized (minimal, essential fields only)
3. AI can seamlessly resume after compaction without friction

---

## Current State

**What Works**:
- ✅ PreCompact hook detects active project from transcript
- ✅ SessionStart hook reads resume-context.md and auto-loads files
- ✅ Auto-loading injects 9 files (3 system + 5 project + 1 skill)
- ✅ Migration script updated 20+ projects to new schema

**What's Missing**:
- ❌ execute-project doesn't update resume-context.md during execution
- ❌ Resume template has bloated body content (validation gate, session history)
- ❌ No automatic updates at task/section completion checkpoints

---

## Problem Analysis

### Issue 1: Manual Resume Updates Only
**Current Behavior**: Resume-context.md only gets updated manually (user must trigger)
**Impact**: After compaction, resume might be stale (doesn't reflect latest progress)
**Solution**: Auto-update at natural checkpoints during execute-project

### Issue 2: Bloated Resume Template
**Current State**: Resume-context.md has verbose body content:
- Validation gate (questions for AI to answer)
- Session history log
- Old progress notes

**Impact**: Unnecessary content in every project's resume file
**Solution**: Streamline to YAML frontmatter only + minimal body

### Issue 3: Update Trigger Points Unclear
**Current State**: No defined strategy for when to update resume
**Impact**: Risk of forgetting to update at critical moments
**Solution**: Define clear trigger points in execute-project workflow

---

## Proposed Solution

### A. Resume Template Optimization

**BEFORE** (current resume-context.md):
```yaml
---
resume_schema_version: "1.0"
last_updated: "2026-01-04T17:00:00Z"
project_id: "24-project-skills-research-resume-expansion"
project_name: "Project Skills Research & Resume Expansion"
current_phase: "ready-for-implementation"
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"
  - "01-planning/steps.md"
  - "02-resources/FINAL-DESIGN.md"
  - "02-resources/resume-state-REVISED.md"
current_section: 3
current_task: 1
progress: "Phase 0 ✅ (10h) | Phase 1 ✅ (1.5h) | Phase 2 ✅ (2h) | Phase 3 ✅ COMPLETE (2h)"
---

# Validation Gate

Before continuing, you MUST verify you understand:
1. **Project Purpose** (from overview.md):
   - What problem are we solving?
   - What is the success criterion?
... (lots of body content)
```

**AFTER** (optimized):
```yaml
---
resume_schema_version: "1.0"
last_updated: "2026-01-04T17:00:00Z"

# PROJECT
project_id: "24-project-skills-research-resume-expansion"
project_name: "Project Skills Research & Resume Expansion"
current_phase: "execution"

# LOADING
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"
  - "01-planning/steps.md"

# STATE
current_section: 3
current_task: 1
total_tasks: 40
tasks_completed: 25
---

*Auto-updated by execute-project skill on task/section completion*
```

**Changes**:
- ❌ Remove validation gate (not needed - auto-loading guarantees files in context)
- ❌ Remove verbose progress string (use simple counters instead)
- ❌ Remove session history (not essential for resume)
- ✅ Keep only essential YAML frontmatter
- ✅ Add minimal footer note

**Benefits**:
- Cleaner, easier to read
- Faster to parse
- Less prone to errors
- Focuses on loading manifest purpose

---

### B. Update Trigger Points in execute-project

**Strategy**: Update resume-context.md at natural checkpoints

**Trigger Points**:

1. **After Task Completion**
   - Update: `current_task`, `tasks_completed`, `last_updated`
   - Frequency: Every task
   - Cost: Minimal (1 file write)

2. **After Section Completion**
   - Update: `current_section`, `current_task`, `tasks_completed`, `last_updated`
   - Frequency: Every section
   - Cost: Minimal (1 file write)

3. **On Phase Transition**
   - Update: `current_phase`, `files_to_load[]`, `next_action`, all counters
   - Frequency: Rare (planning → execution, execution → testing, etc.)
   - Cost: Medium (may need to recalculate files_to_load)

**Implementation Pattern**:
```python
def update_resume_context(project_path, updates):
    """
    Update resume-context.md YAML frontmatter.

    Args:
        project_path: Path to project directory
        updates: Dict of fields to update
    """
    resume_file = project_path / "01-planning" / "resume-context.md"

    # Read current YAML
    import frontmatter
    post = frontmatter.load(resume_file)

    # Update fields
    for key, value in updates.items():
        post.metadata[key] = value

    # Always update timestamp
    from datetime import datetime
    post.metadata["last_updated"] = datetime.utcnow().isoformat() + "Z"

    # Write back
    frontmatter.dump(post, resume_file)
```

---

### C. execute-project Skill Integration Points

**1. Task Completion (Recommended Approach)**:
```python
# After marking task complete with bulk-complete.py
update_resume_context(project_path, {
    "current_task": next_task_number,
    "tasks_completed": total_completed
})
```

**2. Section Completion**:
```python
# After completing all tasks in a section
update_resume_context(project_path, {
    "current_section": next_section_number,
    "current_task": first_task_in_next_section,
    "tasks_completed": total_completed
})
```

**3. Phase Transition** (optional - if needed):
```python
# When transitioning from planning → execution
update_resume_context(project_path, {
    "current_phase": "execution",
    "files_to_load": [
        "01-planning/overview.md",
        "01-planning/plan.md",
        "01-planning/steps.md"
    ],
    "next_action": "execute-project"
})
```

---

## Implementation Steps

### Step 1: Optimize Resume Template (30 min)
- [ ] Create new minimal resume-context.md template
- [ ] Remove validation gate
- [ ] Remove session history
- [ ] Simplify progress tracking (use counters)
- [ ] Test YAML parsing still works

### Step 2: Create Update Helper Script (30 min)
- [ ] Create `update_resume_context.py` in execute-project/scripts/
- [ ] Implement YAML frontmatter update logic
- [ ] Add validation (schema checking)
- [ ] Add error handling (backup, rollback)
- [ ] Test with sample resume-context.md

### Step 3: Integrate into execute-project (45 min)
- [ ] Add resume update calls at task completion
- [ ] Add resume update calls at section completion
- [ ] Update execute-project/SKILL.md documentation
- [ ] Add examples to references/workflow.md

### Step 4: Testing (30 min)
- [ ] Test resume updates during normal execution
- [ ] Test resume survives compaction (manual trigger)
- [ ] Verify next session continues from correct point
- [ ] Performance check (updates should be <100ms)

### Step 5: Migration (15 min)
- [ ] Update existing projects to new resume template
- [ ] Run migration script on all 20+ projects
- [ ] Verify no data loss

---

## Success Criteria

**✅ Optimized Template**:
- Resume-context.md is <50 lines (down from 500+)
- YAML frontmatter only + minimal footer
- No validation gate or session history

**✅ Auto-Updates Work**:
- Resume updates automatically at task/section completion
- `current_task`, `tasks_completed` always accurate
- `last_updated` timestamp current

**✅ Seamless Resume**:
- After compaction, AI continues from correct task
- No need to ask "where were we?"
- Zero friction continuation

---

## Testing Plan

### Test 1: Normal Execution with Updates
1. Start execute-project on existing project
2. Complete 3 tasks
3. Verify resume-context.md updated after each task
4. Check timestamps are current
5. Check task counters are accurate

### Test 2: Compaction Resume
1. Manually trigger compaction (clear conversation)
2. SessionStart hook fires
3. Verify resume-context.md loaded correctly
4. Verify AI continues from last completed task
5. No questions asked, immediate continuation

### Test 3: Performance
1. Time resume update operation
2. Should be <100ms per update
3. No blocking during execution

---

## Open Questions

1. **Update frequency**: After every task or only after sections?
   - **Recommendation**: Every task (more accurate, minimal cost)

2. **Backup strategy**: Should we keep .backup files?
   - **Recommendation**: No - git handles versioning

3. **Migration timing**: Update all projects now or gradually?
   - **Recommendation**: All at once with script (consistent state)

4. **Error handling**: What if resume update fails mid-execution?
   - **Recommendation**: Log error, continue execution (non-blocking)

---

## Next Steps

1. Review this plan with user
2. Get approval on template optimization approach
3. Implement Step 1 (optimize template)
4. Implement Step 2 (update helper)
5. Integrate into execute-project (Step 3)
6. Test thoroughly (Step 4)
7. Run migration (Step 5)

---

**Status**: Ready for implementation pending user approval
