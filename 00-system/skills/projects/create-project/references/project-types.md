# Project Types & Adaptive Planning Guide

**Purpose**: Guide AI in offering appropriate project types and adapting planning templates based on user needs.

---

## Project Type Categories

When user initiates project creation, AI should offer these categories:

### 1. Build/Create Projects
**Description**: Building something tangible (software, product, system, tool)

**Examples**:
- "Build lead qualification workflow"
- "Create customer dashboard"
- "Develop API integration"

**Adaptive Sections for plan.md**:
- Technical Architecture
- Implementation Strategy
- Integration Points
- Testing Approach

---

### 2. Research/Analysis Projects
**Description**: Investigating, analyzing, or studying something

**Examples**:
- "Analyze competitor landscape"
- "Research market opportunities"
- "Evaluate technology options"

**Adaptive Sections for plan.md**:
- Research Methodology
- Data Sources
- Analysis Framework
- Synthesis Plan

---

### 3. Strategy/Planning Projects
**Description**: Making decisions, planning direction, defining strategy

**Examples**:
- "Q1 marketing strategy"
- "Product roadmap planning"
- "Business model design"

**Adaptive Sections for plan.md**:
- Situation Analysis
- Strategic Options
- Evaluation Criteria
- Decision Framework

---

### 4. Content/Creative Projects
**Description**: Creating content (writing, design, media, campaigns)

**Examples**:
- "Create sales deck"
- "Write product documentation"
- "Design marketing campaign"

**Adaptive Sections for plan.md**:
- Creative Brief
- Target Audience
- Content Strategy
- Production Workflow

---

### 5. Process/Operations Projects
**Description**: Improving processes, documenting workflows, operational changes

**Examples**:
- "Streamline onboarding process"
- "Document support workflow"
- "Optimize deployment pipeline"

**Adaptive Sections for plan.md**:
- Current State Analysis
- Process Design
- Implementation Plan
- Change Management

---

### 6. Generic/Flexible Projects
**Description**: Doesn't fit other categories or user prefers minimal structure

**Examples**:
- "Misc tasks for Q1"
- "Personal learning goals"
- Custom work

**Adaptive Sections for plan.md**:
- Keep minimal base template
- User defines structure as needed

---

## AI Workflow for Project Type Selection

### Step 1: Analyze Project Description

When user says "Create project for [description]", AI should:

1. **Parse description** for keywords
2. **Infer likely type** based on content
3. **Offer suggestion** with option to adjust

**Example**:
```
User: "Create project for lead qualification workflow"

AI: "I'll create a project for lead qualification workflow.

Based on your description, this looks like a **Build/Create** project.
I'll add sections for:
- Technical Architecture
- Implementation Strategy
- Integration Points

Sound good, or would you prefer a different approach?"
```

### Step 2: Confirm or Adjust

User can:
- **Accept**: "Yes" / "Sounds good" → Proceed with suggested type
- **Adjust**: "Actually, this is more research" → Switch to Research type
- **Minimal**: "Keep it simple" → Use generic template

### Step 3: Create with Adaptive Sections

AI creates base structure + adds type-specific sections to plan.md

---

## Mental Models for Collaborative Planning

During planning session, AI should proactively use these thinking frameworks:

### 1. Socratic Questioning

**Purpose**: Help user think deeper about their approach

**Questions to Ask**:
- "What assumptions are you making?"
- "What evidence supports this approach?"
- "How would you know if this assumption is wrong?"
- "What would need to be true for this to work?"

**When to Use**: During "Approach" and "Key Decisions" sections

**Example**:
```
User: "We'll use GPT-4 for lead qualification"

AI: "Good choice. Let me ask: What assumptions are you making about GPT-4's accuracy?
Have you tested it with sample leads? What's your fallback if accuracy is below expectations?"
```

---

### 2. Devil's Advocate

**Purpose**: Identify risks and blind spots

**Questions to Ask**:
- "What could go wrong with this plan?"
- "What are you not considering?"
- "What would make this fail?"
- "Who might disagree with this approach and why?"

**When to Use**: After user defines approach, before finalizing plan

**Example**:
```
User: "Sales team will adopt this immediately"

AI: "Let me play devil's advocate: What if sales team doesn't trust AI qualification?
What if they ignore the notifications? How will you handle resistance to change?"
```

---

### 3. First Principles Thinking

**Purpose**: Break down to fundamental truths

**Questions to Ask**:
- "What's the core problem we're solving?"
- "What are the fundamental constraints?"
- "If we started from scratch, how would we approach this?"

**When to Use**: When user seems stuck or approach feels overly complex

---

### 4. Pre-Mortem Analysis

**Purpose**: Imagine failure and work backward

**Questions to Ask**:
- "Imagine this project failed. What went wrong?"
- "What early warning signs would we see?"
- "How could we prevent that failure?"

**When to Use**: During risk assessment and mitigation planning

---

### 5. Stakeholder Mapping

**Purpose**: Identify all affected parties

**Questions to Ask**:
- "Who will be impacted by this?"
- "Who needs to approve or support this?"
- "Who might resist and why?"

**When to Use**: During Context and Dependencies sections

---

## Adaptive Section Templates

### For Build/Create Projects

```markdown
## Technical Architecture

**System Components**:
- [Component 1] - [Purpose]
- [Component 2] - [Purpose]

**Data Flow**:
[How information moves through the system]

**Technology Stack**:
- [Tool/Framework] - [Why chosen]

## Implementation Strategy

**Development Phases**:
1. [Phase 1] - [Scope]
2. [Phase 2] - [Scope]

**Testing Approach**:
- [How you'll validate]

**Deployment Plan**:
- [How you'll launch]
```

### For Research/Analysis Projects

```markdown
## Research Methodology

**Research Questions**:
- [Question 1]
- [Question 2]

**Data Sources**:
- [Source 1] - [What it provides]
- [Source 2] - [What it provides]

**Analysis Framework**:
[How you'll analyze findings]

## Synthesis Plan

**Reporting Format**:
[How findings will be presented]

**Key Stakeholders**:
[Who needs the insights]
```

### For Strategy/Planning Projects

```markdown
## Situation Analysis

**Current State**:
[Where things stand now]

**Problem Definition**:
[What needs to change]

**Stakeholder Landscape**:
[Who's involved and their interests]

## Strategic Options

**Option 1**: [Approach]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Risks: [What could go wrong]

**Option 2**: [Approach]
- Pros: [Benefits]
- Cons: [Drawbacks]
- Risks: [What could go wrong]

**Recommendation**: [Which option and why]
```

---

## Dependencies & Links Section (MANDATORY)

**CRITICAL**: Every plan.md MUST include this section, populated by AI through research.

### AI's Research Checklist

Before completing plan.md, AI must:

- [ ] **Scan codebase** for related files
- [ ] **Check for related projects** in 02-projects/
- [ ] **Identify related skills** in 03-skills/
- [ ] **Find external system configs** (MCP servers, integrations)
- [ ] **Document all connections** in Dependencies & Links section

### Example Research Process

```
User: "Create project for lead qualification workflow"

AI: [Scans codebase]
    Found:
    - 03-skills/lead-qualification/SKILL.md
    - 04-workspace/airtable-schemas/leads.json
    - .mcp.json (Airtable MCP server configured)
    
    [Checks projects]
    Found:
    - Project 03: CRM Integration (uses same Airtable base)
    
    [Populates Dependencies section]
    **Files Impacted**:
    - `03-skills/lead-qualification/SKILL.md` - Main workflow logic
    - `04-workspace/airtable-schemas/leads.json` - Lead data schema
    
    **External Systems**:
    - Airtable Base: "Leads" - Source of lead data
    - Slack Workspace: #sales - Notification destination
    
    **Related Projects**:
    - Project 03: CRM Integration - Shares Airtable connection
```

---

## Quality Checklist for AI

Before completing project creation, verify:

- [ ] Project type identified and appropriate sections added
- [ ] Socratic questions asked during Approach section
- [ ] Devil's advocate questions asked for risk assessment
- [ ] Dependencies & Links section fully researched and populated
- [ ] All examples are brief and generic (not overly specific)
- [ ] Mental Models Applied section documents thinking frameworks used
- [ ] User has confirmed understanding of approach

---

**Remember**: The goal is **collaborative depth**, not speed. Take time to help user think through their project thoroughly.
