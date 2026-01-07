# Discovery

**Time**: Complete | **Purpose**: Surface dependencies before planning
**Source**: Deep audit from Project 30

---

## Context

**Load First**: `01-planning/01-overview.md` - Understand project purpose
**Output To**: `01-planning/03-plan.md` - Dependencies section auto-populated from this file

**Reference Materials in 02-resources/**:
- `audit-add-integration.md` - Full 699-line audit
- `audit-create-master-skill.md` - Comparison audit (457 lines)
- `integration-architecture-comparison.md` - Side-by-side comparison
- `fix-options-analysis.md` - Detailed fix options
- `merge-from-create-master-skill.md` - Components to merge

---

## The Problem

```
Current Flow:
add-integration → creates integration-config.json → STOPS

Expected Flow:
add-integration → creates config → RUNS SCAFFOLD → generates skills
```

**Root Cause**: SKILL.md Step 8 says "execute-project will run scaffold" but execute-project doesn't know about scaffold_integration.py.

---

## Dependencies

### Files to Modify

| File | Changes |
|------|---------|
| `00-system/skills/system/add-integration/SKILL.md` | Add Step 7.5 scaffold execution |
| `00-system/skills/system/add-integration/scripts/scaffold_integration.py` | Add tests/ generation, validation |

### Files to Create

| File | Purpose |
|------|---------|
| `add-integration/templates/tests/run_tests.py.template` | Test runner template |
| `add-integration/templates/tests/README.md.template` | Test documentation |
| `add-integration/references/research-checklist.md` | Copy from create-master-skill |
| `add-integration/references/master-skill-patterns.md` | Copy from create-master-skill |
| `add-integration/templates/discover_resources.py.template` | Copy from create-master-skill |
| `add-integration/scripts/validate_integration.py` | Post-scaffold validation |

### Files to Copy (from create-master-skill)

| Source | Destination |
|--------|-------------|
| `skill-dev/create-master-skill/references/research-checklist.md` | `system/add-integration/references/` |
| `skill-dev/create-master-skill/references/master-skill-patterns.md` | `system/add-integration/references/` |
| `skill-dev/create-master-skill/templates/discover_resources.py.template` | `system/add-integration/templates/` |

### External Systems

- WebSearch (for API discovery during workflow)
- File system (skill generation)
- Python (scaffold script execution)

---

## Existing Patterns

### Related Skills

| Skill | Relationship |
|-------|--------------|
| `00-system/skills/system/add-integration/` | **TARGET** - skill being improved |
| `00-system/skills/skill-dev/create-master-skill/` | Source of components to merge |
| `00-system/skills/projects/plan-project/` | Router that calls add-integration |
| `00-system/skills/projects/execute-project/` | Could detect integration projects (Option 3) |

### Related Projects

| Project | Relationship |
|---------|--------------|
| `02-projects/30-improve-plan-project-skill/` | Parent project, contains audits |

### Code Patterns

**Scaffold Pattern** (from scaffold_integration.py):
```python
def create_master_skill(config, output_dir):
    """Generate master skill directory."""
    # Load templates
    # Replace placeholders
    # Write files
```

**Template Pattern**:
```python
def render_template(content, vars):
    """Replace {{placeholders}} with values."""
    for key, value in vars.items():
        content = content.replace(f'{{{{{key}}}}}', value)
    return content
```

**Config Check Pattern** (ai_action):
```python
def check_config():
    """Returns JSON with ai_action field."""
    return {
        "status": "missing_config",
        "ai_action": "prompt_for_api_key",  # Tells AI exactly what to do
        "message": "API key not found"
    }
```

---

## Existing Templates (11 total)

| Template | Lines | Status |
|----------|-------|--------|
| master-skill.md.template | 130 | ✅ Complete |
| connect-skill.md.template | 127 | ✅ Complete |
| operation-skill.md.template | 74 | ✅ Complete |
| api-client.py.template | 124 | ✅ Complete |
| config-check.py.template | 164 | ✅ Complete |
| setup-wizard.py.template | 153 | ✅ Complete |
| operation-script.py.template | 85 | ✅ Complete |
| setup-guide.md.template | 95 | ✅ Complete |
| api-reference.md.template | 60 | ✅ Complete |
| error-handling.md.template | 123 | ✅ Complete |
| authentication.md.template | 81 | ✅ Complete |

**Missing**: tests/ templates, discover_resources.py

---

## Scaffold Script Analysis

**Location**: `add-integration/scripts/scaffold_integration.py`
**Lines**: 859
**Quality**: Production-ready

**Functions**:
| Function | Purpose |
|----------|---------|
| `load_template(name)` | Load template file |
| `render_template(content, vars)` | Replace placeholders |
| `generate_auth_methods(auth_type, slug)` | OAuth2/Bearer/API key code |
| `create_master_skill(config, output_dir)` | Generate master skill |
| `create_connect_skill(config, output_dir)` | Generate connect skill |
| `create_operation_skill(config, endpoint, output_dir)` | Generate per-endpoint skills |
| `scaffold_integration(config)` | Main orchestration |

**Auth Types Supported**:
- `oauth2` - Client credentials, token refresh
- `bearer` - API key as Bearer token
- `api_key` - X-API-Key header

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Scaffold timeout for large integrations | Medium | Medium | Add progress output |
| Breaking existing workflow | Low | High | Test thoroughly before merge |
| Template placeholder mismatch | Low | Medium | Validate before execution |
| Auth type not supported | Low | Medium | Document supported types |

### Open Questions

- [x] Which fix option to implement? → **Option 2 (Better)** - Auto-execute scaffold
- [x] Where to merge from create-master-skill? → See `merge-from-create-master-skill.md`
- [x] What tests to add? → Config, client, references validation
- [ ] Should we add --dry-run to scaffold? → Nice to have, not required

---

## Success Criteria (from overview)

**Must achieve**:
- [ ] `scaffold_integration.py` executes during workflow
- [ ] Users get actual skills generated
- [ ] Integration type routing works end-to-end

**Nice to have**:
- [ ] Tests templates merged
- [ ] Research checklist merged
- [ ] Discover resources script added

---

*Auto-populate 03-plan.md Dependencies section from findings above*
