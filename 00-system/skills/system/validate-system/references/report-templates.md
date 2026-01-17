# Validation Report Templates

## Table of Contents

- [Summary](#summary)
- [Issues Found](#issues-found)
- [Python Hook Results](#python-hook-results)
- [Recommendations](#recommendations)
- [Next Steps](#next-steps)

---

## Summary

**Status**: [HEALTHY | ISSUES_FOUND | FIXED]

**Checks Performed**:
- ✅ Core files ({X} files)
- ✅ Folder structure ({Y} folders)
- ✅ Memory files ({Z} files)
- ✅ Navigation files ({W} files)
- ✅ Builds validated ({P} builds)
- ✅ Skills validated ({S} skills)
- ✅ Map integrity ({M} maps)
- {✅/⚠️/❌} Python hooks ({H} hooks)

**Results**:
- Total issues found: {N}
- Auto-fixed: {F}
- Require manual fix: {M}
- Warnings: {W}

---

## Issues Found

[IF no issues:]
✅ No issues found! Your system is healthy.

[IF issues found:]
### Critical Issues
{List critical issues that block system operation}

### Fixable Issues (Auto-Fixed)
{List issues that were automatically fixed}

### Issues Requiring Manual Fix
{List issues that need user action}

### Warnings
{List non-blocking warnings}

---

## Python Hook Results

[IF Python available:]
### validate-structure.py
{Results from hook}

### validate-markdown.py
{Results from hook}

### validate-maps.py
{Results from hook}

[IF Python not available:]
⚠️ Python not detected. Hooks skipped (optional feature).

---

## Recommendations

[Based on issues found, provide actionable recommendations:]

1. [Recommendation 1]
2. [Recommendation 2]
3. [Recommendation 3]

---

## Next Steps

[IF system healthy:]
Your system is in good shape! Continue working normally.

[IF issues auto-fixed:]
Issues have been automatically fixed. You're good to go!

[IF manual fixes required:]
Please address the issues above, then run validate-system again to confirm.

[IF warnings present:]
Warnings are non-blocking but should be reviewed when convenient.

---

**Validation complete.**
```

---

### Step 12: Display Report

Display the generated report to user:

```
✅ System Validation Complete

[Show full report from Step 11]

---

[IF issues auto-fixed:]
I automatically fixed {N} issues. Your system is now healthy! ✅

[IF manual fixes required:]
Please fix the {M} issues above, then run "validate system" again.

[IF system healthy:]
Your system is healthy! No issues found. 🎉

[IF warnings only:]
Your system is operational but has {W} warnings to review. ⚠️
```

---

### Step 13: Auto-Trigger close-session

Auto-trigger the `close-session` skill to:
- Update 02-builds/build-map.md (if needed)
- Regenerate skill-map.md (if it was regenerated in auto-fix)
- Create session report
- Clean up temporary files
- Display session summary

**Format**:
```
Auto-triggering close-session skill...

[close-session workflow executes]

Session saved! ✅
```

---
