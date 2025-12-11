#!/usr/bin/env python3
"""
Unit Tests for bulk-complete.py

Tests coverage:
- File detection (steps.md vs tasks.md)
- Task extraction and counting
- Section parsing (Section X and Phase X formats)
- Range selection parsing
- Bulk completion operations
- Validation and error handling
"""

import sys
import unittest
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path to import the script
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# Import the script module from new bulk-complete skill location
import importlib.util
spec = importlib.util.spec_from_file_location(
    "bulk_complete",
    str(Path(__file__).parent.parent.parent / "bulk-complete" / "scripts" / "bulk-complete.py")
)
bulk_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bulk_module)

# Import functions
find_task_file = bulk_module.find_task_file
extract_tasks = bulk_module.extract_tasks
parse_task_selection = bulk_module.parse_task_selection
extract_section_tasks = bulk_module.extract_section_tasks
count_tasks = bulk_module.count_tasks


class TestFileDetection(unittest.TestCase):
    """Test find_task_file() auto-detection logic"""

    def setUp(self):
        """Create temporary test directory"""
        self.test_dir = tempfile.mkdtemp()
        self.project_path = Path(self.test_dir) / "test-project"
        self.planning_dir = self.project_path / "01-planning"
        self.planning_dir.mkdir(parents=True)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_find_steps_md_when_exists(self):
        """Should prefer steps.md over tasks.md"""
        steps_file = self.planning_dir / "steps.md"
        tasks_file = self.planning_dir / "tasks.md"

        steps_file.write_text("# Steps\n- [ ] Task 1")
        tasks_file.write_text("# Tasks\n- [ ] Task 1")

        result = find_task_file(self.project_path)
        self.assertEqual(result, steps_file)
        self.assertEqual(result.name, "steps.md")

    def test_find_tasks_md_when_only_tasks_exists(self):
        """Should fall back to tasks.md if steps.md doesn't exist"""
        tasks_file = self.planning_dir / "tasks.md"
        tasks_file.write_text("# Tasks\n- [ ] Task 1")

        result = find_task_file(self.project_path)
        self.assertEqual(result, tasks_file)
        self.assertEqual(result.name, "tasks.md")

    def test_find_none_when_neither_exists(self):
        """Should return None if neither file exists"""
        result = find_task_file(self.project_path)
        self.assertIsNone(result)

    def test_find_steps_only(self):
        """Should find steps.md when it's the only file"""
        steps_file = self.planning_dir / "steps.md"
        steps_file.write_text("# Steps\n- [ ] Task 1")

        result = find_task_file(self.project_path)
        self.assertEqual(result, steps_file)


class TestTaskExtraction(unittest.TestCase):
    """Test extract_tasks() functionality"""

    def test_extract_simple_uncompleted_tasks(self):
        """Should extract uncompleted tasks correctly"""
        content = """
# Project Steps
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
"""
        tasks = extract_tasks(content)
        self.assertEqual(len(tasks), 3)
        self.assertEqual(tasks[0][0], 1)  # task_num
        self.assertEqual(tasks[0][2], "Task 1")  # task_text
        self.assertFalse(tasks[0][3])  # is_completed

    def test_extract_mixed_completed_uncompleted(self):
        """Should handle mix of completed and uncompleted tasks"""
        content = """
- [ ] Task 1
- [x] Task 2
- [ ] Task 3
- [x] Task 4
"""
        tasks = extract_tasks(content)
        self.assertEqual(len(tasks), 4)
        self.assertFalse(tasks[0][3])  # Task 1 uncompleted
        self.assertTrue(tasks[1][3])   # Task 2 completed
        self.assertFalse(tasks[2][3])  # Task 3 uncompleted
        self.assertTrue(tasks[3][3])   # Task 4 completed

    def test_extract_case_insensitive_completed(self):
        """Should handle [X] and [x] as completed"""
        content = """
- [x] Task 1
- [X] Task 2
"""
        tasks = extract_tasks(content)
        self.assertTrue(tasks[0][3])
        self.assertTrue(tasks[1][3])

    def test_extract_indented_tasks(self):
        """Should handle indented tasks"""
        content = """
## Section 1
- [ ] Task 1
  - [ ] Subtask 1
  - [ ] Subtask 2
"""
        tasks = extract_tasks(content)
        self.assertEqual(len(tasks), 3)

    def test_extract_no_tasks(self):
        """Should return empty list when no tasks found"""
        content = """
# Project Overview
Just some text, no tasks here.
"""
        tasks = extract_tasks(content)
        self.assertEqual(len(tasks), 0)


class TestTaskCounting(unittest.TestCase):
    """Test count_tasks() functionality"""

    def test_count_all_uncompleted(self):
        """Should count uncompleted tasks correctly"""
        content = """
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3
"""
        uncompleted, completed = count_tasks(content)
        self.assertEqual(uncompleted, 3)
        self.assertEqual(completed, 0)

    def test_count_all_completed(self):
        """Should count completed tasks correctly"""
        content = """
- [x] Task 1
- [x] Task 2
"""
        uncompleted, completed = count_tasks(content)
        self.assertEqual(uncompleted, 0)
        self.assertEqual(completed, 2)

    def test_count_mixed(self):
        """Should count mixed tasks correctly"""
        content = """
- [ ] Task 1
- [x] Task 2
- [ ] Task 3
- [x] Task 4
- [x] Task 5
"""
        uncompleted, completed = count_tasks(content)
        self.assertEqual(uncompleted, 2)
        self.assertEqual(completed, 3)


class TestSectionExtraction(unittest.TestCase):
    """Test extract_section_tasks() for both Section and Phase formats"""

    def test_extract_section_format(self):
        """Should extract tasks from Section N format"""
        content = """
## Section 1: Setup
- [ ] Task 1
- [ ] Task 2

## Section 2: Implementation
- [ ] Task 3
- [ ] Task 4

## Section 3: Testing
- [ ] Task 5
"""
        section_2_tasks = extract_section_tasks(content, "2")
        self.assertEqual(section_2_tasks, {3, 4})

    def test_extract_phase_format(self):
        """Should extract tasks from Phase N format (new init_project.py)"""
        content = """
## Phase 1: Setup & Planning
- [ ] Task 1
- [ ] Task 2

## Phase 2: Build
- [ ] Task 3
- [ ] Task 4

## Phase 3: Testing
- [ ] Task 5
"""
        phase_2_tasks = extract_section_tasks(content, "Phase 2")
        self.assertEqual(phase_2_tasks, {3, 4})

    def test_extract_section_with_colon(self):
        """Should handle section headers with colons"""
        content = """
## Section 1: Planning
- [ ] Task 1

## Section 2: Execution
- [ ] Task 2
- [ ] Task 3
"""
        section_1_tasks = extract_section_tasks(content, "Section 1")
        self.assertEqual(section_1_tasks, {1})

    def test_extract_last_section(self):
        """Should extract tasks from last section (no next section)"""
        content = """
## Section 1
- [ ] Task 1

## Section 2
- [ ] Task 2
- [ ] Task 3
"""
        section_2_tasks = extract_section_tasks(content, "2")
        self.assertEqual(section_2_tasks, {2, 3})

    def test_extract_nonexistent_section(self):
        """Should return empty set for nonexistent section"""
        content = """
## Section 1
- [ ] Task 1
"""
        section_99_tasks = extract_section_tasks(content, "99")
        self.assertEqual(section_99_tasks, set())


class TestRangeSelection(unittest.TestCase):
    """Test parse_task_selection() range parsing"""

    def test_parse_single_number(self):
        """Should parse single task number"""
        result = parse_task_selection("5", 10)
        self.assertEqual(result, {5})

    def test_parse_range(self):
        """Should parse task range"""
        result = parse_task_selection("1-5", 10)
        self.assertEqual(result, {1, 2, 3, 4, 5})

    def test_parse_multiple_ranges(self):
        """Should parse multiple ranges and numbers"""
        result = parse_task_selection("1-3,7,10-12", 15)
        self.assertEqual(result, {1, 2, 3, 7, 10, 11, 12})

    def test_parse_out_of_bounds(self):
        """Should ignore out-of-bounds task numbers"""
        result = parse_task_selection("1-5,99", 10)
        self.assertEqual(result, {1, 2, 3, 4, 5})

    def test_parse_invalid_format(self):
        """Should handle invalid formats gracefully"""
        result = parse_task_selection("1-5,abc,7", 10)
        self.assertEqual(result, {1, 2, 3, 4, 5, 7})

    def test_parse_overlapping_ranges(self):
        """Should handle overlapping ranges (no duplicates)"""
        result = parse_task_selection("1-5,3-7", 10)
        self.assertEqual(result, {1, 2, 3, 4, 5, 6, 7})


class TestIntegration(unittest.TestCase):
    """Integration tests with real file structures"""

    def setUp(self):
        """Create temporary test directory with mock projects"""
        self.test_dir = tempfile.mkdtemp()

        # Create mock project with steps.md (new format)
        self.new_project = Path(self.test_dir) / "01-new-project"
        planning = self.new_project / "01-planning"
        planning.mkdir(parents=True)

        (planning / "steps.md").write_text("""
# Project Steps

## Phase 1: Setup
- [ ] Task 1
- [ ] Task 2

## Phase 2: Build
- [ ] Task 3
- [x] Task 4

## Phase 3: Test
- [ ] Task 5
""")

        # Create mock onboarding project with tasks.md (legacy format)
        self.old_project = Path(self.test_dir) / "00-onboarding"
        old_planning = self.old_project / "01-planning"
        old_planning.mkdir(parents=True)

        (old_planning / "tasks.md").write_text("""
# Onboarding Tasks

## Section 0: Welcome
- [x] Task 1

## Section 1: Goals
- [ ] Task 2
- [ ] Task 3
""")

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_dir)

    def test_detect_new_project_format(self):
        """Should detect and use steps.md for new projects"""
        task_file = find_task_file(self.new_project)
        self.assertEqual(task_file.name, "steps.md")

    def test_detect_legacy_format(self):
        """Should detect and use tasks.md for legacy projects"""
        task_file = find_task_file(self.old_project)
        self.assertEqual(task_file.name, "tasks.md")

    def test_count_new_project_tasks(self):
        """Should count tasks correctly in new format"""
        content = (self.new_project / "01-planning" / "steps.md").read_text()
        uncompleted, completed = count_tasks(content)
        self.assertEqual(uncompleted, 4)
        self.assertEqual(completed, 1)

    def test_extract_phase_from_new_project(self):
        """Should extract Phase 2 tasks from new project"""
        content = (self.new_project / "01-planning" / "steps.md").read_text()
        phase_2_tasks = extract_section_tasks(content, "Phase 2")
        self.assertEqual(phase_2_tasks, {3, 4})


def run_tests():
    """Run all test suites"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestFileDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskExtraction))
    suite.addTests(loader.loadTestsFromTestCase(TestTaskCounting))
    suite.addTests(loader.loadTestsFromTestCase(TestSectionExtraction))
    suite.addTests(loader.loadTestsFromTestCase(TestRangeSelection))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
