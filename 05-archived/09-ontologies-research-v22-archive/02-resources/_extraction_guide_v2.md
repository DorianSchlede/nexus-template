# Extraction Guide v2: Discovery-Oriented

**Purpose**: Guide open-ended extraction that lets patterns emerge rather than confirming hypotheses.

**Philosophy**: Extract what's actually there. Preserve specificity. Note surprises.

---

## Core Extraction Fields

### Field: ontological_primitives
**What to capture**: The irreducible building blocks the framework uses
**Format**: Array of objects with `term`, `definition`, `source`, `unique_aspects`

**Discovery approach**:
- Use the paper's OWN terminology (don't normalize yet)
- Note what the authors consider primitive vs derived
- Capture the actual definition, not a paraphrase
- Flag terms that don't map cleanly to other frameworks

```yaml
ontological_primitives:
  - term: "Endurant"
    definition: "An entity wholly present whenever it exists"
    source: "Chunk 2:45-52"
    unique_aspects: "Contrasts with 4D view where objects have temporal parts"
  - term: "Trope"
    definition: "A particular quality instance (this redness, not redness in general)"
    source: "Chunk 3:23-28"
    unique_aspects: "Not found in BFO - UFO-specific commitment"
```

**Avoid**: Mapping everything to Agent/Activity/Entity immediately

---

### Field: structural_patterns
**What to capture**: Recurring architectural shapes and relationships
**Format**: Array of objects with `pattern_name`, `structure`, `instances`, `source`

**Discovery approach**:
- Look for triads, dyads, hierarchies, networks
- Note the SHAPE of relationships, not just their names
- Count how many times a pattern appears
- Document variations on patterns

```yaml
structural_patterns:
  - pattern_name: "Participation Triad"
    structure: "X participates-in Y affecting Z"
    instances:
      - "Agent participates-in Activity affecting Entity (PROV-O)"
      - "Endurant participates-in Perdurant (DOLCE)"
      - "Continuant participates-in Occurrent (BFO)"
    source: "Multiple papers - see instances"
  - pattern_name: "Anti-rigid Type"
    structure: "Type that can be gained/lost without identity change"
    instances:
      - "Role in UFO"
      - "Phase in UFO"
      - "Social Role in Enterprise Ontology"
    source: "UFO Chunk 4:67-78"
```

---

### Field: novel_concepts
**What to capture**: Ideas unique to this paper/framework
**Format**: Array of objects with `concept`, `definition`, `novelty_claim`, `source`

**Discovery approach**:
- What does this paper add that others don't have?
- What terminology is introduced?
- What problems does it solve that others don't?

```yaml
novel_concepts:
  - concept: "Relator"
    definition: "A moment that mediates entities, making relationships first-class"
    novelty_claim: "UFO treats relationships as entities, not just predicates"
    source: "Chunk 3:89-95"
  - concept: "Object-Centric Event Log"
    definition: "Events linked to multiple objects rather than single case"
    novelty_claim: "Breaks from traditional case-centric process mining"
    source: "Chunk 1:34-45"
```

---

### Field: semantic_commitments
**What to capture**: Philosophical positions the framework adopts
**Format**: Array of objects with `commitment`, `position`, `implications`, `source`

**Discovery approach**:
- What does the framework assume about reality?
- What philosophical tradition does it follow?
- What does it exclude by its choices?

```yaml
semantic_commitments:
  - commitment: "Endurantism vs Perdurantism"
    position: "Endurantist - objects wholly present at each moment"
    implications: "Cannot model objects as 4D spacetime worms"
    source: "Chunk 1:56-67"
  - commitment: "Nominalism vs Realism"
    position: "Moderate realism - universals exist but depend on instances"
    implications: "Types are real but grounded in particulars"
    source: "Chunk 2:23-34"
```

---

### Field: boundary_definitions
**What to capture**: How the framework individuates entities
**Format**: Array of objects with `entity_type`, `identity_criteria`, `boundary_cases`, `source`

**Discovery approach**:
- When does one thing become two things?
- What makes an entity THIS entity?
- Where are the edge cases?

```yaml
boundary_definitions:
  - entity_type: "Process"
    identity_criteria: "Same participants, same temporal extent, same goal"
    boundary_cases: "Is a resumed process the same process?"
    source: "Chunk 4:45-56"
  - entity_type: "Agent"
    identity_criteria: "Continuity of intentional states"
    boundary_cases: "Is a forked AI agent the same agent?"
    source: "Chunk 3:78-89"
```

---

### Field: temporal_modeling
**What to capture**: How time, change, and process are represented
**Format**: Array of objects with `aspect`, `approach`, `mechanism`, `source`

```yaml
temporal_modeling:
  - aspect: "Event granularity"
    approach: "Instantaneous events vs extended processes"
    mechanism: "Events have timestamps, processes have intervals"
    source: "Chunk 2:34-45"
  - aspect: "State change"
    approach: "Fluent-based"
    mechanism: "Qualities can change value over time while entity persists"
    source: "Chunk 3:56-67"
```

---

### Field: agency_spectrum
**What to capture**: The range and degrees of agency in the framework
**Format**: Array of objects with `agent_type`, `capabilities`, `constraints`, `source`

```yaml
agency_spectrum:
  - agent_type: "Human Agent"
    capabilities: "Full intentionality, goal-setting, belief revision"
    constraints: "Bounded rationality, mortality"
    source: "Chunk 2:45-56"
  - agent_type: "Software Agent"
    capabilities: "Goal-directed action, tool use"
    constraints: "No true intentionality, delegated goals"
    source: "Chunk 3:67-78"
  - agent_type: "AI Agent (LLM-based)"
    capabilities: "Reasoning, planning, tool calling, memory"
    constraints: "Hallucination, context limits, no persistent identity"
    source: "Chunk 4:23-34"
```

---

### Field: knowledge_representation
**What to capture**: How knowledge is encoded and reasoned over
**Format**: Array of objects with `mechanism`, `formalism`, `reasoning`, `source`

```yaml
knowledge_representation:
  - mechanism: "Ontology language"
    formalism: "OWL 2 DL"
    reasoning: "Description logic classification, consistency checking"
    source: "Chunk 1:89-95"
  - mechanism: "Knowledge graph"
    formalism: "Labeled property graph (Neo4j)"
    reasoning: "Path queries, graph patterns, no closed-world"
    source: "Chunk 3:45-56"
```

---

### Field: emergence_indicators
**What to capture**: Signals of emergent or system-level properties
**Format**: Array of objects with `phenomenon`, `mechanism`, `evidence`, `source`

```yaml
emergence_indicators:
  - phenomenon: "Organizational behavior"
    mechanism: "Agent roles aggregate to organizational patterns"
    evidence: "Department-level decisions not reducible to individual agents"
    source: "Chunk 5:34-45"
  - phenomenon: "Collective intelligence"
    mechanism: "Multi-agent deliberation produces novel solutions"
    evidence: "SciAgents hypothesis quality exceeds single agent"
    source: "Chunk 4:67-78"
```

---

### Field: integration_surfaces
**What to capture**: Where this framework connects to others
**Format**: Array of objects with `surface`, `connects_to`, `alignment_quality`, `source`

```yaml
integration_surfaces:
  - surface: "Agent concept"
    connects_to: ["PROV-O Agent", "BFO Material Entity", "UFO Substantial"]
    alignment_quality: "Partial - different intentionality requirements"
    source: "Chunk 2:56-67"
  - surface: "Activity/Process"
    connects_to: ["PROV-O Activity", "BFO Occurrent", "BPMN Task"]
    alignment_quality: "Good - temporal extension is common"
    source: "Chunk 3:78-89"
```

---

### Field: gaps_and_tensions
**What to capture**: What's missing or contradictory
**Format**: Array of objects with `gap_type`, `description`, `implications`, `source`

**This is crucial for discovery!**

```yaml
gaps_and_tensions:
  - gap_type: "Omission"
    description: "No account of collective/organizational agency"
    implications: "Cannot model a company as an agent"
    source: "Implicit - not discussed"
  - gap_type: "Tension"
    description: "Endurantism conflicts with process-centric view"
    implications: "Hard to model things-as-processes"
    source: "Chunk 4:23-34"
  - gap_type: "Underspecified"
    description: "Rule/constraint concept mentioned but not formalized"
    implications: "Governance layer missing"
    source: "Chunk 5:67-78"
```

---

### Field: empirical_grounding
**What to capture**: Real-world validation
**Format**: Array of objects with `type`, `domain`, `scale`, `findings`, `source`

```yaml
empirical_grounding:
  - type: "Process mining case study"
    domain: "Manufacturing"
    scale: "50 event logs, 2M events"
    findings: "Object-centric view captured 40% more behavior"
    source: "Chunk 6:34-45"
```

---

## Discovery Signals

### GOOD extraction shows:
- **Surprise**: "I didn't expect to find X"
- **Specificity**: Exact terms, exact definitions
- **Tension**: "Framework A says X, Framework B says not-X"
- **Gaps**: "This isn't addressed anywhere"
- **Novelty**: "This paper introduces a new concept"

### WARNING signs of confirmation bias:
- Everything maps cleanly to expected categories
- No tensions or contradictions found
- All frameworks "basically agree"
- Gap analysis is empty
- Novel concepts section is sparse

---

## Comparative Matrix (Build Incrementally)

As you extract, build this matrix - but let categories emerge:

| Paper | Primitive Terms | Structural Patterns | Novel Contributions | Key Tensions |
|-------|-----------------|---------------------|---------------------|--------------|
| UFO | Endurant, Perdurant, Moment, Trope, Relator | Triad, Anti-rigid types | Relator as first-class | Tropes vs universals |
| PROV-O | Agent, Activity, Entity | Triad (simpler) | Influence, derivation chains | Open-world only |
| ... | ... | ... | ... | ... |

---

## Quality Checklist

Before completing extraction:

- [ ] Used paper's own terminology (not normalized)
- [ ] Captured at least 2 novel concepts
- [ ] Found at least 1 gap or tension
- [ ] Noted at least 1 surprise
- [ ] All extractions have chunk:line references
- [ ] Did NOT force-fit to predefined categories
- [ ] Preserved nuance and qualification

---

**Version**: 2.0 (Discovery-oriented)
**Date**: 2025-12-31
**Philosophy**: Let patterns emerge. Preserve specificity. Note surprises.
