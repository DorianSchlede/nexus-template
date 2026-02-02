# Integration Architecture Pattern

This document explains the master/connect/specialized pattern used for building integrations in Nexus.

---

## Overview

Integrations follow a **three-tier architecture**:

```
{service}/
├── {service}-master/        # Tier 1: Shared resources (NEVER loaded directly)
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── {service}_client.py      # API client
│   │   ├── check_{service}_config.py # Config validator
│   │   └── setup_{service}.py       # Setup wizard
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
│
├── {service}-connect/       # Tier 2: Meta-skill (user entry point)
│   └── SKILL.md             # Routes to appropriate operations
│
└── {service}-{operation}/   # Tier 3: Specialized skills (one per API operation)
    ├── SKILL.md
    └── scripts/
        └── {operation}.py
```

---

## Tier 1: Master Skill

**Purpose**: Shared resource library - NEVER loaded directly by users.

**Contains**:
- **API Client**: Handles authentication, token management, HTTP requests
- **Config Check**: Validates .env variables, returns actionable JSON for AI
- **Setup Wizard**: Interactive credential setup
- **References**: Setup guide, API docs, error handling, auth documentation

**Why it exists**: Eliminates duplication. Instead of each skill containing setup instructions and error handling, they all reference the master.

---

## Tier 2: Connect Skill

**Purpose**: User-facing entry point that routes to appropriate operations.

**Responsibilities**:
1. **Pre-flight check**: Always run config check first
2. **Smart routing**: Match user phrases to operations
3. **Context caching**: Remember discovered resources (agents, contacts, etc.)
4. **Error handling**: Load appropriate reference docs on failure

**Workflow pattern**:
```
Workflow 0: Config Check (Auto - ALWAYS FIRST)
Workflow 1: List {resources}
Workflow 2: Get {resource}
Workflow 3: Create {resource}
Workflow 4: Update {resource}
...
```

---

## Tier 3: Specialized Skills

**Purpose**: One skill per API operation with focused documentation.

**Contains**:
- **SKILL.md**: Prerequisites, usage (CLI + Python), API reference, error handling
- **Script**: Python implementation with argparse CLI and importable function

**Pattern**:
```python
def operation_name(param1, param2) -> dict:
    """Docstring with args and returns"""
    client = get_client()
    return client.get("/endpoint", params={...})

def main():
    parser = argparse.ArgumentParser()
    # Add arguments
    args = parser.parse_args()
    result = operation_name(args.param1, args.param2)
    print(json.dumps(result, indent=2))
```

---

## Why This Pattern?

### DRY Principle
- Setup instructions appear once (in master)
- Auth logic lives in one client
- Error handling documented once

### Progressive Disclosure
- User asks "list contacts" → loads only `{service}-list-contacts`
- That skill references master only when needed (errors, setup)
- Full API docs available but not loaded unless requested

### Maintainability
- Update auth flow? Change one file
- New endpoint? Add one skill, don't touch others
- Bug in client? Fix once, all skills benefit

### AI-Friendly
- Config check returns structured JSON with `ai_action` field
- AI knows exactly what to do: `proceed`, `prompt_for_key`, `run_setup`
- No ambiguity in error handling

---

## Config Check Pattern

Every operation starts with config validation:

```bash
uv run python {service}-master/scripts/check_{service}_config.py --json
```

Returns:
```json
{
  "status": "configured" | "not_configured",
  "ai_action": "proceed_with_operation" | "prompt_for_api_key" | "run_setup_wizard",
  "missing": [...],
  "fix_instructions": [...]
}
```

AI behavior based on `ai_action`:
- `proceed_with_operation`: Continue with the original request
- `prompt_for_api_key`: Ask user for credentials, save to .env
- `run_setup_wizard`: Execute interactive setup script

---

## Example: Beam Integration

```
00-system/skills/beam/
├── beam-master/                    # Shared resources
│   ├── scripts/
│   │   ├── beam_client.py         # Token exchange, requests
│   │   ├── check_beam_config.py   # Validates BEAM_API_KEY, BEAM_WORKSPACE_ID
│   │   ├── setup_beam.py          # Interactive setup
│   │   └── [20+ API scripts]
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md       # 22 endpoints documented
│       ├── error-handling.md
│       └── authentication.md      # Token refresh flow
│
├── beam-connect/                   # User entry point
│   └── SKILL.md                   # 7 workflows, smart routing
│
├── beam-list-agents/              # GET /agent
├── beam-get-agent-graph/          # GET /agent-graphs/{id}
├── beam-create-agent-task/        # POST /agent-tasks
├── beam-get-agent-analytics/      # GET /agent-tasks/analytics
├── beam-test-graph-node/          # POST /agent-graphs/test-node
├── beam-update-graph-node/        # PATCH /agent-graphs/update-node
├── beam-debug-issue-tasks/        # Debug via Langfuse
└── beam-get-nodes-by-tool/        # GET nodes by tool name
```

---

## Creating New Integrations

Use the `add-integration` skill to:

1. **Plan**: Discover API endpoints via web search
2. **Select**: Choose which endpoints to implement
3. **Generate**: Scaffold the complete structure

The scaffolding script (`scaffold_integration.py`) creates all files from templates, ensuring consistency with the established pattern.

---

**Version**: 1.0
**Pattern established**: Based on Beam integration (December 2025)
