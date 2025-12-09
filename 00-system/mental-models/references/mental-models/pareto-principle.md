---
name: "Pareto Principle (80/20 Rule)"
tier: 2
description: "Identify the vital few inputs that produce most outputs to prioritize high-leverage activities. Load for Build/Strategy/Process projects with Simple/Medium complexity when resources limited, need to prioritize features/tasks, or optimize for maximum impact with minimum effort."
applies_to: ["Build", "Strategy", "Process"]
complexity: ["Simple", "Medium"]
---

# Pareto Principle (80/20 Rule)

## Purpose
Identify the vital few (20%) that produce most results (80%) to focus effort on high-leverage activities and eliminate low-value work.

## Core Principle

**The Pareto Principle:** 80% of results come from 20% of efforts

**Examples:**
- 80% of sales from 20% of customers
- 80% of bugs from 20% of features
- 80% of usage from 20% of features
- 80% of value from 20% of work
- 80% of complaints from 20% of issues

**Key Insight:** Not all effort is equal. Most results come from a small fraction of inputs.

---

## The Three-Step Process

### Step 1: Identify All Inputs
List everything that could be done.

**Questions:**
- What are all the features we could build?
- What are all the tasks we could do?
- What are all the customers we could serve?
- What are all the problems we could solve?

**Example - Lead Qualification:**
```
Potential features:
1. AI scoring based on company size
2. AI scoring based on industry
3. AI scoring based on job title
4. LinkedIn profile enrichment
5. Company website analysis
6. Email validation
7. Phone number validation
8. Duplicate detection
9. CRM integration (Salesforce)
10. CRM integration (HubSpot)
11. Slack notifications
12. Email notifications
13. Dashboard analytics
14. Historical trend analysis
15. A/B testing framework
... (30+ potential features)
```

---

### Step 2: Measure Impact
Estimate or measure the value/results of each input.

**Metrics to Consider:**
- Revenue impact
- Time saved
- User satisfaction
- Adoption rate
- Problem solved (severity)
- Strategic value

**Example - Lead Qualification:**
```
Feature Impact Analysis:

HIGH IMPACT (80% of value):
1. AI scoring (company size) → Filters 60% of unqualified leads
2. CRM integration (Salesforce) → Enables actual workflow
3. LinkedIn enrichment → Provides data for scoring
4. Slack notifications → Drives adoption
5. Explainability (show why scored) → Builds trust
6. Override ability → Handles edge cases

MEDIUM IMPACT (15% of value):
7. Dashboard analytics
8. Email notifications
9. Duplicate detection
10. Historical trends

LOW IMPACT (5% of value):
11-30. Everything else (HubSpot, phone validation, A/B testing, etc.)
```

---

### Step 3: Focus on the Vital Few
Ruthlessly prioritize the 20% that drives 80% of results.

**Decision Rules:**
- **DO NOW:** The vital few (20% → 80% results)
- **DO LATER:** Medium impact (if time/resources permit)
- **DON'T DO:** Low impact (nice-to-haves)

**Example Decision:**
```
MUST HAVE (20% → 80% value):
- AI scoring (company size)
- CRM integration (Salesforce)
- LinkedIn enrichment
- Slack notifications
- Explainability
- Override ability

SHOULD HAVE (if time):
- Dashboard analytics
- Duplicate detection

WON'T HAVE (cut):
- HubSpot integration (can add later if needed)
- Phone validation (low value)
- A/B testing (premature optimization)
- 20+ other features
```

---

## Application Frameworks

### Framework 1: Feature Prioritization

**Inputs:** All potential features
**Output:** Ranked list by impact

**Template:**
```markdown
## Feature Pareto Analysis

### Vital Few (Build These)
1. **[Feature]**
   - Impact: [80% of user value / 60% time saved / etc.]
   - Effort: [1 week]
   - ROI: [High impact / Low effort = Top priority]

2. **[Feature]**
   - Impact: [...]
   - Effort: [...]

### Useful Many (Maybe Later)
[Medium impact features]

### Trivial Many (Don't Build)
[Low impact features - cut these]
```

---

### Framework 2: Problem Prioritization

**Inputs:** All customer problems/complaints
**Output:** Focus on root causes

**Pattern:** 80% of complaints come from 20% of root issues

**Example - Lead Qualification:**
```
Customer Complaints (100 total):
- 48 complaints: "AI scores are wrong" → ROOT: Poor data quality
- 32 complaints: "Don't know why lead scored high" → ROOT: No explainability
- 12 complaints: "Notifications too slow" → ROOT: Queue delays
- 8 complaints: Various minor issues

80% of complaints = 2 root causes
Fix those 2 things, eliminate 80% of complaints.
```

---

### Framework 3: Customer Segmentation

**Inputs:** All customers
**Output:** Focus on high-value segments

**Pattern:** 80% of revenue from 20% of customers

**Questions:**
- Which customer segment drives most revenue?
- Which segment has highest retention?
- Which segment costs least to serve?

**Example:**
```
Customer Segments:
- Enterprise (>1000 employees): 20% of customers → 75% of revenue
- Mid-market (100-1000): 50% of customers → 20% of revenue
- SMB (<100): 30% of customers → 5% of revenue

DECISION: Build for Enterprise first, SMB later (or never)
```

---

### Framework 4: Time Allocation

**Inputs:** All activities in your day
**Output:** Focus time on high-leverage activities

**Pattern:** 80% of results from 20% of time spent

**Example - Project Manager:**
```
Time Audit:
- 20% of time: Stakeholder alignment, technical decisions
  → 80% of project value (prevents rework, delays, misalignment)

- 80% of time: Status updates, meetings, admin
  → 20% of project value (necessary but low-leverage)

DECISION: Protect the 20% (block calendar for deep work)
Delegate/automate the 80% (templates, async updates)
```

---

## Pareto Questions Library

### For Features
- Which 20% of features will 80% of users use?
- Which features solve 80% of the user's problem?
- Which features differentiate us from competitors? (vital few)
- Which features are table stakes? (build once, low ongoing value)

### For Customers
- Which 20% of customers generate 80% of revenue?
- Which customers are cheapest to serve?
- Which customers refer the most?
- Which customers churn the least?

### For Problems
- Which 20% of bugs cause 80% of crashes?
- Which 20% of issues generate 80% of support tickets?
- Which root causes drive most symptoms?

### For Effort
- Which 20% of my time produces 80% of my results?
- Which meetings are high-leverage? (keep)
- Which meetings are low-value? (decline)
- Which tasks can I delegate/automate?

---

## Common Patterns

### Pattern 1: The Long Tail
**Observation:** Most features used by <5% of users
**Action:** Build for the head (common use cases), not the tail (edge cases)

**Example - Lead Qualification:**
- 5 core fields (company size, industry, title, revenue, location) → Used for 90% of scoring
- 50 optional fields (employee growth rate, tech stack, funding stage) → Used for 10% of edge cases
- **Decision:** Build 5 core fields first, add others only if needed

---

### Pattern 2: The Vital Bugs
**Observation:** 80% of user frustration from 20% of bugs
**Action:** Fix high-severity bugs first, ignore minor annoyances

**Example:**
- 3 bugs cause 80% of errors:
  1. CRM sync fails (blocks workflow)
  2. AI times out on large files (frustrating)
  3. Slack notification missing (users miss leads)
- 47 bugs cause 20% of frustration (minor UI issues, typos, edge cases)
- **Decision:** Fix the 3 critical bugs, backlog the rest

---

### Pattern 3: The Power Users
**Observation:** 80% of usage from 20% of users
**Action:** Optimize for power users, not average users

**Example - Lead Qualification:**
- 20% of sales reps (top performers) → 80% of lead volume processed
- These reps care about speed, keyboard shortcuts, bulk actions
- Other 80% use basic features occasionally
- **Decision:** Build power features (keyboard shortcuts, bulk edit, advanced filters)

---

### Pattern 4: The Complexity Trap
**Observation:** 80% of complexity from 20% of features
**Action:** Cut complex, low-value features ruthlessly

**Example:**
- Advanced analytics dashboard: 15% of dev time, used by 3% of users
- A/B testing framework: 20% of dev time, marginal value
- Multi-currency support: 10% of dev time, 2 customers need it
- **Decision:** Cut these, keep simple

---

## Anti-Patterns (Common Mistakes)

### 1. False Precision
❌ "We need exactly 80% and exactly 20%"
✅ "Roughly 80/20 - the point is unequal distribution"

**Example:**
- You find 30% of features drive 70% of value
- That's still Pareto! (unequal = useful insight)
- Don't obsess over exact 80/20 split

---

### 2. Ignoring the Long Tail Completely
❌ "Cut everything that's not in the top 20%"
✅ "Prioritize the vital few, but keep some useful many"

**Example:**
- Enterprise customers = 80% of revenue (vital few)
- SMB customers = 20% of revenue (long tail)
- **Wrong:** Cut SMB entirely
- **Right:** Serve Enterprise first, SMB with self-service/automation

---

### 3. Pareto Paralysis
❌ "Can't start until we identify the perfect 20%"
✅ "Start with best guess, refine as you learn"

**Example:**
- You think Feature A is in the vital 20%
- Build it, measure usage
- Turns out it's low-value → Cut it, move on
- Pareto is iterative, not one-time analysis

---

### 4. Only Cutting, Never Adding
❌ "Pareto means always cut features"
✅ "Pareto means focus on high-leverage activities (might mean adding)"

**Example:**
- You spend 80% of time on low-value status updates
- Cut those (delegate, automate)
- Add 20% time on high-value stakeholder alignment
- Result: Better outcomes, same time

---

## Combining Pareto with Other Models

### Pareto + MVP Thinking
**Pattern:** MVP = The 20% that delivers 80% of value

**Example:**
- Full vision: 30 features
- Pareto analysis: 6 features = 80% of value
- MVP: Build those 6 features only
- Result: Ship in 1 month instead of 6 months

---

### Pareto + Pre-Mortem
**Pattern:** Which 20% of risks cause 80% of failures?

**Example - Lead Qualification:**
- Identified 20 potential risks
- 3 risks = 80% of failure probability:
  1. Sales don't trust AI (adoption risk)
  2. CRM data too dirty (technical risk)
  3. Sales manager leaves (organizational risk)
- **Decision:** Mitigate those 3 risks intensely, monitor the rest

---

### Pareto + Stakeholder Mapping
**Pattern:** Which 20% of stakeholders have 80% of influence?

**Example:**
- 15 stakeholders identified
- 3 stakeholders = 80% of decision power:
  1. VP Sales (can kill project)
  2. Sales Manager (drives adoption)
  3. CFO (controls budget)
- **Decision:** Focus engagement on those 3

---

## When to Use

**Best For:**
- ✅ Feature prioritization (what to build)
- ✅ Resource allocation (where to invest)
- ✅ Problem solving (which bugs to fix)
- ✅ Time management (where to focus)
- ✅ Customer segmentation (who to serve)
- ✅ Scope reduction (what to cut)

**Not Ideal For:**
- ❌ Safety-critical systems (can't ignore 80% of bugs)
- ❌ Compliance requirements (must do 100%)
- ❌ When all inputs roughly equal value (rare)
- ❌ Very early exploration (don't know value yet)

**Best Timing:**
- ✅ Feature planning (before building)
- ✅ Scope cuts (over budget/timeline)
- ✅ Performance optimization (which bottleneck to fix)
- ✅ Maintenance (which bugs to fix first)

**Combines Well With:**
- **MVP Thinking** - MVP is the 20% that delivers 80%
- **Pre-Mortem** - Focus on 20% of risks that cause 80% of failures
- **Stakeholder Mapping** - Engage the 20% with 80% influence
- **Systems Thinking** - Find the 20% leverage points with 80% impact

---

## Pareto Analysis Template

```markdown
# Pareto Analysis: [Project/Feature/Problem]

## Step 1: List All Inputs

| Input | Description |
|-------|-------------|
| 1.    |             |
| 2.    |             |
| ...   |             |

## Step 2: Estimate Impact

| Input | Impact Metric | Estimated Value | Effort |
|-------|---------------|-----------------|--------|
| 1.    | [Revenue/Time/Users/etc.] | [High/Med/Low] | [1d/1w/1m] |
| 2.    |                           |                |            |

Sort by: Impact / Effort (ROI)

## Step 3: Pareto Split

### Vital Few (20% → 80% of results)
- [ ] **[Input #1]** - Impact: [...] - Effort: [...] - **DO NOW**
- [ ] **[Input #2]** - Impact: [...] - Effort: [...] - **DO NOW**

### Useful Many (15% → 15% of results)
- [ ] [Input #3] - **MAYBE LATER**
- [ ] [Input #4] - **MAYBE LATER**

### Trivial Many (65% → 5% of results)
- ~~[Input #5]~~ - **DON'T DO**
- ~~[Input #6]~~ - **DON'T DO**

## Decision
**Build:** [List vital few]
**Defer:** [List useful many]
**Cut:** [List trivial many]

**Expected Result:** [80% of value in 20% of time]
```

---

## Quick Pareto (2 Minutes)

**Fast version for simple decisions:**

1. **List top 10 things you could do**
2. **Circle the 2 that would have biggest impact**
3. **Do those 2 first, ignore the rest (for now)**

**Example:**
```
10 possible features:
1. AI scoring ← BIGGEST IMPACT
2. CRM integration ← BIGGEST IMPACT
3. Analytics dashboard
4. Email notifications
5. Phone validation
6-10. [Other features]

Decision: Build #1 and #2 this week. Revisit others later.
```

---

**Remember:** Perfect is the enemy of good. The 20% that's good enough beats the 100% that never ships!
