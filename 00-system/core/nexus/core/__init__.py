"""
Core modules for Nexus.

This package contains the core functionality for:
- loaders: Scanning and loading builds, skills, memory files
- models: Data models (Build, Skill, etc.)
- roadmap: Roadmap parsing, status derivation, sync functions
- service: Service layer for CLI commands
- sync: Synchronization utilities
"""

from .roadmap import (
    # Schema constants
    REQUIRED_FIELDS,
    OPTIONAL_FIELDS,
    VALID_TYPES,
    VALID_PRIORITIES,
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_NOT_STARTED,
    # Slug matching
    slugify,
    names_match,
    # Parsing
    load_roadmap,
    save_roadmap,
    # Status derivation
    derive_item_status,
    # Sync (forwards)
    link_roadmap_item,
    mark_roadmap_complete,
    # Sync (backwards)
    sync_roadmap_backwards,
    # Summary
    get_roadmap_summary,
    format_roadmap_line,
)

__all__ = [
    # Roadmap schema
    "REQUIRED_FIELDS",
    "OPTIONAL_FIELDS",
    "VALID_TYPES",
    "VALID_PRIORITIES",
    "STATUS_COMPLETED",
    "STATUS_IN_PROGRESS",
    "STATUS_NOT_STARTED",
    # Roadmap functions
    "slugify",
    "names_match",
    "load_roadmap",
    "save_roadmap",
    "derive_item_status",
    "link_roadmap_item",
    "mark_roadmap_complete",
    "sync_roadmap_backwards",
    "get_roadmap_summary",
    "format_roadmap_line",
]
