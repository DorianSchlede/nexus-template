# Airtable Master - Test Suite

## Overview

This test suite validates the airtable-master scripts work correctly with the Airtable API.

## Prerequisites

1. **Airtable Personal Access Token** configured in `.env`:
   ```
   AIRTABLE_API_KEY=pat.xxxxx
   ```

2. **At least one accessible base** in your Airtable workspace

3. **Python dependencies**:
   ```bash
   pip install requests pyyaml
   ```

## Running Tests

### Quick Validation (No API calls)
```bash
python run_tests.py --dry-run
```

### Full Test Suite
```bash
python run_tests.py
```

### Verbose Output
```bash
python run_tests.py --verbose
```

### Test Specific Script
```bash
python run_tests.py --script check_airtable_config
python run_tests.py --script discover_bases
python run_tests.py --script query_records
python run_tests.py --script manage_records
```

## Test Coverage

| Script | Tests | Description |
|--------|-------|-------------|
| `check_airtable_config.py` | 4 | Environment, config, API, base access |
| `discover_bases.py` | 3 | List bases, schema discovery, caching |
| `query_records.py` | 4 | List, filter, pagination, fields |
| `manage_records.py` | 3 | Create, update, delete (uses test table) |

## Test Data

The `manage_records` tests use a **Test Table** that is created and cleaned up automatically:
- Creates temporary test records
- Validates CRUD operations
- Deletes test records after completion

**Warning**: Do NOT run manage_records tests against production data tables.

## Expected Results

```
=== Airtable Master Test Suite ===

[1/4] Testing check_airtable_config.py...
  ✓ Environment check passed
  ✓ Config validation passed
  ✓ API connection passed
  ✓ Base access passed

[2/4] Testing discover_bases.py...
  ✓ List bases passed
  ✓ Schema discovery passed
  ✓ Cache creation passed

[3/4] Testing query_records.py...
  ✓ List records passed
  ✓ Filter records passed
  ✓ Pagination passed
  ✓ Field selection passed

[4/4] Testing manage_records.py...
  ✓ Create record passed
  ✓ Update record passed
  ✓ Delete record passed

=== Results ===
Passed: 14/14
Failed: 0
```

## Troubleshooting

### "AIRTABLE_API_KEY not set"
Add your PAT to `.env` file at Nexus root.

### "Could not find base"
Run `discover_bases.py` first to cache your bases.

### "Rate limited"
Wait 30 seconds and retry. Scripts have built-in backoff.

### "Permission denied"
Check your PAT scopes include the required permissions.
