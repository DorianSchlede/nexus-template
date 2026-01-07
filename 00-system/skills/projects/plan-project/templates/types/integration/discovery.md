# {{project_name}} - Discovery

**Project Type**: Integration
**Discovery Method**: add-integration skill

---

## Discovery Status

**Skill Used**: add-integration
**Load Command**: `python 00-system/core/nexus-loader.py --skill add-integration`

*This file is populated by the add-integration skill during discovery.*

---

## Service Information

| Attribute | Value |
|-----------|-------|
| Service Name | {{service_name}} |
| Service Slug | {{service_slug}} |
| Base URL | {{base_url}} |
| Auth Type | {{auth_type}} |
| Environment Key | {{env_key}} |
| API Docs | {{api_docs_url}} |

---

## Rate Limits

{{rate_limits}}

---

## Selected Endpoints

| Endpoint | Method | Path | Description |
|----------|--------|------|-------------|
| {{name}} | {{method}} | {{path}} | {{description}} |

---

## Authentication Details

{{auth_details}}

---

## Dependencies

### Files to Create

| File | Purpose |
|------|---------|
| `03-skills/{{service_slug}}/{{service_slug}}-master/SKILL.md` | Shared resources |
| `03-skills/{{service_slug}}/{{service_slug}}-connect/SKILL.md` | Connection setup |
| `03-skills/{{service_slug}}/{{service_slug}}-{{operation}}/SKILL.md` | Per-endpoint skill |

### External Systems

- {{service_name}} API

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Rate limiting | Medium | Medium | Implement backoff |
| Auth token expiry | Low | High | Auto-refresh logic |

---

*Populated by add-integration skill*
