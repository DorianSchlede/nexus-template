# Audit: add-integration

**Date**: 2026-01-07
**Auditor**: Claude (subagent)
**Skill Location**: `00-system/skills/system/add-integration/`

## Executive Summary

**VERDICT: NOT PRODUCTION READY** - This skill is a well-designed PLANNING tool but has a critical gap: **it produces NO executable scaffolding output**. The skill creates project planning documents but the `scaffold_integration.py` script is never called during the skill workflow. Users end up with a project full of plans but zero implementation.

**Critical Issues**:
1. Planning phase creates project, but scaffold script is never executed
2. Templates exist but aren't used during the skill workflow
3. User must manually run scaffold_integration.py (not documented clearly)
4. Missing setup wizard template (setup-wizard.py.template does not exist)

---

## 1. SKILL.md Analysis

### Defined Workflow (8 Steps)

1. **Initialize TodoList** - Track workflow progress
2. **Interactive Service Selection** - Ask user which service to integrate
3. **Web Search for API Documentation** - Use WebSearch + WebFetch to discover endpoints
4. **Create Integration Project** - Load create-project skill, create project structure
5. **Parse and Present Endpoints** - Categorize and display discovered endpoints
6. **User Selects Endpoints** - User chooses which endpoints to implement
7. **Gather Authentication Details & Finalize Project** - Confirm auth setup, write config files
8. **Prompt Close Session & Start Project** - Tell user to close session and return

### What It Claims to Produce

**During Planning Phase (add-integration skill)**:
- Integration project in `02-projects/{id}-{service}-integration/`
- `overview.md` - Project metadata
- `plan.md` - Approach (from create-project template)
- `steps.md` - Implementation checklist
- `integration-config.json` - Full configuration with selected endpoints
- `discovered-endpoints.json` - Raw endpoint discovery data

**During Implementation Phase (execute-project)**:
- Claims scaffold_integration.py will generate:
  - `{service}-master/` skill with API client, config check, setup wizard, references
  - `{service}-connect/` meta-skill
  - `{service}-{operation}/` skills (one per endpoint)

### External Dependencies

- **WebSearch** - Find API documentation (Steps 3)
- **WebFetch** - Parse API docs content (Step 3)
- **create-project** - Create project structure (Step 4, MANDATORY via nexus-loader)
- **execute-project** - Run scaffolding script (mentioned but not enforced)

### Execution Time Estimate

- **Claimed**: 15-25 minutes (planning phase only)
- **Actual**: Planning works as described, but leaves user with incomplete deliverable

---

## 2. Templates Analysis

| Template | Path | Placeholders | Complete? | Purpose |
|----------|------|--------------|-----------|---------|
| master-skill.md | templates/master-skill.md.template | SERVICE_NAME, SERVICE_SLUG, BASE_URL, ENV_KEY, ENV_VARS, SKILL_LIST, SCRIPT_LIST, AUTH_DESCRIPTION, CREATED_DATE | YES | SKILL.md for master skill |
| connect-skill.md | templates/connect-skill.md.template | SERVICE_NAME, SERVICE_SLUG, TRIGGER_PHRASES, PURPOSE_LIST, TRIGGER_LIST, CREDENTIAL_INSTRUCTIONS, ENV_VARS, WORKFLOWS, ROUTING_TABLE, SKILL_HANDOFF_TABLE, EXAMPLE_INTERACTIONS, CREATED_DATE | YES | SKILL.md for connect meta-skill |
| operation-skill.md | templates/operation-skill.md.template | SERVICE_NAME, SERVICE_SLUG, OPERATION_NAME, OPERATION_SLUG, OPERATION_DESCRIPTION, TRIGGER_PHRASES, ENV_VARS, ENV_KEY, CLI_EXAMPLES, FUNCTION_NAME, PYTHON_EXAMPLES, API_DOCS_URL, HTTP_METHOD, BASE_URL, ENDPOINT_PATH, AUTH_HEADER, PARAMETERS_SECTION, SUCCESS_CODE, RESPONSE_EXAMPLE, CREATED_DATE | YES | SKILL.md for operation skills |
| api-client.py | templates/api-client.py.template | SERVICE_NAME, SERVICE_SLUG, CLIENT_CLASS_NAME, BASE_URL, ENV_KEY, AUTH_METHODS, GET_HEADERS_BODY, ADDITIONAL_IMPORTS, ADDITIONAL_INIT_VARS, ADDITIONAL_CONFIG_LOADING, ADDITIONAL_VALIDATION | YES | Python API client |
| config-check.py | templates/config-check.py.template | SERVICE_NAME, SERVICE_SLUG, ENV_KEY, ENV_TEMPLATE, REQUIRED_VARS_CHECK, ADDITIONAL_MISSING_CHECKS, API_KEY_URL, CONNECTION_TEST_CODE | YES | Configuration validator with --json flag |
| setup-wizard.py | templates/setup-wizard.py.template | SERVICE_NAME, SERVICE_SLUG, ENV_KEY, API_KEY_INSTRUCTIONS, CONNECTION_TEST_CODE, ADDITIONAL_SETUP_STEPS, ADDITIONAL_TEST_PARAMS, ADDITIONAL_TEST_ARGS, ADDITIONAL_SAVE_VARS, FINAL_STEP_NUM, USAGE_EXAMPLES | YES | Interactive setup wizard |
| operation-script.py | templates/operation-script.py.template | SERVICE_NAME, SERVICE_SLUG, OPERATION_NAME, OPERATION_SLUG, OPERATION_DESCRIPTION, FUNCTION_NAME, FUNCTION_PARAMS, FUNCTION_DOCSTRING, ARGS_DOCSTRING, RETURNS_DOCSTRING, FUNCTION_BODY, CLI_ARGS, CLI_EXAMPLES, ENV_VARS_HELP, ARGPARSE_ARGS, FUNCTION_CALL_ARGS | YES | Python script for API operations |
| setup-guide.md | templates/references/setup-guide.md.template | SERVICE_NAME, SERVICE_SLUG, ENV_KEY, ENV_TEMPLATE, API_KEY_INSTRUCTIONS, ADDITIONAL_TROUBLESHOOTING, CREATED_DATE | YES | Setup documentation |
| api-reference.md | templates/references/api-reference.md.template | SERVICE_NAME, BASE_URL, AUTH_DOCUMENTATION, ENDPOINTS_DOCUMENTATION, RATE_LIMIT_INFO, PAGINATION_INFO, API_DOCS_URL, ADDITIONAL_DOCS_LINKS, CREATED_DATE | YES | API endpoint documentation |
| error-handling.md | templates/references/error-handling.md.template | SERVICE_NAME, SERVICE_SLUG, ENV_KEY, BASE_URL, AUTH_HEADER, COMMON_ISSUES, API_DOCS_URL, CREATED_DATE | YES | Error troubleshooting guide |
| authentication.md | templates/references/authentication.md.template | SERVICE_NAME, SERVICE_SLUG, AUTH_TYPE, AUTH_TYPE_DESCRIPTION, ENV_TEMPLATE, HEADERS_DOCUMENTATION, AUTH_FLOW_DOCUMENTATION, TOKEN_MANAGEMENT, TOKEN_EXPIRED_HANDLING, CREATED_DATE | YES | Authentication documentation |

**Total Templates**: 11 (all complete and well-designed)

**Template Quality**: EXCELLENT - Templates match production patterns, include all necessary placeholders, and follow the master/connect/specialized architecture.

---

## 3. Scripts Analysis

### scaffold_integration.py

**Lines of Code**: 859
**Location**: `scripts/scaffold_integration.py`

**Functions**:
1. `slugify(text)` - Convert to slug format
2. `pascal_case(text)` - Convert to PascalCase
3. `load_template(name)` - Load template file
4. `render_template(content, vars)` - Replace {{placeholders}}
5. `generate_auth_methods(auth_type, slug)` - Generate OAuth2/Bearer/API key auth code
6. `generate_get_headers(auth_type)` - Generate header construction code
7. `create_master_skill(config, output_dir)` - Generate master skill directory
8. `create_api_client(config, scripts_dir)` - Generate API client script
9. `create_config_check(config, scripts_dir)` - Generate config checker
10. `create_setup_wizard(config, scripts_dir)` - Generate setup wizard
11. `create_references(config, refs_dir)` - Generate 4 reference docs
12. `create_connect_skill(config, output_dir)` - Generate connect meta-skill
13. `create_operation_skill(config, endpoint, output_dir)` - Generate operation skill
14. `create_operation_script(config, endpoint, scripts_dir)` - Generate operation Python script
15. `scaffold_integration(config)` - Main orchestration function
16. `main()` - CLI entry point with argparse

**What It Generates**:
```
00-system/skills/{service_slug}/
├── {service_slug}-master/
│   ├── SKILL.md
│   ├── scripts/
│   │   ├── {service_slug}_client.py
│   │   ├── check_{service_slug}_config.py
│   │   └── setup_{service_slug}.py
│   └── references/
│       ├── setup-guide.md
│       ├── api-reference.md
│       ├── error-handling.md
│       └── authentication.md
├── {service_slug}-connect/
│   └── SKILL.md
└── {service_slug}-{operation_slug}/  [one per endpoint]
    ├── SKILL.md
    └── scripts/
        └── {operation_slug}.py
```

**Auth Types Supported**:
- `oauth2` - OAuth 2.0 client credentials flow with token refresh
- `bearer` - Bearer token authentication (API key as token)
- `api_key` - API key in header (X-API-Key)

**Config JSON Schema**:
```json
{
  "service_name": "string",          // e.g., "HubSpot"
  "service_slug": "string",          // e.g., "hubspot"
  "base_url": "string",              // e.g., "https://api.hubapi.com"
  "auth_type": "oauth2|api_key|bearer",
  "env_key": "string",               // e.g., "HUBSPOT_API_KEY"
  "api_docs_url": "string",
  "endpoints": [
    {
      "name": "string",              // e.g., "List Contacts"
      "slug": "string",              // e.g., "list-contacts"
      "method": "GET|POST|PATCH|DELETE",
      "path": "string",              // e.g., "/contacts"
      "description": "string",
      "triggers": ["string"],        // User phrases
      "parameters": [                // Optional
        {
          "name": "string",
          "type": "string",
          "description": "string",
          "required": boolean,
          "default": "any"
        }
      ]
    }
  ],
  "status": "planning|ready",
  "created": "timestamp",
  "created_by": "string"
}
```

**Is It Tested/Reliable?**
- NO automated tests found
- Script appears well-structured and comprehensive
- Uses simple string replacement (not Jinja2) - reliable but basic
- Path construction uses `pathlib` - cross-platform safe
- Error handling minimal (will crash on missing templates)

---

## 4. References Analysis

**Location**: `references/`

| File | Purpose | Size | Quality |
|------|---------|------|---------|
| integration-architecture.md | Documents the 3-tier pattern (master/connect/specialized) | 6.0 KB | EXCELLENT - Clear explanation of why this pattern exists |
| integration-ideas.md | Use cases and integration suggestions | 13.7 KB | GOOD - Provides context and examples |
| mcp-guide.md | Model Context Protocol guide | 11.7 KB | GOOD - MCP-specific integration patterns |
| mcp-introduction.md | What MCP is and how it works | 8.1 KB | GOOD - Background for MCP approach |
| mcp-setup-guide.md | Manual MCP server setup | 13.5 KB | GOOD - Alternative to REST API approach |
| troubleshooting-guide.md | Common integration issues | 15.7 KB | GOOD - Comprehensive troubleshooting |

**Total Reference Files**: 6

**Architecture Documentation**: YES - `integration-architecture.md` clearly explains the pattern and shows Beam integration as example (though Beam doesn't exist in the codebase anymore).

**MCP Guides**: YES - 3 files dedicated to MCP approach (alternative to REST integrations).

**Troubleshooting**: YES - Comprehensive error handling guide.

---

## 5. Gap Analysis

| Feature | Claimed in SKILL.md | Actually Implemented | Gap |
|---------|-------------------|---------------------|-----|
| Web search for API docs | YES (Step 3) | YES - Workflow includes WebSearch | NONE |
| User endpoint selection | YES (Steps 5-6) | YES - Interactive selection | NONE |
| Create project structure | YES (Step 4) | YES - Via create-project skill | NONE |
| Save integration-config.json | YES (Step 7) | YES - Written to 02-resources/ | NONE |
| Generate steps.md | YES (Step 7) | YES - Implementation checklist | NONE |
| **Execute scaffold script** | **MENTIONED (Step 8 notes)** | **NO - Never called during skill** | **CRITICAL** |
| Generate master skill | Implied via scaffold | NO - Script exists but not run | CRITICAL |
| Generate connect skill | Implied via scaffold | NO - Script exists but not run | CRITICAL |
| Generate operation skills | Implied via scaffold | NO - Script exists but not run | CRITICAL |
| Setup wizard creation | YES - Via templates | NO - Template doesn't exist | **MISSING TEMPLATE** |

### Critical Finding

**THE DISCONNECT**: The skill creates a beautiful project with `integration-config.json` containing all the data needed to scaffold, BUT:

1. Step 8 says "When the user returns and says 'work on {service} integration', the execute-project skill will run scaffold_integration.py"
2. But there's NO evidence that execute-project knows about scaffold_integration.py
3. No project template includes the scaffold command
4. User is left with plans but NO actual skills

**What's Missing**:
- The `steps.md` should include: "Run scaffold_integration.py with integration-config.json"
- OR execute-project should auto-detect integration projects and run the scaffold
- OR the skill should run the scaffold immediately after finalization

---

## 6. Production Comparison

### Real Langfuse Integration (Production)

**Structure**:
```
03-skills/langfuse/
├── langfuse-master/
│   ├── SKILL.md (80 lines)
│   └── scripts/
│       ├── langfuse_client.py (100 lines)
│       └── check_langfuse_config.py (118 lines)
├── langfuse-connect/
│   └── SKILL.md
└── langfuse-{operation}/ (70 skills total)
    ├── SKILL.md (31 lines average)
    └── scripts/
        └── {operation}.py (45 lines average)
```

**Total Skills**: 70 operation skills + 1 connect + 1 master = **72 skills**

**Master Scripts**: 2 (client + config check) - NO setup wizard

### What scaffold_integration.py Would Generate

**Structure**:
```
00-system/skills/{service}/
├── {service}-master/
│   ├── SKILL.md (130 lines from template)
│   └── scripts/
│       ├── {service}_client.py (124 lines)
│       ├── check_{service}_config.py (164 lines)
│       └── setup_{service}.py (153 lines)
│   └── references/ (4 files)
└── {service}-connect/
    └── SKILL.md (127 lines)
└── {service}-{operation}/ (N skills based on config)
    ├── SKILL.md (74 lines)
    └── scripts/
        └── {operation}.py (85 lines)
```

**Master Scripts**: 3 (client + config check + setup wizard)

### Gap Analysis

| Component | Real Langfuse | Scaffold Output | Gap |
|-----------|--------------|----------------|-----|
| Master SKILL.md | Minimal (80 lines) | Rich (130 lines) | Scaffold is MORE complete |
| API client | Basic, custom | Generated, multi-auth | Scaffold is MORE capable |
| Config check | Basic | JSON output with ai_action | Scaffold is BETTER |
| Setup wizard | MISSING | Generated | Scaffold ADDS value |
| References | MISSING | 4 comprehensive guides | Scaffold ADDS value |
| Connect skill | Minimal routing | Full routing table | Scaffold is MORE complete |
| Operation skills | Hand-written, minimal | Generated, complete | **Equivalent quality** |

### Key Finding

**The templates are SUPERIOR to production**. Langfuse integration was hand-written with minimal documentation. The scaffold would generate MORE complete skills with better documentation and tooling (setup wizard, references, etc.).

**BUT**: The scaffold is never run, so users get NOTHING.

---

## 7. Template Quality Assessment

| Template | Generic? | Production Quality? | Issues |
|----------|----------|-------------------|--------|
| master-skill.md | YES | EXCELLENT | Includes progressive disclosure, ai_action handling, comprehensive references |
| connect-skill.md | YES | EXCELLENT | Smart routing, pre-flight checks, example interactions |
| operation-skill.md | YES | GOOD | Clean, focused, API reference included |
| api-client.py | YES | EXCELLENT | Multi-auth support, token management, error handling |
| config-check.py | YES | EXCELLENT | JSON output for AI, actionable errors, --test flag |
| setup-wizard.py | YES | EXCELLENT | Interactive, tests connection, preserves .env |
| operation-script.py | YES | EXCELLENT | Argparse CLI, importable function, proper error handling |
| setup-guide.md | YES | GOOD | Clear steps, troubleshooting, security notes |
| api-reference.md | YES | GOOD | Structured endpoint docs, response codes, pagination |
| error-handling.md | YES | GOOD | HTTP errors, config errors, debugging tips |
| authentication.md | YES | GOOD | Auth type explanation, best practices, troubleshooting |

**Overall Quality**: 9/10 - Templates are production-ready and follow best practices.

**Customization Required**: LOW - Templates use placeholders intelligently. Only endpoint-specific details need customization (happens automatically via config).

**Missing from Production**: References, setup wizard, comprehensive error handling - all valuable additions.

---

## 8. Verdict

### Is this skill production-ready?

**NO**

### Why not?

1. **Critical Gap**: The skill produces planning documents but never executes the scaffold script
2. **Broken Promise**: User expects implementation, gets only plans
3. **Missing Link**: No clear path from project to actual skills
4. **Orphaned Templates**: Beautiful templates that never get used

### What would make it production-ready?

**Minimum Viable Fix (2 hours)**:
1. Add to `steps.md` generation (Step 7):
   ```markdown
   ## Phase 1: Generate Skills
   - [ ] Run scaffold: `python 00-system/skills/system/add-integration/scripts/scaffold_integration.py --config 02-resources/integration-config.json`
   ```
2. Update Step 8 message to include manual scaffold command
3. Test with real API (Stripe, HubSpot, etc.)

**Proper Solution (1 day)**:
1. Modify execute-project to detect integration projects (check for integration-config.json)
2. Auto-run scaffold_integration.py when project status changes to IN_PROGRESS
3. Add validation that skills were created successfully
4. Update steps.md to mark scaffold as completed
5. Add error handling for scaffold failures

**Complete Solution (2-3 days)**:
1. All of the above
2. Add `--dry-run` flag to scaffold to preview output
3. Create automated tests for scaffold_integration.py
4. Add post-scaffold validation (check that skills load, scripts are executable)
5. Create example integration (Stripe or Notion) as reference
6. Add interactive mode: scaffold then immediately test one endpoint
7. Generate README.md in integration folder with quickstart

---

## 9. Recommendations

### Priority 1: Critical (Fix Immediately)

1. **Bridge the gap** - Add scaffold execution to the workflow:
   - Option A: Auto-execute after project finalization (in add-integration skill)
   - Option B: Include explicit command in steps.md + final message
   - Option C: Modify execute-project to detect and run scaffold

2. **Test end-to-end** - Actually run the full workflow:
   - Pick a real API (Stripe recommended - well documented, free tier)
   - Run add-integration skill
   - Execute scaffold manually
   - Test generated skills
   - Document gaps

### Priority 2: High (Complete Before Next Use)

3. **Verify templates** - Ensure all referenced templates exist:
   - ✓ All Python templates exist
   - ✓ All Markdown templates exist
   - Template references in scaffold.py match filesystem

4. **Add validation** - Scaffold should validate output:
   - Check SKILL.md syntax
   - Verify Python scripts are valid syntax
   - Test that generated skills load in nexus-loader

5. **Error recovery** - Handle scaffold failures gracefully:
   - If scaffold fails, don't leave partial output
   - Provide clear error messages
   - Allow re-running scaffold after fixing config

### Priority 3: Medium (Improve Quality)

6. **Enhance templates** - Based on production integrations:
   - Add rate limiting to api-client.py
   - Add retry logic with exponential backoff
   - Include logging/debug mode toggle

7. **Add examples** - Create reference implementation:
   - Full Stripe integration (payments API)
   - Include in references/ as example
   - Document any manual customization needed

8. **Improve documentation**:
   - Add "What gets generated" section to SKILL.md with full file tree
   - Include before/after screenshots
   - Document customization points

### Priority 4: Low (Nice to Have)

9. **Interactive enhancement**:
   - After scaffold, offer to test one endpoint immediately
   - Generate example .env with placeholder values
   - Create test scripts for each operation

10. **Maintenance tooling**:
    - Update script to sync existing integration with new template versions
    - Diff tool to compare generated vs hand-modified skills
    - Validate script to check integration health

---

## 10. Reusable Components

### For `create-master-skill`

**Highly Reusable**:
1. **Template System** - The `load_template()` + `render_template()` pattern is clean and simple
2. **Auth Generation** - `generate_auth_methods()` and `generate_get_headers()` support 3 auth types
3. **Master Skill Template** - `master-skill.md.template` is excellent for any shared resource library
4. **Config Check Template** - `config-check.py.template` with JSON output and ai_action is brilliant
5. **Setup Wizard Template** - `setup-wizard.py.template` for interactive credential setup

**Copy Verbatim**:
- `templates/api-client.py.template` - Generic API client
- `templates/config-check.py.template` - Config validator
- `templates/setup-wizard.py.template` - Setup wizard
- `templates/references/*.template` - All 4 reference doc templates

**Adapt for Master Skills**:
- The `create_master_skill()` function - structure is perfect for non-integration master skills
- The references pattern (setup-guide, api-reference, error-handling, authentication)
- The DRY principle of extracting shared content

**Patterns to Copy**:
1. **Progressive Disclosure** - Master has all docs, operation skills reference them
2. **AI-Friendly Errors** - JSON output with `ai_action` field tells AI exactly what to do
3. **Setup Wizard Pattern** - Interactive, tests connection, saves to .env
4. **Skill Architecture** - master (shared) + connect (router) + specialized (focused) is brilliant

**NOT Reusable for create-master-skill**:
- Integration-specific patterns (endpoints, API operations)
- The connect skill concept (only applies to multi-skill integrations)
- Web search for documentation (only applies to external APIs)

### Concrete Recommendations for create-master-skill

When building `create-master-skill`, **steal these verbatim**:

1. **Template rendering system**:
   ```python
   def load_template(name): ...
   def render_template(content, vars): ...
   ```

2. **Config check pattern**:
   - Use `config-check.py.template` as-is
   - Adapt REQUIRED_VARS_CHECK for different env vars
   - Keep JSON output with ai_action field

3. **Master SKILL.md structure**:
   ```markdown
   # {Name} Master
   **DO NOT LOAD DIRECTLY** - Shared resource library

   ## Purpose
   Provides shared resources to eliminate duplication...

   ## Shared Resources
   ### references/
   - setup-guide.md
   - usage-guide.md
   - error-handling.md

   ### scripts/
   - check_config.py
   - helper_functions.py
   ```

4. **Reference docs template structure**:
   - setup-guide.md (how to configure)
   - error-handling.md (troubleshooting)
   - {domain}-guide.md (domain-specific content)

5. **The entire philosophy**:
   - Extract duplication into master
   - Progressive disclosure via references
   - AI-friendly error handling
   - Shared scripts imported by specialized skills

---

## Appendix A: File Inventory

### Templates (11 total)
```
templates/
├── master-skill.md.template            (130 lines)
├── connect-skill.md.template           (127 lines)
├── operation-skill.md.template         (74 lines)
├── api-client.py.template              (124 lines)
├── config-check.py.template            (164 lines)
├── setup-wizard.py.template            (153 lines)
├── operation-script.py.template        (85 lines)
└── references/
    ├── setup-guide.md.template         (95 lines)
    ├── api-reference.md.template       (60 lines)
    ├── error-handling.md.template      (123 lines)
    └── authentication.md.template      (81 lines)
```

### Scripts (1 total)
```
scripts/
└── scaffold_integration.py             (859 lines)
```

### References (6 total)
```
references/
├── integration-architecture.md         (191 lines)
├── integration-ideas.md                (13.7 KB)
├── mcp-guide.md                        (11.7 KB)
├── mcp-introduction.md                 (8.1 KB)
├── mcp-setup-guide.md                  (13.5 KB)
└── troubleshooting-guide.md            (15.7 KB)
```

### Main Skill File
```
SKILL.md                                (622 lines)
```

**Total Files**: 19
**Total Lines of Code**: ~2,500 (Python) + ~1,500 (Markdown templates) + ~15,000 (Markdown docs)

---

## Appendix B: Comparison with Real Integration

### Langfuse Integration Stats

**Location**: `03-skills/langfuse/`

**Structure**:
- 1 master skill (langfuse-master)
- 1 connect skill (langfuse-connect)
- 70 operation skills (langfuse-{operation})
- 72 total skills

**Master Skill Components**:
- SKILL.md (80 lines) - Minimal, just lists scripts
- langfuse_client.py (100 lines) - Basic auth client
- check_langfuse_config.py (118 lines) - Basic config check
- NO setup wizard
- NO reference docs
- NO error handling guide

**Operation Skill Pattern**:
- SKILL.md (31 lines avg) - Name, description, usage
- {operation}.py (45 lines avg) - Script with CLI

**Hand-Written Quality**: FUNCTIONAL but MINIMAL
- Gets the job done
- Lacks comprehensive docs
- No setup wizard (user must manually create .env)
- No references for troubleshooting

### What Scaffold Would Have Generated

**Same 72 skills, but with**:
- Master SKILL.md (130 lines) - Comprehensive, explains pattern
- API client (124 lines) - Multi-auth, token management
- Config check (164 lines) - JSON output with ai_action
- **Setup wizard (153 lines)** - NEW, interactive setup
- **4 reference docs** - NEW, comprehensive guides
- Operation SKILLs (74 lines) - More detailed, API reference included

**Value Add of Scaffold**:
- +153 lines: Interactive setup wizard (saves manual .env editing)
- +416 lines: Reference documentation (setup, API, errors, auth)
- +2,160 lines: Richer SKILL.md files (74 vs 31 lines × 70 skills)
- TOTAL: ~2,700 lines of high-value documentation and tooling

### Conclusion

**The scaffold templates are objectively better** than production integrations, but they're never used because the workflow doesn't execute them.

---

## Appendix C: Proposed Fix

### Minimal Fix (Add to SKILL.md Step 7)

After finalizing `integration-config.json`, add this to the displayed message:

```markdown
Project Finalized!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 02-projects/{id}-{service_slug}-integration/

NEXT: Generate the integration skills

Run this command:
```bash
python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
  --config 02-projects/{id}-{service_slug}-integration/02-resources/integration-config.json
```

This will create:
• {service_slug}-master/ (shared resources)
• {service_slug}-connect/ (meta-skill)
• {count} operation skills

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Better Fix (Auto-execute after finalization)

Add to Step 7, after writing integration-config.json:

```python
# Display confirmation
display("""
Project Finalized!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Now generating integration skills...
""")

# Run scaffold
run(f"""python 00-system/skills/system/add-integration/scripts/scaffold_integration.py \
  --config 02-projects/{project_id}-{service_slug}-integration/02-resources/integration-config.json""")

display("""
Integration skills generated successfully!

Created:
• 00-system/skills/{service_slug}/{service_slug}-master/
• 00-system/skills/{service_slug}/{service_slug}-connect/
• {count} operation skills

You can now use: "connect to {service_slug}"
""")
```

### Best Fix (Integrate with execute-project)

Modify execute-project skill to detect integration projects and auto-scaffold:

```python
# In execute-project skill, after loading project

# Check if this is an integration project
config_path = project_path / "02-resources" / "integration-config.json"
if config_path.exists():
    display("This is an integration project. Checking if skills exist...")

    config = json.load(config_path)
    service_slug = config['service_slug']

    # Check if already scaffolded
    master_path = Path(f"00-system/skills/{service_slug}/{service_slug}-master")

    if not master_path.exists():
        display(f"Skills not generated yet. Running scaffold...")
        run(f"python 00-system/skills/system/add-integration/scripts/scaffold_integration.py --config {config_path}")
        display("Skills generated!")
    else:
        display("Skills already exist. Skipping scaffold.")

    # Continue with normal project execution
```

This makes integration projects "just work" - user creates project, returns later, execute-project auto-scaffolds if needed.

---

**End of Audit**
