# Error Scenarios and Recovery

Common errors during skill creation and how to handle them.

## YAML Errors

### Invalid YAML Syntax

**Error:** `YAML parsing failed: invalid syntax at line X`

**Cause:** Malformed YAML frontmatter

**Fix:**
- Check colons have spaces after them (`name: value` not `name:value`)
- Check quotes match (no smart quotes)
- Verify indentation is consistent
- Ensure `---` delimiters present

**Example:**
```yaml
---
name: my-skill
description: Does something useful.
---
```

### Extra YAML Fields

**Error:** `Validation failed: only 'name' and 'description' allowed in frontmatter`

**Cause:** Including deprecated or custom fields

**Fix:** Remove all fields except `name` and `description`

**Wrong:**
```yaml
---
name: my-skill
description: Description here
type: workflow        # ← Remove
version: 1.0          # ← Remove
---
```

**Right:**
```yaml
---
name: my-skill
description: Description here
---
```

## Naming Errors

### Invalid Name Format

**Error:** `Skill name must be hyphen-case (lowercase with hyphens)`

**Cause:** Name uses underscores, camelCase, or spaces

**Fix:** Convert to hyphen-case

**Examples:**
- ❌ `my_skill` → ✅ `my-skill`
- ❌ `mySkill` → ✅ `my-skill`
- ❌ `My Skill` → ✅ `my-skill`
- ❌ `MySkill` → ✅ `my-skill`

### Skill Already Exists

**Error:** `Skill 'skill-name' already exists at path/to/skill-name`

**Options:**
1. **Update existing** - Edit the existing skill instead
2. **Different name** - Choose a different, more specific name
3. **Replace** - Delete existing skill first (risky - backup first)

**Recovery:** Use `init_skill.py --path` to specify different location or choose different name

## File Size Errors

### SKILL.md Too Large

**Error:** `SKILL.md exceeds 500 lines (currently XXX lines)`

**Fix:** Split content into references/

**Strategy:**
1. Identify large sections (API docs, schemas, examples)
2. Move to references/ files
3. Reference from SKILL.md: `See [api-docs.md](references/api-docs.md)`
4. Keep only essential workflow in SKILL.md

**Example split:**
```
Before: SKILL.md (600 lines)
After:
- SKILL.md (300 lines) - workflow + navigation
- references/api-docs.md (200 lines)
- references/examples.md (100 lines)
```

## Validation Errors

### Missing Required Sections

**Error:** `Validation failed: missing required content`

**Cause:** SKILL.md lacks frontmatter or body

**Fix:**
- Verify YAML frontmatter exists
- Verify markdown body has instructions
- Check file isn't empty or template-only

### Description Too Short

**Error:** `Description should be comprehensive (at least 50 characters)`

**Cause:** Description doesn't provide enough context

**Fix:** Expand description with:
- What the skill does
- When to use it
- Key functionality
- Example triggers/contexts

**Too short:**
```yaml
description: PDF tool
```

**Better:**
```yaml
description: Process PDF documents - rotate pages, extract text, fill forms. Use when working with PDF files that need manipulation or data extraction.
```

### Broken Resource References

**Error:** `Referenced file not found: references/missing-file.md`

**Cause:** SKILL.md references non-existent file

**Fix:**
- Create the referenced file
- Remove the reference
- Fix the file path/name

## Script Errors

### Script Not Executable

**Error:** `Permission denied when executing scripts/script-name.py`

**Fix:**
```bash
chmod +x scripts/script-name.py
```

Or execute with interpreter explicitly:
```bash
python scripts/script-name.py
```

### Script Runtime Error

**Error:** Script fails during testing

**Fix:**
1. Test script manually first
2. Check dependencies installed
3. Verify input parameters
4. Add error handling to script
5. Test with various inputs

**Best practice:** Test all scripts before packaging

## Packaging Errors

### Validation Failed - Cannot Package

**Error:** `Cannot create package: validation failed`

**Cause:** Skill has validation errors

**Fix:**
1. Read validation error messages carefully
2. Fix each error reported
3. Run `package_skill.py` again
4. Repeat until validation passes

**Note:** Packaging includes automatic validation - you cannot package invalid skills

### Missing Files

**Error:** `Referenced file does not exist: assets/template.docx`

**Cause:** SKILL.md or scripts reference missing files

**Fix:**
- Add the missing file
- Remove the reference
- Fix the file path

## Directory Structure Errors

### Resources in Wrong Location

**Error:** Files not found by Claude

**Cause:** Resources in wrong directory or incorrectly referenced

**Fix:** Use correct structure:
```
skill-name/
├── SKILL.md
├── scripts/         ← Executable code here
├── references/      ← Documentation here
└── assets/          ← Templates/images here
```

**Reference correctly from SKILL.md:**
- Scripts: `scripts/script-name.py`
- References: `[docs](references/docs.md)`
- Assets: `assets/template.png`

## Recovery Strategies

### Start Fresh

If skill is severely broken:

1. Backup current work
2. Run `init_skill.py` with different name
3. Copy working parts from backup
4. Rebuild cleanly

### Incremental Testing

Prevent errors by:

1. Test after each major change
2. Validate frequently during development
3. Test scripts as you write them
4. Keep SKILL.md under 500 lines from start

### Use Version Control

Track changes:
```bash
git init
git add .
git commit -m "Initial skill structure"
# Make changes
git commit -m "Added PDF rotation script"
```

Rollback if needed:
```bash
git log                    # Find good commit
git checkout <commit>      # Return to that state
```

## Prevention Checklist

Before packaging, verify:
- [ ] YAML has only name + description
- [ ] Name is hyphen-case
- [ ] Description is comprehensive
- [ ] SKILL.md under 500 lines
- [ ] All scripts tested
- [ ] All referenced files exist
- [ ] No extraneous files (README, etc.)
- [ ] Resources in correct directories

## Getting Help

If stuck:
1. Check skill-format-specification.md
2. Review existing working skills
3. Validate frequently to catch errors early
4. Start with minimal skill, add complexity gradually
