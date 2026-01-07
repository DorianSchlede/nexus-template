# Fix Options Analysis

**Created**: 2026-01-07
**Problem**: `scaffold_integration.py` is never executed during add-integration workflow

---

## The Problem

```
Current Flow:
add-integration → creates integration-config.json → STOPS

Expected Flow:
add-integration → creates config → RUNS SCAFFOLD → generates skills
```

Users complete the add-integration workflow and get:
- ✅ Project folder with planning docs
- ✅ `integration-config.json` with all endpoint details
- ❌ NO actual skills generated
- ❌ NO master/connect/operation structure

---

## Fix Option 1: Minimal (2 hours)

### What to Change

**File**: `add-integration/SKILL.md`

**Change Step 7** output to include scaffold command:

```markdown
## Step 7 Output (REVISED)

Project Finalized!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 02-projects/{id}-{service}-integration/

**NEXT STEP - Generate Skills:**

Run this command to create the integration skills:

```bash
python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
  --config 02-projects/{id}-{service}-integration/02-resources/integration-config.json
```

This will create:
• {service}-master/ (shared resources)
• {service}-connect/ (user entry point)
• {count} operation skills

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Also update Step 8** message to reinforce:
```markdown
Before closing this session, run the scaffold command above!
```

### Pros
- Minimal code changes
- Backward compatible
- User has control over when scaffold runs

### Cons
- Manual step (user might forget)
- Not automated
- Extra user action required

### Effort
- 2 hours

---

## Fix Option 2: Better (1 day)

### What to Change

**File**: `add-integration/SKILL.md`

**Add Step 7.5**: Auto-execute scaffold after config finalization

```markdown
## Step 7.5: Generate Integration Skills (NEW)

After writing integration-config.json:

1. Display message: "Generating integration skills..."

2. Execute scaffold:
   ```bash
   python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
     --config {project_path}/02-resources/integration-config.json
   ```

3. Verify success:
   - Check {service}-master/ exists
   - Check {service}-connect/ exists
   - Check operation skills created

4. Display summary:
   ```
   ✅ Skills Generated!

   Created:
   • 00-system/skills/{service}/{service}-master/
   • 00-system/skills/{service}/{service}-connect/
   • {count} operation skills

   You can now use: "connect to {service}"
   ```
```

### Pros
- Fully automated
- User gets complete output
- No manual steps

### Cons
- More complex workflow
- Need error handling
- Session might timeout for large integrations

### Effort
- 1 day

---

## Fix Option 3: Complete (2-3 days)

### What to Change

**Multiple files**:

1. **execute-project skill** - Add integration detection
2. **add-integration/SKILL.md** - Update workflow
3. **scaffold_integration.py** - Add validation

### Implementation

**execute-project changes**:
```python
# After loading project, check if integration project
config_path = project_path / "02-resources" / "integration-config.json"

if config_path.exists():
    config = json.load(config_path)
    service_slug = config['service_slug']

    # Check if already scaffolded
    master_path = Path(f"00-system/skills/{service_slug}/{service_slug}-master")

    if not master_path.exists():
        display("Integration project detected. Running scaffold...")
        run_scaffold(config_path)
        display("Skills generated!")
    else:
        display("Skills already exist. Skipping scaffold.")
```

**scaffold_integration.py changes**:
```python
# Add --validate flag
if args.validate:
    validate_generated_skills(output_dir)

# Add --dry-run flag
if args.dry_run:
    preview_output(config)
```

### Pros
- Best user experience
- Works with existing execute-project flow
- Idempotent (won't regenerate if exists)

### Cons
- Most complex
- Touches multiple skills
- Higher risk of breaking something

### Effort
- 2-3 days

---

## Recommendation

### Start with Option 2 (Better)

**Why**:
1. Fully automated - user gets skills without extra steps
2. Contained to add-integration skill (no cross-skill changes)
3. Reasonable effort (1 day)
4. Can upgrade to Option 3 later if needed

### Implementation Plan

1. **Update SKILL.md** (Step 7.5)
   - Add scaffold execution after config write
   - Add success verification
   - Add error handling

2. **Test manually**
   - Run full workflow with real API (Stripe recommended)
   - Verify skills generated
   - Verify skills work

3. **Document**
   - Update workflow diagram
   - Add "What gets generated" section
   - Add troubleshooting for scaffold failures

---

## Error Handling

### Scaffold Failures

| Error | Cause | Recovery |
|-------|-------|----------|
| Template not found | Missing template file | Check templates/ folder |
| Permission denied | Can't write to skills/ | Check permissions |
| Config invalid | Malformed JSON | Re-run Step 7 |
| Skill already exists | Previously scaffolded | Skip or use --force |

### Recommended Error Flow

```markdown
IF scaffold fails:
  1. Display error message with details
  2. Save error log to 03-working/scaffold-error.log
  3. Provide manual command to retry
  4. Do NOT mark project as complete
```

---

## Testing Plan

### Test Cases

1. **Happy path**: New service, valid config, scaffold succeeds
2. **Existing skills**: Service already scaffolded, should skip
3. **Invalid config**: Missing required fields, should error gracefully
4. **Large integration**: 20+ endpoints, verify timeout handling
5. **Auth types**: Test all 3 (oauth2, bearer, api_key)

### Test API Recommendations

| API | Why | Complexity |
|-----|-----|------------|
| Stripe | Well documented, free tier | Medium |
| GitHub | Familiar, good docs | Low |
| Notion | Already have integration | Reference |
| Airtable | Already have integration | Reference |

---

## Timeline

| Phase | Task | Effort |
|-------|------|--------|
| Day 1 AM | Update SKILL.md with Step 7.5 | 2 hrs |
| Day 1 PM | Test with Stripe API | 2 hrs |
| Day 1 PM | Error handling | 2 hrs |
| Day 2 AM | Documentation | 2 hrs |
| Day 2 PM | Final testing | 2 hrs |

**Total**: 10 hours over 2 days

---

## Success Criteria

- [ ] Running add-integration workflow generates actual skills
- [ ] Generated skills match production quality (langfuse, notion)
- [ ] Error handling prevents partial/broken output
- [ ] Documentation updated with new workflow
- [ ] End-to-end test passes with real API
