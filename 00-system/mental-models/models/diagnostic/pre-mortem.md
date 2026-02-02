---
name: Pre-Mortem Analysis
category: diagnostic
description: Identify failure modes before implementation
when_to_use:
  - High-stakes builds
  - Risk mitigation
  - Build planning
  - Launch preparation
best_for: Preventing failures before they happen
---

# Pre-Mortem Analysis

**Purpose**: Identify failure modes before implementation

## The Concept

Unlike a post-mortem (analyzing failure after it happens), a pre-mortem imagines the build has already failed and works backward to identify what went wrong.

## Questions to Ask

- It's [6 months/1 year] from now and this failed. What went wrong?
- What are the most likely causes of failure?
- What would be the early warning signs?
- What could we do NOW to prevent each failure mode?
- What's the single biggest risk?

## Process

1. Set the scene: "Imagine it's the future and this build has failed spectacularly"
2. Each person writes down reasons for the failure (independently)
3. Share and compile all failure modes
4. Prioritize by likelihood and impact
5. For each major failure mode, identify:
   - Early warning signs
   - Prevention measures
   - Mitigation if it happens
6. Build prevention into the plan

## Why It Works

- Gives permission to voice concerns
- Overcomes optimism bias
- Surfaces issues before they become problems
- Creates psychological safety to discuss risks

## Output

Risk inventory with mitigation strategies
