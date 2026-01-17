#!/usr/bin/env python3
"""
Tests for nexus-loader.py

Run with: python -m pytest test_nexus_loader.py -v
Or simply: python test_nexus_loader.py
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path
from unittest import TestCase, main

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from importlib import import_module

# Import the module (handles hyphen in filename)
import importlib.util
spec = importlib.util.spec_from_file_location("nexus_loader", Path(__file__).parent / "nexus-loader.py")
nexus_loader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nexus_loader)


class TestPendingOnboarding(TestCase):
    """Test the pending_onboarding feature in nexus-loader"""

    def setUp(self):
        """Create a temporary Nexus workspace for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.base_path = Path(self.test_dir)

        # Create minimal Nexus structure
        (self.base_path / "00-system" / "core").mkdir(parents=True)
        (self.base_path / "00-system" / "skills" / "learning").mkdir(parents=True)
        (self.base_path / "01-memory").mkdir(parents=True)
        (self.base_path / "02-builds").mkdir(parents=True)
        (self.base_path / "03-skills").mkdir(parents=True)
        (self.base_path / "04-workspace").mkdir(parents=True)

        # Create system-map.md (mandatory)
        (self.base_path / "00-system" / "system-map.md").write_text("# System Map\nTest file")

        # Create memory-map.md
        (self.base_path / "01-memory" / "memory-map.md").write_text("# Memory Map\nTest file")

        # Create goals.md with smart_default
        (self.base_path / "01-memory" / "goals.md").write_text(
            "---\nsmart_default: true\n---\n# Goals\nTest"
        )

        # Create default user-config.yaml (all onboarding incomplete)
        self.user_config_path = self.base_path / "01-memory" / "user-config.yaml"
        self.write_user_config(all_complete=False)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def write_user_config(self, all_complete=False, completed_skills=None):
        """Helper to write user-config.yaml with specific completion states"""
        if completed_skills is None:
            completed_skills = {}

        defaults = {
            'setup_goals': all_complete,
            'setup_workspace': all_complete,
            'learn_integrations': all_complete,
            'learn_builds': all_complete,
            'learn_skills': all_complete,
            'learn_nexus': all_complete,
        }
        defaults.update(completed_skills)

        config = f"""---
smart_default: true
user_preferences:
  language: ""
  timezone: ""
learning_tracker:
  session_count: 0
  completed:
    setup_goals: {str(defaults['setup_goals']).lower()}
    setup_workspace: {str(defaults['setup_workspace']).lower()}
    learn_integrations: {str(defaults['learn_integrations']).lower()}
    learn_builds: {str(defaults['learn_builds']).lower()}
    learn_skills: {str(defaults['learn_skills']).lower()}
    learn_nexus: {str(defaults['learn_nexus']).lower()}
---
"""
        self.user_config_path.write_text(config)

    def test_all_onboarding_pending_when_none_complete(self):
        """When no onboarding is complete, all 6 skills should be in pending_onboarding"""
        self.write_user_config(all_complete=False)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        self.assertEqual(len(pending), 6, "Should have 6 pending onboarding skills")

        # Check all expected skills are present
        pending_keys = {item['key'] for item in pending}
        expected_keys = {'setup_goals', 'setup_workspace', 'learn_integrations',
                        'learn_builds', 'learn_skills', 'learn_nexus'}
        self.assertEqual(pending_keys, expected_keys)

        # Should NOT be complete
        self.assertFalse(stats.get('onboarding_complete', True))

    def test_no_pending_when_all_complete(self):
        """When all onboarding is complete, pending_onboarding should be empty"""
        self.write_user_config(all_complete=True)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        self.assertEqual(len(pending), 0, "Should have 0 pending onboarding skills")

        # Should be complete
        self.assertTrue(stats.get('onboarding_complete', False))

    def test_partial_completion(self):
        """When some skills are complete, only incomplete ones should be pending"""
        self.write_user_config(completed_skills={
            'setup_goals': True,
            'setup_workspace': True,
            'learn_builds': True,
        })

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        self.assertEqual(len(pending), 3, "Should have 3 pending onboarding skills")

        # Check correct skills are pending
        pending_keys = {item['key'] for item in pending}
        expected_keys = {'learn_integrations', 'learn_skills', 'learn_nexus'}
        self.assertEqual(pending_keys, expected_keys)

        # Should NOT be complete
        self.assertFalse(stats.get('onboarding_complete', True))

    def test_pending_onboarding_has_required_fields(self):
        """Each pending item should have key, name, trigger, priority, time"""
        self.write_user_config(all_complete=False)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        required_fields = {'key', 'name', 'trigger', 'priority', 'time'}

        for item in pending:
            item_fields = set(item.keys())
            self.assertTrue(
                required_fields.issubset(item_fields),
                f"Item {item.get('key')} missing fields. Has: {item_fields}, needs: {required_fields}"
            )

    def test_priority_values(self):
        """Check that priority values are correct for each skill"""
        self.write_user_config(all_complete=False)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        priorities = {item['key']: item['priority'] for item in pending}

        # setup_goals should be critical
        self.assertEqual(priorities.get('setup_goals'), 'critical')

        # learn_nexus should be medium
        self.assertEqual(priorities.get('learn_nexus'), 'medium')

        # Others should be high
        for key in ['setup_workspace', 'learn_builds', 'learn_skills', 'learn_integrations']:
            self.assertEqual(priorities.get(key), 'high', f"{key} should have high priority")

    def test_trigger_values(self):
        """Check that trigger values match expected commands"""
        self.write_user_config(all_complete=False)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        triggers = {item['key']: item['trigger'] for item in pending}

        expected_triggers = {
            'setup_goals': 'setup goals',
            'setup_workspace': 'setup workspace',
            'learn_builds': 'learn builds',
            'learn_skills': 'learn skills',
            'learn_integrations': 'learn integrations',
            'learn_nexus': 'learn nexus',
        }

        for key, expected in expected_triggers.items():
            self.assertEqual(triggers.get(key), expected, f"Trigger for {key} should be '{expected}'")

    def test_learning_completed_still_in_stats(self):
        """The learning_completed dict should still be in stats for backward compatibility"""
        self.write_user_config(completed_skills={'setup_goals': True, 'learn_builds': True})

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        learning_completed = stats.get('learning_completed', {})
        self.assertTrue(learning_completed.get('setup_goals'))
        self.assertTrue(learning_completed.get('learn_builds'))
        self.assertFalse(learning_completed.get('setup_workspace'))

    def test_missing_user_config_defaults_to_all_pending(self):
        """If user-config.yaml is missing, all onboarding should be pending"""
        # Remove user-config.yaml
        self.user_config_path.unlink()

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        pending = stats.get('pending_onboarding', [])
        self.assertEqual(len(pending), 6, "Should default to all 6 pending when config missing")
        self.assertFalse(stats.get('onboarding_complete', True))

    def test_malformed_user_config_defaults_gracefully(self):
        """If user-config.yaml is malformed, should default gracefully"""
        # Write malformed YAML
        self.user_config_path.write_text("not valid yaml: {{{{")

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        # Should still return defaults without crashing
        pending = stats.get('pending_onboarding', [])
        self.assertEqual(len(pending), 6, "Should default to all 6 pending when config malformed")


class TestDisplayHints(TestCase):
    """Test the display_hints feature in nexus-loader"""

    def setUp(self):
        """Create a temporary Nexus workspace for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.base_path = Path(self.test_dir)

        # Create minimal Nexus structure
        (self.base_path / "00-system" / "core").mkdir(parents=True)
        (self.base_path / "00-system" / "skills").mkdir(parents=True)
        (self.base_path / "01-memory").mkdir(parents=True)
        (self.base_path / "02-builds").mkdir(parents=True)
        (self.base_path / "03-skills").mkdir(parents=True)
        (self.base_path / "04-workspace").mkdir(parents=True)

        (self.base_path / "00-system" / "system-map.md").write_text("# System Map\nTest file")
        (self.base_path / "01-memory" / "memory-map.md").write_text("# Memory Map\nTest file")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_display_hints_exists_in_stats(self):
        """display_hints should always be present in stats"""
        # Create goals with smart_default
        (self.base_path / "01-memory" / "goals.md").write_text(
            "---\nsmart_default: true\n---\n# Goals"
        )

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        self.assertIn('display_hints', stats)
        self.assertIsInstance(stats['display_hints'], list)

    def test_display_hints_shows_onboarding_incomplete(self):
        """display_hints should include ONBOARDING_INCOMPLETE when skills pending"""
        (self.base_path / "01-memory" / "goals.md").write_text(
            "---\nsmart_default: true\n---\n# Goals"
        )
        # Default user-config has all onboarding incomplete
        config = """---
smart_default: true
learning_tracker:
  completed:
    setup_goals: false
    setup_workspace: false
    learn_integrations: false
    learn_builds: false
    learn_skills: false
    learn_nexus: false
---
"""
        (self.base_path / "01-memory" / "user-config.yaml").write_text(config)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        hints = result.get('stats', {}).get('display_hints', [])

        onboarding_hints = [h for h in hints if 'ONBOARDING_INCOMPLETE' in h]
        self.assertEqual(len(onboarding_hints), 1)
        self.assertIn('6 skills pending', onboarding_hints[0])

    def test_display_hints_shows_setup_goals_prompt(self):
        """display_hints should include PROMPT_SETUP_GOALS when goals not personalized"""
        (self.base_path / "01-memory" / "goals.md").write_text(
            "---\nsmart_default: true\n---\n# Goals"
        )

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        hints = result.get('stats', {}).get('display_hints', [])

        goals_hints = [h for h in hints if 'PROMPT_SETUP_GOALS' in h]
        self.assertEqual(len(goals_hints), 1)

    def test_display_hints_empty_when_all_configured(self):
        """display_hints should be empty when everything is configured"""
        # Personalized goals (no smart_default)
        (self.base_path / "01-memory" / "goals.md").write_text(
            "---\nname: My Goals\n---\n# Goals\nPersonalized content"
        )
        # All onboarding complete
        config = """---
learning_tracker:
  completed:
    setup_goals: true
    setup_workspace: true
    learn_integrations: true
    learn_builds: true
    learn_skills: true
    learn_nexus: true
---
"""
        (self.base_path / "01-memory" / "user-config.yaml").write_text(config)
        # Workspace configured
        (self.base_path / "04-workspace" / "workspace-map.md").write_text(
            "---\nname: My Workspace\n---\n# Workspace Map\nConfigured"
        )

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        hints = result.get('stats', {}).get('display_hints', [])

        # Should be empty (no update check, so no update hint)
        self.assertEqual(len(hints), 0)


class TestOnboardingIntegration(TestCase):
    """Integration tests for onboarding with other nexus-loader features"""

    def setUp(self):
        """Create a temporary Nexus workspace"""
        self.test_dir = tempfile.mkdtemp()
        self.base_path = Path(self.test_dir)

        # Create minimal structure
        (self.base_path / "00-system" / "core").mkdir(parents=True)
        (self.base_path / "00-system" / "skills" / "learning").mkdir(parents=True)
        (self.base_path / "01-memory").mkdir(parents=True)
        (self.base_path / "02-builds").mkdir(parents=True)
        (self.base_path / "03-skills").mkdir(parents=True)
        (self.base_path / "04-workspace").mkdir(parents=True)

        (self.base_path / "00-system" / "system-map.md").write_text("# System Map\nTest")
        (self.base_path / "01-memory" / "memory-map.md").write_text("# Memory Map\nTest")
        (self.base_path / "01-memory" / "goals.md").write_text("---\nsmart_default: true\n---\n# Goals")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_onboarding_complete_with_goals_personalized(self):
        """When onboarding complete, goals_personalized may still be false (separate tracking)"""
        # All onboarding complete
        config = """---
smart_default: true
learning_tracker:
  completed:
    setup_goals: true
    setup_workspace: true
    learn_integrations: true
    learn_builds: true
    learn_skills: true
    learn_nexus: true
---
"""
        (self.base_path / "01-memory" / "user-config.yaml").write_text(config)

        result = nexus_loader.load_startup(str(self.base_path), check_updates=False)
        stats = result.get('stats', {})

        # Onboarding complete
        self.assertTrue(stats.get('onboarding_complete'))
        self.assertEqual(len(stats.get('pending_onboarding', [])), 0)

        # But goals still has smart_default, so not personalized
        # (goals_personalized checks goals.md, not learning_tracker)
        self.assertFalse(stats.get('goals_personalized'))


if __name__ == '__main__':
    main(verbosity=2)
