# Master Skill Architecture Patterns

**Extracted from notion-master analysis - proven patterns for building master skills.**

---

## Core Principles

### 1. DRY (Don't Repeat Yourself)

**Problem:** Multiple skills share identical content
- Setup instructions repeated 3x
- API documentation repeated 3x
- Error handling tables repeated 3x
- Total: 950 lines duplicated

**Solution:** Extract to master skill
- Single source of truth
- Child skills reference, not duplicate
- Result: 60% context reduction

### 2. Progressive Disclosure

**Pattern:** Load resources only when needed

```markdown
# In child skill SKILL.md:

## Setup
Run pre-flight check first.
**Need setup?** See [Setup Guide](../integration-master/references/setup-guide.md)

## Errors
**Troubleshooting?** See [Error Handling](../integration-master/references/error-handling.md)
```

**Benefits:**
- Smaller initial context
- On-demand loading
- Faster skill execution

### 3. Clear Boundaries

**Master skill NEVER:**
- Loaded directly by users
- Contains interactive workflows
- Processes user requests

**Master skill ALWAYS:**
- Declares "DO NOT load directly" in description
- Lists which child skills use it
- Provides resources only

---

## Folder Structure Pattern

```
{integration}-master/
│
├── SKILL.md                    # Resource library declaration
│                               # - YAML metadata with "DO NOT load" warning
│                               # - Purpose and architecture sections
│                               # - Resource catalog
│                               # - Integration pattern documentation
│
├── references/                 # Documentation (markdown)
│   ├── setup-guide.md         # First-time setup wizard
│   ├── api-reference.md       # API patterns and endpoints
│   ├── error-handling.md      # Troubleshooting guide
│   └── [domain-specific].md   # Schema, filters, types, etc.
│
├── scripts/                    # Reusable utilities (Python)
│   ├── check_config.py        # Pre-flight validation
│   ├── discover_resources.py  # Resource discovery
│   ├── [operation].py         # CRUD and query scripts
│   └── rate_limiter.py        # Rate limit handling (if API)
│
└── tests/                      # Validation framework
    ├── README.md              # Test documentation
    └── run_tests.py           # Test runner
```

---

## SKILL.md Pattern

```yaml
---
name: {integration}-master
description: Shared resource library for {Integration} skills. DO NOT load directly - provides common references and scripts used by {child-1}, {child-2}, {child-3}.
---
```

**Required Sections:**

1. **Warning Banner** - "This is NOT a user-facing skill"
2. **Purpose** - What problem it solves, which skills use it
3. **Architecture** - DRY principle, context reduction metrics
4. **Shared Resources** - Catalog of references/ and scripts/
5. **Integration Pattern** - How child skills reference resources
6. **Usage Example** - User flow showing master is never loaded
7. **Version Info** - Version, dates, changelog

---

## Reference File Patterns

### setup-guide.md

**Structure:**
1. Pre-flight check (quick validation)
2. First-time setup wizard (step-by-step)
3. Configuration files (.env, user-config.yaml)
4. Validation commands
5. Troubleshooting table

**Key Elements:**
- Clear numbered steps
- Code blocks for commands
- Expected outputs
- Common pitfalls

### api-reference.md

**Structure:**
1. Base URL and headers
2. Authentication
3. Key endpoints with examples
4. Request/response formats
5. Rate limits
6. Pagination patterns

**Key Elements:**
- curl examples
- JSON schemas
- Status codes
- Official doc links

### error-handling.md

**Structure:**
1. Error code table (code, message, cause, solution)
2. Skill-specific errors
3. Configuration errors
4. Network errors
5. Troubleshooting steps
6. Recovery patterns
7. Debugging tips

**Key Elements:**
- Actionable solutions
- Code examples for recovery
- Debug commands

---

## Script Patterns

### check_config.py

**Purpose:** Validate all configuration before operations

**Pattern:**
```python
def main():
    print("[1/N] Checking .env file...")
    # Check required environment variables

    print("[2/N] Checking user-config.yaml...")
    # Check optional user config

    print("[3/N] Testing API connection...")
    # Make test API call

    # Return exit codes:
    # 0 = All configured
    # 1 = Partial config
    # 2 = Failed
```

### discover_resources.py

**Purpose:** Find and cache available resources

**Pattern:**
```python
def discover():
    # Call API to list resources
    # Extract schemas/properties
    # Save to context file (YAML)
    # Support --refresh flag
    # Support --json output
```

### rate_limiter.py

**Purpose:** Handle API rate limits gracefully

**Pattern:**
```python
def make_request_with_retry(method, url, headers, max_retries=3):
    for attempt in range(max_retries):
        response = requests.request(method, url, headers=headers)
        if response.status_code == 429:
            wait = 2 ** attempt  # Exponential backoff
            time.sleep(wait)
            continue
        return response
    raise Exception("Max retries exceeded")
```

---

## Integration Pattern

### How Child Skills Reference Master

**In child SKILL.md:**

```markdown
## Prerequisites

Before using this skill, ensure {Integration} is configured.

**Quick check:**
\`\`\`bash
python 00-system/skills/{integration}-master/scripts/check_config.py
\`\`\`

**First time setup?** See [{Integration} Setup Guide](../{integration}-master/references/setup-guide.md)

## Workflow

1. Run pre-flight check
2. Execute operation using master scripts
3. Handle errors per [Error Guide](../{integration}-master/references/error-handling.md)
```

### Script Execution Pattern

```bash
# Always from Nexus root
python 00-system/skills/{integration}-master/scripts/check_config.py
python 00-system/skills/{integration}-master/scripts/discover_resources.py
python 00-system/skills/{integration}-master/scripts/query_resources.py --filter "..."
```

---

## Metrics to Track

| Metric | How to Measure |
|--------|----------------|
| **Lines Reduced** | Total lines in child skills before vs after |
| **Context Reduction %** | (before - after) / before * 100 |
| **Child Skills Served** | Count of skills referencing master |
| **Test Coverage** | Tests passing / total tests |

**Target:** 50%+ context reduction across 3+ child skills

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why It's Bad | Do This Instead |
|--------------|--------------|-----------------|
| Loading master directly | Confuses users | Clear "DO NOT load" warning |
| Duplicating reference content | Defeats purpose | Reference via path |
| Hardcoding paths in scripts | Breaks portability | Discover Nexus root dynamically |
| Skipping validation script | Config errors slip through | Always run check_config first |
| No tests | Regressions go unnoticed | Minimum test coverage |

---

**Last Updated:** 2025-12-11
**Source:** notion-master architecture analysis
