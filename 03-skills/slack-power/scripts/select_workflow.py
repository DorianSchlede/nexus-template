#!/usr/bin/env python3
"""
Slack Power Workflow Scanner

Scans all workflow files and outputs metadata for AI selection.
Each workflow is a separate .md file with YAML frontmatter.

Usage:
    python select_workflow.py [--category CATEGORY] [--format FORMAT]

Arguments:
    --category  Filter by category (extraction, preparation, broadcast, analysis)
    --format    Output format: 'full' (default), 'brief', 'list'

Output:
    JSON array with metadata for each workflow
"""

import yaml
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_yaml_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """Extract YAML frontmatter from markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None

        yaml_content = match.group(1)
        metadata = yaml.safe_load(yaml_content)

        if metadata:
            metadata['_file_path'] = str(file_path)
            metadata['_file_name'] = file_path.name
            metadata['_category_folder'] = file_path.parent.name

        return metadata

    except Exception as e:
        return {'error': str(e), '_file_path': str(file_path)}

def scan_workflows(workflows_dir: Path, category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Scan all workflow files recursively and extract metadata.
    Structure: workflows/{category}/{workflow-name}.md
    """
    workflows = []

    if not workflows_dir.exists():
        return []

    for workflow_file in workflows_dir.glob("**/*.md"):
        metadata = extract_yaml_frontmatter(workflow_file)
        if metadata and 'error' not in metadata:
            if category_filter:
                wf_category = metadata.get('category', metadata.get('_category_folder', ''))
                if wf_category != category_filter:
                    continue

            workflows.append({
                "name": metadata.get('name', ''),
                "slug": metadata.get('slug', ''),
                "category": metadata.get('category', metadata.get('_category_folder', '')),
                "description": metadata.get('description', ''),
                "triggers": metadata.get('triggers', []),
                "inputs": metadata.get('inputs', {}),
                "outputs": metadata.get('outputs', []),
                "scripts": metadata.get('scripts', []),
                "file": metadata.get('_file_path', '')
            })

    workflows.sort(key=lambda x: (x.get('category', ''), x.get('name', '')))
    return workflows

def format_output(workflows: List[Dict[str, Any]], format_type: str) -> str:
    """Format output based on requested format."""
    if format_type == 'brief':
        brief = []
        for w in workflows:
            brief.append({
                "name": w.get('name'),
                "slug": w.get('slug'),
                "category": w.get('category'),
                "description": w.get('description'),
                "triggers": w.get('triggers', [])[:3]  # First 3 triggers
            })
        return json.dumps(brief, indent=2, ensure_ascii=False)

    elif format_type == 'list':
        by_category = {}
        for w in workflows:
            cat = w.get('category', 'other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(w.get('name'))
        return json.dumps(by_category, indent=2, ensure_ascii=False)

    else:  # 'full'
        return json.dumps(workflows, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='Scan slack-power workflows')
    parser.add_argument('--category', type=str, help='Filter by category')
    parser.add_argument('--format', type=str, default='full',
                        choices=['full', 'brief', 'list'],
                        help='Output format')
    args = parser.parse_args()

    # Auto-detect base path (script in slack-power/scripts/)
    script_path = Path(__file__).resolve()
    skill_path = script_path.parent.parent
    workflows_dir = skill_path / "workflows"

    workflows = scan_workflows(workflows_dir, args.category)
    print(format_output(workflows, args.format))

if __name__ == "__main__":
    main()
