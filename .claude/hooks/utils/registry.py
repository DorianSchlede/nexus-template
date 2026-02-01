"""
Shortcut registry lookup for executable detection.

Single source of truth: registry tells us type and path.
No pattern guessing needed for Bash shortcuts.
"""

import os
import re
from pathlib import Path
from typing import Optional, Dict, Any

# Cache registry to avoid repeated file reads
_registry_cache: Optional[Dict[str, Any]] = None
_registry_mtime: float = 0

# Path patterns for type detection (used by registry and Read fallback)
ENTITY_TYPE_PATTERNS = {
    "agent": r"/01-agents/",
    "skill": r"/02-skills/",
    "task": r"/03-tasks/",
    "workflow": r"/04-workflows/",
}


def get_registry_path() -> Path:
    """Get path to shortcut registry."""
    # Try relative to CWD first (for mutagent-obsidian repo)
    cwd = Path.cwd()
    candidates = [
        cwd / ".architech" / "navigation" / "shortcut-registry.yaml",
        cwd / "architech" / ".architech" / "navigation" / "shortcut-registry.yaml",
    ]
    for p in candidates:
        if p.exists():
            return p
    return candidates[0]  # Return first candidate even if not exists


def load_registry() -> Dict[str, Any]:
    """Load and cache the shortcut registry."""
    global _registry_cache, _registry_mtime

    registry_path = get_registry_path()

    if not registry_path.exists():
        return {"static_shortcuts": {}, "repo_aware_shortcuts": {}}

    # Check if we need to reload
    try:
        current_mtime = registry_path.stat().st_mtime
    except Exception:
        return {"static_shortcuts": {}, "repo_aware_shortcuts": {}}

    if _registry_cache is not None and current_mtime == _registry_mtime:
        return _registry_cache

    try:
        # Use PyYAML if available, otherwise parse manually
        try:
            import yaml
            with open(registry_path, "r", encoding="utf-8") as f:
                _registry_cache = yaml.safe_load(f) or {}
        except ImportError:
            # Fallback: simple line-based parsing
            _registry_cache = _parse_yaml_simple(registry_path)

        _registry_mtime = current_mtime
        return _registry_cache

    except Exception:
        return {"static_shortcuts": {}, "repo_aware_shortcuts": {}}


def _parse_yaml_simple(path: Path) -> Dict[str, Any]:
    """Simple YAML parser for shortcut registry (no external deps)."""
    result: Dict[str, Any] = {"static_shortcuts": {}, "repo_aware_shortcuts": {}}
    current_section: Optional[str] = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip()
            if not line or line.startswith("#"):
                continue

            if line == "static_shortcuts:":
                current_section = "static_shortcuts"
            elif line == "repo_aware_shortcuts:":
                current_section = "repo_aware_shortcuts"
            elif current_section and line.startswith("  "):
                # Parse "  ~shortcut: path" or "  ~shortcut:"
                match = re.match(r"\s+(~[^:]+):\s*(.+)?", line)
                if match:
                    shortcut = match.group(1)
                    value = match.group(2)
                    if value:
                        result[current_section][shortcut] = value.strip()

    return result


def detect_type_from_path(path: str) -> Optional[str]:
    """Detect entity type from file path."""
    normalized = path.replace("\\", "/")
    for entity_type, pattern in ENTITY_TYPE_PATTERNS.items():
        if re.search(pattern, normalized, re.IGNORECASE):
            return entity_type
    return None


def extract_id_from_path(path: str) -> str:
    """
    Extract executable ID from file path.

    Handles:
    - /01-agents/meta-architect/current/meta-architect.md -> meta-architect
    - /01-agents/meta-architect.md -> meta-architect
    - /02-skills/plan-build/plan-build.md -> plan-build
    """
    normalized = path.replace("\\", "/")

    # Pattern: /XX-type/name/... -> extract name (folder-based structure)
    match = re.search(r"/\d{2}-(?:agents|skills|tasks|workflows)/([^/]+)/", normalized)
    if match:
        return match.group(1)

    # Pattern: /XX-type/name.md -> extract name (file-based structure)
    match = re.search(r"/\d{2}-(?:agents|skills|tasks|workflows)/([^/]+)\.md$", normalized)
    if match:
        return match.group(1)

    return "_unknown_"


def lookup_shortcut(shortcut: str) -> Optional[Dict[str, str]]:
    """
    Look up shortcut in registry to get type and resolved path.

    Args:
        shortcut: The shortcut to look up (e.g., "~meta-architect")

    Returns:
        {"type": "agent", "id": "meta-architect", "path": "..."} or None
    """
    registry = load_registry()

    # Check static shortcuts
    static = registry.get("static_shortcuts", {})
    if shortcut in static:
        path = static[shortcut]
        entity_type = detect_type_from_path(path)
        if entity_type:
            return {
                "type": entity_type,
                "id": extract_id_from_path(path),
                "path": path
            }

    # Check repo-aware shortcuts (they store path specs, not direct paths)
    repo_aware = registry.get("repo_aware_shortcuts", {})
    if shortcut in repo_aware:
        spec = repo_aware[shortcut]
        # For repo-aware, we'd need to resolve the spec
        # For now, extract type from the spec pattern
        entity_type = detect_type_from_path(spec) if isinstance(spec, str) else None
        if entity_type:
            return {
                "type": entity_type,
                "id": extract_id_from_path(spec) if isinstance(spec, str) else shortcut.lstrip("~"),
                "path": spec if isinstance(spec, str) else ""
            }

    return None
