# Airtable Skill Development - Plan

**Last Updated**: 2025-12-31

---

## Approach

**Analogous Reasoning**: Notion-Skill als exakte Vorlage nutzen.

1. **Gap-Analyse**: Notion-Scripts mit Airtable-Scripts vergleichen
2. **Portieren**: Fehlende Scripts 1:1 von Notion nach Airtable adaptieren
3. **Multi-Token**: Alle Scripts um `--token` Parameter erweitern
4. **Test**: Mit neuer Base `app1gngDx52VAgjVQ` validieren

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Script-Struktur | Notion 1:1 kopieren | Konsistenz, bewährtes Pattern |
| Multi-Token | `--token NAME` Flag | Einfach, flexibel, .env-basiert |
| Token-Naming | `AIRTABLE_API_KEY_{NAME}` | Convention, leicht erweiterbar |
| Default Token | `AIRTABLE_API_KEY` | Backward-compatible |

---

## Technical Architecture

### Neue Scripts (zu erstellen)

```
airtable-master/scripts/
├── manage_tables.py      # CREATE/UPDATE/DELETE tables (analog manage_database.py)
├── manage_fields.py      # ADD/UPDATE/DELETE fields (analog manage_blocks.py)
└── [existing scripts]    # Alle erweitern um --token
```

### Multi-Token Pattern

```python
# In jedem Script:
def get_api_key(token_name: str = None) -> str:
    """Get API key from .env, supporting multiple tokens."""
    if token_name:
        key = f"AIRTABLE_API_KEY_{token_name.upper()}"
    else:
        key = "AIRTABLE_API_KEY"
    return os.getenv(key)

# CLI:
parser.add_argument("--token", help="Token name (e.g., MUTAGENT -> uses AIRTABLE_API_KEY_MUTAGENT)")
```

### API Endpoints benötigt

| Operation | Endpoint | Method |
|-----------|----------|--------|
| Create Table | `/meta/bases/{baseId}/tables` | POST |
| Update Table | `/meta/bases/{baseId}/tables/{tableId}` | PATCH |
| Create Field | `/meta/bases/{baseId}/tables/{tableId}/fields` | POST |
| Update Field | `/meta/bases/{baseId}/tables/{tableId}/fields/{fieldId}` | PATCH |

---

## Dependencies & Links

**Files Impacted**:
- `00-system/skills/airtable/airtable-master/scripts/check_airtable_config.py` - Add --token
- `00-system/skills/airtable/airtable-master/scripts/discover_bases.py` - Add --token
- `00-system/skills/airtable/airtable-master/scripts/query_records.py` - Add --token
- `00-system/skills/airtable/airtable-master/scripts/manage_records.py` - Add --token + refactor to use utils
- `00-system/skills/airtable/airtable-master/scripts/export_base_schema.py` - Add --token
- `00-system/skills/airtable/airtable-master/scripts/setup_airtable.py` - Add --token (MISSED!)
- `00-system/skills/airtable/airtable-connect/SKILL.md` - Document multi-token

**New Files**:
- `00-system/skills/airtable/airtable-master/scripts/airtable_utils.py` - NEW (shared utilities)
- `00-system/skills/airtable/airtable-master/scripts/manage_tables.py` - NEW
- `00-system/skills/airtable/airtable-master/scripts/manage_fields.py` - NEW
- `00-system/skills/airtable/airtable-master/references/filter-syntax.md` - NEW

**Reference (Notion Analogs)**:
- `00-system/skills/notion/notion-master/scripts/manage_database.py` → `manage_tables.py`
- `00-system/skills/notion/notion-master/scripts/manage_blocks.py` → `manage_fields.py`

**External Systems**:
- Airtable Base: `app1gngDx52VAgjVQ` (Mutagent workspace) - Target für Tests
- Airtable Base: `appKMeDNFn4gJdccO` (AI Development Platform) - Existing

---

## Implementation Strategy

### Phase 1: Multi-Token Support (Foundation)
- Utility function `get_api_key(token_name)` erstellen
- Alle 5 existierenden Scripts um `--token` erweitern
- Test mit beiden Keys

### Phase 2: Table Management
- `manage_tables.py` erstellen (create/update/list)
- In airtable-connect SKILL.md dokumentieren
- Test: Table in `app1gngDx52VAgjVQ` erstellen

### Phase 3: Field Management
- `manage_fields.py` erstellen (create/update)
- Field-Type Reference Doc erweitern
- Test: Fields zu neuer Table hinzufügen

### Phase 4: Integration & Docs
- airtable-connect SKILL.md updaten
- Workflows für Table/Field Mgmt hinzufügen
- End-to-End Test

---

## Mental Models Applied

**Analogous Reasoning**:
- Notion-Skill = bewährte Architektur, 1:1 übertragen
- Gleiche Patterns = weniger cognitive load

**MECE (Mutually Exclusive, Collectively Exhaustive)**:
- Scripts klar getrennt: records vs tables vs fields
- Keine Überlappung, vollständige Abdeckung

---

## Open Questions

- [x] Welche Airtable API Endpoints für Table/Field Creation? → Dokumentiert oben
- [x] Fehlt setup_airtable.py im Plan? → JA, hinzugefügt zu Phase 2
- [x] Brauchen wir rate_limiter.py separat? → NEIN, extrahieren zu airtable_utils.py
- [x] Context file update nach Table/Field creation? → JA, hinzugefügt zu Phase 3
- [x] Fehlt filter-syntax.md Reference? → JA, hinzugefügt zu Phase 7
- [ ] Field-Type Validation in manage_fields.py? → Später, erstmal basic

---

*Next: Complete steps.md to break down execution*
