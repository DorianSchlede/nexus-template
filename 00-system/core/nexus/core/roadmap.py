"""
Roadmap management for Nexus.

This module handles roadmap parsing, status derivation, and bidirectional
sync between roadmap items and builds.

Key Principles:
- Status is DERIVED, never stored (prevents drift)
- `completed_at` is the only persistent completion marker
- `build_id` links roadmap items to builds
- Slug matching enables backwards sync
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

logger = logging.getLogger(__name__)

# =============================================================================
# YAML SCHEMA CONSTANTS
# =============================================================================

# Required fields for each roadmap item
REQUIRED_FIELDS: List[str] = ["name"]

# Optional fields with their default values
OPTIONAL_FIELDS: Dict[str, Any] = {
    "type": "feature",
    "priority": "medium",
    "rationale": "",
    "done_when": "",
    "build_id": None,
    "completed_at": None,
    "depends_on": [],
}

# Valid values for constrained fields
VALID_TYPES: List[str] = ["feature", "integration", "research", "strategy", "fix", "improvement"]
VALID_PRIORITIES: List[str] = ["critical", "high", "medium", "low"]

# Status values (derived, never stored)
STATUS_COMPLETED = "completed"
STATUS_IN_PROGRESS = "in_progress"
STATUS_NOT_STARTED = "not_started"


# =============================================================================
# SLUG MATCHING
# =============================================================================


def slugify(name: str) -> str:
    """
    Convert a name to a slug for matching.

    Slug matching rules (CRITICAL - exact algorithm):
    1. Lowercase the entire string
    2. Replace spaces with hyphens
    3. Remove all non-alphanumeric characters except hyphens
    4. Collapse multiple hyphens into one
    5. Strip leading/trailing hyphens

    Examples:
        "Content Calendar" -> "content-calendar"
        "Slack Integration!" -> "slack-integration"
        "01-content-calendar" -> "01-content-calendar" (already a slug)
        "API v2 Updates" -> "api-v2-updates"
    """
    # Lowercase
    slug = name.lower()
    # Replace spaces with hyphens
    slug = slug.replace(" ", "-")
    # Remove non-alphanumeric except hyphens
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    # Collapse multiple hyphens
    slug = re.sub(r"-+", "-", slug)
    # Strip leading/trailing hyphens
    slug = slug.strip("-")
    return slug


def names_match(item_name: str, build_id: str) -> bool:
    """
    Check if a roadmap item name matches a build ID.

    Matching rules (CRITICAL - exact algorithm):
    1. Slugify the item name
    2. The build_id slug must CONTAIN the item slug
    3. This allows "01-content-calendar" to match "content-calendar"

    Args:
        item_name: Human-readable name from roadmap (e.g., "Content Calendar")
        build_id: Build folder ID (e.g., "01-content-calendar")

    Returns:
        True if the slugified item_name is contained in slugified build_id
    """
    item_slug = slugify(item_name)
    build_slug = slugify(build_id)

    # Check if item slug is contained in build slug
    # This handles numbered prefixes like "01-content-calendar"
    return item_slug in build_slug


# =============================================================================
# PARSING FUNCTIONS
# =============================================================================


def load_roadmap(path: Path) -> Dict[str, Any]:
    """
    Load and parse a roadmap.yaml file.

    Args:
        path: Path to the roadmap.yaml file

    Returns:
        Dict with 'items' list and 'metadata' dict.
        Returns empty items list on error.

    Error Handling (REQ-NF-2):
        - Missing file: Returns empty items, logs debug
        - Malformed YAML: Returns empty items, logs error
        - Missing required fields: Skips item, logs warning
    """
    result: Dict[str, Any] = {"items": [], "metadata": {}}

    if not path.exists():
        logger.debug(f"Roadmap file not found: {path}")
        return result

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logger.error(f"Malformed YAML in roadmap: {path} - {e}")
        return result
    except Exception as e:
        logger.error(f"Error reading roadmap: {path} - {e}")
        return result

    if not data:
        logger.debug(f"Empty roadmap file: {path}")
        return result

    # Extract metadata (top-level fields except 'items')
    if isinstance(data, dict):
        result["metadata"] = {k: v for k, v in data.items() if k != "items"}
        raw_items = data.get("items", [])
    else:
        logger.warning(f"Roadmap is not a dict: {path}")
        return result

    # Validate and normalize items
    if not isinstance(raw_items, list):
        logger.warning(f"Roadmap 'items' is not a list: {path}")
        return result

    for i, item in enumerate(raw_items):
        if not isinstance(item, dict):
            logger.warning(f"Roadmap item {i} is not a dict, skipping")
            continue

        # Check required fields
        missing = [f for f in REQUIRED_FIELDS if f not in item]
        if missing:
            logger.warning(f"Roadmap item {i} missing required fields {missing}, skipping")
            continue

        # Normalize item with defaults
        normalized = {**OPTIONAL_FIELDS, **item}

        # Validate constrained fields
        if normalized["type"] not in VALID_TYPES:
            logger.warning(f"Invalid type '{normalized['type']}' for item '{normalized['name']}', using 'feature'")
            normalized["type"] = "feature"

        if normalized["priority"] not in VALID_PRIORITIES:
            logger.warning(
                f"Invalid priority '{normalized['priority']}' for item '{normalized['name']}', using 'medium'"
            )
            normalized["priority"] = "medium"

        result["items"].append(normalized)

    return result


def save_roadmap(path: Path, data: Dict[str, Any]) -> bool:
    """
    Save roadmap data to a YAML file.

    Args:
        path: Path to save the roadmap.yaml file
        data: Dict with 'items' list and optional 'metadata' dict

    Returns:
        True on success, False on error
    """
    try:
        # Combine metadata and items
        output = {**data.get("metadata", {}), "items": data.get("items", [])}

        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(output, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        logger.debug(f"Saved roadmap to {path}")
        return True

    except Exception as e:
        logger.error(f"Error saving roadmap: {path} - {e}")
        return False


# =============================================================================
# STATUS DERIVATION
# =============================================================================


def derive_item_status(item: Dict[str, Any], active_ids: Set[str], complete_ids: Set[str]) -> str:
    """
    Derive the status of a roadmap item from build state.

    Status Derivation Rules (REQ-3, REQ-4, REQ-10):
    1. If `completed_at` is set -> "completed" (survives build deletion)
    2. If `build_id` is in complete_ids -> "completed"
    3. If `build_id` is in active_ids -> "in_progress"
    4. If `build_id` is null/None -> "not_started"
    5. If `build_id` set but not found -> "in_progress" (orphan, still counts as active)

    Args:
        item: Roadmap item dict
        active_ids: Set of build IDs in 02-builds/active/
        complete_ids: Set of build IDs in 02-builds/complete/

    Returns:
        One of: "completed", "in_progress", "not_started"
    """
    # Rule 1: completed_at takes absolute precedence
    if item.get("completed_at"):
        return STATUS_COMPLETED

    build_id = item.get("build_id")

    # Rule 4: No build_id means not started
    if not build_id:
        return STATUS_NOT_STARTED

    # Rule 2: Build in complete folder
    if build_id in complete_ids:
        return STATUS_COMPLETED

    # Rule 3: Build in active folder
    if build_id in active_ids:
        return STATUS_IN_PROGRESS

    # Rule 5: build_id set but folder not found (orphan)
    # Treat as in_progress - user might have renamed or it's mid-transition
    return STATUS_IN_PROGRESS


# =============================================================================
# SYNC FUNCTIONS (FORWARDS)
# =============================================================================


def link_roadmap_item(roadmap_path: Path, item_name: str, build_id: str) -> bool:
    """
    Link a roadmap item to a build by setting its build_id.

    Called by plan-build skill when creating a build from a roadmap item.

    Args:
        roadmap_path: Path to roadmap.yaml
        item_name: Name of the roadmap item to link
        build_id: Build ID to link to

    Returns:
        True if item was found and linked, False otherwise
    """
    roadmap = load_roadmap(roadmap_path)
    if not roadmap["items"]:
        logger.warning(f"Cannot link item: roadmap empty or not found")
        return False

    # Find matching item by name
    found = False
    for item in roadmap["items"]:
        if item["name"] == item_name:
            if item.get("build_id"):
                logger.warning(f"Item '{item_name}' already linked to build '{item['build_id']}'")
                return False
            item["build_id"] = build_id
            found = True
            logger.info(f"Linked roadmap item '{item_name}' to build '{build_id}'")
            break

    if not found:
        logger.warning(f"Roadmap item not found: '{item_name}'")
        return False

    return save_roadmap(roadmap_path, roadmap)


def mark_roadmap_complete(roadmap_path: Path, build_id: str) -> bool:
    """
    Mark a roadmap item as complete when its build moves to complete/.

    Called when archive-build moves a build to 02-builds/complete/.

    Args:
        roadmap_path: Path to roadmap.yaml
        build_id: Build ID that was completed

    Returns:
        True if item was found and marked, False otherwise
    """
    roadmap = load_roadmap(roadmap_path)
    if not roadmap["items"]:
        logger.debug(f"No roadmap items to mark complete")
        return False

    # Find item by build_id
    found = False
    for item in roadmap["items"]:
        if item.get("build_id") == build_id:
            if item.get("completed_at"):
                logger.debug(f"Item already marked complete: '{item['name']}'")
                return True
            item["completed_at"] = datetime.now().strftime("%Y-%m-%d")
            found = True
            logger.info(f"Marked roadmap item '{item['name']}' as complete")
            break

    if not found:
        logger.debug(f"No roadmap item linked to build '{build_id}'")
        return False

    return save_roadmap(roadmap_path, roadmap)


# =============================================================================
# SYNC FUNCTIONS (BACKWARDS)
# =============================================================================


def sync_roadmap_backwards(
    roadmap_path: Path,
    active_builds: List[Dict[str, str]],
    complete_builds: List[Dict[str, str]],
) -> Dict[str, List[str]]:
    """
    Sync roadmap backwards by auto-linking unlinked items to existing builds.

    Called on session startup to keep roadmap in sync with build state.

    Process (REQ-6, REQ-7):
    1. For each unlinked roadmap item (build_id is null):
       a. Slugify the item name
       b. Check if any active/complete build matches by slug
       c. If match found: set build_id
    2. For each linked item where build is in complete/:
       a. If completed_at is not set: set it

    Args:
        roadmap_path: Path to roadmap.yaml
        active_builds: List of dicts with 'id' key for builds in active/
        complete_builds: List of dicts with 'id' key for builds in complete/

    Returns:
        Dict with 'linked' (newly linked items) and 'completed' (newly marked complete)
    """
    result: Dict[str, List[str]] = {"linked": [], "completed": []}

    roadmap = load_roadmap(roadmap_path)
    if not roadmap["items"]:
        logger.debug("No roadmap items to sync")
        return result

    # Build lookup sets
    active_ids = {b["id"] for b in active_builds if "id" in b}
    complete_ids = {b["id"] for b in complete_builds if "id" in b}
    all_builds = list(active_builds) + list(complete_builds)

    modified = False

    for item in roadmap["items"]:
        item_name = item["name"]

        # Case 1: Unlinked item - try to find matching build
        if not item.get("build_id"):
            for build in all_builds:
                build_id = build.get("id", "")
                if names_match(item_name, build_id):
                    item["build_id"] = build_id
                    result["linked"].append(item_name)
                    modified = True
                    logger.debug(f"Backwards sync: linked '{item_name}' to '{build_id}'")
                    break

        # Case 2: Linked item in complete/ - ensure completed_at is set
        build_id = item.get("build_id")
        if build_id and build_id in complete_ids and not item.get("completed_at"):
            item["completed_at"] = datetime.now().strftime("%Y-%m-%d")
            result["completed"].append(item_name)
            modified = True
            logger.debug(f"Backwards sync: marked '{item_name}' complete")

    # Save if any changes were made
    if modified:
        save_roadmap(roadmap_path, roadmap)

    # Log summary at debug level (silent by design)
    if result["linked"] or result["completed"]:
        logger.debug(f"Backwards sync: linked {len(result['linked'])}, completed {len(result['completed'])}")

    return result


# =============================================================================
# SUMMARY FUNCTIONS
# =============================================================================


def get_roadmap_summary(
    roadmap_path: Path,
    active_ids: Set[str],
    complete_ids: Set[str],
) -> Dict[str, Any]:
    """
    Get a summary of roadmap status for menu display.

    Args:
        roadmap_path: Path to roadmap.yaml
        active_ids: Set of build IDs in 02-builds/active/
        complete_ids: Set of build IDs in 02-builds/complete/

    Returns:
        Dict with:
        - total: Total item count
        - completed: Completed item count
        - in_progress: In-progress item count
        - not_started: Not started item count
        - next: Name of next suggested item (first not_started by priority)
        - exists: Whether roadmap file exists
    """
    result: Dict[str, Any] = {
        "total": 0,
        "completed": 0,
        "in_progress": 0,
        "not_started": 0,
        "next": None,
        "exists": roadmap_path.exists(),
    }

    if not result["exists"]:
        return result

    roadmap = load_roadmap(roadmap_path)
    items = roadmap.get("items", [])
    result["total"] = len(items)

    # Priority order for "next" suggestion
    priority_order = {p: i for i, p in enumerate(VALID_PRIORITIES)}
    next_candidates: List[Tuple[int, str]] = []

    for item in items:
        status = derive_item_status(item, active_ids, complete_ids)

        if status == STATUS_COMPLETED:
            result["completed"] += 1
        elif status == STATUS_IN_PROGRESS:
            result["in_progress"] += 1
        else:
            result["not_started"] += 1
            # Track as potential "next" item
            priority = item.get("priority", "medium")
            priority_rank = priority_order.get(priority, 2)
            next_candidates.append((priority_rank, item["name"]))

    # Select highest priority not_started item as "next"
    if next_candidates:
        next_candidates.sort(key=lambda x: x[0])
        result["next"] = next_candidates[0][1]

    return result


def format_roadmap_line(summary: Dict[str, Any]) -> Optional[str]:
    """
    Format a summary line for menu display.

    Args:
        summary: Dict from get_roadmap_summary()

    Returns:
        Formatted string like "📋 Roadmap: 2 active, 3 planned | Next: Content Calendar"
        Returns None if roadmap doesn't exist
    """
    if not summary.get("exists"):
        return None

    parts = []

    # Count active (in_progress + not_started)
    active = summary.get("in_progress", 0)
    planned = summary.get("not_started", 0)
    completed = summary.get("completed", 0)

    if active > 0:
        parts.append(f"{active} active")
    if planned > 0:
        parts.append(f"{planned} planned")
    if completed > 0:
        parts.append(f"{completed} done")

    if not parts:
        return "📋 Roadmap: empty"

    line = f"📋 Roadmap: {', '.join(parts)}"

    # Add "Next" suggestion
    next_item = summary.get("next")
    if next_item:
        line += f" | Next: {next_item}"

    return line
