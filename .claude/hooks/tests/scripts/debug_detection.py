"""Debug why build 21 was detected incorrectly."""
import json
import re
from pathlib import Path

BUILD_PATTERN = re.compile(r'02-builds[/\\]([0-9]{2}-[a-zA-Z0-9_-]+)', re.IGNORECASE)

t = Path.home() / '.claude/builds/c--Users-dsber-infinite-auto-company-strategy-nexus/528f44e2-a3a0-4a28-beac-aa655e7c6369.jsonl'

with open(t, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")
print("Looking for tool_use entries with build paths...")

for i, line in enumerate(lines):
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

            match = BUILD_PATTERN.search(file_path)
            if match:
                print(f'Line {i}: {tool_name} matched {match.group(1)}')
                print(f'  file_path: {file_path[:120]}')
    except:
        continue

print("\nDone.")
