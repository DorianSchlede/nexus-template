#!/usr/bin/env python3
"""
Validate workspace-map.md against actual 04-workspace/ structure.

This script:
1. Scans 04-workspace/ for actual folders and files
2. Parses workspace-map.md for documented structure
3. Identifies discrepancies (missing, extra, stale entries)
4. Outputs JSON report for AI to process

Usage:
    python validate-workspace.py
    python validate-workspace.py --auto-fix  # Generate updated map content
"""

import os
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

def get_workspace_root() -> Path:
    """Find workspace root (contains 04-workspace/)."""
    current = Path(__file__).resolve()
    while current.parent != current:
        if (current / '04-workspace').exists():
            return current
        current = current.parent
    raise FileNotFoundError("Could not find workspace root (no 04-workspace/ found)")

def scan_workspace(workspace_path: Path) -> Dict:
    """Scan 04-workspace/ and return structure."""
    if not workspace_path.exists():
        return {"folders": [], "files": {}, "structure": {}}

    folders = []
    files = {}
    structure = {}

    # Scan top-level folders
    for item in workspace_path.iterdir():
        if item.name.startswith('.'):  # Skip hidden
            continue
        if item.name == 'workspace-map.md':  # Skip the map itself
            continue

        if item.is_dir():
            folder_name = item.name + '/'
            folders.append(folder_name)

            # Scan files in this folder
            folder_files = []
            folder_subfolders = []

            try:
                for subitem in item.iterdir():
                    if subitem.name.startswith('.'):
                        continue
                    if subitem.is_file():
                        folder_files.append(subitem.name)
                    elif subitem.is_dir():
                        folder_subfolders.append(subitem.name + '/')
            except PermissionError:
                pass

            files[folder_name] = folder_files
            structure[folder_name] = {
                "files": folder_files,
                "subfolders": folder_subfolders
            }

    return {
        "folders": sorted(folders),
        "files": files,
        "structure": structure
    }

def parse_workspace_map(map_path: Path) -> Dict:
    """Parse workspace-map.md and extract documented folders."""
    if not map_path.exists():
        return {"folders": [], "descriptions": {}}

    content = map_path.read_text(encoding='utf-8')
    folders = set()
    descriptions = {}

    # Extract ONLY the "Your Workspace Structure" section
    structure_match = re.search(
        r'## Your Workspace Structure\s*\n```(.*?)```',
        content,
        re.DOTALL
    )

    if structure_match:
        structure_section = structure_match.group(1)

        # Method 1: Find folders in tree structure (├──, └──)
        tree_pattern = r'[├└]──\s+(\w[\w-]*/)'
        for match in re.finditer(tree_pattern, structure_section):
            folder_name = match.group(1)
            folders.add(folder_name)

    # Method 2: Find folder headings in "Folder Descriptions" section ONLY
    # This prevents false positives from example text
    desc_section_match = re.search(
        r'## Folder Descriptions(.*?)(?=^##|\Z)',
        content,
        re.DOTALL | re.MULTILINE
    )

    if desc_section_match:
        desc_section = desc_section_match.group(1)
        heading_pattern = r'###\s+\*\*(\w[\w-]*/)\*\*|###\s+(\w[\w-]*/)'
        for match in re.finditer(heading_pattern, desc_section):
            folder_name = match.group(1) or match.group(2)
            folders.add(folder_name)

            # Extract description (next line after heading)
            start_pos = match.end()
            next_lines = desc_section[start_pos:start_pos+500]
            desc_match = re.search(r'\n([^\n#]+)', next_lines)
            if desc_match:
                descriptions[folder_name] = desc_match.group(1).strip()

    return {
        "folders": sorted(list(folders)),
        "descriptions": descriptions
    }

def compare_structures(actual: Dict, documented: Dict) -> Dict:
    """Compare actual vs documented and identify discrepancies."""
    actual_folders = set(actual["folders"])
    documented_folders = set(documented["folders"])

    missing_from_map = actual_folders - documented_folders
    extra_in_map = documented_folders - actual_folders
    perfect_match = len(missing_from_map) == 0 and len(extra_in_map) == 0

    # Check for file-level changes in documented folders
    file_changes = {}
    for folder in actual_folders & documented_folders:
        # Check if folder has files that might be important
        if folder in actual["files"] and len(actual["files"][folder]) > 0:
            file_changes[folder] = {
                "file_count": len(actual["files"][folder]),
                "key_files": actual["files"][folder][:5]  # First 5 files
            }

    return {
        "perfect_match": perfect_match,
        "missing_from_map": sorted(list(missing_from_map)),
        "extra_in_map": sorted(list(extra_in_map)),
        "common_folders": sorted(list(actual_folders & documented_folders)),
        "file_changes": file_changes,
        "actual_count": len(actual_folders),
        "documented_count": len(documented_folders)
    }

def generate_report(actual: Dict, documented: Dict, comparison: Dict) -> Dict:
    """Generate comprehensive validation report."""
    return {
        "status": "valid" if comparison["perfect_match"] else "needs_update",
        "timestamp": str(Path.cwd()),  # Placeholder for actual timestamp
        "actual_structure": actual,
        "documented_structure": documented,
        "comparison": comparison,
        "recommendations": generate_recommendations(comparison)
    }

def generate_recommendations(comparison: Dict) -> List[str]:
    """Generate actionable recommendations."""
    recs = []

    if comparison["missing_from_map"]:
        recs.append(f"Document {len(comparison['missing_from_map'])} new folders: {', '.join(comparison['missing_from_map'])}")

    if comparison["extra_in_map"]:
        recs.append(f"Remove {len(comparison['extra_in_map'])} stale entries: {', '.join(comparison['extra_in_map'])}")

    if comparison["perfect_match"]:
        recs.append("✅ workspace-map.md is accurate and up-to-date")

    return recs

def main():
    """Main validation workflow."""
    try:
        # Find workspace root
        root = get_workspace_root()
        workspace_path = root / '04-workspace'
        map_path = workspace_path / 'workspace-map.md'

        # Scan actual structure
        actual = scan_workspace(workspace_path)

        # Parse documented structure
        documented = parse_workspace_map(map_path)

        # Compare
        comparison = compare_structures(actual, documented)

        # Generate report
        report = generate_report(actual, documented, comparison)

        # Output JSON
        print(json.dumps(report, indent=2))

        # Exit code
        sys.exit(0 if comparison["perfect_match"] else 1)

    except Exception as e:
        error_report = {
            "status": "error",
            "error": str(e),
            "recommendations": ["Fix error and retry validation"]
        }
        print(json.dumps(error_report, indent=2))
        sys.exit(2)

if __name__ == '__main__':
    main()
