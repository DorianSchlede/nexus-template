#!/usr/bin/env python3
"""
Integration Scaffolding Script

Generates the complete integration skill structure from templates.
Used during build execution phase (not during add-integration skill planning).

Usage:
    python scaffold_integration.py --config integration_config.json
    python scaffold_integration.py --service hubspot --base-url https://api.hubapi.com --auth-type oauth2

Config JSON format:
{
    "service_name": "HubSpot",
    "service_slug": "hubspot",
    "base_url": "https://api.hubapi.com",
    "auth_type": "oauth2",  // oauth2, api_key, bearer
    "env_key": "HUBSPOT_API_KEY",
    "api_docs_url": "https://developers.hubspot.com/docs/api",
    "endpoints": [
        {
            "name": "List Contacts",
            "slug": "list-contacts",
            "method": "GET",
            "path": "/crm/v3/objects/contacts",
            "description": "Retrieve all contacts from HubSpot",
            "triggers": ["list contacts", "get contacts", "show contacts"]
        }
    ]
}
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from string import Template

SCRIPT_DIR = Path(__file__).parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
SKILLS_DIR = PROJECT_ROOT / "00-system" / "skills"


def slugify(text: str) -> str:
    """Convert text to slug format"""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def pascal_case(text: str) -> str:
    """Convert text to PascalCase"""
    words = re.split(r'[-_\s]+', text)
    return ''.join(word.capitalize() for word in words)


def load_template(template_name: str) -> str:
    """Load a template file"""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")
    return template_path.read_text(encoding='utf-8')


def render_template(template_content: str, variables: dict) -> str:
    """Render a template with variables using {{var}} syntax"""
    result = template_content
    for key, value in variables.items():
        result = result.replace(f"{{{{{key}}}}}", str(value))
    return result


def generate_auth_methods(auth_type: str, service_slug: str) -> str:
    """Generate authentication methods based on auth type"""
    if auth_type == "oauth2":
        return f'''
    def _authenticate(self):
        """Get access token via OAuth2"""
        import requests

        response = requests.post(
            f"{{BASE_URL}}/oauth/v1/token",
            data={{
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }},
            timeout=30
        )

        if response.status_code not in [200, 201]:
            raise Exception(f"Authentication failed: {{response.status_code}} - {{response.text}}")

        tokens = response.json()
        self.access_token = tokens.get('access_token')
        self.token_expiry = time.time() + tokens.get('expires_in', 3600) - 60

    def _ensure_token(self):
        """Ensure we have a valid access token"""
        if not self.access_token or time.time() > self.token_expiry:
            self._authenticate()
'''
    elif auth_type == "bearer":
        return '''
    def _authenticate(self):
        """Use API key as bearer token"""
        self.access_token = self.api_key

    def _ensure_token(self):
        """API key doesn't expire"""
        if not self.access_token:
            self._authenticate()
'''
    else:  # api_key
        return '''
    def _authenticate(self):
        """API key auth doesn't need token exchange"""
        pass

    def _ensure_token(self):
        """API key doesn't expire"""
        pass
'''


def generate_get_headers(auth_type: str) -> str:
    """Generate get_headers method based on auth type"""
    if auth_type == "oauth2":
        return '''self._ensure_token()
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }'''
    elif auth_type == "bearer":
        return '''return {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }'''
    else:  # api_key
        return '''return {
            'X-API-Key': self.api_key,
            'Content-Type': 'application/json'
        }'''


def create_master_skill(config: dict, output_dir: Path):
    """Create the master skill directory and files"""
    master_dir = output_dir / f"{config['service_slug']}-master"
    master_dir.mkdir(parents=True, exist_ok=True)
    (master_dir / "scripts").mkdir(exist_ok=True)
    (master_dir / "references").mkdir(exist_ok=True)

    # Generate skill list for SKILL.md
    skill_list = "\n".join([
        f"- `{config['service_slug']}-{ep['slug']}` - {ep['name']}"
        for ep in config['endpoints']
    ])

    # Generate script list
    script_list = "\n".join([
        f"**[{ep['slug']}.py](scripts/{ep['slug']}.py)** - {ep['name']}\n- {ep['method']} {ep['path']}"
        for ep in config['endpoints']
    ])

    # Generate env vars
    env_vars = f"{config['env_key']}=your_api_key_here"
    if config.get('additional_env_vars'):
        env_vars += "\n" + "\n".join(config['additional_env_vars'])

    # Auth description
    auth_desc = {
        'oauth2': '- OAuth 2.0 client credentials flow\n- Automatic token refresh',
        'bearer': '- Bearer token authentication\n- API key used directly as token',
        'api_key': '- API key authentication\n- Key passed in header'
    }.get(config['auth_type'], '- API key authentication')

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'BASE_URL': config['base_url'],
        'ENV_KEY': config['env_key'],
        'ENV_VARS': env_vars,
        'SKILL_LIST': skill_list,
        'SCRIPT_LIST': script_list,
        'AUTH_DESCRIPTION': auth_desc,
        'CREATED_DATE': datetime.now().strftime('%Y-%m-%d')
    }

    # Create SKILL.md
    template = load_template("master-skill.md.template")
    content = render_template(template, variables)
    (master_dir / "SKILL.md").write_text(content, encoding='utf-8')

    # Create API client
    create_api_client(config, master_dir / "scripts")

    # Create config check script
    create_config_check(config, master_dir / "scripts")

    # Create setup wizard
    create_setup_wizard(config, master_dir / "scripts")

    # Create reference files
    create_references(config, master_dir / "references")

    print(f"  Created: {master_dir.relative_to(PROJECT_ROOT)}/")


def create_api_client(config: dict, scripts_dir: Path):
    """Create the API client script"""
    template = load_template("api-client.py.template")

    auth_methods = generate_auth_methods(config['auth_type'], config['service_slug'])
    get_headers = generate_get_headers(config['auth_type'])

    # Additional init vars for OAuth
    additional_init = ""
    additional_config = ""
    additional_validation = ""
    additional_imports = ""

    if config['auth_type'] == 'oauth2':
        additional_init = "self.client_id = None\n        self.client_secret = None"
        additional_config = f'''
        self.client_id = env_vars.get('{config["service_slug"].upper()}_CLIENT_ID') or os.getenv('{config["service_slug"].upper()}_CLIENT_ID')
        self.client_secret = env_vars.get('{config["service_slug"].upper()}_CLIENT_SECRET') or os.getenv('{config["service_slug"].upper()}_CLIENT_SECRET')'''
        additional_validation = f'''
        if not self.client_id:
            raise ValueError("{config['service_slug'].upper()}_CLIENT_ID not found in .env or environment")
        if not self.client_secret:
            raise ValueError("{config['service_slug'].upper()}_CLIENT_SECRET not found in .env or environment")'''

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'CLIENT_CLASS_NAME': f"{pascal_case(config['service_slug'])}Client",
        'BASE_URL': config['base_url'],
        'ENV_KEY': config['env_key'],
        'AUTH_METHODS': auth_methods,
        'GET_HEADERS_BODY': get_headers,
        'ADDITIONAL_IMPORTS': additional_imports,
        'ADDITIONAL_INIT_VARS': additional_init,
        'ADDITIONAL_CONFIG_LOADING': additional_config,
        'ADDITIONAL_VALIDATION': additional_validation
    }

    content = render_template(template, variables)
    (scripts_dir / f"{config['service_slug']}_client.py").write_text(content, encoding='utf-8')


def create_config_check(config: dict, scripts_dir: Path):
    """Create the config check script"""
    template = load_template("config-check.py.template")

    # Build required vars check
    required_vars = [f'        ("{config["env_key"]}", "API key for {config["service_name"]}"),']
    if config['auth_type'] == 'oauth2':
        required_vars.extend([
            f'        ("{config["service_slug"].upper()}_CLIENT_ID", "OAuth client ID"),',
            f'        ("{config["service_slug"].upper()}_CLIENT_SECRET", "OAuth client secret"),'
        ])

    # Additional missing checks
    additional_checks = ""
    if config['auth_type'] == 'oauth2':
        additional_checks = f'''
        if "{config['service_slug'].upper()}_CLIENT_ID" in missing_items:
            result["fix_instructions"].append(
                "Get your OAuth client ID from {config['service_name']} developer settings"
            )'''

    # Env template
    env_template = f"{config['env_key']}=your_api_key_here"
    if config['auth_type'] == 'oauth2':
        env_template += f"\n{config['service_slug'].upper()}_CLIENT_ID=your_client_id\n{config['service_slug'].upper()}_CLIENT_SECRET=your_client_secret"

    # Connection test code
    connection_test = f'''
        headers = {{"Authorization": f"Bearer {{api_key}}"}}
        response = requests.get(
            "{config['base_url']}/ping",  # Adjust endpoint
            headers=headers,
            timeout=10
        )
        return {{"success": response.status_code in [200, 401, 403]}}'''

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'ENV_KEY': config['env_key'],
        'ENV_TEMPLATE': env_template,
        'REQUIRED_VARS_CHECK': '\n'.join(required_vars),
        'ADDITIONAL_MISSING_CHECKS': additional_checks,
        'API_KEY_URL': config.get('api_key_url', f'{config["service_name"]} developer settings'),
        'CONNECTION_TEST_CODE': connection_test
    }

    content = render_template(template, variables)
    (scripts_dir / f"check_{config['service_slug']}_config.py").write_text(content, encoding='utf-8')


def create_setup_wizard(config: dict, scripts_dir: Path):
    """Create the setup wizard script"""
    template = load_template("setup-wizard.py.template")

    # API key instructions
    api_key_instructions = f'''print("1. Go to your {config['service_name']} dashboard")
    print("2. Navigate to Settings > API Keys (or Developer section)")
    print("3. Create a new API key")
    print("4. Copy the key")'''

    # Connection test code
    connection_test = f'''
        headers = {{"Authorization": f"Bearer {{api_key}}"}}
        response = requests.get(
            "{config['base_url']}/me",  # Adjust endpoint
            headers=headers,
            timeout=10
        )
        if response.status_code in [200, 201]:
            print("  Authenticated successfully!")
            return True
        else:
            print(f"  Error: {{response.status_code}} - {{response.text}}")
            return False'''

    # Additional setup for OAuth
    additional_steps = ""
    additional_params = ""
    additional_args = ""
    additional_save = ""
    final_step = "2"

    if config['auth_type'] == 'oauth2':
        final_step = "4"
        additional_steps = f'''
    # Get client ID
    print()
    print("Step 2: Get your OAuth Client ID")
    print("-" * 40)
    print("Find this in your {config['service_name']} developer settings")
    print()

    client_id = input("Paste your Client ID: ").strip()
    if not client_id:
        print("Error: Client ID is required")
        sys.exit(1)

    # Get client secret
    print()
    print("Step 3: Get your OAuth Client Secret")
    print("-" * 40)

    client_secret = input("Paste your Client Secret: ").strip()
    if not client_secret:
        print("Error: Client Secret is required")
        sys.exit(1)
'''
        additional_params = ", client_id=None, client_secret=None"
        additional_args = ", client_id, client_secret"
        additional_save = f'''            '{config["service_slug"].upper()}_CLIENT_ID': client_id,
            '{config["service_slug"].upper()}_CLIENT_SECRET': client_secret,'''

    # Usage examples
    usage_examples = "\n".join([
        f'        print("  - {ep["name"]}")'
        for ep in config['endpoints'][:3]
    ])

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'ENV_KEY': config['env_key'],
        'API_KEY_INSTRUCTIONS': api_key_instructions,
        'CONNECTION_TEST_CODE': connection_test,
        'ADDITIONAL_SETUP_STEPS': additional_steps,
        'ADDITIONAL_TEST_PARAMS': additional_params,
        'ADDITIONAL_TEST_ARGS': additional_args,
        'ADDITIONAL_SAVE_VARS': additional_save,
        'FINAL_STEP_NUM': final_step,
        'USAGE_EXAMPLES': usage_examples
    }

    content = render_template(template, variables)
    (scripts_dir / f"setup_{config['service_slug']}.py").write_text(content, encoding='utf-8')


def create_references(config: dict, refs_dir: Path):
    """Create reference documentation files"""
    created_date = datetime.now().strftime('%Y-%m-%d')

    # Setup guide
    template = load_template("references/setup-guide.md.template")
    env_template = f"{config['env_key']}=your_api_key_here"

    api_key_instructions = f'''1. Log into your {config['service_name']} account
2. Navigate to Settings or Developer section
3. Find API Keys or Authentication
4. Create a new API key
5. Copy the key immediately (you may not see it again)'''

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'ENV_KEY': config['env_key'],
        'ENV_TEMPLATE': env_template,
        'API_KEY_INSTRUCTIONS': api_key_instructions,
        'ADDITIONAL_TROUBLESHOOTING': '',
        'CREATED_DATE': created_date
    }
    content = render_template(template, variables)
    (refs_dir / "setup-guide.md").write_text(content, encoding='utf-8')

    # API reference
    template = load_template("references/api-reference.md.template")

    # Build endpoints documentation
    endpoints_doc = ""
    for ep in config['endpoints']:
        endpoints_doc += f'''
### {ep['name']}

**Endpoint**: `{ep['method']} {ep['path']}`

{ep.get('description', '')}

```bash
curl -X {ep['method']} "{config['base_url']}{ep['path']}" \\
  -H "Authorization: Bearer $API_KEY"
```

---
'''

    auth_doc = {
        'oauth2': 'OAuth 2.0 with client credentials. Token included in Authorization header.',
        'bearer': 'Bearer token authentication. API key used as bearer token.',
        'api_key': 'API key authentication. Key passed in request header.'
    }.get(config['auth_type'], 'API key authentication')

    variables = {
        'SERVICE_NAME': config['service_name'],
        'BASE_URL': config['base_url'],
        'AUTH_DOCUMENTATION': auth_doc,
        'ENDPOINTS_DOCUMENTATION': endpoints_doc,
        'RATE_LIMIT_INFO': 'Check official documentation for current rate limits.',
        'PAGINATION_INFO': 'Most list endpoints support pagination via offset/limit or cursor parameters.',
        'API_DOCS_URL': config.get('api_docs_url', f'https://developers.{config["service_slug"]}.com'),
        'ADDITIONAL_DOCS_LINKS': '',
        'CREATED_DATE': created_date
    }
    content = render_template(template, variables)
    (refs_dir / "api-reference.md").write_text(content, encoding='utf-8')

    # Error handling
    template = load_template("references/error-handling.md.template")
    auth_header = 'Bearer $TOKEN' if config['auth_type'] in ['oauth2', 'bearer'] else 'X-API-Key: $KEY'

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'ENV_KEY': config['env_key'],
        'BASE_URL': config['base_url'],
        'AUTH_HEADER': auth_header,
        'COMMON_ISSUES': '',
        'API_DOCS_URL': config.get('api_docs_url', ''),
        'CREATED_DATE': created_date
    }
    content = render_template(template, variables)
    (refs_dir / "error-handling.md").write_text(content, encoding='utf-8')

    # Authentication
    template = load_template("references/authentication.md.template")

    auth_type_desc = {
        'oauth2': '''OAuth 2.0 uses client credentials to obtain access tokens.
The client exchanges client ID and secret for a time-limited access token.''',
        'bearer': '''Bearer token authentication uses your API key directly as the bearer token.
No token exchange required.''',
        'api_key': '''API key authentication passes your key directly in request headers.
Simple and straightforward, no token management needed.'''
    }.get(config['auth_type'], '')

    headers_doc = {
        'oauth2': '''```http
Authorization: Bearer {access_token}
Content-Type: application/json
```''',
        'bearer': '''```http
Authorization: Bearer {api_key}
Content-Type: application/json
```''',
        'api_key': '''```http
X-API-Key: {api_key}
Content-Type: application/json
```'''
    }.get(config['auth_type'], '')

    env_template = f"{config['env_key']}=your_api_key_here"

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'AUTH_TYPE': config['auth_type'].upper().replace('_', ' '),
        'AUTH_TYPE_DESCRIPTION': auth_type_desc,
        'ENV_TEMPLATE': env_template,
        'HEADERS_DOCUMENTATION': headers_doc,
        'AUTH_FLOW_DOCUMENTATION': '',
        'TOKEN_MANAGEMENT': 'Token management is handled automatically by the API client.',
        'TOKEN_EXPIRED_HANDLING': 'The client automatically refreshes expired tokens.',
        'CREATED_DATE': created_date
    }
    content = render_template(template, variables)
    (refs_dir / "authentication.md").write_text(content, encoding='utf-8')


def create_connect_skill(config: dict, output_dir: Path):
    """Create the connect meta-skill"""
    connect_dir = output_dir / f"{config['service_slug']}-connect"
    connect_dir.mkdir(parents=True, exist_ok=True)

    template = load_template("connect-skill.md.template")

    # Generate trigger phrases
    triggers = [f"'{config['service_slug']}'"]
    for ep in config['endpoints']:
        for trigger in ep.get('triggers', []):
            triggers.append(f"'{trigger}'")
    trigger_phrases = ", ".join(triggers[:5])

    # Purpose list
    purpose_list = "\n".join([f"- **{ep['name']}**" for ep in config['endpoints'][:5]])

    # Trigger list
    trigger_list = "\n".join([f"- \"{config['service_slug']}\""] + [
        f'- "{t}"' for ep in config['endpoints'] for t in ep.get('triggers', [])[:2]
    ][:10])

    # Credential instructions
    cred_instructions = f'''1. Log into {config['service_name']}
2. Go to Settings > API or Developer section
3. Create a new API key
4. Copy the key'''

    # Env vars
    env_vars = f"{config['env_key']}=xxx"

    # Workflows
    workflows = ""
    for i, ep in enumerate(config['endpoints'], 1):
        workflows += f'''
### Workflow {i}: {ep['name']}
**Trigger**: {", ".join([f'"{t}"' for t in ep.get("triggers", [ep["name"].lower()])])}

```bash
python 00-system/skills/{config['service_slug']}/{config['service_slug']}-master/scripts/{ep['slug']}.py --json
```

---
'''

    # Routing table
    routing = "\n".join([
        f'| "{ep.get("triggers", [ep["name"].lower()])[0]}" | Workflow {i} |'
        for i, ep in enumerate(config['endpoints'], 1)
    ])

    # Skill handoff table
    handoff = "\n".join([
        f'| `{config["service_slug"]}-{ep["slug"]}` | {ep["description"][:50]}... |'
        for ep in config['endpoints'][:5]
    ])

    # Example interactions
    examples = f'''
**User**: "{config['endpoints'][0].get('triggers', ['do something'])[0] if config['endpoints'] else 'help'}"

**AI**:
```
Let me check your {config['service_name']} configuration first...
{chr(10032)} Configuration valid

[Proceeds with operation...]
```
'''

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'TRIGGER_PHRASES': trigger_phrases,
        'PURPOSE_LIST': purpose_list,
        'TRIGGER_LIST': trigger_list,
        'CREDENTIAL_INSTRUCTIONS': cred_instructions,
        'ENV_VARS': env_vars,
        'WORKFLOWS': workflows,
        'ROUTING_TABLE': routing,
        'SKILL_HANDOFF_TABLE': handoff,
        'EXAMPLE_INTERACTIONS': examples,
        'CREATED_DATE': datetime.now().strftime('%Y-%m-%d')
    }

    content = render_template(template, variables)
    (connect_dir / "SKILL.md").write_text(content, encoding='utf-8')

    print(f"  Created: {connect_dir.relative_to(PROJECT_ROOT)}/")


def create_operation_skill(config: dict, endpoint: dict, output_dir: Path):
    """Create a specialized skill for a single endpoint"""
    skill_dir = output_dir / f"{config['service_slug']}-{endpoint['slug']}"
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)

    # Create SKILL.md
    template = load_template("operation-skill.md.template")

    triggers = ", ".join([f'"{t}"' for t in endpoint.get('triggers', [endpoint['name'].lower()])])
    function_name = endpoint['slug'].replace('-', '_')

    # CLI examples
    cli_examples = f'''# Basic usage
python scripts/{endpoint['slug']}.py

# With output file
python scripts/{endpoint['slug']}.py --output result.json'''

    # Python examples
    python_examples = f'''# Basic call
result = {function_name}()
print(result)'''

    # Parameters section
    params_section = ""
    if endpoint.get('parameters'):
        params_section = "**Parameters**:\n"
        for param in endpoint['parameters']:
            params_section += f"- `{param['name']}` ({param.get('type', 'string')}) - {param.get('description', '')}\n"

    auth_header = 'Bearer $TOKEN' if config['auth_type'] in ['oauth2', 'bearer'] else 'X-API-Key: $KEY'

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'OPERATION_NAME': endpoint['name'],
        'OPERATION_SLUG': endpoint['slug'],
        'OPERATION_DESCRIPTION': endpoint['description'],
        'TRIGGER_PHRASES': triggers,
        'ENV_VARS': f"{config['env_key']}=your_api_key_here",
        'ENV_KEY': config['env_key'],
        'CLI_EXAMPLES': cli_examples,
        'FUNCTION_NAME': function_name,
        'PYTHON_EXAMPLES': python_examples,
        'API_DOCS_URL': config.get('api_docs_url', ''),
        'HTTP_METHOD': endpoint['method'],
        'BASE_URL': config['base_url'],
        'ENDPOINT_PATH': endpoint['path'],
        'AUTH_HEADER': auth_header,
        'PARAMETERS_SECTION': params_section,
        'SUCCESS_CODE': '200 OK',
        'RESPONSE_EXAMPLE': '{\n  "data": [...]\n}',
        'CREATED_DATE': datetime.now().strftime('%Y-%m-%d')
    }

    content = render_template(template, variables)
    (skill_dir / "SKILL.md").write_text(content, encoding='utf-8')

    # Create operation script
    create_operation_script(config, endpoint, skill_dir / "scripts")

    print(f"  Created: {skill_dir.relative_to(PROJECT_ROOT)}/")


def create_operation_script(config: dict, endpoint: dict, scripts_dir: Path):
    """Create the Python script for an endpoint"""
    template = load_template("operation-script.py.template")

    function_name = endpoint['slug'].replace('-', '_')

    # Build function params and argparse
    func_params = ""
    args_doc = ""
    argparse_args = ""
    func_call_args = ""
    env_vars_help = f"    {config['env_key']}    {config['service_name']} API key"

    if endpoint.get('parameters'):
        params = []
        for param in endpoint['parameters']:
            param_name = param['name'].replace('-', '_')
            param_type = param.get('type', 'str')
            default = param.get('default', 'None')

            params.append(f"{param_name}: {param_type} = {default}")
            args_doc += f"        {param_name}: {param.get('description', '')}\n"

            # Argparse
            if param.get('required'):
                argparse_args += f'''
    parser.add_argument(
        "{param_name}",
        help="{param.get('description', '')}"
    )
'''
            else:
                argparse_args += f'''
    parser.add_argument(
        "--{param['name']}",
        help="{param.get('description', '')}",
        default={default}
    )
'''
            func_call_args += f"args.{param_name}, "

        func_params = ", ".join(params)
        func_call_args = func_call_args.rstrip(", ")

    # Function body
    if endpoint['method'] == 'GET':
        func_body = f'''
    params = {{}}
    # Add parameters to params dict as needed

    return client.get("{endpoint['path']}", params=params)'''
    elif endpoint['method'] == 'POST':
        func_body = f'''
    data = {{}}
    # Add request body fields as needed

    return client.post("{endpoint['path']}", data=data)'''
    elif endpoint['method'] == 'PATCH':
        func_body = f'''
    data = {{}}
    # Add fields to update

    return client.patch("{endpoint['path']}", data=data)'''
    else:  # DELETE
        func_body = f'''
    return client.delete("{endpoint['path']}")'''

    cli_examples = f"    python {endpoint['slug']}.py"

    variables = {
        'SERVICE_NAME': config['service_name'],
        'SERVICE_SLUG': config['service_slug'],
        'OPERATION_NAME': endpoint['name'],
        'OPERATION_SLUG': endpoint['slug'],
        'OPERATION_DESCRIPTION': endpoint['description'],
        'FUNCTION_NAME': function_name,
        'FUNCTION_PARAMS': func_params,
        'FUNCTION_DOCSTRING': endpoint['description'],
        'ARGS_DOCSTRING': args_doc or '        None',
        'RETURNS_DOCSTRING': '',
        'FUNCTION_BODY': func_body,
        'CLI_ARGS': '',
        'CLI_EXAMPLES': cli_examples,
        'ENV_VARS_HELP': env_vars_help,
        'ARGPARSE_ARGS': argparse_args,
        'FUNCTION_CALL_ARGS': func_call_args
    }

    content = render_template(template, variables)
    (scripts_dir / f"{endpoint['slug']}.py").write_text(content, encoding='utf-8')


def scaffold_integration(config: dict):
    """Main scaffolding function"""
    print(f"\nScaffolding {config['service_name']} integration...")
    print("=" * 50)

    output_dir = SKILLS_DIR / config['service_slug']
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create master skill
    print("\n1. Creating master skill...")
    create_master_skill(config, output_dir)

    # Create connect skill
    print("\n2. Creating connect skill...")
    create_connect_skill(config, output_dir)

    # Create operation skills
    print("\n3. Creating operation skills...")
    for endpoint in config['endpoints']:
        create_operation_skill(config, endpoint, output_dir)

    print("\n" + "=" * 50)
    print(f"Integration scaffolded successfully!")
    print(f"Location: {output_dir.relative_to(PROJECT_ROOT)}/")
    print()
    print("Next steps:")
    print(f"1. Review generated files in {output_dir.relative_to(PROJECT_ROOT)}/")
    print("2. Update API client authentication if needed")
    print("3. Test connection with config check script")
    print("4. Customize operation scripts as needed")


def main():
    parser = argparse.ArgumentParser(
        description="Scaffold a new integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--config", "-c",
        help="Path to JSON config file"
    )
    parser.add_argument(
        "--service",
        help="Service name (e.g., 'HubSpot')"
    )
    parser.add_argument(
        "--base-url",
        help="API base URL"
    )
    parser.add_argument(
        "--auth-type",
        choices=['oauth2', 'api_key', 'bearer'],
        default='bearer',
        help="Authentication type"
    )

    args = parser.parse_args()

    if args.config:
        # Load from config file
        config_path = Path(args.config)
        if not config_path.exists():
            print(f"Error: Config file not found: {config_path}")
            sys.exit(1)

        with open(config_path, 'r') as f:
            config = json.load(f)
    elif args.service:
        # Build config from arguments
        service_slug = slugify(args.service)
        config = {
            'service_name': args.service,
            'service_slug': service_slug,
            'base_url': args.base_url or f'https://api.{service_slug}.com',
            'auth_type': args.auth_type,
            'env_key': f'{service_slug.upper().replace("-", "_")}_API_KEY',
            'endpoints': []
        }
        print("Warning: No endpoints specified. Creating skeleton structure.")
    else:
        parser.print_help()
        sys.exit(1)

    scaffold_integration(config)


if __name__ == "__main__":
    main()
