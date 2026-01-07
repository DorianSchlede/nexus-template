---
id: 36-improve-add-integration-skill
name: Improve Add-Integration Skill
status: PLANNING
description: "Fix critical bugs and merge best components from create-master-skill"
created: 2026-01-07
project_path: 02-projects/36-improve-add-integration-skill/
spun_off_from: 30-improve-plan-project-skill
---

# Improve Add-Integration Skill

## Project Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

Fix the `add-integration` skill so it actually generates integration skills, and merge high-value components from `create-master-skill` to make it the definitive integration creation workflow.

**Origin**: Spun off from Project 30 after deep audit revealed:
- `add-integration` has superior templates but scaffold is never executed
- `create-master-skill` has valuable components to merge

---

## Success Criteria

**Must achieve**:
- [ ] `scaffold_integration.py` executes during workflow (not left as manual step)
- [ ] Users get actual skills generated, not just planning documents
- [ ] Integration type routing works end-to-end through plan-project

**Nice to have**:
- [ ] Merge `tests/` templates from create-master-skill
- [ ] Merge `research-checklist.md` (10 search areas vs 2-3)
- [ ] Merge `master-skill-patterns.md` documentation
- [ ] Merge `discover_resources.py.template`

---

## Context

**Background**:
Deep audit (see `30-improve-plan-project-skill/03-working/audit-*.md`) revealed:
- `add-integration` creates beautiful plans but **never executes scaffold**
- Users get `integration-config.json` but no actual skills
- Templates are SUPERIOR to production (would generate better skills than langfuse)
- Critical disconnect between planning and execution

**Stakeholders**:
- Anyone creating new integrations via plan-project
- Future integration builders

**Constraints**:
- Must not break existing integrations
- Should work with plan-project router pattern
- Keep backward compatibility with manual scaffold execution

---

## Audit Findings (from Project 30)

### Critical Bug
```
Step 8 says "execute-project will run scaffold_integration.py"
BUT: execute-project doesn't know about scaffold_integration.py
RESULT: Users get plans, no skills
```

### What add-integration HAS (excellent)
- 11 production-ready templates
- 859-line scaffold script
- 3 auth types (oauth2, bearer, api_key)
- Complete structure generation (master + connect + operations)

### What to merge from create-master-skill
1. `tests/run_tests.py.template` - Test runner
2. `tests/README.md.template` - Test docs
3. `references/research-checklist.md` - 10 search areas
4. `references/master-skill-patterns.md` - DRY architecture docs
5. `templates/discover_resources.py.template` - Resource discovery

### Fix Options (from audit)
1. **Minimal** (2 hrs): Add scaffold command to steps.md + final message
2. **Better** (1 day): Auto-execute scaffold after config finalization
3. **Complete** (2-3 days): Full integration with execute-project detection

---

## Reference Materials

- `30-improve-plan-project-skill/03-working/audit-add-integration.md` - Full audit (699 lines)
- `30-improve-plan-project-skill/03-working/audit-create-master-skill.md` - Comparison audit (457 lines)
- `00-system/skills/system/add-integration/` - Skill location
- `00-system/skills/skill-dev/create-master-skill/` - Components to merge

---

*Next: Fill in 02-discovery.md with technical details*
