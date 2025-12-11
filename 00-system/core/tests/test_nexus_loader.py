import unittest
import os
import sys
import tempfile
import shutil
import yaml
from pathlib import Path

# Add parent directory to path to import nexus-loader
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import importlib.util

# Import nexus-loader dynamically to handle the hyphen in filename
spec = importlib.util.spec_from_file_location("nexus_loader", os.path.abspath(os.path.join(os.path.dirname(__file__), '../nexus-loader.py')))
nexus_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nexus_loader)

class TestNexusLoader(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for the Nexus workspace
        self.test_dir = tempfile.mkdtemp()
        self.base_path = Path(self.test_dir)
        
        # Setup directory structure
        (self.base_path / "00-system" / "core").mkdir(parents=True)
        (self.base_path / "00-system" / "skills").mkdir(parents=True)
        (self.base_path / "01-memory").mkdir(parents=True)
        (self.base_path / "02-projects").mkdir(parents=True)
        (self.base_path / "03-skills").mkdir(parents=True)

    def tearDown(self):
        # Remove temporary directory
        shutil.rmtree(self.test_dir)

    def create_dummy_project(self, pid, name, status="IN_PROGRESS", tasks_total=5, tasks_done=2):
        project_dir = self.base_path / "02-projects" / f"{pid}-{name.lower().replace(' ', '-')}"
        planning_dir = project_dir / "01-planning"
        planning_dir.mkdir(parents=True)
        
        # Create overview.md
        overview_content = f"""---
id: "{pid}"
name: "{name}"
status: "{status}"
created: "2025-01-01"
updated: "2025-01-02"
description: "This is a test project.\\nIt has multiple lines."
---
# Overview
"""
        (planning_dir / "overview.md").write_text(overview_content, encoding='utf-8')
        
        # Create steps.md
        steps_content = "# Steps\n\n"
        for i in range(tasks_done):
            steps_content += f"- [x] Task {i+1}\n"
        for i in range(tasks_total - tasks_done):
            steps_content += f"- [ ] Task {tasks_done + i + 1}\n"
            
        (planning_dir / "steps.md").write_text(steps_content, encoding='utf-8')

    def create_dummy_skill(self, name, is_system=False):
        if is_system:
            skill_dir = self.base_path / "00-system" / "skills" / name
        else:
            skill_dir = self.base_path / "03-skills" / name
            
        skill_dir.mkdir(parents=True)
        
        content = f"""---
name: "{name}"
description: "This is a test skill.\\nIt helps with testing."
triggers:
  - "test {name}"
---
# Skill
"""
        (skill_dir / "SKILL.md").write_text(content, encoding='utf-8')

    def test_extract_yaml_frontmatter(self):
        file_path = self.base_path / "test.md"
        file_path.write_text("---\nkey: value\nlist:\n  - item1\n---\n# Content", encoding='utf-8')
        
        data = nexus_loader.extract_yaml_frontmatter(str(file_path))
        self.assertEqual(data['key'], 'value')
        self.assertEqual(data['list'], ['item1'])

    def test_count_checkboxes(self):
        file_path = self.base_path / "steps.md"
        content = """
        - [x] Done 1
        - [X] Done 2
        - [ ] Todo 1
        - [ ] Todo 2
        - [ ] Todo 3
        """
        file_path.write_text(content, encoding='utf-8')
        
        total, completed, uncompleted = nexus_loader.count_checkboxes(file_path)
        self.assertEqual(total, 5)
        self.assertEqual(completed, 2)
        self.assertEqual(uncompleted, 3)

    def test_scan_projects_minimal(self):
        self.create_dummy_project("01", "Test Project")
        
        projects = nexus_loader.scan_projects(str(self.base_path), minimal=True)
        self.assertEqual(len(projects), 1)
        p = projects[0]
        
        # Check minimal fields
        self.assertEqual(p['id'], "01")
        self.assertEqual(p['name'], "Test Project")
        self.assertEqual(p['tasks_completed'], 2)
        self.assertEqual(p['tasks_total'], 5)
        self.assertEqual(p['progress'], 0.4)
        self.assertEqual(p['current_task'], "Task 3")
        
        # Verify description is NOT truncated (per user request)
        self.assertEqual(p['description'], "This is a test project.\nIt has multiple lines.")
        
        # Verify date fields are present (for sorting)
        self.assertIn('created', p)
        self.assertIn('updated', p)

    def test_scan_projects_full(self):
        self.create_dummy_project("01", "Test Project")
        
        projects = nexus_loader.scan_projects(str(self.base_path), minimal=False)
        self.assertEqual(len(projects), 1)
        p = projects[0]
        
        # Full metadata should include everything
        self.assertEqual(p['id'], "01")
        self.assertEqual(p['description'], "This is a test project.\nIt has multiple lines.")

    def test_scan_skills(self):
        self.create_dummy_skill("user-skill", is_system=False)
        self.create_dummy_skill("system-skill", is_system=True)
        
        skills = nexus_loader.scan_skills(str(self.base_path), minimal=True)
        self.assertEqual(len(skills), 2)
        
        names = [s['name'] for s in skills]
        self.assertIn("user-skill", names)
        self.assertIn("system-skill", names)

    def test_startup_first_time(self):
        # No goals.md exists - smart defaults are created
        result = nexus_loader.load_startup(str(self.base_path))
        self.assertEqual(result['system_state'], 'first_time_with_defaults')
        self.assertEqual(result['instructions']['action'], 'display_menu')
        self.assertTrue(result['instructions'].get('suggest_onboarding', False))

    def test_startup_operational(self):
        # Create goals.md
        (self.base_path / "01-memory" / "goals.md").write_text("# Goals", encoding='utf-8')
        
        result = nexus_loader.load_startup(str(self.base_path))
        self.assertEqual(result['system_state'], 'operational')
        self.assertEqual(result['instructions']['action'], 'display_menu')

    def test_startup_onboarding_project_treated_as_regular(self):
        # Onboarding is now skill-based (via learning_tracker in user-config.yaml)
        # Projects with onboarding: true are treated as regular IN_PROGRESS projects
        (self.base_path / "01-memory" / "goals.md").write_text("# Goals", encoding='utf-8')

        # Create an incomplete project with legacy onboarding flag
        project_dir = self.base_path / "02-projects" / "00-onboarding" / "01-first-project"
        (project_dir / "01-planning").mkdir(parents=True)

        overview_content = """---
id: "01-first-project"
name: "First Project"
onboarding: true
status: "IN_PROGRESS"
---
"""
        (project_dir / "01-planning" / "overview.md").write_text(overview_content, encoding='utf-8')

        # Create steps with incomplete tasks
        steps_content = "- [x] Done\n- [ ] Not Done"
        (project_dir / "01-planning" / "steps.md").write_text(steps_content, encoding='utf-8')

        result = nexus_loader.load_startup(str(self.base_path))

        # Should be treated as operational with active projects (not forced onboarding)
        self.assertEqual(result['system_state'], 'operational_with_active_projects')
        self.assertEqual(result['instructions']['action'], 'display_menu')

    def test_startup_onboarding_complete_active_project(self):
        # Create goals.md
        (self.base_path / "01-memory" / "goals.md").write_text("# Goals", encoding='utf-8')
        
        # Create a COMPLETED onboarding project
        onboarding_dir = self.base_path / "02-projects" / "00-onboarding" / "01-first-project"
        (onboarding_dir / "01-planning").mkdir(parents=True)
        
        # Mark as 100% complete in steps.md
        (onboarding_dir / "01-planning" / "overview.md").write_text("---\nid: '01'\nonboarding: true\nstatus: 'COMPLETE'\n---\n", encoding='utf-8')
        (onboarding_dir / "01-planning" / "steps.md").write_text("- [x] Done 1\n- [x] Done 2", encoding='utf-8')
        
        # Create an ACTIVE normal project
        self.create_dummy_project("05", "Active Work", status="IN_PROGRESS")
        
        result = nexus_loader.load_startup(str(self.base_path))
        
        self.assertEqual(result['system_state'], 'operational_with_active_projects')
        self.assertEqual(result['instructions']['action'], 'display_menu')
        self.assertIn("05", result['instructions']['reason'])

    def test_startup_onboarding_complete_no_active(self):
        # Create goals.md
        (self.base_path / "01-memory" / "goals.md").write_text("# Goals", encoding='utf-8')
        
        # Create a COMPLETED onboarding project
        onboarding_dir = self.base_path / "02-projects" / "00-onboarding" / "01-first-project"
        (onboarding_dir / "01-planning").mkdir(parents=True)
        
        (onboarding_dir / "01-planning" / "overview.md").write_text("---\nid: '01'\nonboarding: true\nstatus: 'COMPLETE'\n---\n", encoding='utf-8')
        (onboarding_dir / "01-planning" / "steps.md").write_text("- [x] Done 1\n- [x] Done 2", encoding='utf-8')
        
        result = nexus_loader.load_startup(str(self.base_path))
        
        self.assertEqual(result['system_state'], 'operational')
        self.assertEqual(result['instructions']['action'], 'display_menu')

    # --- NEW TESTS FOR ULTRATHINK COVERAGE ---

    def test_load_project_success(self):
        self.create_dummy_project("01", "My Project")
        
        # Create an output file to test listing
        outputs_dir = self.base_path / "02-projects" / "01-my-project" / "03-outputs"
        outputs_dir.mkdir(parents=True)
        (outputs_dir / "final_report.md").write_text("# Report", encoding='utf-8')
        
        result = nexus_loader.load_project("01", str(self.base_path))
        
        self.assertEqual(result['project_id'], "01")
        self.assertIn('01-planning/overview.md', result['files'])
        self.assertIn('01-planning/steps.md', result['files'])
        self.assertIn('final_report.md', result['outputs'])

    def test_load_project_not_found(self):
        result = nexus_loader.load_project("99", str(self.base_path))
        self.assertIn('error', result)

    def test_load_skill_success(self):
        self.create_dummy_skill("test-skill")
        result = nexus_loader.load_skill("test-skill", str(self.base_path))
        
        self.assertEqual(result['skill_name'], "test-skill")
        self.assertIn('SKILL.md', result['files'])

    def test_load_skill_autoloading(self):
        # Create a skill with auto-loading configuration
        skill_dir = self.base_path / "03-skills" / "complex-skill"
        skill_dir.mkdir(parents=True)
        (skill_dir / "references").mkdir()
        (skill_dir / "scripts").mkdir()
        
        # Create the files to be loaded
        (skill_dir / "references" / "ref1.md").write_text("# Ref", encoding='utf-8')
        (skill_dir / "scripts" / "script1.py").write_text("print('hi')", encoding='utf-8')
        
        # SKILL.md with auto-load config
        skill_content = """---
name: complex-skill
load_references:
  - ref1.md
load_scripts:
  - script1.py
---
"""
        (skill_dir / "SKILL.md").write_text(skill_content, encoding='utf-8')
        
        result = nexus_loader.load_skill("complex-skill", str(self.base_path))
        
        # Verify auto-loaded files are in the 'files' dict
        self.assertIn('references/ref1.md', result['files'])
        self.assertIn('scripts/script1.py', result['files'])
        self.assertIn('ref1.md', result['references_loaded'])
        self.assertIn('script1.py', result['scripts_loaded'])

    def test_malformed_yaml(self):
        file_path = self.base_path / "bad.md"
        # YAML forbids tabs - this should definitely fail
        file_path.write_text("---\nkey: value\n\tindent_error: value\n---\n", encoding='utf-8')
        
        data = nexus_loader.extract_yaml_frontmatter(str(file_path))
        self.assertIn('error', data)

    def test_missing_steps_file(self):
        # Project with overview but no steps.md
        project_dir = self.base_path / "02-projects" / "02-ghost" / "01-planning"
        project_dir.mkdir(parents=True)
        (project_dir / "overview.md").write_text("---\nid: 02\nname: Ghost\n---\n", encoding='utf-8')
        
        # Should not crash
        projects = nexus_loader.scan_projects(str(self.base_path))
        self.assertEqual(len(projects), 1)
        self.assertEqual(projects[0]['tasks_total'], 0)

    def test_token_estimation(self):
        text = "1234" * 100  # 400 chars
        tokens = nexus_loader.estimate_tokens(text)
        self.assertEqual(tokens, 100)  # 4 chars per token

if __name__ == '__main__':
    unittest.main()
