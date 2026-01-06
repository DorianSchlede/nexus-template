---
id: 16-ontologies-research-v3
name: Ontologies Research V3 (Standard Pipeline)
status: COMPLETE
description: "Standard pipeline synthesis of ontologies research. 23 papers analyzed with Schema 2.3, ready for 7-level synthesis."
created: 2025-12-31
schema_version: "v2.3"
---

# Ontologies Research V3 (Standard Pipeline)

> **Standard Pipeline Project** - Using proper 7-level synthesis architecture from synthesize-research-project skill.

## Purpose

**Research Question**: What are the foundational ontologies for digital work, and how do they ground entity definitions, framework comparisons, and AI agent/generative AI integration patterns?

---

## Current State

**Analysis Complete**:
- 23 papers analyzed with Schema 2.3
- All papers have `index.md` with `chunk_index` and `fields_found`
- Synthesis routing and subagent plan already generated

**Ready for Synthesis**:
- `_synthesis_routing.yaml` exists
- `_subagent_plan.yaml` exists
- All prerequisites met

---

## Next Action

Run synthesis skill:
```
/synthesize-research-project 16-ontologies-research-v3
```

---

## Key Files

### Analysis Inputs
- `02-resources/_briefing.md` - Research question + research_purpose
- `02-resources/_analysis_kit.md` - Extraction schema + synthesis_goals
- `02-resources/_extraction_guide.md` - Field examples

### Analysis Outputs
- `02-resources/papers/*/index.md` - 23 papers with Schema 2.3 analysis
- `02-resources/_synthesis_routing.yaml` - Routing table
- `02-resources/_subagent_plan.yaml` - Subagent allocation

### Synthesis Outputs (pending)
- `04-outputs/_synthesis_*.yaml` - Per-field aggregations
- `04-outputs/_synthesis_report.md` - Final report

---

## Papers (23)

All analyzed with Schema 2.3:
- 01-UFO, 02-Knowledge_Graphs, 03-PROV-AGENT
- 04-PROV-O_to_BFO, 05-DOLCE, 06-BFO_Function_Role
- 07-Classifying_Processes, 09-OCEL_20, 10-OC-PM
- 11-Process_Mining_Event_KG, 12-Foundations_Process
- 14-RAG_Ontologic (excluded from V2 due to wrong PDF)
- 15-SciAgents, 16-KG-Agent, 17-KG_Reasoning
- 18-Multi-Agent_Taxonomy, 19-Graph_of_Thoughts
- 20-Agentic_RAG, 21-LLM_Smart_Contracts
- 22-RPA_Framework, 23-UFO_Story
- 24-Enterprise_Ontology, 31-BBO_BPMN

---

*Project 16 - Ready for 7-level synthesis (2025-12-31)*
