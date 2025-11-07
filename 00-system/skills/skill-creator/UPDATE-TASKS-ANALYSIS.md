# update-tasks Skill Optimization Analysis

**Date**: 2025-11-03
**Current Status**: 70% Compliant (Quick Template Integration Needed)

---

## Current Structure

```
update-tasks/
└── SKILL.md (82 lines, 1,671 bytes)
```

**No references/, no scripts/, no assets/** - Pure, simple skill!

---

## Compliance Analysis

### ✅ What's Excellent

- [x] SKILL.md WELL under 500 limit (82 lines = 84% under!)
- [x] Proper YAML frontmatter (name + description only)
- [x] Clear description with triggers ("update tasks", "check off tasks")
- [x] One-line purpose statement
- [x] Clear workflow (4 steps)
- [x] Simple and focused
- [x] No TOCs needed (file is <100 lines)
- [x] No references needed (simple workflow)

### ⚠️ Needs Improvement

1. **No TodoWrite Integration** (NEW TEMPLATE REQUIREMENT)
   - Missing Step 1: Initialize TodoList
   - Current workflow starts at "Step 1: Load Current Project"
   - Need to insert TodoWrite step and renumber

2. **No close-session Final Step** (NEW TEMPLATE REQUIREMENT)
   - Missing final step auto-trigger
   - Should ensure progress is saved

### Compliance Score

**Before**: 70% (excellent structure, missing new template requirements)
**After**: 100% (add TodoWrite + close-session)

---

## Step 1: Understanding with Concrete Examples

### Example 1: User Mid-Session Update
```
User: "update tasks"
System: "Checking current project..."
  1. Loads project-map.md "Current Focus"
  2. Shows first 10 unchecked tasks
  3. User: "1, 3, 5"
  4. System checks off tasks 1, 3, 5
  5. Displays new progress: "15/20 (75%)"
  6. Asks: "Update more?"
  7. User: "no"
Result: "Tasks updated! ✅"
```

### Example 2: Project Completion
```
User: "mark tasks complete"
System: "Checking current project..."
  1. Shows last 2 unchecked tasks
  2. User: "1, 2"
  3. System checks off both
  4. Displays: "20/20 (100%)"
  5. Suggests: "archive project [name]"
Result: "Project complete! 🎉"
```

### Example 3: No Active Project
```
User: "check off tasks"
System: "No active project. Say 'work on [project]' first."
Result: Graceful exit
```

### Key Features Identified
1. **Mid-Session Updates**: Unlike close-session, doesn't require session end
2. **Interactive Selection**: Shows 10 tasks, user picks by number
3. **Progress Tracking**: Auto-calculates from checkboxes
4. **Iterative**: Can update multiple times in a session
5. **Lightweight**: No map regeneration (that's close-session's job)
6. **Motivation**: Immediate feedback on progress

---

## Step 2: Planning Reusable Contents

### Scripts (None Needed)
- **Decision**: No scripts
- **Reason**: Simple file reads and checkbox updates
- **All logic in Claude**: No deterministic code needed

### References (None Needed)
- **Decision**: No references
- **Reason**: Workflow is only 82 lines, very straightforward
- **All content in SKILL.md**: No need to split

### Assets (None Needed)
- **Decision**: No assets
- **Reason**: No templates, output files, or images needed

---

## Optimizations to Apply

### 1. Add TodoWrite Step 1 ✅

Insert at beginning of Workflow section:
```markdown
### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Load current project
- [ ] Show unchecked tasks
- [ ] Process user selection
- [ ] Update tasks.md
- [ ] Display progress
- [ ] Close session to save progress
```

**Mark tasks complete as you finish each step.**
```

### 2. Renumber Existing Steps ✅

- Current Step 1 → **Step 2**: Load Current Project
- Current Step 2 → **Step 3**: Show Tasks
- Current Step 3 → **Step 4**: Process Selection
- Current Step 4 → **Step 5**: Show Progress

### 3. Add close-session Final Step ✅

Add at end of Workflow section:
```markdown
### Final Step: Close Session

**Automatically trigger the close-session skill**:
```
Auto-triggering close-session to save progress...
```

This ensures task updates are saved to memory and maps are updated.
```

---

## Optimized Structure

```
update-tasks/
└── SKILL.md (~105 lines, with TodoWrite and close-session)
```

**Estimated**: ~105 lines (still well under 500 limit!)

---

## Comparison

### Before (70% Compliant)
```
update-tasks/
└── SKILL.md (82 lines)
    ├── ✅ Good structure
    ├── ✅ Clear workflow
    ├── ❌ No TodoWrite
    └── ❌ No close-session
```

### After (100% Compliant)
```
update-tasks/
└── SKILL.md (~105 lines)
    ├── ✅ Good structure
    ├── ✅ Clear workflow
    ├── ✅ TodoWrite Step 1
    └── ✅ close-session final step
```

**Compliance Score**: 70% → 100% ✅

---

## Next Steps

1. ✅ Analysis complete
2. ⬜ Add TodoWrite Step 1 to SKILL.md
3. ⬜ Renumber existing steps (1-4 → 2-5)
4. ⬜ Add close-session final step
5. ⬜ Verify line count under 500
6. ⬜ Test (manual walkthrough)
7. ⬜ Mark complete

---

**Ready to proceed with optimization!**

**Note**: This is the SIMPLEST optimization yet - just template integration, no restructuring needed. Skill is already well-designed at 82 lines.

**Estimated Time**: 10-15 minutes
