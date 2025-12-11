---
name: better-doc
description: Improve documents for clarity, precision, and impact. Load when user says "better doc", "improve writing", "make clearer", "smart brevity", or provides text asking for style improvements. Uses Classical Style (Pinker) and Smart Brevity (Axios) principles.
---

# Better Doc

Review documents against two complementary frameworks:
- **Classical Style** (Pinker) - Clarity, precision, necessity
- **Smart Brevity** (Axios) - Structure, scannability, impact

Goal: Make text a transparent window to meaning. Brevity is confidence; length is fear.

## Critical Rule: Preserve Substance

**Brevity ≠ Deletion. Simplify the expression, preserve the meaning.**

When reviewing existing documents (especially prompts):

| Do | Don't |
|----|-------|
| Make verbose requirements **more direct** | Delete requirements that seem long |
| Condense wordy explanations | Remove context the reader needs |
| Replace vague terms with **specific** ones | Strip out constraints or edge cases |
| Restructure for clarity | Lose information while restructuring |

**Before cutting anything, ask:**
1. Does this convey a requirement, constraint, or context?
2. Would removing it change the outcome?
3. Can I say the same thing in fewer words instead of deleting?

**For prompts specifically:**
- Requirements buried in paragraphs → Extract as explicit bullet points
- Implicit constraints → Make them explicit, don't assume they're obvious
- Verbose context → Condense, but keep if it affects behavior
- Examples → Keep if they clarify edge cases, cut if redundant

**Wrong approach**: "This paragraph is long, delete it."
**Right approach**: "This paragraph contains 3 requirements. Rewrite as 3 bullet points."

## Core Principles

### Classical Style (8 Principles)

1. **Direct language** - Active voice, clear actors
2. **Necessary content only** - Remove what doesn't improve understanding
3. **No artificial complexity** - Structure serves clarity, not decoration
4. **Specific over abstract** - Concrete, verifiable terms
5. **Consistent terminology** - One name per concept
6. **Clear intent** - Goal, constraints, output format (for prompts)
7. **Reader-first order** - Sequence follows understanding path
8. **Verifiable claims** - Facts and logic, not impressions

### Smart Brevity (4 Components)

1. **Strong headline** - 6 words or fewer, grab attention
2. **One takeaway** - First sentence = the ONE thing to remember
3. **Why it matters** - Context on relevance to the reader
4. **Go deeper** - Optional details, chunked into bullets

For detailed explanations: [references/principles.md](references/principles.md)

## Review Workflow

### Step 1: Classify Document

| Type                   | Focus Areas                           |
| ---------------------- | ------------------------------------- |
| **Email/Update**       | Smart Brevity structure, scannability |
| **Prompt/Instruction** | Intent clarity, constraints, format   |
| **Technical doc**      | Precision, terminology, hierarchy     |
| **General text**       | Classical style, flow, necessity      |

### Step 2: Check Smart Brevity Structure

For emails, updates, announcements:

```
✓ Headline: ≤6 strong words?
✓ First sentence: ONE key takeaway?
✓ "Why it matters": Reader relevance clear?
✓ Details: Bulleted, scannable?
✓ Bold: Key terms highlighted?
```

### Step 3: Check Classical Style

| Principle         | Red Flags                                           |
| ----------------- | --------------------------------------------------- |
| Direct language   | Passive voice, nominalizations, buried verbs        |
| Necessary content | Filler, repetition, obvious statements              |
| No complexity     | Over-formatted, nested bullets, unnecessary headers |
| Specific          | "Various", "aspects", undefined jargon              |
| Consistent terms  | Same thing, different names                         |
| Clear intent      | Missing goal, vague constraints                     |
| Reader order      | Jumping topics, conclusion before context           |
| Verifiable        | "It seems", unsupported claims                      |

### Step 4: Check Word-Level Issues

Smart Brevity word rules:
- **Short words win**: 1 syllable > 2 > 3
- **Cut**: Adverbs, weak words, hedge words
- **Active verbs always**

| Cut This                | Keep/Replace With |
| ----------------------- | ----------------- |
| "In order to"           | "To"              |
| "Due to the fact that"  | "Because"         |
| "At this point in time" | "Now"             |
| "Utilize"               | "Use"             |
| "Implement"             | "Do" / "Build"    |
| "Facilitate"            | "Help" / "Enable" |

### Step 5: Report Findings

```
## Review Summary

**Type**: [email/prompt/technical/general]
**Overall**: [one-line assessment]

## Structure (Smart Brevity)
- Headline: [✓/✗ + fix]
- First sentence: [✓/✗ + fix]
- Why it matters: [✓/✗ + fix]
- Scannability: [✓/✗ + fix]

## Style (Classical)
[List violations with location, problem, fix]

## Suggested Revision
[Improved version if requested]
```

## Quick Reference: Smart Brevity Format

For emails and updates, use this structure:

```
**[6-word headline]**

[ONE sentence: the key takeaway]

**Why it matters**: [1-2 sentences on reader relevance]

**What's next** / **Go deeper** / **The details**:
• [Bullet 1]
• [Bullet 2]
• [Bullet 3]

**Bottom line**: [Optional closing takeaway]
```

## Prompt-Specific Checks

Target structure:
```
Goal: [Single clear statement]

Constraints:
- [Boundary 1]
- [What NOT to do]
- [Length/format limits]

Output Format: [Exact structure]
```

**When improving existing prompts:**

| Original Problem                | Fix (NOT delete)                         |
| ------------------------------- | ---------------------------------------- |
| Requirement buried in prose     | Extract → explicit bullet                |
| Vague constraint ("be careful") | Make specific ("never exceed X")         |
| Implicit assumption             | State explicitly                         |
| Redundant example               | Remove only if another example covers it |
| Long explanation of edge case   | Condense, keep the rule                  |

**Checklist before finalizing:**
- [ ] All original requirements still present?
- [ ] Constraints more explicit than before?
- [ ] Nothing lost in restructuring?
- [ ] Shorter AND clearer (not just shorter)?

Flag: Missing goal, vague terms ("good", "appropriate"), no output format.

## Common Fixes

| Problem | Before | After |
|---------|--------|-------|
| Passive | "Data is processed" | "System processes data" |
| Nominalization | "Make a decision" | "Decide" |
| Filler | "It is important to note" | [delete] |
| Long word | "Utilize" | "Use" |
| Vague | "Various factors" | "Cost, time, scope" |
| Weak headline | "Update on project" | "Project ships Friday" |
| Buried lede | [paragraph before point] | [point first] |
