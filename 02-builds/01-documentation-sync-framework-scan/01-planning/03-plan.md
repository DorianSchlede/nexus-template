# Documentation Sync - Plan

**Build Type**: Content (Documentation Update)
**Status**: Planning Complete

---

## Context

**Load Before Execution**:
- `01-planning/02-discovery.md` - Discrepancy analysis

---

## Approach

Update 3 documentation files systematically using discovery findings as reference.

### Update Pipeline
```
Read Current Doc → Identify Sections to Update → Edit In-Place → Validate → Next Doc
```

**Key Principle**: Surgical updates, not rewrites. Preserve doc structure and purpose.

---

## Content Outline

### Document 1: product-overview.md

**Purpose**: User-facing overview of what problems Nexus solves
**Length**: ~500 lines
**Changes Required**:
- Update title (remove version number or update to current)
- Update folder structure diagram (build planning files)
- Update skill examples (add integration ecosystem)
- Add hooks system summary
- Update session pattern (hooks-based, not manual)
- Update version/date footer

### Document 2: framework-overview.md

**Purpose**: Technical architecture for developers
**Length**: ~1,400 lines
**Changes Required**:
- Update system skills count (25 → 152)
- Update mental models count (59 → 90)
- Update CLI commands section (add all flags)
- Update build structure section (numbered files)
- Add hooks system section (6 hooks)
- Update onboarding skills section
- Update version footer (V4.0 → current)

### Document 3: ux-onboarding-philosophy.md

**Purpose**: Design standards for onboarding experiences
**Length**: ~1,500 lines
**Changes Required**:
- Update case study section (Build 00 references)
- Update last updated date
- Verify metrics still accurate
- Check for deprecated feature references

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Edit in-place vs rewrite | Edit in-place | Preserve existing structure, less risk |
| Update version numbers | Update dates, keep version labels | Documents are living, dates matter more |
| Add hooks section | Add brief section, not comprehensive | Product overview needs awareness, not deep dive |
| Skills count | Use category totals | "152 system skills across 7 categories" vs listing all |

---

## Dependencies & Links

### Reference Files
- `02-discovery.md` - Discrepancy analysis
- `00-system/system-map.md` - Authoritative structure
- `00-system/core/orchestrator.md` - Current routing rules
- `.claude/settings.json` - Hooks configuration

### No New Assets Required
Updates are text-only within existing files.

---

## Success Criteria (from overview.md)

- [ ] All file paths/locations match actual filesystem
- [ ] All CLI commands documented match actual commands
- [ ] All skill names/triggers match current catalog
- [ ] Build structure documentation matches templates
- [ ] Version numbers and dates updated
- [ ] No references to deprecated features

---

*Execution steps in 04-steps.md*
