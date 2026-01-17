"""
Git sync operations for Nexus.

This module handles:
- Running git commands
- Checking for upstream updates
- Syncing system files from upstream
- Version management
"""

import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False
    yaml = None

from .config import DEFAULT_UPSTREAM_URL, SYNC_PATHS
from .utils import parse_simple_yaml


def run_git_command(args: List[str], cwd: str = None) -> Tuple[bool, str]:
    """
    Run a git command and return (success, output).

    Args:
        args: Git command arguments (e.g., ['status', '--porcelain'])
        cwd: Working directory (default: current directory)

    Returns:
        Tuple of (success: bool, output: str)
    """
    try:
        result = subprocess.run(
            ["git"] + args,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return result.returncode == 0, output
    except subprocess.TimeoutExpired:
        return False, "Git command timed out"
    except FileNotFoundError:
        return False, "Git is not installed"
    except Exception as e:
        return False, str(e)


def get_local_version(base_path: str) -> str:
    """
    Read local version from 00-system/VERSION file.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Version string or "unknown"
    """
    version_file = Path(base_path) / "00-system" / "VERSION"
    try:
        if version_file.exists():
            return version_file.read_text(encoding="utf-8").strip()
        return "unknown"
    except Exception:
        return "unknown"


def get_upstream_url(base_path: str) -> str:
    """
    Get upstream URL from user-config.yaml or use default.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Upstream repository URL
    """
    config_path = Path(base_path) / "01-memory" / "user-config.yaml"

    if config_path.exists():
        try:
            content = config_path.read_text(encoding="utf-8")
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 2:
                    if HAS_YAML:
                        config = yaml.safe_load(parts[1])
                    else:
                        config = parse_simple_yaml(parts[1])
                    if config and "sync" in config:
                        url = config["sync"].get("upstream_url")
                        if url:
                            return url
        except Exception:
            pass

    return DEFAULT_UPSTREAM_URL


def ensure_upstream_remote(base_path: str) -> Tuple[bool, str]:
    """
    Ensure 'upstream' remote exists. Add it if missing.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Tuple of (success, message/url)
    """
    # Check if upstream already exists
    success, output = run_git_command(["remote", "get-url", "upstream"], cwd=base_path)

    if success:
        return True, output  # Already configured

    # Add upstream remote
    upstream_url = get_upstream_url(base_path)
    success, output = run_git_command(
        ["remote", "add", "upstream", upstream_url], cwd=base_path
    )

    if success:
        return True, upstream_url
    else:
        return False, f"Failed to add upstream: {output}"


def check_for_updates(base_path: str) -> Dict[str, Any]:
    """
    Check if updates are available from upstream.

    This is designed to be FAST - called on every startup.
    Only fetches refs, doesn't download content.

    Args:
        base_path: Root path to Nexus installation

    Returns:
        Dict with update status and version info
    """
    result = {
        "checked": True,
        "update_available": False,
        "local_version": get_local_version(base_path),
        "upstream_version": None,
        "error": None,
    }

    # Pre-flight: Check if we're in a git repo
    success, _ = run_git_command(["rev-parse", "--git-dir"], cwd=base_path)
    if not success:
        result["checked"] = False
        result["error"] = "Not a git repository"
        return result

    # Ensure upstream remote exists
    success, upstream_url = ensure_upstream_remote(base_path)
    if not success:
        result["checked"] = False
        result["error"] = upstream_url  # Contains error message
        return result

    result["upstream_url"] = upstream_url

    # Fetch upstream (just refs, fast)
    success, output = run_git_command(["fetch", "upstream", "--quiet"], cwd=base_path)
    if not success:
        # Network error - don't fail startup, just note it
        result["checked"] = False
        result["error"] = f"Could not reach upstream: {output}"
        return result

    # Compare local vs upstream 00-system/
    # Get hash of local 00-system/
    success, local_hash = run_git_command(
        ["rev-parse", "HEAD:00-system"],
        cwd=base_path,
    )
    if not success:
        local_hash = "unknown"

    # Get hash of upstream 00-system/
    success, upstream_hash = run_git_command(
        ["rev-parse", "upstream/main:00-system"],
        cwd=base_path,
    )
    if not success:
        result["error"] = f"Could not read upstream version: {output}"
        return result

    # Try to read upstream VERSION file
    success, upstream_version = run_git_command(
        ["show", "upstream/main:00-system/VERSION"],
        cwd=base_path,
    )
    if success:
        result["upstream_version"] = upstream_version.strip()

    # Compare hashes
    if local_hash != upstream_hash:
        result["update_available"] = True

        # Get list of changed files
        success, diff_output = run_git_command(
            [
                "diff",
                "--name-only",
                "HEAD",
                "upstream/main",
                "--",
                "00-system/",
                "CLAUDE.md",
                "README.md",
            ],
            cwd=base_path,
        )
        if success and diff_output:
            result["changed_files"] = diff_output.split("\n")
            result["changes_count"] = len(result["changed_files"])

    return result


def sync_from_upstream(
    base_path: str, dry_run: bool = False, force: bool = False
) -> Dict[str, Any]:
    """
    Sync system files from upstream repository.

    Args:
        base_path: Root path to Nexus installation
        dry_run: If True, show what would change without changing
        force: If True, skip confirmation prompts

    Returns:
        Dict with sync results
    """
    result = {
        "success": False,
        "dry_run": dry_run,
        "local_version": get_local_version(base_path),
        "upstream_version": None,
        "files_updated": [],
        "backup_path": None,
        "error": None,
    }

    # Pre-flight checks
    # 1. Check git installed and we're in a repo
    success, _ = run_git_command(["rev-parse", "--git-dir"], cwd=base_path)
    if not success:
        result["error"] = "Not a git repository"
        return result

    # 2. Check for uncommitted changes (warn user)
    success, status_output = run_git_command(["status", "--porcelain"], cwd=base_path)
    if success and status_output and not force:
        result["error"] = "Uncommitted changes detected. Commit first or use --force."
        result["uncommitted_changes"] = status_output.split("\n")
        return result

    # 3. Ensure upstream exists and fetch
    success, upstream_url = ensure_upstream_remote(base_path)
    if not success:
        result["error"] = upstream_url
        return result

    result["upstream_url"] = upstream_url

    success, _ = run_git_command(["fetch", "upstream"], cwd=base_path)
    if not success:
        result["error"] = "Could not fetch from upstream. Check your internet connection."
        return result

    # Get upstream version
    success, upstream_version = run_git_command(
        ["show", "upstream/main:00-system/VERSION"],
        cwd=base_path,
    )
    if success:
        result["upstream_version"] = upstream_version.strip()

    # Get changed files
    success, diff_output = run_git_command(
        [
            "diff",
            "--name-only",
            "HEAD",
            "upstream/main",
            "--",
            "00-system/",
            "CLAUDE.md",
            "README.md",
        ],
        cwd=base_path,
    )

    if not success or not diff_output.strip():
        result["success"] = True
        result["message"] = "Already up-to-date"
        return result

    changed_files = [f for f in diff_output.strip().split("\n") if f]
    result["files_to_update"] = changed_files

    # Dry run - just show what would change
    if dry_run:
        result["success"] = True
        result["message"] = f"Would update {len(changed_files)} files"
        return result

    # Create backup of local system files that will be overwritten
    backup_dir = Path(base_path) / ".sync-backup" / datetime.now().strftime(
        "%Y-%m-%d-%H%M%S"
    )
    backup_dir.mkdir(parents=True, exist_ok=True)
    result["backup_path"] = str(backup_dir)

    for file_path in changed_files:
        local_file = Path(base_path) / file_path
        if local_file.exists():
            backup_file = backup_dir / file_path
            backup_file.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(local_file, backup_file)
            except Exception as e:
                result["error"] = f"Backup failed: {e}"
                return result

    # Perform the sync - checkout system files from upstream
    for sync_path in SYNC_PATHS:
        success, output = run_git_command(
            ["checkout", "upstream/main", "--", sync_path],
            cwd=base_path,
        )
        if success:
            result["files_updated"].append(sync_path)
        else:
            # Non-fatal: file might not exist in upstream
            pass

    result["success"] = True
    result["message"] = f"Updated {len(result['files_updated'])} paths from upstream"

    return result
