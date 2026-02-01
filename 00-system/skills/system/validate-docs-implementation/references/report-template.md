# Documentation Validation Report Template

Use this template to generate comprehensive validation reports.

---

## Report Structure

```markdown
# Documentation Validation Report

**Implementation**: [Name of script/module/feature validated]
**Date**: YYYY-MM-DD
**Validation ID**: validation-{implementation-name}-YYYY-MM-DD
**Scope**: [System-wide / Specific subsystem / User-facing only]
**Thoroughness**: [Quick scan / Comprehensive / Critical-path only]

---

## Executive Summary

**Status**: [OK] All documentation matches implementation / [!] Partial fixes / [ERROR] Issues remain

**Key Findings**:
- [Brief 1-sentence summary of what was found]
- [Most significant mismatch discovered]
- [Impact of fixes]

**Actions Taken**:
- Files updated: N
- Total fixes: N
- Verification: [Pass/Fail]

---

## Implementation Analysis

### What the Code Actually Does

[Summarize implementation truth - what files/folders/behavior the code creates]

**Creates**:
- [List all artifacts with counts]
- Example: 4 directories (01-planning/, 02-resources/, 03-working/, 04-outputs/)
- Example: 3 files in 01-planning/ (overview.md, plan.md, steps.md)

**Does NOT Create** (documented but missing):
- [List things docs mentioned but code doesn't create]
- Example: design.md (old name, removed)
- Example: requirements.md (never existed)

**Key Details**:
- [Important implementation notes]
- [Edge cases or special handling]

---

## Search Results

### Patterns Searched

| Pattern | Purpose | Files Found |
|---------|---------|-------------|
| `design\.md` | Old file name | 6 |
| `tasks\.md` | Old file name | 8 |
| `02-working` | Old folder structure | 3 |

### Files Requiring Updates

| File | Priority | Mismatches Found |
|------|----------|------------------|
| system-map.md | Critical | File names, structure |
| SKILL.md | Critical | Counts, missing info |
| framework-overview.md | High | File names, examples |
| workflows.md | High | Structure, steps |
| build-schema.yaml | Medium | Comments |
| orchestrator.md | High | Loading pattern |

**Total Files**: N

---

## Mismatches Identified

### By Type

| Type | Count | Examples |
|------|-------|----------|
| File name mismatch | N | design.md → plan.md, tasks.md → steps.md |
| Structure mismatch | N | Missing 02-resources/, wrong folder numbers |
| Count mismatch | N | "3 files" → "4 directories + 3 files" |
| Missing information | N | 02-resources/ not documented anywhere |
| Obsolete information | N | References to removed requirements.md |
| Inconsistent terminology | N | "planning files" vs "core files" |

**Total Mismatches**: N

### By Impact

| Impact Level | Count | Examples |
|--------------|-------|----------|
| **Critical** (breaks workflow) | N | [Examples] |
| **High** (causes confusion) | N | [Examples] |
| **Medium** (minor inconsistency) | N | [Examples] |
| **Low** (cosmetic) | N | [Examples] |

---

## Fixes Applied

### File-by-File Changes

#### 1. [Filename]

**Location**: `path/to/file`
**Priority**: Critical/High/Medium/Low
**Changes**: N

**Change 1**:
```markdown
Line X:
OLD: [Old text]
NEW: [New text]
Reason: [Why this was changed]
```

**Change 2**:
```markdown
Lines X-Y:
OLD:
[Old text
spanning
multiple lines]

NEW:
[New text
spanning
multiple lines]
Reason: [Why this was changed]
```

[Repeat for all changes in this file]

---

#### 2. [Next filename]

[Same structure as above]

---

[Continue for ALL files updated]

---

## Verification Results

### Re-Search Verification

| Old Term | Expected Result | Actual Result | Status |
|----------|-----------------|---------------|--------|
| `design\.md` | 0 results | 0 results | [OK] Pass |
| `tasks\.md` | 0 results | 0 results | [OK] Pass |
| `requirements\.md` | 0 results | 0 results | [OK] Pass |
| `02-working` | 0 results | 0 results | [OK] Pass |
| `03-outputs` | 0 results | 0 results | [OK] Pass |

**Overall Verification**: [OK] All old terms removed

### Spot Checks

| Location | Check | Result |
|----------|-------|--------|
| system-map.md | Structure diagram accurate | [OK] Pass |
| SKILL.md | Workflow makes sense | [OK] Pass |
| framework-overview.md | Examples consistent | [OK] Pass |

**Overall Spot Checks**: [OK] All pass

---

## Statistics

### Change Metrics

- **Files Updated**: N
- **Total Lines Changed**: N
- **Average Changes per File**: N
- **Largest Update**: [Filename] (N changes)

### Time Investment

- Analysis: X minutes
- Search: X minutes
- Categorization: X minutes
- Fixing: X minutes
- Verification: X minutes
- **Total**: ~X minutes

### Coverage

- **Files Scanned**: N
- **Files Needing Updates**: N
- **Update Coverage**: N% (files updated / files scanned)

---

## Status

### Current State

[OK] **Documentation Status**: All documentation matches implementation
- Zero grep results for old/deprecated terms
- All structure diagrams match reality
- All counts accurate
- All file references use current names
- All examples work as documented

### Remaining Issues (if any)

- [ ] [Issue 1]
- [ ] [Issue 2]

---

## Recommendations

### Immediate Next Steps

1. [Action item 1]
2. [Action item 2]

### Future Validations

**Suggested Next Validations**:
- [Related implementation to validate]
- [System to check]

**Validation Frequency**:
- After major refactors: Immediate
- Before releases: Always
- Routine maintenance: Monthly/Quarterly

### Process Improvements

**What Worked Well**:
- [Positive observation]
- [Successful pattern]

**What Could Be Improved**:
- [Suggestion for next time]
- [Process optimization idea]

---

## Appendix

### Search Commands Used

```bash
# File name searches
grep -r "design\.md\|tasks\.md\|requirements\.md" 00-system/

# Folder structure searches
grep -r "02-working\|03-outputs" 00-system/

# Verification searches
grep -r "design\.md" 00-system/  # Should return 0
grep -r "tasks\.md" 00-system/   # Should return 0
```

### Related Files

**Implementation File**:
- `[path/to/implementation.py]`

**Key Documentation Updated**:
- `[path/to/doc1.md]`
- `[path/to/doc2.md]`

**Reference Documentation**:
- [Link to related docs]

---

## Metadata

**Generated By**: validate-docs-implementation skill
**Report Version**: 1.0
**Report Format**: Markdown
**Storage Location**: [Where this report is saved]

---

**End of Report**
```

---

## Usage Notes

### Filling Out the Template

1. **Replace ALL placeholders** in [brackets]
2. **Include specific examples** - don't leave generic text
3. **Be comprehensive** - document every change made
4. **Link to files** - use markdown links so user can click through
5. **Include grep commands** - so validation can be reproduced

### What to Emphasize

**Critical Sections** (must be complete):
- Executive Summary (user reads this first)
- Implementation Analysis (ground truth)
- Fixes Applied (detailed changelog)
- Verification Results (proof it worked)

**Important Sections** (provide context):
- Mismatches Identified (categorization helps future work)
- Statistics (shows scope of validation)
- Recommendations (actionable next steps)

**Optional Sections** (nice to have):
- Appendix (for reproducibility)
- Metadata (for organization)

### Report File Naming

**Format**: `validation-{implementation-name}-YYYY-MM-DD.md`

**Examples**:
- `validation-init-build-2025-11-24.md`
- `validation-create-skill-2025-11-24.md`
- `validation-nexus-loader-2025-11-24.md`
- `validation-system-wide-2025-11-24.md`

**Why this format**:
- Searchable by implementation name
- Chronologically sortable
- Clear purpose (validation report)
- No spaces (filesystem friendly)

### Storage Locations

**Option 1: Workspace (Recommended)**
- Location: `04-workspace/validation-reports/`
- Pros: Organized, searchable, part of user's work
- Cons: Not in version control by default

**Option 2: Memory**
- Location: `01-memory/validation-reports/`
- Pros: Persistent, part of system memory
- Cons: Can clutter memory folder

**Option 3: Custom**
- Location: User-specified
- Pros: Maximum flexibility
- Cons: Needs to be tracked separately

---

## Quick Reference: Minimal Report

For quick validations, use this minimal version:

```markdown
# Validation: [Implementation] - [Date]

## Summary
- Files updated: N
- Total fixes: N
- Status: [OK]

## What Was Fixed
1. [File 1] - [Change summary]
2. [File 2] - [Change summary]

## Verification
[OK] All old terms removed
[OK] Spot checks pass

---
Report: [filename]
```

---

**This template ensures every validation creates a comprehensive, searchable, reproducible record!**
