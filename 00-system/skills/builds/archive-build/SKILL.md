---
name: archive-build
description: "archive build, archive [name], move to archived."
---

# Archive Build

Move completed builds to archive for a clean, focused build list.

## Purpose

Archive builds that are:
- 100% complete
- Cancelled or on-hold
- No longer active

Archived builds stay accessible but don't clutter your active list.

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Identify build to archive
- [ ] Load and verify build status
- [ ] Confirm archive action
- [ ] Move build to archive
- [ ] Update build-map.md
- [ ] Display success message
- [ ] Close session to save progress
```

**Mark tasks complete as you finish each step.**

### Step 2: Identify Build

**If user specified build** (e.g., "archive 01-build-nexus-v3") → Use that

**If not** → List active builds and ask: "Which build?"

### Step 3: Load & Verify

Load `02-builds/{ID}-{name}/01-planning/tasks.md` and overview.md

Count checkboxes → Calculate progress

Display:
```
Build: {name}
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
2. **Move build**: `02-builds/{ID}-{name}/ → 05-archived/{ID}-{name}/`
3. **Update build-map.md**:
   - Remove from Active Builds
   - Add to Archived Builds section
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

This ensures the archive action is saved to memory and build-map.md is properly updated.

---

## Additional Commands

**"list archived"** → Scan 05-archived/ and display all archived builds

**"restore [build]"** → Move build back from 05-archived/ to 02-builds/

---

## Notes

- Archive ≠ Delete (all files preserved)
- Keeps active list focused
- Can restore anytime

---

**Clean list = clear mind!**
