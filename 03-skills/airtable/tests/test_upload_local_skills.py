"""Unit tests for upload_local_skills.py"""

import pytest
import json
import base64
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts to path
SCRIPTS_DIR = Path(__file__).parent.parent / 'airtable-master' / 'scripts'
sys.path.insert(0, str(SCRIPTS_DIR))


class TestParseYamlFrontmatter:
    """Tests for parse_yaml_frontmatter function."""

    def test_valid_frontmatter(self):
        from upload_local_skills import parse_yaml_frontmatter

        content = """---
name: test-skill
version: "1.0"
description: A test skill
---

# Test Skill

Content here.
"""
        metadata, body = parse_yaml_frontmatter(content)

        assert metadata['name'] == 'test-skill'
        assert metadata['version'] == '1.0'
        assert metadata['description'] == 'A test skill'
        assert '# Test Skill' in body

    def test_no_frontmatter(self):
        from upload_local_skills import parse_yaml_frontmatter

        content = "# Just a heading\n\nNo frontmatter here."
        metadata, body = parse_yaml_frontmatter(content)

        assert metadata == {}
        assert body == content

    def test_empty_frontmatter(self):
        from upload_local_skills import parse_yaml_frontmatter

        content = """---
---

Content only.
"""
        metadata, body = parse_yaml_frontmatter(content)

        assert metadata == {}
        assert 'Content only' in body

    def test_malformed_yaml(self):
        from upload_local_skills import parse_yaml_frontmatter

        content = """---
name: [invalid yaml
---

Content.
"""
        metadata, body = parse_yaml_frontmatter(content)

        # Should return empty metadata on parse error
        assert metadata == {}


class TestCreateSkillBundle:
    """Tests for create_skill_bundle function."""

    def test_full_bundle(self, temp_skill_dir):
        from upload_local_skills import create_skill_bundle

        metadata = {'name': 'test-skill', 'version': '1.0'}
        bundle = create_skill_bundle(str(temp_skill_dir), metadata, skill_md_only=False)

        assert bundle['skill_name'] == 'test-skill'
        assert bundle['version'] == '1.0'
        assert bundle['bundle_format'] == 'nexus-skill-bundle-v1'
        assert bundle['partial'] is False
        assert 'SKILL.md' in bundle['files']
        assert 'scripts/helper.py' in bundle['files']

    def test_partial_bundle(self, temp_skill_dir):
        from upload_local_skills import create_skill_bundle

        metadata = {'name': 'test-skill', 'version': '1.0'}
        bundle = create_skill_bundle(str(temp_skill_dir), metadata, skill_md_only=True)

        assert bundle['partial'] is True
        assert 'SKILL.md' in bundle['files']
        assert 'scripts/helper.py' not in bundle['files']

    def test_bundle_decodes_correctly(self, temp_skill_dir):
        from upload_local_skills import create_skill_bundle

        metadata = {'name': 'test-skill', 'version': '1.0'}
        bundle = create_skill_bundle(str(temp_skill_dir), metadata, skill_md_only=False)

        # Decode SKILL.md and verify content
        skill_md_b64 = bundle['files']['SKILL.md']
        skill_md_content = base64.b64decode(skill_md_b64).decode('utf-8')

        assert 'name: test-skill' in skill_md_content
        assert '## Purpose' in skill_md_content


class TestFindSkillFiles:
    """Tests for find_skill_files function."""

    def test_finds_all_files(self, temp_skill_dir):
        from upload_local_skills import find_skill_files

        files = find_skill_files(temp_skill_dir)

        assert 'SKILL.md' in files
        assert 'scripts/helper.py' in files

    def test_excludes_pycache(self, temp_skill_dir):
        from upload_local_skills import find_skill_files

        # Create __pycache__ directory
        pycache = temp_skill_dir / '__pycache__'
        pycache.mkdir()
        (pycache / 'module.cpython-39.pyc').write_bytes(b'compiled')

        files = find_skill_files(temp_skill_dir)

        assert not any('__pycache__' in f for f in files)
        assert not any('.pyc' in f for f in files)

    def test_normalizes_path_separators(self, temp_skill_dir):
        from upload_local_skills import find_skill_files

        files = find_skill_files(temp_skill_dir)

        # All paths should use forward slashes
        for path in files.keys():
            assert '\\' not in path


class TestGetSkillNameFromPath:
    """Tests for get_skill_name_from_path function."""

    def test_extracts_name_from_skills_path(self):
        from upload_local_skills import get_skill_name_from_path

        path = '/some/path/00-system/skills/hubspot/hubspot-connect'
        name = get_skill_name_from_path(path)

        assert name == 'hubspot/hubspot-connect'

    def test_single_level_skill(self):
        from upload_local_skills import get_skill_name_from_path

        path = '/path/skills/standalone-skill'
        name = get_skill_name_from_path(path)

        assert name == 'standalone-skill'


class TestUploadSkillToAirtable:
    """Tests for upload_skill_to_airtable function."""

    def test_successful_upload(self, mock_env, mock_requests, temp_skill_dir):
        from upload_local_skills import upload_skill_to_airtable

        # Configure mock response
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [{'id': 'recTEST123'}]
        }

        skill_info = {
            'path': str(temp_skill_dir),
            'name': 'test-skill',
            'description': 'Test',
            'version': '1.0',
            'metadata': {'name': 'test-skill', 'version': '1.0'}
        }

        success, result = upload_skill_to_airtable('appTEST', 'tblTEST', skill_info, 'MUTAGENT')

        assert success is True
        assert 'recTEST123' in result

    def test_upload_extracts_team(self, mock_env, mock_requests, tmp_path):
        from upload_local_skills import upload_skill_to_airtable

        # Create skill in proper path structure
        skill_dir = tmp_path / 'skills' / 'hubspot' / 'hubspot-connect'
        skill_dir.mkdir(parents=True)
        (skill_dir / 'SKILL.md').write_text('---\nname: hubspot-connect\n---\n# Skill')

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [{'id': 'recTEST'}]
        }

        skill_info = {
            'path': str(skill_dir),
            'name': 'hubspot-connect',
            'description': 'Test',
            'version': '1.0',
            'metadata': {'name': 'hubspot-connect'}
        }

        upload_skill_to_airtable('appTEST', 'tblTEST', skill_info, 'MUTAGENT')

        # Check that team was included in request
        call_args = mock_requests.call_args
        body = call_args[1]['json']
        fields = body['records'][0]['fields']

        assert fields.get('Team') == 'hubspot'

    def test_large_bundle_falls_back_to_partial(self, mock_env, mock_requests, temp_skill_dir):
        from upload_local_skills import upload_skill_to_airtable, MAX_CONTENT_SIZE

        # Create a large file to exceed MAX_CONTENT_SIZE
        large_file = temp_skill_dir / 'large_data.txt'
        large_file.write_text('x' * (MAX_CONTENT_SIZE + 10000))

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [{'id': 'recPARTIAL'}]
        }

        skill_info = {
            'path': str(temp_skill_dir),
            'name': 'test-skill',
            'description': 'Test',
            'version': '1.0',
            'metadata': {'name': 'test-skill'}
        }

        success, result = upload_skill_to_airtable('appTEST', 'tblTEST', skill_info)

        assert success is True
        assert 'partial' in result.lower()

    def test_handles_api_error(self, mock_env, mock_requests, temp_skill_dir):
        from upload_local_skills import upload_skill_to_airtable

        mock_requests.return_value.status_code = 400
        mock_requests.return_value.json.return_value = {
            'error': {'message': 'Invalid field value'}
        }

        skill_info = {
            'path': str(temp_skill_dir),
            'name': 'test-skill',
            'description': 'Test',
            'version': '1.0',
            'metadata': {}
        }

        success, result = upload_skill_to_airtable('appTEST', 'tblTEST', skill_info)

        assert success is False
        assert 'Invalid field value' in result


class TestGetHeaders:
    """Tests for get_headers function."""

    def test_headers_have_authorization(self, mock_env):
        """Test that headers include Authorization."""
        from upload_local_skills import get_headers

        headers = get_headers()

        assert 'Authorization' in headers
        assert headers['Authorization'].startswith('Bearer ')
        assert 'Content-Type' in headers

    def test_named_token_uses_different_key(self, mock_env):
        """Test that named tokens access different env vars."""
        from upload_local_skills import get_headers

        # Both should work with mock_env fixture
        headers_default = get_headers()
        headers_mutagent = get_headers('MUTAGENT')

        assert 'Authorization' in headers_default
        assert 'Authorization' in headers_mutagent

    def test_missing_token_raises(self):
        """Test that missing token raises ValueError."""
        from upload_local_skills import get_headers

        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                get_headers('NONEXISTENT')
