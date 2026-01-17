---
name: A/B Testing Framework
slug: ab-testing
category: validation
description: Controlled comparison of alternatives
when_to_use:
  - Optimization
  - Feature decisions
  - Marketing
  - UX improvements
best_for: Scientifically validating which option performs better
---

# A/B Testing Framework

**Purpose**: Controlled comparison of alternatives

## The Concept

Compare two variants (A and B) by randomly splitting users and measuring which performs better on a key metric.

## Process

1. **Define hypothesis**: What do you expect and why?
2. **Create variants**: A = control (current), B = treatment (new)
3. **Randomize**: Randomly assign users to A or B
4. **Measure**: Track the key metric
5. **Analyze**: Check for statistical significance
6. **Decide**: Implement winner

## Questions to Ask

- What's the one variable we're changing?
- What metric are we optimizing for?
- What sample size do we need for significance?
- How long should we run the test?
- What will we do if B wins? If A wins?

## Key Concepts

| Term | Definition |
|------|------------|
| **Control (A)** | Current/baseline version |
| **Treatment (B)** | New version being tested |
| **Sample size** | Number of users needed |
| **Statistical significance** | Confidence result isn't random (usually 95%) |
| **Effect size** | Magnitude of the difference |
| **p-value** | Probability result is due to chance |

## Rules for Valid Tests

- Test ONE variable at a time
- Randomize properly
- Don't peek at results early
- Run long enough for significance
- Define success criteria before testing

## Common Mistakes

- Stopping test early when results look good
- Testing too many things at once
- Insufficient sample size
- Not accounting for time-based patterns

## Output

Statistically validated winning variant
