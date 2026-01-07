#!/usr/bin/env python3
"""
Code-Based Unit Tests: plan-project Router v2.4

Tests deterministic functionality that doesn't require AI behavior:
- File structure validation (P5)
- Schema validation (P5, REQ-NF-2)
- Function unit tests (init_project.py)
- Template content validation (REQ-NF-4, REQ-NF-5)

Run with: pytest test_plan_project.py -v
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, List, Any
import pytest

# Add the scripts directory to path for imports
NEXUS_ROOT = Path(__file__).parent.parent.parent.parent.parent
PLAN_PROJECT_DIR = NEXUS_ROOT / "00-system" / "skills" / "projects" / "plan-project"
SCRIPTS_DIR = PLAN_PROJECT_DIR / "scripts"
TEMPLATES_DIR = PLAN_PROJECT_DIR / "templates" / "types"

sys.path.insert(0, str(SCRIPTS_DIR))

# Import functions from init_project.py
try:
    from init_project import (
        sanitize_project_name,
        load_type_template,
        get_type_config,
        get_next_project_id,
        init_project
    )
    INIT_PROJECT_AVAILABLE = True
except ImportError as e:
    INIT_PROJECT_AVAILABLE = False
    IMPORT_ERROR = str(e)


# =============================================================================
# CONSTANTS
# =============================================================================

EXPECTED_TYPES = ["build", "integration", "research", "strategy", "content", "process", "skill", "generic"]
EXPECTED_FILES_PER_TYPE = ["_type.yaml", "overview.md", "discovery.md", "plan.md", "steps.md"]

REQUIRED_TYPE_YAML_FIELDS = ["name", "description", "discovery", "outputs", "mental_models"]
SKILL_BASED_TYPES = ["integration", "research", "skill"]
INLINE_DISCOVERY_TYPES = ["build", "strategy", "content", "process", "generic"]
EARS_TYPES = ["build", "skill"]


# =============================================================================
# P5: TEMPLATE STRUCTURE INVARIANT
# =============================================================================

class TestTemplateStructure:
    """
    Property 5: Template Structure Invariant

    "For all 8 project types, the templates/types/{type}/ folder contains
    exactly 5 files (_type.yaml, overview.md, discovery.md, plan.md, steps.md)
    with valid content."
    """

    def test_templates_directory_exists(self):
        """Verify templates/types/ directory exists"""
        assert TEMPLATES_DIR.exists(), f"Templates directory not found: {TEMPLATES_DIR}"
        assert TEMPLATES_DIR.is_dir(), f"Templates path is not a directory: {TEMPLATES_DIR}"

    def test_exactly_8_type_folders_exist(self):
        """Verify exactly 8 type folders exist"""
        type_folders = [f for f in TEMPLATES_DIR.iterdir() if f.is_dir()]
        type_names = sorted([f.name for f in type_folders])

        assert len(type_folders) == 8, f"Expected 8 type folders, found {len(type_folders)}: {type_names}"
        assert type_names == sorted(EXPECTED_TYPES), f"Type folders mismatch. Expected: {sorted(EXPECTED_TYPES)}, Found: {type_names}"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_type_folder_exists(self, type_name: str):
        """Verify each expected type folder exists"""
        type_folder = TEMPLATES_DIR / type_name
        assert type_folder.exists(), f"Type folder missing: {type_name}"
        assert type_folder.is_dir(), f"Type path is not a directory: {type_name}"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_type_folder_has_exactly_5_files(self, type_name: str):
        """Verify each type folder has exactly 5 required files"""
        type_folder = TEMPLATES_DIR / type_name
        files = [f.name for f in type_folder.iterdir() if f.is_file()]

        assert len(files) == 5, f"Type '{type_name}' has {len(files)} files, expected 5: {files}"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    @pytest.mark.parametrize("file_name", EXPECTED_FILES_PER_TYPE)
    def test_required_file_exists(self, type_name: str, file_name: str):
        """Verify each required file exists in each type folder"""
        file_path = TEMPLATES_DIR / type_name / file_name
        assert file_path.exists(), f"Missing file: {type_name}/{file_name}"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    @pytest.mark.parametrize("file_name", EXPECTED_FILES_PER_TYPE)
    def test_required_file_not_empty(self, type_name: str, file_name: str):
        """Verify each required file has content"""
        file_path = TEMPLATES_DIR / type_name / file_name
        content = file_path.read_text(encoding='utf-8')
        assert len(content.strip()) > 0, f"File is empty: {type_name}/{file_name}"


# =============================================================================
# REQ-NF-2: TYPE YAML SCHEMA VALIDATION
# =============================================================================

class TestTypeYamlSchema:
    """
    REQ-NF-2: THE _type.yaml schema SHALL include: name, description,
    discovery.skill (optional), discovery.inline (boolean), outputs.discovery_file,
    mental_models.dynamic.
    """

    def _parse_yaml_simple(self, content: str) -> Dict[str, Any]:
        """Simple YAML parser for flat structure (no external dependencies)"""
        result = {}
        current_key = None
        current_value_lines = []
        indent_level = 0

        for line in content.split('\n'):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue

            # Check for key: value on same line
            if ':' in line:
                key_part = line.split(':')[0]
                value_part = ':'.join(line.split(':')[1:]).strip()

                # Calculate indent
                line_indent = len(line) - len(line.lstrip())

                if line_indent == 0:
                    # Top-level key
                    current_key = key_part.strip()
                    if value_part and not value_part.startswith('|'):
                        result[current_key] = value_part.strip('"\'')
                    elif value_part.startswith('|'):
                        result[current_key] = ""  # Multi-line string, will be populated
                    else:
                        result[current_key] = {}
                elif current_key and isinstance(result.get(current_key), dict):
                    # Nested key
                    nested_key = key_part.strip()
                    nested_value = value_part.strip('"\'')
                    result[current_key][nested_key] = nested_value if nested_value else True

        return result

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_type_yaml_has_required_fields(self, type_name: str):
        """Verify _type.yaml has all required top-level fields"""
        yaml_path = TEMPLATES_DIR / type_name / "_type.yaml"
        content = yaml_path.read_text(encoding='utf-8')

        # Check for required field presence (simple string check)
        for field in REQUIRED_TYPE_YAML_FIELDS:
            assert f"{field}:" in content, f"Missing required field '{field}' in {type_name}/_type.yaml"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_type_yaml_has_name(self, type_name: str):
        """Verify _type.yaml has name field"""
        yaml_path = TEMPLATES_DIR / type_name / "_type.yaml"
        content = yaml_path.read_text(encoding='utf-8')

        assert "name:" in content, f"Missing 'name' field in {type_name}/_type.yaml"

        # Extract name value
        for line in content.split('\n'):
            if line.strip().startswith('name:'):
                name_value = line.split(':', 1)[1].strip()
                assert len(name_value) > 0, f"Empty 'name' in {type_name}/_type.yaml"
                break

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_type_yaml_has_description(self, type_name: str):
        """Verify _type.yaml has description field with content"""
        yaml_path = TEMPLATES_DIR / type_name / "_type.yaml"
        content = yaml_path.read_text(encoding='utf-8')

        assert "description:" in content, f"Missing 'description' field in {type_name}/_type.yaml"
        # Multi-line descriptions have | after description:
        assert "description: |" in content or "description:" in content

    @pytest.mark.parametrize("type_name", SKILL_BASED_TYPES)
    def test_skill_based_type_has_skill_field(self, type_name: str):
        """Verify skill-based types have discovery.skill field"""
        yaml_path = TEMPLATES_DIR / type_name / "_type.yaml"
        content = yaml_path.read_text(encoding='utf-8')

        assert "skill:" in content, f"Skill-based type '{type_name}' missing discovery.skill field"
        assert "skill_load_command:" in content, f"Skill-based type '{type_name}' missing skill_load_command field"

    @pytest.mark.parametrize("type_name", INLINE_DISCOVERY_TYPES)
    def test_inline_type_has_inline_true(self, type_name: str):
        """Verify inline discovery types have discovery.inline: true"""
        yaml_path = TEMPLATES_DIR / type_name / "_type.yaml"
        content = yaml_path.read_text(encoding='utf-8')

        assert "inline: true" in content, f"Inline type '{type_name}' missing 'inline: true'"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_type_yaml_has_mental_models_dynamic(self, type_name: str):
        """Verify _type.yaml has mental_models.dynamic field"""
        yaml_path = TEMPLATES_DIR / type_name / "_type.yaml"
        content = yaml_path.read_text(encoding='utf-8')

        assert "mental_models:" in content, f"Missing 'mental_models' section in {type_name}/_type.yaml"
        assert "dynamic:" in content, f"Missing 'dynamic' field in {type_name}/_type.yaml"


# =============================================================================
# REQ-NF-4: EARS REQUIREMENTS IN BUILD/SKILL TEMPLATES
# =============================================================================

class TestEarsRequirements:
    """
    REQ-NF-4: FOR build and skill project types, THE discovery.md template
    SHALL include EARS-formatted requirements and INCOSE quality checklist.
    """

    @pytest.mark.parametrize("type_name", EARS_TYPES)
    def test_discovery_has_ears_section(self, type_name: str):
        """Verify discovery.md has EARS requirements section"""
        discovery_path = TEMPLATES_DIR / type_name / "discovery.md"
        content = discovery_path.read_text(encoding='utf-8')

        # Check for EARS-related content
        ears_indicators = ["EARS", "THE", "WHEN", "WHILE", "IF", "WHERE", "SHALL"]
        found_indicators = [ind for ind in ears_indicators if ind in content]

        assert len(found_indicators) >= 3, f"EARS patterns not found in {type_name}/discovery.md. Found: {found_indicators}"

    @pytest.mark.parametrize("type_name", EARS_TYPES)
    def test_discovery_has_incose_checklist(self, type_name: str):
        """Verify discovery.md has INCOSE quality checklist"""
        discovery_path = TEMPLATES_DIR / type_name / "discovery.md"
        content = discovery_path.read_text(encoding='utf-8')

        # Check for INCOSE-related content
        incose_indicators = ["INCOSE", "quality", "checklist", "vague", "pronoun", "testable", "active voice"]
        found_indicators = [ind for ind in incose_indicators if ind.lower() in content.lower()]

        assert len(found_indicators) >= 2, f"INCOSE checklist not found in {type_name}/discovery.md. Found: {found_indicators}"

    @pytest.mark.parametrize("type_name", EARS_TYPES)
    def test_discovery_has_requirements_section(self, type_name: str):
        """Verify discovery.md has Requirements section"""
        discovery_path = TEMPLATES_DIR / type_name / "discovery.md"
        content = discovery_path.read_text(encoding='utf-8')

        assert "Requirements" in content or "REQ-" in content, f"Requirements section not found in {type_name}/discovery.md"


# =============================================================================
# REQ-NF-5: CORRECTNESS PROPERTIES IN BUILD/SKILL TEMPLATES
# =============================================================================

class TestCorrectnessProperties:
    """
    REQ-NF-5: FOR build and skill project types, THE plan.md template
    SHALL include Correctness Properties section with universal quantifications.
    """

    @pytest.mark.parametrize("type_name", EARS_TYPES)
    def test_plan_has_correctness_properties_section(self, type_name: str):
        """Verify plan.md has Correctness Properties section"""
        plan_path = TEMPLATES_DIR / type_name / "plan.md"
        content = plan_path.read_text(encoding='utf-8')

        assert "Correctness Properties" in content or "Property" in content, \
            f"Correctness Properties section not found in {type_name}/plan.md"

    @pytest.mark.parametrize("type_name", EARS_TYPES)
    def test_plan_has_universal_quantification(self, type_name: str):
        """Verify plan.md shows universal quantification format"""
        plan_path = TEMPLATES_DIR / type_name / "plan.md"
        content = plan_path.read_text(encoding='utf-8')

        # Check for universal quantification patterns
        quant_patterns = ["For all", "For any", "all valid", "any given"]
        found = any(pattern.lower() in content.lower() for pattern in quant_patterns)

        assert found, f"Universal quantification not found in {type_name}/plan.md"


# =============================================================================
# INIT_PROJECT.PY FUNCTION TESTS
# =============================================================================

@pytest.mark.skipif(not INIT_PROJECT_AVAILABLE, reason=f"init_project.py not importable: {IMPORT_ERROR if not INIT_PROJECT_AVAILABLE else ''}")
class TestSanitizeProjectName:
    """Unit tests for sanitize_project_name() function"""

    def test_lowercase_conversion(self):
        """Verify names are converted to lowercase"""
        assert sanitize_project_name("MyProject") == "myproject"
        assert sanitize_project_name("PROJECT") == "project"

    def test_space_to_hyphen(self):
        """Verify spaces are converted to hyphens"""
        assert sanitize_project_name("my project") == "my-project"
        assert sanitize_project_name("my  project") == "my-project"  # Double space

    def test_special_characters_removed(self):
        """Verify special characters are removed"""
        assert sanitize_project_name("my@project!") == "myproject"
        assert sanitize_project_name("project#123") == "project123"
        assert sanitize_project_name("project (v2)") == "project-v2"

    def test_multiple_hyphens_collapsed(self):
        """Verify multiple hyphens are collapsed to single"""
        assert sanitize_project_name("my--project") == "my-project"
        assert sanitize_project_name("my - - project") == "my-project"

    def test_leading_trailing_hyphens_stripped(self):
        """Verify leading/trailing hyphens are stripped"""
        assert sanitize_project_name("-project-") == "project"
        assert sanitize_project_name("--project--") == "project"

    def test_empty_after_sanitization(self):
        """Verify handling of names that become empty"""
        assert sanitize_project_name("@#$%") == ""
        assert sanitize_project_name("!!!") == ""

    def test_complex_names(self):
        """Test complex real-world project names"""
        assert sanitize_project_name("Build Feature #123 (API)") == "build-feature-123-api"
        assert sanitize_project_name("User's Dashboard - v2.0") == "users-dashboard-v20"


@pytest.mark.skipif(not INIT_PROJECT_AVAILABLE, reason=f"init_project.py not importable")
class TestLoadTypeTemplate:
    """Unit tests for load_type_template() function"""

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_loads_discovery_template(self, type_name: str):
        """Verify discovery.md template loads for each type"""
        content = load_type_template(type_name, "discovery.md")
        assert content is not None, f"Failed to load discovery.md for {type_name}"
        assert len(content) > 0, f"Empty discovery.md for {type_name}"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_loads_plan_template(self, type_name: str):
        """Verify plan.md template loads for each type"""
        content = load_type_template(type_name, "plan.md")
        assert content is not None, f"Failed to load plan.md for {type_name}"
        assert len(content) > 0, f"Empty plan.md for {type_name}"

    def test_returns_none_for_missing_template(self):
        """Verify returns None for non-existent template"""
        content = load_type_template("build", "nonexistent.md")
        assert content is None

    def test_returns_none_for_invalid_type(self):
        """Verify returns None for invalid type"""
        content = load_type_template("invalid_type", "discovery.md")
        assert content is None


@pytest.mark.skipif(not INIT_PROJECT_AVAILABLE, reason=f"init_project.py not importable")
class TestGetTypeConfig:
    """Unit tests for get_type_config() function"""

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_loads_type_config(self, type_name: str):
        """Verify _type.yaml config loads for each type"""
        config = get_type_config(type_name)
        assert config is not None, f"Failed to load config for {type_name}"
        assert isinstance(config, dict), f"Config is not a dict for {type_name}"

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_config_has_name(self, type_name: str):
        """Verify config has name field"""
        config = get_type_config(type_name)
        assert "name" in config, f"Config missing 'name' for {type_name}"

    def test_returns_empty_for_invalid_type(self):
        """Verify returns empty dict for invalid type"""
        config = get_type_config("invalid_type")
        assert config == {}


@pytest.mark.skipif(not INIT_PROJECT_AVAILABLE, reason=f"init_project.py not importable")
class TestGetNextProjectId:
    """Unit tests for get_next_project_id() function"""

    def test_returns_01_for_empty_directory(self):
        """Verify returns '01' for empty projects directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            next_id = get_next_project_id(tmpdir)
            assert next_id == "01"

    def test_returns_01_for_nonexistent_directory(self):
        """Verify returns '01' for non-existent directory"""
        next_id = get_next_project_id("/nonexistent/path/12345")
        assert next_id == "01"

    def test_increments_from_existing(self):
        """Verify increments from highest existing ID"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create some project folders
            os.makedirs(os.path.join(tmpdir, "01-first-project"))
            os.makedirs(os.path.join(tmpdir, "05-fifth-project"))
            os.makedirs(os.path.join(tmpdir, "03-third-project"))

            next_id = get_next_project_id(tmpdir)
            assert next_id == "06"

    def test_ignores_non_project_folders(self):
        """Verify ignores folders without numeric prefix"""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.makedirs(os.path.join(tmpdir, "01-project"))
            os.makedirs(os.path.join(tmpdir, "templates"))  # Should be ignored
            os.makedirs(os.path.join(tmpdir, "archive"))    # Should be ignored

            next_id = get_next_project_id(tmpdir)
            assert next_id == "02"


@pytest.mark.skipif(not INIT_PROJECT_AVAILABLE, reason=f"init_project.py not importable")
class TestInitProject:
    """Integration tests for init_project() function"""

    def test_creates_project_structure(self):
        """Verify creates complete project structure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = init_project(
                project_name="Test Project",
                path=tmpdir,
                project_type="build",
                description="A test project"
            )

            assert result is not None
            assert result.exists()

            # Check folders
            assert (result / "01-planning").is_dir()
            assert (result / "02-resources").is_dir()
            assert (result / "03-working").is_dir()
            assert (result / "04-outputs").is_dir()

            # Check planning files
            assert (result / "01-planning" / "01-overview.md").is_file()
            assert (result / "01-planning" / "02-discovery.md").is_file()
            assert (result / "01-planning" / "03-plan.md").is_file()
            assert (result / "01-planning" / "04-steps.md").is_file()
            assert (result / "01-planning" / "resume-context.md").is_file()

    def test_uses_type_specific_templates(self):
        """Verify uses type-specific templates"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = init_project(
                project_name="Build Test",
                path=tmpdir,
                project_type="build"
            )

            # Build type should have EARS in discovery
            discovery_content = (result / "01-planning" / "02-discovery.md").read_text()
            assert "EARS" in discovery_content or "THE" in discovery_content

    def test_resume_context_has_project_type(self):
        """Verify resume-context.md has project_type field"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = init_project(
                project_name="Type Test",
                path=tmpdir,
                project_type="integration"
            )

            resume_content = (result / "01-planning" / "resume-context.md").read_text()
            assert 'project_type: "integration"' in resume_content

    @pytest.mark.parametrize("type_name", EXPECTED_TYPES)
    def test_all_types_create_successfully(self, type_name: str):
        """Verify all 8 types create projects successfully"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = init_project(
                project_name=f"Test {type_name}",
                path=tmpdir,
                project_type=type_name
            )

            assert result is not None, f"Failed to create project for type: {type_name}"
            assert result.exists(), f"Project directory not created for type: {type_name}"

    def test_rejects_invalid_name(self):
        """Verify rejects names that sanitize to empty"""
        with tempfile.TemporaryDirectory() as tmpdir:
            result = init_project(
                project_name="@#$%",
                path=tmpdir,
                project_type="build"
            )

            assert result is None

    def test_rejects_existing_project(self):
        """Verify rejects if project directory already exists (same ID + same name)"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create first project
            init_project(project_name="Duplicate", path=tmpdir, project_type="build")

            # Try to create with SAME name AND same ID - this should fail
            result = init_project(
                project_name="Duplicate",  # Same name as first
                path=tmpdir,
                project_type="build",
                project_id_override=1  # Same ID as first project
            )

            assert result is None


# =============================================================================
# REFERENCE FILES VALIDATION
# =============================================================================

class TestReferenceFiles:
    """Verify reference documentation files exist"""

    def test_routing_logic_exists(self):
        """Verify routing-logic.md exists"""
        ref_path = PLAN_PROJECT_DIR / "references" / "routing-logic.md"
        assert ref_path.exists(), "Missing references/routing-logic.md"

    def test_ears_patterns_exists(self):
        """Verify ears-patterns.md exists"""
        ref_path = PLAN_PROJECT_DIR / "references" / "ears-patterns.md"
        assert ref_path.exists(), "Missing references/ears-patterns.md"

    def test_incose_rules_exists(self):
        """Verify incose-rules.md exists"""
        ref_path = PLAN_PROJECT_DIR / "references" / "incose-rules.md"
        assert ref_path.exists(), "Missing references/incose-rules.md"


# =============================================================================
# RUN CONFIGURATION
# =============================================================================

if __name__ == "__main__":
    # Run with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
