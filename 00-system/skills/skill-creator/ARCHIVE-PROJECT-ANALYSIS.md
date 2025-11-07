# archive-project Skill Optimization Analysis

**Date**: 2025-11-03
**Current Status**: 70% Compliant (Quick Template Integration Needed)

---

## Current Structure

```
archive-project/
└── SKILL.md (92 lines, 1,910 bytes)
```

**No references/, no scripts/, no assets/** - Another pure, simple skill!

---

## Compliance Analysis

### ✅ What's Excellent

- [x] SKILL.md WELL under 500 limit (92 lines = 82% under!)
- [x] Proper YAML frontmatter (name + description only)
- [x] Clear description with triggers ("archive project", "move to archived")
- [x] One-line purpose statement
- [x] Clear workflow (5 steps)
- [x] Additional commands documented (list archived, restore)
- [x] Simple and focused
- [x] No TOCs needed (file is <100 lines)
- [x] No references needed (simple workflow)

### ⚠️ Needs Improvement

1. **No TodoWrite Integration** (NEW TEMPLATE REQUIREMENT)
   - Missing Step 1: Initialize TodoList
   - Current workflow starts at "Step 1: Identify Project"
   - Need to insert TodoWrite step and renumber

2. **No close-session Final Step** (NEW TEMPLATE REQUIREMENT)
   - Missing final step auto-trigger
   - Should ensure archive action is saved to memory

### Compliance Score

**Before**: 70% (excellent structure, missing new template requirements)
**After**: 100% (add TodoWrite + close-session)

---

## Step 1: Understanding with Concrete Examples

### Example 1: User Archives Complete Project
```
User: "archive 05-website-development"
System: "Loading project..."
  1. Loads tasks.md and overview.md
  2. Calculates: "20/20 tasks (100%)"
  3. Displays: "Ready to archive!"
  4. Asks: "Archive website-development?"
  5. User: "yes"
  6. Creates 05-archived/ folder
  7. Moves project folder
  8. Updates project-map.md
  9. Adds archive metadata to overview.md
  10. Displays success message
Result: "✅ Archived: website-development"
```

### Example 2: Archive Incomplete Project
```
User: "archive project"
System: "Which project?"
User: "03-client-outreach"
System: "Loading project..."
  1. Calculates: "5/15 tasks (33%)"
  2. Displays: "Not complete. Archive anyway?"
  3. User: "yes"
  4. Archives project with metadata
Result: "✅ Archived: client-outreach (incomplete)"
```

### Example 3: List Archived Projects
```
User: "list archived"
System: "Scanning 05-archived/..."
  1. Lists all archived projects
  2. Shows progress and archive date
Result: "Found 3 archived projects"
```

### Example 4: Restore Archived Project
```
User: "restore 01-setup-nexus"
System: "Restoring project..."
  1. Moves from 05-archived/ to 02-projects/
  2. Updates project-map.md
  3. Removes archive metadata
Result: "✅ Restored: setup-nexus"
```

### Key Features Identified
1. **Flexible Selection**: Specify project or select from list
2. **Progress Verification**: Shows completion status before archiving
3. **Confirmation Required**: User must confirm archive action
4. **Non-Destructive**: Files preserved, just moved
5. **Metadata Tracking**: Archive date added to overview.md
6. **Bidirectional**: Can restore archived projects
7. **List View**: Can see all archived projects
8. **Map Integration**: Updates project-map.md automatically

---

## Step 2: Planning Reusable Contents

### Scripts (None Needed)
- **Decision**: No scripts
- **Reason**: Simple folder moves and file updates
- **All logic in Claude**: No deterministic code needed

### References (None Needed)
- **Decision**: No references
- **Reason**: Workflow is only 92 lines, very straightforward
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
- [ ] Identify project to archive
- [ ] Load and verify project status
- [ ] Confirm archive action
- [ ] Move project to archive
- [ ] Update project-map.md
- [ ] Display success message
- [ ] Close session to save progress
```

**Mark tasks complete as you finish each step.**
```

### 2. Renumber Existing Steps ✅

- Current Step 1 → **Step 2**: Identify Project
- Current Step 2 → **Step 3**: Load & Verify
- Current Step 3 → **Step 4**: Confirm
- Current Step 4 → **Step 5**: Archive
- Current Step 5 → **Step 6**: Confirm Success

### 3. Add close-session Final Step ✅

Add after Step 6 and before Additional Commands:
```markdown
### Final Step: Close Session

**Automatically trigger the close-session skill**:
```
Auto-triggering close-session to save progress...
```

This ensures the archive action is saved to memory and project-map.md is properly updated.
```

---

## Optimized Structure

```
archive-project/
└── SKILL.md (~115 lines, with TodoWrite and close-session)
```

**Estimated**: ~115 lines (still well under 500 limit!)

---

## Comparison

### Before (70% Compliant)
```
archive-project/
└── SKILL.md (92 lines)
    ├── ✅ Good structure
    ├── ✅ Clear workflow
    ├── ✅ Additional commands
    ├── ❌ No TodoWrite
    └── ❌ No close-session
```

### After (100% Compliant)
```
archive-project/
└── SKILL.md (~115 lines)
    ├── ✅ Good structure
    ├── ✅ Clear workflow
    ├── ✅ Additional commands
    ├── ✅ TodoWrite Step 1
    └── ✅ close-session final step
```

**Compliance Score**: 70% → 100% ✅

---

## Next Steps

1. ✅ Analysis complete
2. ⬜ Add TodoWrite Step 1 to SKILL.md
3. ⬜ Renumber existing steps (1-5 → 2-6)
4. ⬜ Add close-session final step
5. ⬜ Verify line count under 500
6. ⬜ Test (manual walkthrough)
7. ⬜ Mark complete

---

**Ready to proceed with optimization!**

**Note**: This is another SIMPLE optimization - just template integration, identical pattern to update-tasks. Skill is already well-designed at 92 lines.

**Estimated Time**: 10-15 minutes
