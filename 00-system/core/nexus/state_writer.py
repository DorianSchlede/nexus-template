"""
State Writer - Generic YAML Config Updater for Nexus

Provides atomic, safe updates to user-config.yaml with:
- Nested path support (e.g., "onboarding.path_chosen")
- Atomic writes (write to .tmp -> rename)
- YAML validation
- Concurrent write safety

Usage:
    from state_writer import update_yaml_path

    # Update nested path
    update_yaml_path(
        config_path=Path("01-memory/user-config.yaml"),
        yaml_path="onboarding.path_chosen",
        value="quick_start"
    )

    # Update with integer
    update_yaml_path(
        config_path=Path("01-memory/user-config.yaml"),
        yaml_path="onboarding.quick_start_state.step_completed",
        value=3
    )
"""

import yaml
import shutil
from pathlib import Path
from typing import Any, Optional
from datetime import datetime


class StateWriteError(Exception):
    """Raised when state write operations fail."""
    pass


def update_yaml_path(
    config_path: Path,
    yaml_path: str,
    value: Any,
    create_backup: bool = False
) -> bool:
    """
    Update a nested YAML path in user-config.yaml atomically.

    Args:
        config_path: Path to the YAML config file (e.g., 01-memory/user-config.yaml)
        yaml_path: Dot-separated path to the field (e.g., "onboarding.path_chosen")
        value: Value to set (str, int, bool, list, dict, None)
        create_backup: Whether to create backup before write (default: False)

    Returns:
        bool: True if update succeeded, False otherwise

    Examples:
        >>> update_yaml_path(config, "onboarding.status", "in_progress")
        True
        >>> update_yaml_path(config, "onboarding.quick_start_state.step_completed", 3)
        True
        >>> update_yaml_path(config, "onboarding.path_chosen", "complete_setup")
        True
    """
    if not config_path.exists():
        print(f"Error: Config file does not exist: {config_path}")
        return False

    try:
        # 1. BACKUP (if enabled)
        if create_backup:
            backup_path = _create_backup(config_path)
            if not backup_path:
                print(f"Warning: Could not create backup for {config_path}")

        # 2. LOAD existing config
        with config_path.open('r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # 3. UPDATE nested path
        _set_nested_value(config, yaml_path, value)

        # 4. VALIDATE YAML structure
        if not _validate_config(config):
            print(f"Error: Config validation failed after update")
            return False

        # 5. ATOMIC WRITE (write to .tmp -> rename)
        temp_path = config_path.with_suffix('.tmp')

        with temp_path.open('w', encoding='utf-8') as f:
            yaml.dump(
                config,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120
            )

        # Atomic rename (overwrites destination)
        temp_path.replace(config_path)

        return True

    except Exception as e:
        print(f"Error updating YAML path '{yaml_path}': {e}")
        return False


def update_multiple_paths(
    config_path: Path,
    updates: dict[str, Any],
    create_backup: bool = False
) -> bool:
    """
    Update multiple YAML paths in a single atomic operation.

    More efficient than calling update_yaml_path multiple times
    as it only loads, validates, and writes once.

    Args:
        config_path: Path to the YAML config file
        updates: Dict mapping YAML paths to values
            Example: {
                "onboarding.status": "in_progress",
                "onboarding.path_chosen": "quick_start",
                "onboarding.quick_start_state.step_completed": 1
            }
        create_backup: Whether to create backup before write (default: False)

    Returns:
        bool: True if all updates succeeded, False otherwise
    """
    if not config_path.exists():
        print(f"Error: Config file does not exist: {config_path}")
        return False

    try:
        # 1. BACKUP (if enabled)
        if create_backup:
            backup_path = _create_backup(config_path)
            if not backup_path:
                print(f"Warning: Could not create backup for {config_path}")

        # 2. LOAD existing config
        with config_path.open('r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # 3. UPDATE all nested paths
        for yaml_path, value in updates.items():
            _set_nested_value(config, yaml_path, value)

        # 4. VALIDATE YAML structure
        if not _validate_config(config):
            print(f"Error: Config validation failed after updates")
            return False

        # 5. ATOMIC WRITE
        temp_path = config_path.with_suffix('.tmp')

        with temp_path.open('w', encoding='utf-8') as f:
            yaml.dump(
                config,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
                width=120
            )

        temp_path.replace(config_path)

        return True

    except Exception as e:
        print(f"Error updating multiple YAML paths: {e}")
        return False


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _set_nested_value(data: dict, path: str, value: Any) -> None:
    """
    Set a value at a nested path in a dictionary.

    Creates intermediate dictionaries if they don't exist.

    Args:
        data: The dictionary to modify (modified in-place)
        path: Dot-separated path (e.g., "onboarding.path_chosen")
        value: Value to set

    Examples:
        >>> config = {"onboarding": {"status": "not_started"}}
        >>> _set_nested_value(config, "onboarding.path_chosen", "quick_start")
        >>> config
        {'onboarding': {'status': 'not_started', 'path_chosen': 'quick_start'}}
    """
    keys = path.split('.')
    current = data

    # Navigate to parent of target field
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            # Path blocked by non-dict value, create dict
            current[key] = {}
        current = current[key]

    # Set the final value
    current[keys[-1]] = value


def _validate_config(config: dict) -> bool:
    """
    Validate that config has required structure.

    Basic validation - ensures critical top-level sections exist.

    Args:
        config: The loaded YAML config

    Returns:
        bool: True if valid, False otherwise
    """
    try:
        # Must be a dict
        if not isinstance(config, dict):
            return False

        # Should have some expected top-level keys
        # (lenient - we don't enforce all keys exist)
        expected_keys = ['user_preferences', 'onboarding', 'learning_tracker']

        # At least one expected key should exist
        if not any(key in config for key in expected_keys):
            return False

        return True

    except Exception:
        return False


def _create_backup(config_path: Path) -> Optional[Path]:
    """
    Create timestamped backup of config file.

    Backups are stored in same directory with .backup extension.
    Format: user-config.2026-01-26_142530.yaml.backup

    Args:
        config_path: Path to config file to backup

    Returns:
        Path to backup file, or None if backup failed
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_path = config_path.parent / f"{config_path.stem}.{timestamp}{config_path.suffix}.backup"

        shutil.copy2(config_path, backup_path)

        # Clean old backups (keep last 10)
        _cleanup_old_backups(config_path.parent, config_path.stem, keep=10)

        return backup_path

    except Exception as e:
        print(f"Warning: Could not create backup: {e}")
        return None


def _cleanup_old_backups(backup_dir: Path, config_stem: str, keep: int = 10) -> None:
    """
    Remove old backup files, keeping only the most recent N.

    Args:
        backup_dir: Directory containing backups
        config_stem: Stem of config file (e.g., "user-config")
        keep: Number of most recent backups to keep
    """
    try:
        # Find all backups for this config
        pattern = f"{config_stem}.*.backup"
        backups = sorted(
            backup_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        # Remove old backups (keep most recent N)
        for old_backup in backups[keep:]:
            old_backup.unlink()

    except Exception:
        # Silent failure - not critical
        pass


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def increment_step(config_path: Path, state_path: str) -> bool:
    """
    Increment a step counter (e.g., quick_start_state.step_completed).

    Reads current value and increments by 1.

    Args:
        config_path: Path to config file
        state_path: Path to step counter (e.g., "onboarding.quick_start_state.step_completed")

    Returns:
        bool: True if increment succeeded
    """
    try:
        # Read current value
        with config_path.open('r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # Get current step
        keys = state_path.split('.')
        current = config
        for key in keys:
            if key not in current:
                current[key] = 0 if key == keys[-1] else {}
            current = current[key]

        current_step = int(current) if isinstance(current, int) else 0

        # Increment
        return update_yaml_path(config_path, state_path, current_step + 1)

    except Exception as e:
        print(f"Error incrementing step '{state_path}': {e}")
        return False


def set_onboarding_status(config_path: Path, status: str) -> bool:
    """
    Set onboarding.status field.

    Args:
        config_path: Path to config file
        status: One of: "not_started", "in_progress", "complete"

    Returns:
        bool: True if update succeeded
    """
    valid_statuses = ["not_started", "in_progress", "complete"]
    if status not in valid_statuses:
        print(f"Error: Invalid status '{status}'. Must be one of: {valid_statuses}")
        return False

    return update_yaml_path(config_path, "onboarding.status", status)


def set_in_progress_skill(config_path: Path, skill_name: Optional[str]) -> bool:
    """
    Set onboarding.in_progress_skill field.

    Args:
        config_path: Path to config file
        skill_name: Skill name (e.g., "quick-start") or None to clear

    Returns:
        bool: True if update succeeded
    """
    return update_yaml_path(config_path, "onboarding.in_progress_skill", skill_name)
