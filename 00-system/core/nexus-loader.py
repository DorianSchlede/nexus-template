#!/usr/bin/env python3
"""
nexus-loader.py - Context loader and directive executor for Nexus

This is a thin CLI wrapper that delegates to the nexus package.

Usage:
    python nexus-loader.py --startup           # Load session context + return instructions
    python nexus-loader.py --resume            # Resume from context summary
    python nexus-loader.py --project ID        # Load specific project
    python nexus-loader.py --skill name        # Load specific skill
    python nexus-loader.py --list-projects     # Scan project metadata
    python nexus-loader.py --list-skills       # Scan skill metadata
    python nexus-loader.py --metadata          # Load only metadata
    python nexus-loader.py --check-update      # Check if upstream updates available
    python nexus-loader.py --sync              # Sync system files from upstream
"""

import sys
import json
import argparse
from pathlib import Path

# Add the core directory to path for nexus package import
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from nexus import NexusService
from nexus.config import BASH_OUTPUT_LIMIT, METADATA_BUDGET_WARNING
from nexus.utils import calculate_bundle_tokens

# =============================================================================
# BACKWARD COMPATIBILITY SHIM
# These functions are exported for tests and direct imports
# =============================================================================


def load_startup(base_path: str = ".", include_metadata: bool = True,
                 resume_mode: bool = False, check_updates: bool = True):
    """Backward compatible wrapper for NexusService.startup()"""
    service = NexusService(base_path)
    return service.startup(
        include_metadata=include_metadata,
        resume_mode=resume_mode,
        check_updates=check_updates
    )


def load_project(project_id: str, base_path: str = "."):
    """Backward compatible wrapper for NexusService.load_project()"""
    service = NexusService(base_path)
    return service.load_project(project_id)


def load_skill(skill_name: str, base_path: str = "."):
    """Backward compatible wrapper for NexusService.load_skill()"""
    service = NexusService(base_path)
    return service.load_skill(skill_name)


def load_metadata(base_path: str = "."):
    """Backward compatible wrapper for NexusService.load_metadata()"""
    service = NexusService(base_path)
    return service.load_metadata()


def scan_projects(base_path: str = ".", minimal: bool = True):
    """Backward compatible wrapper for project scanning"""
    from nexus.loaders import scan_projects as _scan_projects
    return _scan_projects(base_path, minimal)


def scan_skills(base_path: str = ".", minimal: bool = True):
    """Backward compatible wrapper for skill scanning"""
    from nexus.loaders import scan_skills as _scan_skills
    return _scan_skills(base_path, minimal)


def check_for_updates(base_path: str = "."):
    """Backward compatible wrapper for update checking"""
    service = NexusService(base_path)
    return service.check_updates()


def sync_from_upstream(base_path: str = ".", dry_run: bool = False, force: bool = False):
    """Backward compatible wrapper for sync"""
    service = NexusService(base_path)
    return service.sync(dry_run=dry_run, force=force)


def main():
    # Configure UTF-8 output for Windows console
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    # DYNAMIC BASE PATH DETECTION
    # Script lives in: {nexus-root}/00-system/core/nexus-loader.py
    # So nexus-root is 2 levels up from script location
    detected_nexus_root = SCRIPT_DIR.parent.parent

    parser = argparse.ArgumentParser(description="Nexus-v4 Context Loader")
    parser.add_argument('--startup', action='store_true', help='Load startup context with embedded memory files')
    parser.add_argument('--resume', action='store_true', help='Resume after context summary (skip menu, continue working)')
    parser.add_argument('--skip-update-check', action='store_true', help='Skip update check during startup (faster startup)')
    parser.add_argument('--metadata', action='store_true', help='Load only project/skill metadata (use after --startup --no-metadata)')
    parser.add_argument('--no-metadata', action='store_true', help='Exclude metadata from startup (smaller output, use --metadata separately)')
    parser.add_argument('--project', help='Load project by ID')
    parser.add_argument('--skill', help='Load skill by name')
    parser.add_argument('--list-projects', action='store_true', help='List all projects')
    parser.add_argument('--list-skills', action='store_true', help='List all skills')
    parser.add_argument('--full', action='store_true', help='Return complete metadata (default: minimal fields for efficiency)')
    parser.add_argument('--base-path', default=str(detected_nexus_root), help='Base path to Nexus-v4 (default: auto-detected)')
    parser.add_argument('--show-tokens', action='store_true', help='Include token cost analysis')
    # Sync commands
    parser.add_argument('--check-update', action='store_true', help='Check if upstream updates are available')
    parser.add_argument('--sync', action='store_true', help='Sync system files from upstream')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without changing (use with --sync)')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompts (use with --sync)')

    args = parser.parse_args()

    # Create service instance
    service = NexusService(args.base_path)

    # Execute command
    if args.check_update:
        result = service.check_updates()
    elif args.sync:
        result = service.sync(dry_run=args.dry_run, force=args.force)
    elif args.startup or args.resume:
        include_metadata = not args.no_metadata
        check_updates = not args.skip_update_check
        result = service.startup(
            include_metadata=include_metadata,
            resume_mode=args.resume,
            check_updates=check_updates
        )
    elif args.metadata:
        result = service.load_metadata()
    elif args.project:
        result = service.load_project(args.project)
    elif args.skill:
        result = service.load_skill(args.skill)
    elif args.list_projects:
        result = service.list_projects(full=args.full)
    elif args.list_skills:
        result = service.list_skills(full=args.full)
    else:
        parser.print_help()
        return

    # Add token analysis if requested
    if args.show_tokens:
        token_stats = calculate_bundle_tokens(result)
        result['token_cost'] = token_stats

        # Warn if metadata budget exceeded
        if token_stats.get('metadata', 0) > METADATA_BUDGET_WARNING:
            result['warnings'] = result.get('warnings', [])
            result['warnings'].append(
                f"Metadata tokens ({token_stats['metadata']}) exceeds recommended budget ({METADATA_BUDGET_WARNING})"
            )

    # Output JSON (always pretty-printed for human readability)
    output = json.dumps(result, indent=2, ensure_ascii=False)
    output_chars = len(output)

    # Add truncation detection metadata at the very end
    result['_output'] = {
        'chars': output_chars,
        'truncation_risk': output_chars > BASH_OUTPUT_LIMIT * 0.9,
        'split_recommended': output_chars > BASH_OUTPUT_LIMIT,
    }

    # Re-serialize with metadata
    final_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(final_output)


if __name__ == "__main__":
    main()
