#!/usr/bin/env python3
"""
Unit Tests for init_project.py

Tests coverage:
- Project name sanitization
- Project ID auto-assignment
- Directory structure creation
- Template file generation
- Edge cases and error handling
"""

import sys
import unittest
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path to import the script
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Import functions from init_project.py
from init_project import (
    sanitize_project_name,
    get_next_project_id,
    init_project,
)


class TestProjectNameSanitization(unittest.TestCase):
    """Test sanitize_project_name() edge cases"""

    def test_basic_lowercase(self):
        """Should convert to lowercase"""
        result = sanitize_project_name("MyProject")
        self.assertEqual(result, "myproject")

    def test_spaces_to_hyphens(self):
        """Should replace spaces with hyphens"""
        result = sanitize_project_name("My Cool Project")
        self.assertEqual(result, "my-cool-project")

    def test_special_chars_removed(self):
        """Should remove special characters"""
        result = sanitize_project_name("Project@123!")
        self.assertEqual(result, "project123")

    def test_multiple_hyphens_collapsed(self):
        """Should collapse multiple hyphens"""
        result = sanitize_project_name("my---project")
        self.assertEqual(result, "my-project")

    def test_leading_trailing_hyphens_removed(self):
        """Should remove leading/trailing hyphens"""
        result = sanitize_project_name("-my-project-")
        self.assertEqual(result, "my-project")

    def test_unicode_chars_removed(self):
        """Should remove unicode characters"""
        result = sanitize_project_name("Projet Spécial")
        self.assertEqual(result, "projet-spcial")

    def test_numbers_preserved(self):
        """Should preserve numbers"""
        result = sanitize_project_name("Project 2025 Q1")
        self.assertEqual(result, "project-2025-q1")

    def test_empty_after_sanitization(self):
        """Should handle edge case of name becoming empty"""
        result = sanitize_project_name("@#$%^&*()")
        self.assertEqual(result, "")

    def test_mixed_case_numbers_special(self):
        """Should handle complex mix"""
        result = sanitize_project_name("Lead-Qualification_System v2.0!")
        # Underscore is removed, not converted to hyphen
        self.assertEqual(result, "lead-qualificationsystem-v20")


class TestProjectIDAssignment(unittest.TestCase):
    """Test get_next_project_id() logic"""

    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.projects_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_first_project_id(self):
        """Should return 01 for first project"""
        result = get_next_project_id(self.projects_path)
        self.assertEqual(result, "01")

    def test_sequential_ids(self):
        """Should increment IDs sequentially"""
        # Create mock projects
        (self.projects_path / "01-first-project").mkdir()
        (self.projects_path / "02-second-project").mkdir()

        result = get_next_project_id(self.projects_path)
        self.assertEqual(result, "03")

    def test_non_sequential_ids(self):
        """Should return next ID after highest existing"""
        # Create non-sequential projects
        (self.projects_path / "01-project").mkdir()
        (self.projects_path / "05-project").mkdir()
        (self.projects_path / "03-project").mkdir()

        result = get_next_project_id(self.projects_path)
        self.assertEqual(result, "06")

    def test_zero_padding(self):
        """Should maintain zero-padding for single digits"""
        (self.projects_path / "01-project").mkdir()

        result = get_next_project_id(self.projects_path)
        self.assertEqual(result, "02")

    def test_double_digit_ids(self):
        """Should handle double-digit IDs correctly"""
        (self.projects_path / "09-project").mkdir()

        result = get_next_project_id(self.projects_path)
        self.assertEqual(result, "10")

    def test_ignore_non_matching_dirs(self):
        """Should ignore directories that don't match NN-name pattern"""
        (self.projects_path / "01-project").mkdir()
        (self.projects_path / "not-a-project").mkdir()
        (self.projects_path / "00-onboarding").mkdir()

        result = get_next_project_id(self.projects_path)
        self.assertEqual(result, "02")

    def test_nonexistent_directory(self):
        """Should return 01 for nonexistent directory"""
        nonexistent = Path(self.test_dir) / "does-not-exist"
        result = get_next_project_id(nonexistent)
        self.assertEqual(result, "01")


class TestProjectInitialization(unittest.TestCase):
    """Test init_project() full workflow"""

    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.projects_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_create_basic_project(self):
        """Should create complete project structure"""
        result = init_project("Test Project", str(self.projects_path))

        self.assertIsNotNone(result)
        self.assertTrue(result.exists())
        self.assertEqual(result.name, "01-test-project")

    def test_create_directory_structure(self):
        """Should create all required directories"""
        result = init_project("Test Project", str(self.projects_path))

        # Check all directories exist
        self.assertTrue((result / "01-planning").exists())
        self.assertTrue((result / "02-resources").exists())
        self.assertTrue((result / "03-working").exists())
        self.assertTrue((result / "04-outputs").exists())

    def test_create_planning_files(self):
        """Should create all planning files from templates"""
        result = init_project("Test Project", str(self.projects_path))

        planning = result / "01-planning"
        self.assertTrue((planning / "overview.md").exists())
        self.assertTrue((planning / "plan.md").exists())
        self.assertTrue((planning / "steps.md").exists())

    def test_overview_contains_project_info(self):
        """Should populate overview.md with project info"""
        result = init_project("Test Project", str(self.projects_path))

        overview_content = (result / "01-planning" / "overview.md").read_text()

        self.assertIn("Test Project", overview_content)
        self.assertIn("01-test-project", overview_content)
        self.assertIn("status: PLANNING", overview_content)

    def test_steps_has_checkbox_tasks(self):
        """Should create steps.md with checkbox tasks"""
        result = init_project("Test Project", str(self.projects_path))

        steps_content = (result / "01-planning" / "steps.md").read_text()

        # Should have multiple checkbox tasks
        self.assertIn("- [ ]", steps_content)
        self.assertIn("Phase", steps_content)

    def test_plan_has_mental_models_section(self):
        """Should include mental models section in plan.md"""
        result = init_project("Test Project", str(self.projects_path))

        plan_content = (result / "01-planning" / "plan.md").read_text()

        self.assertIn("Mental Models", plan_content)
        self.assertIn("Socratic Questioning", plan_content)
        self.assertIn("Devil's Advocate", plan_content)

    def test_sequential_projects(self):
        """Should assign sequential IDs to multiple projects"""
        project1 = init_project("First Project", str(self.projects_path))
        project2 = init_project("Second Project", str(self.projects_path))

        self.assertEqual(project1.name, "01-first-project")
        self.assertEqual(project2.name, "02-second-project")

    def test_duplicate_project_name(self):
        """Should fail gracefully if project already exists"""
        # Create first project
        result1 = init_project("Test Project", str(self.projects_path))
        self.assertIsNotNone(result1)
        self.assertEqual(result1.name, "01-test-project")

        # Create second project with same name - gets different ID
        result2 = init_project("Test Project", str(self.projects_path))
        self.assertIsNotNone(result2)
        self.assertEqual(result2.name, "02-test-project")

        # Note: Script allows same name with different IDs
        # This is intentional - ID is auto-assigned

    def test_invalid_project_name(self):
        """Should fail gracefully with invalid name"""
        result = init_project("@#$%^&*()", str(self.projects_path))
        self.assertIsNone(result)

    def test_complex_project_name(self):
        """Should handle complex project names"""
        result = init_project("Lead Qualification System v2.0", str(self.projects_path))

        self.assertIsNotNone(result)
        self.assertEqual(result.name, "01-lead-qualification-system-v20")


class TestTemplateContent(unittest.TestCase):
    """Test template file content generation"""

    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.projects_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_overview_has_yaml_frontmatter(self):
        """Should have valid YAML frontmatter"""
        result = init_project("Test Project", str(self.projects_path))
        content = (result / "01-planning" / "overview.md").read_text()

        # Check frontmatter structure
        self.assertTrue(content.startswith("---\n"))
        self.assertIn("\nid:", content)
        self.assertIn("\nname:", content)
        self.assertIn("\nstatus:", content)
        self.assertIn("\ndescription:", content)
        self.assertIn("\ncreated:", content)

    def test_steps_has_all_phases(self):
        """Should have Phase 1-4 in steps.md"""
        result = init_project("Test Project", str(self.projects_path))
        content = (result / "01-planning" / "steps.md").read_text()

        self.assertIn("## Phase 1:", content)
        self.assertIn("## Phase 2:", content)
        self.assertIn("## Phase 3:", content)
        self.assertIn("## Phase 4:", content)

    def test_plan_has_dependencies_section(self):
        """Should have Dependencies & Links section"""
        result = init_project("Test Project", str(self.projects_path))
        content = (result / "01-planning" / "plan.md").read_text()

        self.assertIn("## Dependencies & Links", content)
        self.assertIn("Files Impacted", content)
        self.assertIn("External Systems", content)

    def test_all_files_have_content(self):
        """Should not create empty files"""
        result = init_project("Test Project", str(self.projects_path))

        overview = (result / "01-planning" / "overview.md").read_text()
        plan = (result / "01-planning" / "plan.md").read_text()
        steps = (result / "01-planning" / "steps.md").read_text()

        self.assertGreater(len(overview), 500)
        self.assertGreater(len(plan), 500)
        self.assertGreater(len(steps), 500)


def run_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestProjectNameSanitization))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectIDAssignment))
    suite.addTests(loader.loadTestsFromTestCase(TestProjectInitialization))
    suite.addTests(loader.loadTestsFromTestCase(TestTemplateContent))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
