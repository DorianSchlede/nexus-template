# Example Validation Session

This document shows a complete example of the validation workflow in action.

---

## Context

**User Request**: "Does the plan-build SKILL.md comply with the files that the build creation actually creates?"

**Initial Observation**: User noticed a potential mismatch between documentation and implementation.

---

## Step 1: Implementation Analysis

### Read the Implementation

**File analyzed**: `00-system/skills/plan-build/scripts/init_build.py`

**Key findings**:
```python
# Lines 343-377: Creates 4 directories
planning_dir = build_dir / "01-planning"
resources_dir = build_dir / "02-resources"  # ← Note: resources!
working_dir = build_dir / "03-working"
outputs_dir = build_dir / "04-outputs"

# Lines 382-421: Creates 3 files in planning/
overview.md (lines 382-395)
plan.md (lines 397-408)
steps.md (lines 410-421)
```

**Implementation Truth**:
```markdown
[OK] Creates: 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/)
[OK] Creates: 3 files in 01-planning/ (overview.md, plan.md, steps.md)
[ERROR] Does NOT create: design.md, tasks.md, requirements.md (old names)
```

### Check Actual Build Structure

```bash
$ ls -la "02-builds/01-onboarding-ux-improvements"
drwxr-xr-x 1 dsber 197610 0 Nov 23 07:18 01-planning
drwxr-xr-x 1 dsber 197610 0 Nov 23 07:18 02-resources  ← Confirmed!
drwxr-xr-x 1 dsber 197610 0 Nov 23 07:18 03-working
drwxr-xr-x 1 dsber 197610 0 Nov 23 07:18 04-outputs
```

**Verified**: Implementation creates 4 directories as documented in code.

---

## Step 2: Search Documentation

### Search for Old File Names

```bash
$ grep -r "(design\.md|tasks\.md)" 00-system/
```

**Results**: 31 files found with references to old file names

**Key files identified**:
- `00-system/skills/plan-build/SKILL.md` (multiple refs)
- `00-system/system-map.md` (structure diagram)
- `00-system/documentation/framework-overview.md` (examples)
- `00-system/skills/plan-build/references/workflows.md` (workflow steps)
- `00-system/skills/plan-build/references/build-schema.yaml` (comments)
- `00-system/core/orchestrator.md` (loading pattern)

### Search for Old Folder Structure

```bash
$ grep -r "(02-working|03-outputs)" 00-system/
```

**Results**: References to old folder numbering scheme found

**Finding**: Documentation showed `02-working/` and `03-outputs/` but actual structure is:
- `02-resources/` (missing from docs!)
- `03-working/` (off by one)
- `04-outputs/` (off by one)

---

## Step 3: Categorize Mismatches

### Mismatch Summary

| File | Issue | Type | Priority |
|------|-------|------|----------|
| SKILL.md | "3 core files" | Count | Critical |
| SKILL.md | Missing directory mention | Missing info | Critical |
| system-map.md | Shows design.md, tasks.md | File names | Critical |
| system-map.md | Missing 02-resources/ | Structure | Critical |
| framework-overview.md | "tasks.md" refs | File names | High |
| workflows.md | "design.md" steps | File names | High |
| build-schema.yaml | "tasks.md" in comments | File names | Medium |
| orchestrator.md | Load pattern wrong | File names | High |

**Total**: 6 files with multiple mismatches each

---

## Step 4: Fix All Mismatches

### Fix 1: plan-build/SKILL.md

**Line 15**:
```markdown
OLD: 4. [OK] RUN init_build.py IMMEDIATELY (creates 3 planning files)
NEW: 4. [OK] RUN init_build.py IMMEDIATELY (creates 4 directories + 3 planning files)
```

**Line 56**:
```markdown
OLD: - **Script-Generated Structure**: 3 core files (overview, plan, steps) created immediately

NEW: - **Script-Generated Structure**: 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/) + 3 planning files (overview, plan, steps) created immediately
```

**Lines 110-111**:
```markdown
OLD:
- Run `scripts/init_build.py "Build Name" --path 02-builds`
- Auto-generates 3 core files: `overview.md`, `plan.md`, `steps.md`

NEW:
- Run `scripts/init_build.py "Build Name" --path 02-builds`
- Auto-generates 4 directories: `01-planning/`, `02-resources/`, `03-working/`, `04-outputs/`
- Auto-generates 3 planning files in 01-planning/: `overview.md`, `plan.md`, `steps.md`
```

**Lines 244-248**:
```markdown
OLD:
- **init_build.py**: ⚡ NEW! Quick build template generator
  - Auto-generates empty build with all planning files
  - Auto-assigns next available build ID
  - Creates overview.md, plan.md, steps.md from templates

NEW:
- **init_build.py**: ⚡ Quick build template generator
  - Auto-generates build structure with 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/)
  - Auto-assigns next available build ID
  - Creates 3 planning files in 01-planning/: overview.md, plan.md, steps.md from templates
```

**Result**: 4 fixes in SKILL.md [OK]

---

### Fix 2: system-map.md

**Lines 94-100** (structure diagram):
```markdown
OLD:
│   └── {ID}-{name}/                # User builds
│       ├── 01-planning/
│       │   ├── overview.md         # YAML metadata
│       │   ├── design.md
│       │   └── tasks.md            # Checkbox list (state source)
│       ├── 02-working/
│       └── 03-outputs/

NEW:
│   └── {ID}-{name}/                # User builds
│       ├── 01-planning/
│       │   ├── overview.md         # YAML metadata
│       │   ├── plan.md
│       │   └── steps.md            # Checkbox list (state source)
│       ├── 02-resources/           # Reference materials
│       ├── 03-working/             # Work-in-progress files
│       └── 04-outputs/             # Final deliverables
```

**Line 132**:
```markdown
OLD: - **State**: Checkbox tasks in `tasks.md`
NEW: - **State**: Checkbox tasks in `steps.md`
```

**Line 182**:
```markdown
OLD: **Note**: `tasks_total`, `tasks_completed`, `progress` auto-calculated from tasks.md
NEW: **Note**: `tasks_total`, `tasks_completed`, `progress` auto-calculated from steps.md
```

**Result**: 3 major fixes in system-map.md [OK]

---

### Fix 3: framework-overview.md

**Lines 292-293**:
```markdown
OLD:
Read: {build}/01-planning/overview.md
Read: {build}/01-planning/design.md
Read: {build}/01-planning/tasks.md

NEW:
Read: {build}/01-planning/overview.md
Read: {build}/01-planning/plan.md
Read: {build}/01-planning/steps.md
```

**Lines 538-539**:
```markdown
OLD:
  - 02-builds/05-website-development/01-planning/overview.md
  - 02-builds/05-website-development/01-planning/requirements.md
  - 02-builds/05-website-development/01-planning/design.md
  - 02-builds/05-website-development/01-planning/tasks.md

NEW:
  - 02-builds/05-website-development/01-planning/overview.md
  - 02-builds/05-website-development/01-planning/plan.md
  - 02-builds/05-website-development/01-planning/steps.md
```

**Additional fixes**: Lines 210, 625, 879, 1045

**Result**: 7 fixes in framework-overview.md [OK]

---

### Fix 4: workflows.md

**Table of Contents** (lines 24-26):
```markdown
OLD:
- [Step 6: INTERACTIVE - requirements.md](#step-6-️-interactive---requirementsmd)
- [Step 7: INTERACTIVE - design.md](#step-7-️-interactive---designmd)
- [Step 8: INTERACTIVE - tasks.md](#step-8-️-interactive---tasksmd)

NEW:
- [Step 6: INTERACTIVE - plan.md](#step-6-️-interactive---planmd)
- [Step 7: INTERACTIVE - steps.md](#step-7-️-interactive---stepsmd)
```

**TodoList template** (lines 239-241):
```markdown
OLD:
- [ ] Fill overview.md
- [ ] Interactive requirements.md (with pause)
- [ ] Interactive design.md (with pause)
- [ ] Interactive tasks.md (with pause)

NEW:
- [ ] Fill overview.md
- [ ] Interactive plan.md (with pause)
- [ ] Interactive steps.md (with pause)
```

**Structure diagram** (lines 295-302):
```markdown
OLD:
Builds/{ID}-{name}/
├── /planning
│   ├── overview.md
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── /outputs
    └── .gitkeep

NEW:
02-builds/{ID}-{name}/
├── 01-planning/
│   ├── overview.md
│   ├── plan.md
│   └── steps.md
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

**Step headers** (lines 427-449):
```markdown
OLD:
## Step 7: [!] INTERACTIVE - design.md
...
## Step 8: [!] INTERACTIVE - tasks.md

NEW:
## Step 6: [!] INTERACTIVE - plan.md
...
## Step 7: [!] INTERACTIVE - steps.md
```

**Result**: 8 fixes in workflows.md [OK]

---

### Fix 5: build-schema.yaml

**Lines 21-24**:
```markdown
OLD:
calculated:
  - tasks_total: int            # Counted from checkboxes in tasks.md
  - tasks_completed: int        # Counted from [x] in tasks.md
  - progress: float             # Calculated as completed / total (0.0-1.0)
  - current_task: string        # First unchecked [ ] task in tasks.md

NEW:
calculated:
  - tasks_total: int            # Counted from checkboxes in steps.md
  - tasks_completed: int        # Counted from [x] in steps.md
  - progress: float             # Calculated as completed / total (0.0-1.0)
  - current_task: string        # First unchecked [ ] task in steps.md
```

**Lines 38-40**:
```markdown
OLD:
  # Note: tasks_total, tasks_completed, progress, and current_task are
  # calculated by nexus-loader from tasks.md checkboxes. Do NOT include
  # them in YAML - they're automatically added to loader output!

NEW:
  # Note: tasks_total, tasks_completed, progress, and current_task are
  # calculated by nexus-loader from steps.md checkboxes. Do NOT include
  # them in YAML - they're automatically added to loader output!
```

**Result**: 2 fixes in build-schema.yaml [OK]

---

### Fix 6: orchestrator.md

**Lines 284-286**:
```markdown
OLD:
Read: {build}/01-planning/overview.md
Read: {build}/01-planning/design.md
Read: {build}/01-planning/tasks.md

NEW:
Read: {build}/01-planning/overview.md
Read: {build}/01-planning/plan.md
Read: {build}/01-planning/steps.md
```

**Result**: 1 fix in orchestrator.md [OK]

---

## Step 5: Verification

### Re-search for Old Terms

```bash
$ grep -r "design\.md" 00-system/
# No results [OK]

$ grep -r "tasks\.md" 00-system/
# Only in execute-build (intentional backward compatibility) [OK]

$ grep -r "requirements\.md" 00-system/
# No results [OK]

$ grep -r "02-working" 00-system/
# No results [OK]

$ grep -r "03-outputs" 00-system/
# No results [OK]
```

**Verification**: All old terms successfully removed! [OK]

---

### Spot Checks

**system-map.md structure**:
- Shows 4 directories [OK]
- Includes 02-resources/ [OK]
- Uses plan.md and steps.md [OK]
- Descriptions match reality [OK]

**SKILL.md workflow**:
- Mentions 4 directories + 3 files [OK]
- Lists all directory names [OK]
- No references to old names [OK]

**framework-overview.md examples**:
- All examples use new names [OK]
- Loading patterns updated [OK]
- Consistent terminology [OK]

---

## Final Report

```markdown
## [OK] All References Fixed!

### Files Updated: 6

1. **00-system/skills/plan-build/SKILL.md** - Core skill documentation
   - Line 15: Updated mandatory step description
   - Line 56: Updated key features
   - Lines 110-111: Updated step 1 workflow
   - Lines 244-248: Updated script description

2. **00-system/system-map.md** - System navigation hub
   - Lines 94-100: Updated build structure diagram
   - Line 132: Changed tasks.md → steps.md reference
   - Line 182: Updated YAML note

3. **00-system/documentation/framework-overview.md** - Complete guide
   - Lines 210, 292-293, 538-539: Changed file names
   - Lines 625, 879, 1045: Updated progress tracking refs

4. **00-system/skills/plan-build/references/workflows.md** - Workflow details
   - Lines 24-25: Updated TOC
   - Lines 239-240: Updated TodoList
   - Lines 295-302: Updated structure diagram
   - Lines 427-449: Updated step names

5. **00-system/skills/plan-build/references/build-schema.yaml** - Schema docs
   - Lines 21-24: Updated calculated fields comments
   - Lines 38-40: Updated note

6. **00-system/core/orchestrator.md** - Orchestration logic
   - Lines 284-286: Updated loading pattern

---

### Mismatch Breakdown

| Type | Count | Description |
|------|-------|-------------|
| File names | 12 | design.md → plan.md, tasks.md → steps.md |
| Structure | 8 | Added 02-resources/, renumbered folders |
| Counts | 3 | "3 files" → "4 dirs + 3 files" |

**Total Fixes**: 23

---

### Status

[OK] **Zero grep results** for old/deprecated terms
[OK] **All structure diagrams** match actual folder structure
[OK] **All counts** accurate and complete
[OK] **All file references** use current names
[OK] **Spot-checks** pass

**Documentation Status**: [OK] All docs match implementation
```

---

## Key Takeaways

### What Made This Successful

1. **Started with implementation truth**: Read the code first, not the docs
2. **Exhaustive search**: Used grep to find ALL references, not just obvious ones
3. **Systematic fixing**: Fixed files in priority order (core docs → skill docs → references)
4. **Tracked progress**: Used TodoWrite to show user what was happening
5. **Verified thoroughly**: Re-searched to confirm old terms gone

### Common Patterns Found

- **Count mismatches**: "3 files" should be "4 directories + 3 files"
- **Missing directories**: 02-resources/ not mentioned anywhere
- **Old file names**: design.md, tasks.md throughout docs
- **Structure numbering**: 02-working → 03-working (off by one after adding 02-resources/)

### Time Investment

- **Analysis**: 5 minutes (read script, check structure)
- **Search**: 3 minutes (grep commands in parallel)
- **Categorization**: 2 minutes (organize findings)
- **Fixing**: 15 minutes (6 files, multiple edits each)
- **Verification**: 3 minutes (re-search + spot checks)

**Total**: ~28 minutes for comprehensive validation

---

**Result**: User can now confidently follow documentation knowing it accurately reflects the implementation!
