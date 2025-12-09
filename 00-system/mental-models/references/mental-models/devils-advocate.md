---
name: "Devil's Advocate"
tier: 1
description: "Identify risks, blind spots, and failure modes by deliberately arguing against the proposed approach. Always apply to all projects to surface potential problems before they occur."
applies_to: ["Build", "Research", "Strategy", "Content", "Process"]
complexity: ["Simple", "Medium", "Complex"]
---

# Devil's Advocate

## Purpose
Systematically challenge plans and assumptions to identify weaknesses, risks, and blind spots. Play the role of skeptic to strengthen the approach.

## Core Question Types

### 1. Challenge the Approach
**Purpose:** Test if the solution is sound

**Questions to Ask:**
- What could go wrong with this plan?
- Why might this approach fail?
- What are we overlooking?
- What's the weakest part of this design?
- Why shouldn't we do this?

---

### 2. Identify Risks
**Purpose:** Surface potential failure modes

**Questions to Ask:**
- What risks does this introduce?
- What dependencies could break?
- What external factors could derail this?
- What happens if [key assumption] is wrong?
- Where is this most likely to fail?

---

### 3. Challenge Assumptions
**Purpose:** Test critical beliefs

**Questions to Ask:**
- What if users don't behave as expected?
- What if the technology doesn't work as promised?
- What if stakeholders don't buy in?
- What if costs are 10x higher than estimated?
- What if timeline slips by 3 months?

---

### 4. Explore Negative Outcomes
**Purpose:** Imagine worst-case scenarios

**Questions to Ask:**
- What's the worst that could happen?
- How could this backfire?
- What unintended consequences might emerge?
- Could this make things worse?
- What damage could this cause?

---

### 5. Question Resource Availability
**Purpose:** Test feasibility

**Questions to Ask:**
- Do we really have the skills needed?
- Is the budget realistic?
- Can we deliver in this timeframe?
- What if key people leave the project?
- Are we over-committing?

---

### 6. Challenge the "Why"
**Purpose:** Ensure this is worth doing

**Questions to Ask:**
- Is this really solving the core problem?
- Are there cheaper/faster alternatives?
- What if we did nothing instead?
- Is this the highest-priority problem?
- Are we solving a symptom instead of the cause?

---

## Example Application

**Project:** Lead Qualification Workflow

**Challenge Approach:**
- "What if AI misses nuanced enterprise deals that require human judgment?"
- "Why automate this when we could just hire another sales person?"

**Identify Risks:**
- "API costs could spike with high volume - have we budgeted for this?"
- "What if GPT-4 API has downtime during peak hours?"

**Challenge Assumptions:**
- "You assume sales team will trust AI scores - what if they ignore them?"
- "What if leads feel impersonal interaction and conversion drops?"

**Negative Outcomes:**
- "Could this create bias in which leads get attention?"
- "What if automated rejection emails damage brand reputation?"

**Resource Questions:**
- "Do we have AI/integration expertise to maintain this?"
- "What happens when GPT-5 comes out - migration cost?"

**Challenge Why:**
- "Is slow qualification the real bottleneck, or is it low lead quality?"
- "Could we improve lead sources instead of automating bad leads?"

---

## Mitigation Strategy

After identifying risks, document mitigation:

```markdown
**Risk Identified:** AI might miss nuanced enterprise deals
**Mitigation:** Human review for all deals >$50K ARR

**Risk Identified:** API cost spike
**Mitigation:** Cost monitoring + circuit breaker at $500/month
```

---

## When to Use

**Best For:**
- ✅ All projects (Tier 1 - always apply)
- ✅ High-stakes decisions
- ✅ Novel approaches without proven track record
- ✅ Expensive or irreversible commitments
- ✅ Projects with significant risk

**Application Timing:**
- During Approach section (challenge the plan)
- During Risk Assessment
- Before finalizing Key Decisions

---

**Remember:** Playing Devil's Advocate isn't about being negative - it's about making the plan more robust by stress-testing it!
