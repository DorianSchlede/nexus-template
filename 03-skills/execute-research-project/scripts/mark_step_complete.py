#!/usr/bin/env python3
"""
Research Project Progress Tracker

Automates updating steps.md checkboxes and plan.md Current State table.

Usage:
    python mark_step_complete.py <project_path> --step "<step_text>"
    python mark_step_complete.py <project_path> --phase <1-5> --status "in_progress|complete"
    python mark_step_complete.py <project_path> --update-metrics --papers-analyzed 3 --total-papers 5

Examples:
    # Mark a specific checkbox complete
    python mark_step_complete.py ./02-projects/10-my-research --step "Define research question"

    # Update phase status
    python mark_step_complete.py ./02-projects/10-my-research --phase 4 --status in_progress

    # Update analysis metrics
    python mark_step_complete.py ./02-projects/10-my-research --update-metrics --papers-analyzed 3
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


def mark_checkbox_complete(steps_content: str, step_text: str) -> tuple[str, bool]:
    """
    Mark a checkbox as complete in steps.md content.

    Args:
        steps_content: Full content of steps.md
        step_text: Text to search for (partial match supported)

    Returns:
        (updated_content, was_changed)
    """
    # Pattern: - [ ] <text> -> - [x] <text>
    # Use case-insensitive partial match
    pattern = re.compile(
        r'^(\s*-\s*)\[ \](\s+.*?' + re.escape(step_text) + r'.*?)$',
        re.MULTILINE | re.IGNORECASE
    )

    new_content, count = pattern.subn(r'\1[x]\2', steps_content)
    return new_content, count > 0


def update_phase_status(steps_content: str, phase: int, status: str, details: str = None) -> str:
    """
    Update the Progress Summary table in steps.md.

    Args:
        steps_content: Full content of steps.md
        phase: Phase number (1-5)
        status: Status string (pending, in_progress, complete)
        details: Optional details string
    """
    phase_names = {
        1: "Definition",
        2: "Selection",
        3: "Acquisition",
        4: "Analysis",
        5: "Synthesis"
    }

    phase_name = phase_names.get(phase, f"Phase {phase}")

    # Pattern for table row: | N. Name | status | details |
    pattern = re.compile(
        rf'^\|\s*{phase}\.\s*{phase_name}\s*\|([^|]+)\|([^|]+)\|',
        re.MULTILINE | re.IGNORECASE
    )

    if details:
        replacement = f'| {phase}. {phase_name} | {status} | {details} |'
    else:
        # Keep existing details if not provided
        def replace_status(match):
            existing_details = match.group(2).strip()
            return f'| {phase}. {phase_name} | {status} | {existing_details} |'
        return pattern.sub(replace_status, steps_content)

    return pattern.sub(replacement, steps_content)


def update_last_updated(content: str) -> str:
    """Update the Last Updated timestamp."""
    today = datetime.now().strftime("%Y-%m-%d")
    pattern = re.compile(r'\*\*Last Updated\*\*:\s*\S+')
    return pattern.sub(f'**Last Updated**: {today}', content)


def update_plan_current_state(plan_content: str, updates: dict) -> str:
    """
    Update the Current State table in plan.md.

    Args:
        plan_content: Full content of plan.md
        updates: Dict of metric name -> value, e.g. {"Phase": "4-Analysis", "Papers Analyzed": "3"}
    """
    for metric, value in updates.items():
        # Pattern: | Metric | old_value |
        pattern = re.compile(
            rf'^\|\s*{re.escape(metric)}\s*\|([^|]+)\|',
            re.MULTILINE
        )
        plan_content = pattern.sub(f'| {metric} | {value} |', plan_content)

    return plan_content


def update_paper_corpus_table(plan_content: str, paper_id: str, status: str) -> str:
    """
    Update a paper's status in the Paper Corpus table.

    Args:
        plan_content: Full content of plan.md
        paper_id: Paper ID to update
        status: New status (ready, analyzed, failed)
    """
    # Pattern: | paper_id | chunks | tokens | subagents | old_status |
    pattern = re.compile(
        rf'^\|(\s*{re.escape(paper_id)}\s*)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]+)\|',
        re.MULTILINE
    )

    def update_status(match):
        return f'|{match.group(1)}|{match.group(2)}|{match.group(3)}|{match.group(4)}| {status} |'

    return pattern.sub(update_status, plan_content)


def main():
    parser = argparse.ArgumentParser(
        description="Update research project progress tracking"
    )
    parser.add_argument(
        "project_path",
        help="Path to the project folder"
    )
    parser.add_argument(
        "--step",
        help="Mark this step checkbox as complete (partial text match)"
    )
    parser.add_argument(
        "--phase",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Phase number to update"
    )
    parser.add_argument(
        "--status",
        choices=["pending", "in_progress", "complete"],
        help="Status to set for phase"
    )
    parser.add_argument(
        "--details",
        help="Details string for phase status"
    )
    parser.add_argument(
        "--update-metrics",
        action="store_true",
        help="Update plan.md Current State metrics"
    )
    parser.add_argument(
        "--papers-approved",
        type=int,
        help="Number of papers approved"
    )
    parser.add_argument(
        "--papers-downloaded",
        type=int,
        help="Number of papers downloaded"
    )
    parser.add_argument(
        "--papers-chunked",
        type=int,
        help="Number of papers with chunks"
    )
    parser.add_argument(
        "--papers-analyzed",
        type=int,
        help="Number of papers analyzed"
    )
    parser.add_argument(
        "--total-chunks",
        type=int,
        help="Total chunk count"
    )
    parser.add_argument(
        "--paper-status",
        nargs=2,
        metavar=("PAPER_ID", "STATUS"),
        help="Update a paper's status in corpus table"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without writing files"
    )

    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"ERROR: Project path not found: {project_path}")
        sys.exit(1)

    steps_path = project_path / "01-planning" / "steps.md"
    plan_path = project_path / "01-planning" / "plan.md"

    changes_made = []

    # Process steps.md updates
    if steps_path.exists() and (args.step or args.phase):
        steps_content = steps_path.read_text(encoding='utf-8')
        original_steps = steps_content

        if args.step:
            steps_content, changed = mark_checkbox_complete(steps_content, args.step)
            if changed:
                changes_made.append(f"Marked checkbox complete: '{args.step}'")
            else:
                print(f"WARNING: Checkbox not found or already complete: '{args.step}'")

        if args.phase and args.status:
            steps_content = update_phase_status(
                steps_content, args.phase, args.status, args.details
            )
            changes_made.append(f"Updated Phase {args.phase} status to '{args.status}'")

        if steps_content != original_steps:
            steps_content = update_last_updated(steps_content)
            if args.dry_run:
                print(f"[DRY RUN] Would update: {steps_path}")
            else:
                steps_path.write_text(steps_content, encoding='utf-8')
                print(f"Updated: {steps_path}")

    # Process plan.md updates
    if plan_path.exists() and (args.update_metrics or args.paper_status):
        plan_content = plan_path.read_text(encoding='utf-8')
        original_plan = plan_content

        if args.update_metrics:
            metrics = {}
            if args.papers_approved is not None:
                metrics["Papers Approved"] = str(args.papers_approved)
            if args.papers_downloaded is not None:
                metrics["Papers Downloaded"] = str(args.papers_downloaded)
            if args.papers_chunked is not None:
                metrics["Papers with Chunks"] = str(args.papers_chunked)
            if args.papers_analyzed is not None:
                metrics["Papers Analyzed"] = str(args.papers_analyzed)
            if args.total_chunks is not None:
                metrics["Total Chunks"] = str(args.total_chunks)

            if metrics:
                plan_content = update_plan_current_state(plan_content, metrics)
                changes_made.append(f"Updated metrics: {list(metrics.keys())}")

        if args.paper_status:
            paper_id, status = args.paper_status
            plan_content = update_paper_corpus_table(plan_content, paper_id, status)
            changes_made.append(f"Updated paper '{paper_id}' status to '{status}'")

        if plan_content != original_plan:
            if args.dry_run:
                print(f"[DRY RUN] Would update: {plan_path}")
            else:
                plan_path.write_text(plan_content, encoding='utf-8')
                print(f"Updated: {plan_path}")

    # Summary
    if changes_made:
        print("\nChanges made:")
        for change in changes_made:
            print(f"  - {change}")
    else:
        print("No changes made.")


if __name__ == "__main__":
    main()
