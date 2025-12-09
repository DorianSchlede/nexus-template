# Skill Format Specification

Complete specification for skill structure and requirements.

## Directory Structure

```
skill-name/
├── SKILL.md                 (required)
├── scripts/                 (optional)
│   └── *.py, *.sh, etc.
├── references/              (optional)
│   └── *.md
└── assets/                  (optional)
    └── templates, images, etc.
```

## SKILL.md Format

### Frontmatter (Required)

```yaml
---
name: skill-name
description: Comprehensive description of what the skill does and when to use it. Include key terms and specific triggers/contexts. Claude uses this to choose from 100+ skills, so be thorough, concise, and direct.
---
```

**Required fields:**
- `name`: Skill identifier in hyphen-case (e.g., `pdf-editor`, `brand-guidelines`)
- `description`: Detailed description (100-500 words typical, be specific)

**No other fields allowed.** Do not include: `type`, `triggers`, `frequency`, `tags`, `version`, `author`, etc.

**Description guidelines:**
- Be specific about functionality
- Include key terms for discoverability
- Mention when/why to use the skill
- Can mention example triggers naturally ("when rotating PDFs", "for client proposals")
- Focus on clear selection criteria

### Body (Required)

Markdown instructions for using the skill. No rigid structure required—organize to suit the skill's needs.

**Typical sections** (use what fits):
- Introduction/overview of skill capabilities
- Workflow or process steps
- Tool/API usage instructions
- Examples or patterns
- References to bundled resources

**Key principles:**
- **Concise** - Challenge every sentence's token cost
- **Claude is smart** - Only add what Claude doesn't know
- **Actionable** - Provide clear guidance
- **Progressive disclosure** - Keep SKILL.md lean, use references for details

**Keep under 500 lines.** Split to references/ if approaching this limit.

## Resource Organization

### scripts/ (Optional)

Executable code for deterministic reliability or repeated operations.

**When to include:**
- Same code rewritten repeatedly
- Deterministic behavior required
- Complex operations prone to error

**Formats:** Python, Bash, JavaScript, etc.

**Requirements:**
- Scripts must be tested and functional
- May be executed without loading into context
- May need to be read for patching/adjustments

### references/ (Optional)

Documentation loaded into context as needed by Claude.

**When to include:**
- Database schemas
- API documentation
- Company policies
- Domain knowledge
- Detailed workflows
- Large examples

**Keep SKILL.md lean** - move detailed information to references.

**Best practices:**
- One level deep (all referenced from SKILL.md)
- Include table of contents for files >100 lines
- Use clear, descriptive filenames
- No duplication between SKILL.md and references

**File size warning:** For files >10k words, include grep search patterns in SKILL.md

### assets/ (Optional)

Files used in output, not loaded into context.

**When to include:**
- Templates (PPTX, DOCX, HTML)
- Images, icons, logos
- Fonts
- Boilerplate code
- Sample documents

**Usage:** Copied, modified, or referenced in Claude's output

## What NOT to Include

Do not create extraneous files:
- ❌ README.md
- ❌ INSTALLATION_GUIDE.md
- ❌ QUICK_REFERENCE.md
- ❌ CHANGELOG.md
- ❌ Setup/testing documentation
- ❌ User-facing guides

Skills are for AI agents. Include only what's needed for execution.

## Progressive Disclosure

Three-level loading system:

1. **Metadata** (~100 words) - Always in context
2. **SKILL.md** (<5k words) - Loaded when skill triggers
3. **Resources** (unlimited) - Loaded as needed

**Splitting patterns:**

**Pattern 1: Variant-specific**
```
cloud-deploy/
├── SKILL.md (overview + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

**Pattern 2: Domain-specific**
```
bigquery-skill/
├── SKILL.md (navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

**Pattern 3: Feature-specific**
```
pdf-skill/
├── SKILL.md (quick start)
└── references/
    ├── forms.md
    ├── api-reference.md
    └── examples.md
```

Load only what's needed for the current task.

## Degrees of Freedom

Match specificity to task fragility:

**High freedom (text instructions):**
- Multiple valid approaches
- Context-dependent decisions
- Heuristic guidance

**Medium freedom (pseudocode/parameterized scripts):**
- Preferred patterns exist
- Some variation acceptable
- Configuration affects behavior

**Low freedom (specific scripts):**
- Operations are fragile
- Consistency is critical
- Specific sequence required

## Validation Requirements

Required checks:
- ✅ YAML has only `name` and `description`
- ✅ Name is hyphen-case
- ✅ Description is comprehensive and specific
- ✅ Body contains actionable instructions
- ✅ File is under 500 lines (or split appropriately)
- ✅ No extraneous files (README, etc.)
- ✅ Referenced resources exist
- ✅ Scripts are tested and functional

## Common Mistakes

1. **Verbose SKILL.md** - Move details to references
2. **Missing description specificity** - Include key terms and triggers
3. **Extraneous YAML fields** - Only name + description
4. **Creating README files** - Skills don't need them
5. **Deeply nested references** - Keep one level deep
6. **Assuming Claude knows domain specifics** - Include schemas, policies, etc.
7. **Not testing scripts** - Scripts must work
8. **Over 500 lines** - Split to references

## Packaging

Skills package as `.skill` files (zip with .skill extension).

**Package contents:**
- All files in skill directory
- Maintains directory structure
- Scripts remain executable

**Validation:** Automatic during packaging - fix errors before package creation.

## Examples

**Minimal skill:**
```
pdf-rotator/
└── SKILL.md (name, description, instructions, script reference)
└── scripts/
    └── rotate.py
```

**Medium complexity:**
```
brand-guidelines/
├── SKILL.md (overview, when to use each asset)
├── references/
│   └── voice-tone.md
└── assets/
    ├── logo.png
    └── colors.json
```

**High complexity:**
```
data-pipeline/
├── SKILL.md (workflow + navigation)
├── scripts/
│   ├── extract.py
│   └── transform.py
├── references/
│   ├── schemas.md
│   ├── api-docs.md
│   └── examples.md
└── assets/
    └── config-template.yaml
```

## Quick Reference

**Must have:**
- SKILL.md with YAML frontmatter
- Name and description in YAML
- Clear instructions in body

**Should have:**
- Resources that reduce token overhead
- Progressive disclosure strategy
- Appropriate degrees of freedom

**Avoid:**
- Extra documentation files
- Verbose explanations Claude doesn't need
- Untested scripts
- Over 500-line SKILL.md
