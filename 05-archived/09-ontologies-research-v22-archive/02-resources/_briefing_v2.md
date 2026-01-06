---
research_question: "What ontological primitives, patterns, and structures emerge from analyzing foundational ontologies, knowledge graphs, and AI agent frameworks - and what novel synthesis can we derive?"

# Discovery-oriented purpose (NO hypothesis validation)
research_purpose: "Open exploration of ontological foundations for digital work. Let patterns emerge from the data. Discover unexpected connections, gaps, and novel synthesis opportunities. Build grounded theory from papers rather than testing predefined hypotheses."

approach: "DISCOVERY"  # Not VALIDATION

domain: "Ontology engineering, Knowledge representation, AI/LLM systems, Process mining, Multi-agent systems"

extraction_schema:
  # CORE DISCOVERY FIELDS (what's actually in the papers)
  - field: ontological_primitives
    description: "What are the fundamental building blocks this framework uses? What can't be reduced further?"
    priority: critical
    guidance: "Don't map to predefined categories. Extract what the paper actually defines as primitive."

  - field: structural_patterns
    description: "What recurring structures appear? Triads, hierarchies, networks, layers?"
    priority: critical
    guidance: "Look for repeating architectural patterns. Document the shape of relationships."

  - field: novel_concepts
    description: "What concepts does this paper introduce that aren't in other frameworks?"
    priority: critical
    guidance: "Focus on unique contributions. What's NEW here?"

  - field: semantic_commitments
    description: "What philosophical/ontological commitments does the framework make?"
    priority: high
    guidance: "4D vs 3D, endurantism vs perdurantism, nominalism vs realism, etc."

  - field: boundary_definitions
    description: "How does the framework define entity boundaries? When does one thing become two things?"
    priority: high
    guidance: "Identity conditions, individuation criteria, mereological principles."

  - field: temporal_modeling
    description: "How is time/change/process handled?"
    priority: high
    guidance: "Events, states, processes, durations, instantaneous vs extended."

  - field: agency_spectrum
    description: "Where does agency live? What can be an agent? What are the degrees of agency?"
    priority: high
    guidance: "Human, AI, software, organization, collective - what's the range?"

  - field: knowledge_representation
    description: "How is knowledge encoded, stored, queried, reasoned over?"
    priority: high
    guidance: "RDF, OWL, property graphs, embeddings, hybrid approaches."

  - field: emergence_indicators
    description: "What patterns suggest emergent properties? What can't be predicted from parts?"
    priority: medium
    guidance: "Collective behavior, system-level properties, non-compositional semantics."

  - field: integration_surfaces
    description: "Where does this framework connect to others? What are the joints?"
    priority: medium
    guidance: "Mapping points, alignment opportunities, bridge concepts."

  - field: gaps_and_tensions
    description: "What's missing? What contradictions or tensions exist?"
    priority: medium
    guidance: "Explicit limitations, unstated assumptions, unresolved debates."

  - field: empirical_grounding
    description: "What real-world data/use cases validate or motivate this work?"
    priority: medium
    guidance: "Case studies, process logs, enterprise applications, benchmarks."

# NO PREDEFINED HYPOTHESES - Let findings emerge
synthesis_goals:
  - "Discover emergent patterns across papers (don't force-fit to predefined categories)"
  - "Identify unexpected connections between frameworks"
  - "Surface novel synthesis opportunities"
  - "Build grounded taxonomy from observed primitives"
  - "Map the actual landscape of ontological approaches"
  - "Find gaps and opportunities for new contributions"

anti_patterns:
  - "DO NOT validate a predefined 8-entity hypothesis"
  - "DO NOT force papers into Goal/Task/Rule/Resource/Role/Data/Event/Agent categories"
  - "DO NOT assume Agent-Activity-Entity is universal until it emerges from data"
  - "DO NOT prioritize confirmation over discovery"

skip_sections:
  - "Acknowledgments"
  - "Author biographies"
  - "Conference logistics"
  - "References (but DO note cited frameworks)"
---

# Research Briefing v2: Ontological Foundations Discovery

## Approach: GROUNDED DISCOVERY

This is **NOT** a hypothesis validation exercise. We are conducting open-ended exploration to discover what patterns, primitives, and structures actually exist in the literature.

### Core Principle

> "Let the data speak. Extract what's there, not what we expect to find."

## Primary Research Question

**What ontological primitives, patterns, and structures emerge from analyzing foundational ontologies, knowledge graphs, and AI agent frameworks?**

## Discovery Sub-questions

### Ontological Foundations
1. What primitives do different frameworks actually use? (Not what we think they should use)
2. What structural patterns recur across frameworks?
3. Where do frameworks diverge in their fundamental assumptions?
4. What semantic commitments distinguish different approaches?

### Emergent Patterns
5. What triads, hierarchies, or networks appear organically?
6. What boundary conditions separate different approaches?
7. What's the spectrum of agency across frameworks?
8. How is temporality handled differently?

### AI/Agent Integration
9. How do AI frameworks connect to foundational ontologies?
10. What novel patterns appear in LLM-era papers?
11. Where do classical ontology and AI agent research diverge?
12. What integration surfaces exist but aren't exploited?

### Gaps and Opportunities
13. What's conspicuously absent from the literature?
14. Where do frameworks contradict each other?
15. What synthesis opportunities exist?
16. What would a novel contribution look like?

## Extraction Philosophy

### DO
- Extract what's actually written
- Note unique terminology
- Capture author's own categorizations
- Record unexpected findings
- Document tensions and contradictions
- Preserve nuance and qualification

### DON'T
- Map to predefined categories
- Normalize away interesting differences
- Assume universal patterns exist
- Privilege certain frameworks
- Filter for "relevance" to a hypothesis
- Ignore what doesn't fit

## Expected Outputs

1. **Emergent Taxonomy**: Categories that arise from data, not imposed on it
2. **Pattern Catalog**: Structures that recur, with variation noted
3. **Divergence Map**: Where frameworks disagree and why
4. **Gap Analysis**: What's missing from the literature
5. **Synthesis Opportunities**: Novel combinations not yet explored
6. **Grounded Framework**: If patterns warrant, a new synthesis

## Paper Categories for Discovery

| Category | Discovery Focus |
|----------|-----------------|
| Foundational Ontology (UFO, BFO, DOLCE) | What primitives? What commitments? |
| Provenance (PROV-O, PROV-AGENT) | What's traceable? What's the agent model? |
| Process (OCEL, BBO, BPMN) | How is activity structured? What entities participate? |
| Knowledge Graphs | How is knowledge represented? What reasoning? |
| AI/LLM Agents | What's the agent architecture? How does knowledge integrate? |
| Multi-Agent Systems | What coordination patterns? What emergence? |

## Quality Signals

Good extraction shows:
- Surprise (findings that weren't expected)
- Specificity (exact terminology, not paraphrases)
- Tension (where papers disagree)
- Gaps (what's not addressed)
- Connection (unexpected links to other work)

Poor extraction shows:
- Confirmation (only finding expected patterns)
- Homogenization (making everything look similar)
- Completeness bias (claiming everything is covered)
- Category forcing (mapping to predefined buckets)

---

**Version**: 2.0 (Discovery-oriented)
**Date**: 2025-12-31
**Replaces**: _briefing.md (hypothesis-validation version)
