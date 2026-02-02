---
name: mental-models
description: "mental model, think through this, help me decide, first principles, pre-mortem."
---

# Mental Models

Apply structured thinking frameworks to decisions, problems, and planning.

## Workflow

### Step 1: Run Scanner

```bash
uv run nexus-mental-models --format brief
```

Output shows slugs by category with path pattern:
```
# Path: 00-system/mental-models/models/{category}/{slug}.md
analytical: decision-matrix, swot-analysis, cost-benefit-analysis...
diagnostic: pre-mortem, five-whys, fishbone-diagram...
```

### Step 2: Select & Load

Based on user's context, pick 1-2 models and load using the path pattern:

```
Read: 00-system/mental-models/models/diagnostic/pre-mortem.md
```

### Step 3: Apply

Each model file contains purpose, questions, and process. Guide user through it.

---

## Quick Reference

| Situation | Models |
|-----------|--------|
| Decisions | decision-matrix, inversion, cost-benefit-analysis |
| Problems | first-principles, five-whys, fishbone-diagram |
| Planning | pre-mortem, scenario-planning, stakeholder-mapping |
| Risk | pre-mortem, inversion, margin-of-safety |

---

## Rules

1. **Run scanner first** - don't guess slugs
2. **Use path pattern** - `models/{category}/{slug}.md`
3. **Let user pick** - suggest, don't impose
