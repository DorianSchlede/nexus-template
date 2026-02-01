"""
Schema Migration - Upgrade user-config.yaml from v4 to v5

Handles schema upgrades for user-config.yaml to support hybrid onboarding.

Key Changes in v5:
- Rename: setup_system_state -> complete_setup_state
- Add: onboarding.path_chosen field
- Add: onboarding.quick_start_state object
- Update: in_progress_skill "setup-system" -> "complete-setup"
- Add: schema_version field for future migrations

Usage:
    from migrate import migrate_if_needed

    # Check and migrate if needed
    migrate_if_needed(Path("01-memory/user-config.yaml"))
"""

import yaml
import shutil
from pathlib import Path
from typing import Optional
from datetime import datetime


CURRENT_SCHEMA_VERSION = "5.0"


def migrate_if_needed(config_path: Path, create_backup: bool = True) -> bool:
    """
    Check config schema version and migrate if needed.

    Args:
        config_path: Path to user-config.yaml
        create_backup: Whether to create backup before migration

    Returns:
        bool: True if migration was performed, False if not needed or failed
    """
    if not config_path.exists():
        print(f"Warning: Config file does not exist: {config_path}")
        return False

    try:
        # Load config
        with config_path.open('r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

        # Detect schema version
        current_version = config.get('schema_version', '4.0')  # Default to 4.0 if missing

        if current_version == CURRENT_SCHEMA_VERSION:
            # Already up to date
            return False

        if current_version == '4.0':
            print(f"Migrating user-config.yaml from v{current_version} to v{CURRENT_SCHEMA_VERSION}...")

            # Create backup
            if create_backup:
                _create_migration_backup(config_path)

            # Perform migration
            migrate_v4_to_v5(config)

            # Save migrated config
            _save_config(config_path, config)

            print(f"[OK] Migration complete: v{current_version} -> v{CURRENT_SCHEMA_VERSION}")
            return True

        else:
            print(f"Warning: Unknown schema version '{current_version}'. Skipping migration.")
            return False

    except Exception as e:
        print(f"Error during migration: {e}")
        return False


def migrate_v4_to_v5(config: dict) -> None:
    """
    Migrate config from v4 to v5 schema.

    Modifications (in-place):
    - Add schema_version: "5.0"
    - Rename onboarding.setup_system_state -> complete_setup_state
    - Add onboarding.path_chosen (default: null)
    - Add onboarding.quick_start_state object
    - Update onboarding.in_progress_skill if set to "setup-system"
    - Update comments to reflect new field names

    Args:
        config: The loaded config dict (modified in-place)
    """

    # 1. ADD schema_version
    config['schema_version'] = CURRENT_SCHEMA_VERSION

    # 2. ENSURE onboarding section exists
    if 'onboarding' not in config:
        config['onboarding'] = {}

    onboarding = config['onboarding']

    # 3. RENAME setup_system_state -> complete_setup_state
    if 'setup_system_state' in onboarding:
        onboarding['complete_setup_state'] = onboarding.pop('setup_system_state')

        # Also rename projects_initiated -> first_build_created within state
        if 'projects_initiated' in onboarding['complete_setup_state']:
            onboarding['complete_setup_state']['first_build_created'] = \
                onboarding['complete_setup_state'].pop('projects_initiated')

        # Add hi_menu_taught field if missing
        if 'hi_menu_taught' not in onboarding['complete_setup_state']:
            onboarding['complete_setup_state']['hi_menu_taught'] = False

    # 4. ADD path_chosen field if missing
    if 'path_chosen' not in onboarding:
        # Infer from existing state
        if onboarding.get('chosen_path') == 'direct':
            onboarding['path_chosen'] = 'complete_setup'  # v4 direct -> v5 complete_setup
        else:
            onboarding['path_chosen'] = None  # Not yet chosen

    # 5. ADD quick_start_state object if missing
    if 'quick_start_state' not in onboarding:
        onboarding['quick_start_state'] = {
            'step_completed': 0,
            'intention_captured': False,
            'first_build_created': False,
            'workspace_created': False
        }

    # 6. UPDATE in_progress_skill if set to "setup-system"
    if onboarding.get('in_progress_skill') == 'setup-system':
        onboarding['in_progress_skill'] = 'complete-setup'

    # 7. SIMPLIFY status if using old granular values
    status = onboarding.get('status', 'not_started')
    if status in ['tour_in_progress', 'setup_in_progress']:
        onboarding['status'] = 'in_progress'
    elif status in ['tour_complete', 'system_setup_complete', 'first_build_started']:
        onboarding['status'] = 'complete'


def get_schema_version(config_path: Path) -> str:
    """
    Get the schema version of a config file.

    Args:
        config_path: Path to user-config.yaml

    Returns:
        str: Schema version (e.g., "4.0", "5.0") or "4.0" if missing
    """
    if not config_path.exists():
        return "4.0"

    try:
        with config_path.open('r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}
        return config.get('schema_version', '4.0')
    except Exception:
        return "4.0"


# =============================================================================
# INTERNAL HELPERS
# =============================================================================

def _create_migration_backup(config_path: Path) -> Optional[Path]:
    """
    Create timestamped backup before migration.

    Backup format: user-config.MIGRATION_v4_to_v5_2026-01-26_142530.yaml.backup

    Args:
        config_path: Path to config file

    Returns:
        Path to backup or None if failed
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        current_version = get_schema_version(config_path)
        backup_path = config_path.parent / \
            f"{config_path.stem}.MIGRATION_v{current_version}_to_v{CURRENT_SCHEMA_VERSION}_{timestamp}{config_path.suffix}.backup"

        shutil.copy2(config_path, backup_path)
        print(f"[OK] Backup created: {backup_path.name}")
        return backup_path

    except Exception as e:
        print(f"Warning: Could not create migration backup: {e}")
        return None


def _save_config(config_path: Path, config: dict) -> None:
    """
    Save migrated config with atomic write.

    Args:
        config_path: Path to config file
        config: Migrated config dict
    """
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

    # Atomic rename
    temp_path.replace(config_path)


# =============================================================================
# VALIDATION
# =============================================================================

def validate_v5_schema(config: dict) -> tuple[bool, list[str]]:
    """
    Validate that a config matches v5 schema requirements.

    Args:
        config: The config dict to validate

    Returns:
        tuple[bool, list[str]]: (is_valid, list of error messages)
    """
    errors = []

    # Check schema version
    if config.get('schema_version') != CURRENT_SCHEMA_VERSION:
        errors.append(f"schema_version is '{config.get('schema_version')}', expected '{CURRENT_SCHEMA_VERSION}'")

    # Check onboarding section
    if 'onboarding' not in config:
        errors.append("Missing 'onboarding' section")
        return False, errors

    onboarding = config['onboarding']

    # Check required fields
    required_fields = [
        'status',
        'in_progress_skill',
        'language_preference',
        'path_chosen',
        'quick_start_state',
        'complete_setup_state'
    ]

    for field in required_fields:
        if field not in onboarding:
            errors.append(f"Missing onboarding.{field}")

    # Check quick_start_state structure
    if 'quick_start_state' in onboarding:
        required_quick_start_fields = [
            'step_completed',
            'intention_captured',
            'first_build_created',
            'workspace_created'
        ]
        for field in required_quick_start_fields:
            if field not in onboarding['quick_start_state']:
                errors.append(f"Missing onboarding.quick_start_state.{field}")

    # Check complete_setup_state structure
    if 'complete_setup_state' in onboarding:
        required_complete_setup_fields = [
            'step_completed',
            'files_uploaded',
            'file_analysis_done',
            'role_captured',
            'goals_captured',
            'roadmap_created',
            'workspace_created',
            'first_build_created',
            'hi_menu_taught'
        ]
        for field in required_complete_setup_fields:
            if field not in onboarding['complete_setup_state']:
                errors.append(f"Missing onboarding.complete_setup_state.{field}")

    # Check that old field names don't exist
    if 'setup_system_state' in onboarding:
        errors.append("Old field 'setup_system_state' still exists (should be 'complete_setup_state')")

    if onboarding.get('in_progress_skill') == 'setup-system':
        errors.append("in_progress_skill still set to 'setup-system' (should be 'complete-setup')")

    return len(errors) == 0, errors


# =============================================================================
# CLI FOR TESTING
# =============================================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python3 migrate.py <path-to-user-config.yaml>")
        sys.exit(1)

    config_path = Path(sys.argv[1])

    if not config_path.exists():
        print(f"Error: File not found: {config_path}")
        sys.exit(1)

    # Perform migration
    migrated = migrate_if_needed(config_path)

    if migrated:
        # Validate result
        with config_path.open('r') as f:
            config = yaml.safe_load(f)

        is_valid, errors = validate_v5_schema(config)

        if is_valid:
            print("[OK] Migration successful and validated!")
            sys.exit(0)
        else:
            print("[ERROR] Migration completed but validation failed:")
            for error in errors:
                print(f"  - {error}")
            sys.exit(1)
    else:
        print("[INFO]  No migration needed (already v5 or error occurred)")
        sys.exit(0)
