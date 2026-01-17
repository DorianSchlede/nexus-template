"""
Data models for Nexus.

This module defines type-safe dataclasses and enums for all
domain objects used throughout the Nexus system.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


class BuildStatus(Enum):
    """Build lifecycle states."""

    PLANNING = "PLANNING"
    IN_PROGRESS = "IN_PROGRESS"
    ON_HOLD = "ON_HOLD"
    COMPLETE = "COMPLETE"
    ARCHIVED = "ARCHIVED"


class SystemState(Enum):
    """System state classifications for startup routing."""

    # First time user - smart defaults created
    FIRST_TIME_WITH_DEFAULTS = "first_time_with_defaults"

    # Goals exist but still templates
    GOALS_NOT_PERSONALIZED = "goals_not_personalized"

    # Operational with active builds
    OPERATIONAL_WITH_ACTIVE_BUILDS = "operational_with_active_builds"

    # Operational with no active builds
    OPERATIONAL = "operational"

    # Resume mode (after context summary)
    RESUME = "resume"


@dataclass
class Build:
    """Represents a Nexus build with metadata and progress."""

    id: str
    name: str
    status: BuildStatus
    description: str = ""
    created: Optional[str] = None
    updated: Optional[str] = None

    # Progress tracking
    progress: float = 0.0  # 0.0 to 1.0
    tasks_total: int = 0
    tasks_completed: int = 0
    current_task: Optional[str] = None

    # Flags
    onboarding: bool = False

    # File paths (for internal use)
    _file_path: Optional[str] = None
    _file_name: Optional[str] = None

    def to_dict(self, minimal: bool = True) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        if minimal:
            return {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "status": self.status.value if isinstance(self.status, BuildStatus) else self.status,
                "onboarding": self.onboarding,
                "created": self.created,
                "updated": self.updated,
                "progress": self.progress,
                "tasks_total": self.tasks_total,
                "tasks_completed": self.tasks_completed,
                "current_task": self.current_task,
                "_file_path": self._file_path,
                "_file_name": self._file_name,
            }
        # Full representation includes all fields
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status.value if isinstance(self.status, BuildStatus) else self.status,
            "onboarding": self.onboarding,
            "created": self.created,
            "updated": self.updated,
            "progress": self.progress,
            "tasks_total": self.tasks_total,
            "tasks_completed": self.tasks_completed,
            "current_task": self.current_task,
            "_file_path": self._file_path,
            "_file_name": self._file_name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Build":
        """Create a Build from a dictionary."""
        status = data.get("status", "PLANNING")
        if isinstance(status, str):
            try:
                status = BuildStatus(status)
            except ValueError:
                status = BuildStatus.PLANNING

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            status=status,
            description=data.get("description", ""),
            created=data.get("created"),
            updated=data.get("updated"),
            progress=data.get("progress", 0.0),
            tasks_total=data.get("tasks_total", 0),
            tasks_completed=data.get("tasks_completed", 0),
            current_task=data.get("current_task"),
            onboarding=data.get("onboarding", False),
            _file_path=data.get("_file_path"),
            _file_name=data.get("_file_name"),
        )


@dataclass
class Skill:
    """Represents a Nexus skill with metadata."""

    name: str
    description: str = ""

    # File paths (for internal use)
    _file_path: Optional[str] = None
    _file_name: Optional[str] = None

    def to_dict(self, minimal: bool = True) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "description": self.description,
            "_file_path": self._file_path,
            "_file_name": self._file_name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create a Skill from a dictionary."""
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            _file_path=data.get("_file_path"),
            _file_name=data.get("_file_name"),
        )


@dataclass
class Integration:
    """Represents a configured integration."""

    name: str
    slug: str
    skills: List[str] = field(default_factory=list)
    active: bool = False
    required_env: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "slug": self.slug,
            "skills": self.skills,
            "active": self.active,
            "required_env": self.required_env,
        }


@dataclass
class Instructions:
    """Execution instructions returned by the loader."""

    action: str  # "display_menu", "continue_working", "load_and_execute_build"
    execution_mode: str  # "interactive", "immediate"
    message: str
    reason: str
    workflow: List[str] = field(default_factory=list)
    display_hints: List[str] = field(default_factory=list)

    # Optional fields for specific actions
    suggest_onboarding: bool = False
    suggest_build: Optional[str] = None
    build_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "action": self.action,
            "execution_mode": self.execution_mode,
            "message": self.message,
            "reason": self.reason,
            "workflow": self.workflow,
        }
        if self.display_hints:
            result["display_hints"] = self.display_hints
        if self.suggest_onboarding:
            result["suggest_onboarding"] = self.suggest_onboarding
        if self.suggest_build:
            result["suggest_build"] = self.suggest_build
        if self.build_id:
            result["build_id"] = self.build_id
        return result


@dataclass
class OnboardingSkill:
    """Represents a pending onboarding skill."""

    key: str
    name: str
    trigger: str
    priority: str
    time: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "key": self.key,
            "name": self.name,
            "trigger": self.trigger,
            "priority": self.priority,
            "time": self.time,
        }


@dataclass
class Stats:
    """System statistics for menu display."""

    files_embedded: int = 0
    mandatory_maps_loaded: int = 0
    mandatory_maps_total: int = 0
    total_builds: int = 0
    active_builds: int = 0
    non_complete_builds: int = 0
    total_skills: int = 0
    user_skills: int = 0
    goals_personalized: bool = False
    workspace_configured: bool = False
    integrations_configured: bool = False
    configured_integrations: List[Dict[str, Any]] = field(default_factory=list)
    learning_completed: Dict[str, bool] = field(default_factory=dict)
    pending_onboarding: List[Dict[str, Any]] = field(default_factory=list)
    onboarding_complete: bool = False
    update_available: bool = False
    update_info: Dict[str, Any] = field(default_factory=dict)
    display_hints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "display_hints": self.display_hints,
            "files_embedded": self.files_embedded,
            "mandatory_maps_loaded": self.mandatory_maps_loaded,
            "mandatory_maps_total": self.mandatory_maps_total,
            "total_builds": self.total_builds,
            "active_builds": self.active_builds,
            "non_complete_builds": self.non_complete_builds,
            "total_skills": self.total_skills,
            "user_skills": self.user_skills,
            "goals_personalized": self.goals_personalized,
            "workspace_configured": self.workspace_configured,
            "integrations_configured": self.integrations_configured,
            "configured_integrations": self.configured_integrations,
            "learning_completed": self.learning_completed,
            "pending_onboarding": self.pending_onboarding,
            "onboarding_complete": self.onboarding_complete,
            "update_available": self.update_available,
            "update_info": self.update_info,
        }


@dataclass
class StartupResult:
    """Complete result from startup/resume operations."""

    loaded_at: str
    bundle: str  # "startup", "resume", "build", "skill", "metadata"
    system_state: Optional[str] = None
    memory_content: Dict[str, str] = field(default_factory=dict)
    instructions: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    stats: Dict[str, Any] = field(default_factory=dict)

    # Optional fields
    smart_defaults_created: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "loaded_at": self.loaded_at,
            "bundle": self.bundle,
            "system_state": self.system_state,
            "memory_content": self.memory_content,
            "instructions": self.instructions,
            "metadata": self.metadata,
            "stats": self.stats,
        }
        if self.smart_defaults_created:
            result["smart_defaults_created"] = self.smart_defaults_created
        return result

    @classmethod
    def now(cls, bundle: str = "startup") -> "StartupResult":
        """Create a new StartupResult with current timestamp."""
        return cls(
            loaded_at=datetime.now().isoformat(),
            bundle=bundle,
        )
