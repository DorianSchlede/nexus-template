"""
Test script for state_writer.py

Run with: python3 00-system/core/nexus/test_state_writer.py
"""

import yaml
import tempfile
from pathlib import Path
from state_writer import update_yaml_path, update_multiple_paths, set_onboarding_status


def create_test_config():
    """Create a minimal test config similar to user-config.yaml."""
    return {
        'user_preferences': {
            'language': 'de',
            'timezone': 'Europe/Berlin'
        },
        'onboarding': {
            'status': 'not_started',
            'in_progress_skill': None,
            'language_preference': 'de',
            'chosen_path': None
        },
        'learning_tracker': {
            'completed': {
                'setup_memory': False,
                'how_nexus_works': False
            }
        }
    }


def test_nested_path_update():
    """Test updating nested YAML paths."""
    print("\n=== Test 1: Nested Path Updates ===")

    # Create temp config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(create_test_config(), f)

    try:
        # Test 1: Update simple nested path
        print("Test 1a: Update onboarding.status")
        result = update_yaml_path(config_path, "onboarding.status", "in_progress")
        assert result, "Failed to update onboarding.status"

        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        assert config['onboarding']['status'] == 'in_progress', "Value not updated correctly"
        print("[OK] Simple nested path works")

        # Test 2: Update path_chosen (new field)
        print("\nTest 1b: Add new field onboarding.path_chosen")
        result = update_yaml_path(config_path, "onboarding.path_chosen", "quick_start")
        assert result, "Failed to add path_chosen"

        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        assert config['onboarding']['path_chosen'] == 'quick_start', "New field not added"
        print("[OK] New field creation works")

        # Test 3: Create deep nested structure
        print("\nTest 1c: Create deep nested path onboarding.quick_start_state.step_completed")
        result = update_yaml_path(config_path, "onboarding.quick_start_state.step_completed", 3)
        assert result, "Failed to create deep nested path"

        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        assert config['onboarding']['quick_start_state']['step_completed'] == 3, "Deep nested value not set"
        print("[OK] Deep nested path creation works")

        # Test 4: Update boolean
        print("\nTest 1d: Update boolean value")
        result = update_yaml_path(config_path, "onboarding.quick_start_state.intention_captured", True)
        assert result, "Failed to set boolean"

        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        assert config['onboarding']['quick_start_state']['intention_captured'] is True
        print("[OK] Boolean update works")

        print("\n[OK] All nested path tests passed!")

    finally:
        config_path.unlink()


def test_multiple_updates():
    """Test batch updates."""
    print("\n=== Test 2: Multiple Updates (Batch) ===")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(create_test_config(), f)

    try:
        # Update multiple paths at once
        updates = {
            "onboarding.status": "in_progress",
            "onboarding.path_chosen": "complete_setup",
            "onboarding.in_progress_skill": "complete-setup",
            "onboarding.complete_setup_state.step_completed": 1,
            "onboarding.complete_setup_state.files_uploaded": False
        }

        result = update_multiple_paths(config_path, updates)
        assert result, "Failed to update multiple paths"

        # Verify all updates
        with config_path.open('r') as f:
            config = yaml.safe_load(f)

        assert config['onboarding']['status'] == 'in_progress'
        assert config['onboarding']['path_chosen'] == 'complete_setup'
        assert config['onboarding']['in_progress_skill'] == 'complete-setup'
        assert config['onboarding']['complete_setup_state']['step_completed'] == 1
        assert config['onboarding']['complete_setup_state']['files_uploaded'] is False

        print("[OK] Batch update test passed!")

    finally:
        config_path.unlink()


def test_atomic_writes():
    """Test that writes are atomic (no corruption on failure)."""
    print("\n=== Test 3: Atomic Writes ===")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(create_test_config(), f)

    try:
        # Perform update
        original_content = config_path.read_text()

        result = update_yaml_path(config_path, "onboarding.status", "in_progress")
        assert result, "Update failed"

        # Verify no .tmp file left behind
        tmp_files = list(config_path.parent.glob("*.tmp"))
        assert len(tmp_files) == 0, f"Temp file left behind: {tmp_files}"

        # Verify file is valid YAML
        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        assert isinstance(config, dict), "File corrupted after update"

        print("[OK] No temp files left behind")
        print("[OK] File is valid YAML after update")
        print("[OK] Atomic write test passed!")

    finally:
        config_path.unlink()


def test_backup_creation():
    """Test that backups are created."""
    print("\n=== Test 4: Backup Creation ===")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(create_test_config(), f)

    try:
        # Update with backup enabled (default)
        result = update_yaml_path(config_path, "onboarding.status", "in_progress", create_backup=True)
        assert result, "Update failed"

        # Check for backup file
        backup_files = list(config_path.parent.glob(f"{config_path.stem}.*.backup"))
        assert len(backup_files) > 0, "No backup file created"

        print(f"[OK] Backup created: {backup_files[0].name}")
        print("[OK] Backup creation test passed!")

        # Clean up backups
        for backup in backup_files:
            backup.unlink()

    finally:
        config_path.unlink()


def test_convenience_functions():
    """Test convenience functions."""
    print("\n=== Test 5: Convenience Functions ===")

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(create_test_config(), f)

    try:
        # Test set_onboarding_status
        result = set_onboarding_status(config_path, "in_progress")
        assert result, "set_onboarding_status failed"

        with config_path.open('r') as f:
            config = yaml.safe_load(f)
        assert config['onboarding']['status'] == 'in_progress'
        print("[OK] set_onboarding_status() works")

        # Test invalid status (should fail gracefully)
        result = set_onboarding_status(config_path, "invalid_status")
        assert not result, "Should reject invalid status"
        print("[OK] Validation works (rejected invalid status)")

        print("[OK] Convenience functions test passed!")

    finally:
        config_path.unlink()


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("STATE_WRITER.PY TEST SUITE")
    print("="*60)

    try:
        test_nested_path_update()
        test_multiple_updates()
        test_atomic_writes()
        test_backup_creation()
        test_convenience_functions()

        print("\n" + "="*60)
        print("[OK] ALL TESTS PASSED!")
        print("="*60)
        print("\nstate_writer.py is ready for use.")
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
