---
name: Fault Tree Analysis
slug: fault-tree-analysis
category: diagnostic
description: Work backward from failures to root causes
when_to_use:
  - Safety analysis
  - Complex system failures
  - Risk assessment
  - Engineering design
best_for: Systematic failure prevention, safety-critical systems
---

# Fault Tree Analysis

**Purpose**: Work backward from failures to root causes

## The Concept

Start with an undesired event (top event) and systematically work backward using logic gates to identify all possible causes and combinations of causes.

## Logic Gates

- **OR Gate**: Failure occurs if ANY input fails (more common)
- **AND Gate**: Failure occurs only if ALL inputs fail (redundancy)

## Questions to Ask

- What must happen for this failure to occur?
- Is this an AND gate (all must happen) or OR gate (any can cause it)?
- What's the probability of each basic event?
- What are the minimal cut sets?
- Which basic events should we focus on preventing?

## Process

1. Define the "top event" (failure you want to prevent)
2. Ask: What could cause this?
3. For each cause, determine if it's AND or OR relationship
4. Continue branching until you reach basic events
5. Calculate probabilities if data available
6. Identify cut sets (combinations that cause failure)
7. Focus prevention on most likely/impactful paths

## Key Concepts

- **Basic events**: Fundamental failures that can't be broken down further
- **Cut sets**: Minimum combinations of basic events that cause top event
- **Minimal cut set**: Smallest combination needed for failure

## Output

Fault tree diagram with probability analysis
