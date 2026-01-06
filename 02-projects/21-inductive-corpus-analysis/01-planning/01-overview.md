---
id: 21-inductive-corpus-analysis
name: Inductive Corpus Analysis
status: PLANNING
description: "Load when user mentions inductive analysis, unprimed extraction, emergent patterns, or raw corpus findings"
created: 2026-01-01
---

# Inductive Corpus Analysis

## Purpose

Extract patterns **inductively** from the ontology research corpus (23 papers) without theoretical priming. Let categories, relationships, and patterns emerge from the data itself.

**NOT goals**:
- Validating any hypothesis
- Mapping to any metamodel
- Confirming any framework

**Goals**:
- Discover what authors actually define
- Find patterns as they appear in source texts
- Build emergent taxonomy from raw data

---

## Success Criteria

**Must achieve**:
- [ ] Raw entity categories as authors define them
- [ ] Relationship patterns in authors' own terms
- [ ] Workflow/coordination patterns without framing
- [ ] Tool/capability taxonomy from source definitions
- [ ] Problems/gaps as authors state them

**Outputs**:
- `04-outputs/emergent_entities.yaml` - Categories that appear
- `04-outputs/emergent_relationships.yaml` - How things connect
- `04-outputs/emergent_workflows.yaml` - Process patterns
- `04-outputs/emergent_tools.yaml` - Capability categories
- `04-outputs/emergent_gaps.yaml` - Stated limitations
- `04-outputs/inductive_synthesis.md` - What the corpus actually says

---

## Method

1. **No priming prompts** - Don't tell extractors what to find
2. **Quote-first** - Extract exact quotes, then categorize
3. **Author terminology** - Use their words, not canonical mappings
4. **Frequency counts** - What appears most often?
5. **Contradiction capture** - Note where papers disagree

---

## Source Corpus

23 papers in `04-workspace/00-ai-native-org/ontology-research/papers/`

| Category | Papers |
|----------|--------|
| Foundational Ontologies | UFO, DOLCE, BFO, UFO Story |
| Knowledge Graphs | Knowledge Graphs survey, PROV-O to BFO |
| AI Agents | PROV-AGENT, SciAgents, KG-Agent, Multi-Agent Taxonomy, Agentic RAG |
| Process Mining | OCEL 2.0, OC-PM, Event KG, Foundations |
| LLM Reasoning | Graph of Thoughts, KG Reasoning Survey |
| Enterprise/BPM | BBO, LLM Smart Contracts, RPA Framework, Enterprise Ontology |

---

## Related Projects

- **Project 16**: Ontologies Research V3 (primed extraction)
- **Project 20**: Temporal Patterns (primed extraction)

This project intentionally takes a different approach.
