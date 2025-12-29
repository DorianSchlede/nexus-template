# Research Plan: Dynamic Subagent Handover Patterns

## Research Question

**Primary RQ**: Wie können strukturierte Handover-Protokolle die Datenqualität bei LLM-Subagent-Interaktionen verbessern?

**Sub-Questions**:
- RQ1: Forced Reading - Verhindert 3-Point Evidence tatsächlich Skimming?
- RQ2: Hash Verification - Wie hoch ist die Detection-Rate bei inkompletten Reads?
- RQ3: Domain Personas - Verbessern spezialisierte Personas die Extraktionsqualität?
- RQ4: ULTRASEARCH Protocol - Reduziert Ticket-based Handover den Information Loss?

## Extraction Schema

Für die wissenschaftliche Analyse der Dokumentation:

```yaml
extraction_fields:
  # Pattern-Identifikation
  - name: "pattern_definition"
    description: "Definition eines Handover-Patterns"
    examples:
      - "3-Point Evidence: start (100 chars) + mid (100 chars) + end (100 chars)"
      - "Hash Chain: SHA256 verification at each transfer"

  - name: "mechanism_type"
    description: "Art des Mechanismus"
    vocabulary: ["verification", "enforcement", "detection", "prevention"]

  - name: "failure_mode"
    description: "Was passiert wenn das Pattern verletzt wird"
    examples:
      - "Output REJECTED"
      - "Warning issued, continue"

  # Implementierung
  - name: "implementation_detail"
    description: "Konkrete Code-Implementierung"
    examples:
      - "def extract_reading_proof(file_path: Path) -> ReadingProof"

  - name: "integration_point"
    description: "Wo im Pipeline wird es angewendet"
    vocabulary: ["prompt_generation", "execution", "verification", "handover"]

  # Evaluation
  - name: "quality_metric"
    description: "Messbare Qualitätsmetriken"
    examples:
      - "Verification rate > 90%"
      - "Hash mismatch < 5%"

  - name: "limitation"
    description: "Bekannte Einschränkungen des Patterns"
```

## Paper Corpus

### Internal Resources (Ready)

| Resource ID | Type | Tokens (est.) | Priority |
|-------------|------|---------------|----------|
| readme_md | Docs | ~3,300 | HIGH |
| ultrasearch_md | Docs | ~5,700 | HIGH |
| factory_py | Code | ~6,500 | HIGH |
| forced_reading_py | Code | ~4,000 | HIGH |
| generator_py | Code | ~3,600 | MEDIUM |
| verifier_py | Code | ~4,700 | MEDIUM |
| handover_py | Code | ~6,000 | MEDIUM |

**Internal Total**: ~33,800 tokens

### External Papers (2025, Pending Approval)

| # | Paper | arXiv ID | Category | Priority |
|---|-------|----------|----------|----------|
| 1 | Agentic Context Engineering (ACE) | 2510.04618 | Context | HIGH |
| 2 | Survey of Context Engineering | 2507.13334 | Context | HIGH |
| 3 | Context Engineering Multi-Agent Code | 2508.08322 | Context | HIGH |
| 4 | Git Context Controller | 2508.00031 | Context | HIGH |
| 7 | Which Multi-Agent Protocol? | 2510.17149 | Protocol | HIGH |
| 8 | LACP | 2510.13821 | Protocol | HIGH |
| 9 | SEMAP | 2510.12120 | Protocol | HIGH |
| 10 | TalkHier | 2502.11098 | Protocol | HIGH |
| 12 | Multi-Agent Collaboration Survey | 2501.06322 | Protocol | HIGH |
| 15 | LLM Agent Survey | 2503.21460 | Planning | HIGH |
| 18 | Agent Hallucinations Survey | 2509.18970 | Verification | HIGH |
| 19 | HalMit Watchdog | 2507.15903 | Verification | HIGH |
| 22 | PROV-AGENT | 2508.02866 | Workflow | HIGH |
| 24 | Effective GenAI Collaboration | 2412.05449 | Workflow | HIGH |

**Recommended Core Set**: 14 papers (~400k tokens estimated)
**Full Set**: 24 papers (~600k tokens estimated)

See `02-resources/_search_results.md` for complete list with abstracts.

## Orchestrator Instructions

### Subagent Allocation Plan (External Papers)

| Paper ID | Chunks | Est. Tokens | Subagents | Splits |
|----------|--------|-------------|-----------|--------|
| 01-ACE-2510.04618 | 5 | ~25,000 | 1 | 1-5 |
| 02-ContextSurvey-2507.13334 | 26 | ~177,000 | 4 | 1-7, 8-14, 15-20, 21-26 |
| 03-ClaudeCode-2508.08322 | 2 | ~12,000 | 1 | 1-2 |
| 04-GCC-2508.00031 | 2 | ~12,000 | 1 | 1-2 |
| 07-ProtocolBench-2510.17149 | 8 | ~35,000 | 1 | 1-8 |
| 08-LACP-2510.13821 | 2 | ~12,000 | 1 | 1-2 |
| 09-SEMAP-2510.12120 | 2 | ~8,000 | 1 | 1-2 |
| 10-TalkHier-2502.11098 | 5 | ~21,000 | 1 | 1-5 |
| 12-CollabSurvey-2501.06322 | 7 | ~45,000 | 1 | 1-7 |
| 15-AgentSurvey-2503.21460 | 10 | ~56,000 | 2 | 1-5, 6-10 |
| 18-HallucinationSurvey-2509.18970 | 8 | ~42,000 | 1 | 1-8 |
| 19-HalMit-2507.15903 | 4 | ~15,000 | 1 | 1-4 |
| 22-PROV-AGENT-2508.02866 | 2 | ~11,000 | 1 | 1-2 |
| 24-EffectiveCollab-2412.05449 | 4 | ~20,000 | 1 | 1-4 |

**Total subagents**: 18 (including 4 for ContextSurvey, 2 for AgentSurvey)
**Max concurrent**: 15

### Subagent Allocation (Internal Resources)

| Resource | Subagents | Strategy |
|----------|-----------|----------|
| All docs | 1 | Single comprehensive analysis |

### Analysis Subagent Prompt

```markdown
# Dynamic Subagent Pattern Analysis

## ROLE
Du bist Forscher für Multi-Agent-Systems mit Fokus auf LLM-Koordination.

## TASK
Analysiere die bereitgestellten Dokumentationen und extrahiere:
1. Alle definierten Handover-Patterns
2. Mechanismus-Typen und ihre Zwecke
3. Implementierungsdetails
4. Qualitätsmetriken
5. Limitationen

## INPUT CONTRACT
Read these files IN ORDER:
1. 02-resources/docs/README.md
2. 02-resources/docs/ULTRASEARCH_HANDOVER_PATTERNS.md
3. 02-resources/code/dynamic_subagent_factory.py
4. 02-resources/code/forced_reading_contract.py
5. 02-resources/code/generate_dynamic_research_subagent.py
6. 02-resources/code/verify_subagent_reading.py
7. 02-resources/code/handover_manager.py

## OUTPUT
Write to: 04-outputs/_pattern_analysis.md
```

## Current State

| Metric | Value |
|--------|-------|
| Phase | READY FOR EXECUTION |
| Internal Resources | 7/7 ready |
| External Papers | 14 downloaded, 87 chunks |
| Total Chunks | 87 (~2M chars) |
| Resources Analyzed | 0 |
| Analysis Kit | Ready |
| Extraction Guide | Ready |

## Next Steps

1. [x] Copy documentation files to 02-resources/
2. [x] Create _briefing.md with extraction schema
3. [x] Search external papers (24 found, 2025 only)
4. [x] **USER GATE**: Approve paper selection (14 core)
5. [x] Download approved papers (14 PDFs, 17MB)
6. [x] Preprocess PDFs to chunks (87 chunks)
7. [x] Generate _analysis_kit.md
8. [x] Generate _extraction_guide.md
9. [ ] **READY**: Run analysis subagents (use `analyze-research-project` skill)
10. [ ] Synthesize findings (use `synthesize-research-project` skill)
11. [ ] Draft pattern catalog

---

**Version**: 1.1
**Updated**: 2025-12-28
**Resume**: See `_resume.md` for context recovery
