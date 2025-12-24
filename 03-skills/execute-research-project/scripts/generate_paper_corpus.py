#!/usr/bin/env python3
"""
Paper Corpus Table Generator

Scans paper folders in a research project and generates the Paper Corpus table
for plan.md, including chunk counts, token estimates, and subagent allocation.

Usage:
    python generate_paper_corpus.py <project_path>
    python generate_paper_corpus.py <project_path> --update-plan
    python generate_paper_corpus.py <project_path> --json

Examples:
    # Preview corpus table
    python generate_paper_corpus.py ./02-projects/10-my-research

    # Update plan.md with new table
    python generate_paper_corpus.py ./02-projects/10-my-research --update-plan
"""

import argparse
import json
import sys
from pathlib import Path


def estimate_tokens(chars: int) -> int:
    """Estimate tokens from character count (chars / 5 * 1.3)."""
    return int(chars / 5 * 1.3)


def get_subagent_count(chunks: int) -> int:
    """
    Determine subagent allocation based on chunk count.

    Rules:
    - Small papers (<=4 chunks): 1 subagent
    - Medium papers (5-8 chunks): 1 subagent
    - Large papers (9-12 chunks): 1 subagent (may need retry)
    - Very large papers (>12 chunks): 2 subagents (split)
    """
    if chunks <= 12:
        return 1
    else:
        return 2


def scan_paper_folders(resources_path: Path) -> list[dict]:
    """
    Scan paper folders in 02-resources/ and extract metadata.

    Returns list of paper info dicts.
    """
    papers = []

    if not resources_path.exists():
        return papers

    for folder in sorted(resources_path.iterdir()):
        if not folder.is_dir():
            continue

        # Skip special files/folders
        if folder.name.startswith('_'):
            continue

        metadata_path = folder / "_metadata.json"
        index_path = folder / "index.md"

        paper_info = {
            "paper_id": folder.name,
            "chunks": 0,
            "chars": 0,
            "tokens_estimated": 0,
            "subagents": 1,
            "status": "ready",
            "has_metadata": metadata_path.exists(),
            "has_index": index_path.exists()
        }

        # Read metadata if exists
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                paper_info["chunks"] = metadata.get("total_chunks", 0)
                paper_info["chars"] = metadata.get("total_chars", 0)
                paper_info["tokens_estimated"] = estimate_tokens(paper_info["chars"])
                paper_info["subagents"] = get_subagent_count(paper_info["chunks"])

            except (json.JSONDecodeError, IOError) as e:
                paper_info["status"] = "error"
                paper_info["error"] = str(e)

        # Determine status
        if paper_info["has_index"]:
            paper_info["status"] = "analyzed"
        elif paper_info["chunks"] == 0 and paper_info["has_metadata"]:
            paper_info["status"] = "failed"  # 0 chunks = corrupted PDF
        elif not paper_info["has_metadata"]:
            paper_info["status"] = "pending"  # No metadata = not preprocessed

        papers.append(paper_info)

    return papers


def generate_corpus_table(papers: list[dict]) -> str:
    """Generate markdown table for Paper Corpus section."""
    lines = []
    lines.append("### Papers Ready for Analysis")
    lines.append("")
    lines.append("| Paper ID | Chunks | Est. Tokens | Subagents | Status |")
    lines.append("|----------|--------|-------------|-----------|--------|")

    ready_papers = [p for p in papers if p["status"] in ("ready", "analyzed")]
    for paper in ready_papers:
        tokens_str = f"~{paper['tokens_estimated']:,}" if paper['tokens_estimated'] > 0 else "?"
        lines.append(
            f"| {paper['paper_id']} | {paper['chunks']} | {tokens_str} | {paper['subagents']} | {paper['status']} |"
        )

    if not ready_papers:
        lines.append("| (none) | - | - | - | - |")

    # Add unavailable papers section if any
    unavailable = [p for p in papers if p["status"] in ("failed", "pending", "error")]
    if unavailable:
        lines.append("")
        lines.append("### Unavailable Papers")
        lines.append("")
        lines.append("| Paper | Reason |")
        lines.append("|-------|--------|")
        for paper in unavailable:
            reason = paper.get("error", "0 chunks" if paper["status"] == "failed" else "not preprocessed")
            lines.append(f"| {paper['paper_id']} | {reason} |")

    return "\n".join(lines)


def generate_metrics(papers: list[dict]) -> dict:
    """Generate metrics for Current State table."""
    ready = [p for p in papers if p["status"] in ("ready", "analyzed")]
    analyzed = [p for p in papers if p["status"] == "analyzed"]

    return {
        "Papers Approved": len(papers),
        "Papers Downloaded": len([p for p in papers if p["has_metadata"]]),
        "Papers with Chunks": len([p for p in papers if p["chunks"] > 0]),
        "Papers Analyzed": len(analyzed),
        "Total Chunks": sum(p["chunks"] for p in ready)
    }


def update_plan_file(plan_path: Path, corpus_table: str, metrics: dict) -> bool:
    """
    Update plan.md with new corpus table and metrics.

    Returns True if file was updated.
    """
    if not plan_path.exists():
        print(f"ERROR: plan.md not found at {plan_path}")
        return False

    content = plan_path.read_text(encoding='utf-8')
    original = content

    # Update Paper Corpus section
    # Pattern: from "### Papers Ready for Analysis" to next "---"
    import re

    corpus_pattern = re.compile(
        r'(### Papers Ready for Analysis.*?)(^---|\Z)',
        re.MULTILINE | re.DOTALL
    )

    if corpus_pattern.search(content):
        content = corpus_pattern.sub(corpus_table + r'\n\n\2', content)
    else:
        # Section not found - try to insert before Orchestrator Instructions
        orchestrator_marker = "## Orchestrator Instructions"
        if orchestrator_marker in content:
            content = content.replace(
                orchestrator_marker,
                corpus_table + "\n\n---\n\n" + orchestrator_marker
            )

    # Update metrics in Current State table
    for metric, value in metrics.items():
        pattern = re.compile(
            rf'^\|\s*{re.escape(metric)}\s*\|([^|]+)\|',
            re.MULTILINE
        )
        content = pattern.sub(f'| {metric} | {value} |', content)

    if content != original:
        plan_path.write_text(content, encoding='utf-8')
        return True

    return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate Paper Corpus table for research project plan.md"
    )
    parser.add_argument(
        "project_path",
        help="Path to the project folder"
    )
    parser.add_argument(
        "--update-plan",
        action="store_true",
        help="Update plan.md with generated table"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw paper data as JSON"
    )

    args = parser.parse_args()

    project_path = Path(args.project_path).resolve()

    if not project_path.exists():
        print(f"ERROR: Project path not found: {project_path}")
        sys.exit(1)

    resources_path = project_path / "02-resources"

    # Scan papers
    papers = scan_paper_folders(resources_path)

    if args.json:
        print(json.dumps(papers, indent=2))
        return

    # Generate outputs
    corpus_table = generate_corpus_table(papers)
    metrics = generate_metrics(papers)

    print("=" * 60)
    print("PAPER CORPUS SUMMARY")
    print("=" * 60)
    print()
    print(corpus_table)
    print()
    print("---")
    print()
    print("METRICS:")
    for key, value in metrics.items():
        print(f"  {key}: {value}")
    print()

    if args.update_plan:
        plan_path = project_path / "01-planning" / "plan.md"
        if update_plan_file(plan_path, corpus_table, metrics):
            print(f"Updated: {plan_path}")
        else:
            print("No changes made to plan.md")


if __name__ == "__main__":
    main()
