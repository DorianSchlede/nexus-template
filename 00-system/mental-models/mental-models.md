---
title: Mental Models Framework
description: System-level catalog of 30+ thinking frameworks for collaborative elicitation, strategic planning, and deep analysis. Loaded on-demand when referenced by create-project, execute-project, and create-skill at decision points. Supports progressive disclosure.
category: thinking-frameworks
load_type: on-demand
referenced_by: [create-project, execute-project, create-skill]
---

# Mental Models Framework

**Purpose**: System-level catalog of thinking frameworks for collaborative work across all skills and projects.

**When to Use**:
- **Requirements gathering**: Stakeholder mapping, first principles, SWOT
- **Design decisions**: Systems thinking, decision matrix, pre-mortem
- **Risk analysis**: Pre-mortem, force field analysis, red team
- **Problem decomposition**: Root cause (5 Whys), fishbone, MECE
- **Strategic planning**: Scenario planning, OKR, blue ocean
- **Creative ideation**: Design thinking, SCAMPER, lateral thinking

---

## Quick Reference

**What This Skill Provides**:
- ✅ **30+ mental models** across 8 categories
- ✅ **Selection guidance** - Which model for which situation
- ✅ **Question templates** - Ready-to-use elicitation questions
- ✅ **Progressive disclosure** - Reference specific models as needed
- ✅ **User choice** - Always offer options, never prescribe
- ✅ **Cross-skill reusability** - Works with create-project, execute-project, create-skill, etc.

---

## Core Principle: Offer Mental Models Proactively

🎯 **GOLDEN RULE**: AI always loads mental-models skill to see what's available, then offers 2-3 relevant models to the user.

**Usage Pattern**:
1. **AI loads mental-models skill** at appropriate decision points
2. **AI reviews catalog** to identify 2-3 relevant models for current context
3. **AI offers models** with descriptive but efficient metadata
4. **User picks** which model(s) to apply
5. **AI loads detailed reference** and applies selected model questions

**Example**:
```
Now let's think through this comprehensively. I've reviewed the mental models catalog and recommend:

1. **First Principles** – Strip assumptions, find fundamental truths
   Best for: Novel projects, challenging assumptions

2. **Stakeholder Mapping** – Identify all affected parties and interests
   Best for: Multi-party projects, organizational work

3. **Pre-Mortem** – Imagine failure modes before implementation
   Best for: High-stakes projects, risk mitigation

Which approach sounds most useful? Or we could combine them!
```

**Pattern**:
- ✅ AI loads this skill automatically at decision points
- ✅ AI offers relevant models with brief, efficient descriptions
- ✅ User chooses which model(s) to apply
- ✅ AI loads detailed reference files only after user selection

**Never**: "I'll use First Principles thinking..." (prescriptive)
**Always**: "I've identified 3 relevant models. Which would you like to use?" (collaborative)

---

## Metadata Format: Descriptive but Efficient

When offering mental models, use this concise format:

**Format**: `**Model Name** – Core action/outcome (3-7 words)`

**Examples**:
- ✅ `**First Principles** – Strip assumptions, find fundamental truths`
- ✅ `**Pre-Mortem** – Imagine failure modes before implementation`
- ✅ `**Stakeholder Mapping** – Identify all affected parties and interests`
- ❌ `**First Principles** – This is a thinking framework where you break down complex problems to their most fundamental truths by stripping away all assumptions...` (too verbose)
- ❌ `**Pre-Mortem** – Failure analysis` (too brief, not descriptive enough)

**Best for**: Add only when context matters (1 line, 5-10 words)
- Example: `Best for: Novel projects, challenging assumptions`
- Example: `Best for: High-stakes projects, risk mitigation`

**Principle**: User should understand what the model does and when to use it from 1-2 lines, not paragraphs.

---

## 8 Categories of Mental Models

### 1. Cognitive Models (4)
**Purpose**: Fundamental thinking frameworks

- **First Principles** - Strip assumptions, find truths
- **Systems Thinking** - Analyze interdependencies
- **Analogous Reasoning** - Apply patterns from similar domains
- **Lateral Thinking** - Generate creative alternatives

### 2. Collaborative Models (3)
**Purpose**: Multi-perspective analysis

- **Six Thinking Hats** - Explore six perspectives
- **MECE Principle** - Mutually Exclusive, Collectively Exhaustive
- **Stakeholder Mapping** - Identify affected parties

### 3. Diagnostic Models (4)
**Purpose**: Root cause identification

- **Root Cause Analysis (5 Whys)** - Drill to fundamentals
- **Fishbone Diagram** - Visual cause-effect analysis
- **Pre-Mortem Analysis** - Identify failure modes
- **Force Field Analysis** - Driving vs restraining forces

### 4. Strategic Models (5)
**Purpose**: Long-term planning

- **Scenario Planning** - Multiple future states
- **OODA Loop** - Observe-Orient-Decide-Act
- **Jobs to Be Done** - Outcome-focused needs
- **Blue Ocean Strategy** - Uncontested market space
- **PESTLE Analysis** - Political, Economic, Social, Tech, Legal, Environmental

### 5. Analytical Models (5)
**Purpose**: Data-driven decisions

- **Decision Matrix** - Multi-criteria evaluation
- **SWOT Analysis** - Strengths, Weaknesses, Opportunities, Threats
- **Cost-Benefit Analysis** - Quantified impact with ROI
- **Pareto Analysis (80/20)** - Prioritization by impact
- **Assumption Testing** - Validate critical assumptions

### 6. Creative Models (4)
**Purpose**: Innovation and ideation

- **Design Thinking** - Empathize-Define-Ideate-Prototype-Test
- **SCAMPER** - Substitute-Combine-Adapt-Modify-Put to use-Eliminate-Reverse
- **Morphological Analysis** - Systematic solution exploration
- **Blue Ocean Strategy** - Value innovation

### 7. Operational Models (4)
**Purpose**: Process optimization

- **Kanban Thinking** - Visualize work, limit WIP, optimize flow
- **Value Stream Mapping** - End-to-end process flow
- **OKR Framework** - Objectives and Key Results
- **Lean Canvas** - One-page business model

### 8. Validation Models (4)
**Purpose**: Testing assumptions

- **Hypothesis Testing** - Scientific method
- **Prototyping** - Build testable representations
- **Pre-Mortem Analysis** - Imagine failure
- **Red Team Analysis** - Adversarial perspective

---

## Progressive Disclosure Pattern

**Keep SKILL.md lean** - Reference detailed models only when needed:

### Pattern 1: Light Reference (Recommended)
```markdown
# In execute-project SKILL.md

## Step 4: Execute with Mental Models (Optional)

Want to apply structured thinking? Load specific models from mental-models skill:

- **Risk analysis**: See mental-models/references/diagnostic-models.md → Pre-Mortem
- **Decision-making**: See mental-models/references/analytical-models.md → Decision Matrix
- **Requirements**: See mental-models/references/cognitive-models.md → First Principles

[Only load if user wants structured approach]
```

### Pattern 2: Full Integration
```markdown
# In create-project SKILL.md

## Step 6: Collaborative Planning

Offer mental models from mental-models skill:
1. Load: mental-models/SKILL.md (categories overview)
2. User picks category
3. Load: mental-models/references/{category}-models.md
4. Apply selected model questions
```

**Benefits**:
- ✅ Avoid duplicating 500+ lines across skills
- ✅ Load only when user wants structured thinking
- ✅ Single source of truth for model updates
- ✅ Reusable across all skills

---

## Quick Selection Guide

### For Requirements Gathering
**Recommend**: First Principles, Stakeholder Mapping, SWOT

**Load**: `references/requirements-models.md`

### For Design & Architecture
**Recommend**: Systems Thinking, Decision Matrix, Pre-Mortem

**Load**: `references/design-models.md`

### For Task Breakdown
**Recommend**: Kanban, OKR, Pareto (80/20)

**Load**: `references/task-models.md`

### For Risk Analysis
**Recommend**: Pre-Mortem, Force Field, Red Team

**Load**: `references/diagnostic-models.md`

### For Strategic Planning
**Recommend**: Scenario Planning, PESTLE, Blue Ocean

**Load**: `references/strategic-models.md`

---

## Reference Files (Progressive Disclosure)

**Core Reference**:
- **[mental-models-catalog.md](references/mental-models-catalog.md)** - Complete 30+ model catalog with detailed questions

**By Use Case**:
- **[requirements-models.md](references/requirements-models.md)** - Models for requirements gathering
- **[design-models.md](references/design-models.md)** - Models for design & architecture
- **[task-models.md](references/task-models.md)** - Models for task breakdown
- **[elicitation-guide.md](references/elicitation-guide.md)** - Question templates and collaborative process

**By Category** (alternative organization):
- **[cognitive-models.md](references/cognitive-models.md)** - First Principles, Systems Thinking, etc.
- **[diagnostic-models.md](references/diagnostic-models.md)** - Root Cause, Pre-Mortem, etc.
- **[strategic-models.md](references/strategic-models.md)** - Scenario Planning, OODA, etc.
- **[analytical-models.md](references/analytical-models.md)** - Decision Matrix, SWOT, etc.

**Choose organization based on context**:
- **Use-case files** when user knows their goal (e.g., "I need to gather requirements")
- **Category files** when user wants to explore models (e.g., "What cognitive models exist?")

---

## Integration Examples

### Example 1: execute-project Integration

**In execute-project/SKILL.md**:
```markdown
## Step 4D: Section Completion Checkpoint (Optional Mental Models)

Before bulk-completing this section, want to apply structured thinking?

Options:
1. Continue without mental models (faster)
2. Apply Pre-Mortem to check for risks
3. Apply Systems Thinking to validate dependencies

If user chooses 2 or 3:
→ Load: mental-models/references/diagnostic-models.md (Pre-Mortem)
→ Load: mental-models/references/cognitive-models.md (Systems Thinking)
```

**Benefits**:
- ✅ Optional (doesn't slow down execution)
- ✅ Contextual (offered at decision points)
- ✅ Progressive (only loads if user wants)

---

### Example 2: create-project Integration

**In create-project/SKILL.md**:
```markdown
## Step 7: Load plan.md → Apply Mental Models

Before filling plan.md, offer mental models from mental-models skill:

1. Load: mental-models/SKILL.md (show categories)
2. User picks 1-2 models
3. Load specific reference file
4. Apply questions from selected models
5. Fill plan.md collaboratively
```

**Benefits**:
- ✅ Single source of truth (mental-models.md)
- ✅ No duplication in create-project
- ✅ Easy updates (change mental-models, all skills benefit)

---

### Example 3: create-skill Integration

**In create-skill/SKILL.md**:
```markdown
## Step 2: Understanding the Skill (Optional Mental Models)

Want to use structured thinking to understand skill requirements?

Load: mental-models/references/requirements-models.md

Recommended: First Principles, Stakeholder Mapping
```

**Benefits**:
- ✅ Applies to skill design
- ✅ Reuses existing catalog
- ✅ Optional enhancement

---

## Anti-Patterns

❌ **Don't**: Select a mental model without offering choice
✅ **Do**: Present 2-3 options and let user pick

❌ **Don't**: Load full catalog into every skill
✅ **Do**: Reference mental-models skill via progressive disclosure

❌ **Don't**: Use jargon without explaining
✅ **Do**: Explain each model briefly when offering

❌ **Don't**: Make it feel like an interrogation
✅ **Do**: Make it collaborative and conversational

❌ **Don't**: Duplicate mental-models.md content in other skills
✅ **Do**: Reference this skill as single source of truth

---

## Success Criteria

**This skill succeeds when**:
- ✅ Users understand which model fits their situation
- ✅ Questions elicit comprehensive thinking
- ✅ Collaboration feels natural, not procedural
- ✅ Other skills can reference without duplication
- ✅ Progressive disclosure prevents context bloat

---

## Version History

**v1.0** (2025-01-22):
- Extracted from create-project skill
- Reorganized for cross-skill reusability
- Added progressive disclosure patterns
- Created use-case and category reference files
- Established user-choice principle

---

**Remember**: Mental models are thinking tools, not rigid processes. Offer choice, collaborate naturally, and adapt to context!
