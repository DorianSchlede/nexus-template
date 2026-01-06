#!/usr/bin/env python3
"""
Unit tests for save-resume-state.py PreCompact hook.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

# Add hooks directory to path
sys.path.insert(0, str(Path(__file__).parent))

from save_resume_state import (
    find_nexus_root,
    load_cache_context,
    get_active_project,
    parse_transcript_for_skill,
    skill_to_phase,
    write_resume_file,
)


class TestFindNexusRoot(unittest.TestCase):
    def test_uses_env_variable(self):
        with patch.dict(os.environ, {"CLAUDE_PROJECT_DIR": "/test/path"}):
            result = find_nexus_root()
            self.assertEqual(result, Path("/test/path"))

    def test_fallback_to_cwd(self):
        with patch.dict(os.environ, {}, clear=True):
            os.environ.pop("CLAUDE_PROJECT_DIR", None)
            result = find_nexus_root()
            self.assertEqual(result, Path.cwd())


class TestLoadCacheContext(unittest.TestCase):
    def test_returns_empty_if_no_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            result = load_cache_context(Path(tmpdir))
            self.assertEqual(result, {})

    def test_loads_valid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "00-system" / ".cache"
            cache_dir.mkdir(parents=True)
            cache_file = cache_dir / "context_startup.json"
            cache_file.write_text('{"test": "value"}')

            result = load_cache_context(Path(tmpdir))
            self.assertEqual(result, {"test": "value"})

    def test_handles_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cache_dir = Path(tmpdir) / "00-system" / ".cache"
            cache_dir.mkdir(parents=True)
            cache_file = cache_dir / "context_startup.json"
            cache_file.write_text('invalid json {{{')

            result = load_cache_context(Path(tmpdir))
            self.assertEqual(result, {})


class TestGetActiveProject(unittest.TestCase):
    def test_returns_none_for_empty_context(self):
        result = get_active_project({})
        self.assertIsNone(result)

    def test_returns_none_for_no_projects(self):
        result = get_active_project({"metadata": {"projects": []}})
        self.assertIsNone(result)

    def test_returns_first_in_progress_project(self):
        context = {
            "metadata": {
                "projects": [
                    {"id": "01-complete", "status": "COMPLETE"},
                    {"id": "02-active", "status": "IN_PROGRESS"},
                    {"id": "03-also-active", "status": "IN_PROGRESS"},
                ]
            }
        }
        result = get_active_project(context)
        self.assertEqual(result["id"], "02-active")

    def test_returns_none_if_no_in_progress(self):
        context = {
            "metadata": {
                "projects": [
                    {"id": "01-complete", "status": "COMPLETE"},
                    {"id": "02-planning", "status": "PLANNING"},
                ]
            }
        }
        result = get_active_project(context)
        self.assertIsNone(result)


class TestParseTranscriptForSkill(unittest.TestCase):
    def test_returns_none_for_missing_file(self):
        result = parse_transcript_for_skill("/nonexistent/path.jsonl")
        self.assertIsNone(result)

    def test_extracts_skill_from_transcript(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript_file = Path(tmpdir) / "transcript.jsonl"
            transcript_file.write_text(
                '{"content": "python nexus-loader.py --skill execute-project"}\n'
                '{"content": "python nexus-loader.py --skill analyze-research-project"}\n'
            )

            result = parse_transcript_for_skill(str(transcript_file))
            # Should return the last skill found
            self.assertEqual(result, "analyze-research-project")

    def test_handles_no_skill_in_transcript(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript_file = Path(tmpdir) / "transcript.jsonl"
            transcript_file.write_text('{"content": "some other command"}\n')

            result = parse_transcript_for_skill(str(transcript_file))
            self.assertIsNone(result)

    def test_handles_malformed_jsonl(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            transcript_file = Path(tmpdir) / "transcript.jsonl"
            transcript_file.write_text(
                'not valid json\n'
                '{"content": "--skill test-skill"}\n'
            )

            result = parse_transcript_for_skill(str(transcript_file))
            self.assertEqual(result, "test-skill")


class TestSkillToPhase(unittest.TestCase):
    def test_analyze_maps_to_analysis(self):
        self.assertEqual(skill_to_phase("analyze-research-project"), "analysis")

    def test_synthesize_maps_to_synthesis(self):
        self.assertEqual(skill_to_phase("synthesize-research-project"), "synthesis")

    def test_execute_maps_to_execution(self):
        self.assertEqual(skill_to_phase("execute-project"), "execution")

    def test_create_maps_to_planning(self):
        self.assertEqual(skill_to_phase("create-project"), "planning")

    def test_unknown_defaults_to_execution(self):
        self.assertEqual(skill_to_phase("unknown-skill"), "execution")


class TestWriteResumeFile(unittest.TestCase):
    def test_writes_resume_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)

            result = write_resume_file(
                project_path,
                skill="execute-project",
                phase="execution",
                project_id="test-project"
            )

            self.assertTrue(result)

            resume_file = project_path / "_resume.md"
            self.assertTrue(resume_file.exists())

            content = resume_file.read_text()
            self.assertIn('phase: "execution"', content)
            self.assertIn('last_skill: "execute-project"', content)
            self.assertIn('project_id: "test-project"', content)

    def test_yaml_frontmatter_is_valid(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            project_path = Path(tmpdir)

            write_resume_file(
                project_path,
                skill="analyze-research-project",
                phase="analysis",
                project_id="02-research"
            )

            resume_file = project_path / "_resume.md"
            content = resume_file.read_text()

            # Should start with ---
            self.assertTrue(content.startswith("---"))

            # Should have closing ---
            parts = content.split("---")
            self.assertGreaterEqual(len(parts), 3)


class TestIntegration(unittest.TestCase):
    """Integration test simulating full hook execution."""

    def test_full_flow(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Setup: Create cache with active project
            cache_dir = tmpdir / "00-system" / ".cache"
            cache_dir.mkdir(parents=True)

            project_dir = tmpdir / "02-projects" / "test-project" / "01-planning"
            project_dir.mkdir(parents=True)

            cache_content = {
                "metadata": {
                    "projects": [
                        {
                            "id": "test-project",
                            "status": "IN_PROGRESS",
                            "_file_path": str(project_dir / "overview.md")
                        }
                    ]
                }
            }
            (cache_dir / "context_startup.json").write_text(json.dumps(cache_content))

            # Create transcript with skill
            transcript_file = tmpdir / "transcript.jsonl"
            transcript_file.write_text('{"content": "--skill analyze-research-project"}\n')

            # Execute flow
            cache_context = load_cache_context(tmpdir)
            active_project = get_active_project(cache_context)

            self.assertIsNotNone(active_project)
            self.assertEqual(active_project["id"], "test-project")

            last_skill = parse_transcript_for_skill(str(transcript_file))
            self.assertEqual(last_skill, "analyze-research-project")

            phase = skill_to_phase(last_skill)
            self.assertEqual(phase, "analysis")

            project_path = Path(active_project["_file_path"]).parent.parent
            success = write_resume_file(project_path, last_skill, phase, active_project["id"])
            self.assertTrue(success)

            # Verify result
            resume_file = project_path / "_resume.md"
            self.assertTrue(resume_file.exists())
            content = resume_file.read_text()
            self.assertIn('phase: "analysis"', content)
            self.assertIn('last_skill: "analyze-research-project"', content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
