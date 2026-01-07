# Nexus CLI and Cleanup - Execution Steps

**Last Updated**: 2026-01-07

---

## Context Requirements

**Project Location**: `02-projects/31-nexus-cli-and-cleanup/`

**Files to Load for Execution**:
- `01-planning/01-overview.md` - Purpose, success criteria
- `01-planning/04-steps.md` - This file (execution tasks)
- `01-planning/resume-context.md` - Resume state

**Output Locations**:
- `03-working/` - Work in progress files
- `04-outputs/` - Final deliverables

---

## Phase 1: CLI Discovery Implementation

### 1.1 Add --discover flag to nexus-loader.py

- [ ] Read current nexus-loader.py argument parser
- [ ] Add `--discover CATEGORY` argument
- [ ] Wire up to `discover_skills_in_category()` function
- [ ] Return formatted output to stdout
- [ ] Test: `python nexus-loader.py --discover langfuse`

### 1.2 Update XML CLI hints

- [ ] Update `<cli>` tags in build_skills_xml_compact() to show actual command
- [ ] Change from `load-skill {category} --help` to `python nexus-loader.py --discover {category}`

### 1.3 Document CLI usage in orchestrator.md

- [ ] Add skill discovery section explaining CLI pattern
- [ ] Show example usage

---

## Phase 2: Performance Profiling

### 2.1 Measure hook execution time

- [ ] Add timing instrumentation to session_start.py
- [ ] Run 10 startup cycles
- [ ] Record times below
- [ ] Verify <200ms average

**Measurements**:
```
Run 1: ___ ms
Run 2: ___ ms
Run 3: ___ ms
Run 4: ___ ms
Run 5: ___ ms
Average: ___ ms
Target: <200ms
```

### 2.2 Optimize if needed

- [ ] (Conditional) Profile slow operations if >200ms
- [ ] (Conditional) Implement fixes

---

## Phase 3: Documentation Updates

### 3.1 Update system-map.md

- [ ] Document 6 startup state templates
- [ ] Add CLI discovery section
- [ ] Update skills catalog description
- [ ] Verify all file paths accurate

### 3.2 Review startup templates

- [ ] Check all 6 templates in .claude/hooks/templates/
- [ ] Ensure instructions are clear
- [ ] Fix any formatting issues

---

## Phase 4: Project 29 Cleanup

### 4.1 Create final summary

- [ ] Write 04-outputs/SUMMARY.md for Project 29
- [ ] Document token savings (60.9%)
- [ ] Document key changes
- [ ] Document lessons learned

### 4.2 Update Project 29 status

- [ ] Change status: PLANNING -> COMPLETE
- [ ] Update resume-context.md

### 4.3 Archive resources

- [ ] Move TRASH folder contents to archive/ or delete
- [ ] Clean up deprecated files
- [ ] Run archive-project skill

---

## Phase 5: Project 30 Review

- [ ] Check 02-projects/30-improve-plan-project-skill/ status
- [ ] Determine if complete or needs continuation
- [ ] Update status if complete

---

## Phase 6: Completion

- [ ] Update this project status: PLANNING -> COMPLETE
- [ ] Commit all changes
- [ ] Archive this project

---

## Success Criteria

**Must Achieve**:
- [ ] `python nexus-loader.py --discover langfuse` works
- [ ] Hook execution <200ms (measured)
- [ ] system-map.md updated
- [ ] Project 29 archived

---

## Notes

**Current blockers**: None

**Dependencies**:
- nexus-loader.py (add --discover flag)
- loaders.py (discover_skills_in_category already implemented)

---

*Mark tasks complete with [x] as you finish them*
