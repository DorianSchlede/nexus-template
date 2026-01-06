---
id: 11-airtable-skill-development
name: Airtable Skill Development
status: COMPLETE
description: "Load when user mentions 'airtable skill', 'expand airtable', 'airtable table creation', 'airtable field management', 'multi-token airtable', 'AIRTABLE_API_KEY_MUTAGENT'"
created: 2025-12-31
---

# Airtable Skill Development

## Purpose

Erweitern des existierenden Airtable-Skills um **Feature-Parität mit dem Notion-Skill** zu erreichen, plus **Multi-Token Support** für verschiedene Workspaces (z.B. `AIRTABLE_API_KEY` vs `AIRTABLE_API_KEY_MUTAGENT`).

**Problem**: Der aktuelle Airtable-Skill kann nur Records lesen/schreiben. Er kann keine:
- Tables erstellen oder Schema ändern
- Neue Bases strukturieren
- Zwischen verschiedenen API-Keys/Workspaces wechseln
- Field-Types managen (wie Notion's manage_blocks.py)

---

## Success Criteria

**Must achieve**:
- [ ] Multi-Token Support: Wechseln zwischen `AIRTABLE_API_KEY` und `AIRTABLE_API_KEY_MUTAGENT`
- [ ] Table Creation: Neue Tables in existierenden Bases erstellen können
- [ ] Schema Management: Fields hinzufügen/ändern in Tables
- [ ] Neue Base `app1gngDx52VAgjVQ` vollständig nutzbar

**Nice to have**:
- [ ] Field-Type Reference Docs (analog zu Notion's property-types.md)
- [ ] Workspace-Switcher in airtable-connect Skill

---

## Context

**Background**:
- Airtable-Skill existiert bereits mit 5 Scripts und 4 Reference-Docs
- Notion-Skill hat 13 Scripts (vollständiger)
- User hat 2 API-Keys: Standard + Mutagent Workspace
- Neue Base `app1gngDx52VAgjVQ` wurde erstellt, braucht Struktur

**Stakeholders**:
- Mutagent Team (nutzt Airtable für Projekt-Tracking)
- Nexus System (Integration-Skills)

**Constraints**:
- Airtable API kann KEINE Bases erstellen (nur Web-UI)
- Airtable API KANN Tables und Fields erstellen
- Rate Limit: 5 req/s per base

---

## Scope

**In Scope**:
1. `manage_tables.py` - Table CRUD operations
2. `manage_fields.py` - Field/Schema management
3. Multi-Token Routing in Scripts
4. Neue Base strukturieren (Tables, Fields)

**Out of Scope**:
- Base-Erstellung (API-Limitation)
- Airtable Automations
- Airtable Apps/Extensions

---

*Next: Complete plan.md to define the approach*
