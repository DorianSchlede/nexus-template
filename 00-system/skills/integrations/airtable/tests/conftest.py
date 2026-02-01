"""Pytest fixtures for Airtable tests."""

import pytest
import os
import sys
import json
import base64
from pathlib import Path
from unittest.mock import MagicMock, patch

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent / 'airtable-master' / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def mock_env():
    """Mock environment with API keys."""
    env_vars = {
        'AIRTABLE_API_KEY': 'pat.test_default_key',
        'AIRTABLE_API_KEY_MUTAGENT': 'pat.test_mutagent_key',
        'AIRTABLE_API_KEY_CLIENT': 'pat.test_client_key',
    }
    with patch.dict(os.environ, env_vars, clear=False):
        yield env_vars


@pytest.fixture
def sample_skill_bundle():
    """Sample skill bundle for testing."""
    skill_md_content = """---
name: test-skill
description: A test skill for unit tests
version: "1.0"
---

# Test Skill

## Purpose

This is a test skill.
"""
    script_content = """#!/usr/bin/env python3
print("Hello from test script")
"""

    return {
        "skill_name": "test-skill",
        "version": "1.0",
        "bundle_format": "nexus-skill-bundle-v1",
        "created": "2025-12-31T12:00:00",
        "files": {
            "SKILL.md": base64.b64encode(skill_md_content.encode()).decode(),
            "scripts/test.py": base64.b64encode(script_content.encode()).decode(),
        },
        "partial": False
    }


@pytest.fixture
def partial_skill_bundle():
    """Partial skill bundle (SKILL.md only)."""
    skill_md_content = """---
name: large-skill
description: A large skill with partial bundle
version: "2.0"
---

# Large Skill

## Purpose

This skill is too large for full bundle.
"""

    return {
        "skill_name": "large-skill",
        "version": "2.0",
        "bundle_format": "nexus-skill-bundle-v1",
        "created": "2025-12-31T12:00:00",
        "files": {
            "SKILL.md": base64.b64encode(skill_md_content.encode()).decode(),
        },
        "partial": True
    }


@pytest.fixture
def mock_airtable_response():
    """Mock Airtable API response."""
    def _make_response(records):
        return {
            "records": [
                {
                    "id": f"rec{i:010d}",
                    "fields": rec,
                    "createdTime": "2025-12-31T12:00:00.000Z"
                }
                for i, rec in enumerate(records)
            ]
        }
    return _make_response


@pytest.fixture
def mock_requests():
    """Mock requests module."""
    with patch('requests.request') as mock:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"records": []}
        mock.return_value = mock_response
        yield mock


@pytest.fixture
def temp_skill_dir(tmp_path):
    """Create a temporary skill directory for testing."""
    skill_dir = tmp_path / "test-skill"
    skill_dir.mkdir()

    # Create SKILL.md
    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text("""---
name: test-skill
description: Test skill
version: "1.0"
---

# Test Skill

## Purpose

For testing.
""")

    # Create scripts directory
    scripts_dir = skill_dir / "scripts"
    scripts_dir.mkdir()
    (scripts_dir / "helper.py").write_text("# Helper script\n")

    return skill_dir
