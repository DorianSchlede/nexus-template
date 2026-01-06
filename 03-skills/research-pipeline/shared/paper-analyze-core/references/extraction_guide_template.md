# Extraction Guide Template

**Purpose**: Ensure consistent extraction quality and format across all papers in a research project.

**Usage**:
1. Copy this template to `02-resources/_extraction_guide.md` in your project
2. Populate with project-specific field examples
3. Subagents read this before analyzing papers

---

## Format Rules

### Data Types

| Type | When to Use | Format |
|------|-------------|--------|
| **Array of strings** | Multiple discrete items | `["Item 1", "Item 2", "Item 3"]` |
| **Array of objects** | Items with properties | `[{name: "X", source: "Chunk 2"}]` |
| **String** | Single value or paragraph | `"Description here"` |
| **null** | Field not applicable to paper type | `null` |

### Empty vs N/A

| Situation | Use |
|-----------|-----|
| Paper doesn't discuss this topic | `"N/A - not discussed in paper"` |
| Topic discussed but no specific finding | `[]` (empty array) or `""` (empty string) |
| Searched but couldn't find | `"N/A - no relevant content found"` |
| Field doesn't apply to paper type | `null` with note in limitations |

**Never leave a field undefined** - always explicit about why empty.

---

## Extraction Quality Criteria

### DO

- Use exact terminology from the paper
- Include chunk reference for every extraction: `(Chunk 3)`
- Quote significant definitions: `"Author defines X as..."`
- Be specific: `"3-layer architecture"` not `"multi-layer"`
- Standardize to controlled vocabulary when applicable

### DON'T

- Paraphrase when exact quote is better
- Merge distinct concepts into one extraction
- Infer what paper doesn't explicitly state
- Use generic descriptions: `"discusses various methods"`
- Forget chunk references

---

## Controlled Vocabulary Principles

When the paper uses synonyms, standardize to ONE term:

```
# Example pattern
| Paper Uses | Standardize To |
|------------|----------------|
| "method A", "approach A", "technique A" | "Method A" |
| "framework", "system", "architecture" | Choose most specific |
```

**Rules:**
1. Prefer the term the paper uses most frequently
2. If paper defines a term formally, use that definition
3. Capitalize proper nouns and framework names
4. Use singular form for entity types

---

## Confidence Levels

Mark each extraction with confidence:

| Level | When to Use |
|-------|-------------|
| **high** | Explicit statement, direct quote available |
| **medium** | Clear implication, consistent with context |
| **low** | Inference, interpretation, ambiguous source |

**Always flag low confidence**: `[LOW CONFIDENCE: reason]`

---

## Handling Uncertainty

### Ambiguous Content

```yaml
# GOOD
field_name:
  - value: "Pattern X"
    note: "[AMBIGUOUS: Could refer to X or Y, context suggests X]"

# BAD
field_name:
  - "Pattern X"  # No indication of uncertainty
```

### Missing Information

```yaml
# GOOD
field_name: "N/A - paper focuses on Y, does not discuss X"

# BAD
field_name: ""  # Why is it empty?
```

### Contradictory Statements

```yaml
# GOOD
field_name:
  - value: "A is true"
    source: "Chunk 2"
  - value: "A is false"
    source: "Chunk 5"
    note: "[CONTRADICTION: Authors state opposite in different sections]"
```

---

## Example Extractions

### Good Extraction (Array of Objects)

```yaml
methods:
  - name: "Six-Phase Framework"
    description: "Iterative process for thematic analysis"
    source: "Chunk 2:45-67"
    quote: "The process involves six phases: familiarization..."
    confidence: "high"
```

### Good Extraction (Array of Strings)

```yaml
topics:
  - "thematic analysis methodology"
  - "qualitative coding"
  - "theme development"
# All found in Chunk 1
```

### Bad Extraction

```yaml
methods:
  - "various analysis methods"  # Too vague
  - "the framework"  # Which framework?
  - "discussed in paper"  # Not an extraction
```

---

## Field-Specific Instructions

**[PROJECT MUST POPULATE THIS SECTION]**

For each field in `_briefing.md`, add:

```markdown
### Field: {field_name}

**Definition**: What this field captures

**Format**: Array of strings | Array of objects | String

**Priority**: high | medium

**Example GOOD extraction**:
{example}

**Example BAD extraction**:
{example}

**Controlled vocabulary** (if applicable):
| Term | Use When |
|------|----------|
```

---

## Validation Checklist

Before completing analysis, verify:

- [ ] All high-priority fields have at least one extraction OR explicit N/A
- [ ] Every extraction has chunk reference
- [ ] Controlled vocabulary applied consistently
- [ ] Low confidence items flagged
- [ ] No undefined/empty fields without explanation
- [ ] Format matches specification (arrays vs strings vs objects)

---

**Version**: 1.0 (2025-12-28)
