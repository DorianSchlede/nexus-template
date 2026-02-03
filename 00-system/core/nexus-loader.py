#!/usr/bin/env python3
"""
nexus-loader.py - Context loader and directive executor for Nexus

This is a thin CLI wrapper that delegates to the nexus package.

Usage:
    python nexus-loader.py --startup           # Load session context + return instructions
    python nexus-loader.py --resume            # Resume from context summary
    python nexus-loader.py --build ID        # Load specific build
    python nexus-loader.py --skill name        # Load specific skill
    python nexus-loader.py --list-builds     # Scan build metadata
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
from nexus.utils.config import BASH_OUTPUT_LIMIT, METADATA_BUDGET_WARNING, CACHE_DIR, CACHE_STARTUP_FILE
from nexus.utils.utils import calculate_bundle_tokens, handle_large_output

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


def load_build(build_id: str, base_path: str = "."):
    """Backward compatible wrapper for NexusService.load_build()"""
    service = NexusService(base_path)
    return service.load_build(build_id)


def load_skill(skill_name: str, base_path: str = "."):
    """Backward compatible wrapper for NexusService.load_skill()"""
    service = NexusService(base_path)
    return service.load_skill(skill_name)


def load_metadata(base_path: str = "."):
    """Backward compatible wrapper for NexusService.load_metadata()"""
    service = NexusService(base_path)
    return service.load_metadata()


def scan_builds(base_path: str = ".", minimal: bool = True):
    """Backward compatible wrapper for build scanning"""
    from nexus.core.loaders import scan_builds as _scan_builds
    return _scan_builds(base_path, minimal)


def scan_skills(base_path: str = ".", minimal: bool = True):
    """Backward compatible wrapper for skill scanning"""
    from nexus.core.loaders import scan_skills as _scan_skills
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
    parser.add_argument('--metadata', action='store_true', help='Load only build/skill metadata (use after --startup --no-metadata)')
    parser.add_argument('--no-metadata', action='store_true', help='Exclude metadata from startup (smaller output, use --metadata separately)')
    parser.add_argument('--build', help='Load build by ID')
    parser.add_argument('--part', type=int, default=0, help='Part to load for split responses (0=auto, 1=essential, 2=references)')
    parser.add_argument('--skill', help='Load skill by name (returns file tree + SKILL.md, use Read for references)')
    parser.add_argument('--list-builds', action='store_true', help='List all builds')
    parser.add_argument('--list-skills', action='store_true', help='List all skills')
    parser.add_argument('--full', action='store_true', help='Return complete metadata (default: minimal fields for efficiency)')
    parser.add_argument('--base-path', default=str(detected_nexus_root), help='Base path to Nexus-v4 (default: auto-detected)')
    parser.add_argument('--show-tokens', action='store_true', help='Include token cost analysis')
    # Sync commands
    parser.add_argument('--check-update', action='store_true', help='Check if upstream updates are available')
    parser.add_argument('--sync', action='store_true', help='Sync system files from upstream')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change without changing (use with --sync)')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompts (use with --sync)')
    parser.add_argument('--session', help='Unique session ID for multi-instance support (prevents cache collisions)')

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
    elif args.build:
        result = service.load_build(args.build, part=args.part)
    elif args.skill:
        result = service.load_skill(args.skill)
    elif args.list_builds:
        result = service.list_builds(full=args.full)
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

    # Determine command type for filename
    if args.startup or args.resume:
        cmd_type = "startup"
    elif args.build:
        cmd_type = f"build_{args.build}"
    elif args.skill:
        cmd_type = f"skill_{args.skill}"
    elif args.list_builds:
        cmd_type = "list_builds"
    elif args.list_skills:
        cmd_type = "list_skills"
    elif args.metadata:
        cmd_type = "metadata"
    else:
        cmd_type = "output"

    # Build extra fields for startup commands
    extra_fields = None
    if (args.startup or args.resume) and output_chars > BASH_OUTPUT_LIMIT:
        extra_fields = {
            "mode": "resume" if args.resume else "startup",
            "instructions": result.get("instructions", {}),
            "contains": [
                "orchestrator.md - AI behavior rules, routing, menu display (CRITICAL)",
                "system-map.md - Navigation structure",
                "memory files - goals.md, user-config.yaml, memory-map.md",
                "metadata - all builds and skills"
            ],
        }

    # Use shared utility for large output handling
    # MANDATORY: ALL commands must use temp file when output > 30k chars
    final_output = handle_large_output(
        output=output,
        command_name=cmd_type,
        base_path=detected_nexus_root,
        limit=BASH_OUTPUT_LIMIT,
        session_id=args.session,
        extra_fields=extra_fields,
    )

    # If output wasn't cached (under limit), add truncation metadata
    if final_output == output:
        result['_output'] = {
            'chars': output_chars,
            'truncation_risk': output_chars > BASH_OUTPUT_LIMIT * 0.9,
            'split_recommended': output_chars > BASH_OUTPUT_LIMIT,
        }
        final_output = json.dumps(result, indent=2, ensure_ascii=False)

    print(final_output)


if __name__ == "__main__":
    main()
