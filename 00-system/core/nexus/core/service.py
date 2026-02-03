"""
NexusService - Main service layer for Nexus.

This module provides the primary API for the Nexus system:
- startup() - Load session context
- load_build() - Load specific build
- load_skill() - Load specific skill
- check_updates() - Check for upstream updates
- sync() - Sync from upstream
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from ..utils.config import MANDATORY_MAPS, MEMORY_DIR
from .loaders import (
    create_smart_defaults,
    detect_configured_integrations,
    load_build,
    load_skill_slim,
    scan_builds,
    scan_skills,
)
from .models import SystemState
from ..state.state import (
    build_display_hints,
    build_instructions,
    build_pending_onboarding,
    build_stats,
    detect_system_state,
    extract_learning_completed,
)
from .sync import check_for_updates, sync_from_upstream
from ..utils.utils import embed_file_contents, is_template_file


class NexusService:
    """
    Main service class for Nexus operations.

    Provides a clean API for all Nexus functionality.
    """

    def __init__(self, base_path: str = "."):
        """
        Initialize NexusService.

        Args:
            base_path: Root path to Nexus installation
        """
        self.base_path = Path(base_path)

    def startup(
        self,
        include_metadata: bool = True,
        resume_mode: bool = False,
        check_updates: bool = True,
    ) -> Dict[str, Any]:
        """
        Load startup context and determine complete execution plan.

        This is the MASTER CONTROLLER for Nexus startup.
        Analyzes system state and returns EXACTLY what the AI should do.

        Args:
            include_metadata: If True, include full build/skill metadata
            resume_mode: If True, skip menu display (resuming from context summary)
            check_updates: If True, check for upstream updates

        Returns:
            Complete startup result with state, instructions, memory, and metadata
        """
        # ATTENTION OPTIMIZATION: Instructions at START for primacy effect
        # They will also be repeated at END for recency effect (see below)
        result = {
            "loaded_at": datetime.now().isoformat(),
            "bundle": "resume" if resume_mode else "startup",
            ">>> EXECUTE_FIRST <<<": None,  # Placeholder - filled with instructions below
            "system_state": None,
            "memory_content": {},
            "metadata": {},
            "stats": {},
            ">>> EXECUTE_AFTER_READING <<<": None,  # Repeated at end for recency
        }

        # Track files to embed
        files_to_embed = []

        # Step 1: Load mandatory navigation maps
        for map_path in MANDATORY_MAPS:
            full_path = self.base_path / map_path
            if full_path.exists():
                files_to_embed.append(str(full_path))

        # Step 2: Check optional memory files
        memory_path = self.base_path / MEMORY_DIR
        optional_files = {
            "memory_map": memory_path / "memory-map.md",
            "goals": memory_path / "goals.md",
            "user_config": memory_path / "user-config.yaml",
        }

        files_exist = {key: path.exists() for key, path in optional_files.items()}

        # Add existing optional files to embed list
        for key, path in optional_files.items():
            if files_exist[key]:
                files_to_embed.append(str(path))

        # Step 3: Scan builds and skills
        if include_metadata:
            builds = scan_builds(str(self.base_path))
            skills = scan_skills(str(self.base_path))
            result["metadata"]["builds"] = builds
            result["metadata"]["skills"] = skills
        else:
            builds = scan_builds(str(self.base_path))
            skills = []
            result["metadata"] = {"note": "Use --metadata for full build/skill data"}

        # Step 4: Handle first-time setup
        if not files_exist["goals"]:
            defaults_result = create_smart_defaults(str(self.base_path))
            result["smart_defaults_created"] = defaults_result

            # Re-check files after creation
            for key, path in optional_files.items():
                if path.exists() and str(path) not in files_to_embed:
                    files_to_embed.append(str(path))
                    files_exist[key] = True

        # Step 5: Detect system state
        state = detect_system_state(
            files_exist=files_exist,
            goals_path=optional_files["goals"],
            builds=builds,
            resume_mode=resume_mode,
        )
        result["system_state"] = state.value

        # Step 6: Check for updates (non-blocking)
        update_info = {
            "update_available": False,
            "local_version": "unknown",
            "upstream_version": None,
            "checked": False,
        }
        if check_updates:
            try:
                update_info = check_for_updates(str(self.base_path))
            except Exception:
                pass  # Network/git errors should NOT fail startup

        # Step 7: Build stats
        stats = build_stats(
            base_path=self.base_path,
            memory_content={},  # Will be populated below
            builds=builds,
            skills=skills,
            files_exist=files_exist,
            goals_path=optional_files["goals"],
            config_path=optional_files["user_config"],
            update_info=update_info,
            configured_integrations=detect_configured_integrations(str(self.base_path)),
        )
        result["stats"] = stats

        # Step 8: Build instructions
        instructions = build_instructions(
            state=state,
            builds=builds,
            display_hints=stats.get("display_hints", []),
        )

        # ATTENTION SANDWICH: Instructions at START and END of result
        # This exploits both primacy and recency effects in LLM attention
        result[">>> EXECUTE_FIRST <<<"] = instructions
        result[">>> EXECUTE_AFTER_READING <<<"] = instructions  # Repeated for recency

        # Step 9: Embed memory content
        if files_to_embed:
            result["memory_content"] = embed_file_contents(files_to_embed)
            result["stats"]["files_embedded"] = len(result["memory_content"])

        return result

    def load_build(self, build_id: str, part: int = 0) -> Dict[str, Any]:
        """
        Load complete build context.

        Args:
            build_id: Build ID or folder name prefix
            part: Which part to load (0=auto, 1=essential, 2=references)

        Returns:
            Build context with files and metadata
        """
        return load_build(build_id, str(self.base_path), part=part)

    def load_skill(self, skill_name: str) -> Dict[str, Any]:
        """
        Load skill context (file tree + SKILL.md only, no auto-loaded references).

        Args:
            skill_name: Name of the skill to load

        Returns:
            Skill context with file tree, SKILL.md content, and paths to load more
        """
        return load_skill_slim(skill_name, str(self.base_path))

    def load_metadata(self) -> Dict[str, Any]:
        """
        Load only build and skill metadata.

        Returns:
            Metadata only (no memory content)
        """
        from datetime import datetime

        result = {
            "loaded_at": datetime.now().isoformat(),
            "bundle": "metadata",
            "builds": scan_builds(str(self.base_path), minimal=True),
            "skills": scan_skills(str(self.base_path), minimal=True),
        }

        result["stats"] = {
            "total_builds": len(result["builds"]),
            "total_skills": len(result["skills"]),
            "active_builds": len([p for p in result["builds"] if p.get("status") == "IN_PROGRESS"]),
        }

        return result

    def list_builds(self, full: bool = False) -> Dict[str, Any]:
        """
        List all builds.

        Args:
            full: If True, return all fields; if False, minimal fields

        Returns:
            Dict with builds list
        """
        builds = scan_builds(str(self.base_path), minimal=not full)
        return {"builds": builds}

    def list_skills(self, full: bool = False) -> Dict[str, Any]:
        """
        List all skills.

        Args:
            full: If True, return all fields; if False, minimal fields

        Returns:
            Dict with skills list
        """
        skills = scan_skills(str(self.base_path), minimal=not full)
        return {"skills": skills}

    def check_updates(self) -> Dict[str, Any]:
        """
        Check for upstream updates.

        Returns:
            Update status and version info
        """
        return check_for_updates(str(self.base_path))

    def sync(self, dry_run: bool = False, force: bool = False) -> Dict[str, Any]:
        """
        Sync system files from upstream.

        Args:
            dry_run: If True, show what would change without changing
            force: If True, skip confirmation prompts

        Returns:
            Sync results
        """
        return sync_from_upstream(str(self.base_path), dry_run=dry_run, force=force)
