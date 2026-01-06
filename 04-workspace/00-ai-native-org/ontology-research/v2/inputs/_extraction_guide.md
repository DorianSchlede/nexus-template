# Extraction Guide: Ontologies Research

**Purpose**: Ensure consistent extraction quality and format across all 23 papers.

---

## Field Definitions

### Field: entity_types
**Definition**: Core entity types defined in the paper (ontological categories)
**Format**: Array of strings
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
entity_types:
  - "Agent"
  - "Activity"
  - "Entity"
  - "Endurant"
  - "Perdurant"
  - "Object"
  - "Event"
```

**Example BAD extraction**:
```yaml
entity_types:
  - "The paper discusses various entities"
  - "ontological concepts"
```

---

### Field: entity_definitions
**Definition**: Formal definitions quoted or paraphrased from paper
**Format**: Object with entity name as key, definition as value
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
entity_definitions:
  Agent: "An entity capable of autonomous action and bearing intentional states"
  Activity: "A perdurant that depends on exactly one agent for its existence"
  Endurant: "An entity wholly present at any time it exists"
  Perdurant: "An entity that unfolds in time, having temporal parts"
```

**Example BAD extraction**:
```yaml
entity_definitions:
  - "Agents are defined in section 3"
  - "See page 5 for definitions"
```

---

### Field: entity_relationships
**Definition**: Relationships between entities (structural, behavioral, temporal)
**Format**: Array of objects with `from`, `to`, `relationship`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
entity_relationships:
  - from: "Agent"
    to: "Activity"
    relationship: "performs"
    source: "Chunk 2:45-52"
  - from: "Activity"
    to: "Entity"
    relationship: "uses/produces"
    source: "Chunk 2:67-71"
```

**Example BAD extraction**:
```yaml
entity_relationships:
  - "Agents and activities are related"
  - "Various relationships exist"
```

---

### Field: abstraction_level
**Definition**: Where this ontology sits in the ontology stack
**Format**: String - one of: "foundational", "core", "domain", "application"
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
abstraction_level: "foundational"
# Note: UFO, DOLCE, BFO are foundational
# PROV-O, BBO are core/domain
# ArchiMate, TOGAF are application
```

**Example BAD extraction**:
```yaml
abstraction_level: "high level ontology that covers many things"
```

---

### Field: framework_comparison
**Definition**: How this ontology relates to or compares with other frameworks
**Format**: Array of objects with `compared_to`, `relationship`, `details`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
framework_comparison:
  - compared_to: "BFO"
    relationship: "extends"
    details: "UFO extends BFO with social and intentional concepts"
    source: "Chunk 1:89-95"
  - compared_to: "PROV-O"
    relationship: "aligns_with"
    details: "Agent-Activity-Entity triad maps directly to PROV-O core"
    source: "Chunk 3:112-118"
```

**Example BAD extraction**:
```yaml
framework_comparison:
  - "Similar to other ontologies"
  - "Compares favorably"
```

---

### Field: ai_integration
**Definition**: How ontology enables AI/LLM systems
**Format**: Array of objects with `pattern`, `description`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
ai_integration:
  - pattern: "Ontology-guided RAG"
    description: "Entity types used to structure retrieval queries"
    source: "Chunk 4:23-35"
  - pattern: "Schema-constrained generation"
    description: "Ontology provides JSON schema for LLM output validation"
    source: "Chunk 5:67-78"
```

**Example BAD extraction**:
```yaml
ai_integration:
  - "Can be used with AI"
  - "Supports LLMs"
```

**Note**: Many older ontology papers (pre-2020) won't discuss AI. Use:
```yaml
ai_integration: "N/A - paper predates LLM/AI integration discussion"
```

---

### Field: agent_modeling
**Definition**: How agents/actors are represented in the ontology
**Format**: Array of objects with `aspect`, `description`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
agent_modeling:
  - aspect: "Intentionality"
    description: "Agents have beliefs, desires, intentions (BDI)"
    source: "Chunk 2:34-42"
  - aspect: "Autonomy"
    description: "Agents can initiate activities without external trigger"
    source: "Chunk 2:56-63"
  - aspect: "Role-based"
    description: "Agents occupy roles that define permissions and responsibilities"
    source: "Chunk 3:12-18"
```

---

### Field: agentic_workflows
**Definition**: Multi-agent patterns, orchestration, coordination
**Format**: Array of objects with `pattern`, `description`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
agentic_workflows:
  - pattern: "Hierarchical orchestration"
    description: "Manager agent delegates tasks to specialist agents"
    source: "Chunk 3:45-56"
  - pattern: "Peer-to-peer collaboration"
    description: "Agents negotiate task allocation via message passing"
    source: "Chunk 4:23-34"
```

---

### Field: generative_ai_patterns
**Definition**: LLM-specific patterns (prompting, reasoning, tool use)
**Format**: Array of objects with `pattern`, `description`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
generative_ai_patterns:
  - pattern: "ReAct"
    description: "Interleaved reasoning and action steps"
    source: "Chunk 2:78-89"
  - pattern: "Chain-of-Thought"
    description: "Step-by-step reasoning before final answer"
    source: "Chunk 2:92-103"
  - pattern: "Function calling"
    description: "LLM generates structured tool invocations"
    source: "Chunk 3:12-23"
```

---

### Field: agent_ontology_integration
**Definition**: How AI agents interact with ontological knowledge
**Format**: Array of objects with `mechanism`, `description`, `source` keys
**Priority**: HIGH

**Example GOOD extraction**:
```yaml
agent_ontology_integration:
  - mechanism: "Knowledge graph querying"
    description: "Agent translates natural language to SPARQL"
    source: "Chunk 4:56-67"
  - mechanism: "Ontology-guided planning"
    description: "Entity types constrain valid action sequences"
    source: "Chunk 5:23-34"
```

---

### Field: entity_count
**Definition**: Number of entity classes in the framework
**Format**: Integer or object with count and rationale
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
entity_count:
  count: 57
  rationale: "Designed for enterprise architecture coverage"
  source: "Chunk 1:45-52"
```

---

### Field: methodology
**Definition**: Approach to ontology development
**Format**: String - one of: "top-down", "bottom-up", "hybrid"
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
methodology: "top-down"
# Note: Philosophical ontologies (UFO, DOLCE) are typically top-down
# Process mining ontologies (OCEL) are typically bottom-up
# Enterprise ontologies (ArchiMate) are typically hybrid
```

---

### Field: empirical_evidence
**Definition**: Real-world validation or data sources
**Format**: Array of objects with `type`, `description`, `source` keys
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
empirical_evidence:
  - type: "Process mining"
    description: "Validated on 50 event logs from manufacturing domain"
    source: "Chunk 5:34-45"
  - type: "Case study"
    description: "Applied to 3 enterprise architecture projects"
    source: "Chunk 6:12-23"
```

---

### Field: limitations
**Definition**: What the ontology cannot capture
**Format**: Array of strings with chunk references
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
limitations:
  - "Cannot capture tacit knowledge (Chunk 4:89-92)"
  - "Does not model improvisation or workarounds (Chunk 4:95-98)"
  - "Assumes rational agents - no cognitive biases (Chunk 5:12-15)"
```

---

### Field: tools_standards
**Definition**: Technical implementations and standards
**Format**: Array of strings
**Priority**: MEDIUM

**Example GOOD extraction**:
```yaml
tools_standards:
  - "OWL 2"
  - "RDF"
  - "BPMN 2.0"
  - "OCEL 2.0"
  - "Protege"
```

---

## Controlled Vocabulary

When these concepts appear, use these EXACT terms:

| Paper Uses | Standardize To |
|------------|----------------|
| "endurant", "continuant", "thing", "object" | "Endurant" |
| "perdurant", "occurrent", "process", "happening" | "Perdurant" |
| "agent", "actor", "participant", "performer" | "Agent" |
| "activity", "action", "task", "operation" | "Activity" |
| "event", "occurrence", "happening" (instantaneous) | "Event" |
| "entity", "object", "thing" (generic) | "Entity" |
| "role", "position", "function" | "Role" |
| "goal", "objective", "intention" | "Goal" |
| "resource", "artifact", "tool" | "Resource" |
| "rule", "constraint", "norm" | "Rule" |
| "data", "information", "content" | "Data" |

---

## Quality Checklist

Before completing analysis, verify:

- [ ] All 10 HIGH priority fields have at least one extraction OR explicit "N/A - reason"
- [ ] Every extraction has chunk:line reference (e.g., "Chunk 2:45-52")
- [ ] Controlled vocabulary applied consistently
- [ ] Entity definitions are actual definitions, not "see section X"
- [ ] Framework comparisons specify the relationship type
- [ ] AI-related fields marked "N/A" for pre-2020 papers if not discussed
- [ ] Format matches specification (objects vs arrays vs strings)

---

## Paper Type Guidance

### Foundational Ontology Papers (UFO, DOLCE, BFO)
- Focus on: entity_types, entity_definitions, entity_relationships, abstraction_level
- AI fields likely: N/A (pre-LLM)

### Process/BPM Ontology Papers (BBO, OCEL)
- Focus on: entity_types, methodology, empirical_evidence, tools_standards
- AI fields: may have some integration discussion

### AI/LLM Agent Papers
- Focus on: ai_integration, agent_modeling, agentic_workflows, generative_ai_patterns, agent_ontology_integration
- Traditional ontology fields: may be lightweight

### Knowledge Graph Papers
- Focus on: agent_ontology_integration, tools_standards, empirical_evidence
- Both ontology and AI fields relevant

---

**Version**: 1.0 (2025-12-28)
