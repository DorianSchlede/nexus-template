---
name: "First Principles Thinking"
tier: 1
description: "Break down complex problems to fundamental truths and rebuild from scratch. Always apply to all projects to challenge assumptions and avoid copying without understanding. Essential for novel problems and innovative solutions."
applies_to: ["Build", "Research", "Strategy", "Content", "Process"]
complexity: ["Simple", "Medium", "Complex"]
---

# First Principles Thinking

## Purpose
Deconstruct problems to their most basic truths and reason up from there, avoiding analogies and conventions that may not apply.

## Core Process

### 1. Identify Current Assumptions
**Purpose:** Surface what you're taking for granted

**Questions to Ask:**
- What do we believe is true about this problem?
- What conventions are we following without questioning?
- What would someone unfamiliar with this domain assume?
- What are we copying from existing solutions?

**Example - Lead Qualification:**
- Assumption: "Qualification must be done by humans"
- Assumption: "It takes 30 minutes per lead"
- Assumption: "We need to ask 10 questions"

---

### 2. Break Down to Fundamental Truths
**Purpose:** Get to indisputable facts

**Questions to Ask:**
- What is absolutely, certainly true?
- What can we verify through evidence/data?
- What remains when we strip away all assumptions?
- What are the physics/laws/constraints that cannot be changed?

**Example - Lead Qualification:**
- **Truth 1:** We need to determine if a lead is likely to buy
- **Truth 2:** Certain signals (company size, budget, urgency) correlate with buying
- **Truth 3:** Information exists somewhere (LinkedIn, website, form responses)
- **Truth 4:** Humans can pattern-match signals to buying likelihood

---

### 3. Question Each Assumption
**Purpose:** Test if assumptions are necessary

**Questions to Ask:**
- Why do we believe this assumption?
- Is this assumption always true?
- What if this assumption is wrong?
- Is this assumption necessary, or just conventional?
- Can we operate without this assumption?

**Example - Lead Qualification:**
- Q: "Why must humans do qualification?"
  - A: "Because nuance and judgment are required"
  - Challenge: "Can AI also apply judgment? Have we tested it?"

- Q: "Why does it take 30 minutes?"
  - A: "Because we research company background, verify fit"
  - Challenge: "Does all research need to be done upfront?"

---

### 4. Rebuild from Fundamentals
**Purpose:** Construct solution using only verified truths

**Questions to Ask:**
- Starting from basic truths, how would we solve this?
- What's the simplest approach that satisfies the fundamentals?
- If we designed this from scratch today, what would it look like?
- What innovations become possible without old assumptions?

**Example - Lead Qualification:**

**Starting from truths:**
1. Need to determine buying likelihood
2. Signals exist in available data
3. Pattern matching is possible

**Rebuild:**
- Instead of: "Human spends 30 min per lead"
- First Principles: "AI extracts signals from data → scores likelihood → human reviews edge cases"
- Result: 2 min per lead (automated) + 5 min for edge cases

---

## Comparison: Analogy vs First Principles

### Reasoning by Analogy
**Pattern:** "We'll do it like [existing solution] does it"

**Example:**
- "Salesforce does qualification this way, so we will too"
- "Other companies use 10-question forms, so we should too"

**Risk:**
- Copies solutions designed for different contexts
- Inherits unnecessary complexity
- Misses opportunities for innovation

### Reasoning by First Principles
**Pattern:** "What is fundamentally required?"

**Example:**
- "Fundamentally, we need to score buying likelihood"
- "What's the minimum information needed to make that determination?"

**Benefit:**
- Designs for YOUR specific context
- Questions unnecessary complexity
- Enables breakthrough innovations

---

## When Analogy is Useful

First Principles isn't always necessary:

**Use Analogy When:**
- ✅ Problem is well-understood and proven solutions exist
- ✅ Industry standards exist for good reasons (security, compliance)
- ✅ Time-constrained and need quick solution
- ✅ The analogy is genuinely similar to your context

**Use First Principles When:**
- ✅ Novel problem without proven solutions
- ✅ Existing solutions feel overly complex
- ✅ You're in a different context than the analogy
- ✅ Innovation is needed
- ✅ Challenging constraints others accepted as fixed

---

## Application Framework

### Step 1: Write Down Current Approach
```
Current Plan:
- Build 10-question form
- Sales rep manually reviews each field
- Research company on LinkedIn
- Score based on gut feel
- Takes 30 minutes
```

### Step 2: Extract Assumptions
```
Assumptions:
1. Need 10 questions
2. Human must do research
3. Scoring is subjective ("gut feel")
4. Must be sequential (qualify before contacting)
```

### Step 3: Identify Fundamentals
```
Fundamental Truths:
1. Need to predict: Will they buy?
2. Signals exist: company size, budget, industry, timing
3. Pattern matching works (proven by ML)
4. We have data sources: form, LinkedIn, website
```

### Step 4: Rebuild
```
First Principles Solution:
1. Capture 3 key signals (not 10): budget, timeline, decision authority
2. AI auto-enriches: company size, industry, tech stack
3. ML model scores: likelihood based on historical conversions
4. Human reviews: Only scores <70% or >90% (edge cases)
5. Result: 2 min automated + 5 min human review for 20% of leads
```

---

## Example: SpaceX Rocket Cost

**Industry Analogy Reasoning:**
- "Rockets cost $100M+ because that's what Boeing/Lockheed charge"
- "Reusable rockets are impossible because no one does it"

**Elon Musk's First Principles:**
1. Fundamental truth: Rocket is aluminum, titanium, carbon fiber, fuel
2. Raw materials cost: ~$2M
3. Question: Why does it cost $100M if materials are $2M?
4. Rebuild: Design for reusability, vertical integration, simplified manufacturing
5. Result: SpaceX reduced costs by 10x

---

## Common Pitfalls

### 1. Confusing Assumptions with Facts
❌ "We need Salesforce integration" (assumption)
✅ "We need to track leads somewhere" (fact)

### 2. Not Going Deep Enough
❌ "We need AI qualification" (still assuming solution)
✅ "We need to predict buying likelihood" (fundamental need)

### 3. Ignoring Practical Constraints
❌ "Ideal solution requires $1M and 6 months"
✅ "What's possible given our constraints?" (pragmatic first principles)

### 4. Reinventing Proven Wheels
❌ "Let's rebuild email from first principles"
✅ "Let's question our qualification process from first principles"

---

## When to Use

**Best For:**
- ✅ All projects (Tier 1 - always apply at start)
- ✅ Novel problems without clear precedent
- ✅ When current solutions feel unnecessarily complex
- ✅ Innovation projects
- ✅ Cost/time optimization challenges
- ✅ Challenging "that's how it's always been done"

**Application Timing:**
- During initial problem framing
- When defining approach in plan.md
- Before committing to expensive/complex solutions
- When stuck or facing constraints

**Combines Well With:**
- **Socratic Questioning** - Use to surface assumptions
- **MVP Thinking** - Build simplest version that satisfies fundamentals
- **Systems Thinking** - Understand fundamentals of system interactions

---

**Remember:** First Principles isn't about being contrarian - it's about understanding WHY before deciding HOW!
