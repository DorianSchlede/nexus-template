# Airtable Test Dataset Builder - Plan

**Last Updated**: 2025-12-31

---

## Priority Nodes (Latest Version Analysis)

**Analysis Date**: 2025-12-31
**Script**: `03-working/find_priority_nodes.py`
**Output**: `04-outputs/priority-nodes.json`

### Selection Criteria
- Task Accuracy: 60% - 99% (room for improvement)
- Min Tasks: ≥40 (enough data)
- Min Failed (<80%): ≥5 (has edge cases)

### Priority Nodes for Testing

| Node | Agent | Tasks | Failed | Accuracy | Variables |
|------|-------|-------|--------|----------|-----------|
| **Extract All Case Info** | Ops Case Handler | 73 | 6 | 91.9% | 1,408 |
| **1. Schreiben Bank** | TZV Agent 03.09 | 60 | 9 | 87.5% | 120 |
| **2. TZV Zurück** | TZV Agent 03.09 | 42 | 25 | 78.2% | 588 |

### Edge Case Nodes (Stress Testing)

| Node | Agent | Tasks | Failed | Accuracy |
|------|-------|-------|--------|----------|
| Receptionist | Inso Agent MAGA | 45 | 44 | 50.8% |
| Generate request msg | B2B Check | 8 | 8 | 0.0% |

### All Nodes Summary (25 with accuracy data)

| Rank | Node | Agent | Tasks | Accuracy |
|------|------|-------|-------|----------|
| 1 | Classify Incoming Email | Email Mgmt (POC) | 92 | 95.7% |
| 2 | Extract All Case Info | Ops Case Handler | 73 | 91.9% |
| 3 | 3.0 SS Grouping | TZV Agent | 70 | 98.6% |
| 4 | 1. Schreiben Bank | TZV Agent | 60 | 87.5% |
| 5 | Receptionist | Inso Agent MAGA | 45 | 50.8% |

---

## Approach

**3-Phasen-Strategie:**

1. **Inventory** - Zuerst verstehen was wir haben
   - Airtable API abfragen: Agents, Workspaces, Nodes, DatasetVariables
   - Aggregieren: Anzahl Expected Outputs pro Agent/Node
   - Verknüpfungen validieren: DatasetVariables ↔ DatasetNodes ↔ NodeVersion

2. **Export-Pipeline** - Daten extrahieren und formatieren
   - Python-Scripts für Airtable → JSON Konvertierung
   - MetaTuner-kompatibles Format (`PromptDataset`, `PromptDatasetItem`)
   - Filterbar nach Agent/Workspace

3. **Dataset-Konstruktion** - Spezifische Test-Sets bauen
   - Edge Cases (niedrige Accuracy)
   - Happy Path (hohe Accuracy)
   - Regression (vorher gefailte, jetzt fixte Cases)
   - **Per Prompt-Typ** (Extraction, Classification, Generation, etc.)

---

## Key Decisions

- **Lokale JSON statt neue Airtable DB**: Flexibler, keine zusätzlichen Kosten, Git-versionierbar
- **Python für Scripts**: Bereits in Nexus verwendet, gute Airtable-Library (`pyairtable`)
- **Per-Agent Datasets**: Ermöglicht gezieltes Testing einzelner Agents
- **Verknüpfungs-Validierung zuerst**: Ohne korrekte Links sind die Datasets nutzlos

---

## Resources Needed

**Tools/Access**:
- Airtable API Token (bereits vorhanden via MCP)
- Python 3.10+
- pyairtable Library

**Information/Data**:
- Airtable Base ID: `appFPoOfBpUv73M5A` (AI Development Platform)
- Table IDs für: Agents, Nodes, NodeVersions, DatasetVariables, DatasetNodes, DatasetTasks

---

## Dependencies & Links

**Files Impacted**:
- `02-projects/07-airtable-test-dataset-builder/03-working/` - Scripts
- `02-projects/07-airtable-test-dataset-builder/04-outputs/` - Exported Datasets

**External Systems**:
- Airtable: AI Development Platform Base (`appFPoOfBpUv73M5A`)
- Langfuse: LLM Tracing (`https://tracing.beamstudio.ai`)
- MCP Airtable Server: Für API-Zugriff

---

## Airtable ↔ Langfuse Integration

**Key Discovery**: Die Beam Task ID in Airtable entspricht der Session ID in Langfuse.

**Mapping**:
```
Airtable.AgentTasks.Task ID (UUID) = Langfuse.sessionId
```

**Beispiel**:
- Airtable Task ID: `32b88cd9-51ad-4a6e-aba4-fc6d35e32f33`
- Langfuse API: `GET /sessions/32b88cd9-51ad-4a6e-aba4-fc6d35e32f33`
- Returns: Alle Traces (Node-Executions) mit Input/Output, LLM-Calls, Scores

**Was Langfuse liefert (pro Task)**:
- `traces[]` - Alle Node-Ausführungen
  - `input` - Node Input (z.B. Conversation Data)
  - `output` - Node Output (z.B. Extracted Fields)
  - `name` - Node Name (z.B. "GraphTaskExecution")
- `observations[]` - Einzelne LLM-Calls
  - `input` - Prompt (filled)
  - `output` - LLM Response
  - `model` - Model Name (gpt-4o, etc.)
  - `usage_metadata` - Token Counts
- `scores[]` - Evaluations
  - `name` - Score Name (z.B. "Accuracy")
  - `value` - Score Value (0.0-1.0)
  - `comment` - Evaluation Reasoning
- `totalCost` - Gesamtkosten der Task
- `latency` - Ausführungszeit

**Datenfluss für MetaTuner Datasets**:
```
Airtable                          Langfuse
────────────────────────────────────────────────────
AgentTasks.Task ID ───────────────► sessionId
                                    │
DatasetVariables.Expected Value     ▼
        │                    GET /sessions/{id}
        │                           │
        ▼                           ▼
  Ground Truth            Actual Execution Details
        │                    - Filled Prompts
        │                    - LLM Outputs
        │                    - Scores
        │                    - Token Usage
        ▼                           │
        └──────── MERGE ────────────┘
                    │
                    ▼
           MetaTuner Dataset Item
           - input (from Langfuse)
           - prompt (from Langfuse)
           - actualOutput (from Langfuse)
           - expectedOutput (from Airtable)
           - score (from Langfuse/Airtable)
```

**API Endpoints verwendet**:
- `GET /sessions/{sessionId}` - Alle Traces einer Task
- `GET /traces/{traceId}` - Einzelner Trace mit Observations
- `GET /v2/observations?traceId={id}` - Observations (LLM-Calls)

**Langfuse Skills verfügbar**:
- `00-system/skills/langfuse/langfuse-get-session/` - Session abrufen
- `00-system/skills/langfuse/langfuse-get-trace/` - Trace Details
- `00-system/skills/langfuse/langfuse-list-observations/` - Observations

**Related Projects**:
- MetaTuner in `mutagent-monorepo/mutagent/src/framework/metatuner/`

**Skills/Workflows**:
- Keine direkten Skill-Abhängigkeiten

**Reference Documentation**:
- `02-resources/metatuner-algorithm-documentation.md` - Algorithmus-Details
- `01-memory/integrations/airtable/ai-development-platform/_enriched-index.md` - Airtable Schema

---

## Open Questions

- [x] Welche Agents/Workspaces existieren? → Via Inventory klären
- [x] Wie viele Expected Outputs pro Agent? → Via Inventory klären
- [ ] Welche Nodes haben KEINE Expected Outputs? → Coverage-Gap identifizieren
- [ ] Gibt es "orphaned" DatasetVariables ohne NodeVersion-Link?

---

## Technical Architecture

**System Components**:
```
┌─────────────────────────────────────────────────────────────┐
│                    Airtable (Source)                        │
│  ┌─────────┐  ┌─────────┐  ┌──────────────────┐            │
│  │ Agents  │──│  Nodes  │──│  NodeVersions    │            │
│  └─────────┘  └─────────┘  └──────────────────┘            │
│       │            │              │                         │
│       ▼            ▼              ▼                         │
│  ┌─────────┐  ┌─────────────┐  ┌──────────────┐            │
│  │Datasets │──│DatasetNodes │──│DatasetVars   │            │
│  └─────────┘  └─────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼ (Python Scripts)
┌─────────────────────────────────────────────────────────────┐
│                   Export Pipeline                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │ inventory  │  │  validate  │  │   export   │            │
│  │  .py       │  │  _links.py │  │  _dataset  │            │
│  └────────────┘  └────────────┘  │   .py      │            │
│                                   └────────────┘            │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   Local Files (Output)                      │
│  04-outputs/                                                │
│  ├── inventory-report.json                                  │
│  ├── validation-report.json                                 │
│  └── datasets/                                              │
│      ├── agent-{name}/                                      │
│      │   ├── dataset-{type}.json  (MetaTuner format)        │
│      │   └── metadata.json                                  │
│      └── ...                                                │
└─────────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. Airtable API → Python (pyairtable)
2. Python aggregiert/validiert/transformiert
3. Output: JSON Dateien im MetaTuner-Format

**Technology Stack**:
- Python 3.10+ - Script-Sprache
- pyairtable - Airtable API Client
- JSON - Export-Format
- (Optional) pandas - Für komplexere Aggregationen

---

## MetaTuner Export Format

```json
{
  "name": "Agent-X Edge Cases",
  "description": "Low accuracy cases from Agent X",
  "items": [
    {
      "id": "rec_123",
      "input": { "document": "...", "context": "..." },
      "expectedOutput": { "field1": "value1", "field2": "value2" },
      "actualOutput": { "field1": "wrong", "field2": "value2" },
      "userFeedback": "Feld1 war falsch extrahiert",
      "metadata": {
        "agent": "Agent X",
        "node": "Extract Node",
        "nodeVersion": "v1.2",
        "accuracy": 0.5,
        "source": "DatasetVariable.rec_abc"
      }
    }
  ],
  "metadata": {
    "agent": "Agent X",
    "workspace": "Production",
    "exportedAt": "2025-12-28T14:00:00Z",
    "totalItems": 50,
    "avgAccuracy": 0.65
  }
}
```

---

## Data Inventory Plan

### Ziel
Bevor wir Datasets erstellen, müssen wir verstehen:
1. **WAS** haben wir? (Volumen, Verteilung)
2. **WO** sind Lücken? (Coverage Gaps)
3. **WIE** ist die Qualität? (Accuracy-Verteilung)
4. **WELCHE** Dimensionen können wir nutzen? (Slicing-Optionen)

---

### Inventory Dimensionen

#### Dimension 1: Hierarchie (Top-Down)
```
Workspace
  └── Agent
       └── Node
            └── Variable
                 └── DatasetVariable (Expected Value)
```

**Fragen:**
- Wie viele Workspaces/Agents existieren?
- Wie viele Nodes pro Agent?
- Wie viele Variables pro Node?
- Wie viele Expected Values (DatasetVariables) existieren?

#### Dimension 2: Execution Data
```
AgentTasks (= Langfuse Session)
  └── NodeTasks
       └── VariableTasks
            ├── AIValue (Actual Output)
            ├── Expected Value (from DatasetVariable)
            └── Accuracy (0 oder 1)
```

**Fragen:**
- Wie viele AgentTasks pro Agent?
- Wie viele haben Accuracy-Daten?
- Task ID → Langfuse Session verfügbar?

#### Dimension 3: Prompt-Typen (aus NodeVersions)
```
NodeVersions.Tool Type:
  ├── Extraction (Daten aus Dokumenten extrahieren)
  ├── Classification (Kategorisierung)
  ├── Generation (Text generieren)
  ├── Action (API-Calls, Tools)
  └── Routing (Entscheidungen, Edge Selection)
```

**Fragen:**
- Welche Tool Types existieren?
- Wie viele NodeVersions pro Tool Type?
- Accuracy-Verteilung pro Tool Type?

#### Dimension 4: Accuracy-Buckets
```
Accuracy Distribution:
  ├── Perfect (1.0) → Happy Path
  ├── High (0.8-0.99) → Minor Issues
  ├── Medium (0.5-0.79) → Significant Issues
  ├── Low (0.1-0.49) → Edge Cases
  └── Failed (0.0) → Complete Failures
```

#### Dimension 5: Verknüpfungs-Qualität
```
DatasetVariables
  ├── ✓ Linked to DatasetNodes → Valid
  ├── ✓ DatasetNodes → NodeVersion → Has Prompt
  ├── ✗ Orphaned (no DatasetNode link) → Unusable
  └── ✗ Missing NodeVersion → No Prompt available
```

---

### Inventory Report Struktur

```json
{
  "generated_at": "2025-12-28T...",
  "summary": {
    "total_workspaces": 3,
    "total_agents": 15,
    "total_nodes": 45,
    "total_variables": 120,
    "total_dataset_variables": 500,
    "total_agent_tasks": 10000,
    "tasks_with_accuracy": 8500,
    "langfuse_coverage": 0.95
  },

  "by_workspace": [
    {
      "id": "rec...",
      "name": "Production",
      "agents": 5,
      "dataset_variables": 200,
      "avg_accuracy": 0.82
    }
  ],

  "by_agent": [
    {
      "id": "rec...",
      "name": "Customer Support Analyzer",
      "workspace": "Production",
      "nodes": 8,
      "variables": 25,
      "dataset_variables": 150,
      "agent_tasks": 2000,
      "avg_accuracy": 0.78,
      "accuracy_distribution": {
        "perfect": 1200,
        "high": 400,
        "medium": 250,
        "low": 100,
        "failed": 50
      }
    }
  ],

  "by_prompt_type": [
    {
      "tool_type": "Extraction",
      "node_versions": 20,
      "dataset_variables": 300,
      "avg_accuracy": 0.75
    },
    {
      "tool_type": "Classification",
      "node_versions": 10,
      "dataset_variables": 100,
      "avg_accuracy": 0.88
    }
  ],

  "data_quality": {
    "valid_dataset_variables": 480,
    "orphaned_dataset_variables": 20,
    "missing_node_version": 5,
    "missing_prompt": 3,
    "no_langfuse_session": 50
  },

  "coverage_gaps": [
    {
      "agent": "Agent X",
      "node": "Node Y",
      "issue": "No expected values defined",
      "variables_affected": 5
    }
  ]
}
```

---

### Dataset-Konstruktion aus Inventory

Nach dem Inventory können wir gezielt Datasets erstellen:

#### 1. Per-Agent Datasets
```
datasets/
├── agent-customer-support-analyzer/
│   ├── all-cases.json          (alle 150 cases)
│   ├── edge-cases.json         (accuracy < 0.5)
│   ├── happy-path.json         (accuracy = 1.0)
│   └── metadata.json
```

#### 2. Per-Prompt-Type Datasets
```
datasets/
├── prompt-type-extraction/
│   ├── all-extraction.json
│   ├── extraction-edge-cases.json
│   └── extraction-by-agent.json
├── prompt-type-classification/
│   └── ...
```

#### 3. Cross-Cutting Datasets
```
datasets/
├── global-edge-cases.json      (accuracy < 0.5, alle Agents)
├── global-happy-path.json      (accuracy = 1.0, alle Agents)
├── regression-candidates.json  (vorher failed, jetzt fixed)
└── high-value-variables.json   (Key Variables only)
```

---

### Inventory Script Workflow

```python
# 03-working/inventory.py

1. LOAD: Alle relevanten Tables aus Airtable
   - Workspaces, Agents, Nodes, Variables
   - NodeVersions (für Tool Type)
   - DatasetVariables, DatasetNodes, DatasetTasks
   - AgentTasks, VariableTasks (für Accuracy)

2. AGGREGATE: Zählen und Gruppieren
   - Count by Workspace/Agent/Node
   - Accuracy-Verteilung berechnen
   - Prompt-Types kategorisieren

3. VALIDATE: Verknüpfungen prüfen
   - DatasetVariables → DatasetNodes?
   - DatasetNodes → NodeVersion?
   - NodeVersion → Prompt vorhanden?
   - AgentTasks.Task ID → Langfuse Session?

4. EXPORT: JSON Report generieren
   - 04-outputs/inventory-report.json
   - 04-outputs/coverage-gaps.json
   - 04-outputs/orphaned-records.json
```

---

### Nächste Schritte

1. **inventory.py erstellen** - Hauptscript für Datenerhebung
2. **Airtable API testen** - Verbindung und Table IDs validieren
3. **Inventory ausführen** - Report generieren
4. **Analyse** - Report auswerten, Entscheidungen treffen
5. **Dataset-Scripts** - Basierend auf Inventory-Erkenntnissen

---

## Implementation Strategy

### Expected Output Sources (Strukturierte Erhebung)

**Primary Source: DatasetVariables**

| Field | Description | Use Case |
|-------|-------------|----------|
| `Expected Value` | Ground truth value | MetaTuner expectedOutput |
| `Expected Value Status` | Valid/Partial/Invalid | Quality filter |
| `Variable Name` | Field being extracted | Grouping |
| `Variable Type (from Variable)` | Key/Additional Variable | Priority filter |

**Link Chain für vollständige Test Cases:**

```
DatasetVariables (Ground Truth)
     │
     ├── OriginalVariableTask ─────► VariableTasks
     │                                   │
     │                                   ├── AIValue (Actual Output)
     │                                   └── Accuracy (0 or 1)
     │
     ├── OriginalAgentTask ────────► AgentTasks
     │                                   │
     │                                   └── Task ID → Langfuse sessionId
     │
     └── DatasetNodes ─────────────► DatasetNodes
                                         │
                                         ├── NodeVersion → NodeVersions.Prompt
                                         └── NodeTask → NodeTasks.Filled Prompt
```

**Validierungs-Checks (vor Inventory):**

1. `DatasetVariables` mit `Expected Value != BLANK()`
2. `DatasetVariables.OriginalVariableTask != BLANK()` (hat Actual Output)
3. `DatasetVariables.DatasetNodes.NodeVersion != BLANK()` (hat Prompt)

**Datenquellen-Matrix:**

| MetaTuner Field | Airtable Source | Link Path |
|-----------------|-----------------|-----------|
| `input` | `AgentTasks.Actual Task Input` | DatasetVariables → OriginalAgentTask |
| `prompt` | `NodeTasks.Filled Prompt` | DatasetVariables → DatasetNodes → NodeTask |
| `expectedOutput` | `DatasetVariables.Expected Value` | Direct |
| `actualOutput` | `VariableTasks.AIValue` | DatasetVariables → OriginalVariableTask |
| `score` | `VariableTasks.Accuracy` | DatasetVariables → OriginalVariableTask |
| `userFeedback` | `BID Feedback.User_Value` | Via TaskID match |

---

### Langfuse Integration: ExecuteGPT_Tool Filtering

**Wichtig**: Bei Langfuse interessieren uns NUR die `ExecuteGPT_Tool/v1` Observations, nicht alle Traces.

**Datenfluss Langfuse (gefiltert):**

```
Beam Task ID ───► Langfuse Session (sessionId)
                       │
                       └── Traces (GraphTaskExecution)
                                │
                                └── Observations
                                     │
                                     ├── ExecuteGPT_Tool/v1 ◄── NUR DIESE!
                                     │        │
                                     │        ├── input → Filled Prompt + Context
                                     │        └── output → LLM Response (Raw)
                                     │
                                     └── NodeEvaluation/.../GEval
                                              └── Scores (aber Expected kommt aus Airtable!)
```

**Filter für Observations API:**
```python
# Nur ExecuteGPT_Tool Observations abrufen
GET /v2/observations?traceId={id}&name=ExecuteGPT_Tool/v1
```

**Was Langfuse liefert vs. Airtable:**

| Feld | Langfuse (Observation) | Airtable (Primär) |
|------|------------------------|-------------------|
| `prompt` | observation.input | NodeTasks.Filled Prompt |
| `actualOutput` | observation.output.content | VariableTasks.AIValue |
| `model` | observation.model | NodeVersions.Model |
| `usage` | observation.usage_metadata | - |
| **`expectedOutput`** | **NICHT VERFÜGBAR** | **DatasetVariables.Expected Value** |

**Kritischer Punkt**: Expected Output kommt NIEMALS aus Langfuse - immer aus Airtable!

---

### Verifizierte Zählungen (2025-12-29)

| Quelle | Anzahl | Stand |
|--------|--------|-------|
| DatasetVariables (total) | 70,586 | 2025-12-29 |
| DatasetVariables mit Expected Value | 21,963 | 2025-12-29 |
| VariableTasks mit Expected Output | 46,341 | 2025-12-29 |
| DatasetNodes | 4,964 | 2025-12-29 |
| NodeTasks | 18,597 | 2025-12-29 |
| Agents | 38 | 2025-12-29 |

### VariableTasks pro Agent

| Agent | VariableTasks | Expected Values |
|-------|---------------|-----------------|
| TZV Agent 03.09 | 33,834 | 17,154 |
| Deal Breaker | 5,423 | 244 |
| Inso All-In-One Agent MAGA | 2,372 | 1,146 |
| CV Screening Agent v2 | 1,926 | 1,926 |
| Ops Case Handler | 1,767 | 778 |
| B2B Check Agent | 454 | 575 |

---

## Mental Models Applied

**MECE Principle** (Mutually Exclusive, Collectively Exhaustive):
- Datasets nach Agent gruppiert (keine Überlappung)
- Alle DatasetVariables erfasst (nichts vergessen)

**Value Stream Mapping**:
- Datenfluss klar: Airtable → Script → JSON → MetaTuner
- Jeder Schritt hat klaren Input/Output

**Pre-Mortem Analysis**:
- **Risk**: Orphaned DatasetVariables ohne NodeVersion-Link
  - Mitigation: Validation Script identifiziert diese zuerst
- **Risk**: Airtable Rate Limits bei großen Queries
  - Mitigation: Pagination, Caching
- **Risk**: Schema-Änderungen in Airtable brechen Scripts
  - Mitigation: Defensive Parsing, klare Fehlermeldungen

---

## Current Status (2025-12-31)

**Phase**: 5.2 - Dataset Export for Priority Nodes

**Completed**:
- [x] Full inventory of 70k+ DatasetVariables
- [x] CSV exports for all relevant tables
- [x] Export script (`export_dataset.py`)
- [x] Schema validation against MetaTuner types
- [x] Priority node selection (`find_priority_nodes.py`)

**Next Steps**:
1. Add `--node` filter to export_dataset.py
2. Export datasets for 3 priority nodes
3. Export edge case dataset (Receptionist)
4. Validate against MetaTuner

---

*Last updated: 2025-12-31*
