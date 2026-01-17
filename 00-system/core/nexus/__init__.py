"""
Nexus - Context loader and directive executor for Nexus-v4

This package provides the core functionality for:
- Loading startup context and system state detection
- Scanning builds and skills
- Managing memory files
- Syncing with upstream repository

Public API:
    from nexus import NexusService

    service = NexusService()
    result = service.startup()
"""

__version__ = "0.15.1"

# Dependency check - warn but don't fail (graceful degradation)
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    # Note: Some features require PyYAML (YAML frontmatter parsing)
    # Install with: pip install pyyaml

# Public API exports
from .config import (
    CHARS_PER_TOKEN,
    CONTEXT_WINDOW,
    METADATA_BUDGET_WARNING,
    BASH_OUTPUT_LIMIT,
    MANDATORY_MAPS,
    SYNC_PATHS,
    PROTECTED_PATHS,
    DEFAULT_UPSTREAM_URL,
)

from .models import (
    BuildStatus,
    SystemState,
    Build,
    Skill,
    Instructions,
    StartupResult,
)

# Service class
from .service import NexusService

__all__ = [
    # Version
    "__version__",
    # Config constants
    "CHARS_PER_TOKEN",
    "CONTEXT_WINDOW",
    "METADATA_BUDGET_WARNING",
    "BASH_OUTPUT_LIMIT",
    "MANDATORY_MAPS",
    "SYNC_PATHS",
    "PROTECTED_PATHS",
    "DEFAULT_UPSTREAM_URL",
    # Models
    "BuildStatus",
    "SystemState",
    "Build",
    "Skill",
    "Instructions",
    "StartupResult",
    # Service
    "NexusService",
]
