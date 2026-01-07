# Improve Add-Integration Skill - Plan

**Last Updated**: 2026-01-07
**Status**: Ready for Execution
**Approach**: Option 2 (Better) - Auto-execute scaffold

---

## Context

**Load Before Reading**:
- `01-planning/01-overview.md` - Purpose and success criteria
- `01-planning/02-discovery.md` - Dependencies discovered

**Reference Materials**:
- `02-resources/fix-options-analysis.md` - Detailed fix options
- `02-resources/merge-from-create-master-skill.md` - Components to merge
- `02-resources/audit-add-integration.md` - Full audit

---

## Approach

**Fix Option 2 (Better)**: Auto-execute scaffold after config finalization

```
BEFORE:
Step 7: Write integration-config.json → DONE (broken)

AFTER:
Step 7: Write integration-config.json
Step 7.5: Execute scaffold_integration.py → Skills generated
Step 8: Display success + next steps
```

**Why Option 2**:
- Fully automated (user doesn't have to remember manual step)
- Contained to add-integration skill (no cross-skill changes)
- Reasonable effort (1 day)
- Can upgrade to Option 3 later if needed

---

## Key Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Fix approach | Option 2 (auto-execute) | Best balance of effort vs automation |
| Merge components | Yes, from create-master-skill | Adds tests, research depth, discovery |
| Test templates | Add to scaffold output | Enables quality validation |
| Validation script | Create new | Catch errors before user sees them |
| Research checklist | Copy verbatim | 10 searches vs 2-3 improves coverage |

---

## Dependencies & Links

### Files to Modify

| File | Changes |
|------|---------|
| `00-system/skills/system/add-integration/SKILL.md` | Add Step 7.5 scaffold execution |
| `00-system/skills/system/add-integration/scripts/scaffold_integration.py` | Add tests/ generation |

### Files to Create

| File | Purpose |
|------|---------|
| `templates/tests/run_tests.py.template` | Test runner |
| `templates/tests/README.md.template` | Test docs |
| `scripts/validate_integration.py` | Post-scaffold validation |

### Files to Copy

| Source | Destination |
|--------|-------------|
| `create-master-skill/references/research-checklist.md` | `add-integration/references/` |
| `create-master-skill/references/master-skill-patterns.md` | `add-integration/references/` |
| `create-master-skill/templates/discover_resources.py.template` | `add-integration/templates/` |

### External Systems

- WebSearch (API discovery)
- File system (skill generation)
- Python (scaffold execution)

---

## Technical Architecture

### Current Flow (Broken)

```
User: "add slack integration"
    ↓
add-integration SKILL.md
    ↓
Steps 1-7: WebSearch → Parse → Select → Config
    ↓
OUTPUT: integration-config.json ← STOPS HERE
    ↓
Step 8: "execute-project will scaffold" ← LIE, doesn't happen
```

### New Flow (Fixed)

```
User: "add slack integration"
    ↓
add-integration SKILL.md
    ↓
Steps 1-7: WebSearch → Parse → Select → Config
    ↓
Step 7.5 (NEW): Run scaffold_integration.py
    ↓
OUTPUT: {service}-master/, {service}-connect/, {service}-{op}/
    ↓
Step 8: Display success summary
```

### Scaffold Integration

```python
# In SKILL.md Step 7.5:

1. Display: "Generating integration skills..."

2. Execute:
   python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
     --config {project_path}/02-resources/integration-config.json

3. Verify:
   - Check {service}-master/ exists
   - Check {service}-connect/ exists
   - Check operation skills count matches config

4. Display summary:
   ✅ Skills Generated!
   • {service}-master/
   • {service}-connect/
   • {N} operation skills
```

---

## Implementation Strategy

### Phase 1: Core Fix (4 hours)

1. Update SKILL.md with Step 7.5
2. Add scaffold execution instructions
3. Add success verification steps
4. Add error handling for failures

### Phase 2: Merge Components (4 hours)

1. Copy research-checklist.md
2. Copy master-skill-patterns.md
3. Create test templates
4. Update scaffold to generate tests/

### Phase 3: Testing (2 hours)

1. Test with real API (Stripe or GitHub)
2. Verify skills generated correctly
3. Test error handling
4. Verify tests run

### Testing Approach

| Test | Method | Success Criteria |
|------|--------|------------------|
| Happy path | Run full workflow | Skills generated |
| Error handling | Invalid config | Graceful error message |
| Large integration | 20+ endpoints | No timeout |
| Auth types | All 3 | Correct code generated |

### Deployment Plan

1. Make changes in add-integration skill
2. Test locally with real API
3. Document in SKILL.md
4. Update references

---

## Error Handling

### Scaffold Failures

```markdown
IF scaffold fails:
  1. Display error with details
  2. Save error log to 03-working/scaffold-error.log
  3. Provide manual retry command
  4. Do NOT mark project complete
```

### Error Messages

| Error | Message | Recovery |
|-------|---------|----------|
| Template missing | "Template not found: {name}" | Check templates/ folder |
| Permission denied | "Cannot write to {path}" | Check permissions |
| Config invalid | "Invalid config: {field}" | Re-run Step 7 |
| Skill exists | "Skills already exist at {path}" | Use --force or skip |

---

## Open Questions

- [x] Which fix option? → Option 2 (Better)
- [x] What to merge? → tests, research-checklist, patterns, discover
- [ ] Add --dry-run flag? → Nice to have, not blocking

---

## Success Criteria

**Must achieve**:
- [ ] Scaffold executes automatically in workflow
- [ ] Users get actual skills (master + connect + operations)
- [ ] Error handling prevents partial output

**Nice to have**:
- [ ] Test templates generated
- [ ] Research checklist improved (10 searches)
- [ ] Discover resources script added

---

*Next: Break down execution in 04-steps.md*
