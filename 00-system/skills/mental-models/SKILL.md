---
name: mental-models
description: Load when user says "mental model", "think through this", "structured thinking", "help me decide", "analyze this problem", "first principles", "pre-mortem", "stakeholder mapping", "what framework should I use", or any specific model name. Provides 30+ thinking frameworks for decision-making, problem decomposition, and strategic analysis.
---

# Mental Models

Apply structured thinking frameworks to decisions, problems, and planning.

## When This Triggers

- "Help me think through X"
- "What mental model should I use?"
- "Apply first principles to this"
- "Do a pre-mortem on this plan"
- "I need to analyze this decision"
- Any specific model name (SWOT, 5 Whys, etc.)

---

## Workflow

### Step 1: Load Mental Models Framework

Load the system mental models catalog:

```
Read: 00-system/mental-models/mental-models.md
```

This provides:
- 30+ models across 8 categories
- Selection guidance for different situations
- Question templates for elicitation

---

### Step 2: Identify Context and Offer Options

Based on user's situation, offer 2-3 relevant models:

**For decisions**: Decision Matrix, Pre-Mortem, Cost-Benefit
**For problems**: First Principles, Root Cause (5 Whys), Fishbone
**For planning**: Scenario Planning, Stakeholder Mapping, OKR
**For creativity**: Design Thinking, SCAMPER, Lateral Thinking
**For risk**: Pre-Mortem, Force Field, Red Team

Present options with brief descriptions (3-7 words each).

---

### Step 3: Load Specific Model Reference

After user selects, load the detailed reference:

| Category | Reference File |
|----------|---------------|
| Cognitive | `00-system/mental-models/references/cognitive-models.md` |
| Diagnostic | `00-system/mental-models/references/diagnostic-models.md` |
| Strategic | `00-system/mental-models/references/strategic-models.md` |
| Analytical | `00-system/mental-models/references/analytical-models.md` |
| Requirements | `00-system/mental-models/references/requirements-models.md` |
| Design | `00-system/mental-models/references/design-models.md` |
| Tasks | `00-system/mental-models/references/task-models.md` |

---

### Step 4: Apply Model Questions

Use the question templates from the loaded reference to guide the user through structured thinking.

Keep it collaborative - this is a conversation, not an interrogation.

---

## Quick Reference

**8 Categories**:
1. Cognitive - First Principles, Systems Thinking, Lateral Thinking
2. Collaborative - Six Hats, MECE, Stakeholder Mapping
3. Diagnostic - 5 Whys, Fishbone, Pre-Mortem, Force Field
4. Strategic - Scenario Planning, OODA, Jobs to Be Done, Blue Ocean
5. Analytical - Decision Matrix, SWOT, Cost-Benefit, Pareto
6. Creative - Design Thinking, SCAMPER, Morphological
7. Operational - Kanban, Value Stream, OKR, Lean Canvas
8. Validation - Hypothesis Testing, Prototyping, Red Team

---

## Notes

- Always offer choice, never prescribe
- Load detailed references only after user selects
- Combine models when appropriate (e.g., First Principles + Pre-Mortem)
- Adapt formality to user's context
