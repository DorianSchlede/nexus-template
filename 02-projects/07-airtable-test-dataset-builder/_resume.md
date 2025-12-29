# Airtable Test Dataset Builder - Resume Context

> **Purpose**: Quick context load for next agent session
> **Last Updated**: 2025-12-29
> **Status**: Phase 4 Complete - Full VariableTasks Data Available

---

## Quick Start for Next Agent

### 1. Load These Files First

```
02-projects/07-airtable-test-dataset-builder/01-planning/steps.md     # Task checklist (UPDATED)
02-projects/07-airtable-test-dataset-builder/04-outputs/inventory-report-full.json  # Full inventory
```

### 2. Current State

| Phase | Status |
|-------|--------|
| Phase 1: Planning | DONE |
| Phase 2: Inventory | DONE |
| Phase 3: Validation | DONE |
| Phase 4: Export Script | DONE |
| **Phase 5: Dataset Construction** | **NEXT** |

---

## Project Goal

Build test datasets from Airtable for MetaTuner (prompt optimization algorithm).

**Key Insight**: Expected Output comes ONLY from Airtable (`DatasetVariables.Expected Value`), never from Langfuse.

---

## Full Inventory (2025-12-28)

### Table Counts

| Table | Records | File |
|-------|---------|------|
| DatasetVariables | 70,586 | `02-resources/DatasetVariables-FULL.csv` |
| VariableTasks | 46,341 | `02-resources/VariableTasks-WithExpected.csv` |
| DatasetNodes | 4,964 | `02-resources/DatasetNodes-ALL.csv` |
| NodeTasks | 18,597 | `02-resources/NodeTasks-ALL.csv` |

### Quality Tiers

| Tier | Count | Description | Use Case |
|------|-------|-------------|----------|
| **GOLD** | 20,045 | Human Reviewed (Review=1) | Best for training |
| SILVER | 54,868 | Status = Done | Usable test data |
| BRONZE | 21,963 | Has Expected Value | All available data |

### Top Agents with Test Data

| Agent | Expected Values | Reviewed |
|-------|-----------------|----------|
| TZV Agent 03.09 | 17,154 | 15,858 |
| CV Screening Agent v2 | 1,926 | 1,920 |
| Inso All-In-One Agent MAGA | 1,146 | 758 |
| Ops Case Handler (Prod) | 778 | 704 |
| B2B Check Agent | 575 | 533 |
| Deal Breaker | 244 | 213 |

### VariableTasks by Agent (46,341 total)

| Agent | VariableTasks |
|-------|---------------|
| TZV Agent 03.09 | 33,834 |
| Deal Breaker | 5,423 |
| Inso All-In-One Agent MAGA | 2,372 |
| CV Screening Agent v2 | 1,926 |
| Ops Case Handler | 1,767 |
| B2B Check Agent | 454 |

---

## Data Sources for MetaTuner Export

| MetaTuner Field | Source | Table.Field |
|-----------------|--------|-------------|
| `expectedOutput` | **Airtable** | DatasetVariables.Expected Value |
| `actualOutput` | Airtable | VariableTasks.AIValue |
| `prompt` | Airtable | NodeTasks.Filled Prompt |
| `score` | Airtable | VariableTasks.VariableTaskAccuracy |
| `input` | Airtable | AgentTasks.Actual Task Input |

---

## Phase 4 Results (Completed)

**Export Script**: `03-working/export_dataset.py`
- Filters by agent (--agent), quality tier (--tier: gold/silver/bronze), limit (--limit)
- Outputs MetaTuner-compatible JSON/JSONL
- Links DatasetVariables -> DatasetNodes -> NodeTasks for prompts

**Usage:**
```bash
python export_dataset.py --agent "Deal Breaker" --tier gold --verbose
python export_dataset.py --agent "TZV" --tier gold --limit 100
```

**Generated Datasets:**
- `04-outputs/datasets/metatuner-deal-breaker-gold.json` - 213 records, 100% prompts
- `04-outputs/datasets/metatuner-tzv-gold.json` - 100 records (limited), 100% prompts

---

## Next Steps (Phase 5)

1. **Analyze nodes** - Understand which nodes have expected outputs
2. **Count executions per node** - How many test cases per prompt
3. **Identify prompt types** - Extraction, Classification, Generation, etc.
4. **Generate datasets** - Per agent, per node type, edge cases vs happy path

---

## Key Files

```
03-working/inventory.py           # Inventory script (API-based)
03-working/export_dataset.py      # MetaTuner export script (CSV-based)
04-outputs/inventory-report-full.json  # Full inventory from CSV
04-outputs/datasets/              # Generated MetaTuner datasets
02-resources/*.csv                # Full table exports
```

---

## Table IDs (Reference)

```
Base ID: appFPoOfBpUv73M5A

| Table | ID |
|-------|-----|
| Agents | tblVEJD2inVhae855 |
| Nodes | tblPJ9VKG74mKv7JK |
| NodeVersions | tblh0GsN5Et3ApzLS |
| Variables | tblf2ohTHmsucjVUj |
| AgentTasks | tblsEzGhn4XJjNrkt |
| NodeTasks | tblNdPnVWDragZtcK |
| VariableTasks | tblKhpqLs06kI01yv |
| Datasets | tbltUrvSBnfOb4S8v |
| DatasetTasks | tbl9lACSI4fDUzAv4 |
| DatasetNodes | tblflNTX3tR0onX13 |
| DatasetVariables | tblsHYj8CrdHbY8Bt |
```

---

## Resolved Issues

- [x] NodeVersion link rate was 0% - Fixed: field name is `Node Version (from NodeTask)`
- [x] API too slow for 70k records - Solution: Use CSV exports in `02-resources/`

---

*Load steps.md for full task tracking*
