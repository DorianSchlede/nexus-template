# close-session Skill Optimization Analysis

**Date**: 2025-11-03
**Current Status**: 40% Compliant (Needs Major Restructuring)

---

## Current Structure

```
close-session/
├── SKILL.md (664 lines, 17,740 bytes)
└── references/ (empty directory)
```

---

## Compliance Analysis

### ❌ CRITICAL ISSUES

1. **SKILL.md Way Over Limit**
   - **Current**: 664 lines
   - **Target**: <500 lines
   - **Overage**: 164 lines (33% over)
   - **Fix**: Split into SKILL.md + references

2. **No TOC**
   - File is >100 lines but has no table of contents
   - **Fix**: Add comprehensive TOC

3. **References Directory Empty**
   - Directory exists but unused
   - Perfect place for detailed workflow

### ✅ What's Good

- [x] Proper YAML frontmatter (name + description only)
- [x] Clear description with triggers
- [x] Well-structured content
- [x] Comprehensive coverage

---

## Content Analysis

### Sections in SKILL.md (664 lines)

1. **Frontmatter** (9 lines) - Keep
2. **Title + Purpose** (16 lines) - Keep
3. **Workflow** (540 lines) - **SPLIT OUT**
   - Step 1: Initialize TodoList
   - Step 2: Read Active Project State
   - Step 2.5: Review Task Completion
   - Step 3: Update Maps
   - Step 4: Get Fresh Timestamp
   - Step 5: Update Memory Files
   - Step 6: Clean Up Temporary Files
   - Step 7: Create Session Report
   - Step 7.5: Skill Execution Review
   - Step 8: Display Summary
   - Step 9: Mark TodoWrite Complete
4. **Error Handling** (56 lines) - **SPLIT OUT**
5. **Notes** (43 lines) - Keep (important integration info)

**Total**: 664 lines

---

## Optimization Plan

### Target Structure

```
close-session/
├── SKILL.md (~150 lines)
│   ├── Purpose
│   ├── Quick Start
│   ├── Workflow Overview (high-level)
│   ├── Key Features
│   ├── Integration Notes
│   └── References navigation
├── references/
│   ├── workflow.md (~550 lines with TOC)
│   │   └── Complete step-by-step workflow
│   └── error-handling.md (~60 lines with TOC)
│       └── All error scenarios
└── scripts/ (none needed)
```

---

## Step 1: Understanding with Concrete Examples

### Example 1: User Ends Session
```
User: "done for now"
System: "Closing your session..."
  1. Reads current project state
  2. Asks: "Which tasks did you complete?" (shows 10 unchecked)
  3. User: "1, 3, 5"
  4. Updates tasks.md (checks off 3 tasks)
  5. Recalculates progress
  6. Updates project-map.md
  7. Scans Projects/ and Skills/
  8. Regenerates navigation maps
  9. Cleans temp files (asks about each)
  10. Creates session report
  11. Displays summary
Result: "Session saved! ✅"
```

### Example 2: Skill Auto-Trigger
```
create-project skill completes
System: "Auto-triggering close-session skill..."
  [Same workflow as above]
Result: "Session saved! ✅"
```

### Example 3: No Active Project
```
User: "close session"
System: [Skips project steps]
  1. Updates navigation maps
  2. Cleans temp files
  3. Creates general session report
  4. Displays summary
Result: "Session saved! ✅"
```

### Key Features Identified
1. **Interactive task completion**: Asks user which tasks done
2. **Navigation regeneration**: Scans and rebuilds maps
3. **Temp file cleanup**: Interactive cleanup with user choices
4. **Session reporting**: Historical record creation
5. **Progress tracking**: Auto-calculates from checkboxes
6. **Auto-trigger support**: Called by other skills
7. **Memory preservation**: THE critical persistence mechanism

---

## Step 2: Planning Reusable Contents

### Scripts (None Needed)
- **Decision**: No scripts
- **Reason**: All operations are file reads/writes that Claude does well
- **No deterministic code needed**

### References (2 Files Needed)

#### reference/workflow.md
- **Purpose**: Complete step-by-step workflow (all 9 steps)
- **Size**: ~550 lines
- **Needs TOC**: YES (>100 lines)
- **Content**:
  - Step 1: Initialize TodoList
  - Step 2: Read Active Project State
  - Step 2.5: Review Task Completion (interactive)
  - Step 3: Update Maps (scan Projects/ and Skills/)
  - Step 4: Get Fresh Timestamp
  - Step 5: Update Memory Files
  - Step 6: Clean Up Temporary Files (interactive)
  - Step 7: Create Session Report
  - Step 7.5: Skill Execution Review
  - Step 8: Display Summary
  - Step 9: Mark TodoWrite Complete

####  references/error-handling.md
- **Purpose**: All error scenarios and solutions
- **Size**: ~60 lines
- **Needs TOC**: NO (<100 lines)
- **Content**:
  - No Active Project
  - tasks.md Missing
  - Memory Files Corrupted
  - Map Generation Fails
  - Max Session Reports
  - Temp File User Doesn't Respond

### Assets (None Needed)
- **Decision**: No assets
- **Reason**: No templates, images, or output files needed

---

## Optimized SKILL.md Structure

```markdown
---
name: close-session
description: [current description - keep as is]
---

# Close Session

Save progress, update memory, regenerate navigation, ensure system integrity.

## Purpose

[Brief 2-3 paragraph overview]

**CRITICAL**: This skill is AUTO-TRIGGERED by all other skills and projects.

## Quick Start

1. Initialize TodoWrite
2. Follow workflow in [workflow.md](references/workflow.md)
3. Handle errors per [error-handling.md](references/error-handling.md)

## Key Features

- **Interactive Task Completion**: Asks which tasks done
- **Navigation Regeneration**: Auto-scans and rebuilds maps
- **Temp File Cleanup**: Interactive cleanup
- **Session Reporting**: Historical record
- **Progress Tracking**: Auto-calculates from checkboxes
- **Auto-Trigger Support**: Called by other skills
- **Memory Preservation**: THE critical persistence mechanism

## Workflow Overview

Complete workflow with all 9 steps: See [workflow.md](references/workflow.md)

High-level steps:
1. Read project state
2. Interactive task completion
3. Regenerate navigation maps (scan Projects/ and Skills/)
4. Get fresh timestamp
5. Update memory files
6. Clean temp files (interactive)
7. Create session report
8. Display summary

## Integration

**Auto-Trigger Format** (from other skills):
[Example]

**User-Trigger Format** (user says "done"):
[Example]

**All Skills Must End With**:
```markdown
### Final Step: Close Session
Auto-trigger close-session skill to save progress
```

## Error Handling

For complete error scenarios and solutions, see [error-handling.md](references/error-handling.md)

Common scenarios:
- No active project → Skip project steps
- Missing tasks.md → Report in summary
- Corrupted memory → Rebuild from scan

## Critical Notes

**Memory Preservation**:
This skill is the ONLY way to:
- Update 02-projects/project-map.md
- Regenerate skill-map.md
- Create session reports
- Clean temp files

**Without this skill, context does NOT persist across sessions!**

Never skip this skill - it's the foundation of context preservation.
```

**Estimated**: ~150 lines

---

## Optimizations Applied

1. ✅ **Reduce SKILL.md**: 664 lines → ~150 lines (77% reduction)
2. ✅ **Add TOC to workflow.md**: Required for >100 lines
3. ✅ **Split detailed workflow**: Move to references/workflow.md
4. ✅ **Split error handling**: Move to references/error-handling.md
5. ✅ **Clear navigation**: Link to references from SKILL.md
6. ✅ **Describe when to load**: Each reference linked with context

---

## Compliance Score

**Before**: 40% (664 lines, no TOC, no references used)
**After**: 100% (150 lines, TOC in references, proper structure)

---

## Next Steps

1. ✅ Analysis complete
2. ⬜ Initialize new skill structure
3. ⬜ Create references/workflow.md (with TOC)
4. ⬜ Create references/error-handling.md
5. ⬜ Write optimized SKILL.md
6. ⬜ Test (manual walkthrough)
7. ⬜ Replace old version

---

**Ready to proceed to Step 3: Initialize new skill structure**
