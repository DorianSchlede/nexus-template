# Airtable Test Dataset Builder - Execution Steps

**Last Updated**: 2025-12-31

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Setup & Planning

- [x] Complete overview.md
- [x] Complete plan.md
- [x] Complete steps.md
- [x] Research MetaTuner algorithm (6 parallel agents)
- [x] Create algorithm documentation in 02-resources

---

## Phase 2: Inventory & Discovery

Ziel: Verstehen was wir haben - Expected Outputs pro Agent/Workspace/Node

### 2.1 Langfuse Integration (Completed)
- [x] Langfuse API testen
- [x] Mapping entdecken: `Airtable.AgentTasks.Task ID` = `Langfuse.sessionId`
- [x] Session-Abruf validieren (enthält alle Traces + Observations)
- [x] Plan.md mit Langfuse-Integration aktualisieren

### 2.2 Airtable Inventory
- [x] Airtable Tables identifizieren und Table IDs sammeln
  - [x] Agents Table ID (tblVEJD2inVhae855)
  - [x] Nodes Table ID (tblPJ9VKG74mKv7JK)
  - [x] NodeVersions Table ID (tblh0GsN5Et3ApzLS)
  - [x] Variables Table ID (tblf2ohTHmsucjVUj)
  - [x] DatasetVariables Table ID (tblsHYj8CrdHbY8Bt)
  - [x] DatasetNodes Table ID (tblflNTX3tR0onX13)
  - [x] DatasetTasks Table ID (tbl9lACSI4fDUzAv4)
  - [x] Datasets Table ID (tbltUrvSBnfOb4S8v)
- [x] Inventory Script erstellen (`03-working/inventory.py`)
  - [x] Airtable API Connection setup
  - [x] Agents & Workspaces abrufen
  - [x] DatasetVariables zählen pro Agent
  - [x] Aggregierte Stats berechnen (Accuracy distribution)
- [x] Inventory Report generieren (`04-outputs/inventory-report.json`)
- [x] Inventory analysieren

**Inventory Results (2025-12-29) - FULL DATA:**

| Table | Records | File |
|-------|---------|------|
| DatasetVariables | 70,586 | `DatasetVariables-FULL.csv` |
| VariableTasks | 46,341 | `VariableTasks-WithExpected.csv` |
| DatasetNodes | 4,964 | `DatasetNodes-ALL.csv` |
| NodeTasks | 18,597 | `NodeTasks-ALL.csv` |

**Quality Tiers:**
| Tier | Count | Description |
|------|-------|-------------|
| GOLD | 20,045 | Human Reviewed (Review=1) |
| SILVER | 54,868 | Status = Done |
| BRONZE | 21,963 | Has Expected Value |

**Top Agents with Expected Values:**
| Agent | Expected | Reviewed |
|-------|----------|----------|
| TZV Agent 03.09 | 17,154 | 15,858 |
| CV Screening Agent v2 | 1,926 | 1,920 |
| Inso All-In-One Agent MAGA | 1,146 | 758 |
| Ops Case Handler (Prod) | 778 | 704 |
| B2B Check Agent | 575 | 533 |

**VariableTasks by Agent (46,341 total):**
| Agent | VariableTasks |
|-------|---------------|
| TZV Agent 03.09 | 33,834 |
| Deal Breaker | 5,423 |
| Inso All-In-One Agent MAGA | 2,372 |
| CV Screening Agent v2 | 1,926 |
| Ops Case Handler | 1,767 |
| B2B Check Agent | 454 |

**Fixed:** NodeVersion link rate now 87.2% (field name was `Node Version (from NodeTask)`)

---

## Phase 3: Verknüpfungs-Validierung

Ziel: Sicherstellen dass DatasetVariables korrekt mit NodeVersions verbunden sind

- [x] NodeVersion Link Issue gelöst (Feldname war `Node Version (from NodeTask)`)
- [x] Full CSV exports erhalten und analysiert
- [x] Quality Tiers identifiziert (Gold/Silver/Bronze)
- [x] Full Inventory Report generiert (`04-outputs/inventory-report-full.json`)

---

## Phase 4: Export Script Development

Ziel: Airtable Daten in MetaTuner-kompatibles Format exportieren

- [x] Export Script erstellen (`03-working/export_dataset.py`)
  - [x] Filter-Optionen implementieren
    - [x] By Agent (--agent flag, partial match)
    - [ ] By Workspace
    - [ ] By Accuracy Range (edge cases, happy path)
    - [x] By Quality Tier (--tier: gold/silver/bronze)
  - [x] MetaTuner Format Transformation
    - [x] PromptDataset structure (JSON with items array)
    - [x] PromptDatasetItem structure (variableName, expectedOutput, actualOutput, prompt, score, metadata)
    - [x] Metadata enrichment (agent, reviewed, status, datasetVariableUID)
  - [x] Output Directory Struktur erstellen (`04-outputs/datasets/`)
- [x] Test-Export mit einem Agent durchführen
  - [x] Deal Breaker: 213 gold records, 100% prompts
  - [x] TZV Agent: 100 gold records (limited), 100% prompts
- [ ] Export validieren gegen MetaTuner Types

**Export Script Usage:**
```bash
python export_dataset.py --agent "Deal Breaker" --tier gold --verbose
python export_dataset.py --agent "TZV" --tier gold --limit 100
python export_dataset.py --format jsonl  # For line-delimited JSON
```

**Generated Datasets:**
- `04-outputs/datasets/metatuner-deal-breaker-gold.json` - 213 records
- `04-outputs/datasets/metatuner-tzv-gold.json` - 100 records (limited)

---

## Phase 5: Priority Node Selection & Dataset-Konstruktion

Ziel: Identify priority nodes for MetaTuner testing based on latest NodeVersion data

### 5.1 Priority Node Analysis (Completed 2025-12-31)
- [x] Create `find_priority_nodes.py` script
- [x] Query NodeTasks for latest NodeVersion per node
- [x] Calculate accuracy stats (TaskNodeAccuracy from NodeTasks)
- [x] Apply selection criteria
- [x] Generate priority node report (`04-outputs/priority-nodes.json`)

**Selection Criteria:**
- Accuracy: 60% - 99% (room for improvement, not broken)
- Min Tasks: ≥40 (enough data for testing)
- Min Failed: ≥5 tasks with <80% accuracy (has edge cases)

**Priority Nodes Found (Latest Version Only):**

| Node | Agent | Tasks | Failed | Accuracy | Variables |
|------|-------|-------|--------|----------|-----------|
| Extract All Case Info | Ops Case Handler | 73 | 6 | 91.9% | 1,408 |
| 1. Schreiben Bank | TZV Agent 03.09 | 60 | 9 | 87.5% | 120 |
| 2. TZV Zurück | TZV Agent 03.09 | 42 | 25 | 78.2% | 588 |

**Edge Case Nodes (High Failure Rate):**

| Node | Agent | Tasks | Failed | Accuracy |
|------|-------|-------|--------|----------|
| Receptionist (Inso) | Inso Agent MAGA | 45 | 44 | 50.8% |
| Generate request msg | B2B Check | 8 | 8 | 0.0% |

### 5.2 Dataset Generation (Completed 2026-01-01)

**CRITICAL FIX - Export Level Changed:**
- Export now at **NodeTask level** (was VariableTask level)
- One dataset item = one prompt execution with ALL outputs
- Fixed TaskNodeAccuracy parsing ("91%" → 0.91)
- Fixed dataset structure to match MetaTuner PromptDataset interface

**Export Tasks:**
- [x] Refactor export to NodeTask level
- [x] Fix TaskNodeAccuracy parsing (strip % suffix)
- [x] Match MetaTuner PromptDataset schema
  - [x] Dataset-level metadata (prompt template, agent, node)
  - [x] Item-level input (filled prompt only)
  - [x] Remove redundant item metadata
- [x] Re-export all 4 priority datasets
- [x] Organize outputs into folders (current/archive/analysis/inventory)

### 5.3 Input Parsing for MetaTuner (Completed 2026-01-02)

**ISSUE RESOLVED - Input Structure:**
- Input field was containing entire filled prompt (template + data mixed)
- MetaTuner requires separation: `input: {actual varying data}` + `metadata.prompt: template`

**Parsing Implementation:**
- [x] Create `parse_filled_prompt()` function in export_dataset.py
- [x] Implement Deal Breaker format parser (Extract Data node)
  - [x] Extracts document content from `# Data` section
  - [x] Extracts task_query JSON from task metadata
  - [x] Extracts prompt template (extraction instructions)
- [x] Implement TZV Agent format parser (5 datasets)
  - [x] Extracts task data dict from triple-backtick blocks
  - [x] Handles both `entire <task_query>` and alternative endings
  - [x] Covers: Schreiben Bank, TZV Zurück, Receptionist, SS Grouping, Group A
- [x] Implement Email Mgmt Assistant format parser
  - [x] Extracts email_content from @EmailContent parameter
- [x] Implement Ops Case Handler format parser
  - [x] Extracts structured input fields (ADM_Email, Optional, etc.)
- [x] Add fallback for unparsed formats (backward compatible)
- [x] Re-export all 8 datasets with proper parsing

**Final Status**:
- ✅ ALL 8 DATASETS SUCCESSFULLY PARSED
- ✅ 100% input/template separation achieved
- ✅ Ready for MetaTuner optimization

**Final Datasets (NodeTask Level - Latest Versions Only):**
| Dataset | Node | NodeTasks | Variables | Avg Score | Version |
|---------|------|-----------|-----------|-----------|---------|
| metatuner-1-schreiben-bank-gold.json | 1. Schreiben Bank | 60 | 114 | 0.88 | 2025-10-10 |
| metatuner-2-tzv-gold.json | 2. TZV Zurück | 42 | 301 | 0.68 | 2025-10-17 |
| metatuner-extract-all-case-info-gold.json | Extract All Case Info | 73 | 998 | 0.57 | 2025-09-18 |
| metatuner-receptionist-gold.json | 0. Receptionist | 42 | 544 | 0.80 | Latest |

**Total**: 217 NodeTasks with 1,957 output variables (latest versions only)

**Version Filtering**: Export now filters to latest version per node automatically

**Data Quality:**
- 100% input coverage (filled prompts)
- 100% score coverage (TaskNodeAccuracy)
- All datasets validated against MetaTuner interface

---

## Phase 6: Additional Datasets & Testing

### 6.1 Gather Additional Datasets (In Progress 2026-01-01)
- [x] Identify more high-quality nodes from priority list
- [x] Export additional gold tier datasets
  - [x] 3.0 SS Grouping (70 tasks, accuracy 98.6%)
  - [x] 3.1 Group A: Complex Overlaps (26 tasks, accuracy 91.3%)
  - [x] Extract Data (10 tasks, accuracy 93.3%)
  - [x] Classify Incoming Email (92 tasks, accuracy 95.7%)
- [ ] Export silver/bronze tiers for testing
- [ ] Export low-accuracy nodes for stress testing

**Current Collection**: 8 datasets, 415 NodeTasks, 2,949 variables

### 6.2 Manual Dataset Finalization (In Progress 2026-01-04)

Each dataset requires manual review and finalization due to different input structures per node/agent.

**Finalization Checklist per Dataset:**
- [ ] Verify input parsing (classification_context, pdf_content, etc.)
- [ ] Add proper metadata (promptType, agent, node, description)
- [ ] Validate PromptEvaluationMetricResult structure
- [ ] Copy to `final/` folder

**Prompt Types:**
- `extraction` - Extract structured data from documents
- `classification` - Categorize/classify content
- `generation` - Generate text/responses
- `routing` - Route to different paths/decisions

**Dataset Finalization Status:**

| Dataset | Agent | Node | Prompt Type | Status |
|---------|-------|------|-------------|--------|
| metatuner-0-receptionist-gold.json | TZV Agent | 0. Receptionist | classification | ✅ DONE |
| metatuner-1-schreiben-bank-gold.json | TZV Agent | 1. Schreiben Bank | extraction | ✅ DONE |
| metatuner-2-tzv-zurück-gold.json | TZV Agent | 2. TZV Zurück | extraction | ✅ DONE |
| metatuner-30-ss-grouping-gold.json | TZV Agent | 3.0 SS Grouping | extraction | ✅ DONE |
| metatuner-31-group-a-gold.json | TZV Agent | 3.1 Group A | extraction | ✅ DONE |
| metatuner-classify-incoming-email-gold.json | Email Mgmt | Classify Incoming Email | classification | ✅ DONE |
| metatuner-extract-all-case-info-gold.json | Ops Case Handler | Extract All Case Info | extraction | ✅ DONE |
| metatuner-extract-data-gold.json | Deal Breaker | Extract Data | extraction | ✅ DONE |

### 6.3 Full MetaTuner Interface (COMPLETED 2026-01-04)

Expanded export to include complete MetaTuner interface:

**Required Components:**
- [x] PromptDataset (name, description, items, metadata, tags)
- [x] PromptDatasetItem (id, input, expectedOutput, actualOutput, metadata)
- [x] PromptEvaluationResult & PromptEvaluationMetricResult
- [x] MetaTunerPromptInput (prompt, inputSchema, outputSchema, evals)
- [x] PromptEvaluation criteria (one eval per output parameter)
- [x] PromptExecutions bundle

**Final Export Structure (2026-01-04):**
```json
{
  "metadata": {
    "datasetName": "string",
    "agent": "string",
    "node": "string",
    "promptType": "extraction|classification|generation|routing",
    "tier": "gold|silver|bronze",
    "itemCount": number,
    "averageScore": number,
    "succeededCount": number,
    "failedCount": number,
    "generated_at": "ISO timestamp",
    "source": "airtable-export"
  },
  "metatunerPromptInput": {
    "prompt": "# Role... {placeholder}...",
    "inputSchema": { type, properties, required },
    "outputSchema": { type, properties, required },
    "evals": [{ id, name, criteria, threshold, evaluationParams }]
  },
  "promptDataset": { name, description, items[], metadata, tags },
  "PromptExecutions": { id, executions[] }
}
```

**Schema Refinements (2026-01-04):**
- Removed duplicate `inputParameters`/`outputParameters` (schema has descriptions)
- One PromptEvaluation per output parameter (not single checklist)
- Renamed `executions` → `PromptExecutions`
- Moved `metadata` to top, `datasetName` inside metadata

**Documentation:**
- [x] Created `02-resources/metatuner-complete-interface.md` - Full interface reference

### 6.4 Dataset Validation (COMPLETED 2026-01-04)
- [x] Validate all 8 datasets for schema correctness
- [x] Verify input/output data integrity
- [x] Check evaluation metrics consistency

**Validation Results:**
| Dataset | Items | Succeeded | Failed | Avg Score | Evals |
|---------|-------|-----------|--------|-----------|-------|
| metatuner-0-receptionist-gold.json | 42 | 8 | 34 | 0.92 | 20 |
| metatuner-1-schreiben-bank-gold.json | 60 | 51 | 9 | 0.88 | 2 |
| metatuner-2-tzv-zurück-gold.json | 42 | 7 | 35 | 0.78 | 10 |
| metatuner-30-ss-grouping-gold.json | 70 | 64 | 6 | 0.99 | 11 |
| metatuner-31-group-a-gold.json | 26 | 23 | 3 | 0.91 | 10 |
| metatuner-classify-incoming-email-gold.json | 92 | 88 | 4 | 0.96 | 1 |
| metatuner-extract-all-case-info-gold.json | 73 | 28 | 45 | 0.92 | 20 |
| metatuner-extract-data-gold.json | 10 | 5 | 5 | 0.93 | 11 |

**All 8 datasets passed:**
- Schema structure validation
- Input/output data integrity
- Evaluation metrics consistency

### 6.5 MetaTuner Testing
- [ ] Load datasets into MetaTuner
- [ ] Run optimization on high-value nodes
- [ ] Document optimization results
- [ ] Analyze improvement metrics

### 6.6 Skill Development
- [ ] Create Airtable export skill if successful
- [ ] Document usage and best practices

---

## Notes

**Current Status**:
- Phase 5.3 COMPLETED - All 8 datasets properly parsed with input/template separation
- Phase 6.1 COMPLETED - 8 datasets exported (415 NodeTasks) and properly formatted
- Phase 6.4 COMPLETED - Enhanced parser with full context extraction and evaluation results
- **READY**: All datasets ready for MetaTuner optimization testing
- Next: Test MetaTuner optimization on prepared datasets

**Dependencies**:
- Full CSV exports in `02-resources/`
- NodeTasks-ALL.csv (18,597 records) - contains filled prompts
- VariableTasks-WithExpected.csv (46,341 records) - contains expected/actual outputs

**Next Steps**:
1. ✅ **COMPLETED**: Input parsing for all 8 datasets
2. ✅ **COMPLETED**: Enhanced TZV parser with full context extraction
3. ✅ **COMPLETED**: Added evaluation results (PromptEvaluationResult)
4. **READY**: Test with MetaTuner prompt optimization
   - All datasets have proper input/template separation
   - Start with any dataset - all are ready
   - Document optimization results and improvements
5. **Optional**: Export additional datasets
   - Export silver/bronze tiers for wider testing
   - Export low-accuracy nodes for stress testing
6. **If successful**: Create Airtable export skill for reuse

---

## Parser Implementation Summary

### Enhanced TZV Agent Parser (2026-01-04)

**Problem**: Original parser only extracted task metadata, missing:
- Classification context (pre-classification reasoning)
- PDF attachment content (actual document text)

**Solution**: Updated `parse_filled_prompt()` to handle `# Data` section structure:

```
# Role + # Rules + # Document Context + # Variables = Static template
# Data section:
  ## Classification Context '''```{JSON}```''' = Pre-classification reasoning
  ## PDF attachment: '''```{document}```''' = Actual PDF content
  ## input '''```{task_metadata}```''' = Task metadata (beamTaskId, etc.)
```

**Input fields now extracted**:
- `classification_context`: Full pre-classification JSON with reasoning
- `pdf_content`: Document content (email/letter text)
- `task`: Task metadata JSON string
- `beamTaskId`: For Langfuse lookup
- `beamAgentOSTaskID`: Beam agent task ID
- `beamTaskTimestamp`: Execution timestamp
- `attachments`: File attachment references

### MetaTuner Interface Compliance

**PromptDataset structure**:
```typescript
{
  name: string,
  description: string,
  items: PromptDatasetItem[],
  metadata: { prompt, agent, node, tier, generated_at, source },
  tags: string[]
}
```

**PromptDatasetItem structure**:
```typescript
{
  id: string,                    // NodeTask UUID
  input: {
    classification_context,      // Pre-classification reasoning
    pdf_content,                 // Document content
    beamTaskId,                  // For Langfuse lookup
    attachments                  // File references
  },
  expectedOutput: Record<string, any>,
  actualOutput: Record<string, any>,
  metadata: {
    score: number,               // 0.0-1.0
    evaluation: PromptEvaluationResult,
    fullActualOutput: [...]      // Complete node output
  }
}
```

**PromptEvaluationResult structure**:
```typescript
{
  id: string,
  success: boolean,
  score: number,
  successRate: number,
  evaluations: PromptEvaluationMetricResult[]
}
```

**PromptEvaluationMetricResult structure**:
```typescript
{
  id: string,
  name: string,                  // Variable name
  score: number,                 // 0.0 or 1.0
  success: boolean,
  failureMode: string,           // "value_mismatch" | "missing_output" | ""
  expected: string,
  actual: string
}
```

### Evaluation Calculation

Accuracy is computed from expected vs actual comparison (not from VariableTaskAccuracy field which is unreliable):
- Normalize strings (lowercase, strip whitespace)
- Direct string match comparison
- Numeric comparison for decimal values (tolerance: 0.001)
- Failure modes: `value_mismatch`, `missing_output`

---

**Data Files:**
- `02-resources/DatasetVariables-FULL.csv` - 70,586 records
- `02-resources/VariableTasks-WithExpected.csv` - 46,341 records (filtered: with expected output)
- `02-resources/DatasetNodes-ALL.csv` - 4,964 records
- `02-resources/NodeTasks-ALL.csv` - 18,597 records
- `04-outputs/inventory-report-full.json` - Full inventory report

---

*Mark tasks complete with [x] as you finish them*
