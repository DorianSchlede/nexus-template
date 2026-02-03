"""
Integration tests for onboarding flow and build creation

Tests the full lifecycle of build creation, validation, and loading.
Created: 2026-02-02
Purpose: Fix Session Quality Issues (Build 02, Phase 3.4)
"""

import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path
from nexus.core.loaders import scan_builds, load_build, validate_build_schema


class TestOnboardingFlow:
    """Integration tests for build creation and loading"""

    @pytest.fixture
    def temp_nexus_dir(self):
        """Create a temporary Nexus directory structure"""
        temp_dir = Path(tempfile.mkdtemp())

        # Create basic Nexus structure
        builds_active = temp_dir / "02-builds" / "active"
        builds_active.mkdir(parents=True)

        yield temp_dir

        # Cleanup
        shutil.rmtree(temp_dir)

    def test_quick_start_creates_valid_build(self, temp_nexus_dir):
        """Test 1: quick-start creates build with valid schema"""
        # Simulate nexus-init-build call (manual creation for test)
        build_name = "test-build"
        build_id = "01-test-build"
        build_dir = temp_nexus_dir / "02-builds" / "active" / build_id
        planning_dir = build_dir / "01-planning"
        planning_dir.mkdir(parents=True)

        # Create 01-overview.md with valid schema
        overview = planning_dir / "01-overview.md"
        overview.write_text("""---
id: 01-test-build
name: Test Build
description: A test build for validation
status: PLANNING
created: 2026-02-02T10:00:00
build_path: 02-builds/active/01-test-build
---

# Test Build

This is a test build for integration testing.
""")

        # Create other required directories
        (build_dir / "02-resources").mkdir()
        (build_dir / "03-working").mkdir()
        (build_dir / "04-outputs").mkdir()

        # Create 04-steps.md with some tasks
        steps = planning_dir / "04-steps.md"
        steps.write_text("""# Execution Steps

- [ ] Task 1
- [ ] Task 2
- [x] Task 3
""")

        # Scan builds
        builds = scan_builds(str(temp_nexus_dir), minimal=True)

        # Verify build was found
        assert len(builds) == 1
        assert builds[0]["id"] == "01-test-build"
        assert builds[0]["name"] == "Test Build"
        assert builds[0]["status"] == "PLANNING"

        # Verify task counts
        assert builds[0]["tasks_total"] == 3
        assert builds[0]["tasks_completed"] == 1
        assert builds[0]["progress"] == pytest.approx(0.333, abs=0.01)

    def test_build_visible_after_resume(self, temp_nexus_dir):
        """Test 2: Build visible in scan after creation (resume scenario)"""
        # Create a build manually
        build_id = "02-resume-test"
        build_dir = temp_nexus_dir / "02-builds" / "active" / build_id
        planning_dir = build_dir / "01-planning"
        planning_dir.mkdir(parents=True)

        overview = planning_dir / "01-overview.md"
        overview.write_text("""---
id: 02-resume-test
name: Resume Test Build
status: IN_PROGRESS
created: 2026-02-02T11:00:00
build_path: 02-builds/active/02-resume-test
---

# Resume Test
""")

        # Create steps file
        steps = planning_dir / "04-steps.md"
        steps.write_text("- [ ] First task\n- [x] Second task")

        # First scan
        builds_before = scan_builds(str(temp_nexus_dir), minimal=True)
        assert len(builds_before) == 1

        # Simulate resume - scan again
        builds_after = scan_builds(str(temp_nexus_dir), minimal=True)
        assert len(builds_after) == 1
        assert builds_after[0]["id"] == "02-resume-test"
        assert builds_after[0]["status"] == "IN_PROGRESS"

        # Test load_build
        build_data = load_build("02-resume-test", str(temp_nexus_dir))
        assert "error" not in build_data
        assert build_data["build_id"] == "02-resume-test"
        assert "01-planning/01-overview.md" in build_data["files"]

    def test_schema_validation_catches_errors(self, temp_nexus_dir):
        """Test 3: Schema validation catches missing required fields"""
        import warnings

        # Test missing fields
        invalid_metadata = {
            "name": "Invalid Build",
            # Missing: id, status, created, build_path
        }

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            validate_build_schema(invalid_metadata, "test.md")

            # Should have warning about missing fields
            assert len(w) == 1
            assert "Missing required fields" in str(w[0].message)
            assert "id" in str(w[0].message)
            assert "status" in str(w[0].message)

        # Test invalid status
        invalid_status = {
            "id": "test",
            "name": "Test",
            "status": "INVALID_STATUS",
            "created": "2026-02-02",
            "build_path": "test/path"
        }

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            validate_build_schema(invalid_status, "test.md")

            # Should have warning about invalid status
            assert len(w) == 1
            assert "Invalid status" in str(w[0].message)

        # Test invalid date format
        invalid_date = {
            "id": "test",
            "name": "Test",
            "status": "PLANNING",
            "created": "not-a-date",
            "build_path": "test/path"
        }

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            validate_build_schema(invalid_date, "test.md")

            # Should have warning about invalid date
            assert len(w) == 1
            assert "Invalid date format" in str(w[0].message)

    def test_case_variations_work(self, temp_nexus_dir):
        """Test 4: Case variations in status field work (Planning, PLANNING, planning)"""
        # Create builds with different case variations
        for i, status in enumerate(["Planning", "PLANNING", "planning", "In_Progress", "ACTIVE"]):
            build_id = f"0{i+3}-case-test-{status.lower()}"
            build_dir = temp_nexus_dir / "02-builds" / "active" / build_id
            planning_dir = build_dir / "01-planning"
            planning_dir.mkdir(parents=True)

            overview = planning_dir / "01-overview.md"
            overview.write_text(f"""---
id: {build_id}
name: Case Test {status}
status: {status}
created: 2026-02-02T12:0{i}:00
build_path: 02-builds/active/{build_id}
---

# Case Test
""")

            steps = planning_dir / "04-steps.md"
            steps.write_text("- [ ] Task 1")

        # Scan all builds
        builds = scan_builds(str(temp_nexus_dir), minimal=True)

        # All 5 builds should be found (case-insensitive matching)
        assert len(builds) == 5

        # Verify all statuses were normalized/accepted
        statuses = [b["status"] for b in builds]
        assert "Planning" in statuses or "PLANNING" in statuses or "planning" in statuses
        assert "In_Progress" in statuses or "IN_PROGRESS" in statuses
        assert "ACTIVE" in statuses or "Active" in statuses


class TestBuildSchema:
    """Test schema validation in isolation"""

    def test_valid_schema_passes(self):
        """Valid schema should not raise warnings"""
        import warnings

        valid_metadata = {
            "id": "01-test",
            "name": "Test Build",
            "status": "PLANNING",
            "created": "2026-02-02T10:00:00",
            "build_path": "02-builds/active/01-test"
        }

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            validate_build_schema(valid_metadata, "test.md")

            # Should have no warnings
            assert len(w) == 0

    def test_all_valid_statuses(self):
        """Test all valid status values are accepted"""
        import warnings

        valid_statuses = ["PLANNING", "IN_PROGRESS", "ACTIVE", "COMPLETE", "ARCHIVED"]

        for status in valid_statuses:
            metadata = {
                "id": "test",
                "name": "Test",
                "status": status,
                "created": "2026-02-02",
                "build_path": "test/path"
            }

            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("always")
                validate_build_schema(metadata, f"test-{status}.md")

                # Should have no warnings for valid statuses
                assert len(w) == 0, f"Status {status} should be valid but got warning"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
