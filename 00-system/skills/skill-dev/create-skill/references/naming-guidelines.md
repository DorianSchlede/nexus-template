# Skill Naming Guidelines

Guidelines for choosing effective skill names.

## Format

**Required:** hyphen-case (lowercase with hyphens)

```
✅ pdf-editor
✅ client-proposal-generator
✅ weekly-status-report
✅ analyze-sales-data

❌ pdf_editor          (underscores)
❌ pdfEditor           (camelCase)
❌ PDF-Editor          (uppercase)
❌ pdf editor          (spaces)
```

## Naming Patterns

### Pattern 1: Verb-Noun (Preferred)

Action + object makes purpose immediately clear.

```
plan-build
generate-report
analyze-data
rotate-pdf
send-email
validate-system
```

### Pattern 2: Noun-Descriptor

Object + characteristic when verb isn't central.

```
pdf-editor
brand-guidelines
data-pipeline
api-client
```

### Pattern 3: Domain-Tool

Domain + tool for specialized integrations.

```
bigquery-analytics
slack-messenger
github-deployer
```

## Length

**Optimal:** 2-4 words (10-30 characters)

**Too short:**
```
❌ pdf          (ambiguous)
❌ report       (what kind?)
```

**Good:**
```
✅ pdf-editor
✅ weekly-report
```

**Too long:**
```
⚠️  generate-comprehensive-weekly-status-report-with-metrics
→  weekly-status-report (simpler)
```

## Specificity

Match name specificity to skill scope:

**Broad skill → General name:**
```
pdf-processor (handles many PDF operations)
```

**Narrow skill → Specific name:**
```
pdf-form-filler (only fills PDF forms)
```

## Common Mistakes

1. **Too generic** - `tool`, `helper`, `utility`
2. **Too specific** - `rotate-pdf-90-degrees-clockwise`
3. **Mixed case** - `PDF-Editor`, `pdfEditor`
4. **Underscores** - `pdf_editor`
5. **Redundant "skill"** - `pdf-editor-skill` (implied)

## Testing Name Quality

Good skill name checklist:
- [ ] Hyphen-case format
- [ ] 2-4 words
- [ ] Action or purpose clear
- [ ] Not too broad or too narrow
- [ ] No redundant words
- [ ] Easy to remember and type

## Examples by Domain

**Document processing:**
- `pdf-editor`, `docx-generator`, `spreadsheet-analyzer`

**Communication:**
- `send-email`, `slack-notifier`, `meeting-scheduler`

**Data operations:**
- `analyze-metrics`, `transform-data`, `query-database`

**Development:**
- `run-tests`, `deploy-app`, `review-code`

**Creative:**
- `generate-presentation`, `create-diagram`, `write-blog-post`
