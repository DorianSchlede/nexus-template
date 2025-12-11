# Skill Description Guide

Guidelines for writing effective skill descriptions.

## Purpose

The description field determines when Claude loads your skill. Make it comprehensive and specific - Claude uses this to choose from 100+ skills.

## Format

Single paragraph in YAML frontmatter:

```yaml
---
name: skill-name
description: Clear explanation of what the skill does, when to use it, and key functionality. Include specific terms and contexts.
---
```

## Length

**Optimal:** 100-500 words (typically 2-5 sentences)

**Too short:**
```
❌ PDF tool
❌ Generates reports
```

**Good:**
```
✅ Process PDF documents - rotate pages, extract text, fill forms, and merge files. Use when working with PDF files that need manipulation or data extraction. Supports both single operations and batch processing.
```

## Key Elements

Include these in your description:

1. **What it does** - Core functionality
2. **When to use** - Trigger contexts
3. **Key features** - Main capabilities
4. **Input/output** - What it works with (optional)

## Patterns

### Pattern 1: Functionality + Use Cases

```
Generate comprehensive weekly status reports with completed tasks, decisions made, and next steps. Use when creating status updates, progress summaries, or team reports.
```

### Pattern 2: Domain + Operations

```
BigQuery analytics tool for querying company data warehouse. Access sales metrics, user analytics, and financial reports. Use when analyzing business data or generating insights from database tables.
```

### Pattern 3: Tool Integration + Workflow

```
Slack integration for sending notifications and updates. Post messages to channels, send direct messages, and manage threads. Use when communicating team updates or triggering notifications from automated workflows.
```

## Trigger Terms

Include natural trigger words users might say:

**Document processing:**
- "when working with PDFs", "for document manipulation"

**Reporting:**
- "when creating reports", "for status updates"

**Data analysis:**
- "when analyzing data", "for metrics and insights"

**Communication:**
- "when sending notifications", "for team updates"

## Common Mistakes

1. **Too vague** - "Useful tool for work"
2. **Too technical** - Excessive jargon
3. **Missing context** - No mention of when to use
4. **No key terms** - Lacks discoverability words
5. **Too promotional** - "Amazing", "best", "revolutionary"

## Examples

**Poor:**
```
Works with files and does stuff
```

**Better:**
```
File processor for common operations
```

**Best:**
```
Process various file types - convert formats, compress files, extract metadata, and batch rename. Use when working with multiple files that need standardized operations or format conversions.
```

## Testing Descriptions

Ask: "If I say [user request], would Claude pick this skill?"

**Test cases:**
```
Skill: pdf-editor
Description: "Process PDF documents..."

Test: "Help me rotate this PDF"
Result: ✅ Should match (mentions "process PDF documents")

Test: "Analyze this spreadsheet"
Result: ❌ Shouldn't match (different file type)
```

## V2.0 Spec Compliance

**Only name + description allowed:**
```yaml
---
name: my-skill
description: Your description here
---
```

**No other fields:**
```yaml
---
name: my-skill
description: Description here
type: workflow        # ❌ Remove
triggers: [...]       # ❌ Remove
version: 1.0          # ❌ Remove
---
```

Include trigger terms naturally in the description text instead of separate fields.
