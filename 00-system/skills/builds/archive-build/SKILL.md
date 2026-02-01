---
name: archive-build
description: "archive build, archive [name], move to complete."
---

# Archive Build

Move completed builds to the complete folder for a clean, focused build list.

## Purpose

Archive builds that are:
- 100% complete
- Cancelled or on-hold
- No longer active

Archived builds stay accessible in `02-builds/complete/` but don't clutter your active list.

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Identify build to archive
- [ ] Load and verify build status
- [ ] Confirm archive action
- [ ] Move build to complete
- [ ] Update build-map.md
- [ ] Display success message
- [ ] Close session to save progress
```

**Mark tasks complete as you finish each step.**

### Step 2: Identify Build

**If user specified build** (e.g., "archive 01-build-nexus-v3") → Use that

**If not** → List active builds and ask: "Which build?"

### Step 3: Load & Verify

Load `02-builds/active/{ID}-{name}/01-planning/tasks.md` and overview.md

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

Ask: "Archive {name}? This moves it to 02-builds/complete/. (yes/no)"

**If "no"** → Exit

### Step 5: Archive

1. **Move build**: `02-builds/active/{ID}-{name}/ → 02-builds/complete/{ID}-{name}/`
2. **Update build-map.md**:
   - Remove from Active Builds
   - Add to Completed Builds section
   - Clear Current Focus if this was it
3. **Add archive metadata to overview.md**:
   ```yaml
   archived: 2025-11-02
   ```

### Step 6: Confirm Success

```
[OK] Archived: {name}
Location: 02-builds/complete/{ID}-{name}/
Final progress: X/Y (Z%)

View archived: Say "list complete"
```

### Final Step: Close Session

**Automatically trigger the close-session skill**:
```
Auto-triggering close-session to save progress...
```

This ensures the archive action is saved to memory and build-map.md is properly updated.

---

## Additional Commands

**"list complete"** → Scan 02-builds/complete/ and display all completed builds

**"restore [build]"** → Move build back from 02-builds/complete/ to 02-builds/active/

---

## Notes

- Archive ≠ Delete (all files preserved)
- Keeps active list focused
- Can restore anytime

---

**Clean list = clear mind!**
