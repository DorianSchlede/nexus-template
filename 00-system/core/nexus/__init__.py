"""
Nexus - Context loader and directive executor for Nexus-v4

This package provides the core functionality for:
- Loading startup context and system state detection
- Scanning projects and skills
- Managing memory files
- Syncing with upstream repository

Public API:
    from nexus import NexusService

    service = NexusService()
    result = service.startup()
"""

__version__ = "0.15.1"

# Dependency check - fail gracefully with helpful message
try:
    import yaml
except ImportError:
    raise ImportError(
        "PyYAML is required but not installed.\n"
        "Install it with: pip install pyyaml"
    )

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
    ProjectStatus,
    SystemState,
    Project,
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
    "ProjectStatus",
    "SystemState",
    "Project",
    "Skill",
    "Instructions",
    "StartupResult",
    # Service
    "NexusService",
]
