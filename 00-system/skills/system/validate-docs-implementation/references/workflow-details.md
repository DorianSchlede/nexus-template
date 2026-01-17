# Detailed Validation Workflow

This document provides expanded guidance for each step of the validation workflow.

---

## Pre-Validation: Scope Definition

Before starting validation, clarify with the user:

1. **What implementation to validate?**
   - Specific script/file (e.g., "init_build.py")
   - Entire module/system (e.g., "plan-build skill")
   - Recent changes (e.g., "the refactor I just did")

2. **What documentation scope?**
   - System-wide (00-system/)
   - Specific subsystem (skills/, documentation/)
   - User-facing only vs all docs

3. **What level of thoroughness?**
   - Quick scan (major mismatches only)
   - Comprehensive (all references)
   - Critical path only (user-facing docs)

**Example Dialog**:
```
User: "Check if the docs match init_build.py"
AI: "I'll validate init_build.py against all system documentation (00-system/).
     Should I also check user-facing docs like README and guides?"
User: "Yes, check everything"
AI: "Got it - comprehensive validation across all docs. Starting now..."
```

---

## Step 1 Expanded: Implementation Analysis

### What to Extract

For **scripts** (Python/Bash/etc.):
- Functions and their signatures
- Files/folders created (paths, names, structure)
- External dependencies called
- Data structures used
- Constants and configuration

For **modules/classes**:
- Public API (exported functions/classes)
- Expected inputs/outputs
- Side effects (file writes, API calls)
- Error conditions

For **workflows/processes**:
- Steps in sequence
- Decision points
- Required inputs
- Outputs produced

### Analysis Template

```markdown
## Implementation Analysis: [file/module name]

### What It Creates
- [List all artifacts: files, folders, data structures]
- [Include counts, names, locations]

### What It Does
- [List all actions/behaviors]
- [Include sequence if relevant]

### What It Requires
- [List dependencies, inputs, prerequisites]

### What It Does NOT Do
- [List things docs might claim but aren't in code]
- [Old features removed]

### Key Details
- [Important constants, configurations]
- [Edge cases, special handling]
```

### Example Analysis

```markdown
## Implementation Analysis: init_build.py

### What It Creates
- 4 directories in build root:
  - 01-planning/
  - 02-resources/
  - 03-working/
  - 04-outputs/

- 3 files in 01-planning/:
  - overview.md (with YAML frontmatter)
  - plan.md (from template)
  - steps.md (from template)

### What It Does
- Auto-assigns next available build ID (scans existing)
- Sanitizes build name (lowercase, hyphens)
- Creates complete folder structure in one operation
- Populates files from embedded templates
- Returns build directory path

### What It Requires
- build-name (string, any format)
- --path flag (directory where to create)

### What It Does NOT Do
- Does NOT create design.md (old name)
- Does NOT create tasks.md (old name)
- Does NOT create requirements.md (never existed)
- Does NOT create only 3 files (creates 4 dirs + 3 files)

### Key Details
- ID format: Zero-padded 2-digit (01, 02, ..., 10, 11)
- Templates embedded in script (lines 27-253)
- Error handling: Exits if directory exists
```

---

## Step 2 Expanded: Documentation Search

### Search Strategy

**Pattern Matching**:
- Use regex for flexible matching: `design\.md` matches "design.md" but not "designed"
- Search for variations: `(design|tasks|requirements)\.md`
- Include plurals and possessives if relevant

**Search Locations** (priority order):
1. **Core system docs** (highest priority):
   - `00-system/system-map.md`
   - `00-system/core/orchestrator.md`
   - `00-system/documentation/framework-overview.md`

2. **Skill documentation**:
   - `00-system/skills/*/SKILL.md`
   - `00-system/skills/*/references/*.md`

3. **Related skills**:
   - Skills that reference or use the validated implementation

4. **Examples and tests**:
   - Code comments
   - Test files
   - Example workflows

### Search Commands

**Basic search**:
```bash
grep -r "pattern" path/
```

**Multiple patterns**:
```bash
grep -r "design\.md\|tasks\.md" 00-system/
```

**With line numbers**:
```bash
grep -rn "pattern" path/
```

**Files only** (faster for counting):
```bash
grep -rl "pattern" path/
```

### Organizing Results

Create a tracking table:

| File | Line(s) | Pattern Found | Mismatch Type | Priority |
|------|---------|---------------|---------------|----------|
| system-map.md | 96-99 | "design.md", "tasks.md" | File names | Critical |
| SKILL.md | 110 | "3 core files" | Count | High |
| workflows.md | 301 | "02-working/" | Structure | High |

---

## Step 3 Expanded: Mismatch Categorization

### Mismatch Types

**Type 1: File/Folder Name Mismatch**
- **Symptom**: Docs reference files that don't exist
- **Example**: Docs say "design.md" but code creates "plan.md"
- **Fix**: Replace all instances of old name with new name

**Type 2: Structure Mismatch**
- **Symptom**: Folder structure diagrams don't match reality
- **Example**: Docs show 3 folders, code creates 4
- **Fix**: Update structure diagrams, add missing folders

**Type 3: Count/Quantity Mismatch**
- **Symptom**: Numbers don't add up
- **Example**: "Creates 3 files" but actually creates "4 directories + 3 files"
- **Fix**: Update counts with complete description

**Type 4: Missing Information**
- **Symptom**: Code creates things not mentioned in docs
- **Example**: Code creates "02-resources/" but docs don't mention it
- **Fix**: Add missing information to relevant docs

**Type 5: Obsolete Information**
- **Symptom**: Docs describe features that no longer exist
- **Example**: Docs explain "requirements.md" that was removed
- **Fix**: Remove obsolete sections

**Type 6: Inconsistent Terminology**
- **Symptom**: Same thing called different names in different places
- **Example**: "planning files" vs "core files" vs "template files"
- **Fix**: Standardize terminology across all docs

### Prioritization Matrix

| Impact | User-Facing | Internal Docs | Comments/Tests |
|--------|-------------|---------------|----------------|
| **Breaks workflow** | P0 - Fix now | P1 - Fix today | P2 - Fix soon |
| **Causes confusion** | P1 - Fix today | P2 - Fix soon | P3 - Nice to have |
| **Minor inconsistency** | P2 - Fix soon | P3 - Nice to have | P4 - Optional |

---

## Step 4 Expanded: Systematic Fixing

### Fix Order

1. **Core navigation docs first**:
   - system-map.md
   - orchestrator.md
   - framework-overview.md

2. **Skill documentation next**:
   - Main SKILL.md files
   - Workflow references
   - Schema definitions

3. **Examples and tests last**:
   - Example code
   - Test documentation
   - Comments

### Fix Patterns

**Pattern 1: Simple Substitution**
```markdown
OLD: design.md
NEW: plan.md

Search for: design\.md
Replace with: plan.md
```

**Pattern 2: Structure Update**
```markdown
OLD:
├── 01-planning/
├── 02-working/
└── 03-outputs/

NEW:
├── 01-planning/
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

**Pattern 3: Count + Description**
```markdown
OLD: "Auto-generates 3 core files"

NEW: "Auto-generates 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/) + 3 planning files (overview.md, plan.md, steps.md)"
```

**Pattern 4: Add Missing Info**
```markdown
OLD:
├── 01-planning/
└── 03-outputs/

NEW:
├── 01-planning/
├── 02-resources/  ← ADD THIS
└── 03-outputs/
```

### Verification Checklist

After each fix:
- [ ] Read the edited section to verify it makes sense
- [ ] Check surrounding context for related references
- [ ] Ensure examples/diagrams stay consistent
- [ ] Look for duplicate mentions that also need fixing

---

## Step 5 Expanded: Comprehensive Verification

### Re-Search Strategy

After fixing, verify old terms are gone:

```bash
# Should return NO results
grep -r "design\.md" 00-system/
grep -r "tasks\.md" 00-system/
grep -r "requirements\.md" 00-system/

# Should return results (new terms present)
grep -r "plan\.md" 00-system/
grep -r "steps\.md" 00-system/
```

### Spot-Check Locations

**Critical files to manually review**:
1. Main system map (does structure diagram look right?)
2. Primary skill affected (does workflow make sense?)
3. User-facing getting started docs (can user follow them?)

### Final Report Template

```markdown
## Documentation Validation: [Implementation Name]

**Date**: YYYY-MM-DD
**Scope**: [Brief description]
**Thoroughness**: [Quick/Comprehensive/Critical-path]

---

### Implementation Truth

[Summarize what the code actually does]

Example:
- Creates 4 directories + 3 files
- Uses plan.md and steps.md (not design.md/tasks.md)
- Auto-assigns build IDs

---

### Files Updated

**Total**: N files

1. **[Filename 1]** - [Description of changes]
   - [Specific change 1]
   - [Specific change 2]

2. **[Filename 2]** - [Description of changes]
   - [Specific change 1]

[Continue for all files...]

---

### Mismatch Breakdown

| Type | Count | Examples |
|------|-------|----------|
| File names | N | design.md → plan.md |
| Structure | N | Added 02-resources/ |
| Counts | N | "3 files" → "4 dirs + 3 files" |
| Missing info | N | Added folder descriptions |
| Obsolete | N | Removed requirements.md refs |

**Total Fixes**: N

---

### Verification

✅ Old terms search returns 0 results
✅ Structure diagrams match reality
✅ Counts accurate
✅ Examples consistent
✅ Spot-checks pass

---

### Status

**Documentation Status**: ✅ All docs match implementation

**Recommended Next Steps**:
- [Any follow-up actions]
- [Related validations to consider]
```

---

## Edge Cases & Special Situations

### Backward Compatibility

**Scenario**: Code supports both old and new formats

**Example**: execute-build supports "tasks.md OR steps.md"

**Documentation Approach**:
- Document new format as primary
- Mention backward compatibility: "(also supports legacy tasks.md)"
- Don't update examples to show old format

### Intentional Differences

**Scenario**: Docs deliberately differ from implementation

**Example**: Tutorial uses simplified version for pedagogy

**Documentation Approach**:
- Verify difference is intentional (ask user)
- Add note explaining divergence
- Consider adding "Implementation Note" callout

### Future Changes

**Scenario**: Implementation changing soon

**Example**: Planned refactor will change structure

**Documentation Approach**:
- Fix current mismatch now
- Add TODO comment for upcoming change
- Don't pre-document future implementation

---

## Troubleshooting

### "Can't find all references"

**Solution**: Broaden search patterns
```bash
# Search with more variations
grep -ri "design" 00-system/  # Case-insensitive
grep -r "design\|plan" 00-system/  # Multiple terms
```

### "Too many false positives"

**Solution**: Narrow with context
```bash
# Only match as markdown files
grep -r "design\.md" 00-system/

# Exclude certain directories
grep -r "pattern" 00-system/ --exclude-dir=archive
```

### "Changes feel incomplete"

**Solution**: Check related files
- If you fixed system-map.md, check framework-overview.md
- If you fixed a skill, check related skills
- If you fixed core docs, check examples

---

**Remember**: The goal is documentation that accurately reflects reality, preventing user confusion and wasted time!
