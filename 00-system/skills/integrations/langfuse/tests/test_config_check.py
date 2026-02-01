"""Unit tests for Langfuse config checker."""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "langfuse-master" / "scripts"))

from check_langfuse_config import check_config


class TestCheckConfig:
    """Tests for check_config function."""

    def test_config_valid_all_vars_set(self):
        """Test config is valid when all vars are set."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test-key",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }):
            result = check_config()
            assert result["status"] == "configured"
            assert result["ai_action"] == "proceed_with_operation"
            assert result["missing"] == []
            assert "LANGFUSE_PUBLIC_KEY" in result["configured"]
            assert "LANGFUSE_SECRET_KEY" in result["configured"]
            assert "LANGFUSE_HOST" in result["configured"]

    def test_config_missing_public_key(self):
        """Test config detects missing public key."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }, clear=True):
            result = check_config()
            assert result["status"] == "not_configured"
            assert result["ai_action"] == "prompt_for_api_key"
            assert "LANGFUSE_PUBLIC_KEY" in result["missing"]

    def test_config_missing_secret_key(self):
        """Test config detects missing secret key."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test-key",
            "LANGFUSE_SECRET_KEY": "",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }, clear=True):
            result = check_config()
            assert result["status"] == "not_configured"
            assert result["ai_action"] == "prompt_for_api_key"
            assert "LANGFUSE_SECRET_KEY" in result["missing"]

    def test_config_missing_host(self):
        """Test config detects missing host."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test-key",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": ""
        }, clear=True):
            result = check_config()
            assert result["status"] == "not_configured"
            assert result["ai_action"] == "prompt_for_api_key"
            assert "LANGFUSE_HOST" in result["missing"]

    def test_config_missing_multiple(self):
        """Test config detects multiple missing vars."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "",
            "LANGFUSE_SECRET_KEY": "",
            "LANGFUSE_HOST": ""
        }, clear=True):
            result = check_config()
            assert result["status"] == "not_configured"
            assert len(result["missing"]) == 3
            assert len(result["fix_instructions"]) == 3

    def test_config_warns_invalid_public_key_format(self):
        """Test config warns when public key has wrong format."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "invalid-format",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }):
            result = check_config()
            assert result["status"] == "configured"
            assert result["warnings"] is not None
            assert any("pk-lf-" in w for w in result["warnings"])

    def test_config_warns_invalid_secret_key_format(self):
        """Test config warns when secret key has wrong format."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test-key",
            "LANGFUSE_SECRET_KEY": "invalid-format",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }):
            result = check_config()
            assert result["status"] == "configured"
            assert result["warnings"] is not None
            assert any("sk-lf-" in w for w in result["warnings"])

    def test_config_warns_invalid_host_format(self):
        """Test config warns when host has wrong format."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test-key",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": "not-a-url"
        }):
            result = check_config()
            assert result["status"] == "configured"
            assert result["warnings"] is not None
            assert any("http" in w for w in result["warnings"])

    def test_config_no_warnings_valid_format(self):
        """Test config has no warnings when format is valid."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-valid-key",
            "LANGFUSE_SECRET_KEY": "sk-lf-valid-key",
            "LANGFUSE_HOST": "https://valid.langfuse.com"
        }):
            result = check_config()
            assert result["status"] == "configured"
            assert result["warnings"] is None

    def test_config_returns_host_when_configured(self):
        """Test config returns host URL when configured."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test-key",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": "https://my.langfuse.com"
        }):
            result = check_config()
            assert result["host"] == "https://my.langfuse.com"

    def test_config_provides_fix_instructions(self):
        """Test config provides fix instructions for missing vars."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "",
            "LANGFUSE_SECRET_KEY": "sk-lf-test-key",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }, clear=True):
            result = check_config()
            assert "fix_instructions" in result
            assert len(result["fix_instructions"]) > 0
            assert any("LANGFUSE_PUBLIC_KEY" in fix for fix in result["fix_instructions"])

    def test_config_provides_examples(self):
        """Test config provides example values when not configured."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "",
            "LANGFUSE_SECRET_KEY": "",
            "LANGFUSE_HOST": ""
        }, clear=True):
            result = check_config()
            assert "example" in result
            assert "LANGFUSE_PUBLIC_KEY" in result["example"]
            assert "LANGFUSE_SECRET_KEY" in result["example"]
            assert "LANGFUSE_HOST" in result["example"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
