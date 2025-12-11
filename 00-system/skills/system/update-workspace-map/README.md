# Workspace Map Validation System

## Overview

The workspace-map validation system ensures that [04-workspace/workspace-map.md](../../../04-workspace/workspace-map.md) stays synchronized with the actual folder structure in `04-workspace/`.

**Why this matters:**
- workspace-map.md is the navigation guide for AI
- Stale maps = AI can't find your folders
- Automatic validation = always accurate

## How It Works

### 1. Automatic Validation (Built-in)

Workspace validation runs automatically in **three scenarios**:

#### A. During close-session (Every session end)
- Step 5b of [close-session workflow](../close-session/references/workflow.md#5b-validate-workspace-mapmd)
- Scans 04-workspace/ structure
- Compares against workspace-map.md
- Prompts user if mismatches found
- **Silent if everything matches** ✅

#### B. User-triggered (On-demand)
User says:
- "validate workspace map"
- "check workspace map"
- "workspace validation"

#### C. During onboarding
- Project 03 (System Mastery), Task 5.6
- Teaches users about workspace organization
- Validates initial setup

### 2. Validation Process

The system performs **deep structure analysis**:

```
1. Scan actual workspace
   ├─ List all folders (04-workspace/*/)
   ├─ Scan subfolder structure (2 levels deep)
   └─ Identify key files in each folder

2. Parse workspace-map.md
   ├─ Extract folder tree structure
   ├─ Extract folder descriptions
   └─ Build documented structure

3. Compare structures
   ├─ Missing from map: Folders that exist but aren't documented
   ├─ Extra in map: Documented folders that no longer exist (stale)
   └─ File changes: Important files in each folder

4. Report findings
   ├─ Perfect match: ✅ Silent (no action needed)
   └─ Mismatches: ⚠️ Prompt user to update
```

### 3. Validation Script

**Location:** [scripts/validate-workspace.py](scripts/validate-workspace.py)

**Usage:**
```bash
# Run validation
python 00-system/skills/validate-workspace-map/scripts/validate-workspace.py

# Output: JSON report
{
  "status": "needs_update",
  "comparison": {
    "missing_from_map": ["Projects/", "Notes/"],
    "extra_in_map": ["OldClients/"],
    "perfect_match": false
  },
  "recommendations": [
    "Document 2 new folders: Projects/, Notes/",
    "Remove 1 stale entry: OldClients/"
  ]
}
```

**Features:**
- Scans 2 levels deep (top-level + subfolders)
- Identifies file-level changes
- Excludes hidden folders and system files
- Returns actionable recommendations
- Exit codes: 0 (valid), 1 (needs update), 2 (error)

## Update Workflow

When mismatches are detected:

### Interactive Update (Recommended)

```
⚠️ workspace-map.md needs updating

Discrepancies found:

Missing from map (exist but not documented):
• Projects/
• Notes/

Extra in map (documented but don't exist):
• OldClients/

Would you like me to help update workspace-map.md now?
> yes

[AI guides you through documenting each folder]
[AI removes stale entries]
[AI validates the updated map]

✅ workspace-map.md updated and validated!
```

### Manual Update

1. Open [04-workspace/workspace-map.md](../../../04-workspace/workspace-map.md)
2. Add missing folders to tree structure
3. Add folder descriptions (1-2 sentences each)
4. Remove stale folder entries
5. Update "Last Updated" timestamp
6. Run validation again to confirm

## Best Practices

### For Users

1. **Run validation after reorganizing** - Whenever you add/remove folders
2. **Update immediately** - Document while folder purpose is fresh in mind
3. **Keep descriptions brief** - 1-2 sentences per folder
4. **Let close-session handle it** - Automatic validation catches most issues

### For AI

1. **Always validate before claiming "workspace organized"**
2. **If map is stale, fix it immediately** - Don't proceed with stale data
3. **Don't assume folder structure** - Always verify
4. **Silent validation** - No output if everything is accurate

## Integration Points

### 1. close-session Skill
- **Step 5b**: Automatic validation
- **Silent mode**: No output if perfect match
- **Interactive mode**: Prompts user if mismatches found
- **Location**: [close-session/references/workflow.md](../close-session/references/workflow.md)

### 2. Orchestrator
- **Smart routing**: Uses workspace-map for folder navigation
- **Proactive suggestions**: Suggests validation if AI detects folder issues
- **Location**: [00-system/core/orchestrator.md](../../core/orchestrator.md)

### 3. Onboarding
- **Project 03, Task 5.6**: Initial workspace setup
- **Teaches validation**: Users learn the system
- **Location**: [02-projects/00-onboarding/03-system-mastery/](../../../02-projects/00-onboarding/03-system-mastery/)

## Technical Details

### Folder Detection

**Includes:**
- All visible directories in 04-workspace/
- Subfolder structure (2 levels deep)
- Key files in each folder (first 5 shown)

**Excludes:**
- Hidden folders (., .., .git, .vscode, etc.)
- workspace-map.md itself
- System folders and temp files

### Parsing workspace-map.md

The script uses **three methods** to extract documented folders:

1. **Tree structure** - Matches `├──` and `└──` patterns
2. **Folder headings** - Matches `### FolderName/` patterns
3. **Folder mentions** - Matches any word ending with `/`

This multi-method approach ensures accuracy even if map format varies.

### Error Handling

**Missing workspace-map.md:**
```
⚠️ workspace-map.md not found!

Creating template workspace-map.md...
✅ Created! Now documenting your existing folders...
```

**Empty 04-workspace/:**
```
✅ 04-workspace/ is empty

No folders to validate. workspace-map.md is accurate.
```

**Permission errors:**
- Folders without read access are skipped
- Validation continues with accessible folders
- Error is logged in report

## Example Session

```
User: "validate workspace map"

AI: Validating workspace-map.md...

⚠️ workspace-map.md needs updating

Discrepancies found:

Missing from map (exist but not documented):
• Projects/

Extra in map (documented but don't exist):
• OldClients/

Would you like me to help update workspace-map.md now?

User: "yes"

AI: I see you have a "Projects/" folder in 04-workspace/.
    What should I note about this folder?

User: "Active client projects and deliverables"

AI: "OldClients/" is documented but doesn't exist. I'll remove it.

    ✅ workspace-map.md updated and validated!

    Updated sections:
    • Added: Projects/ (Active client projects and deliverables)
    • Removed: OldClients/ (stale)

    workspace-map.md now accurately reflects your 04-workspace/ structure.
```

## Future Enhancements

Potential improvements:

1. **File-level tracking** - Track key files within folders
2. **Subfile folder depth** - Configurable scan depth (currently 2 levels)
3. **Auto-description** - AI-generated folder descriptions based on contents
4. **Change history** - Track workspace-map changes over time
5. **Validation scheduling** - Periodic validation (weekly, monthly)

## Summary

The workspace-map validation system:
- ✅ Runs automatically during close-session
- ✅ Provides deep structure analysis (folders + files)
- ✅ Silent when everything is accurate
- ✅ Interactive when updates needed
- ✅ Ensures AI can always navigate your workspace

**Result:** Your workspace-map is always accurate, and AI can always find your folders.
