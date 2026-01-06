# Airtable Skill Development - Execution Steps

**Last Updated**: 2025-12-31
**Status**: ✅ **COMPLETE** (All phases done)

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Setup & Planning ✅ COMPLETE

- [x] Complete overview.md
- [x] Complete plan.md
- [x] Complete steps.md
- [x] Review planning docs

---

## Phase 2: Multi-Token Foundation ✅ COMPLETE

**Goal**: Alle existierenden Scripts um `--token` Parameter erweitern

- [x] Create shared utility: `airtable_utils.py` mit:
  - `get_api_key(token_name)` - multi-token support
  - `get_headers(token_name)` - headers helper
  - `make_request_with_retry()` - rate limit handling (extract from manage_records.py)
  - `update_context_file()` - cache updater (for later use)
- [x] Update `discover_bases.py` - add `--token` parameter
- [x] Update `query_records.py` - add `--token` parameter
- [x] Update `manage_records.py` - add `--token` parameter + use shared utils
- [x] Test: `python discover_bases.py --token MUTAGENT` → Found 3 bases
- [x] Test: Verify both tokens work independently → ✅

---

## Phase 3: Table Management Script ✅ COMPLETE

**Goal**: `manage_tables.py` analog zu Notion's `manage_database.py`

- [x] Read Notion's `manage_database.py` for reference (DONE in planning)
- [x] Create `manage_tables.py` skeleton with argparse
- [x] Implement `list` subcommand (GET /meta/bases/{baseId}/tables)
- [x] Implement `create` subcommand (POST /meta/bases/{baseId}/tables)
- [x] Implement `update` subcommand (PATCH /meta/bases/{baseId}/tables/{tableId})
- [x] Implement `update_context_file()` - auto-refresh airtable-bases.yaml after changes
- [x] Test: Create table in `app1gngDx52VAgjVQ` using MUTAGENT token → Created tbl83yYyFGvFDpv9V
- [x] Document in airtable-master SKILL.md

---

## Phase 4: Field Management Script ✅ COMPLETE

**Goal**: `manage_fields.py` für Schema-Änderungen

- [x] Read Airtable API docs for field endpoints
- [x] Create `manage_fields.py` skeleton
- [x] Implement `list` subcommand (from table schema)
- [x] Implement `create` subcommand (POST .../fields)
- [x] Implement `update` subcommand (PATCH .../fields/{fieldId})
- [x] Implement `types` subcommand (show available field types)
- [x] Test: Add fields to new table → Status (singleSelect), Description (multilineText)
- [x] Document in airtable-master SKILL.md

---

## Phase 5: airtable-connect Integration ✅ COMPLETE

**Goal**: User-facing skill mit neuen Workflows

- [x] Add Workflow 7: Create Table
- [x] Add Workflow 8: Manage Schema/Fields
- [x] Add multi-token documentation section
- [x] Update examples with `--token` usage
- [x] Test full workflow: create table → add fields → add records (documented in examples)

---

## Phase 6: Neue Base strukturieren ✅ COMPLETE

**Goal**: `app1gngDx52VAgjVQ` (Mutagent) aufbauen

- [x] Define table structure for Mutagent use case
- [x] Create tables using new scripts → Projects table created (tbl83yYyFGvFDpv9V)
- [x] Add fields to each table → Name, Status, Description
- [x] Verify schema in Airtable UI → Verified via manage_tables.py list
- [x] Document base structure in project outputs

**Current Structure**:
- Table 1 (default): 6 fields
- Projects: 3 fields (Name, Status, Description)

---

## Phase 7: Documentation & Cleanup ✅ COMPLETE

- [x] Update field-types.md reference doc → Already comprehensive
- [x] Create filter-syntax.md reference doc (MISSING vs Notion!) → Created
- [x] Add usage examples to all new scripts → In docstrings
- [x] Run full regression test on existing functionality → All passed
- [x] Create session report → See below
- [x] Mark project COMPLETE

**Regression Test Results** (2025-12-31):
- `discover_bases.py --token MUTAGENT` ✅ 3 bases
- `query_records.py --base app1gngDx52VAgjVQ --table Projects --token MUTAGENT` ✅
- `manage_fields.py types` ✅ 19 field types listed
- `manage_tables.py list --base app1gngDx52VAgjVQ --token MUTAGENT` ✅ 2 tables

---

## Phase 8: Skills Database & Import/Export ✅ COMPLETE

**Goal**: Store all local skills in Airtable with full bundles

- [x] Create Skills table (`tblsQL8n9EfMAFIyD`) with fields:
  - Name, Description, Version, Team, Purpose, Content
- [x] Create `upload_local_skills.py` - upload skills with JSON bundles
- [x] Upload 87 local skills (37 full, 50 partial due to size limit)
- [x] Create `download_skill.py` - download and extract from Airtable
- [x] Test round-trip: upload → download → verify ✅
- [x] Create unit tests (36 tests passing)

**Scripts Created**:
- `upload_local_skills.py` - Batch upload local skills
- `download_skill.py` - Download skills from Airtable
- `update_skill_metadata.py` - Update Purpose field

---

## Phase 9: Linked Tables for Complete Bundles ✅ COMPLETE

**Goal**: Store ALL files for large skills using linked tables

- [x] Design linked table schema (`linked-skills-schema.md`)
- [x] Create SkillFiles table (`tblhx8DRvcHN7GWmJ`)
- [x] Add Skill link field (`fldJWKWKeCpsWELX2`)
- [x] Create `upload_skill_files.py` for uploading individual files
- [x] Update `download_skill.py` for linked mode (`--files-table` option)
- [x] Upload 271 files for 11 partial skills
- [x] Add unit tests for linked table operations (42 tests total)

**Tables**:
| Table | ID | Records | Purpose |
|-------|-----|---------|---------|
| Skills | `tblsQL8n9EfMAFIyD` | 87 | Main skill records (76 full, 11 partial) |
| SkillFiles | `tblhx8DRvcHN7GWmJ` | 271 | Individual files for partial skills |

**New Scripts**:
- `upload_skill_files.py` - Upload files to SkillFiles linked table
- `download_skill.py --files-table` - Download with linked file support

---

## Notes

**Current blockers**: None

**Dependencies**:
- Airtable API Key MUTAGENT already configured in .env
- Base `app1gngDx52VAgjVQ` exists and accessible

**Test Commands**:
```bash
# Phase 2 validation
python scripts/discover_bases.py --token MUTAGENT --json

# Phase 3 validation
python scripts/manage_tables.py create --base app1gngDx52VAgjVQ --name "Projects" --token MUTAGENT

# Phase 4 validation
python scripts/manage_fields.py create --base app1gngDx52VAgjVQ --table "Projects" --name "Status" --type singleSelect --token MUTAGENT
```

---

## Code Reference (Notion → Airtable Mapping)

### Pattern 1: Multi-Token get_api_key()
```python
def get_api_key(token_name: str = None) -> str:
    """Get API key supporting multiple tokens."""
    load_env()  # Ensure .env loaded
    if token_name:
        key_name = f"AIRTABLE_API_KEY_{token_name.upper()}"
    else:
        key_name = "AIRTABLE_API_KEY"

    api_key = os.environ.get(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not set in .env")
    return api_key

def get_headers(token_name: str = None):
    """Get API headers with optional token selection."""
    api_key = get_api_key(token_name)
    return {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
```

### Pattern 2: manage_tables.py (analog Notion manage_database.py)
```python
# Airtable API for Table Creation
# POST https://api.airtable.com/v0/meta/bases/{baseId}/tables

def create_table(base_id, name, fields, token_name=None):
    headers = get_headers(token_name)
    url = f"https://api.airtable.com/v0/meta/bases/{base_id}/tables"

    body = {
        "name": name,
        "fields": [build_field_schema(f) for f in fields]
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    # ... error handling like Notion
```

### Pattern 3: Field Schema Builder (analog Notion build_property_schema)
```python
def build_field_schema(field_def):
    """Build Airtable field schema from simplified definition."""
    field_type = field_def.get('type', 'singleLineText')
    schema = {
        "name": field_def.get('name'),
        "type": field_type
    }

    # Type-specific options
    if field_type == 'singleSelect':
        schema["options"] = {
            "choices": [{"name": opt} for opt in field_def.get('choices', [])]
        }
    elif field_type == 'multipleSelects':
        schema["options"] = {
            "choices": [{"name": opt} for opt in field_def.get('choices', [])]
        }
    elif field_type == 'number':
        schema["options"] = {
            "precision": field_def.get('precision', 0)
        }
    # ... etc

    return schema
```

### Airtable Field Types Reference
| Type | Airtable Name | Options |
|------|---------------|---------|
| Text | `singleLineText` | - |
| Long Text | `multilineText` | - |
| Number | `number` | precision |
| Single Select | `singleSelect` | choices |
| Multi Select | `multipleSelects` | choices |
| Date | `date` | dateFormat |
| Checkbox | `checkbox` | - |
| URL | `url` | - |
| Email | `email` | - |
| Phone | `phoneNumber` | - |
| Currency | `currency` | precision, symbol |
| Percent | `percent` | precision |
| Rating | `rating` | max, icon |
| Duration | `duration` | format |

### Notion Script → Airtable Script Mapping
| Notion Script | → | Airtable Script | Status |
|--------------|---|-----------------|--------|
| `manage_database.py` | → | `manage_tables.py` | **TO CREATE** |
| `manage_blocks.py` | → | `manage_fields.py` | **TO CREATE** |
| `discover_databases.py` | → | `discover_bases.py` | EXISTS (add --token) |
| `check_notion_config.py` | → | `check_airtable_config.py` | EXISTS (add --token) |
| `search_skill_database.py` | → | `query_records.py` | EXISTS (add --token) |
| `create_page.py` | → | (via manage_records.py create) | EXISTS |
| `manage_page.py` | → | `manage_records.py` | EXISTS (add --token) |

---

*Mark tasks complete with [x] as you finish them*
