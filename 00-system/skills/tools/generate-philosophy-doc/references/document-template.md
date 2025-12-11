# Philosophy Document Template Guide

This document explains the standard structure and purpose of each section in a philosophy document.

## Document Structure Overview

Every philosophy document follows this structure:

1. **Header Section** - Document metadata
2. **Executive Summary** - Core philosophy and proof
3. **Foundational Principles** - 5-8 key principles
4. **Framework & Methodology** - Step-by-step application
5. **Anti-Patterns Dictionary** - Common mistakes
6. **Design Checklists** - Quality assurance tools
7. **Case Studies** - Real-world examples
8. **Measurement Framework** - Success metrics
9. **Research References** - Citations and sources

---

## Section Guidelines

### 1. Header Section

**Purpose**: Provide metadata and navigation

**Must Include**:
- Document title with domain
- Document type, scope, status, version
- Last updated date
- Table of contents with anchor links

**Format**:
```markdown
# [Domain] Philosophy: Design Standards & Best Practices

**Document Type**: Design Standards & Philosophy
**Scope**: [Domain]
**Status**: Living Document
**Version**: 1.0
**Last Updated**: YYYY-MM-DD

## Table of Contents
[numbered list with anchor links]
```

---

### 2. Executive Summary

**Purpose**: Communicate core philosophy in <2 minutes

**Must Include**:
- Core philosophy (1 sentence)
- The problem being solved
- The solution/approach
- Proof or evidence of effectiveness

**Length**: 100-200 words

**Test**: Can reader understand value proposition in 90 seconds?

---

### 3. Foundational Principles

**Purpose**: Establish the "why" behind the philosophy

**Must Include**:
- 5-8 principles (not more, not less)
- Each principle has:
  - Name (concise, memorable)
  - Definition (clear explanation)
  - Why it works (research-backed rationale)
  - Application (wrong vs. right examples)
  - Test (verification method)

**Format Pattern**:
```markdown
### Principle [N]: [Name]

**Definition**: [One sentence]

**Why This Works**: [Research explanation]

**Application**:
- ❌ WRONG: [Example]
- ✅ RIGHT: [Example]

**Test**: [How to verify]
```

**Quality Standards**:
- Each principle is actionable
- Examples are concrete (not abstract)
- Research citations included
- Tests are practical

---

### 4. Framework & Methodology

**Purpose**: Provide step-by-step application guidance

**Must Include**:
- Named framework (memorable name)
- Visual diagram or flowchart
- 3-5 phases/steps
- Each phase includes:
  - Purpose
  - Key activities
  - Quality checklist
  - Time budget

**Format Pattern**:
```markdown
### [Framework Name]

[Visual representation]

#### Phase 1: [Name]

**Purpose**: [What this accomplishes]

**Key Activities**:
- [Bulleted list]

**Quality Checklist**:
- [ ] [Checkbox items]

**Time Budget**: [X%] of process
```

**Quality Standards**:
- Framework is sequential and logical
- Each phase has clear deliverables
- Checklists are specific and measurable
- Visual aids enhance understanding

---

### 5. Anti-Patterns Dictionary

**Purpose**: Document common mistakes to avoid

**Must Include**:
- 5-10 anti-patterns
- Each anti-pattern has:
  - Memorable name
  - Symptom (how to recognize)
  - Example (concrete case)
  - Why it fails (explanation with data)
  - Fix (solution)
  - Metrics (impact data)

**Format Pattern**:
```markdown
### Anti-Pattern [N]: "[Name]"

**Symptom**: [How to recognize]

**Example**:
❌ WRONG:
[Concrete example]

**Why It Fails**: [Explanation with metrics]

**Fix**: [Solution]

**Metrics**: [Impact data]
```

**Quality Standards**:
- Names are memorable and descriptive
- Examples are from real scenarios
- Fixes are actionable
- Impact is quantified where possible

---

### 6. Design Checklists

**Purpose**: Provide practical QA tools

**Must Include**:
- Pre-design checklist
- Mid-design checklist
- Post-design checklist
- Optional: Execution checklist

**Each Checklist Contains**:
- Grouped by category (3-5 groups)
- 3-5 items per group
- Checkbox format
- Specific and measurable items

**Quality Standards**:
- Items are binary (yes/no)
- No ambiguous criteria
- Covers critical quality points
- Can be completed in <10 minutes

---

### 7. Case Studies

**Purpose**: Prove effectiveness with real examples

**Must Include**:
- 2-3 case studies
- Each case study has:
  - Context and background
  - Challenge/problem
  - Approach (how principles applied)
  - Before metrics
  - After metrics
  - Improvement percentages
  - Key insights

**Format Pattern**:
```markdown
### Case Study: [Name]

**Context**: [Background]

**Challenge**: [Problem]

**Approach**: [Application of principles]

**Before**:
- [Metric]: [Value]

**After**:
- [Metric]: [Value] ([X%] improvement)

**Key Insights**:
- [Bulleted insights]
```

**Quality Standards**:
- Real (not hypothetical) examples
- Quantified improvements
- Clear connection to principles
- Actionable insights extracted

---

### 8. Measurement Framework

**Purpose**: Enable success tracking and optimization

**Must Include**:
- Tiered metrics (Tier 1-4 by importance)
- Target values and baselines
- Red flags (critical issues)
- Warning signs
- Measurement methods

**Format Pattern**:
```markdown
### Success Metrics Hierarchy

[Tiered boxes with metrics, targets, baselines]

### Red Flags

🚨 CRITICAL RED FLAGS:
[Conditions requiring immediate action]

⚠️  WARNING SIGNS:
[Conditions suggesting improvements needed]

### Measurement Methods

[How to collect and analyze each metric]
```

**Quality Standards**:
- Metrics are measurable
- Targets are realistic
- Baselines are documented
- Red flags are actionable

---

### 9. Research References

**Purpose**: Provide credibility and further reading

**Must Include**:
- Academic sources (peer-reviewed)
- Industry research (authoritative)
- Best practice documentation

**Organization**:
- Grouped by category
- Proper citation format
- URLs where applicable
- Brief annotations

**Quality Standards**:
- Sources are authoritative
- Citations are complete
- Mix of academic and practical
- Recent (within 5-10 years preferred)

---

## Formatting Guidelines

### Markdown Standards

**Headers**:
- H1 (#): Document title only
- H2 (##): Main sections
- H3 (###): Subsections
- H4 (####): Sub-subsections (use sparingly)

**Emphasis**:
- **Bold**: Section labels, key terms, emphasis
- *Italic*: Occasional emphasis (use sparingly)
- `Code`: Technical terms, commands, file names

**Lists**:
- Bulleted: Related items without order
- Numbered: Sequential steps or ranked items
- Checkboxes: Actionable items for reader

**Visual Elements**:
- Code blocks with language: ```python ... ```
- Blockquotes: > Purpose statements, key quotes
- Tables: Comparison data, metric tracking
- ASCII diagrams: Frameworks, hierarchies

**Separators**:
- `---`: Section breaks
- Blank lines: Between paragraphs and elements

---

## Quality Standards

### Content Quality

**Comprehensiveness**:
- All 8 core sections present
- Each section meets minimum requirements
- No placeholder text in final version

**Clarity**:
- Written for target audience
- Technical terms defined
- Examples are concrete
- No ambiguous language

**Actionability**:
- Principles are applicable
- Checklists are usable
- Framework is followable
- Tests are practical

**Evidence-Based**:
- Research citations included
- Metrics support claims
- Case studies are real
- Data is credible

### Document Quality

**Consistency**:
- Formatting is uniform
- Section structure is parallel
- Voice and tone consistent
- Terminology consistent

**Completeness**:
- TOC matches sections
- Links work correctly
- No [TODO] markers
- No missing references

**Usability**:
- Navigable via TOC
- Scannable (headers, lists, emphasis)
- Searchable (good keywords)
- Printable (reasonable length)

---

## Length Guidelines

**Total Document**: 1,500-3,000 words (typical)

**By Section**:
- Executive Summary: 100-200 words
- Foundational Principles: 400-800 words (80-160 per principle)
- Framework: 400-600 words
- Anti-Patterns: 400-600 words (60-80 per pattern)
- Checklists: 200-400 words
- Case Studies: 300-500 words (150-250 per study)
- Measurement: 300-400 words
- References: 100-200 words

**Note**: These are guidelines. Quality matters more than hitting exact targets.

---

## Adaptation Guidelines

### When to Modify Structure

**Add Sections** when:
- Domain has unique requirements
- Additional frameworks needed
- More context necessary

**Remove Sections** when:
- Section not applicable to domain
- Content would be redundant
- Document becomes too long

**Merge Sections** when:
- Sections overlap significantly
- Better flow achieved
- Simpler structure appropriate

### Domain-Specific Adaptations

**Technical Domains** (API design, architecture):
- Add code examples
- Include technical specifications
- Reference standards (REST, etc.)

**Creative Domains** (UX, design):
- Add visual examples
- Include design systems
- Reference accessibility standards

**Business Domains** (sales, marketing):
- Add ROI calculations
- Include conversion metrics
- Reference industry benchmarks

---

## Version Control

**Version Numbering**:
- 1.0: Initial complete version
- 1.1: Minor updates (typos, clarifications)
- 2.0: Major revisions (new sections, restructure)

**Update Protocol**:
1. Update "Last Updated" date
2. Increment version number
3. Document changes in version history (if maintained)
4. Review all sections for consistency

**Living Document Status**:
- Philosophy docs should evolve with research
- Review quarterly or after major industry changes
- Incorporate feedback and new case studies
- Archive old versions for reference

---

This template ensures consistent, high-quality philosophy documents across all domains.
