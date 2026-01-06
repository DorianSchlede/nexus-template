---
research_question: "What are the foundational ontologies for digital work, and how do they ground entity definitions, framework comparisons, and AI agent/generative AI integration patterns?"

# G22a: WHY this research matters (provides context to subagents)
research_purpose: "Validate the 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent) for UDWO metamodel grounding. Inform internal ontology design for AI agent orchestration platform. Enable ontology-guided LLM reasoning and structured generation patterns."

domain: "Ontology engineering, Enterprise architecture, Business process management, AI/LLM systems, Agentic AI, Generative AI"
extraction_schema:
  - field: entity_types
    description: "Core entity types defined (e.g., Agent, Activity, Entity, Endurant, Perdurant)"
    priority: high
  - field: entity_definitions
    description: "Formal definitions and distinguishing characteristics of each entity"
    priority: high
  - field: entity_relationships
    description: "Relationships between entities (structural, behavioral, organizational)"
    priority: high
  - field: entity_count
    description: "Number of entity classes/types in the framework and rationale"
    priority: medium
  - field: abstraction_level
    description: "Level of abstraction (foundational, domain, application) and purpose"
    priority: high
  - field: framework_comparison
    description: "How this ontology compares to others (UFO, PROV-O, BBO, ArchiMate, TOGAF, OCEL)"
    priority: high
  - field: methodology
    description: "Top-down (theoretical) vs bottom-up (empirical) approach"
    priority: medium
  - field: ai_integration
    description: "How ontology enables AI agents, LLMs, RAG, planning, guardrails"
    priority: high
  - field: agent_modeling
    description: "How agents/actors are modeled (autonomous, intentional, role-based)"
    priority: high
  - field: agentic_workflows
    description: "Multi-agent systems, agent orchestration, tool use, planning strategies"
    priority: high
  - field: generative_ai_patterns
    description: "LLM reasoning, chain-of-thought, ReAct, function calling, structured outputs"
    priority: high
  - field: agent_ontology_integration
    description: "How AI agents interact with ontologies (RAG, KG querying, ontology-guided reasoning)"
    priority: high
  - field: empirical_evidence
    description: "Process mining data, enterprise logs, real-world validation"
    priority: medium
  - field: limitations
    description: "What the ontology cannot capture (tacit knowledge, improvisation, etc.)"
    priority: medium
  - field: tools_standards
    description: "Technical implementations (OWL, RDF, BPMN, CMMN, DMN, OCEL 2.0)"
    priority: medium
focus_areas:
  - "Foundational ontologies: UFO (Unified Foundational Ontology), PROV-O, BBO"
  - "The Agent-Activity-Entity triad as universal pattern"
  - "Entity count abstraction-dependency (4-106 entities based on purpose)"
  - "Integration with BPM+ standards (BPMN, CMMN, DMN, SDMN)"
  - "Object-Centric Process Mining (OCEL 2.0) empirical grounding"
  - "MVO metamodel and AI agent integration patterns"
  - "Validation of 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent)"
  - "AI Agent architectures: ReAct, Chain-of-Thought, function calling, tool use"
  - "Multi-agent systems and agent orchestration frameworks"
  - "Ontology-guided LLM reasoning and structured generation"
  - "Knowledge graphs as agent memory and reasoning substrate"
  - "Agentic workflow patterns for business process automation"
skip_sections:
  - "Acknowledgments"
  - "Author biographies"
  - "Conference logistics"
context_documents:
  - path: "04-workspace/09-ontology research/input/claude-dr-ontology-model.md"
    summary: "Deep research on foundational triad (Agent-Activity-Entity), abstraction-dependency, UFO/PROV-O/BBO analysis, Activity Theory gap"
  - path: "04-workspace/09-ontology research/input/gemini-onlogoy-model.md"
    summary: "UDWO proposal with 8-entity hypothesis, MVO metamodel, BPM+ integration, OCEL 2.0 grounding, AI agent patterns"
---

# Research Briefing: Foundational Ontologies for Digital Work

## Primary Research Question

**What are the foundational ontologies for digital work, and how do they ground entity definitions, framework comparisons, and AI agent/generative AI integration patterns?**

## Sub-questions

### Foundational Ontologies
1. What entities are universal across foundational ontologies (UFO, PROV-O, BBO)?
2. How does the Agent-Activity-Entity triad manifest in different frameworks?
3. What is the relationship between abstraction level and entity count?
4. How can foundational ontologies ground the 8-entity hypothesis (Goal, Task, Rule, Resource, Role, Data, Event, Agent)?

### AI Agents & Generative AI
5. What patterns enable AI agents to interact with ontological structures?
6. How do LLM-based agents use ontologies for reasoning, planning, and tool selection?
7. What multi-agent architectures leverage ontological knowledge?
8. How can ontologies structure and constrain generative AI outputs?
9. What role do knowledge graphs play as agent memory and reasoning substrate?

### Integration & Limitations
10. What aspects of digital work resist formalization?
11. How do agentic workflow patterns map to ontological entities?

## Existing Synthesis (from input documents)

### Key Findings to Validate/Extend

1. **Foundational Triad**: Agent-Activity-Entity appears universal across UFO, PROV-O, BBO
2. **Entity Count**: 4-106 entities depending on purpose (Petri nets 4, OCEL 4-8, ArchiMate 57, BBO 106)
3. **Abstraction Dependency**: Entity count reflects analytical needs, not ontological reality
4. **8-Entity Hypothesis**: Goal, Task, Rule, Resource, Role, Data, Event, Agent as atomic units
5. **Activity Theory Gap**: Human-centric aspects (contradictions, mediation, tacit knowledge) under-captured

### Frameworks to Investigate

| Framework | Entity Count | Primary Purpose |
|-----------|-------------|-----------------|
| UFO | ~50 | Philosophical grounding |
| PROV-O | 3 core | Provenance tracking |
| BBO | 106 | BPMN ontological grounding |
| ArchiMate | 57 | Enterprise architecture |
| TOGAF | 33 | EA development lifecycle |
| OCEL 2.0 | 4-8 per process | Process mining |
| Petri nets | 4 | Formal verification |

## Search Strategy

### Primary Search Terms
- "foundational ontology" AND "digital work"
- "UFO ontology" OR "Unified Foundational Ontology"
- "PROV-O" AND "provenance ontology"
- "BBO ontology" OR "BPMN Based Ontology"
- "ontology" AND "business process" AND "entity"
- "object-centric process mining" AND "ontology"
- "enterprise ontology" AND "agent" AND "activity"

### Secondary Search Terms
- "ArchiMate ontology" OR "ArchiMate metamodel"
- "DOLCE ontology" (foundational)
- "GFO ontology" (General Formal Ontology)
- "BFO" (Basic Formal Ontology)
- "ontology" AND "LLM" AND "agent"
- "knowledge graph" AND "business process"

## Expected Outputs

1. **Entity Taxonomy**: Validated/refined entity types across foundational ontologies
2. **Framework Comparison Matrix**: Entity counts, purposes, trade-offs
3. **AI Integration Patterns**: How ontologies enable agent reasoning
4. **Synthesis Document**: Grounding for UDWO/MVO metamodel
