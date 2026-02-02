---
name: google-sheets
description: "Read and write Google Sheets data. Load when user mentions 'google sheets', 'spreadsheet', 'update sheet', 'read sheet', 'append to sheet', or references extracting data to update a tracking sheet."
version: 1.2
---

# Google Sheets

Read, write, and manage Google Sheets via OAuth authentication.

## Pre-Flight Check (ALWAYS FIRST)

```bash
uv run python 00-system/skills/google/google-master/scripts/google_auth.py --check --service sheets
```

**Exit codes:**
- **0**: Ready - proceed with user's request
- **1**: Need login - run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
- **2**: Missing deps - see [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

---

## Quick Reference

### Read Data
```bash
uv run python 00-system/skills/google/google-sheets/scripts/sheets_operations.py read <spreadsheet_id> "Sheet1!A1:D10"
```

### Write Data
```bash
uv run python 00-system/skills/google/google-sheets/scripts/sheets_operations.py write <spreadsheet_id> "Sheet1!A1" --values '[["Name", "Amount"], ["Contract A", 5000]]'
```

### Append Rows
```bash
uv run python 00-system/skills/google/google-sheets/scripts/sheets_operations.py append <spreadsheet_id> "Sheet1!A:D" --values '[["New Row", "Data", "Here", "Now"]]'
```

### Get Sheet Info
```bash
uv run python 00-system/skills/google/google-sheets/scripts/sheets_operations.py info <spreadsheet_id>
```

### List Spreadsheets
```bash
uv run python 00-system/skills/google/google-sheets/scripts/sheets_operations.py list --query "tracking"
```

### Create Spreadsheet
```bash
uv run python 00-system/skills/google/google-sheets/scripts/sheets_operations.py create "New Spreadsheet" --sheets "Data" "Summary"
```

---

## Common Workflows

### Extract Data -> Update Sheet

```python
from sheets_operations import append_rows

data = [
    ["Contract A", "2024-01-15", 5000, "Active"],
    ["Contract B", "2024-02-01", 7500, "Pending"]
]
result = append_rows(spreadsheet_id, "Contracts!A:D", data)
print(f"Added {result['updated_rows']} rows")
```

### Batch Update Multiple Cells

```python
from sheets_operations import batch_update

data = [
    {"range": "Sheet1!A1", "values": [["Header 1"]]},
    {"range": "Sheet1!B1", "values": [["Header 2"]]},
]
batch_update(spreadsheet_id, data)
```

---

## Spreadsheet ID

The spreadsheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/[SPREADSHEET_ID]/edit
```

---

## A1 Notation

| Example | Meaning |
|---------|---------|
| `A1` | Single cell |
| `A1:B5` | Range from A1 to B5 |
| `Sheet1!A1:B5` | Range in specific sheet |
| `A:A` | Entire column A |
| `1:1` | Entire row 1 |

---

## Available Operations

| Operation | Function | Description |
|-----------|----------|-------------|
| **Read** | `read_range()` | Read data from range |
| **Write** | `write_range()` | Write data to range |
| **Append** | `append_rows()` | Append rows to sheet |
| **Clear** | `clear_range()` | Clear values (keep formatting) |
| **Batch** | `batch_update()` | Update multiple ranges |
| **Create** | `create_spreadsheet()` | Create new spreadsheet |
| **Info** | `get_spreadsheet_info()` | Get metadata and sheets |
| **List** | `list_spreadsheets()` | List accessible spreadsheets |

---

## Error Handling

See [../google-master/references/error-handling.md](../google-master/references/error-handling.md) for common errors and solutions.

---

## Setup

First-time setup: [../google-master/references/setup-guide.md](../google-master/references/setup-guide.md)

**Quick start:**
1. `pip install google-auth google-auth-oauthlib google-api-python-client`
2. Create OAuth credentials in Google Cloud Console (enable Google Sheets API & Drive API, choose "Desktop app")
3. Add to `.env` file at Nexus root:
   ```
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   GOOGLE_PROJECT_ID=your-project-id
   ```
4. Run `python3 00-system/skills/google/google-master/scripts/google_auth.py --login`
