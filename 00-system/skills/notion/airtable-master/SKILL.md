---
name: airtable-master
description: Shared resource library for Airtable integration skills. DO NOT load directly - provides common references (setup, API docs, error handling, field types) and scripts used by airtable-connect, airtable-query, and airtable-sync.
---

# Airtable Master

**This is NOT a user-facing skill.** It's a shared resource library.

## Purpose

Provides shared resources to eliminate duplication across:
- `airtable-connect` - Connect to bases, discover schema
- `airtable-query` - Query records with filters
- `airtable-sync` - Import/export records

**Instead of loading this skill**, users invoke the specific skill above.

---

## Architecture: DRY Principle

**Problem solved:** Multiple Airtable skills would have duplicated content (setup instructions, API docs, error handling).

**Solution:** Extract shared content into `references/` and `scripts/`.

**Result:** Single source of truth, reduced context per skill.

---

## Shared Resources

### references/

**[setup-guide.md](references/setup-guide.md)** - Complete setup wizard
- Creating Personal Access Token (PAT)
- Configuring .env file
- Selecting scopes
- Validation steps

**[api-reference.md](references/api-reference.md)** - API patterns
- Base URL and headers
- Key endpoints (bases, tables, records)
- Pagination
- Batch operations
- Rate limits

**[error-handling.md](references/error-handling.md)** - Troubleshooting
- HTTP error codes (401, 403, 404, 422, 429)
- Recovery patterns
- Debugging tips

**[field-types.md](references/field-types.md)** - Field type reference
- All 20+ Airtable field types
- Read and write formats
- Type-specific validation

### scripts/

**[check_airtable_config.py](scripts/check_airtable_config.py)** - Pre-flight validation
- Checks .env for AIRTABLE_API_KEY
- Tests API connection
- Returns actionable errors

**[discover_bases.py](scripts/discover_bases.py)** - Base discovery
- Finds all accessible bases
- Gets table schemas
- Saves to context file

**[query_records.py](scripts/query_records.py)** - Record querying
- List records with filters
- Pagination handling
- Formatted output

**[manage_records.py](scripts/manage_records.py)** - CRUD operations
- Create, update, delete records
- Batch operations (up to 10)
- Field type handling

---

## How Skills Reference This

Each skill loads shared resources **only when needed** (progressive disclosure):

**airtable-connect** uses:
- `check_airtable_config.py` (validate before connection)
- `discover_bases.py` (find and cache bases)
- `api-reference.md` (schema endpoints)
- `error-handling.md` (troubleshooting)

**airtable-query** uses:
- `check_airtable_config.py` (validate before query)
- `query_records.py` (list/filter records)
- `api-reference.md` (query patterns)
- `field-types.md` (interpret results)

**airtable-sync** uses:
- `check_airtable_config.py` (validate before sync)
- `manage_records.py` (CRUD operations)
- `api-reference.md` (batch patterns)
- `error-handling.md` (recovery)

---

## Usage Example

**User says:** "query my Projects base in Airtable"

**What happens:**
1. AI loads `airtable-query` (NOT airtable-master)
2. `airtable-query` SKILL.md says: "Run check_airtable_config.py first"
3. AI executes: `python airtable-master/scripts/check_airtable_config.py`
4. AI executes: `python airtable-master/scripts/query_records.py --base "Projects"`
5. If errors occur, AI loads: `airtable-master/references/error-handling.md`

**airtable-master is NEVER loaded directly** - it's just a resource library.

---

## Key Differences from Notion

| Aspect | Airtable | Notion |
|--------|----------|--------|
| Auth | Personal Access Token (PAT) | Integration Token |
| Rate Limit | 5 req/s per base | 3 req/s |
| Batch Size | 10 records | Variable |
| Pagination | Offset-based | Cursor-based |
| Field Types | 20+ types | 20+ property types |

---

**Version**: 1.0
**Created**: 2025-12-11
**Status**: Production Ready
