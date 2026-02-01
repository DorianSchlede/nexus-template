---
name: mental-models
description: "mental model, think through this, help me decide, first principles, pre-mortem."
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

### Step 1: MANDATORY - Run Mental Models Scanner First

**ALWAYS run this script first** to see all available models with their paths:

```bash
uv run nexus-mental-models --format brief
```

Output format (grouped by category):
```json
{
  "diagnostic": [
    {
      "name": "Pre-Mortem Analysis",
      "description": "Identify failure modes before implementation",
      "path": "00-system/mental-models/models/diagnostic/pre-mortem.md"
    }
  ]
}
```

**Optional filters**:
```bash
# Filter by category
uv run nexus-mental-models --category cognitive --format brief

# Names only (quick reference)
uv run nexus-mental-models --format list
```

---

### Step 2: Select Models for the Situation

Based on user's context, suggest 2-3 relevant models from the script output:

| Situation | Recommended Models |
|-----------|-------------------|
| **Decisions** | Decision Matrix, Pre-Mortem, Cost-Benefit, Inversion |
| **Problems** | First Principles, Root Cause (5 Whys), Fishbone |
| **Planning** | Scenario Planning, Stakeholder Mapping, OKR |
| **Creativity** | Design Thinking, SCAMPER, Lateral Thinking |
| **Risk/Verification** | Pre-Mortem, Inversion, Red Team, Assumption Testing |
| **Communication** | Pyramid Principle, BLUF, Steel Manning |
| **Learning** | Feynman Technique, Deliberate Practice |

Present options with descriptions from the script output.

---

### Step 3: Load Model Files Using Paths from Script

Use the `path` field from the script output to load the model:

```
User picks: "Pre-Mortem + Inversion"

AI loads (using paths from script):
-> Read: 00-system/mental-models/models/diagnostic/pre-mortem.md
-> Read: 00-system/mental-models/models/cognitive/inversion.md
```

**Do NOT guess paths** - always use the paths from the script output.

---

### Step 4: Apply Model Questions

Each model file contains:
- **Purpose**: What the model does
- **Questions to Ask**: Ready-to-use prompts
- **Process**: Step-by-step application
- **Output**: What you get from using it

Guide the user through the questions collaboratively.

---

## Categories (59 Models)

1. **analytical** - Decision Matrix, SWOT, Cost-Benefit, Pareto, Assumption Testing, Sensitivity
2. **cognitive** - First Principles, Inversion, Systems Thinking, Lateral Thinking, Second-Order, Analogous
3. **collaborative** - Six Hats, MECE, Stakeholder Mapping, Devil's Advocate
4. **communication** - Pyramid Principle, BLUF, SCR, Steel Manning
5. **creative** - Design Thinking, SCAMPER, Morphological, Random Entry, Constraint Removal
6. **diagnostic** - 5 Whys, Fishbone, Pre-Mortem, Force Field, Fault Tree
7. **learning** - Feynman Technique, Spaced Repetition, Deliberate Practice, T-Shaped
8. **operational** - Kanban, Value Stream, OKR, Lean Canvas, Theory of Constraints
9. **probability-risk** - Expected Value, Margin of Safety, Black Swan, Bayesian, Regret Minimization
10. **strategic** - Scenario Planning, OODA, JTBD, Blue Ocean, PESTLE, Porter's Five Forces
11. **time-resource** - Eisenhower Matrix, Time Boxing, Opportunity Cost, Sunk Cost, Resource Mapping
12. **validation** - Hypothesis Testing, Prototyping, Red Team, A/B Testing

---

## Critical Rules

1. **ALWAYS run the script first** - never guess which models exist
2. **Use paths from script output** - never hardcode paths
3. **Offer choice** - let user pick which model(s) to apply
4. **Combine models** when appropriate (e.g., Pre-Mortem + Inversion for risk analysis)
5. **Be collaborative** - this is a conversation, not an interrogation
