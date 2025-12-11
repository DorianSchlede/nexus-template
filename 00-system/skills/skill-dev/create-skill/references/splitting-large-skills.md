# Splitting Large Skills

When SKILL.md approaches 500 lines, split content into references for progressive disclosure.

## The 500-Line Rule

**Limit:** Keep SKILL.md under 500 lines

**Why:**
- Context efficiency (less bloat)
- Progressive disclosure (load only what's needed)
- Faster skill loading
- Easier maintenance

## When to Split

Split when:
- SKILL.md exceeds 400 lines (approaching limit)
- Contains large reference sections (API docs, schemas)
- Supports multiple variants/frameworks
- Has extensive examples or patterns

## Splitting Strategies

### Strategy 1: By Variant

**Use when:** Skill supports multiple tools/frameworks

```
Before: SKILL.md (600 lines)
- Overview (50 lines)
- AWS deployment (200 lines)
- GCP deployment (200 lines)
- Azure deployment (150 lines)

After:
cloud-deploy/
├── SKILL.md (100 lines) - overview + selection
└── references/
    ├── aws.md (200 lines)
    ├── gcp.md (200 lines)
    └── azure.md (150 lines)
```

Claude loads only the relevant variant.

### Strategy 2: By Domain

**Use when:** Skill covers multiple business domains

```
Before: SKILL.md (700 lines)
- Overview (50 lines)
- Finance queries (200 lines)
- Sales queries (200 lines)
- Product queries (250 lines)

After:
bigquery-skill/
├── SKILL.md (100 lines) - navigation
└── references/
    ├── finance.md (200 lines)
    ├── sales.md (200 lines)
    └── product.md (250 lines)
```

Claude loads only the relevant domain.

### Strategy 3: By Feature

**Use when:** Skill has basic + advanced features

```
Before: SKILL.md (550 lines)
- Quick start (100 lines)
- Basic usage (150 lines)
- Advanced features (200 lines)
- API reference (100 lines)

After:
pdf-skill/
├── SKILL.md (250 lines) - quick start + basic usage
└── references/
    ├── advanced.md (200 lines)
    └── api-reference.md (100 lines)
```

Claude loads advanced docs only when needed.

## What to Keep in SKILL.md

**Always keep:**
- Overview and purpose
- Basic workflow
- Navigation to references
- When to use each reference

**Example:**
```markdown
# PDF Processing

## Quick Start

Extract text with pdfplumber:
[basic example]

## Advanced Features

- **Form filling**: See [forms.md](references/forms.md)
- **API reference**: See [api-reference.md](references/api-reference.md)
- **Examples**: See [examples.md](references/examples.md)
```

## What to Move to References

**Move to references/:**
- Detailed API documentation
- Extensive examples
- Schemas and data models
- Framework-specific guides
- Advanced configurations
- Troubleshooting guides

## Reference File Structure

**Keep references one level deep:**
```
✅ Good:
skill/
├── SKILL.md
└── references/
    ├── api-docs.md
    ├── examples.md
    └── schemas.md

❌ Avoid:
skill/
├── SKILL.md
└── references/
    ├── api/
    │   └── endpoints.md
    └── examples/
        └── basic.md
```

**Why:** Claude loads from SKILL.md → references/file.md (one hop). Nested references harder to discover.

## File Size Guidelines

**SKILL.md:** <500 lines
**Reference files:** No hard limit, but consider splitting if >300 lines
**Very large references:** Include table of contents and grep patterns

## Testing Split Skills

After splitting, verify:
- [ ] SKILL.md under 500 lines
- [ ] All references linked from SKILL.md
- [ ] Clear guidance on when to load each reference
- [ ] One level of nesting (no references/subdirs/)
- [ ] Each reference file has clear purpose
- [ ] No duplication between SKILL.md and references

## Example: Before and After

**Before (600 lines):**
```markdown
# BigQuery Skill

[Overview - 50 lines]
[Finance schemas - 150 lines]
[Finance queries - 100 lines]
[Sales schemas - 150 lines]
[Sales queries - 100 lines]
[Setup - 50 lines]
```

**After (100 + 300 + 250 lines):**
```markdown
# BigQuery Skill (SKILL.md - 100 lines)

[Overview]
[Setup]

## Domain References

- **Finance**: See [finance.md](references/finance.md) for schemas and queries
- **Sales**: See [sales.md](references/sales.md) for schemas and queries

## Usage

Mention the domain ("finance metrics", "sales pipeline") and Claude will load the relevant reference.
```

```markdown
# Finance Domain (references/finance.md - 300 lines)

[Schemas]
[Example queries]
[Metrics definitions]
```

```markdown
# Sales Domain (references/sales.md - 250 lines)

[Schemas]
[Example queries]
[Pipeline metrics]
```

## Progressive Disclosure in Action

1. **Startup**: Skill metadata loaded (~100 words)
2. **Skill triggers**: SKILL.md loaded (<5k words)
3. **Domain specified**: Relevant reference loaded (as needed)

**Result:** Only load what's needed for current task.
