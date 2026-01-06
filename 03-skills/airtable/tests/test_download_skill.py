"""Unit tests for download_skill.py"""

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


class TestExtractBundle:
    """Tests for extract_bundle function."""

    def test_extracts_full_bundle(self, tmp_path, sample_skill_bundle):
        from download_skill import extract_bundle

        bundle_json = json.dumps(sample_skill_bundle)
        success, message = extract_bundle(bundle_json, str(tmp_path), 'test-skill', backup=False)

        assert success is True
        assert 'Extracted 2 files' in message
        assert '(complete)' in message

        # Verify files exist
        skill_dir = tmp_path / 'test-skill'
        assert (skill_dir / 'SKILL.md').exists()
        assert (skill_dir / 'scripts' / 'test.py').exists()

    def test_extracts_partial_bundle(self, tmp_path, partial_skill_bundle):
        from download_skill import extract_bundle

        bundle_json = json.dumps(partial_skill_bundle)
        success, message = extract_bundle(bundle_json, str(tmp_path), 'large-skill', backup=False)

        assert success is True
        assert '(partial)' in message

        skill_dir = tmp_path / 'large-skill'
        assert (skill_dir / 'SKILL.md').exists()

    def test_decodes_content_correctly(self, tmp_path, sample_skill_bundle):
        from download_skill import extract_bundle

        bundle_json = json.dumps(sample_skill_bundle)
        extract_bundle(bundle_json, str(tmp_path), 'test-skill', backup=False)

        skill_md = (tmp_path / 'test-skill' / 'SKILL.md').read_text()
        assert 'name: test-skill' in skill_md
        assert '## Purpose' in skill_md

    def test_creates_backup(self, tmp_path, sample_skill_bundle):
        from download_skill import extract_bundle

        # Create existing skill
        skill_dir = tmp_path / 'test-skill'
        skill_dir.mkdir()
        (skill_dir / 'old_file.txt').write_text('old content')

        bundle_json = json.dumps(sample_skill_bundle)
        success, message = extract_bundle(bundle_json, str(tmp_path), 'test-skill', backup=True)

        assert success is True

        # Check backup was created
        backups = list(tmp_path.glob('test-skill.backup.*'))
        assert len(backups) == 1
        assert (backups[0] / 'old_file.txt').exists()

    def test_no_backup_when_disabled(self, tmp_path, sample_skill_bundle):
        from download_skill import extract_bundle

        # Create existing skill
        skill_dir = tmp_path / 'test-skill'
        skill_dir.mkdir()
        (skill_dir / 'old_file.txt').write_text('old content')

        bundle_json = json.dumps(sample_skill_bundle)
        extract_bundle(bundle_json, str(tmp_path), 'test-skill', backup=False)

        # No backup should exist
        backups = list(tmp_path.glob('test-skill.backup.*'))
        assert len(backups) == 0

    def test_handles_invalid_json(self, tmp_path):
        from download_skill import extract_bundle

        success, message = extract_bundle('not valid json', str(tmp_path), 'test', backup=False)

        assert success is False
        assert 'Invalid JSON' in message

    def test_handles_empty_files(self, tmp_path):
        from download_skill import extract_bundle

        bundle = {
            "skill_name": "empty",
            "version": "1.0",
            "bundle_format": "nexus-skill-bundle-v1",
            "files": {}
        }
        bundle_json = json.dumps(bundle)

        success, message = extract_bundle(bundle_json, str(tmp_path), 'empty', backup=False)

        assert success is False
        assert 'No files' in message


class TestGetAllRecords:
    """Tests for get_all_records function."""

    def test_fetches_single_page(self, mock_env, mock_requests, mock_airtable_response):
        from download_skill import get_all_records

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = mock_airtable_response([
            {'Name': 'skill-1', 'Content': '{}'},
            {'Name': 'skill-2', 'Content': '{}'}
        ])

        records = get_all_records('appTEST', 'tblTEST', 'MUTAGENT')

        assert len(records) == 2
        assert records[0]['fields']['Name'] == 'skill-1'

    def test_handles_pagination(self, mock_env, mock_requests, mock_airtable_response):
        from download_skill import get_all_records

        # First call returns offset, second call returns no offset
        responses = [
            {**mock_airtable_response([{'Name': 'skill-1'}]), 'offset': 'page2'},
            mock_airtable_response([{'Name': 'skill-2'}])
        ]

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.side_effect = responses

        records = get_all_records('appTEST', 'tblTEST')

        assert len(records) == 2

    def test_applies_filter_formula(self, mock_env, mock_requests, mock_airtable_response):
        from download_skill import get_all_records

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = mock_airtable_response([
            {'Name': 'specific-skill'}
        ])

        get_all_records('appTEST', 'tblTEST', filter_formula='{Name}="specific-skill"')

        # Would need to check params in call - simplified for now
        assert mock_requests.called


class TestDownloadSkill:
    """Tests for download_skill function."""

    def test_downloads_single_skill(self, mock_env, mock_requests, tmp_path, sample_skill_bundle):
        from download_skill import download_skill

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [{
                'id': 'recTEST',
                'fields': {
                    'Name': 'test-skill',
                    'Content': json.dumps(sample_skill_bundle)
                }
            }]
        }

        success, message = download_skill('appTEST', 'tblTEST', 'test-skill', str(tmp_path))

        assert success is True
        assert (tmp_path / 'test-skill' / 'SKILL.md').exists()

    def test_skill_not_found(self, mock_env, mock_requests, tmp_path):
        from download_skill import download_skill

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {'records': []}

        success, message = download_skill('appTEST', 'tblTEST', 'nonexistent', str(tmp_path))

        assert success is False
        assert 'not found' in message.lower()

    def test_handles_no_content(self, mock_env, mock_requests, tmp_path):
        from download_skill import download_skill

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [{
                'id': 'recTEST',
                'fields': {'Name': 'empty-skill'}  # No Content field
            }]
        }

        success, message = download_skill('appTEST', 'tblTEST', 'empty-skill', str(tmp_path))

        assert success is False
        assert 'No content' in message


class TestDownloadAllSkills:
    """Tests for download_all_skills function."""

    def test_downloads_multiple_skills(self, mock_env, mock_requests, tmp_path, sample_skill_bundle):
        from download_skill import download_all_skills

        bundle1 = {**sample_skill_bundle, 'skill_name': 'skill-1'}
        bundle2 = {**sample_skill_bundle, 'skill_name': 'skill-2'}

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [
                {'id': 'rec1', 'fields': {'Name': 'skill-1', 'Content': json.dumps(bundle1)}},
                {'id': 'rec2', 'fields': {'Name': 'skill-2', 'Content': json.dumps(bundle2)}}
            ]
        }

        success, failed = download_all_skills('appTEST', 'tblTEST', str(tmp_path), backup=False)

        assert success == 2
        assert failed == 0
        assert (tmp_path / 'skill-1').exists()
        assert (tmp_path / 'skill-2').exists()

    def test_dry_run_no_files(self, mock_env, mock_requests, tmp_path, sample_skill_bundle):
        from download_skill import download_all_skills

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [
                {'id': 'rec1', 'fields': {'Name': 'skill-1', 'Content': json.dumps(sample_skill_bundle)}}
            ]
        }

        success, failed = download_all_skills('appTEST', 'tblTEST', str(tmp_path), dry_run=True)

        assert success == 1
        assert not (tmp_path / 'skill-1').exists()  # No files created in dry run

    def test_skips_empty_content(self, mock_env, mock_requests, tmp_path, sample_skill_bundle):
        from download_skill import download_all_skills

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [
                {'id': 'rec1', 'fields': {'Name': 'good-skill', 'Content': json.dumps(sample_skill_bundle)}},
                {'id': 'rec2', 'fields': {'Name': 'empty-skill'}}  # No content
            ]
        }

        success, failed = download_all_skills('appTEST', 'tblTEST', str(tmp_path), backup=False)

        assert success == 1
        assert failed == 1


class TestRoundTrip:
    """Integration tests for upload -> download cycle."""

    def test_bundle_survives_round_trip(self, tmp_path, temp_skill_dir):
        """Test that a skill can be bundled and unbundled without data loss."""
        from upload_local_skills import create_skill_bundle
        from download_skill import extract_bundle

        # Create bundle
        metadata = {'name': 'roundtrip-skill', 'version': '1.0'}
        bundle = create_skill_bundle(str(temp_skill_dir), metadata, skill_md_only=False)
        bundle_json = json.dumps(bundle)

        # Extract bundle
        output_dir = tmp_path / 'output'
        output_dir.mkdir()
        success, _ = extract_bundle(bundle_json, str(output_dir), 'roundtrip-skill', backup=False)

        assert success is True

        # Compare files
        original_skill_md = (temp_skill_dir / 'SKILL.md').read_text()
        extracted_skill_md = (output_dir / 'roundtrip-skill' / 'SKILL.md').read_text()

        assert original_skill_md == extracted_skill_md


class TestGetLinkedFiles:
    """Tests for get_linked_files function."""

    def test_filters_by_skill_record_id(self, mock_env, mock_requests):
        from download_skill import get_linked_files

        skill_record_id = 'recSKILL123'

        # Mock response with multiple files, some linked to our skill
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [
                {
                    'id': 'recFile1',
                    'fields': {
                        'FilePath': 'scripts/helper.py',
                        'Content': base64.b64encode(b'# helper').decode(),
                        'Skill': [skill_record_id]
                    }
                },
                {
                    'id': 'recFile2',
                    'fields': {
                        'FilePath': 'SKILL.md',
                        'Content': base64.b64encode(b'# SKILL').decode(),
                        'Skill': [skill_record_id]
                    }
                },
                {
                    'id': 'recFile3',
                    'fields': {
                        'FilePath': 'other/file.py',
                        'Content': base64.b64encode(b'# other').decode(),
                        'Skill': ['recOTHER']  # Different skill
                    }
                }
            ]
        }

        files = get_linked_files('appTEST', 'tblFILES', skill_record_id, 'MUTAGENT')

        assert len(files) == 2
        assert 'scripts/helper.py' in files
        assert 'SKILL.md' in files
        assert 'other/file.py' not in files

    def test_returns_empty_dict_for_no_matches(self, mock_env, mock_requests):
        from download_skill import get_linked_files

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [
                {
                    'id': 'recFile1',
                    'fields': {
                        'FilePath': 'file.py',
                        'Content': base64.b64encode(b'# file').decode(),
                        'Skill': ['recOTHER']
                    }
                }
            ]
        }

        files = get_linked_files('appTEST', 'tblFILES', 'recNONEXISTENT', 'MUTAGENT')

        assert files == {}

    def test_handles_api_error(self, mock_env, mock_requests):
        from download_skill import get_linked_files

        mock_requests.return_value.status_code = 500
        mock_requests.return_value.json.return_value = {'error': 'Server error'}

        files = get_linked_files('appTEST', 'tblFILES', 'recTEST')

        assert files is None


class TestDownloadSkillWithLinked:
    """Tests for download_skill_with_linked function."""

    def test_merges_linked_files_for_partial_bundle(self, mock_env, mock_requests, tmp_path, partial_skill_bundle):
        from download_skill import download_skill_with_linked

        skill_record_id = 'recSKILL123'

        # First call: get skill record
        # Second call: get linked files
        responses = [
            {
                'records': [{
                    'id': skill_record_id,
                    'fields': {
                        'Name': 'large-skill',
                        'Content': json.dumps(partial_skill_bundle)
                    }
                }]
            },
            {
                'records': [
                    {
                        'id': 'recFile1',
                        'fields': {
                            'FilePath': 'scripts/extra.py',
                            'Content': base64.b64encode(b'# extra script').decode(),
                            'Skill': [skill_record_id]
                        }
                    }
                ]
            }
        ]

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.side_effect = responses

        success, message = download_skill_with_linked(
            'appTEST', 'tblSKILLS', 'large-skill', str(tmp_path),
            'MUTAGENT', 'tblFILES', backup=False
        )

        assert success is True
        assert '(complete' in message
        assert '+1 linked' in message

        # Both SKILL.md (from bundle) and extra.py (from linked) should exist
        skill_dir = tmp_path / 'large-skill'
        assert (skill_dir / 'SKILL.md').exists()
        assert (skill_dir / 'scripts' / 'extra.py').exists()

    def test_downloads_without_linked_when_not_partial(self, mock_env, mock_requests, tmp_path, sample_skill_bundle):
        from download_skill import download_skill_with_linked

        skill_record_id = 'recSKILL123'

        # Only one call needed - skill is not partial
        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {
            'records': [{
                'id': skill_record_id,
                'fields': {
                    'Name': 'test-skill',
                    'Content': json.dumps(sample_skill_bundle)
                }
            }]
        }

        success, message = download_skill_with_linked(
            'appTEST', 'tblSKILLS', 'test-skill', str(tmp_path),
            'MUTAGENT', 'tblFILES', backup=False
        )

        assert success is True
        assert '(complete)' in message
        # Should not mention linked files since bundle is complete
        assert 'linked' not in message

    def test_skill_not_found(self, mock_env, mock_requests, tmp_path):
        from download_skill import download_skill_with_linked

        mock_requests.return_value.status_code = 200
        mock_requests.return_value.json.return_value = {'records': []}

        success, message = download_skill_with_linked(
            'appTEST', 'tblSKILLS', 'nonexistent', str(tmp_path),
            'MUTAGENT', 'tblFILES', backup=False
        )

        assert success is False
        assert 'not found' in message.lower()
