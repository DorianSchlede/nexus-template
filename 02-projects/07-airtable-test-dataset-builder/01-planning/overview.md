---
id: 07-airtable-test-dataset-builder
name: Airtable Test Dataset Builder
status: PLANNING
description: "Load when user mentions 'test datasets', 'airtable datasets', 'metatuner testing', 'algorithm testing', 'export datasets', 'inventory datasets'"
created: 2025-12-28
---

# Airtable Test Dataset Builder

## Purpose

Erstelle exportierbare Test-Datasets aus der bestehenden AI Development Platform Airtable-Basis, um den MetaTuner (Prompt-Optimierungs-Algorithmus) systematisch zu testen.

**Problem**: Wir haben Expected Outputs in Airtable verteilt über verschiedene Agents/Workspaces, aber kein klares Bild davon, was existiert und wie wir es für Algorithmus-Tests nutzen können.

**Lösung**:
1. **Inventory** - Verstehen was wir haben (Expected Outputs pro Agent/Workspace/Node)
2. **Verknüpfungs-Validierung** - Sicherstellen dass DatasetVariables korrekt mit NodeVersions verbunden sind
3. **Export** - Lokale JSON/CSV Dateien für MetaTuner-kompatible Datasets
4. **Per-Agent Datasets** - Separate Test-Cases pro Workspace/Agent

---

## Success Criteria

**Must achieve**:
- [ ] Inventory-Report: Anzahl Expected Outputs pro Agent/Workspace/Node
- [ ] Validierte Verknüpfungen: DatasetVariables ↔ DatasetNodes ↔ NodeVersion
- [ ] Export-Script: Airtable → lokale MetaTuner-kompatible JSON Dateien
- [ ] Mindestens 3 verschiedene Dataset-Typen (Edge Cases, Happy Path, Regression)

**Nice to have**:
- [ ] Import-Script: Lokale Dateien → zurück nach Airtable
- [ ] Coverage-Report: Welche Nodes haben keine Expected Outputs
- [ ] Dashboard/Visualisierung der Dataset-Qualität

---

## Context

**Background**:
- MetaTuner braucht Test-Datasets mit: `input`, `prompt`, `actualOutput`, `expectedOutput`, `score`
- Airtable AI Development Platform hat bereits:
  - `DatasetVariables.Expected Value` (Ground Truth)
  - `NodeTasks.Filled Prompt` + `Node Output` (Actual Executions)
  - `VariableTasks.Accuracy` (Scores)
- Verknüpfungskette: DatasetVariables → DatasetNodes → NodeVersion → Prompt

**Stakeholders**:
- Entwickler (MetaTuner-Testing)
- QA (Regression-Tests)

**Constraints**:
- Keine neue Airtable-Datenbank erstellen
- Export muss lokal nutzbar sein (JSON/CSV)
- Muss Agent/Workspace-spezifisch filtern können

---

## Key Data Relationships

```
Workspace (1) → Agents (N)
Agent (1) → Nodes (N) → Variables (N)
Agent (1) → AgentVersions (N) → NodeVersions (N)

DatasetVariables.Expected Value
    ↓ linked via
DatasetNodes (→ NodeVersion.Prompt)
    ↓ linked via
DatasetTasks (→ Agent, AgentVersion)
    ↓ linked via
Datasets (→ Agents)
```

---

## Timeline

**Phase 1**: Inventory & Validierung
**Phase 2**: Export-Scripts
**Phase 3**: Dataset-Konstruktion

---

*Next: Complete plan.md to define your approach*
