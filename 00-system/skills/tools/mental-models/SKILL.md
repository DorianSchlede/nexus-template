---
name: mental-models
description: Load when user says "mental model", "think through this", "structured thinking", "help me decide", "analyze this problem", "first principles", "pre-mortem", "stakeholder mapping", "what framework should I use", or any specific model name. Provides 59 thinking frameworks for decision-making, problem decomposition, and strategic analysis.
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

### Step 1: Run Mental Models Scanner

Run the script to get all available models:

```bash
python 00-system/mental-models/scripts/select_mental_models.py --format brief
```

This returns JSON with all 59 models across 12 categories.

**Optional filters**:
```bash
# Filter by category
python 00-system/mental-models/scripts/select_mental_models.py --category cognitive --format brief

# List format (names only, grouped by category)
python 00-system/mental-models/scripts/select_mental_models.py --format list
```

---

### Step 2: Identify Context and Offer Options

Based on user's situation, offer 2-3 relevant models:

**For decisions**: Decision Matrix, Pre-Mortem, Cost-Benefit, Inversion
**For problems**: First Principles, Root Cause (5 Whys), Fishbone
**For planning**: Scenario Planning, Stakeholder Mapping, OKR
**For creativity**: Design Thinking, SCAMPER, Lateral Thinking
**For risk**: Pre-Mortem, Force Field, Red Team, Black Swan
**For communication**: Pyramid Principle, BLUF, Steel Manning
**For learning**: Feynman Technique, Deliberate Practice

Present options with brief descriptions (3-7 words each).

---

### Step 3: Load Specific Model File

After user selects, load the individual model file:

**File structure**: `00-system/mental-models/models/{category}/{model-slug}.md`

| Category | Path |
|----------|------|
| Cognitive | `models/cognitive/first-principles.md`, `inversion.md`, etc. |
| Collaborative | `models/collaborative/six-thinking-hats.md`, `mece.md`, etc. |
| Diagnostic | `models/diagnostic/pre-mortem.md`, `five-whys.md`, etc. |
| Strategic | `models/strategic/scenario-planning.md`, `ooda-loop.md`, etc. |
| Analytical | `models/analytical/decision-matrix.md`, `swot-analysis.md`, etc. |
| Creative | `models/creative/design-thinking.md`, `scamper.md`, etc. |
| Operational | `models/operational/kanban-thinking.md`, `okr-framework.md`, etc. |
| Validation | `models/validation/hypothesis-testing.md`, `red-team-analysis.md`, etc. |
| Time & Resource | `models/time-resource/eisenhower-matrix.md`, `opportunity-cost.md`, etc. |
| Communication | `models/communication/pyramid-principle.md`, `bluf.md`, etc. |
| Learning | `models/learning/feynman-technique.md`, `deliberate-practice.md`, etc. |
| Probability & Risk | `models/probability-risk/expected-value.md`, `black-swan-awareness.md`, etc. |

**Example**:
```
User picks: "First Principles + Pre-Mortem"

AI loads:
→ Read: 00-system/mental-models/models/cognitive/first-principles.md
→ Read: 00-system/mental-models/models/diagnostic/pre-mortem.md
```

---

### Step 4: Apply Model Questions

Use the question templates from the loaded model file to guide the user through structured thinking.

Each model file contains:
- **Purpose**: What the model does
- **When to Use**: Best situations for this model
- **Questions to Ask**: Ready-to-use prompts
- **Process**: Step-by-step application
- **Output**: What you get from using it

Keep it collaborative - this is a conversation, not an interrogation.

---

## Quick Reference

**12 Categories (59 Models)**:
1. **Cognitive** - First Principles, Systems Thinking, Lateral Thinking, Inversion, Second-Order Thinking, Analogous Reasoning
2. **Collaborative** - Six Hats, MECE, Stakeholder Mapping, Devil's Advocate
3. **Diagnostic** - 5 Whys, Fishbone, Pre-Mortem, Force Field, Fault Tree
4. **Strategic** - Scenario Planning, OODA, Jobs to Be Done, Blue Ocean, PESTLE, Porter's Five Forces
5. **Analytical** - Decision Matrix, SWOT, Cost-Benefit, Pareto, Assumption Testing, Sensitivity Analysis
6. **Creative** - Design Thinking, SCAMPER, Morphological, Random Entry, Constraint Removal
7. **Operational** - Kanban, Value Stream, OKR, Lean Canvas, Theory of Constraints
8. **Validation** - Hypothesis Testing, Prototyping, Red Team, A/B Testing
9. **Time & Resource** - Eisenhower Matrix, Time Boxing, Opportunity Cost, Sunk Cost, Resource Mapping
10. **Communication** - Pyramid Principle, BLUF, Situation-Complication-Resolution, Steel Manning
11. **Learning** - Feynman Technique, Spaced Repetition, Deliberate Practice, T-Shaped Skills
12. **Probability & Risk** - Expected Value, Margin of Safety, Black Swan, Bayesian Updating, Regret Minimization

---

## Notes

- Always offer choice, never prescribe
- Run script first to see all available models
- Load individual model files only after user selects
- Combine models when appropriate (e.g., First Principles + Pre-Mortem)
- Adapt formality to user's context
