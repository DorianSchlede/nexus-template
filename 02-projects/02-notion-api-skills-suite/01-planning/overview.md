---
id: 02-notion-api-skills-suite
name: Notion API Skills Suite
status: COMPLETE
description: "Load when user mentions 'notion', 'notion API', 'connect notion', 'notion databases', 'notion pages', 'notion blocks', or any database name from persistent context. Meta-skill architecture for complete Notion workspace integration."
created: 2025-12-10
updated: 2025-12-11
completed: 2025-12-11
---

# Notion API Skills Suite

## Purpose

Build a complete Notion API integration using a **meta-skill architecture** that:
1. **Discovers** all databases in user's Notion workspace
2. **Builds persistent context** over time (database schemas, property types, relationships)
3. **Routes intelligently** to endpoint-specific workflows based on user intent
4. **Wraps ALL Notion API endpoints** into reusable, composable skills

**Value**: User says "query my Projects database" or "add a page to CRM" and it just works - no manual API calls, no remembering database IDs, no schema lookups.

---

## Success Criteria

**Must achieve**:
- [ ] Meta-skill discovers all accessible Notion databases automatically
- [ ] Persistent context file stores database IDs + schemas for instant access
- [ ] User can query ANY database by name (fuzzy match)
- [ ] User can create pages in any database with property validation
- [ ] Database CREATE/UPDATE operations (schema management)
- [ ] Block-level content manipulation (append, edit, delete)
- [ ] All 29 Notion API endpoints wrapped in skills

**Nice to have**:
- [ ] File upload/download support
- [ ] Comment threading on pages
- [ ] User listing for @mentions
- [ ] Data source support (2025 API)

---

## Context

**Background**:
- Existing Notion skills (`query-notion-db`, `import-skill-to-nexus`, `export-skill-to-notion`) only work with the Beam Skills database
- Users have many OTHER Notion databases they want to interact with
- Current approach requires manual database ID lookup and schema discovery each time
- Need a meta-skill that learns user's workspace and enables natural language interaction

**Stakeholders**:
- Nexus users who use Notion as their primary workspace
- Teams sharing Notion databases for collaboration

**Constraints**:
- Notion API rate limit: 3 requests/second average
- Must follow existing `notion-master` shared resource pattern (DRY)
- Must use progressive disclosure (don't load all schemas at startup)
- Must persist context to `01-memory/integrations/` for cross-session learning

---

## Timeline

**Target**: Complete in 4 phases

**Milestones**:
- Phase 1 (MVP): Database discovery + smart queries - 1 session
- Phase 2: Page CRUD operations - 1 session
- Phase 3: Block manipulation - 1 session
- Phase 4: Advanced (files, comments, users, data sources) - 1-2 sessions

---

## Scope: All Notion API Endpoints

### Phase 1: Foundation (MVP)
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/search` | POST | Discover all databases |
| `/v1/databases/{id}` | GET | Retrieve schema |
| `/v1/databases/{id}/query` | POST | Query with filters |

### Phase 1.5: Database Management
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/databases` | POST | Create new database |
| `/v1/databases/{id}` | PATCH | Update database schema |

### Phase 2: Pages
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/pages` | POST | Create page |
| `/v1/pages/{id}` | GET | Retrieve page |
| `/v1/pages/{id}` | PATCH | Update page |
| `/v1/pages/{id}` | DELETE | Trash page |
| `/v1/pages/{id}/properties/{id}` | GET | Get property |

### Phase 3: Blocks
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/blocks/{id}` | GET | Retrieve block |
| `/v1/blocks/{id}/children` | GET | List children |
| `/v1/blocks/{id}/children` | PATCH | Append children |
| `/v1/blocks/{id}` | PATCH | Update block |
| `/v1/blocks/{id}` | DELETE | Delete block |

### Phase 4: Advanced
| Category | Endpoints |
|----------|-----------|
| Users | `/v1/users`, `/v1/users/{id}`, `/v1/users/me` |
| Comments | `/v1/comments` (create, list, get) |
| Files | `/v1/files` (create, send, complete, get, list) |
| Data Sources | `/v1/data_sources` (2025 API) |

---

*Next: Complete plan.md to define architecture and approach*
