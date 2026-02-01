"""
Comprehensive validation that all 3 blockers are resolved.

Tests:
1. Blocker #1: state_writer.py works and can be imported
2. Blocker #2: setup-system renamed to complete-setup everywhere
3. Blocker #3: migrate.py works and integrates with session_start.py

Run with: python3 00-system/core/nexus/test_blockers_resolved.py
"""

import sys
import yaml
import tempfile
from pathlib import Path


def test_blocker_1_state_writer():
    """Test Blocker #1: Generic YAML Config Updater."""
    print("\n" + "="*60)
    print("BLOCKER #1: state_writer.py")
    print("="*60)

    # Test 1: Can import
    print("\n1. Testing import...")
    try:
        from state_writer import update_yaml_path, update_multiple_paths
        print("[OK] state_writer.py can be imported")
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False

    # Test 2: Can update nested paths
    print("\n2. Testing nested path updates...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        test_config = {
            'onboarding': {
                'status': 'not_started'
            }
        }
        yaml.dump(test_config, f)

    try:
        # Update nested path
        result = update_yaml_path(config_path, "onboarding.path_chosen", "quick_start")
        if not result:
            print("[ERROR] update_yaml_path failed")
            return False

        # Verify
        with config_path.open('r') as f:
            updated = yaml.safe_load(f)

        if updated['onboarding']['path_chosen'] != 'quick_start':
            print(f"[ERROR] Value not updated correctly: {updated}")
            return False

        print("[OK] Nested path updates work")

    finally:
        config_path.unlink()

    # Test 3: Batch updates
    print("\n3. Testing batch updates...")
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(test_config, f)

    try:
        updates = {
            "onboarding.status": "in_progress",
            "onboarding.path_chosen": "complete_setup",
            "onboarding.complete_setup_state.step_completed": 2
        }
        result = update_multiple_paths(config_path, updates)

        if not result:
            print("[ERROR] update_multiple_paths failed")
            return False

        with config_path.open('r') as f:
            updated = yaml.safe_load(f)

        if updated['onboarding']['status'] != 'in_progress':
            print("[ERROR] Batch update failed (status)")
            return False
        if updated['onboarding']['complete_setup_state']['step_completed'] != 2:
            print("[ERROR] Batch update failed (step_completed)")
            return False

        print("[OK] Batch updates work")

    finally:
        config_path.unlink()

    print("\n[OK] BLOCKER #1 RESOLVED")
    return True


def test_blocker_2_skill_rename():
    """Test Blocker #2: Skill Rename."""
    print("\n" + "="*60)
    print("BLOCKER #2: setup-system -> complete-setup rename")
    print("="*60)

    # Get workspace root
    base_path = Path("/Users/dorian/Library/CloudStorage/GoogleDrive-schlede.dorian@gmail.com/Other computers/My Laptop/Nexus Instances/Nexus-v5-base")

    # Test 1: Directory renamed
    print("\n1. Checking directory rename...")
    old_dir = base_path / "00-system" / "skills" / "learning" / "setup-system"
    new_dir = base_path / "00-system" / "skills" / "learning" / "complete-setup"

    if old_dir.exists():
        print(f"[ERROR] Old directory still exists: {old_dir}")
        return False

    if not new_dir.exists():
        print(f"[ERROR] New directory doesn't exist: {new_dir}")
        return False

    print(f"[OK] Directory renamed correctly")

    # Test 2: No references to old name in critical files
    print("\n2. Checking file references...")

    critical_files = [
        ".claude/hooks/session_start.py",
        ".claude/hooks/templates/compact_onboarding_resume.md",
        ".claude/hooks/templates/startup_first_run.md",
        "00-system/core/nexus/templates/user-config.yaml",
        "00-system/core/nexus/loaders.py",
        "00-system/skills/learning/complete-setup/SKILL.md"
    ]

    for rel_path in critical_files:
        file_path = base_path / rel_path
        if not file_path.exists():
            print(f"[!]  Warning: Expected file doesn't exist: {rel_path}")
            continue

        content = file_path.read_text(encoding='utf-8', errors='ignore')

        if 'setup-system' in content or 'setup_system' in content:
            print(f"[ERROR] Found old references in: {rel_path}")
            # Show where
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'setup-system' in line or 'setup_system' in line:
                    print(f"   Line {i}: {line.strip()[:80]}")
            return False

    print(f"[OK] All references updated ({len(critical_files)} files checked)")

    print("\n[OK] BLOCKER #2 RESOLVED")
    return True


def test_blocker_3_migration():
    """Test Blocker #3: Schema Migration."""
    print("\n" + "="*60)
    print("BLOCKER #3: Schema Migration (v4 -> v5)")
    print("="*60)

    # Test 1: Can import
    print("\n1. Testing import...")
    try:
        from migrate import migrate_if_needed, migrate_v4_to_v5, validate_v5_schema
        print("[OK] migrate.py can be imported")
    except ImportError as e:
        print(f"[ERROR] Import failed: {e}")
        return False

    # Test 2: Migration works
    print("\n2. Testing migration...")
    v4_config = {
        'user_preferences': {
            'language': 'de'
        },
        'onboarding': {
            'status': 'setup_in_progress',
            'in_progress_skill': 'setup-system',
            'chosen_path': 'direct',
            'setup_system_state': {
                'step_completed': 2,
                'files_uploaded': True,
                'file_analysis_done': False,
                'role_captured': False,
                'goals_captured': False,
                'roadmap_created': False,
                'workspace_created': False,
                'projects_initiated': False
            }
        }
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        config_path = Path(f.name)
        yaml.dump(v4_config, f)

    try:
        # Migrate
        result = migrate_if_needed(config_path)

        if not result:
            print("[ERROR] Migration failed or was skipped")
            return False

        # Verify migration
        with config_path.open('r') as f:
            migrated = yaml.safe_load(f)

        # Check schema version
        if migrated.get('schema_version') != '5.0':
            print(f"[ERROR] schema_version not set: {migrated.get('schema_version')}")
            return False

        # Check rename
        if 'setup_system_state' in migrated['onboarding']:
            print("[ERROR] Old field still exists")
            return False

        if 'complete_setup_state' not in migrated['onboarding']:
            print("[ERROR] New field not created")
            return False

        # Check skill name update
        if migrated['onboarding']['in_progress_skill'] != 'complete-setup':
            print(f"[ERROR] Skill name not updated: {migrated['onboarding']['in_progress_skill']}")
            return False

        # Validate
        is_valid, errors = validate_v5_schema(migrated)
        if not is_valid:
            print(f"[ERROR] Validation failed: {errors}")
            return False

        print("[OK] Migration works correctly")

    finally:
        config_path.unlink()

    # Test 3: Integration with session_start.py
    print("\n3. Checking session_start.py integration...")
    base_path = Path("/Users/dorian/Library/CloudStorage/GoogleDrive-schlede.dorian@gmail.com/Other computers/My Laptop/Nexus Instances/Nexus-v5-base")
    session_start_path = base_path / ".claude" / "hooks" / "session_start.py"

    if not session_start_path.exists():
        print(f"[!]  Warning: session_start.py not found at {session_start_path}")
        print("   (This is OK if running tests outside workspace)")
    else:
        content = session_start_path.read_text()

        if 'from nexus.migrate import migrate_if_needed' not in content:
            print("[ERROR] Migration not imported in session_start.py")
            return False

        if 'migrate_if_needed(config_path' not in content:
            print("[ERROR] migrate_if_needed not called in session_start.py")
            return False

        print("[OK] Integrated into session_start.py")

    print("\n[OK] BLOCKER #3 RESOLVED")
    return True


def run_all_validations():
    """Run all blocker validation tests."""
    print("="*60)
    print("BLOCKER RESOLUTION VALIDATION")
    print("="*60)
    print("\nValidating that all 3 blockers are resolved:")
    print("1. Generic YAML Config Updater (state_writer.py)")
    print("2. Skill Rename (setup-system -> complete-setup)")
    print("3. Schema Migration (migrate.py)")

    results = {
        "Blocker #1": test_blocker_1_state_writer(),
        "Blocker #2": test_blocker_2_skill_rename(),
        "Blocker #3": test_blocker_3_migration()
    }

    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    all_passed = True
    for blocker, passed in results.items():
        status = "[OK] RESOLVED" if passed else "[ERROR] FAILED"
        print(f"{blocker}: {status}")
        if not passed:
            all_passed = False

    print("="*60)

    if all_passed:
        print("\n🎉 ALL BLOCKERS RESOLVED!")
        print("\nYou can now proceed with Phase 1 implementation:")
        print("  1. Update startup_first_run.md (fork decision)")
        print("  2. Create quick-start skill")
        print("  3. Update complete-setup skill")
        print("  4. Update state schema in user-config.yaml")
        print("  5. Update session start routing")
        return True
    else:
        print("\n[!]  SOME BLOCKERS STILL UNRESOLVED")
        print("Review the errors above and fix before proceeding.")
        return False


if __name__ == "__main__":
    success = run_all_validations()
    sys.exit(0 if success else 1)
