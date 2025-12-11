---
name: add-integration
description: Build a new API integration for Nexus. Load when user mentions "add integration", "new integration", "integrate with", "connect to [service]", or "build [service] integration". Interactive workflow that discovers API endpoints, plans the integration, and creates a project for implementation.
---

# Add Integration

Build complete API integrations following the master/connect/specialized pattern.

## Purpose

The `add-integration` skill transforms API documentation into a complete, production-ready integration. It:

1. **Discovers** available API endpoints via web search
2. **Presents** endpoints for user selection
3. **Plans** the integration architecture
4. **Creates a project** for implementation

**Architecture Pattern**: See [references/integration-architecture.md](references/integration-architecture.md)

**Time Estimate**: 15-25 minutes (planning phase)

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────┐
│                   ADD INTEGRATION                        │
├─────────────────────────────────────────────────────────┤
│  Step 1: Ask which service to integrate                 │
│  Step 2: Web search for API documentation               │
│  Step 3: Parse and present available endpoints          │
│  Step 4: User selects endpoints to implement            │
│  Step 5: Gather authentication details                  │
│  Step 6: Create integration project with full plan      │
│  Step 7: Prompt user to close session & start project   │
└─────────────────────────────────────────────────────────┘
```

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Ask which service to integrate
- [ ] Search for API documentation
- [ ] Parse and present endpoints
- [ ] User selects endpoints
- [ ] Gather authentication details
- [ ] Create integration project
- [ ] Close session
```

**Mark tasks complete as you finish each step.**

---

### Step 2: Interactive Service Selection

Display:
```
Let's build a new integration! 🔌

Which service would you like to integrate?

Examples:
• HubSpot (CRM, marketing automation)
• Stripe (payments, subscriptions)
• Twilio (SMS, voice, messaging)
• Airtable (databases, spreadsheets)
• Slack (messaging, notifications)
• GitHub (repos, issues, PRs)
• Linear (issue tracking)
• Notion (notes, databases)
• Or any service with a REST API

Tell me the service name:
```

**Wait for user response.**

**Capture and normalize**:
- Store service name (e.g., "HubSpot")
- Generate slug (e.g., "hubspot")
- Note any specific features mentioned

---

### Step 3: Web Search for API Documentation

**CRITICAL: Use WebSearch to find current API documentation**

```
AI Action:
1. WebSearch: "{service_name} REST API documentation endpoints"
2. WebSearch: "{service_name} API reference authentication"
3. Identify official API docs URL
4. Use WebFetch on official docs to get endpoint details
```

**Search targets**:
- Official API documentation
- Authentication methods
- Available endpoints by category
- Rate limits and requirements

**Display progress**:
```
Searching for {Service} API documentation...

Found:
• Official docs: {url}
• API version: {version}
• Auth type: {oauth2/api_key/bearer}
```

---

### Step 4: Parse and Present Endpoints

After fetching API docs, categorize and present:

```
I found {N} API endpoints for {Service}:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AUTHENTICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [1] POST /oauth/token - Get access token
  [2] POST /oauth/refresh - Refresh token

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CATEGORY 1} (e.g., CONTACTS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [3] GET /contacts - List all contacts
  [4] GET /contacts/{id} - Get contact by ID
  [5] POST /contacts - Create contact
  [6] PATCH /contacts/{id} - Update contact
  [7] DELETE /contacts/{id} - Delete contact

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{CATEGORY 2} (e.g., DEALS)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [8] GET /deals - List deals
  [9] POST /deals - Create deal
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Which endpoints do you want to implement?

Options:
• "all" - Implement everything ({N} endpoints)
• "1,3,5,8" - Select by number
• "contacts, deals" - Select by category
• "core" - Essential CRUD operations only
```

**Wait for user response.**

---

### Step 5: Gather Authentication Details

Based on API docs discovered:

```
Authentication Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{Service} uses {auth_type} authentication.

To set up:
{auth_instructions from API docs}

I'll need this info for the integration config:

1. API Base URL: {detected_base_url}
   Is this correct? (or provide alternative)

2. Auth type: {oauth2/api_key/bearer}
   Confirm or correct

3. Environment variable name suggestion:
   {SERVICE_SLUG}_API_KEY

   Okay? Or suggest different name
```

**Wait for user confirmation/corrections.**

---

### Step 6: Create Integration Project

**Use create-project skill internally** to create a project for implementation.

**Project structure**:
```
02-projects/{next_id}-{service_slug}-integration/
├── 01-planning/
│   ├── overview.md          # Project metadata
│   └── steps.md             # Implementation checklist
├── 02-resources/
│   └── integration-config.json   # Captured configuration
├── 03-working/
└── 04-outputs/
```

**overview.md content**:
```yaml
---
id: {next_id}-{service_slug}-integration
name: {Service Name} Integration
status: PLANNING
description: Load when user mentions '{service_slug} integration', 'implement {service_slug}', 'build {service_slug} skills'
created: {today}
---

# {Service Name} Integration

Build complete {Service Name} integration following the master/connect/specialized pattern.

## Scope

- **Service**: {Service Name}
- **Base URL**: {base_url}
- **Auth Type**: {auth_type}
- **Endpoints**: {count} selected

## Architecture

Will create:
- `{service_slug}-master/` - Shared resources
- `{service_slug}-connect/` - Meta-skill entry point
- `{service_slug}-{operation}/` - One skill per endpoint

## References

- API Docs: {api_docs_url}
- Pattern: See 00-system/skills/system/add-integration/references/integration-architecture.md
```

**steps.md content**:
```markdown
# Implementation Steps

## Phase 1: Setup Master Skill
- [ ] Create {service_slug}-master/ directory structure
- [ ] Generate {service_slug}_client.py from template
- [ ] Generate check_{service_slug}_config.py
- [ ] Generate setup_{service_slug}.py wizard
- [ ] Create references/setup-guide.md
- [ ] Create references/api-reference.md
- [ ] Create references/error-handling.md
- [ ] Create references/authentication.md

## Phase 2: Setup Connect Skill
- [ ] Create {service_slug}-connect/ directory
- [ ] Generate SKILL.md with routing table
- [ ] Map workflows to endpoints

## Phase 3: Create Operation Skills
{for each selected endpoint:}
- [ ] Create {service_slug}-{endpoint_slug}/ skill
- [ ] Generate SKILL.md with API reference
- [ ] Generate {endpoint_slug}.py script

## Phase 4: Test & Validate
- [ ] Run config check script
- [ ] Test authentication flow
- [ ] Test each endpoint script
- [ ] Verify error handling

## Phase 5: Documentation
- [ ] Update master SKILL.md with all skills
- [ ] Document any service-specific quirks
- [ ] Add usage examples
```

**integration-config.json content**:
```json
{
  "service_name": "{Service Name}",
  "service_slug": "{service_slug}",
  "base_url": "{base_url}",
  "auth_type": "{auth_type}",
  "env_key": "{ENV_KEY}",
  "api_docs_url": "{api_docs_url}",
  "endpoints": [
    {
      "name": "{Endpoint Name}",
      "slug": "{endpoint-slug}",
      "method": "GET|POST|PATCH|DELETE",
      "path": "/api/path",
      "description": "{description}",
      "triggers": ["trigger phrase 1", "trigger phrase 2"],
      "parameters": []
    }
  ],
  "created": "{timestamp}",
  "created_by": "add-integration skill"
}
```

**Display confirmation**:
```
Project Created!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 02-projects/{id}-{service_slug}-integration/

This project contains:
• Full implementation plan in steps.md
• Configuration saved in integration-config.json
• {N} endpoints ready to implement

The implementation will create:
• {service_slug}-master/ (shared resources)
• {service_slug}-connect/ (meta-skill)
• {count} operation skills

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 7: Prompt Close Session & Start Implementation

**Final message**:
```
Integration planning complete! 🎉

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Say "done" to close this session
   (This saves your planning work)

2. Start a new session

3. Say "work on {service_slug} integration"
   (This will execute the implementation project)

The project will guide you through:
• Creating all skill folders
• Generating scripts from templates
• Setting up authentication
• Testing each endpoint

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to close this session? Say "done"
```

**Wait for user to say "done"** → Triggers close-session skill

---

## Project Execution Notes

When the user returns and says "work on {service} integration", the `execute-project` skill will:

1. **Load** the integration-config.json
2. **Run** scaffold_integration.py with the config:
   ```bash
   python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
     --config 02-projects/{id}-{service_slug}-integration/02-resources/integration-config.json
   ```
3. **Check off** steps.md tasks as completed
4. **Guide** through testing and validation

---

## Templates & Scripts

### Templates (in templates/)
- `master-skill.md.template` - Master SKILL.md
- `connect-skill.md.template` - Connect SKILL.md
- `operation-skill.md.template` - Operation SKILL.md
- `api-client.py.template` - API client class
- `config-check.py.template` - Config validator
- `setup-wizard.py.template` - Setup wizard
- `operation-script.py.template` - Operation script
- `references/*.template` - Reference documents

### Scripts (in scripts/)
- `scaffold_integration.py` - Main scaffolding script

---

## Error Handling

### Web Search Fails
```
I couldn't find official API documentation for {Service}.

Options:
1. Provide the API docs URL directly
2. Tell me the base URL and auth type manually
3. Try a different service name

What would you like to do?
```

### No Endpoints Found
```
I found {Service} docs but couldn't parse specific endpoints.

Let me try:
1. Fetching a different docs page
2. You provide endpoint list manually

Which approach?
```

### User Cancels
```
No problem! Integration planning cancelled.

Your progress was not saved. Run "add integration"
again when you're ready.
```

---

## Notes

**Why projects?**
- Integration implementation is multi-step work (project)
- Planning is reusable (skill handles discovery)
- Separates planning from execution

**Why web search?**
- APIs change frequently
- Ensures current endpoint info
- Discovers auth requirements automatically

**Pattern consistency**:
- All integrations follow same architecture
- Matches existing Beam integration
- Templates ensure quality

---

## References

- [Integration Architecture](references/integration-architecture.md) - The pattern explained
- [MCP Introduction](references/mcp-introduction.md) - What MCP is
- [MCP Setup Guide](references/mcp-setup-guide.md) - Manual MCP setup
- [Troubleshooting](references/troubleshooting-guide.md) - Common issues
- [Integration Ideas](references/integration-ideas.md) - Use cases

---

**Version**: 2.0
**Updated**: 2025-12-11
**Major change**: Now creates projects for implementation instead of doing everything in one session
