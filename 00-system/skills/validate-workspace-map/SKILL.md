---
name: validate-workspace-map
description: Validate workspace-map.md accuracy against actual 04-workspace/ structure
trigger: User says "validate workspace map", "check workspace map", or from close-session
---

# Validate Workspace Map

Ensure workspace-map.md stays synchronized with actual 04-workspace/ folder structure.

## Purpose

The workspace-map.md file helps AI understand your custom folder organization in 04-workspace/. When it becomes stale (folders added/removed but not documented), AI navigation becomes unreliable.

This skill:
- Compares actual folders with documented folders
- Identifies mismatches (missing or extra folders)
- Guides you through updates
- Validates accuracy

**When to use**:
- You reorganized 04-workspace/ folders
- You notice AI can't find your folders
- During onboarding (Project 03, Task 5.6)
- As part of regular maintenance

---

## Workflow

### Step 1: Scan Actual Workspace Structure

**List all folders in 04-workspace/**:
```bash
ls -d 04-workspace/*/
```

**Store**: ACTUAL_FOLDERS = ["Clients/", "Templates/", "Research/"]

**Exclude**:
- Hidden folders (starting with .)
- Files (only directories)
- workspace-map.md itself

**Time**: 5 seconds

---

### Step 2: Parse workspace-map.md

**Read**: 04-workspace/workspace-map.md

**Extract documented folders**:
- Look in "Your Workspace Structure" section
- Look in "Folder Descriptions" section
- Parse folder names from tree structure and descriptions

**Store**: MAPPED_FOLDERS = ["Clients/", "Templates/", "Research/"]

**Time**: 5 seconds

---

### Step 3: Compare Structures

**Compare**: ACTUAL_FOLDERS vs MAPPED_FOLDERS

**Identify**:
- **Missing from map**: Folders that exist but aren't documented
- **Extra in map**: Folders documented but don't exist (stale entries)
- **Perfect match**: All folders accounted for

**Time**: 2 seconds

---

### Step 4: Report Results

#### If Perfect Match ✅

```
✅ workspace-map.md is accurate!

All 04-workspace/ folders are properly documented:
• Clients/
• Templates/
• Research/

No action needed.
```

**Time**: 5 seconds
**Exit**: Skill complete

---

#### If Mismatches Found ⚠️

```
⚠️ workspace-map.md needs updating

Discrepancies found:

Missing from map (exist but not documented):
• Projects/
• Notes/

Extra in map (documented but don't exist):
• OldClients/ (stale entry)

Would you like me to help update workspace-map.md now?

Options:
• "yes" - Update now (interactive, 2-3 min)
• "no" - Skip for now
• "later" - Remind me next session
```

**Wait for user response**

**Time**: 10 seconds

---

### Step 5: Update workspace-map.md (If user says "yes")

#### For each MISSING folder:

```
I see you have a "Projects/" folder in 04-workspace/.

What should I note about this folder? (1-2 sentences)
> [User describes purpose]
```

**Capture**: Folder description
**Time**: 30 seconds per folder

---

#### For each EXTRA folder:

```
"OldClients/" is documented in workspace-map.md but doesn't exist anymore.

I'll remove it from the map.
```

**Action**: Remove stale entry
**Time**: 5 seconds per folder

---

#### Update the file:

**1. Update "Your Workspace Structure" section**:
```markdown
04-workspace/
├── Clients/
├── Templates/
├── Research/
├── Projects/        # NEW
└── Notes/           # NEW
```

**2. Add "Folder Descriptions"**:
```markdown
### Projects/
[User-provided description]
- [Additional details if provided]

### Notes/
[User-provided description]
- [Additional details if provided]
```

**3. Remove stale entries**:
- Delete entire section for OldClients/

**4. Update timestamp**:
```markdown
**Last Updated**: 2024-03-15 14:30:00
```

**Time**: 30 seconds

---

#### Validate Update:

**Re-read**: workspace-map.md
**Re-scan**: 04-workspace/
**Re-compare**: Verify perfect match

**Display**:
```
✅ workspace-map.md updated and validated!

Updated sections:
• Added: Projects/, Notes/
• Removed: OldClients/ (stale)

workspace-map.md now accurately reflects your 04-workspace/ structure.
```

**Time**: 10 seconds

---

### If User Says "no" or "later":

```
Noted! workspace-map.md needs updating.

To update later, say:
• "validate workspace map"
• Or run this skill manually

Remember: Accurate workspace-map.md helps me navigate your folders correctly.
```

**Time**: 5 seconds

---

## Total Time

- **Perfect match**: ~12 seconds
- **With updates**: 2-4 minutes (depends on number of folders)

---

## Integration

### close-session Integration

This skill is automatically triggered during close-session (Step 5b). See:
- [close-session workflow.md](../close-session/references/workflow.md#step-5b-validate-workspace-mapmd-new---auto-validate)

**Automatic behavior**:
- close-session calls this skill
- If perfect match: Silent (no output)
- If mismatches: Prompts user to update

---

## Technical Notes

### Folder Detection

**Include**:
- All directories in 04-workspace/
- Visible folders only

**Exclude**:
- Hidden folders (., .., .git, etc.)
- Files (workspace-map.md, README.md, etc.)
- System folders

### Parsing workspace-map.md

**Look for folder mentions in**:
1. Tree structure (lines with `├──`, `└──`)
2. Folder descriptions (lines starting with `###`)
3. Any section mentioning folder names with `/` suffix

**Edge cases**:
- Handle empty workspace (no folders)
- Handle missing workspace-map.md (create template)
- Handle malformed workspace-map.md (rebuild)

### Error Handling

**Missing workspace-map.md**:
```
⚠️ workspace-map.md not found!

Creating template workspace-map.md...
[Create from template]
✅ Created! Now documenting your existing folders...
```

**Empty 04-workspace/**:
```
✅ 04-workspace/ is empty

No folders to validate. workspace-map.md is accurate.
```

---

## Best Practices

**For Users**:
- Run this after reorganizing folders
- Keep descriptions brief (1-2 sentences)
- Update immediately (while folder purpose is fresh)

**For AI**:
- Always validate before claiming "workspace organized"
- If map is stale, fix it immediately
- Don't assume folder structure—verify

---

## Example Session

```
You: "validate workspace map"

AI: Validating workspace-map.md...

⚠️ workspace-map.md needs updating

Discrepancies found:

Missing from map (exist but not documented):
• Projects/

Extra in map (documented but don't exist):
• OldClients/

Would you like me to help update workspace-map.md now?
> yes

I see you have a "Projects/" folder in 04-workspace/.
What should I note about this folder?
> Active client projects and deliverables

"OldClients/" is documented but doesn't exist. I'll remove it.

✅ workspace-map.md updated and validated!

Updated sections:
• Added: Projects/ (Active client projects and deliverables)
• Removed: OldClients/ (stale)

workspace-map.md now accurately reflects your 04-workspace/ structure.
```

---

**Remember**: Accurate workspace-map.md = Reliable AI navigation!
