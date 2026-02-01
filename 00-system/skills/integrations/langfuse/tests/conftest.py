"""Pytest configuration and fixtures for Langfuse tests."""

import os
import sys
from pathlib import Path

import pytest

# Load .env file for tests
from dotenv import load_dotenv
load_dotenv()

# Add all script paths to sys.path
base_path = Path(__file__).parent.parent

script_paths = [
    base_path / "langfuse-master" / "scripts",
    base_path / "langfuse-list-traces" / "scripts",
    base_path / "langfuse-get-trace" / "scripts",
    base_path / "langfuse-list-observations" / "scripts",
    base_path / "langfuse-get-observation" / "scripts",
    base_path / "langfuse-list-sessions" / "scripts",
    base_path / "langfuse-get-session" / "scripts",
    base_path / "langfuse-list-scores" / "scripts",
    base_path / "langfuse-get-score" / "scripts",
    base_path / "langfuse-list-models" / "scripts",
    base_path / "langfuse-get-model" / "scripts",
    base_path / "langfuse-get-project" / "scripts",
]

for path in script_paths:
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))


@pytest.fixture(scope="session")
def langfuse_configured():
    """Check if Langfuse is configured."""
    return all([
        os.getenv("LANGFUSE_PUBLIC_KEY"),
        os.getenv("LANGFUSE_SECRET_KEY"),
        os.getenv("LANGFUSE_HOST")
    ])


@pytest.fixture
def reset_client_singleton():
    """Reset the client singleton before each test."""
    import langfuse_client
    langfuse_client._client = None
    yield
    langfuse_client._client = None
