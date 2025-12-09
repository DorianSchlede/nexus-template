---
name: "Pre-Mortem Analysis"
tier: 2
description: "Imagine project failure to identify preventable risks before they occur. Load for Build/Strategy projects with Medium/Complex complexity when stakes are high, multiple dependencies exist, or consequences of failure are severe."
applies_to: ["Build", "Strategy"]
complexity: ["Medium", "Complex"]
---

# Pre-Mortem Analysis

## Purpose
Imagine the project has failed spectacularly, then work backwards to identify what went wrong. Proactively surface risks and failure modes before committing resources.

## Core Concept

**Traditional Risk Analysis:** "What could go wrong?"
**Pre-Mortem:** "The project failed. What happened?"

**Key Insight:** When you assume failure already occurred, your brain generates more specific, actionable risks than hypothetical brainstorming.

---

## The Pre-Mortem Process

### Step 1: Set the Scene
**Timeframe:** Project is complete (6 months from now, 1 year from now, etc.)
**Outcome:** Project failed catastrophically

**Prompt to Use:**
```
"It's [future date]. The [project name] has failed completely.
Not just missed targets - total disaster.
What happened?"
```

**Why This Works:**
- Removes optimism bias
- Makes failure concrete and real
- Activates pattern recognition for problems

---

### Step 2: Individual Silent Brainstorm (5-10 min)
**Instructions:**
- Each person writes down 3-5 specific failure causes
- Write as past tense (it already happened)
- Be specific (not "poor communication" but "sales team didn't find out about launch until 2 days before")

**Questions to Trigger Thinking:**
- What technical failure killed this?
- What organizational/political issue destroyed this?
- What external factor blindsided us?
- What assumption turned out to be completely wrong?
- What dependency failed?
- What did we not know that we should have known?

---

### Step 3: Round-Robin Sharing
**Process:**
1. Each person shares one failure cause
2. Continue until all causes shared
3. Group similar items
4. Identify patterns

**Capture Format:**
```markdown
## Failure Causes

### Technical
- [Specific technical failure that occurred]
- [Another technical failure]

### Organizational
- [People/process failure]
- [Communication breakdown]

### External
- [Market change]
- [Dependency failure]

### Assumptions
- [Wrong assumption #1]
- [Wrong assumption #2]
```

---

### Step 4: Prioritize Risks
**Framework: Likelihood × Impact**

```
High Impact + High Likelihood = CRITICAL (prevent at all costs)
High Impact + Low Likelihood = MONITOR (have contingency)
Low Impact + High Likelihood = MITIGATE (reduce friction)
Low Impact + Low Likelihood = ACCEPT (don't worry)
```

**Questions:**
- Which failure causes are most likely?
- Which would be most catastrophic?
- Which can we actually prevent?

---

### Step 5: Design Preventions
For each critical risk, create a prevention strategy:

**Template:**
```markdown
### Risk: [The specific failure that occurred]

**Early Warning Signs:**
- [Signal 1 that this is starting to happen]
- [Signal 2]

**Prevention:**
- [Action to prevent this risk]
- [Deadline for taking action]

**Contingency (if it happens anyway):**
- [Backup plan if prevention fails]
```

---

## Example Application - Lead Qualification System

### Scenario
"It's 6 months from now. The AI lead qualification system failed completely. Sales team refuses to use it. What happened?"

### Failure Causes Identified

**Technical:**
- AI scoring was 40% accurate, sales lost trust after first week
- CRM integration broke every time Salesforce updated
- System couldn't handle peak lead volume (500+ leads/day during campaign)

**Organizational:**
- Sales team never bought into the system (we built without their input)
- Sales manager left 2 months in, new manager didn't support it
- Marketing kept sending garbage leads, system couldn't score accurately

**External:**
- LinkedIn changed their API, our enrichment broke
- Competitor launched better solution, sales wanted that instead

**Assumptions:**
- We assumed sales would trust AI scores (they don't trust AI)
- We assumed CRM data was clean (it's 60% garbage)
- We assumed 70% accuracy was "good enough" (sales need 90%+)

### Prioritized Risks

**CRITICAL (Prevent at all costs):**
1. **Sales don't trust AI scores (High likelihood, High impact)**
   - Early warning: Sales ask "how did you get this score?" and we can't explain
   - Prevention: Build explainability from day 1, show AI reasoning
   - Deadline: Week 1 of development

2. **CRM data quality too poor for AI (High likelihood, High impact)**
   - Early warning: Sample 100 leads, >30% have bad data
   - Prevention: Data cleaning phase before AI training
   - Deadline: Before training any models

**MONITOR (Contingency ready):**
3. **LinkedIn API changes (Low likelihood, High impact)**
   - Early warning: LinkedIn announces API deprecation
   - Contingency: Have 2 backup enrichment sources ready

**MITIGATE:**
4. **CRM integration breaks (Medium likelihood, Medium impact)**
   - Prevention: Build retry logic, error handling from start

**ACCEPT:**
5. **Competitor launches better solution (Low likelihood, Low impact)**
   - We can switch if needed, not critical to prevent

---

## Pre-Mortem Questions Library

### Technical Failure
- What broke at 2am that nobody knew how to fix?
- What integration failed silently for weeks?
- What performance issue made the system unusable?
- What security vulnerability did we miss?
- What data corruption destroyed everything?

### Organizational Failure
- Which key person left and took critical knowledge?
- What political battle killed the project?
- Which stakeholder turned against us and why?
- What communication breakdown caused misalignment?
- Which team refused to adopt the solution?

### Assumption Failure
- What did we assume about users that was completely wrong?
- What did we assume about the technology that failed?
- What market assumption proved false?
- What timeline assumption was unrealistic?

### External Failure
- What external dependency failed?
- What market shift made this irrelevant?
- What regulation changed and blocked us?
- What competitor move destroyed our advantage?

### Resource Failure
- What resource constraint killed us (time, money, people)?
- What skill did we not have that we needed?
- What tool/technology didn't exist or didn't work?

---

## Pre-Mortem vs Other Approaches

### Pre-Mortem vs Traditional Risk Analysis
**Traditional:**
- "What risks might we face?"
- Generates generic risks ("scope creep", "resource constraints")
- Easy to dismiss ("we'll handle it")

**Pre-Mortem:**
- "It failed. What happened?"
- Generates specific scenarios ("Sales manager left, new manager killed project")
- Harder to dismiss (concrete and vivid)

### Pre-Mortem vs Devil's Advocate
**Devil's Advocate:** Argues against current approach
**Pre-Mortem:** Assumes current approach failed

**When to use each:**
- Devil's Advocate: During planning (challenge approach)
- Pre-Mortem: After approach decided (identify execution risks)

---

## Anti-Patterns (Common Mistakes)

### 1. Too Generic
❌ "Poor planning led to failure"
✅ "We didn't allocate 2 weeks for data cleaning, so AI trained on garbage data and never worked"

### 2. Solutions in Disguise
❌ "We failed because we didn't use Kubernetes"
✅ "System couldn't scale past 100 leads/day, sales stopped using it"

### 3. Blaming Others
❌ "Sales team was lazy and didn't adopt"
✅ "We didn't involve sales in design, built wrong features, they rejected it"

### 4. Not Specific Enough
❌ "Integration issues"
✅ "Salesforce API rate limit hit after 1000 leads, system queued for 6 hours, sales missed hot leads"

---

## When to Use

**Best For:**
- ✅ High-stakes projects (expensive, visible, critical)
- ✅ Complex projects with many dependencies
- ✅ Projects with severe failure consequences
- ✅ Teams prone to optimism bias
- ✅ Projects with unclear requirements
- ✅ Before committing significant resources

**Not Ideal For:**
- ❌ Low-stakes experiments (overkill)
- ❌ Well-understood, routine projects
- ❌ Very early exploration (too soon to imagine failure)
- ❌ Teams already paralyzed by fear (adds more anxiety)

**Best Timing:**
- ✅ After planning, before execution
- ✅ Before major milestones/releases
- ✅ When deciding to pivot or persevere

**Combines Well With:**
- **Devil's Advocate** - Challenge approach, then imagine execution failure
- **Systems Thinking** - Identify feedback loops that could cause failure
- **Stakeholder Mapping** - Identify which stakeholders could kill project
- **Design Thinking** - Test phase validates pre-mortem assumptions

---

## Pre-Mortem Template

```markdown
# Pre-Mortem: [Project Name]

## Scenario
It's [DATE]. The [PROJECT] has failed completely. [Describe catastrophic outcome]

## Failure Causes (Individual Brainstorm)

### Technical Failures
-
-

### Organizational Failures
-
-

### Assumption Failures
-
-

### External Failures
-
-

### Resource Failures
-
-

## Prioritized Risks

### CRITICAL (Prevent at all costs)
1. **[Risk]**
   - Likelihood: High/Medium/Low
   - Impact: High/Medium/Low
   - Early Warning Signs: [...]
   - Prevention: [...]
   - Contingency: [...]

### MONITOR (Contingency ready)
[...]

### MITIGATE
[...]

### ACCEPT
[...]

## Action Items
- [ ] [Prevention action] - Owner: [...] - Deadline: [...]
- [ ] [Prevention action] - Owner: [...] - Deadline: [...]
```

---

**Remember:** A good pre-mortem makes you uncomfortable. If everyone feels relaxed afterwards, you didn't go deep enough!
