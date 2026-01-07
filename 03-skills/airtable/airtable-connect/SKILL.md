---
name: airtable-connect
description: "airtable, connect airtable, query [base], add to [table]."
version: "1.1"
---

# Airtable Connect

**Meta-skill for complete Airtable workspace integration.**

## Purpose

Enable natural language interaction with ANY Airtable base. User says "query my Projects base" or "add a record to CRM" and it just works - no manual API calls, no remembering base IDs, no schema lookups.

---

## Shared Resources

This skill uses `airtable-master` shared library. Load references as needed:

| Resource | When to Load |
|----------|--------------|
| `airtable-master/scripts/check_airtable_config.py` | Always first (pre-flight) |
| `airtable-master/references/setup-guide.md` | If config check fails |
| `airtable-master/references/error-handling.md` | On any API errors |
| `airtable-master/references/api-reference.md` | For API details |
| `airtable-master/references/field-types.md` | For field type options |

---

## Multi-Token Support

Use `--token NAME` to switch between different Airtable workspaces/accounts:

```bash
# Default token (AIRTABLE_API_KEY)
python discover_bases.py

# Named token (AIRTABLE_API_KEY_MUTAGENT)
python discover_bases.py --token MUTAGENT
```

**Setup multiple tokens in `.env`:**
```
AIRTABLE_API_KEY=pat.xxx...          # Default token
AIRTABLE_API_KEY_MUTAGENT=pat.yyy... # Named token for Mutagent workspace
AIRTABLE_API_KEY_CLIENT=pat.zzz...   # Named token for client workspace
```

**All scripts support `--token`:**
- `discover_bases.py --token NAME`
- `query_records.py --token NAME`
- `manage_records.py --token NAME`
- `manage_tables.py --token NAME`
- `manage_fields.py --token NAME`

---

## First-Time User Setup

**If user has never used Airtable integration before:**

1. Run config check with JSON to detect setup state:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/check_airtable_config.py --json
   ```

2. Parse the `ai_action` field in JSON output:
   - `prompt_for_api_key` → Guide user to get PAT, add to .env
   - `run_setup_wizard` → Run interactive wizard
   - `proceed_with_warning` → Partial config, warn but continue
   - `proceed_with_operation` → All good, continue

3. If setup needed, help user:
   - Tell them: "Airtable needs a Personal Access Token (PAT)"
   - Link: https://airtable.com/create/tokens
   - Scopes needed: `data.records:read`, `data.records:write`, `schema.bases:read`
   - **Write directly to `.env`** when user provides token
   - Re-verify with config check

**Setup triggers**: "setup airtable", "connect airtable", "configure airtable"

---

## Workflow 0: Config Check (ALWAYS FIRST)

Every workflow MUST start with config validation:

```bash
python 00-system/skills/airtable/airtable-master/scripts/check_airtable_config.py --json
```

**Parse `ai_action` from JSON:**
- **`proceed_with_operation`**: Fully configured, continue
- **`proceed_with_warning`**: API works but no bases (warn user to add bases to PAT)
- **`prompt_for_api_key`**: Need API key, guide user through setup
- **`run_setup_wizard`**: Run setup wizard

**If not configured:**
1. Tell user: "Airtable integration needs to be set up first."
2. Either guide them manually OR run: `python 00-system/skills/airtable/airtable-master/scripts/setup_airtable.py`
3. Restart workflow after setup complete

---

## Workflow 1: Discover Bases

**Triggers**: "connect airtable", "sync airtable", "discover bases", "what bases", "refresh airtable"

**Purpose**: Find all accessible bases in user's Airtable workspace and cache schemas.

**Steps**:
1. Run config check (Workflow 0)
2. Run discovery script:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/discover_bases.py
   ```
3. Script outputs:
   - Number of bases found
   - Base names and IDs
   - Creates/updates: `01-memory/integrations/airtable-bases.yaml`
4. Show user summary of discovered bases
5. Confirm context file saved

**First-time flow**: If `airtable-bases.yaml` doesn't exist, discovery runs automatically.

---

## Workflow 2: Query Records

**Triggers**: "query [base]", "find in [table]", "search [base]", "show [table]", "list records"

**Purpose**: Query any base/table by name with optional filters.

**Steps**:
1. Run config check (Workflow 0)
2. Load context: Read `01-memory/integrations/airtable-bases.yaml`
   - If file doesn't exist → Run Workflow 1 (Discover) first
3. Match base name (fuzzy):
   - User says "Projects" → matches "Client Projects", "My Projects", etc.
   - If multiple matches → Show disambiguation prompt
   - If no match → Suggest running discovery
4. Run query:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/query_records.py \
     --base <base_id> --table <table_name> [--filter "..."] [--sort ...] [--limit N]
   ```
5. Format and display results using field types from cached schema
6. Offer follow-up actions: "Want to add a record?" / "Query with different filters?"

**Filter Syntax**:
- `--filter "Status = Active"`
- `--filter "Priority = High"`
- `--filter "{Field} contains Design"`

---

## Workflow 3: Create Record

**Triggers**: "add to [table]", "create in [base]", "new [item] in [table]"

**Purpose**: Create a new record in any table with field validation.

**Steps**:
1. Run config check (Workflow 0)
2. Load context and match base/table (same as Workflow 2)
3. Load schema for target table from context file
4. Prompt user for required fields based on schema:
   - Show field name + type + options (for single/multiple select)
   - Validate input against field type
5. Run create:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/manage_records.py create \
     --base <base_id> --table <table_name> \
     --fields '{"Name": "...", "Status": "..."}'
   ```
6. Confirm creation with record ID
7. Offer: "Add another?" / "View in Airtable?"

---

## Workflow 4: Update Record

**Triggers**: "update [record]", "edit [record]", "change [field] to [value]"

**Purpose**: Modify fields of an existing record.

**Steps**:
1. Run config check (Workflow 0)
2. Identify record:
   - By record ID if known
   - By search in table: `python query_records.py --filter "Name contains [search]"`
3. Show current field values
4. Accept changes from user
5. Run update:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/manage_records.py update \
     --base <base_id> --table <table_name> --record <record_id> \
     --fields '{"Status": "Done", "Priority": "High"}'
   ```
6. Confirm changes with updated record

---

## Workflow 5: Delete Record

**Triggers**: "delete [record]", "remove [record]"

**Purpose**: Delete a record from a table.

**Steps**:
1. Run config check (Workflow 0)
2. Identify record (by ID or search)
3. Confirm with user: "Are you sure you want to delete [record name]?"
4. Run delete:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/manage_records.py delete \
     --base <base_id> --table <table_name> --record <record_id>
   ```
5. Confirm deletion

---

## Workflow 6: Batch Operations

**Triggers**: "bulk update", "update multiple", "batch create"

**Purpose**: Create, update, or delete multiple records at once (max 10 per batch).

**Steps**:
1. Run config check (Workflow 0)
2. Collect records to process
3. Run batch operation:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/manage_records.py batch-create \
     --base <base_id> --table <table_name> \
     --records '[{"fields": {...}}, {"fields": {...}}]'
   ```
4. Report results (success/failure counts)

**Note**: Airtable limits batch operations to 10 records per request.

---

## Workflow 7: Create Table

**Triggers**: "create table", "new table in [base]", "add table to [base]"

**Purpose**: Create a new table in an existing Airtable base.

**Steps**:
1. Run config check (Workflow 0)
2. Load context and identify target base
3. List existing tables to avoid name conflicts:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/manage_tables.py list \
     --base <base_id> [--token NAME]
   ```
4. Collect table details from user:
   - Table name (required)
   - Description (optional)
   - Initial fields (optional, defaults to "Name" singleLineText)
5. Create table:
   ```bash
   python 00-system/skills/airtable/airtable-master/scripts/manage_tables.py create \
     --base <base_id> --name "Table Name" \
     --fields '[{"name": "Name", "type": "singleLineText"}, {"name": "Status", "type": "singleSelect", "options": {"choices": [{"name": "Todo"}, {"name": "Done"}]}}]' \
     [--token NAME]
   ```
6. Confirm creation with table ID
7. Offer: "Add more fields?" / "Create records?"

**Field Definition Format**:
```json
[
  {"name": "Name", "type": "singleLineText"},
  {"name": "Status", "type": "singleSelect", "options": {"choices": [{"name": "Todo"}, {"name": "In Progress"}, {"name": "Done"}]}},
  {"name": "Priority", "type": "number", "options": {"precision": 0}},
  {"name": "Due Date", "type": "date"}
]
```

---

## Workflow 8: Manage Schema/Fields

**Triggers**: "add field", "create field", "update field", "list fields", "show schema"

**Purpose**: Add, update, or list fields in a table.

### List Fields
```bash
python 00-system/skills/airtable/airtable-master/scripts/manage_fields.py list \
  --base <base_id> --table <table_id_or_name> [--token NAME]
```

### Create Field
```bash
python 00-system/skills/airtable/airtable-master/scripts/manage_fields.py create \
  --base <base_id> --table <table_id_or_name> \
  --name "Field Name" --type singleSelect \
  --choices "Option1,Option2,Option3" \
  [--token NAME]
```

### Update Field
```bash
python 00-system/skills/airtable/airtable-master/scripts/manage_fields.py update \
  --base <base_id> --table <table_id_or_name> --field <field_id> \
  --name "New Name" --description "Updated description" \
  [--token NAME]
```

### Show Available Field Types
```bash
python 00-system/skills/airtable/airtable-master/scripts/manage_fields.py types
```

**Common Field Types**:
| Type | Description | Options |
|------|-------------|---------|
| `singleLineText` | Short text | - |
| `multilineText` | Long text/notes | - |
| `number` | Numeric value | `precision` (0-8) |
| `singleSelect` | Dropdown (one) | `choices` |
| `multipleSelects` | Multi-select | `choices` |
| `date` | Date field | `dateFormat` |
| `checkbox` | Boolean toggle | - |
| `url` | Web link | - |
| `email` | Email address | - |
| `currency` | Money value | `precision`, `symbol` |
| `percent` | Percentage | `precision` |
| `rating` | Star rating | `max`, `icon` |

---

## Context File Format

**Location**: `01-memory/integrations/airtable-bases.yaml`

```yaml
---
last_synced: 2025-12-11T12:00:00
bases:
  - id: "appXXXXXXXXXXXXXX"
    name: "Client Projects"
    permission_level: "create"
    tables:
      - id: "tblXXXXXXXXXXXXXX"
        name: "Projects"
        fields:
          - name: "Name"
            type: "singleLineText"
          - name: "Status"
            type: "singleSelect"
            options: ["Not Started", "In Progress", "Complete"]
          - name: "Priority"
            type: "singleSelect"
            options: ["Low", "Medium", "High"]
          - name: "Due Date"
            type: "date"
  - id: "appYYYYYYYYYYYYYY"
    name: "CRM"
    permission_level: "edit"
    tables:
      - id: "tblYYYYYYYYYYYYYY"
        name: "Contacts"
        fields: [...]
---

# Airtable Bases Context

Auto-generated by airtable-connect skill.
Run "refresh airtable" to update.
```

---

## Fuzzy Matching Logic

When user says a base/table name:

1. **Exact match**: "Client Projects" → finds "Client Projects"
2. **Case-insensitive**: "client projects" → finds "Client Projects"
3. **Partial match**: "Projects" → finds "Client Projects", "Personal Projects"
4. **Word match**: "crm" → finds "Sales CRM", "CRM Database"

**Disambiguation prompt** (if multiple matches):
```
Found 3 bases matching "Projects":
1. Client Projects
2. Personal Projects
3. Project Templates

Which one? (enter number or be more specific)
```

---

## Error Handling

| Error | Action |
|-------|--------|
| No bases found | Check PAT has base access at https://airtable.com/create/tokens |
| Base not in context | Run discovery: "refresh airtable" |
| Permission denied | Verify PAT has correct scopes |
| Rate limited (429) | Wait and retry with exponential backoff |
| Invalid field | Show valid options from cached schema |

Load `airtable-master/references/error-handling.md` for detailed troubleshooting.

---

## Examples

**First-time setup**:
```
User: "connect to airtable"
AI: [Runs config check, detects no API key]
    Airtable integration needs setup. I need your Personal Access Token (PAT).

    Get one at: https://airtable.com/create/tokens
    Required scopes: data.records:read, data.records:write, schema.bases:read

    Paste your PAT here (starts with 'pat.'):

User: pat.xxxxx...
AI: [Writes to .env, re-runs config check]
    ✅ Connected! Found 3 bases: Client Projects, CRM, Tasks
    What would you like to do?
```

**Query by name**:
```
User: "query my Projects for active items"
AI: Querying "Client Projects" → "Projects" table...
    Found 12 active items:
    1. Website Redesign (High priority, due Jan 15)
    2. Q1 Marketing Plan (Medium priority, due Jan 30)
    ...
```

**Create record**:
```
User: "add a new task to my Tasks base"
AI: Creating in "Tasks" base → "Tasks" table.
    Required fields:
    - Task Name: [your input]
    - Status: Not Started / In Progress / Complete
    - Due Date: [optional, format: YYYY-MM-DD]

    What's the task name?
```

---

## Examples (with Multi-Token)

**Create table with MUTAGENT token**:
```
User: "create a Projects table in my Mutagent base"
AI: [Uses MUTAGENT token]
    Creating table "Projects" in base app1gngDx52VAgjVQ...

    python manage_tables.py create --base app1gngDx52VAgjVQ --name "Projects" --token MUTAGENT

    ✅ Table created: tbl83yYyFGvFDpv9V
    Want to add fields to this table?
```

**Add fields to new table**:
```
User: "yes, add Status and Description fields"
AI: Adding fields to Projects table...

    python manage_fields.py create --base app1gngDx52VAgjVQ --table tbl83yYyFGvFDpv9V \
      --name "Status" --type singleSelect --choices "Todo,In Progress,Done" --token MUTAGENT
    ✅ Created: Status (singleSelect)

    python manage_fields.py create --base app1gngDx52VAgjVQ --table tbl83yYyFGvFDpv9V \
      --name "Description" --type multilineText --token MUTAGENT
    ✅ Created: Description (multilineText)
```

**Full workflow: Create table → Add fields → Add record**:
```
User: "create a Tasks table with Name, Status, Priority, and DueDate fields"
AI: [Creates table, adds fields, confirms schema]

User: "add a task: Review PR, High priority, due tomorrow"
AI: [Uses manage_records.py to create record with proper field mapping]
```

---

*Airtable Connect v1.1 - Meta-skill for complete Airtable workspace integration with multi-token support*
