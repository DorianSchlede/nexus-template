#!/usr/bin/env python3
"""
Worktree Manager for Validation Testing

Creates and manages git worktrees for isolated parallel subagent testing.
Use when testing features that create/modify files (plan-project, execute-project, etc.)

Usage:
    # Setup worktrees
    python worktree-manager.py setup --count 3 --prefix test-validation

    # List active worktrees
    python worktree-manager.py list

    # Cleanup worktrees
    python worktree-manager.py cleanup --prefix test-validation

    # Cleanup all test worktrees
    python worktree-manager.py cleanup --all
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


def run_git(args: list, cwd: str = None) -> tuple[int, str, str]:
    """Run a git command and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result.returncode, result.stdout, result.stderr


def get_repo_root() -> Path:
    """Get the git repository root."""
    code, stdout, _ = run_git(["rev-parse", "--show-toplevel"])
    if code != 0:
        print("Error: Not in a git repository")
        sys.exit(1)
    return Path(stdout.strip())


def setup_worktrees(count: int, prefix: str) -> list[dict]:
    """Create N worktrees for parallel testing.

    CRITICAL: Returns ABSOLUTE paths using Path.resolve() to ensure
    subagents can access the worktrees regardless of their working directory.
    """
    repo_root = get_repo_root()
    parent_dir = repo_root.parent

    worktrees = []

    for i in range(count):
        branch_name = f"test/{prefix}-{i}"
        # CRITICAL: Use resolve() for absolute path
        worktree_path = (parent_dir / f"{prefix}-{i}").resolve()

        # Check if worktree already exists
        if worktree_path.exists():
            print(f"[SKIP] Worktree already exists: {worktree_path}")
            worktrees.append({
                "index": i,
                "branch": branch_name,
                "path": str(worktree_path),
                "status": "exists"
            })
            continue

        # Create worktree with new branch
        code, stdout, stderr = run_git([
            "worktree", "add",
            str(worktree_path),
            "-b", branch_name
        ])

        if code != 0:
            # Branch might exist, try without -b
            code, stdout, stderr = run_git([
                "worktree", "add",
                str(worktree_path),
                branch_name
            ])

        if code == 0:
            print(f"[OK] Created worktree: {worktree_path}")
            worktrees.append({
                "index": i,
                "branch": branch_name,
                "path": str(worktree_path),
                "status": "created"
            })
        else:
            print(f"[ERROR] Failed to create worktree {i}: {stderr}")
            worktrees.append({
                "index": i,
                "branch": branch_name,
                "path": str(worktree_path),
                "status": "error",
                "error": stderr
            })

    return worktrees


def list_worktrees() -> list[dict]:
    """List all git worktrees."""
    code, stdout, stderr = run_git(["worktree", "list", "--porcelain"])

    if code != 0:
        print(f"Error listing worktrees: {stderr}")
        return []

    worktrees = []
    current = {}

    for line in stdout.split("\n"):
        if line.startswith("worktree "):
            if current:
                worktrees.append(current)
            current = {"path": line[9:]}
        elif line.startswith("HEAD "):
            current["head"] = line[5:]
        elif line.startswith("branch "):
            current["branch"] = line[7:]
        elif line == "bare":
            current["bare"] = True
        elif line == "detached":
            current["detached"] = True

    if current:
        worktrees.append(current)

    return worktrees


def cleanup_worktrees(prefix: str = None, cleanup_all: bool = False) -> int:
    """Remove worktrees matching prefix or all test worktrees."""
    worktrees = list_worktrees()
    removed = 0

    for wt in worktrees:
        path = wt.get("path", "")
        branch = wt.get("branch", "")

        # Skip main worktree
        if not branch or "refs/heads/test/" not in branch:
            if not cleanup_all:
                continue

        # Check prefix match
        if prefix and prefix not in path:
            continue

        # Remove worktree
        code, _, stderr = run_git(["worktree", "remove", path, "--force"])

        if code == 0:
            print(f"[OK] Removed worktree: {path}")
            removed += 1

            # Also delete the branch
            branch_name = branch.replace("refs/heads/", "")
            run_git(["branch", "-D", branch_name])
            print(f"[OK] Deleted branch: {branch_name}")
        else:
            print(f"[ERROR] Failed to remove {path}: {stderr}")

    return removed


def main():
    parser = argparse.ArgumentParser(
        description="Manage git worktrees for validation testing"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Create worktrees")
    setup_parser.add_argument(
        "--count", "-n", type=int, default=3,
        help="Number of worktrees to create (default: 3)"
    )
    setup_parser.add_argument(
        "--prefix", "-p", type=str, default="test-validation",
        help="Prefix for worktree names (default: test-validation)"
    )

    # List command
    subparsers.add_parser("list", help="List all worktrees")

    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Remove worktrees")
    cleanup_parser.add_argument(
        "--prefix", "-p", type=str,
        help="Remove worktrees matching this prefix"
    )
    cleanup_parser.add_argument(
        "--all", "-a", action="store_true",
        help="Remove all test/* worktrees"
    )

    args = parser.parse_args()

    if args.command == "setup":
        worktrees = setup_worktrees(args.count, args.prefix)
        print(f"\nCreated {len([w for w in worktrees if w['status'] == 'created'])} worktrees")
        print("\nWorktree paths for subagents:")
        for wt in worktrees:
            print(f"  {wt['path']}")

    elif args.command == "list":
        worktrees = list_worktrees()
        print(f"Found {len(worktrees)} worktrees:\n")
        for wt in worktrees:
            branch = wt.get("branch", "detached").replace("refs/heads/", "")
            print(f"  {wt['path']}")
            print(f"    Branch: {branch}")
            print()

    elif args.command == "cleanup":
        if not args.prefix and not args.all:
            print("Error: Specify --prefix or --all")
            sys.exit(1)
        removed = cleanup_worktrees(args.prefix, args.all)
        print(f"\nRemoved {removed} worktrees")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
