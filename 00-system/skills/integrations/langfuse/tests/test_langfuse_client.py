"""Unit tests for Langfuse client."""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add parent paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "langfuse-master" / "scripts"))

from langfuse_client import LangfuseClient, get_client


class TestLangfuseClient:
    """Tests for LangfuseClient class."""

    def test_client_init_with_env_vars(self):
        """Test client initialization from environment variables."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test",
            "LANGFUSE_SECRET_KEY": "sk-lf-test",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }):
            client = LangfuseClient()
            assert client.public_key == "pk-lf-test"
            assert client.secret_key == "sk-lf-test"
            assert client.host == "https://test.langfuse.com"
            assert client.base_url == "https://test.langfuse.com/api/public"

    def test_client_init_with_params(self):
        """Test client initialization with explicit parameters."""
        client = LangfuseClient(
            public_key="pk-lf-explicit",
            secret_key="sk-lf-explicit",
            host="https://explicit.langfuse.com"
        )
        assert client.public_key == "pk-lf-explicit"
        assert client.secret_key == "sk-lf-explicit"
        assert client.host == "https://explicit.langfuse.com"

    def test_client_init_missing_public_key(self):
        """Test client raises error when public key is missing."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "",
            "LANGFUSE_SECRET_KEY": "sk-lf-test",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }, clear=True):
            with pytest.raises(ValueError, match="Missing Langfuse credentials"):
                LangfuseClient()

    def test_client_init_missing_secret_key(self):
        """Test client raises error when secret key is missing."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test",
            "LANGFUSE_SECRET_KEY": "",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }, clear=True):
            with pytest.raises(ValueError, match="Missing Langfuse credentials"):
                LangfuseClient()

    def test_client_init_missing_host(self):
        """Test client raises error when host is missing."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test",
            "LANGFUSE_SECRET_KEY": "sk-lf-test",
            "LANGFUSE_HOST": ""
        }, clear=True):
            with pytest.raises(ValueError, match="Missing Langfuse host"):
                LangfuseClient()

    def test_client_strips_trailing_slash(self):
        """Test client strips trailing slash from host."""
        client = LangfuseClient(
            public_key="pk-lf-test",
            secret_key="sk-lf-test",
            host="https://test.langfuse.com/"
        )
        assert client.host == "https://test.langfuse.com"

    def test_client_sets_auth(self):
        """Test client sets Basic Auth correctly."""
        client = LangfuseClient(
            public_key="pk-lf-test",
            secret_key="sk-lf-test",
            host="https://test.langfuse.com"
        )
        assert client.session.auth == ("pk-lf-test", "sk-lf-test")

    def test_client_sets_headers(self):
        """Test client sets correct headers."""
        client = LangfuseClient(
            public_key="pk-lf-test",
            secret_key="sk-lf-test",
            host="https://test.langfuse.com"
        )
        assert client.session.headers["Content-Type"] == "application/json"
        assert client.session.headers["Accept"] == "application/json"

    @patch("langfuse_client.requests.Session")
    def test_get_request(self, mock_session_class):
        """Test GET request is made correctly."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": []}
        mock_session.get.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = LangfuseClient(
            public_key="pk-lf-test",
            secret_key="sk-lf-test",
            host="https://test.langfuse.com"
        )
        result = client.get("/traces", params={"limit": 10})

        mock_session.get.assert_called_once_with(
            "https://test.langfuse.com/api/public/traces",
            params={"limit": 10}
        )
        assert result == {"data": []}

    @patch("langfuse_client.requests.Session")
    def test_post_request(self, mock_session_class):
        """Test POST request is made correctly."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"id": "new-id"}
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = LangfuseClient(
            public_key="pk-lf-test",
            secret_key="sk-lf-test",
            host="https://test.langfuse.com"
        )
        result = client.post("/scores", data={"name": "test"})

        mock_session.post.assert_called_once_with(
            "https://test.langfuse.com/api/public/scores",
            json={"name": "test"}
        )
        assert result == {"id": "new-id"}

    @patch("langfuse_client.requests.Session")
    def test_delete_request(self, mock_session_class):
        """Test DELETE request is made correctly."""
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = {"deleted": True}
        mock_session.delete.return_value = mock_response
        mock_session_class.return_value = mock_session

        client = LangfuseClient(
            public_key="pk-lf-test",
            secret_key="sk-lf-test",
            host="https://test.langfuse.com"
        )
        result = client.delete("/traces/abc123")

        mock_session.delete.assert_called_once_with(
            "https://test.langfuse.com/api/public/traces/abc123",
            params=None
        )
        assert result == {"deleted": True}


class TestGetClient:
    """Tests for get_client singleton function."""

    def test_get_client_returns_client(self):
        """Test get_client returns a LangfuseClient instance."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test",
            "LANGFUSE_SECRET_KEY": "sk-lf-test",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }):
            # Reset singleton
            import langfuse_client
            langfuse_client._client = None

            client = get_client()
            assert isinstance(client, LangfuseClient)

    def test_get_client_returns_singleton(self):
        """Test get_client returns same instance on multiple calls."""
        with patch.dict(os.environ, {
            "LANGFUSE_PUBLIC_KEY": "pk-lf-test",
            "LANGFUSE_SECRET_KEY": "sk-lf-test",
            "LANGFUSE_HOST": "https://test.langfuse.com"
        }):
            # Reset singleton
            import langfuse_client
            langfuse_client._client = None

            client1 = get_client()
            client2 = get_client()
            assert client1 is client2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
