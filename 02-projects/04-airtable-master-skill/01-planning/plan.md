# Airtable Master Skill - Plan

**Last Updated**: 2025-12-11

---

## Approach

Build a **shared resource library** (master skill) for Airtable integration, following the proven notion-master architecture pattern:

1. **Extract common patterns** from Airtable API research
2. **Create reusable references** (setup, API, errors, field types)
3. **Build utility scripts** (config check, discovery, CRUD)
4. **Enable child skills** to reference without duplication

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **Auth method** | Personal Access Tokens (PATs) | API keys deprecated Feb 2024 |
| **Python library** | Direct requests (not pyairtable) | Keep dependency-light, more control |
| **Rate limiting** | Built-in exponential backoff | 5 req/s per base limit |
| **Base discovery** | Cache to YAML context file | Reduce API calls, faster access |
| **Field type reference** | Separate domain-specific doc | Airtable has 20+ field types |

---

## Resources Needed

**Tools/Access**:
- Airtable Personal Access Token
- Python 3.x with `requests` and `pyyaml`

**Information/Data**:
- Airtable API documentation (captured in research.md)
- Field type specifications

---

## Dependencies & Links

**Files Impacted**:
- `.env` - Will store `AIRTABLE_API_KEY`
- `01-memory/user-config.yaml` - Optional `airtable_user_id`
- `01-memory/integrations/airtable-bases.yaml` - Discovered bases cache

**External Systems**:
- Airtable API: https://api.airtable.com/v0

**Related Projects**:
- notion-master skill (architecture reference)
- create-master-skill skill (templates)

**Skills/Workflows**:
- `airtable-connect` - Meta-skill using this master (future)
- `airtable-query` - Query operations (future)
- `airtable-sync` - Import/export (future)

---

## Technical Architecture

### Master Skill Structure

```
airtable-master/
├── SKILL.md                    # Resource library declaration
├── references/
│   ├── setup-guide.md          # PAT creation, .env config
│   ├── api-reference.md        # Endpoints, headers, pagination
│   ├── error-handling.md       # Error codes, recovery patterns
│   └── field-types.md          # All 20+ Airtable field types
├── scripts/
│   ├── check_airtable_config.py    # Pre-flight validation
│   ├── discover_bases.py           # Find accessible bases
│   ├── query_records.py            # List/filter records
│   └── manage_records.py           # CRUD operations
└── tests/
    ├── README.md
    └── run_tests.py
```

### Child Skills Architecture

```
User Request → Child Skill → Master Scripts → Airtable API
                    ↓
            Master References (on-demand)
```

### Data Flow

1. User invokes child skill (e.g., "query my Tasks base")
2. Child skill runs `check_airtable_config.py`
3. Child skill runs `discover_bases.py` if needed
4. Child skill runs specific operation script
5. Results returned to user

---

## Implementation Strategy

### Phase 1: Core Infrastructure
- [ ] Create folder structure
- [ ] SKILL.md with "DO NOT load directly" declaration
- [ ] setup-guide.md (PAT creation, .env config)
- [ ] check_airtable_config.py (validate PAT, test connection)

### Phase 2: API Documentation
- [ ] api-reference.md (endpoints, headers, pagination)
- [ ] error-handling.md (error codes, recovery)
- [ ] field-types.md (all field types with formats)

### Phase 3: Utility Scripts
- [ ] discover_bases.py (find and cache bases)
- [ ] query_records.py (list with filters)
- [ ] manage_records.py (create, update, delete)

### Phase 4: Validation
- [ ] Basic test suite
- [ ] Manual testing with real Airtable base
- [ ] Documentation review

---

## Mental Models Applied

### Socratic Questioning
- **Q:** What assumptions am I making about users' Airtable setup?
- **A:** They have at least one base with data. Handle empty bases gracefully.

- **Q:** Why not use pyairtable SDK?
- **A:** Keeps Nexus dependency-light, gives full control over requests, educational value.

### Devil's Advocate
- **Risk:** Rate limits could block heavy operations
- **Mitigation:** Built-in exponential backoff, batch operations (10 records max)

- **Risk:** Field types change over time
- **Mitigation:** Reference official docs, note API version in references

### DRY Analysis (from notion-master)
- **Without master skill:** 3 child skills × 300 lines = 900 lines duplicated
- **With master skill:** 400 lines in master + 3 × 100 lines = 700 lines
- **Savings:** ~22% context reduction + single source of truth

---

*Next: Complete steps.md to break down execution*
