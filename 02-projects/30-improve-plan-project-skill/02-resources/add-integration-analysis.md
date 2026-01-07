# Add-Integration Skill Analysis

**Location**: `00-system/skills/system/add-integration/`

---

## What It Does (7 Steps)

1. **Step 1-2**: User names service → Claude does WebSearch for API docs
2. **Step 3-4**: Parse and cache API documentation (endpoints, auth, base URL)
3. **Step 5**: Present endpoint list → User selects which to implement
4. **Step 6**: Create integration project with config JSON
5. **Step 7**: Execute project using `scaffold_integration.py`

---

## File Structure

```
add-integration/
├── SKILL.md                          # 7-step workflow definition
├── scripts/
│   └── scaffold_integration.py       # Generates entire integration structure
├── templates/
│   ├── master-skill.md.template      # Master skill template
│   ├── connect-skill.md.template     # Connect skill template
│   ├── operation-skill.md.template   # Per-endpoint skill
│   ├── api-client.py.template        # Shared API client
│   ├── config-check.py.template      # Pre-flight validation
│   ├── setup-wizard.py.template      # Interactive setup
│   ├── operation-script.py.template  # Endpoint script
│   └── references/
│       ├── api-reference.md.template
│       ├── authentication.md.template
│       ├── error-handling.md.template
│       └── setup-guide.md.template
└── references/
    ├── integration-architecture.md   # 3-tier pattern docs
    ├── integration-ideas.md          # Use cases/inspiration
    ├── mcp-guide.md                  # MCP setup instructions
    ├── mcp-introduction.md           # MCP conceptual overview
    ├── mcp-setup-guide.md            # Detailed MCP setup
    └── troubleshooting-guide.md      # Error resolution
```

---

## Integration Config JSON Format

```json
{
  "service_name": "HubSpot",
  "service_slug": "hubspot",
  "base_url": "https://api.hubapi.com",
  "auth_type": "oauth2|api_key|bearer",
  "env_key": "HUBSPOT_API_KEY",
  "api_docs_url": "https://developers.hubspot.com/docs/api",
  "endpoints": [
    {
      "name": "List Contacts",
      "slug": "list-contacts",
      "method": "GET",
      "path": "/crm/v3/objects/contacts",
      "description": "Retrieve all contacts",
      "triggers": ["list contacts", "get contacts"]
    }
  ]
}
```

---

## Generated Output Structure (3-Tier Architecture)

```
03-skills/{service}/
├── {service}-master/           # Tier 1: Shared resources (NEVER loaded directly)
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── {service}_client.py
│   │   ├── check_{service}_config.py
│   │   └── setup_{service}.py
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
├── {service}-connect/          # Tier 2: User entry point
│   └── SKILL.md
└── {service}-{operation}/      # Tier 3: Per-endpoint skills
    ├── SKILL.md
    └── scripts/
        └── {operation}.py
```

---

## Key Workflow Features to Preserve

1. **Web Search for API Discovery** - Uses WebSearch to find API docs
2. **Endpoint Selection UI** - User picks which endpoints to implement
3. **Scaffolding Script** - Generates all files from templates
4. **3-Tier Architecture** - Master/Connect/Operation pattern
5. **Config Check Pattern** - `--json` flag for AI-consumable output

---

## Modification for Router Pattern

When called from plan-project:
- **Skip Step 6** (project creation) - already done by plan-project
- **Accept project_path parameter** - where to store config
- **Return config JSON** - for plan-project to store in 02-resources/

```yaml
# Entry mode from plan-project
entry_mode: "from_router"
project_path: "02-projects/31-hubspot-integration/"
skip_steps: [6]  # Don't create project
output:
  config_json: "02-resources/integration-config.json"
  ready_for_scaffold: true
```
