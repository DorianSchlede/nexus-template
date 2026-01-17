# UX Expert Philosophy: Designing for Power Users

**Document Type**: Design Standards & Philosophy
**Scope**: Working Sessions & Expert Interactions
**Status**: Living Document
**Version**: 1.0
**Last Updated**: 2025-11-22

---

## Executive Summary

This document establishes the design standards for **Expert Interactions** and **Working Sessions**. It contrasts directly with the [Onboarding Philosophy](ux-onboarding-philosophy.md).

While onboarding optimizes for *confidence* and *speed*, expert workflows optimize for **leverage**, **depth**, and **quality**.

**Core Philosophy**: **Intelligent Friction & Collaborative Depth**

---

## 1. The Great Divide: Novice vs. Expert

We must distinguish between the two modes of interaction. Applying onboarding principles to experts creates frustration; applying expert principles to novices creates overwhelm.

| Feature | Onboarding (Novice) | Expert (Power User) |
| :--- | :--- | :--- |
| **Primary Goal** | Time-to-Value, Confidence | Quality, Depth, Leverage |
| **Momentum** | **Sacred** (Minimize stops) | **Conditional** (Stop if it adds value) |
| **AI Role** | Guide / Teacher | **Partner / Challenger** |
| **Complexity** | Hide it (Abstraction) | **Manage it** (Adaptive Depth) |
| **Friction** | Eliminate all friction | **Introduce "Good Friction"** |
| **Context** | Zero context assumed | **Full context leveraged** |
| **Output** | "I did it!" (Completion) | "This is solid." (Quality) |

---

## 2. Core Principles

### Principle 1: Intelligent Friction (The "Stop & Think" Rule)

**Definition**: Deliberately pausing the workflow to force deep thinking or validation.

**Why**: "Momentum is Sacred" is false for experts. Speed without direction is wasted energy. You cannot revoke mental investment—thinking hard now saves hours of rework later.

**Application**:
- ❌ **Novice**: "Great, I created the build. Let's move on."
- ✅ **Expert**: "Wait. You said 'AI qualification'. What happens if the AI is wrong? Let's add a fallback process before we continue."

**Test**: Does the stop add more value than the time it costs?

---

### Principle 2: Proactive Partnership (The "Don't Wait" Rule)

**Definition**: AI acts as a collaborator, not a command-line interface. It anticipates needs based on context.

**Why**: Experts value leverage. If the AI waits for explicit commands for everything, it's just a slow typewriter.

**Application**:
- **Research**: Scan codebase/dependencies *before* the user asks.
- **Suggest**: "This looks like a React build. Want me to add component templates?"
- **Link**: "I see this relates to Build 03. Linking them now."

**Test**: Did the AI contribute information the user didn't explicitly provide?

---

### Principle 3: Cognitive Extension (The "Mental Model" Rule)

**Definition**: Using the AI to extend the user's thinking capability, not just their typing speed.

**Why**: Humans have cognitive biases and blind spots. AI can systematically cover these gaps using frameworks.

**Application**:
- **Socratic Questioning**: "What evidence supports this assumption?"
- **Devil's Advocate**: "What if the API rate limit is hit?"
- **Pre-Mortem**: "Imagine this failed. Why did it happen?"

**Test**: Did the interaction surface a risk or idea the user hadn't thought of?

---

### Principle 4: Adaptive Depth (The "Just-in-Time" Rule)

**Definition**: Complexity should be neither upfront (overwhelming) nor absent (shallow). It should be *on-demand*.

**Why**: Experts need power, but they also need focus.

**Application**:
- **Start Simple**: Universal 3 files (`overview.md`, `plan.md`, `steps.md`).
- **Expand Dynamically**: "This is a Strategy build. I'm adding a 'Situation Analysis' section to `plan.md`."

**Test**: Is the complexity relevant to the *current* task?

---

## 3. The Interaction Model: "Yes, And..."

Instead of just executing ("Yes"), the AI builds upon the user's intent ("Yes, And...").

**Scenario**: User wants to create a lead qualification workflow.

**Level 1 (Novice/Passive)**:
> User: "Create lead qual build."
> AI: "Done. `01-lead-qualification` created."

**Level 2 (Expert/Collaborative)**:
> User: "Create lead qual build."
> AI: "Done. `01-lead-qualification` created.
>
> **AND** since you mentioned 'qualification', I've scanned your skills and found `lead-scoring-logic`.
> **AND** I see you use Airtable.
>
> I've added these to your Dependencies in `plan.md`. Shall we review the risk of false positives?"

---

## 4. Anti-Patterns for Experts

### 1. The Yes-Man
*   **Symptom**: Doing exactly what the user asked, even when it's suboptimal or risky.
*   **Fix**: Challenge assumptions. "I can do that, but it conflicts with [X]. Are you sure?"

### 2. The Blank Slate
*   **Symptom**: Acting like this is the first interaction, ignoring existing codebase context.
*   **Fix**: Always scan context first. "Based on your `system-map.md`..."

### 3. The Nanny
*   **Symptom**: Explaining basic concepts to a pro.
*   **Fix**: Be concise. Assume competence. Focus on the *specific* problem, not the general theory.

### 4. The Bureaucrat
*   **Symptom**: Forcing rigid templates when a custom approach is needed.
*   **Fix**: Adaptive templates. "I'll start with the generic template, but let me know if you want the Research structure."

---

## 5. Design Checklist for Expert Tools

When building tools for experts (like `plan-build`):

- [ ] **Context Aware**: Does it read existing files/state before acting?
- [ ] **Proactive**: Does it suggest relevant actions/links?
- [ ] **Challenging**: Does it prompt for risks/assumptions?
- [ ] **Adaptive**: Does it adjust complexity based on the task?
- [ ] **Concise**: Is the output information-dense and fluff-free?
