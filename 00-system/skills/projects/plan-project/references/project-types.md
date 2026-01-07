# Project Types & Adaptive Planning Guide

**Purpose**: Guide AI in offering appropriate project types and adapting planning templates based on user needs.

**Router Pattern**: plan-project semantically matches user input against _type.yaml descriptions.

---

## 8 Project Types

| Type | When to Use | Discovery Method |
|------|-------------|------------------|
| **build** | Creating software, features, tools, systems | Inline |
| **integration** | Connecting APIs, external services, webhooks | Skill: add-integration |
| **research** | Academic papers, systematic analysis | Skill: create-research-project |
| **strategy** | Business decisions, planning, analysis | Inline |
| **content** | Marketing, documentation, creative work | Inline |
| **process** | Workflow optimization, automation | Inline |
| **skill** | Creating Nexus skills and capabilities | Skill: create-skill |
| **generic** | Doesn't fit other categories | Inline |

---

## Type Descriptions

### 1. Build Projects

**Description**: Building something tangible (software, product, system, tool)

**Examples**:
- "Build lead qualification workflow"
- "Create customer dashboard"
- "Develop authentication system"

**Discovery Method**: Inline (EARS requirements format)

**Adaptive Sections for plan.md**:
- Technical Architecture
- Implementation Strategy
- Integration Points
- Testing Approach

**Special Features**:
- EARS-formatted requirements in discovery.md
- Correctness Properties in plan.md
- INCOSE quality rules applied

---

### 2. Integration Projects

**Description**: Connecting external APIs and services to Nexus

**Examples**:
- "Add Slack integration"
- "Connect HubSpot API"
- "Integrate payment gateway"

**Discovery Method**: Skill (add-integration)

**What add-integration does**:
- WebSearch for API documentation
- Parse endpoints and auth methods
- User selects which endpoints to implement
- Creates integration config JSON

**Adaptive Sections for plan.md**:
- API Architecture
- Authentication Flow
- Endpoint Mapping
- Error Handling Strategy

---

### 3. Research Projects

**Description**: Systematic investigation and analysis of academic papers or topics

**Examples**:
- "Research ontology comparison"
- "Analyze AI agent frameworks"
- "Survey knowledge graph approaches"

**Discovery Method**: Skill (create-research-project)

**What create-research-project does**:
- Define research question and extraction schema
- Search 9 academic APIs
- Download and preprocess papers
- Generate analysis kit for synthesis

**Adaptive Sections for plan.md**:
- Research Methodology
- Data Sources
- Analysis Framework
- Synthesis Plan

---

### 4. Strategy Projects

**Description**: Making decisions, planning direction, defining strategy

**Examples**:
- "Q1 marketing strategy"
- "Product roadmap planning"
- "Business model design"

**Discovery Method**: Inline (decision framework questions)

**Adaptive Sections for plan.md**:
- Situation Analysis
- Strategic Options
- Evaluation Criteria
- Decision Framework

---

### 5. Content Projects

**Description**: Creating content (writing, design, media, campaigns)

**Examples**:
- "Create sales deck"
- "Write product documentation"
- "Design marketing campaign"

**Discovery Method**: Inline (creative brief questions)

**Adaptive Sections for plan.md**:
- Creative Brief
- Target Audience
- Content Strategy
- Production Workflow

---

### 6. Process Projects

**Description**: Improving processes, documenting workflows, operational changes

**Examples**:
- "Streamline onboarding process"
- "Document support workflow"
- "Optimize deployment pipeline"

**Discovery Method**: Inline (current/future state questions)

**Adaptive Sections for plan.md**:
- Current State Analysis
- Process Design
- Implementation Plan
- Change Management

---

### 7. Skill Projects (NEW)

**Description**: Creating new Nexus skills and automation capabilities

**Examples**:
- "Create Slack power skill"
- "Build data extraction skill"
- "Develop meeting notes automation"

**Discovery Method**: Skill (create-skill)

**What create-skill does**:
- Skill-worthiness assessment (3-criteria framework)
- Define triggers and complexity
- Scaffold skill structure
- Generate SKILL.md and references

**Adaptive Sections for plan.md**:
- Skill Architecture
- Trigger Design
- Workflow Steps
- Testing Strategy

**Special Features**:
- EARS-formatted requirements in discovery.md
- Correctness Properties in plan.md
- Follows skill-format-specification.md

---

### 8. Generic Projects

**Description**: Doesn't fit other categories or user prefers minimal structure

**Examples**:
- "Misc tasks for Q1"
- "Personal learning goals"
- Custom work

**Discovery Method**: Inline (minimal questions)

**Adaptive Sections for plan.md**:
- Keep minimal base template
- User defines structure as needed

---

## Type Detection (Semantic Matching)

The router does NOT use keyword triggers. Instead:

1. **Read all _type.yaml descriptions**
2. **Compare user input semantically** against descriptions
3. **Select best match** OR ask user if ambiguous

**Example**:
```
User: "plan project for slack notifications"

AI reads _type.yaml descriptions:
- integration: "Connect external APIs and services" ← best match
- build: "Create software, features, tools"
- skill: "Create Nexus skills"

AI: "This looks like an Integration project. I'll use add-integration
     to discover Slack's API. Sound right?"
```

### If Ambiguous

```markdown
I detected this could be a few different project types:

1. **Integration** - Connecting Slack API
2. **Build** - Building notification system
3. **Skill** - Creating reusable notification skill

Which type best matches what you're building?
```

---

## EARS Requirements (Build/Skill Types)

For **build** and **skill** projects, discovery includes EARS-formatted requirements:

| Pattern | Template | Example |
|---------|----------|---------|
| Ubiquitous | THE `<system>` SHALL `<response>` | THE API SHALL validate inputs |
| Event-driven | WHEN `<trigger>`, THE `<system>` SHALL `<response>` | WHEN user clicks, THE form SHALL submit |
| State-driven | WHILE `<condition>`, THE `<system>` SHALL `<response>` | WHILE loading, THE UI SHALL show spinner |
| Unwanted | IF `<condition>`, THEN THE `<system>` SHALL `<response>` | IF error, THEN THE system SHALL log |
| Optional | WHERE `<option>`, THE `<system>` SHALL `<response>` | WHERE debug mode, THE logger SHALL verbose |
| Complex | Combined patterns | WHERE admin, WHEN delete, THE system SHALL confirm |

**See**: [ears-patterns.md](ears-patterns.md) for full guide.

---

## Correctness Properties (Build/Skill Types)

For **build** and **skill** projects, plan.md includes Correctness Properties:

```markdown
## Correctness Properties

**Property 1: Input Validation**
For all user inputs, the system either accepts valid input OR returns descriptive error.
**Validates**: REQ-2, REQ-3

**Property 2: State Consistency**
For any operation sequence, resume-context.md reflects actual state.
**Validates**: REQ-4
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

---

## Mental Models (After Discovery)

Mental models are applied AFTER discovery, not before:

1. **First Principles** - Strip assumptions, find fundamental truths
2. **Pre-Mortem** - Imagine failure before implementation
3. **Devil's Advocate** - Identify risks and blind spots
4. **Stakeholder Mapping** - Identify affected parties

**Key Insight**: Questions are INFORMED by discovery:
- "Given your requirement REQ-1, what assumptions are embedded?"
- "Given these API constraints, what could break?"

---

## Quality Checklist for AI

Before completing project creation, verify:

- [ ] Project type correctly detected (semantic matching)
- [ ] Discovery completed BEFORE mental models
- [ ] Discovery findings written to 02-discovery.md
- [ ] Mental models applied to discovery findings
- [ ] Dependencies & Links section researched and populated
- [ ] Resume-context.md updated with phase transitions
- [ ] User confirmed understanding at each pause

---

**Remember**: The router ensures every project gets proper discovery and mental model application. Discovery BEFORE mental models ensures informed questioning.
