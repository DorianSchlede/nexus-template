# Notion Skills Comprehensive Test Suite

Complete testing framework for all Notion integration scripts.

## Quick Start

```bash
# Run basic tests (36 tests, ~15s)
python 00-system/skills/notion/notion-master/tests/run_tests.py

# Run quick smoke tests (4 tests, ~3s)
python 00-system/skills/notion/notion-master/tests/run_tests.py --quick

# Run FULL test suite - ALL tests (~60s)
python 00-system/skills/notion/notion-master/tests/run_tests.py --full
```

## Test Suites

### 1. Basic Tests (`run_tests.py`)
Quick checks for script existence, help output, and basic functionality.

```bash
python run_tests.py                    # All basic tests
python run_tests.py --category query   # Specific category
python run_tests.py --quick            # Smoke tests only
```

**Categories:** config, discovery, search, pages, blocks, users, comments, skills, database, utils, integration

### 2. Script Integration Tests (`test_scripts.py`)
Tests each Python script's actual command-line behavior.

```bash
python test_scripts.py           # Run script tests
python test_scripts.py --verbose # With details
```

**Tests:** 32 tests covering all scripts

### 3. Live API Tests (`test_live_api.py`)
Direct API endpoint testing with real Notion operations.

```bash
python test_live_api.py          # Run API tests
python test_live_api.py --cleanup # Cleanup only
```

**Tests:** 31+ API operations including:
- GET/POST users
- Database queries with filters, AND logic, sorting, pagination
- Page create/read/update/archive
- Block append/read/update
- Rate limiting behavior
- **Skill search** (search_skill_database.py with filters, AND logic, JSON output)
- **Skill export** (upload_skill.py --dry-run validation, bundle creation)
- **Skill import** (download_skill.py error handling, validation)

**Note:** Creates and cleans up test data automatically.

## Full Suite

Run everything together:

```bash
python run_tests.py --full
```

This runs:
1. Basic tests (36 tests)
2. Script integration tests (32 tests)
3. Live API tests (31+ tests)

**Total: 99+ tests**

## Test Categories Detail

| Category | Count | Description |
|----------|-------|-------------|
| config | 6 | .env, API key, setup wizard |
| discovery | 3 | Database discovery, context |
| search | 6 | Skill search, filters, AND logic |
| pages | 4 | Page CRUD operations |
| blocks | 2 | Block management |
| users | 3 | User listing, bot info |
| comments | 2 | Comment operations |
| skills | 5 | Import/export validation |
| database | 2 | Schema management |
| utils | 2 | Rate limiter |
| integration | 1 | Full end-to-end flow |

## Live API Tests Detail

| Endpoint | Operations Tested |
|----------|-------------------|
| `/users/me` | Get current bot |
| `/users` | List all users |
| `/databases/{id}` | Get database |
| `/databases/{id}/query` | Basic, filter, AND, sort |
| `/search` | Search databases |
| `/pages` | Create, get, update, archive |
| `/blocks/{id}/children` | Append, list |
| `/blocks/{id}` | Get, update |
| `/comments` | List, create |
| Rate limiting | Rapid request handling |
| Pagination | Cursor-based paging |
| Skill Search | search_skill_database.py with --skills, --team, --json |
| Skill Export | upload_skill.py --dry-run validation |
| Skill Import | download_skill.py error handling |

## Requirements

- Python 3.8+
- requests
- pyyaml
- Notion API key in .env

## Writing New Tests

### Basic Test
```python
def test_your_feature(self) -> TestResult:
    start = time.time()
    # Test logic here
    passed = your_condition
    result = self._test("Test name", passed, "Details if failed")
    result.duration = time.time() - start
    return result
```

### Script Test
```python
def test_your_script(self):
    code, stdout, stderr = self._run('your_script.py', ['--arg'])
    if code == 0 and 'expected' in stdout:
        self._log("PASS", "Test name")
    else:
        self._log("FAIL", "Test name", f"Exit: {code}")
```

### Live API Test
```python
def test_api_endpoint(self):
    response = requests.get(url, headers=self.headers)
    if response.status_code == 200:
        self._log("PASS", "GET /endpoint")
    else:
        self._log("FAIL", "GET /endpoint", f"Status: {response.status_code}")
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All tests passed |
| 1 | One or more tests failed |

## Cleanup

Test data created by `test_live_api.py` is automatically archived after tests complete. To manually cleanup:

```bash
python test_live_api.py --cleanup
```

## Troubleshooting

**"No API key configured"**
- Add `NOTION_API_KEY` to `.env`

**"Comments API 403"**
- Integration needs "Insert comments" capability in Notion

**Tests timing out**
- Check network connection
- Increase timeout in test if needed
