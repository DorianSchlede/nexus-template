"""
Validation script: Test transcript parsing against real Claude Code transcripts.

Run with: python .claude/hooks/tests/validate_real_transcripts.py
"""

import json
import re
import sys
from pathlib import Path

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.transcript import (
    parse_transcript_for_build,
    check_skill_switch_after_build,
    BUILD_PATTERN,
)


def validate_transcripts(limit: int = 10):
    """Validate parsing against real transcripts."""

    transcripts_dir = Path.home() / '.claude' / 'builds' / 'c--Users-dsber-infinite-auto-company-strategy-nexus'

    if not transcripts_dir.exists():
        print(f"Transcripts dir not found: {transcripts_dir}")
        return

    transcripts = sorted(
        transcripts_dir.glob('*.jsonl'),
        key=lambda x: x.stat().st_mtime,
        reverse=True
    )[:limit]

    print(f"Validating {len(transcripts)} most recent transcripts...\n")
    print("=" * 80)

    for t in transcripts:
        print(f"\n{t.name[:50]}...")

        # Run the actual production function
        detected_build, method = parse_transcript_for_build(str(t))
        skill_switch = check_skill_switch_after_build(str(t), detected_build)

        # Also manually inspect what's happening
        with open(t, 'r', encoding='utf-8') as f:
            lines = f.readlines()[-100:]

        build_refs = []
        skill_refs = []

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

                    # Check for build refs
                    match = BUILD_PATTERN.search(file_path)
                    if match:
                        build_refs.append((idx, tool_name, match.group(1), file_path[:60]))

                    # Check for skill refs
                    if '/SKILL.md' in file_path:
                        skill_refs.append((idx, file_path[:60]))

            except:
                continue

        print(f"  Tool-based build refs found: {len(build_refs)}")
        for idx, tool, pid, path in build_refs[-5:]:  # Last 5
            print(f"    [{idx}] {tool}: {pid}")

        print(f"  Skill refs found: {len(skill_refs)}")
        for idx, path in skill_refs[-3:]:  # Last 3
            print(f"    [{idx}] {path}")

        print(f"  >>> RESULT: build={detected_build}, method={method}, skill_switch={skill_switch}")

        # Check if result makes sense
        if build_refs and not detected_build:
            print(f"  !!! WARNING: Found build refs but detection returned None")

        if detected_build and skill_switch:
            last_build_idx = max(r[0] for r in build_refs) if build_refs else -1
            last_skill_idx = max(r[0] for r in skill_refs) if skill_refs else -1
            print(f"  !!! SKILL SWITCH: proj@{last_build_idx}, skill@{last_skill_idx}")

    print("\n" + "=" * 80)
    print("Validation complete.")


if __name__ == "__main__":
    validate_transcripts(10)
