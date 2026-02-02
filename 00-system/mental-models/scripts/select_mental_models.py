#!/usr/bin/env python3
"""
Mental Models Metadata Scanner

Scans all mental model files and outputs metadata for AI selection.
Each model is a separate .md file with YAML frontmatter.

Usage:
    python select_mental_models.py [--category CATEGORY] [--format FORMAT]

Arguments:
    --category  Filter by category (e.g., cognitive, diagnostic, strategic)
    --format    Output format: 'full' (default), 'brief', 'list'

Output:
    JSON array with metadata for each model
"""

import yaml
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_yaml_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from markdown file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Match YAML frontmatter: ---\n[yaml]\n---
        match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not match:
            return None

        yaml_content = match.group(1)
        metadata = yaml.safe_load(yaml_content)

        if metadata:
            metadata['_file_path'] = str(file_path)
            metadata['_file_name'] = file_path.name
            # Extract category from parent folder
            metadata['_category_folder'] = file_path.parent.name

        return metadata

    except Exception as e:
        return {'error': str(e), '_file_path': str(file_path)}

def scan_mental_models(models_dir: Path, category_filter: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Scan all mental model files recursively and extract metadata.

    Structure: models/{category}/{model-name}.md
    """
    models = []

    if not models_dir.exists():
        return []

    # Find all .md files recursively in category subdirectories
    for model_file in models_dir.glob("**/*.md"):
        metadata = extract_yaml_frontmatter(model_file)
        if metadata and 'error' not in metadata:
            # Apply category filter if specified
            if category_filter:
                model_category = metadata.get('category', metadata.get('_category_folder', ''))
                if model_category != category_filter:
                    continue

            # Derive slug from filename (no YAML field needed)
            slug = Path(metadata.get('_file_name', '')).stem
            models.append({
                "name": metadata.get('name', ''),
                "slug": slug,
                "category": metadata.get('_category_folder', ''),
                "file": metadata.get('_file_path', '')
            })

    # Sort by category, then by name
    models.sort(key=lambda x: (x.get('category', ''), x.get('name', '')))

    return models

def format_output(models: List[Dict[str, Any]], format_type: str, base_path: Path) -> str:
    """Format output based on requested format."""
    if format_type == 'brief':
        # Compact: category → slug list (AI derives path from pattern)
        # Path pattern: 00-system/mental-models/models/{category}/{slug}.md
        by_category = {}
        for m in models:
            cat = m.get('category', 'other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(m.get('slug', ''))

        lines = ["# Models by Category", "# Path: 00-system/mental-models/models/{category}/{slug}.md", ""]
        for cat, slugs in sorted(by_category.items()):
            lines.append(f"{cat}: {', '.join(slugs)}")
        return '\n'.join(lines)

    elif format_type == 'list':
        # Names only for display to user
        by_category = {}
        for m in models:
            cat = m.get('category', 'other')
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(m.get('name'))

        lines = []
        for cat, names in sorted(by_category.items()):
            lines.append(f"**{cat}**: {', '.join(names)}")
        return '\n'.join(lines)

    else:  # 'full'
        return json.dumps(models, indent=2, ensure_ascii=False)

def main():
    parser = argparse.ArgumentParser(description='Scan mental models metadata')
    parser.add_argument('--category', type=str, help='Filter by category')
    parser.add_argument('--format', type=str, default='full',
                        choices=['full', 'brief', 'list'],
                        help='Output format')
    args = parser.parse_args()

    # Auto-detect base path
    # Script lives in: {nexus-root}/00-system/mental-models/scripts/
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent.parent.parent

    # Models directory - individual files organized by category
    models_dir = base_path / "00-system" / "mental-models" / "models"

    # Scan all models
    all_models = scan_mental_models(models_dir, args.category)

    # Output formatted JSON
    print(format_output(all_models, args.format, base_path))

if __name__ == "__main__":
    main()
