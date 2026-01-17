# Complete Validation Workflow

## Table of Contents

- [Step 1: Initialize TodoList](#step-1-initialize-todolist)
- [Step 2: Check Core Files](#step-2-check-core-files)
- [Step 3: Check Folder Structure](#step-3-check-folder-structure)
- [Step 4: Check Memory Files](#step-4-check-memory-files)
- [Step 5: Check Navigation Files](#step-5-check-navigation-files)
- [Step 6: Validate Builds](#step-6-validate-builds)
- [Step 7: Validate Skills](#step-7-validate-skills)
- [Step 8: Validate Map Integrity](#step-8-validate-map-integrity-new)
- [Step 9: Run Python Validation Hooks](#step-9-run-python-validation-hooks-new)
- [Step 10: Auto-Fix Issues](#step-10-auto-fix-issues)
- [Step 11: Generate Report](#step-11-generate-report)
- [Step 12: Display Report](#step-12-display-report)
- [Step 13: Auto-Trigger close-session](#step-13-auto-trigger-close-session)

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all validation steps:
- Check core files
- Check folder structure
- Check memory files
- Check navigation files
- Validate builds
- Validate skills
- Validate map integrity
- Run Python hooks (if available)
- Auto-fix issues
- Generate report
- Display report
- Auto-trigger close-session

---

### Step 2: Check Core Files

**Verify existence of critical system files:**

- [ ] `00-system/framework-map.md` exists
- [ ] `00-system/Agents/orchestrator.md` exists
- [ ] `claude.md` exists (root)
- [ ] All `00-system/Skills/*/SKILL.md` files exist

**For each check:**
- IF exists → Mark as ✅ PASS
- IF missing → Mark as ❌ FAIL, add to issues list

**Report format:**
```
Checking core files...
✅ 00-system/framework-map.md
✅ 00-system/Agents/orchestrator.md
✅ claude.md
✅ 00-system/Skills/close-session/SKILL.md
✅ 00-system/Skills/plan-build/SKILL.md
✅ 00-system/Skills/create-skill/SKILL.md
✅ 00-system/Skills/validate-system/SKILL.md
✅ 00-system/Skills/add-integration/SKILL.md
```

**If any failures:**
- Add to issues: "Critical file missing: {file-path}"
- Mark as CRITICAL (cannot auto-fix)

---

### Step 3: Check Folder Structure

**Verify existence of required folders:**

- [ ] `00-system/` exists
- [ ] `00-system/Agents/` exists
- [ ] `00-system/Skills/` exists
- [ ] `Builds/` exists
- [ ] `Skills/` exists (user skills)
- [ ] `Memory/` exists
- [ ] `01-memory/session-reports/` exists
- [ ] `User-Folders/` exists (created during onboarding)

**For each check:**
- IF exists → Mark as ✅ PASS
- IF missing → Mark as ❌ FAIL, add to issues list

**Report format:**
```
Checking folder structure...
✅ 00-system/ folder
✅ 00-system/Agents/ folder
✅ 00-system/Skills/ folder
✅ Builds/ folder
✅ Skills/ folder
✅ Memory/ folder
✅ 01-memory/session-reports/ folder
✅ User-Folders/ folder
```

**If any failures:**
- Add to issues: "Required folder missing: {folder-path}"
- Mark as AUTO-FIXABLE (can recreate empty folder)

---

### Step 4: Check Memory Files

**Verify existence and validity of Memory/ files:**

- [ ] `02-builds/build-map.md` exists and is valid markdown
- [ ] `01-memory/goals.md` exists
- [ ] `01-memory/core-learnings.md` exists

**For each file:**
- IF exists and valid markdown → ✅ PASS
- IF exists but invalid markdown → ❌ FAIL (corrupted)
- IF missing → ⚠️ WARN (system might be uninitialized)

**Report format:**
```
Checking memory files...
✅ 02-builds/build-map.md (valid markdown)
✅ 01-memory/goals.md
✅ 01-memory/core-learnings.md
```

**If any failures:**
- Corrupted file → Add to issues: "Memory file corrupted: {file}"
- Missing file → Add to issues: "Memory file missing: {file}" (might be uninitialized system)

---

### Step 5: Check Navigation Files

**Verify existence and freshness of navigation:**

- [ ] `skill-map.md` exists (root level)
- [ ] `skill-map.md` timestamp is recent (check "Last Updated" line)

**Freshness Check:**
- Extract timestamp from skill-map.md ("Last Updated: YYYY-MM-DD HH:MM:SS")
- Compare to current timestamp
- IF >24 hours old AND Skills/ folder modified since → Mark as STALE

**Report format:**
```
Checking navigation files...
✅ skill-map.md exists
⚠️  skill-map.md is stale (last updated: 2025-10-30, Skills/ modified: 2025-10-31)
```

**If stale:**
- Add to issues: "Navigation stale: skill-map.md"
- Mark as AUTO-FIXABLE (regenerate via close-session)

---

### Step 6: Validate Builds

**Scan Builds/ folder:**

For each folder in `Builds/`:
1. Extract build ID and name from folder name
2. Check required structure:
   - [ ] Has `/planning` folder
   - [ ] Has `/outputs` folder
   - [ ] Has `planning/overview.md`
   - [ ] Has `planning/requirements.md`
   - [ ] Has `planning/design.md`
   - [ ] Has `planning/tasks.md`
3. Check `planning/tasks.md` validity:
   - [ ] Valid markdown syntax
   - [ ] Contains checkbox format: `- [ ]` or `- [x]`
   - [ ] Has at least one task

**Report format:**
```
Validating builds...
Scanning Builds/ folder...

✅ 00-setup-memory
   ✓ /planning folder
   ✓ /outputs folder
   ✓ All planning files present
   ✓ tasks.md valid (15 tasks)

✅ 05-website-development
   ✓ /planning folder
   ✓ /outputs folder
   ✓ All planning files present
   ✓ tasks.md valid (8 tasks)

❌ 06-client-outreach
   ✓ /planning folder
   ✓ /outputs folder
   ✗ Missing: planning/tasks.md

Total builds scanned: 3
Issues found: 1
```

**If any failures:**
- Missing folder → Add to issues: "Build {ID}-{name} missing {folder}"
- Missing file → Add to issues: "Build {ID}-{name} missing {file}"
- Invalid tasks.md → Add to issues: "Build {ID}-{name} has invalid tasks.md"
- Mark as FIXABLE (can regenerate template or guide user)

---

### Step 7: Validate Skills

**Scan Skills/ folder:**

For each folder in `Skills/`:
1. Extract skill name from folder name
2. Check required structure:
   - [ ] Has `SKILL.md` file
   - [ ] `SKILL.md` is valid markdown
   - [ ] `SKILL.md` has "# {Name}" H1 title
   - [ ] `SKILL.md` has "## Purpose" section
   - [ ] `SKILL.md` has "## Workflow" section
   - [ ] `SKILL.md` workflow ends with close-session step
   - [ ] `SKILL.md` does NOT have YAML frontmatter (`---` at top)
3. Check optional resources:
   - Note if `/scripts` folder exists
   - Note if `/references` folder exists
   - Note if `/assets` folder exists

**Report format:**
```
Validating skills...
Scanning Skills/ folder...

✅ weekly-status-report
   ✓ SKILL.md exists
   ✓ Valid format (no YAML frontmatter)
   ✓ Has required sections
   ✓ Ends with close-session
   ✓ Has /references folder

✅ client-proposal-generator
   ✓ SKILL.md exists
   ✓ Valid format (no YAML frontmatter)
   ✓ Has required sections
   ✓ Ends with close-session

❌ analyze-data
   ✓ SKILL.md exists
   ✗ Invalid format: Has YAML frontmatter (NOT ALLOWED!)
   ✓ Has required sections

⚠️  Skills/ folder is empty
   → No user skills yet. Run create-skill to add one!

Total skills scanned: 2
Issues found: 1
```

**If any failures:**
- Missing SKILL.md → Add to issues: "Skill {name} missing SKILL.md"
- Invalid format → Add to issues: "Skill {name} has invalid SKILL.md format"
- YAML frontmatter → Add to issues: "Skill {name} has YAML frontmatter (not allowed)"
- Missing sections → Add to issues: "Skill {name} missing required sections"

---

### Step 8: Validate Map Integrity (NEW)

**Check skill-map.md accuracy:**

1. **Load skill-map.md** and extract all listed skills
2. **Scan Skills/ folder** and get all actual skill folders
3. **Compare:**
   - [ ] All Skills/ folders are listed in skill-map.md
   - [ ] All skills in skill-map.md exist in Skills/
   - [ ] No dead links or references

**Check 02-builds/build-map.md accuracy:**

1. **Load 02-builds/build-map.md** and extract all listed builds
2. **Scan Builds/ folder** and get all actual build folders
3. **Compare:**
   - [ ] All Builds/ folders are listed in 02-builds/build-map.md
   - [ ] All builds in 02-builds/build-map.md exist in Builds/
   - [ ] No dead links or references

**Report format:**
```
Validating map integrity...

skill-map.md:
✅ All 2 skills from Skills/ folder are listed
✅ All 2 skills in skill-map.md exist
✅ No dead links

02-builds/build-map.md:
✅ All 6 builds from Builds/ folder are listed
❌ Build "07-marketing-campaign" listed but folder doesn't exist
✅ No other dead links

Issues found: 1
```

**If any failures:**
- Skill not listed → Add to issues: "Skill {name} exists but not in skill-map.md"
- Skill listed but missing → Add to issues: "Skill {name} in skill-map.md but folder missing"
- Build not listed → Add to issues: "Build {ID}-{name} exists but not in build-map.md"
- Build listed but missing → Add to issues: "Build {ID}-{name} in build-map.md but folder missing"
- Mark as AUTO-FIXABLE (regenerate maps via close-session)

---

### Step 9: Run Python Validation Hooks (NEW)

**Check Python availability:**

Try to run: `python --version`

- IF succeeds → Python available, proceed with hooks
- IF fails → Python not available, gracefully skip with note

**If Python available:**

**Hook 1: validate-structure.py**

Execute: `python 00-system/hooks/validate-structure.py`

- IF script exists:
  - Run script
  - Parse JSON output: `{"valid": true/false, "errors": [...], "warnings": [...]}`
  - Add results to validation report
- IF script doesn't exist:
  - Note: "validate-structure.py not found (optional hook)"

**Hook 2: validate-markdown.py**

Execute: `python 00-system/hooks/validate-markdown.py`

- IF script exists:
  - Run script
  - Parse JSON output: `{"valid": true/false, "errors": [...]}`
  - Add results to validation report
- IF script doesn't exist:
  - Note: "validate-markdown.py not found (optional hook)"

**Hook 3: validate-maps.py**

Execute: `python 00-system/hooks/validate-maps.py`

- IF script exists:
  - Run script
  - Parse JSON output: `{"valid": true/false, "errors": [...]}`
  - Add results to validation report
- IF script doesn't exist:
  - Note: "validate-maps.py not found (optional hook)"

**Report format:**
```
Running Python validation hooks...

✅ Python 3.11.5 detected

validate-structure.py:
✅ All folder structures valid
✅ All required files present

validate-markdown.py:
✅ All markdown syntax valid
⚠️  2 warnings:
   - overview.md: line 15: Consider using consistent header levels
   - tasks.md: line 42: Checkbox format inconsistent (use - [ ] not -[ ])

validate-maps.py:
❌ Map integrity issues:
   - skill-map.md: Missing entry for "new-skill-name"
   - build-map.md: Outdated progress for "05-website-development"

Python hooks complete.
Errors from hooks: 1
Warnings from hooks: 2
```

**If Python not available:**
```
Running Python validation hooks...

⚠️  Python not detected
   Python hooks skipped (optional feature)
   Install Python 3.x to enable automated validation

Python hooks skipped.
```

**If hook execution fails:**
- Catch error gracefully
- Report: "Hook {name} failed: {error message}"
- Continue with other hooks
- Add to issues list

---

### Step 10: Auto-Fix Issues

**Review all issues collected:**

For each issue, determine if auto-fixable:

**AUTO-FIXABLE Issues:**

1. **Stale navigation (skill-map.md)**
   - Fix: Trigger close-session map update step
   - Display: "Regenerating skill-map.md..."
   - Result: "✓ skill-map.md regenerated"

2. **Missing Memory/ files**
   - Fix: Create empty template from standard template
   - Display: "Recreating Memory/{file}..."
   - Result: "✓ Memory/{file} created from template"

3. **Missing folders**
   - Fix: Create empty folder
   - Display: "Creating {folder}..."
   - Result: "✓ {folder} created"

4. **Map integrity issues (missing entries)**
   - Fix: Trigger close-session map update step
   - Display: "Updating maps to include all builds/skills..."
   - Result: "✓ Maps updated"

5. **Build folder missing files**
   - Fix: Create missing file from template
   - Display: "Creating {build}/planning/{file} from template..."
   - Result: "✓ {file} created"

**NOT AUTO-FIXABLE Issues** (require user action):

1. **Critical system files missing** (framework-map, orchestrator, claude.md)
   - Report: Cannot auto-fix, system corrupted
   - Suggest: Restore from backup or reinstall

2. **Corrupted tasks.md** (invalid syntax)
   - Report: Cannot auto-fix, user edits required
   - Suggest: Check {build}/planning/tasks.md for syntax errors

3. **YAML frontmatter in SKILL.md**
   - Report: Cannot auto-fix, user must remove manually
   - Suggest: Edit {skill}/SKILL.md and remove `---` at top

4. **Python hook errors**
   - Report: Hook reported issues, see details above
   - Suggest: Review hook output and fix reported issues

**Report format:**
```
Auto-fixing issues...

✓ Fixed: Regenerated stale skill-map.md
✓ Fixed: Created missing 01-memory/core-learnings.md from template
✓ Fixed: Updated build-map.md with missing builds

Cannot auto-fix:
❌ Skill "analyze-data" has YAML frontmatter
   → Action required: Edit Skills/analyze-data/SKILL.md and remove "---" at top

Auto-fix complete.
Fixed: 3 issues
Require manual fix: 1 issue
```

---

### Step 11: Generate Report

**Compile comprehensive report:**

```markdown
# System Validation Report

**Generated**: {YYYY-MM-DD HH:MM:SS}

---
