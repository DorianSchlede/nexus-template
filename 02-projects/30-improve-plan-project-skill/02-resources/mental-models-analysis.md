# Mental Models Analysis for plan-project

**Purpose**: Document how mental models should be applied in project planning

---

## When to Inject Mental Models

**Answer**: BEFORE type-specific discovery, AFTER type detection

```
User: "create project for Slack integration"
    │
    ├── Step 1: Type Detection → "integration"
    │
    ├── Step 2: MENTAL MODELS (HERE!)
    │   ├── First Principles: "What's the core problem?"
    │   ├── Socratic: "What assumptions are you making?"
    │   ├── Devil's Advocate: "What could go wrong?"
    │   ├── Pre-Mortem: "Imagine this failed - why?"
    │   └── Success Criteria: "How will you know it worked?"
    │
    ├── Step 3: Create project structure
    │
    └── Step 4: Route to add-integration for API discovery
```

**Why here?**
1. Mental models help FRAME the problem correctly
2. Success criteria should exist BEFORE discovery
3. Devil's advocate catches bad assumptions EARLY
4. User is still engaged (not deep in technical details yet)

---

## Mental Models from project-types.md

### 1. Socratic Questioning
**Purpose**: Help user think deeper
**Questions**:
- "What assumptions are you making?"
- "What evidence supports this approach?"
- "How would you know if this assumption is wrong?"
- "What would need to be true for this to work?"

**When**: During success criteria definition

### 2. Devil's Advocate
**Purpose**: Identify risks and blind spots
**Questions**:
- "What could go wrong with this plan?"
- "What are you not considering?"
- "What would make this fail?"
- "Who might disagree and why?"

**When**: After user defines initial approach

### 3. First Principles Thinking
**Purpose**: Break down to fundamentals
**Questions**:
- "What's the core problem we're solving?"
- "What are the fundamental constraints?"
- "If starting from scratch, how would we approach this?"

**When**: When approach feels overly complex

### 4. Pre-Mortem Analysis
**Purpose**: Imagine failure and work backward
**Questions**:
- "Imagine this project failed. What went wrong?"
- "What early warning signs would we see?"
- "How could we prevent that failure?"

**When**: During risk assessment

### 5. Stakeholder Mapping
**Purpose**: Identify all affected parties
**Questions**:
- "Who will be impacted by this?"
- "Who needs to approve or support this?"
- "Who might resist and why?"

**When**: During context definition

---

## Type-Specific Mental Model Focus

| Project Type | Primary Models | Why |
|--------------|----------------|-----|
| Integration | Devil's Advocate, First Principles | API changes, breaking dependencies |
| Research | Socratic, Pre-Mortem | Bias in research questions, scope creep |
| Build | First Principles, Stakeholder | Over-engineering, missing requirements |
| Strategy | All models | High-stakes decisions |
| Content | Stakeholder, Socratic | Audience fit, message clarity |
| Process | Pre-Mortem, Stakeholder | Change resistance, edge cases |

---

## Implementation in plan-project

### Mental Model Step Template
```markdown
## Step 2: Mental Model Application

Before diving into discovery, let's think through this project carefully.

### 2.1 First Principles
What's the CORE problem you're solving?
[User response or AI guided discussion]

### 2.2 Success Criteria
How will you know this project succeeded?
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]

### 2.3 Devil's Advocate
What could make this fail?
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk 1] | | | |

### 2.4 Stakeholders
Who cares about this project?
- [Stakeholder 1]: [Their interest]

---
Mental models complete. Proceeding to type-specific discovery...
```

---

## Integration with Existing Skills

When routing to specialized skills, pass mental model outputs:
```yaml
# Passed to add-integration or create-research-project
mental_models:
  core_problem: "User needs Slack notifications for lead updates"
  success_criteria:
    - "Leads posted to #sales within 30 seconds"
    - "Include lead score and source"
  risks:
    - "Slack API rate limits"
    - "Message formatting edge cases"
  stakeholders:
    - "Sales team (receivers)"
    - "Marketing (lead source)"
```

This context helps the specialized skill make better decisions during discovery.
