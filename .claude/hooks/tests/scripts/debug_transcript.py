"""Debug a specific transcript."""
import json
import re
from pathlib import Path

PROJECT_PATTERN = re.compile(r'02-projects[/\\]([0-9]{2}-[a-zA-Z0-9_-]+)', re.IGNORECASE)

t = Path.home() / '.claude/projects/c--Users-dsber-infinite-auto-company-strategy-nexus/528f44e2-a3a0-4a28-beac-aa655e7c6369.jsonl'

with open(t, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f'Total lines: {len(lines)}')
print('Checking ALL entries...')

project_mentions = {}
for idx, line in enumerate(lines):
    try:
        data = json.loads(line)
        msg = data.get('message', {})

        if msg.get('role') != 'assistant':
            continue

        content = msg.get('content', [])
        for item in content:
            if item.get('type') != 'tool_use':
                continue

            tool_name = item.get('name', '')
            if tool_name not in ('Read', 'Write', 'Edit', 'Glob', 'Grep', 'Bash'):
                continue

            tool_input = item.get('input', {})
            file_path = tool_input.get('file_path', '') or tool_input.get('path', '')

            match = PROJECT_PATTERN.search(file_path)
            if match:
                pid = match.group(1)
                project_mentions[pid] = idx
                print(f'  [{idx}] {tool_name}: {pid}')

    except:
        continue

print(f'\nTotal project mentions via file_path/path: {len(project_mentions)}')
if project_mentions:
    winner = max(project_mentions.items(), key=lambda x: x[1])[0]
    print(f'Most recent: {winner}')
else:
    print('NO MATCHES - checking if the pattern matches raw line content...')
    # Check raw content
    for idx, line in enumerate(lines[-50:]):
        if '21-inductive' in line:
            print(f'  Line {idx}: contains 21-inductive')
