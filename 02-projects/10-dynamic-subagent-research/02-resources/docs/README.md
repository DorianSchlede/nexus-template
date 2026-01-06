# Dynamic Research Subagent System

> **HIGH QUALITY DATA TRANSFER through FORCED COMPLETE READING**

---

## Das Problem

LLM-Subagents neigen dazu:
1. **Zu überfliegen** statt gründlich zu lesen
2. **Details auszulassen** die nicht "interessant" erscheinen
3. **Zitate zu halluzinieren** die nicht existieren
4. **Line-Referenzen zu raten** statt exakt zu zitieren

**Konsequenz**: Schlechte Extraktion, unzuverlässige Synthese, verlorene Erkenntnisse.

---

## Die Lösung: 4-Säulen-Verifizierung

```
┌──────────────────────────────────────────────────────────────────────┐
│                    DYNAMIC SUBAGENT SYSTEM                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. INPUT CONTRACT          2. FORCED READING                        │
│  ├─ Explizite Dateiliste    ├─ 3-Point Evidence                     │
│  ├─ Verbotene Dateien       ├─ SHA256 Hash                          │
│  └─ Violation = Reject      ├─ Spot Check Questions                 │
│                              └─ Line/Word Count                      │
│                                                                      │
│  3. OUTPUT SCHEMA           4. POST-VERIFICATION                     │
│  ├─ Exaktes Format          ├─ Evidence Matching                    │
│  ├─ Pflichtfelder           ├─ Quote-Line Check                     │
│  ├─ Validation Rules        ├─ Hash Verification                    │
│  └─ Citation Format         └─ Reference Existence                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Komponenten

### 1. `dynamic_subagent_factory.py`

**Zweck**: Domain-spezifische Subagent-Prompts generieren

**Features**:
- Domain Registry (Ontologie, NLP, Multi-Agent, Knowledge Graph)
- Automatische Domain-Erkennung aus `_briefing.md`
- Task-spezifische Methodologie
- INPUT CONTRACT Generierung
- OUTPUT SCHEMA Generierung

**Domains**:
| Domain | Keywords | Persona |
|--------|----------|---------|
| ontology | BFO, DOLCE, UFO, entity | Ontologie-Ingenieur |
| nlp | LLM, transformer, token | NLP/LLM-Forscher |
| multi_agent | agent, coordination | Multi-Agent-Experte |
| knowledge_graph | KG, RDF, SPARQL | KG-Spezialist |

### 2. `forced_reading_contract.py`

**Zweck**: Erzwingen, dass der Subagent ALLES liest

**Mechanismen**:

#### 3-Point Evidence
```yaml
chunk_evidence:
  chunk_1:
    start: "First 100 chars after header..."
    mid: "100 chars from 50% position..."
    end: "Last 100 chars..."
    hash: "SHA256..."
```

#### Spot Check Questions
```
Zeile 42: Was steht dort?
Zeile 150: Was steht dort?
Zeile 280: Was steht dort?
```
→ Falsche Antwort = Chunk wurde nicht gelesen

#### Anti-Skimming Protocol
- Sequenzielles Lesen in 100-Zeilen-Blöcken
- Erst ALLES lesen, DANN extrahieren
- Self-Check Questions nach jedem Chunk

### 3. `generate_dynamic_research_subagent.py`

**Zweck**: Haupt-Entry-Point für Prompt-Generierung

**Usage**:
```bash
# Paper Analysis
python generate_dynamic_research_subagent.py \
  02-projects/02-ontologies-research \
  paper_analysis \
  --paper-id 02-Knowledge_Graphs

# Batch Extraction
python generate_dynamic_research_subagent.py \
  02-projects/02-ontologies-research \
  batch_extraction \
  --field entity_types \
  --batch-num 1
```

**Output**:
- `03-working/prompts/_prompt_{task_id}.md`
- `.claude/agents/{task_id}.md` (für Claude Code Subagent)

### 4. `verify_subagent_reading.py`

**Zweck**: Post-Execution Verifizierung

**Checks**:
| Check | Was wird geprüft | Failure = |
|-------|------------------|-----------|
| evidence_start | Erste 100 Zeichen | Nicht von Anfang gelesen |
| evidence_end | Letzte 100 Zeichen | Nicht bis Ende gelesen |
| hash | SHA256 des Chunks | Content manipuliert/unvollständig |
| reference_exists | Chunk-Datei existiert | Falsche Referenz |
| quote_at_line | Zitat an Zeile | Halluziniertes Zitat |

**Usage**:
```bash
# Verify paper analysis
python verify_subagent_reading.py \
  02-projects/02-ontologies-research \
  --paper-id 02-Knowledge_Graphs

# Verify batch extraction
python verify_subagent_reading.py \
  02-projects/02-ontologies-research \
  --batch 03-working/_batch_entity_types_1.yaml
```

---

## Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                         RESEARCH TASK                               │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 1. PROMPT GENERATION                                                │
│    python generate_dynamic_research_subagent.py                     │
│                                                                     │
│    Outputs:                                                         │
│    - Domain-specific persona                                        │
│    - Strict INPUT CONTRACT                                          │
│    - FORCED READING requirements                                    │
│    - Exact OUTPUT SCHEMA                                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 2. SUBAGENT EXECUTION                                               │
│    Task(subagent_type="general-purpose", prompt=generated_prompt)   │
│                                                                     │
│    Subagent MUST:                                                   │
│    - Read EVERY file in INPUT CONTRACT                              │
│    - Record 3-point evidence for each chunk                         │
│    - Answer spot check questions                                    │
│    - Follow exact OUTPUT SCHEMA                                     │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│ 3. POST-VERIFICATION                                                │
│    python verify_subagent_reading.py                                │
│                                                                     │
│    Checks:                                                          │
│    - 3-point evidence matches actual content                        │
│    - Hash matches actual chunk                                      │
│    - References exist and are valid                                 │
│    - Quotes exist at cited lines                                    │
│                                                                     │
│    Result: PASS or FAIL + detailed report                           │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                    ┌─────────────┴─────────────┐
                    ▼                           ▼
            ┌───────────┐               ┌───────────────┐
            │   PASS    │               │     FAIL      │
            │           │               │               │
            │ Continue  │               │ Retry with    │
            │ pipeline  │               │ stricter      │
            └───────────┘               │ constraints   │
                                        └───────────────┘
```

---

## Integration mit Projekt 6

Das Dynamic Subagent System integriert sich in die 7-Level Synthesis Pipeline:

| Level | Current | With Dynamic Subagents |
|-------|---------|------------------------|
| L1 Routing | Script | Script (unchanged) |
| L2 Allocation | Script | Script (unchanged) |
| L3 Prompt Gen | Script | **Uses dynamic_subagent_factory.py** |
| L4 Extraction | Subagent | **Domain-specific + Forced Reading** |
| L5 Verification | Script | **Uses verify_subagent_reading.py** |
| L6 Aggregation | Script | Script (unchanged) |
| L7 Report | Subagent | **Domain-specific + Token Budget** |

---

## Beispiel: Generierter Prompt

```markdown
---
name: paper_analysis_02-Knowledge_Graphs
description: Analyze single paper → index.md with chunk_index
tools: Read, Glob, Grep
model: inherit
---

# Paper Analysis: paper_analysis_02-Knowledge_Graphs

**Generated**: 2025-12-28T15:30:00
**Task Type**: paper_analysis
**Domain**: ontology

---

## DEINE ROLLE

Du bist **Ontologie-Ingenieur**.

### Expertise
- Foundational Ontologies (BFO, DOLCE, UFO, SUMO)
- Entity-Hierarchien und Taxonomien
- Axiomatische Definitionen und Constraints

### Fachvokabular
| Term | Definition |
|------|------------|
| **Endurant** | Entity wholly present at any time (continuant) |
| **Perdurant** | Entity that unfolds over time (occurrent) |

---

## INPUT CONTRACT (STRICT)

### Files You MUST Read (in this order)
1. `02-projects/02-ontologies-research/02-resources/_briefing.md`
2. `02-resources/papers/02-Knowledge_Graphs/_metadata.json`
3. `02-resources/papers/02-Knowledge_Graphs/02-Knowledge_Graphs_1.md`
4. `02-resources/papers/02-Knowledge_Graphs/02-Knowledge_Graphs_2.md`
...

### Files You MUST NOT Read
- `*.pdf`
- `04-outputs/*`
- `../*`

**VIOLATION = Output rejected**

---

## FORCED READING CONTRACT

### Proof-of-Reading Requirements

Für JEDEN Chunk musst du dokumentieren:

```yaml
chunk_evidence:
  02-Knowledge_Graphs_1:
    start: "{first 100 chars}"
    mid: "{100 chars from 50%}"
    end: "{last 100 chars}"
    hash: "{SHA256}"
    line_count: {N}
```

### Spot Check Questions

#### 02-Knowledge_Graphs_1
- **Erwartete Zeilenzahl**: 487
- **Hash-Prefix**: `a7b8c9d4e5f6...`

**Spot Check Fragen:**
- Zeile 97: Was steht dort?
- Zeile 243: Was steht dort?

---

## KRITISCHE REGELN

1. **LIES JEDEN CHUNK VOLLSTÄNDIG** - Kein Überfliegen
2. **RECORD 3-POINT EVIDENCE** für jeden Chunk
3. **BEANTWORTE SPOT CHECK FRAGEN** - Falsche Antwort = Ablehnung
```

---

## Files

```
03-skills/research-pipeline/validation/
├── dynamic_subagent_factory.py      # Domain + Task templates
├── forced_reading_contract.py       # Anti-skimming mechanisms
├── scripts/
│   ├── generate_dynamic_research_subagent.py  # Main entry point
│   └── verify_subagent_reading.py   # Post-execution verification
└── DYNAMIC_SUBAGENT_README.md       # This file
```

---

## Next Steps

1. **Test auf Ontologies-Research**: Generiere Prompt für ein Paper, führe aus, verifiziere
2. **Feedback Loop**: Wenn Verification fails, analysiere warum und verbessere Prompts
3. **Integration**: Ersetze generische Prompts in `synthesize-research-project/SKILL.md`

---

**Version**: 1.0 (2025-12-28)
**Author**: Dynamic Subagent Factory
**Goal**: HIGH QUALITY DATA TRANSFER through FORCED COMPLETE READING
