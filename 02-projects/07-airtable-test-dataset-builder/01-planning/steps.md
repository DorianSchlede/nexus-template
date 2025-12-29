# Airtable Test Dataset Builder - Execution Steps

**Last Updated**: 2025-12-29

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

## Phase 5: Dataset-Konstruktion

Ziel: Spezifische Test-Datasets für verschiedene Use Cases

- [ ] Dataset Types definieren
  - [ ] Edge Cases (Accuracy < 0.5)
  - [ ] Happy Path (Accuracy > 0.9)
  - [ ] Regression (vorher failed, jetzt passed)
  - [ ] Full Agent (alle Cases eines Agents)
- [ ] Für jeden Agent Datasets generieren
  - [ ] Agent 1: [Name]
  - [ ] Agent 2: [Name]
  - [ ] (weitere nach Inventory)
- [ ] Datasets in `04-outputs/datasets/` speichern
- [ ] Metadata-Files pro Dataset erstellen

---

## Phase 6: Testing & Dokumentation

- [ ] Exported Datasets gegen MetaTuner testen
- [ ] Dokumentation aktualisieren
- [ ] Scripts dokumentieren (Usage, Examples)
- [ ] Bei Erfolg: Überlegen ob als Skill konvertieren

---

## Notes

**Current blockers**:
- None - VariableTasks-WithExpected.csv now has 46,341 records for all agents

**Dependencies**:
- Airtable API Zugriff (via .env AIRTABLE_API_KEY)
- Full CSV exports in `02-resources/` (DatasetVariables-FULL.csv, VariableTasks-ALL.csv, DatasetNodes-ALL.csv, NodeTasks-ALL.csv)

**Nächster Schritt**:
Phase 5 - Datasets für alle Agents generieren (oder VariableTasks-FULL.csv für vollständige Accuracy-Daten)

**Data Files:**
- `02-resources/DatasetVariables-FULL.csv` - 70,586 records
- `02-resources/VariableTasks-WithExpected.csv` - 46,341 records (filtered: with expected output)
- `02-resources/DatasetNodes-ALL.csv` - 4,964 records
- `02-resources/NodeTasks-ALL.csv` - 18,597 records
- `04-outputs/inventory-report-full.json` - Full inventory report

---

*Mark tasks complete with [x] as you finish them*
