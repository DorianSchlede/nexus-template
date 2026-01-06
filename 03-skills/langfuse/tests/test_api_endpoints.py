"""Unit tests for all Langfuse API endpoint scripts."""

import os
import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

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


class TestListTraces:
    """Tests for list_traces endpoint."""

    def test_list_traces_default_params(self):
        """Test list_traces with default parameters."""
        with patch("list_traces.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": [], "meta": {"page": 1}}
            mock_get_client.return_value = mock_client

            from list_traces import list_traces
            result = list_traces()

            mock_client.get.assert_called_once()
            call_args = mock_client.get.call_args
            assert call_args[0][0] == "/traces"
            assert call_args[1]["params"]["limit"] == 50
            assert call_args[1]["params"]["page"] == 1

    def test_list_traces_with_limit(self):
        """Test list_traces with custom limit."""
        with patch("list_traces.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_traces import list_traces
            list_traces(limit=20)

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["limit"] == 20

    def test_list_traces_limit_capped_at_100(self):
        """Test list_traces caps limit at 100."""
        with patch("list_traces.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_traces import list_traces
            list_traces(limit=200)

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["limit"] == 100

    def test_list_traces_with_filters(self):
        """Test list_traces with all filters."""
        with patch("list_traces.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_traces import list_traces
            list_traces(
                user_id="user123",
                session_id="sess123",
                name="test-trace",
                from_timestamp="2025-01-01T00:00:00Z",
                to_timestamp="2025-12-31T23:59:59Z",
                order_by="timestamp",
                order="asc"
            )

            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["userId"] == "user123"
            assert params["sessionId"] == "sess123"
            assert params["name"] == "test-trace"
            assert params["fromTimestamp"] == "2025-01-01T00:00:00Z"
            assert params["toTimestamp"] == "2025-12-31T23:59:59Z"
            assert params["orderBy"] == "timestamp"
            assert params["order"] == "asc"


class TestGetTrace:
    """Tests for get_trace endpoint."""

    def test_get_trace(self):
        """Test get_trace with valid ID."""
        with patch("get_trace.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"id": "trace123", "name": "test"}
            mock_get_client.return_value = mock_client

            from get_trace import get_trace
            result = get_trace("trace123")

            mock_client.get.assert_called_once_with("/traces/trace123")
            assert result["id"] == "trace123"

    def test_get_trace_different_id(self):
        """Test get_trace with different ID."""
        with patch("get_trace.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"id": "abc-xyz"}
            mock_get_client.return_value = mock_client

            from get_trace import get_trace
            get_trace("abc-xyz")

            mock_client.get.assert_called_once_with("/traces/abc-xyz")


class TestListObservations:
    """Tests for list_observations endpoint."""

    def test_list_observations_default(self):
        """Test list_observations with defaults."""
        with patch("list_observations.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_observations import list_observations
            list_observations()

            call_args = mock_client.get.call_args
            assert call_args[0][0] == "/v2/observations"
            assert call_args[1]["params"]["limit"] == 50

    def test_list_observations_with_cursor(self):
        """Test list_observations with cursor pagination."""
        with patch("list_observations.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": [], "meta": {"nextCursor": "xyz"}}
            mock_get_client.return_value = mock_client

            from list_observations import list_observations
            list_observations(cursor="abc123")

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["cursor"] == "abc123"

    def test_list_observations_with_type_filter(self):
        """Test list_observations with type filter."""
        with patch("list_observations.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_observations import list_observations
            list_observations(obs_type="GENERATION")

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["type"] == "GENERATION"

    def test_list_observations_with_trace_filter(self):
        """Test list_observations filtered by trace."""
        with patch("list_observations.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_observations import list_observations
            list_observations(trace_id="trace123")

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["traceId"] == "trace123"


class TestGetObservation:
    """Tests for get_observation endpoint."""

    def test_get_observation(self):
        """Test get_observation with valid ID."""
        with patch("get_observation.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"id": "obs123", "type": "SPAN"}
            mock_get_client.return_value = mock_client

            from get_observation import get_observation
            result = get_observation("obs123")

            mock_client.get.assert_called_once_with("/observations/obs123")
            assert result["id"] == "obs123"


class TestListSessions:
    """Tests for list_sessions endpoint."""

    def test_list_sessions_default(self):
        """Test list_sessions with defaults."""
        with patch("list_sessions.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_sessions import list_sessions
            list_sessions()

            call_args = mock_client.get.call_args
            assert call_args[0][0] == "/sessions"
            assert call_args[1]["params"]["limit"] == 50
            assert call_args[1]["params"]["page"] == 1

    def test_list_sessions_with_time_filter(self):
        """Test list_sessions with time filters."""
        with patch("list_sessions.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_sessions import list_sessions
            list_sessions(
                from_timestamp="2025-01-01T00:00:00Z",
                to_timestamp="2025-12-31T23:59:59Z"
            )

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["fromTimestamp"] == "2025-01-01T00:00:00Z"
            assert call_args[1]["params"]["toTimestamp"] == "2025-12-31T23:59:59Z"


class TestGetSession:
    """Tests for get_session endpoint."""

    def test_get_session(self):
        """Test get_session with valid ID."""
        with patch("get_session.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"id": "sess123", "traces": []}
            mock_get_client.return_value = mock_client

            from get_session import get_session
            result = get_session("sess123")

            mock_client.get.assert_called_once_with("/sessions/sess123")
            assert result["id"] == "sess123"


class TestListScores:
    """Tests for list_scores endpoint."""

    def test_list_scores_default(self):
        """Test list_scores with defaults."""
        with patch("list_scores.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_scores import list_scores
            list_scores()

            call_args = mock_client.get.call_args
            assert call_args[0][0] == "/v2/scores"
            assert call_args[1]["params"]["limit"] == 50

    def test_list_scores_with_filters(self):
        """Test list_scores with all filters."""
        with patch("list_scores.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_scores import list_scores
            list_scores(
                trace_id="trace123",
                observation_id="obs123",
                name="accuracy",
                source="API"
            )

            call_args = mock_client.get.call_args
            params = call_args[1]["params"]
            assert params["traceId"] == "trace123"
            assert params["observationId"] == "obs123"
            assert params["name"] == "accuracy"
            assert params["source"] == "API"


class TestGetScore:
    """Tests for get_score endpoint."""

    def test_get_score(self):
        """Test get_score with valid ID."""
        with patch("get_score.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"id": "score123", "value": 0.95}
            mock_get_client.return_value = mock_client

            from get_score import get_score
            result = get_score("score123")

            mock_client.get.assert_called_once_with("/v2/scores/score123")
            assert result["value"] == 0.95


class TestListModels:
    """Tests for list_models endpoint."""

    def test_list_models_default(self):
        """Test list_models with defaults."""
        with patch("list_models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_models import list_models
            list_models()

            call_args = mock_client.get.call_args
            assert call_args[0][0] == "/models"
            assert call_args[1]["params"]["limit"] == 50
            assert call_args[1]["params"]["page"] == 1

    def test_list_models_with_pagination(self):
        """Test list_models with pagination."""
        with patch("list_models.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": []}
            mock_get_client.return_value = mock_client

            from list_models import list_models
            list_models(limit=25, page=3)

            call_args = mock_client.get.call_args
            assert call_args[1]["params"]["limit"] == 25
            assert call_args[1]["params"]["page"] == 3


class TestGetModel:
    """Tests for get_model endpoint."""

    def test_get_model(self):
        """Test get_model with valid ID."""
        with patch("get_model.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"id": "model123", "name": "gpt-4"}
            mock_get_client.return_value = mock_client

            from get_model import get_model
            result = get_model("model123")

            mock_client.get.assert_called_once_with("/models/model123")
            assert result["name"] == "gpt-4"


class TestGetProject:
    """Tests for get_project endpoint."""

    def test_get_project(self):
        """Test get_project returns current project."""
        with patch("get_project.get_client") as mock_get_client:
            mock_client = MagicMock()
            mock_client.get.return_value = {"data": [{"id": "proj123", "name": "My Project"}]}
            mock_get_client.return_value = mock_client

            from get_project import get_project
            result = get_project()

            mock_client.get.assert_called_once_with("/projects")
            assert result["data"][0]["name"] == "My Project"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
