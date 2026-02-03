"""
Test script for migrate.py

Run with: python3 00-system/core/nexus/test_migrate.py
"""

import yaml
import tempfile
from pathlib import Path
from migrate import migrate_if_needed, migrate_v4_to_v5, validate_v5_schema, get_schema_version


def create_v4_config():
    """Create a v4 config (no schema_version field)."""
    return {
        'user_preferences': {
            'language': 'de',
            'timezone': 'Europe/Berlin'
        },
        'onboarding': {
            'status': 'setup_in_progress',
            'in_progress_skill': 'setup-system',
            'language_preference': 'de',
            'chosen_path': 'direct',
            'setup_system_state': {
                'step_completed': 3,
                'files_uploaded': True,
                'file_analysis_done': True,
                'role_captured': True,
                'goals_captured': False,
                'roadmap_created': False,
                'workspace_created': False,
                'projects_initiated': False
            }
        },
        'learning_tracker': {
            'completed': {
                'how_nexus_works': True
            }
        }
    }


def test_v4_to_v5_migration():
    """Test migration from v4 to v5."""
    print("\n=== Test 1: v4 -> v5 Migration ===")

    config = create_v4_config()

    # Verify it's v4 (no schema_version)
    assert 'schema_version' not in config, "Test config should not have schema_version"
    assert 'setup_system_state' in config['onboarding'], "Should have old field name"
    assert config['onboarding']['in_progress_skill'] == 'setup-system', "Should have old skill name"

    # Perform migration
    migrate_v4_to_v5(config)

    # Verify migration results
    print("\nVerifying migration results...")

    # 1. schema_version added
    assert config['schema_version'] == '5.0', "Should add schema_version"
    print("[OK] schema_version added")

    # 2. setup_system_state renamed
    assert 'setup_system_state' not in config['onboarding'], "Old field should be removed"
    assert 'complete_setup_state' in config['onboarding'], "New field should exist"
    print("[OK] setup_system_state -> complete_setup_state")

    # 3. projects_initiated renamed
    assert 'projects_initiated' not in config['onboarding']['complete_setup_state']
    assert 'first_build_created' in config['onboarding']['complete_setup_state']
    print("[OK] projects_initiated -> first_build_created")

    # 4. hi_menu_taught added
    assert 'hi_menu_taught' in config['onboarding']['complete_setup_state']
    print("[OK] hi_menu_taught field added")

    # 5. path_chosen added and inferred correctly
    assert config['onboarding']['path_chosen'] == 'complete_setup', "Should infer from chosen_path='direct'"
    print("[OK] path_chosen inferred correctly")

    # 6. quick_start_state added
    assert 'quick_start_state' in config['onboarding']
    assert config['onboarding']['quick_start_state']['step_completed'] == 0
    print("[OK] quick_start_state added")

    # 7. in_progress_skill updated
    assert config['onboarding']['in_progress_skill'] == 'complete-setup'
    print("[OK] in_progress_skill updated")

    # 8. status simplified
    assert config['onboarding']['status'] == 'in_progress', "setup_in_progress -> in_progress"
    print("[OK] status simplified")

    # 9. Data preserved
    assert config['onboarding']['complete_setup_state']['step_completed'] == 3, "Data should be preserved"
    assert config['onboarding']['complete_setup_state']['files_uploaded'] is True
    print("[OK] Existing data preserved")

    print("\n[OK] v4 -> v5 migration test passed!")


def test_schema_validation():
    """Test v5 schema validation."""
    print("\n=== Test 2: Schema Validation ===")

    config = create_v4_config()
    migrate_v4_to_v5(config)

    # Validate
    is_valid, errors = validate_v5_schema(config)

    if not is_valid:
        print(f"Validation errors: {errors}")

    assert is_valid, f"Migrated config should be valid, but got errors: {errors}"
    print("[OK] Migrated config passes validation")

    # Test with invalid config
    invalid_config = {'schema_version': '5.0', 'onboarding': {}}  # Missing required fields
    is_valid, errors = validate_v5_schema(invalid_config)

    assert not is_valid, "Should detect missing fields"
    assert len(errors) > 0, "Should return error messages"
    print(f"[OK] Validation correctly rejects invalid config ({len(errors)} errors detected)")

    print("\n[OK] Schema validation test passed!")


def test_migrate_if_needed():
    """Test migrate_if_needed with actual file."""
    print("\n=== Test 3: migrate_if_needed (Full Flow) ===")

    # Create temp config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(create_v4_config(), f)

    try:
        # Check version
        version = get_schema_version(config_path)
        assert version == '4.0', f"Should detect v4, got {version}"
        print("[OK] Correctly detected v4 schema")

        # Migrate
        result = migrate_if_needed(config_path, create_backup=True)
        assert result is True, "Should perform migration"
        print("[OK] Migration performed")

        # Verify backup created
        backups = list(config_path.parent.glob(f"{config_path.stem}.MIGRATION_*.backup"))
        assert len(backups) > 0, "Should create backup"
        print(f"[OK] Backup created: {backups[0].name}")

        # Check new version
        version = get_schema_version(config_path)
        assert version == '5.0', f"Should be v5 now, got {version}"
        print("[OK] Config upgraded to v5")

        # Load and validate
        with config_path.open('r') as f:
            migrated_config = yaml.safe_load(f)

        is_valid, errors = validate_v5_schema(migrated_config)
        assert is_valid, f"Migrated config should be valid: {errors}"
        print("[OK] Migrated config is valid")

        # Run migrate again (should skip)
        result = migrate_if_needed(config_path)
        assert result is False, "Should skip migration when already v5"
        print("[OK] Correctly skips migration when already v5")

        print("\n[OK] Full migration flow test passed!")

        # Clean up backups
        for backup in backups:
            backup.unlink()

    finally:
        config_path.unlink()


def test_edge_cases():
    """Test edge cases."""
    print("\n=== Test 4: Edge Cases ===")

    # Test 1: Tour path (not direct)
    print("\nTest 4a: Tour path inference")
    config = create_v4_config()
    config['onboarding']['chosen_path'] = 'tour'
    migrate_v4_to_v5(config)

    assert config['onboarding']['path_chosen'] is None, "Tour path should not set path_chosen"
    print("[OK] Tour path correctly inferred as null")

    # Test 2: Missing setup_system_state (fresh install)
    print("\nTest 4b: Fresh install (no setup_system_state)")
    config = {
        'user_preferences': {},
        'onboarding': {
            'status': 'not_started',
            'in_progress_skill': None
        }
    }
    migrate_v4_to_v5(config)

    assert 'complete_setup_state' not in config['onboarding'], "Should not create if didn't exist"
    assert 'quick_start_state' in config['onboarding'], "Should add quick_start_state"
    assert 'path_chosen' in config['onboarding'], "Should add path_chosen"
    print("[OK] Fresh install migration works")

    # Test 3: Different status values
    print("\nTest 4c: Status simplification")
    test_statuses = [
        ('tour_in_progress', 'in_progress'),
        ('setup_in_progress', 'in_progress'),
        ('tour_complete', 'complete'),
        ('system_setup_complete', 'complete'),
        ('first_build_started', 'complete'),
        ('not_started', 'not_started'),
        ('complete', 'complete')
    ]

    for old_status, expected_new in test_statuses:
        config = create_v4_config()
        config['onboarding']['status'] = old_status
        migrate_v4_to_v5(config)
        assert config['onboarding']['status'] == expected_new, \
            f"Status {old_status} should become {expected_new}, got {config['onboarding']['status']}"

    print("[OK] All status transitions work correctly")

    print("\n[OK] Edge cases test passed!")


def run_all_tests():
    """Run all migration tests."""
    print("="*60)
    print("MIGRATE.PY TEST SUITE")
    print("="*60)

    try:
        test_v4_to_v5_migration()
        test_schema_validation()
        test_migrate_if_needed()
        test_edge_cases()

        print("\n" + "="*60)
        print("[OK] ALL MIGRATION TESTS PASSED!")
        print("="*60)
        print("\nmigrate.py is ready for use.")
        return True

    except AssertionError as e:
        print(f"\n[ERROR] TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n[ERROR] UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import sys
    success = run_all_tests()
    sys.exit(0 if success else 1)
