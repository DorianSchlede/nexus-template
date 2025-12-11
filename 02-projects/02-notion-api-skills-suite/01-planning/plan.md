# Notion API Skills Suite - Plan

**Last Updated**: 2025-12-10

---

## Approach

**Meta-Skill Architecture**: Build ONE orchestrating skill (`notion-connect`) that:
1. Discovers user's Notion workspace on first use
2. Persists database schemas to `01-memory/integrations/notion-databases.yaml`
3. Routes to endpoint-specific workflows based on user intent
4. Learns database names as triggers for intelligent matching

**Progressive Build**: Start with MVP (3 endpoints), add capabilities in phases. Each phase is independently valuable.

---

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| **One meta-skill vs many small skills** | One meta-skill with internal routing | Simpler UX - user says "notion" and it figures out the rest |
| **Context storage location** | `01-memory/integrations/notion-databases.yaml` | Follows memory system pattern, loaded on startup if exists |
| **Extend notion-master vs new shared lib** | Extend `notion-master` | DRY principle - add new references/scripts to existing library |
| **Schema caching strategy** | Full schema in YAML, refresh on demand | Balance between startup speed and accuracy |
| **Database matching** | Fuzzy match by name | Natural language UX - "query Projects" matches "Client Projects" |

---

## Resources Needed

**Tools/Access**:
- Notion API key (already configured in `.env`)
- Notion workspace with databases to test

**Information/Data**:
- Notion API documentation (already researched)
- Property type mappings (20+ types)
- Filter/sort syntax

---

## Dependencies & Links

**Files to Create in `notion-connect/`** (meta-skill only):
- `00-system/skills/notion-connect/SKILL.md` - Meta-skill with routing logic

**Files to Create in `notion-master/scripts/`** (shared library - reusable):
- `discover_databases.py` - Discovery + schema caching
- `query_database.py` - Generic query with filters
- `create_page.py` - Page creation with validation
- `update_page.py` - Page update/delete
- `manage_blocks.py` - Block CRUD operations
- `manage_comments.py` - Comment operations
- `manage_files.py` - File upload/download
- `manage_users.py` - User listing

**Files to Create in `01-memory/`**:
- `integrations/notion-databases.yaml` - Persistent database context

**Files to Add to `notion-master/references/`**:
- `filter-syntax.md` - Query filter operators
- `property-types.md` - All 20+ property types with schemas
- `block-types.md` - All 50+ block types

**Existing Skills (Keep Separate)**:
- `query-notion-db` - Beam Skills database (specialized)
- `import-skill-to-nexus` - Skill import workflow
- `export-skill-to-notion` - Skill export workflow

**External Systems**:
- Notion API: `https://api.notion.com` - All endpoints
- Rate limit: 3 req/sec average

---

## Open Questions

- [x] Where to store persistent context? → `01-memory/integrations/`
- [x] One skill or many? → One meta-skill with routing
- [x] How to handle database name collisions? → Append parent page name for disambiguation: "Projects (Marketing)" vs "Projects (Engineering)"
- [x] Should we auto-refresh context on every session or on-demand only? → On-demand only (user says "refresh notion") - avoids startup latency
- [x] How to handle very large databases (1000+ pages)? → Paginate with cursor, show first 100 results, offer "load more" command

---

## Technical Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────────┐
│                     notion-connect (META-SKILL)                 │
│                                                                 │
│  SKILL.md: Routing logic + workflow definitions                 │
│                                                                 │
│  Workflows:                                                     │
│  ├── discover → Finds all databases, saves context              │
│  ├── query → Routes to database-specific query                  │
│  ├── create → Creates pages with property validation            │
│  ├── update → Updates pages/blocks                              │
│  └── advanced → Files, comments, users                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                     notion-master (SHARED LIB)                  │
│                                                                 │
│  scripts/                      references/                      │
│  ├── check_notion_config.py    ├── setup-guide.md              │
│  ├── discover_databases.py     ├── api-reference.md            │
│  ├── query_database.py         ├── error-handling.md           │
│  ├── create_page.py            ├── database-schema.md          │
│  ├── manage_blocks.py          ├── filter-syntax.md (NEW)      │
│  └── manage_files.py           ├── property-types.md (NEW)     │
│                                └── block-types.md (NEW)        │
└─────────────────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│              01-memory/integrations/notion-databases.yaml       │
│                                                                 │
│  Persistent context file - loaded when notion-connect triggers  │
│                                                                 │
│  last_synced: 2025-12-10T23:00:00                              │
│  databases:                                                     │
│    - id: "abc123"                                               │
│      name: "Client Projects"                                    │
│      properties: [...]                                          │
│    - id: "def456"                                               │
│      name: "Content Calendar"                                   │
│      properties: [...]                                          │
└─────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User: "Query my Projects database for active items"
                    │
                    ▼
┌──────────────────────────────────────┐
│ 1. notion-connect skill triggers     │
│    (matches "query" + "database")    │
└──────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│ 2. Load persistent context           │
│    Read: notion-databases.yaml       │
│    Find: "Projects" → id: abc123     │
└──────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│ 3. Execute query workflow            │
│    Run: query_database.py            │
│    --db abc123                        │
│    --filter "Status = Active"        │
└──────────────────────────────────────┘
                    │
                    ▼
┌──────────────────────────────────────┐
│ 4. Format and display results        │
│    Use property types for formatting │
│    Show: table/list based on data    │
└──────────────────────────────────────┘
```

### Technology Stack

- **Python 3.x** - Scripts for API interaction
- **YAML** - Persistent context storage (human-readable)
- **Notion API v2025-09-03** - Latest API version with data sources
- **requests** - HTTP client (already used in existing scripts)

---

## Implementation Strategy

### Development Phases

**Phase 1: MVP Foundation**
- Create `notion-connect/SKILL.md` with routing logic
- Create `discover_databases.py` script
- Create `query_database.py` script
- Create `01-memory/integrations/` directory
- Add `filter-syntax.md` reference
- Test: Discover databases → Query by name

**Phase 2: Page Operations**
- Add `create_page.py` script
- Add page update/delete to routing
- Add `property-types.md` reference
- Test: Create page in any database

**Phase 3: Block Operations**
- Add `manage_blocks.py` script
- Add block append/update/delete routing
- Add `block-types.md` reference
- Test: Append content to pages

**Phase 4: Advanced Features**
- Add file upload/download
- Add comments support
- Add users listing
- Add data sources (2025 API)

### Testing Approach

Each phase tested with:
1. **Happy path**: Standard operation works
2. **Error handling**: Invalid inputs handled gracefully
3. **Edge cases**: Empty results, rate limits, permissions
4. **Integration**: Works with existing Notion skills

### Deployment Plan

1. Create skill in `00-system/skills/notion-connect/`
2. Add scripts to `notion-master/scripts/`
3. Add references to `notion-master/references/`
4. Test with real Notion workspace
5. Document in skill SKILL.md

---

## Mental Models Applied

### First Principles Thinking
**Core question**: What's the simplest way to make Notion databases accessible via natural language?

**Fundamentals identified**:
1. User needs to reference databases by name, not ID
2. Schemas change rarely - cache them
3. Most operations are read (query) not write
4. One skill that "just works" > many specialized skills

### Pre-Mortem Analysis
**If this fails, it will be because...**

| Failure Mode | Mitigation |
|--------------|------------|
| Database name collisions | Show disambiguation prompt with URLs |
| Stale cached schemas | Add "refresh" command, show last_synced |
| Rate limiting | Batch requests, add backoff logic |
| Permission errors | Clear error messages, link to Notion sharing |
| Context file too large | Limit to 50 databases, paginate display |

### Stakeholder Mapping
**Who uses this?**
- **Primary**: Nexus users with Notion workspaces
- **Secondary**: Teams sharing databases
- **Affected**: Existing Notion skill users (no breaking changes)

---

## Skill Bundling Strategy

### Why ONE Meta-Skill vs Many Skills?

| Approach | Pros | Cons |
|----------|------|------|
| **Many skills** (notion-databases, notion-pages, notion-blocks) | Clear separation, focused triggers | User must know which to invoke, context switching |
| **One meta-skill** (notion-connect) | Natural language routing, unified context | Larger SKILL.md, more complex routing |

**Decision**: One meta-skill because:
1. User says "notion" → system figures out intent
2. Shared context (database schemas) loaded once
3. Easier to add new capabilities (just add workflow)
4. Matches user mental model ("I want to do something in Notion")

### Workflow Organization in SKILL.md

```markdown
## Workflows

### 0. Config Check (Always First)
Every workflow MUST start with config validation:
1. Run: `python notion-master/scripts/check_notion_config.py`
2. If missing API key/config → Trigger setup workflow (load setup-guide.md)
3. If valid → Continue to requested operation

### 1. Discover (First-Time / Refresh)
Triggers: "connect notion", "sync notion", "what databases"
→ discover_databases.py

### 2. Query
Triggers: "query [database]", "find in [database]", "search [database]"
→ query_database.py

### 3. Create
Triggers: "add to [database]", "create in [database]", "new [item]"
→ create_page.py

### 4. Update
Triggers: "update [page]", "edit [page]", "change [property]"
→ update_page.py (Phase 2)

### 5. Content (Blocks)
Triggers: "append to [page]", "add section", "edit content"
→ manage_blocks.py (Phase 3)

### 6. Advanced
Triggers: "upload file", "add comment", "list users"
→ Specific scripts (Phase 4)
```

---

*Next: Complete steps.md to break down execution tasks*
