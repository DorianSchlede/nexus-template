#!/usr/bin/env python3
"""
Mental Models Metadata Scanner

Simple scanner that outputs ALL mental model metadata.
NO selection logic - just scans and returns metadata.

Usage:
    python select_mental_models.py

Output:
    JSON array with file path and description for each model
"""

import yaml
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

def extract_yaml_frontmatter(file_path: Path) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from markdown file.
    Identical to nexus-loader.py logic.
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

        return metadata

    except Exception as e:
        return {'error': str(e), '_file_path': str(file_path)}

def scan_mental_models(models_dir: Path) -> List[Dict[str, Any]]:
    """
    Scan all mental model files and extract metadata.
    Returns list with only file path and description.
    """
    models = []

    if not models_dir.exists():
        return []

    # Find all .md files
    for model_file in models_dir.glob("*.md"):
        metadata = extract_yaml_frontmatter(model_file)
        if metadata and 'error' not in metadata:
            # Only include file path and description (no name)
            models.append({
                "file": metadata.get('_file_path'),
                "description": metadata.get('description', '')
            })

    return models

def main():
    # Auto-detect base path (like nexus-loader.py)
    # Script lives in: {nexus-root}/00-system/mental-models/scripts/select_mental_models.py
    # Go up 3 levels: scripts -> mental-models -> 00-system -> nexus-root
    script_path = Path(__file__).resolve()
    base_path = script_path.parent.parent.parent.parent

    # Models directory (system-level)
    models_dir = base_path / "00-system" / "mental-models" / "references" / "mental-models"

    # Scan all models (distributed YAML frontmatter)
    all_models = scan_mental_models(models_dir)

    # Output JSON (pretty-printed for readability)
    print(json.dumps(all_models, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
