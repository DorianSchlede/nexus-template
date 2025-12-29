#!/usr/bin/env python3
"""
generate_subagent_prompts.py - Level 3 of 7-Level Synthesis Architecture

Generates subagent prompts with:
- INPUT CONTRACT (Gap G13)
- research_purpose (Gap G22a)
- synthesis_goals (Gap G22b)

Usage:
    python generate_subagent_prompts.py PROJECT_PATH --input PLAN_FILE --output-dir PROMPTS_DIR
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import yaml


PROMPT_TEMPLATE = """# Batch Extraction: {field_name} (Batch {batch_num} of {total_batches})

## INPUT CONTRACT (STRICT - Gap G13)

### Files You MUST Read (in this order)
1. `{project_path}/02-resources/_briefing.md`
2. `{project_path}/02-resources/_extraction_guide.md`
{chunk_list}

### Files You MUST NOT Read
- ANY `.pdf` file
- ANY other batch's chunks
- ANY file in 04-outputs/
- ANY file outside `{project_path}/`

### Directory Traversal FORBIDDEN
- Do NOT use `../` paths
- Do NOT follow symbolic links
- Stay within `{project_path}/` boundary

VIOLATION = Extraction fails validation.

---

## CONTEXT

### Research Purpose (Gap G22a)
{research_purpose}

### Synthesis Goals (Gap G22b)
{synthesis_goals}

---

## EXTRACTION CONTRACT

For field "{field_name}":
1. Read EACH chunk file completely - do not skim
2. Extract ALL patterns related to "{field_name}"
3. For EVERY pattern you find, include:
   - name: Pattern name (specific, not generic)
   - chunk_ref: "Paper-ID (Chunk N:Line-Line)"
   - quote: "Exact text from chunk" (100-150 chars)
   - description: Full context and detail

4. Write YAML output to: `{project_path}/03-working/_batch_{field_name}_{batch_num}.yaml`

---

## OUTPUT SCHEMA

```yaml
---
batch_id: "{field_name}_{batch_num}"
field: {field_name}
extracted_at: "{{timestamp}}"
chunks_read: {{count}}
patterns_found: {{count}}
---

patterns:
  - name: "Pattern Name"
    chunk_ref: "Paper-ID (Chunk N:Line-Line)"
    quote: "Exact text proving pattern exists in this chunk..."
    description: "Full context: what this pattern means, how it relates to {field_name}"

  - name: "Another Pattern"
    chunk_ref: "Paper-ID (Chunk M:Line-Line)"
    quote: "Another exact quote..."
    description: "Context for this pattern"
```

---

## CRITICAL REQUIREMENTS

1. You MUST read the actual chunk files listed above
2. You MUST include exact quotes with line numbers
3. You MUST use citation format: Paper-ID (Chunk N:Line-Line)
4. Do NOT summarize - include full detail from chunks
5. Do NOT skip any relevant patterns in the chunks
6. Do NOT read any files not listed in INPUT CONTRACT
"""


def load_yaml(path: Path) -> Dict[str, Any]:
    """Load YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_yaml_frontmatter(content: str) -> Dict[str, Any]:
    """Parse YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}

    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def read_briefing(project_path: Path) -> Dict[str, Any]:
    """Read _briefing.md for research_purpose."""
    briefing_path = project_path / "02-resources" / "_briefing.md"
    if not briefing_path.exists():
        return {}

    content = briefing_path.read_text(encoding='utf-8')
    return parse_yaml_frontmatter(content)


def read_analysis_kit(project_path: Path) -> Dict[str, Any]:
    """Read _analysis_kit.md for synthesis_goals."""
    kit_path = project_path / "02-resources" / "_analysis_kit.md"
    if not kit_path.exists():
        return {}

    content = kit_path.read_text(encoding='utf-8')
    return parse_yaml_frontmatter(content)


def generate_prompts(
    project_path: Path,
    plan: Dict[str, Any],
    briefing: Dict[str, Any],
    analysis_kit: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Generate prompt files for each batch."""
    prompts = []

    # Extract context fields
    research_purpose = briefing.get('research_purpose', 'Not specified in _briefing.md')

    # Build synthesis goals from analysis_kit or generate default
    synthesis_goals_parts = []
    if 'comparison_goal' in analysis_kit:
        synthesis_goals_parts.append(f"Compare: {analysis_kit['comparison_goal']}")
    if 'identification_goal' in analysis_kit:
        synthesis_goals_parts.append(f"Identify: {analysis_kit['identification_goal']}")
    if 'analysis_goal' in analysis_kit:
        synthesis_goals_parts.append(f"Analyze: {analysis_kit['analysis_goal']}")

    if not synthesis_goals_parts:
        synthesis_goals = "Extract patterns that support cross-paper synthesis (synthesis goals not specified in _analysis_kit.md)"
    else:
        synthesis_goals = "\n".join(f"- {g}" for g in synthesis_goals_parts)

    # Count batches per field
    field_batch_counts = {}
    for batch in plan['level4_batches']:
        field = batch['field']
        field_batch_counts[field] = field_batch_counts.get(field, 0) + 1

    # Generate prompts
    field_batch_nums = {}
    for batch in plan['level4_batches']:
        field_name = batch['field']
        batch_id = batch['batch_id']
        chunks = batch['chunks']

        # Track batch number per field
        field_batch_nums[field_name] = field_batch_nums.get(field_name, 0) + 1
        batch_num = field_batch_nums[field_name]
        total_batches = field_batch_counts[field_name]

        # Build chunk list for INPUT CONTRACT
        chunk_lines = []
        for i, chunk in enumerate(chunks, 3):  # Start at 3 since briefing is 1, extraction_guide is 2
            paper_id = chunk['paper_id']
            chunk_num = chunk['chunk']
            chunk_lines.append(
                f"{i}. `{project_path}/02-resources/papers/{paper_id}/{paper_id}_{chunk_num}.md`"
            )
        chunk_list = "\n".join(chunk_lines)

        # Generate prompt content
        prompt_content = PROMPT_TEMPLATE.format(
            field_name=field_name,
            batch_num=batch_num,
            total_batches=total_batches,
            project_path=project_path,
            chunk_list=chunk_list,
            research_purpose=research_purpose,
            synthesis_goals=synthesis_goals
        )

        prompts.append({
            'batch_id': batch_id,
            'field': field_name,
            'filename': f"_prompt_{batch_id}.md",
            'content': prompt_content
        })

    return prompts


def main():
    parser = argparse.ArgumentParser(
        description='Generate subagent prompts with INPUT CONTRACT (Level 3 of 7-Level Architecture)'
    )
    parser.add_argument('project_path', type=Path, help='Path to research project')
    parser.add_argument('--input', '-i', type=Path, required=True, help='Input subagent plan YAML file')
    parser.add_argument('--output-dir', '-o', type=Path, required=True, help='Output directory for prompts')
    args = parser.parse_args()

    project_path = args.project_path
    if not project_path.is_absolute():
        project_path = Path.cwd() / project_path

    # Resolve input path
    input_path = args.input
    if not input_path.is_absolute():
        input_path = project_path / input_path

    if not input_path.exists():
        print(f"ERROR: Subagent plan not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Load inputs
    print(f"Loading subagent plan from {input_path}...")
    plan = load_yaml(input_path)

    print("Reading _briefing.md for research_purpose (G22a)...")
    briefing = read_briefing(project_path)

    print("Reading _analysis_kit.md for synthesis_goals (G22b)...")
    analysis_kit = read_analysis_kit(project_path)

    # Generate prompts
    print("Generating prompts with INPUT CONTRACT (G13)...")
    prompts = generate_prompts(project_path, plan, briefing, analysis_kit)

    # Write prompts
    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = project_path / output_dir

    output_dir.mkdir(parents=True, exist_ok=True)

    for prompt in prompts:
        prompt_path = output_dir / prompt['filename']
        prompt_path.write_text(prompt['content'], encoding='utf-8')

    print(f"\nLevel 3 Complete: {len(prompts)} prompts written to {output_dir}")
    print(f"\nContext included:")
    print(f"  ✓ INPUT CONTRACT (G13)")
    print(f"  ✓ research_purpose (G22a)")
    print(f"  ✓ synthesis_goals (G22b)")


if __name__ == '__main__':
    main()
