---
name: "MVP Thinking (Lean Startup)"
tier: 2
description: "Build minimum viable version for rapid learning and validation. Load for Build/Strategy projects with Simple/Medium complexity when need to validate assumptions quickly with minimal investment before full commitment."
applies_to: ["Build", "Strategy"]
complexity: ["Simple", "Medium"]
---

# MVP Thinking (Lean Startup)

## Purpose
Build the smallest version that delivers core value and enables learning. Minimize waste, maximize validated learning, and avoid over-engineering.

## Core Principles

### 1. Minimum (Not Minimal)
**What it means:** The smallest thing that enables learning, not the crappiest version

**Questions to Ask:**
- What's the core value proposition?
- What's the riskiest assumption to test?
- What can we cut without losing the learning opportunity?
- What would make this "good enough" to validate?

**NOT MVP:**
- ❌ Poor quality version of final product
- ❌ Prototype that can't be used by real users
- ❌ Feature-complete but buggy

**IS MVP:**
- ✅ Core functionality that solves the main problem
- ✅ Sufficient quality for real usage and feedback
- ✅ Deliberate trade-offs to ship faster

---

### 2. Viable (Actually Works)
**What it means:** Delivers enough value for users to actually use it

**Questions to Ask:**
- Would users actually pay for this (or use it seriously)?
- Does it solve the core problem well enough?
- Is the quality sufficient to get honest feedback?
- Can this provide real value, not just a demo?

**Test:** Would you be embarrassed to show this to users?
- ✅ A little embarrassed about missing features → Good MVP
- ❌ Very embarrassed about quality → Not viable

---

### 3. Product (Something Real)
**What it means:** Real offering users can interact with, not a survey or prototype

**Questions to Ask:**
- Can users actually use this for their real workflow?
- Does this integrate with their existing tools?
- Is this production-ready enough to learn from real usage?

**NOT Product:**
- ❌ Landing page with email signup
- ❌ Survey asking "would you use this?"
- ❌ Powerpoint mockup

**IS Product:**
- ✅ Working software (even if limited scope)
- ✅ Manual process delivered as service
- ✅ Concierge MVP (you do manually what will be automated)

---

## MVP Strategies

### 1. Concierge MVP
**What:** Manually deliver the service you'll automate later

**Example - Lead Qualification:**
- Instead of: Build AI qualification system
- MVP: Sales manager manually scores 20 leads/day using AI prompts
- Learning: Does AI scoring match human judgment? Do sales trust it?
- Cost: 1 day vs 2 weeks development

### 2. Wizard of Oz MVP
**What:** Users think it's automated, but you're doing it manually behind the scenes

**Example - Lead Qualification:**
- Instead of: Fully automated system
- MVP: Form submission triggers email to you → You research lead + email score back
- Learning: Do sales act on the scores? What data do they need?
- Cost: 1 day vs 2 weeks

### 3. Single Feature MVP
**What:** One feature done well, not all features done poorly

**Example - Lead Qualification:**
- Instead of: Full CRM integration + scoring + routing + notifications
- MVP: Just AI scoring, sales manually copies into CRM
- Learning: Is the score accurate and useful?
- Cost: 3 days vs 3 weeks

### 4. Customer Segment MVP
**What:** Solve perfectly for one narrow segment, ignore others

**Example - Lead Qualification:**
- Instead of: Qualify all lead types
- MVP: Only qualify inbound demo requests from companies >100 employees
- Learning: Does scoring work for this segment?
- Cost: 1 week vs 1 month

---

## The Build-Measure-Learn Loop

```
Build MVP → Measure Results → Learn Insights → Pivot or Persevere
    ↑                                                    ↓
    └──────────── Iterate or Pivot ─────────────────────┘
```

### Build
- Fastest path to learning
- Deliberate feature cuts
- "Good enough" quality

### Measure
- Define metrics before building
- Actionable metrics (not vanity metrics)
- Cohort analysis

### Learn
- What assumptions were validated?
- What assumptions were invalidated?
- What unexpected insights emerged?

### Decision
- **Persevere:** Build worked, keep going
- **Pivot:** Build failed, change direction
- **Iterate:** Build partially worked, adjust and retry

---

## MVP Sizing Questions

**80/20 Rule Applied:**
- What 20% of features deliver 80% of the value?
- What 20% of users have 80% of the pain?
- What 20% of the workflow takes 80% of the time?

**Riskiest Assumption Test:**
- What's the #1 thing that could make this fail?
- How can we test THAT assumption first?
- What's the cheapest way to validate it?

**Time Box:**
- What can we build in 1 week that provides learning?
- What can we test in 1 day with 10 users?
- What decision can this MVP help us make?

---

## Example Application

**Project:** Lead Qualification Workflow

**Full Vision:**
- AI analyzes LinkedIn, website, form data, company news
- Integrates with Salesforce, enriches data from 5 sources
- Automated routing to right sales rep
- Slack notifications with full lead summary
- Dashboard with analytics
- **Estimated time:** 6 weeks

**MVP (Week 1):**
- Airtable form captures basics
- Manual GPT-4 prompt qualifies leads
- Score emailed to sales manager
- Sales manager assigns manually
- **What we learn:** Does AI score match human judgment?

**MVP v2 (Week 2 - if v1 works):**
- Automate the GPT-4 scoring (no more manual)
- Add LinkedIn enrichment
- **What we learn:** Does automation work reliably?

**MVP v3 (Week 3 - if v2 works):**
- Add Slack notification
- **What we learn:** Do sales act on notifications?

**Decision Points:**
- Week 1: If AI scores don't match human → **PIVOT** to human-in-loop approach
- Week 2: If automation works → **PERSEVERE** to v3
- Week 3: If Slack ignored → **PIVOT** to email or dashboard

---

## Common MVP Mistakes

### 1. Too Minimum (Not Viable)
❌ "Let's just do a landing page with email signup"
- Doesn't test if solution actually works
- Only tests if problem exists (cheaper ways to do that)

### 2. Too Polished (Not Minimum)
❌ "Let's add this nice-to-have feature before launch"
- Delays learning
- Wastes effort on features users might not want

### 3. Wrong Hypothesis
❌ Building to validate "would users use this?" instead of "does this solve the problem?"
- Test problem/solution fit, not demand
- Demand validation comes after solution validation

### 4. Vanity Metrics
❌ "100 people signed up for our waitlist!"
- Signups ≠ usage
- Track behavior, not interest

---

## When to Use

**Best For:**
- ✅ New product/feature development
- ✅ High uncertainty about user needs
- ✅ Limited resources/time
- ✅ Need to validate before big investment
- ✅ Startup or innovation projects

**Not Ideal For:**
- ❌ Life-critical systems (medical, safety)
- ❌ Regulated industries requiring certification
- ❌ Projects where failure is very costly
- ❌ Maintenance or refactoring (not new builds)

**Combines Well With:**
- **Design Thinking** - MVP aligns with Prototype phase
- **Pre-Mortem** - Identify risks before building MVP
- **Pareto Principle (80/20)** - Find the 20% to build
- **Jobs to Be Done** - Understand the job before building MVP

---

**Remember:** The goal of an MVP is learning, not shipping. If you learned your idea won't work, that's a successful MVP!
