#!/usr/bin/env python3
"""Upload the 11 failed skills with SKILL.md only (partial bundle)."""

import os
import sys
import json
import base64
import requests
from pathlib import Path
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

def find_nexus_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    return None

nexus_root = find_nexus_root()
if not nexus_root:
    print('Could not find Nexus root')
    sys.exit(1)

# Load .env
env_path = os.path.join(nexus_root, '.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

api_key = os.environ.get('AIRTABLE_API_KEY_MUTAGENT')
if not api_key:
    print('AIRTABLE_API_KEY_MUTAGENT not set')
    sys.exit(1)

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

base_id = 'app1gngDx52VAgjVQ'
table_id = 'tblsQL8n9EfMAFIyD'
url = f'https://api.airtable.com/v0/{base_id}/{table_id}'

# Failed skills - upload with SKILL.md only
failed_skills = [
    ('google', 'google-integration', '00-system/skills/google'),
    ('notebooklm', 'notebooklm', '00-system/skills/notebooklm'),
    ('slack', 'slack', '00-system/skills/slack'),
    ('system', 'add-integration', '00-system/skills/system/add-integration'),
    ('skill-dev', 'create-skill', '00-system/skills/skill-dev/create-skill'),
    ('projects', 'execute-project', '00-system/skills/projects/execute-project'),
    ('notion', 'notion-master', '00-system/skills/notion/notion-master'),
    ('hubspot', 'hubspot-master', '00-system/skills/hubspot/hubspot-master'),
    ('slack', 'slack-master', '00-system/skills/slack/slack-master'),
    ('beam', 'beam-master', '00-system/skills/beam/beam-master'),
    ('airtable', 'airtable-master', '00-system/skills/airtable/airtable-master'),
]

success = 0
failed = 0

for team, name, rel_path in failed_skills:
    skill_path = Path(nexus_root) / rel_path
    skill_md = skill_path / 'SKILL.md'

    if not skill_md.exists():
        print(f'{name}: SKILL.md not found')
        failed += 1
        continue

    # Read SKILL.md content
    with open(skill_md, 'rb') as f:
        content = f.read()

    # Create minimal bundle
    bundle = {
        'skill_name': name,
        'version': '1.0',
        'bundle_format': 'nexus-skill-bundle-v1',
        'created': datetime.now().isoformat(),
        'files': {
            'SKILL.md': base64.b64encode(content).decode('utf-8')
        },
        'partial': True
    }

    bundle_json = json.dumps(bundle, ensure_ascii=False)

    # Build fields
    fields = {
        'Name': name,
        'Version': '1.0',
        'Content': bundle_json,
        'Team': team
    }

    body = {
        'records': [{'fields': fields}],
        'typecast': True
    }

    print(f'{name}...', end=' ', flush=True)

    try:
        response = requests.post(url, headers=headers, json=body, timeout=30)
        if response.status_code == 200:
            data = response.json()
            record_id = data['records'][0]['id']
            print(f'OK ({record_id}) [partial]')
            success += 1
        else:
            error = response.json().get('error', {})
            print(f'FAILED: {error.get("message", response.status_code)}')
            failed += 1
    except Exception as e:
        print(f'ERROR: {e}')
        failed += 1

print(f'\nDone! {success} uploaded, {failed} failed')
