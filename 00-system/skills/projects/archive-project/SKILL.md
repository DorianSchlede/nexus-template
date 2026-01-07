---
name: archive-project
description: "archive project, archive [name], move to archived."
---

# Archive Project

Move completed projects to archive for a clean, focused project list.

## Purpose

Archive projects that are:
- 100% complete
- Cancelled or on-hold
- No longer active

Archived projects stay accessible but don't clutter your active list.

---

## Workflow

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

### Step 2: Identify Project

**If user specified project** (e.g., "archive 01-build-nexus-v3") → Use that

**If not** → List active projects and ask: "Which project?"

### Step 3: Load & Verify

Load `02-projects/{ID}-{name}/01-planning/tasks.md` and overview.md

Count checkboxes → Calculate progress

Display:
```
Project: {name}
Progress: X/Y tasks (Z%)
Status: {status}

[If <100%] → "Not complete. Archive anyway? (yes/no)"
[If 100%] → "Ready to archive!"
```

### Step 4: Confirm

Ask: "Archive {name}? This moves it to 05-archived/. (yes/no)"

**If "no"** → Exit

### Step 5: Archive

1. **Create 05-archived/ if needed**
2. **Move project**: `02-projects/{ID}-{name}/ → 05-archived/{ID}-{name}/`
3. **Update project-map.md**:
   - Remove from Active Projects
   - Add to Archived Projects section
   - Clear Current Focus if this was it
4. **Add archive metadata to overview.md**:
   ```yaml
   archived: 2025-11-02
   ```

### Step 6: Confirm Success

```
✅ Archived: {name}
Location: 05-archived/{ID}-{name}/
Final progress: X/Y (Z%)

View archived: Say "list archived"
```

### Final Step: Close Session

**Automatically trigger the close-session skill**:
```
Auto-triggering close-session to save progress...
```

This ensures the archive action is saved to memory and project-map.md is properly updated.

---

## Additional Commands

**"list archived"** → Scan 05-archived/ and display all archived projects

**"restore [project]"** → Move project back from 05-archived/ to 02-projects/

---

## Notes

- Archive ≠ Delete (all files preserved)
- Keeps active list focused
- Can restore anytime

---

**Clean list = clear mind!**
