"""Integration tests for Langfuse API (uses real API)."""

import os
import sys
import pytest
from pathlib import Path

# Skip all tests if env vars not set
pytestmark = pytest.mark.skipif(
    not all([
        os.getenv("LANGFUSE_PUBLIC_KEY"),
        os.getenv("LANGFUSE_SECRET_KEY"),
        os.getenv("LANGFUSE_HOST")
    ]),
    reason="Langfuse credentials not configured"
)

# Add paths for imports
base_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_path / "langfuse-master" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-list-traces" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-get-trace" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-list-observations" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-get-observation" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-list-sessions" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-get-session" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-list-scores" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-get-score" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-list-models" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-get-model" / "scripts"))
sys.path.insert(0, str(base_path / "langfuse-get-project" / "scripts"))


class TestIntegrationClient:
    """Integration tests for Langfuse client."""

    def test_client_connects(self):
        """Test client can connect to Langfuse."""
        from langfuse_client import get_client
        client = get_client()
        assert client is not None
        assert client.host is not None


class TestIntegrationProject:
    """Integration tests for project endpoint."""

    def test_get_project_returns_data(self):
        """Test get_project returns project data."""
        from get_project import get_project
        result = get_project()

        assert "data" in result
        assert isinstance(result["data"], list)
        assert len(result["data"]) > 0
        assert "id" in result["data"][0]
        assert "name" in result["data"][0]


class TestIntegrationTraces:
    """Integration tests for traces endpoints."""

    def test_list_traces_returns_data(self):
        """Test list_traces returns trace data."""
        from list_traces import list_traces
        result = list_traces(limit=5)

        assert "data" in result
        assert "meta" in result
        assert isinstance(result["data"], list)

    def test_list_traces_pagination(self):
        """Test list_traces pagination works."""
        from list_traces import list_traces
        result = list_traces(limit=2, page=1)

        assert "meta" in result
        assert "page" in result["meta"]
        assert result["meta"]["page"] == 1

    def test_get_trace_with_valid_id(self):
        """Test get_trace with a valid trace ID."""
        from list_traces import list_traces
        from get_trace import get_trace

        # First get a trace ID
        traces = list_traces(limit=1)
        if traces["data"]:
            trace_id = traces["data"][0]["id"]
            result = get_trace(trace_id)

            assert result is not None
            assert result["id"] == trace_id


class TestIntegrationObservations:
    """Integration tests for observations endpoints."""

    def test_list_observations_returns_data(self):
        """Test list_observations returns observation data."""
        from list_observations import list_observations
        result = list_observations(limit=5)

        assert "data" in result
        assert isinstance(result["data"], list)

    def test_list_observations_by_type(self):
        """Test list_observations filtered by type."""
        from list_observations import list_observations
        result = list_observations(limit=5, obs_type="GENERATION")

        assert "data" in result
        # All returned observations should be GENERATION type
        for obs in result["data"]:
            assert obs.get("type") == "GENERATION"


class TestIntegrationSessions:
    """Integration tests for sessions endpoints."""

    def test_list_sessions_returns_data(self):
        """Test list_sessions returns session data."""
        from list_sessions import list_sessions
        result = list_sessions(limit=5)

        assert "data" in result
        assert isinstance(result["data"], list)


class TestIntegrationScores:
    """Integration tests for scores endpoints."""

    def test_list_scores_returns_data(self):
        """Test list_scores returns score data."""
        from list_scores import list_scores
        result = list_scores(limit=5)

        assert "data" in result
        assert isinstance(result["data"], list)


class TestIntegrationModels:
    """Integration tests for models endpoints."""

    def test_list_models_returns_data(self):
        """Test list_models returns model data."""
        from list_models import list_models
        result = list_models(limit=10)

        assert "data" in result
        assert isinstance(result["data"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
