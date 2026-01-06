---
project_id: "10-dynamic-subagent-research"
project_path: "02-projects/10-dynamic-subagent-research"
generated: "2025-12-28"
schema_version: "2.3"
---

# Analysis Kit for Dynamic Subagent Handover Patterns

**This file contains everything a subagent needs to analyze a paper in this project.**

---

## Research Question

**Primary RQ**: Wie können strukturierte Handover-Protokolle die Datenqualität bei LLM-Subagent-Interaktionen verbessern?

**Sub-Questions**:
- RQ1: Forced Reading - Verhindert 3-Point Evidence tatsächlich Skimming?
- RQ2: Hash Verification - Wie hoch ist die Detection-Rate bei inkompletten Reads?
- RQ3: Domain Personas - Verbessern spezialisierte Personas die Extraktionsqualität?
- RQ4: ULTRASEARCH Protocol - Reduziert Ticket-based Handover den Information Loss?

---

## Research Purpose

**WHY this research matters:**

Wissenschaftliche Analyse der entwickelten Dynamic Subagent Patterns für High-Quality Data Transfer.
Ziel: Pattern-Catalog, Best-Practice Guidelines, und akademische Publikation.

Use this context to:
- Prioritize extractions about handover patterns and protocols
- Flag findings about data quality mechanisms (verification, enforcement, detection)
- Focus on patterns that prevent information loss and hallucination

---

## Synthesis Goals

**What the synthesis will aggregate across papers:**

1. **Compare**: Multi-agent communication protocols across different frameworks (A2A, LACP, SEMAP, TalkHier)
2. **Identify**: Common patterns for high-quality data transfer between LLM agents
3. **Analyze**: Gaps between academic literature and our internal implementation (ULTRASEARCH patterns)

**Extract patterns that support these goals.**

---

## Extraction Schema

Extract these fields from each paper:

| Field | Description | Priority |
|-------|-------------|----------|
| `pattern_definition` | Definition eines Handover-Patterns mit Namen, Zweck, und Mechanismus | HIGH |
| `mechanism_type` | Art des Mechanismus: verification, enforcement, detection, prevention | HIGH |
| `failure_mode` | Was passiert wenn das Pattern verletzt wird | MEDIUM |
| `implementation_detail` | Konkrete Code-Implementierung (Funktion, Klasse, Datenstruktur) | HIGH |
| `integration_point` | Wo im Pipeline: prompt_generation, execution, verification, handover | HIGH |
| `quality_metric` | Messbare Qualitätsmetriken die das Pattern beeinflusst | HIGH |
| `limitation` | Bekannte Einschränkungen oder Nachteile des Patterns | MEDIUM |
| `related_pattern` | Andere Patterns die mit diesem zusammenhängen | LOW |

---

## Focus Areas

Look specifically for:
- LLM multi-agent coordination mechanisms
- Subagent communication protocols (A2A, MCP, LACP)
- Data quality verification approaches
- Prompt engineering for extraction accuracy
- Information loss prevention strategies
- Context engineering techniques
- Hallucination detection and mitigation
- Agent handover patterns

---

## Skip Sections

Don't extract from:
- Acknowledgments
- Author Contributions
- Funding
- References (unless citing specific patterns)

---

## Output Requirements

### 1. Analysis Log (`_analysis_log.md`)

For methodology reference, read: `03-skills/research-pipeline/shared/paper-analyze-core/references/analysis_log_template.md`

Key requirements:
- Record 3-point evidence (start, mid, end + hash) for each chunk
- Include chunk:line reference for every extraction
- Log which chunks were read

### 2. Index File (`index.md`)

For output format, read: `03-skills/research-pipeline/shared/paper-analyze-core/references/index_template.md`

**REQUIRED YAML frontmatter fields:**

```yaml
---
paper_id: "{paper_id}"
chunks_expected: {N}      # From _metadata.json
chunks_read: {N}          # Must equal chunks_expected
analysis_complete: true   # Set to true when done
high_priority_fields_found: {N}  # Count of HIGH priority fields with extractions
---
```

Key requirements:
- YAML frontmatter with paper metadata AND validation fields
- Extracted fields matching schema above
- Chunk navigation with summaries
- Chunk:line references for all quotes

---

## Paper Corpus

### Internal Resources (7 files)

| Resource | Path | Priority |
|----------|------|----------|
| README.md | 02-resources/docs/README.md | HIGH |
| ULTRASEARCH_HANDOVER_PATTERNS.md | 02-resources/docs/ULTRASEARCH_HANDOVER_PATTERNS.md | HIGH |
| dynamic_subagent_factory.py | 02-resources/code/dynamic_subagent_factory.py | HIGH |
| forced_reading_contract.py | 02-resources/code/forced_reading_contract.py | HIGH |
| generate_dynamic_research_subagent.py | 02-resources/code/generate_dynamic_research_subagent.py | MEDIUM |
| verify_subagent_reading.py | 02-resources/code/verify_subagent_reading.py | MEDIUM |
| handover_manager.py | 02-resources/code/handover_manager.py | MEDIUM |

### External Papers (14 papers, 87 chunks)

| Paper ID | Chunks | Category |
|----------|--------|----------|
| 01-ACE-2510_04618 | 5 | Context Engineering |
| 02-ContextSurvey-2507_13334 | 26 | Context Engineering |
| 03-ClaudeCode-2508_08322 | 2 | Context Engineering |
| 04-GCC-2508_00031 | 2 | Context Engineering |
| 07-ProtocolBench-2510_17149 | 8 | Multi-Agent Protocols |
| 08-LACP-2510_13821 | 2 | Multi-Agent Protocols |
| 09-SEMAP-2510_12120 | 2 | Multi-Agent Protocols |
| 10-TalkHier-2502_11098 | 5 | Multi-Agent Protocols |
| 12-CollabSurvey-2501_06322 | 7 | Multi-Agent Protocols |
| 15-AgentSurvey-2503_21460 | 10 | Task Decomposition |
| 18-HallucinationSurvey-2509_18970 | 8 | Verification |
| 19-HalMit-2507_15903 | 4 | Verification |
| 22-PROV-AGENT-2508_02866 | 2 | Workflow |
| 24-EffectiveCollab-2412_05449 | 4 | Workflow |

---

## File Locations

| Purpose | Path |
|---------|------|
| Paper chunks | `02-resources/papers/{paper_id}/{paper_id}_N.md` |
| Chunk metadata | `02-resources/papers/{paper_id}/_metadata.json` |
| Analysis log output | `02-resources/papers/{paper_id}/_analysis_log.md` |
| Index output | `02-resources/papers/{paper_id}/index.md` |

**Note:** `{paper_id}` is the folder name (e.g., `01-ACE-2510_04618`). All paths are relative to project root.

---

## Subagent Instructions

```
1. Read this analysis kit (you're reading it now)
2. Read the methodology: 03-skills/research-pipeline/shared/paper-analyze-core/SKILL.md
3. Read the paper's _metadata.json to get chunk list
4. Read ALL chunks listed in _metadata.json
5. Extract findings per the schema above
6. Write _analysis_log.md with 3-point evidence
7. Write index.md with REQUIRED frontmatter
```

**CRITICAL RULES:**
- Do NOT read the PDF file
- Do NOT skip any chunks
- Include chunk:line reference for every finding (e.g., "Chunk 3:127-134")
- Set `chunks_read` = `chunks_expected` (validates you read everything)
- Set `analysis_complete: true` only when fully done
- Provide 3-point evidence (start/mid/end + hash) for each chunk

---

## Validation Contract

Your output will be validated. The following MUST be true:

| Check | Requirement |
|-------|-------------|
| `index.md` exists | File must be created |
| `_analysis_log.md` exists | Log must be created |
| `chunks_read == chunks_expected` | All chunks were read |
| `analysis_complete == true` | Analysis finished |
| `high_priority_fields_found >= 1` | At least 1 HIGH priority extraction |
| Evidence has chunk:line refs | Every finding cites chunk:line |
| 3-point evidence for all chunks | Anti-hallucination check |

**If validation fails, the paper will be retried.**

---

## Pattern Categories to Extract

Based on our internal ULTRASEARCH patterns, look for similar concepts in literature:

1. **Ticket-based Handover** - Input manifest + output contract + completion receipt
2. **Hash-chain Verification** - Integrity checking at each transfer
3. **Citation Chain Preservation** - Traceability through pipeline stages
4. **3-Point Evidence** - Start/mid/end sampling for anti-skimming
5. **Structured Handover Protocol (SHP)** - Formal handover with verification
6. **Context Injection Protocol** - Token-optimized context levels
7. **Error Recovery Patterns** - Partial work preservation and retry

---

**Version**: 1.0
**Generated**: 2025-12-28
