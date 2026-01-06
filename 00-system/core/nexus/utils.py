"""
Utility functions for Nexus.

This module contains shared helper functions for:
- YAML frontmatter extraction
- File reading and loading
- Token estimation
- Checkbox counting
- Template detection
"""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# PyYAML is optional - graceful degradation if not available
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None

from .config import CHARS_PER_TOKEN, get_templates_dir


def parse_simple_yaml(yaml_text: str) -> Dict[str, Any]:
    """
    Simple YAML parser for basic frontmatter (fallback when PyYAML unavailable).

    Supports:
    - Simple key: value pairs
    - Lists with - items
    - Nested objects (one level)
    - Quoted strings
    - Numbers and booleans

    Does NOT support:
    - Multi-line values
    - Complex nested structures
    - YAML anchors/references
    """
    result = {}
    current_key = None
    current_list = None

    for line in yaml_text.split('\n'):
        stripped = line.strip()

        # Skip empty lines and comments
        if not stripped or stripped.startswith('#'):
            continue

        # List item
        if stripped.startswith('- '):
            if current_list is not None:
                item = stripped[2:].strip()
                # Remove quotes
                if item.startswith('"') and item.endswith('"'):
                    item = item[1:-1]
                elif item.startswith("'") and item.endswith("'"):
                    item = item[1:-1]
                current_list.append(item)
            continue

        # Key: value pair
        if ':' in stripped:
            key, _, value = stripped.partition(':')
            key = key.strip()
            value = value.strip()

            # Start of a list
            if not value:
                current_key = key
                current_list = []
                result[key] = current_list
                continue

            # Regular key-value
            current_list = None
            current_key = None

            # Parse value type
            if value.lower() == 'true':
                result[key] = True
            elif value.lower() == 'false':
                result[key] = False
            elif value.lower() == 'null':
                result[key] = None
            elif value.startswith('"') and value.endswith('"'):
                result[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                result[key] = value[1:-1]
            else:
                # Try number
                try:
                    if '.' in value:
                        result[key] = float(value)
                    else:
                        result[key] = int(value)
                except ValueError:
                    # Keep as string
                    result[key] = value

    return result


def extract_yaml_frontmatter(file_path: str) -> Optional[Dict[str, Any]]:
    """
    Extract YAML frontmatter from a markdown file.

    Args:
        file_path: Path to the file to parse

    Returns:
        Dictionary with parsed YAML metadata, or None if no frontmatter found.
        On error, returns dict with 'error' key.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Match YAML frontmatter: ---\n[yaml]\n---
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not match:
            return None

        yaml_content = match.group(1)

        # Try PyYAML first (more reliable)
        if HAS_YAML:
            metadata = yaml.safe_load(yaml_content)
        else:
            # Fallback to simple parser
            metadata = parse_simple_yaml(yaml_content)

        if metadata:
            # Convert any date objects to ISO format strings for JSON serialization
            for key, value in metadata.items():
                if hasattr(value, "isoformat"):  # datetime, date objects
                    metadata[key] = value.isoformat()

            metadata["_file_path"] = str(file_path)
            metadata["_file_name"] = Path(file_path).name

        return metadata

    except Exception as e:
        return {"error": str(e), "_file_path": str(file_path)}


def load_file_content(file_path: str) -> str:
    """
    Load full file content as a string.

    Args:
        file_path: Path to the file to read

    Returns:
        File contents as string, or error message on failure
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"ERROR: {e}"


def estimate_tokens(text: str) -> int:
    """
    Estimate token count from text (rough approximation).

    Uses ~4 characters per token as a heuristic.

    Args:
        text: Text to estimate tokens for

    Returns:
        Estimated token count
    """
    if not text:
        return 0
    return len(text) // CHARS_PER_TOKEN


def count_checkboxes(steps_file: Path) -> Tuple[int, int, int]:
    """
    Count checkboxes in a steps.md or tasks.md file.

    Args:
        steps_file: Path to the file to count checkboxes in

    Returns:
        Tuple of (total, completed, uncompleted)
    """
    if not steps_file.exists():
        return (0, 0, 0)

    try:
        content = steps_file.read_text(encoding="utf-8")

        # Match checkbox patterns: - [ ] or - [x] or - [X]
        checked = len(re.findall(r"^\s*-\s*\[x\]", content, re.MULTILINE | re.IGNORECASE))
        unchecked = len(re.findall(r"^\s*-\s*\[\s\]", content, re.MULTILINE))

        total = checked + unchecked
        return (total, checked, unchecked)
    except Exception:
        return (0, 0, 0)


def is_template_file(file_path: str) -> bool:
    """
    Check if a file is a smart default template (not yet personalized).

    Detection methods:
    1. Check for `smart_default: true` in YAML frontmatter
    2. Fallback: Check for `[TODO: Set in onboarding` pattern

    Args:
        file_path: Path to file to check

    Returns:
        True if file is a template, False if personalized or doesn't exist
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Method 1: Check YAML frontmatter for smart_default flag
        match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if match:
            try:
                yaml_content = yaml.safe_load(match.group(1))
                if yaml_content and yaml_content.get("smart_default") is True:
                    return True
            except yaml.YAMLError:
                pass

        # Method 2: Fallback - check for TODO placeholder pattern
        if "[TODO: Set in onboarding" in content:
            return True

        return False

    except Exception:
        return False


def load_template(template_name: str) -> str:
    """
    Load a template file from the templates directory.

    Args:
        template_name: Name of the template file (e.g., "goals.md")

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template doesn't exist
    """
    template_path = get_templates_dir() / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_name}")

    return template_path.read_text(encoding="utf-8")


def embed_file_contents(file_paths: List[str]) -> Dict[str, str]:
    """
    Read all files and return their contents keyed by filename.

    Args:
        file_paths: List of absolute file paths to read

    Returns:
        Dictionary with filename as key and file content as value
    """
    contents = {}
    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                filename = Path(file_path).name
                contents[filename] = f.read()
        except Exception as e:
            filename = Path(file_path).name
            contents[filename] = f"ERROR reading file: {e}"
    return contents


def get_first_unchecked_task(content: str) -> Optional[str]:
    """
    Find the first unchecked task in markdown content.

    Args:
        content: Markdown content with checkbox tasks

    Returns:
        Description of the first unchecked task, or None if all complete
    """
    match = re.search(r"^\s*-\s*\[\s\]\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return None


def parse_env_file(env_path: Path) -> Dict[str, str]:
    """
    Parse a .env file and return key-value pairs.

    Only includes entries with non-empty values.

    Args:
        env_path: Path to the .env file

    Returns:
        Dictionary of environment variable names to values
    """
    env_vars = {}
    if not env_path.exists():
        return env_vars

    try:
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, value = line.partition("=")
                    # Remove quotes if present
                    value = value.strip().strip('"').strip("'")
                    if value:  # Only count if value is non-empty
                        env_vars[key.strip()] = value
    except Exception:
        pass

    return env_vars


def calculate_bundle_tokens(result: Dict[str, Any]) -> Dict[str, int]:
    """
    Calculate token costs for a loaded bundle.

    Args:
        result: Bundle result dictionary with 'files' and 'metadata'

    Returns:
        Token count statistics including total, by file, and percentage
    """
    from .config import CONTEXT_WINDOW
    import json

    token_counts = {
        "total": 0,
        "files": 0,
        "metadata": 0,
        "by_file": {},
    }

    # Count tokens in files
    for file_key, file_data in result.get("files", {}).items():
        if isinstance(file_data, dict) and "content" in file_data:
            tokens = estimate_tokens(file_data["content"])
            token_counts["files"] += tokens
            token_counts["by_file"][file_key] = tokens

    # Count tokens in metadata
    metadata = result.get("metadata", {})
    if metadata:
        metadata_str = json.dumps(metadata)
        token_counts["metadata"] = estimate_tokens(metadata_str)

    token_counts["total"] = token_counts["files"] + token_counts["metadata"]

    # Calculate percentage of context window
    token_counts["percentage"] = round((token_counts["total"] / CONTEXT_WINDOW) * 100, 2)

    return token_counts
