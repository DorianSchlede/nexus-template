#!/usr/bin/env python3
"""
Paper collection management script.

Usage:
    python paper_manage.py --list                    # List all collections
    python paper_manage.py --status TA_LLM           # Detailed collection status
    python paper_manage.py --rebuild TA_LLM          # Rebuild _collection.md
    python paper_manage.py --stats                   # Aggregate stats
    python paper_manage.py --json                    # Output as JSON
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PaperInfo:
    """Info about a single paper."""
    name: str
    status: str  # "analyzed" or "pending"
    chunks: int = 0
    tokens_estimated: int = 0
    year: Optional[int] = None
    topics: list = field(default_factory=list)
    has_index: bool = False


@dataclass
class CollectionInfo:
    """Info about a paper collection."""
    name: str
    path: str
    papers_total: int = 0
    papers_analyzed: int = 0
    papers_pending: int = 0
    total_tokens: int = 0
    has_briefing: bool = False
    papers: list = field(default_factory=list)
    topics_aggregated: dict = field(default_factory=dict)
    last_updated: Optional[str] = None


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}

    # Find end of frontmatter
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}

    yaml_content = content[4:end_match.start() + 3]

    # Simple YAML parsing (key: value or key: [list])
    result = {}
    current_key = None
    current_list = None

    for line in yaml_content.split('\n'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue

        # Check for list item
        if line.startswith('  - ') and current_key:
            if current_list is None:
                current_list = []
            current_list.append(line[4:].strip().strip('"\''))
            result[current_key] = current_list
            continue

        # Check for key: value
        if ':' in line:
            if current_list is not None:
                current_list = None

            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            current_key = key

            if value.startswith('[') and value.endswith(']'):
                # Inline list
                items = value[1:-1].split(',')
                result[key] = [item.strip().strip('"\'') for item in items if item.strip()]
            elif value.startswith('"') and value.endswith('"'):
                result[key] = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                result[key] = value[1:-1]
            elif value.isdigit():
                result[key] = int(value)
            elif value.replace('.', '').isdigit():
                result[key] = float(value)
            elif value.lower() in ('true', 'false'):
                result[key] = value.lower() == 'true'
            elif value.lower() == 'null' or value == '':
                result[key] = None
            else:
                result[key] = value

    return result


def scan_paper_folder(paper_path: Path) -> PaperInfo:
    """Scan a paper folder for status info."""
    name = paper_path.name

    # Check for index.md
    index_path = paper_path / "index.md"
    has_index = index_path.exists()

    # Initialize info
    info = PaperInfo(
        name=name,
        status="analyzed" if has_index else "pending",
        has_index=has_index
    )

    # Count chunks
    chunks = list(paper_path.glob(f"{name}_*.md"))
    info.chunks = len(chunks)

    # Read metadata if exists
    metadata_path = paper_path / "_metadata.json"
    if metadata_path.exists():
        try:
            with open(metadata_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
                info.tokens_estimated = int(meta.get('total_chars', 0) / 5 * 1.3)
        except (json.JSONDecodeError, IOError):
            pass

    # Read index.md for more details
    if has_index:
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
                frontmatter = parse_yaml_frontmatter(content)
                info.year = frontmatter.get('year')
                info.topics = frontmatter.get('topics', [])
                if frontmatter.get('tokens_estimated'):
                    info.tokens_estimated = frontmatter['tokens_estimated']
        except IOError:
            pass

    return info


def scan_collection(collection_path: Path) -> CollectionInfo:
    """Scan a collection folder for all papers."""
    name = collection_path.name
    info = CollectionInfo(name=name, path=str(collection_path))

    # Check for _briefing.md
    info.has_briefing = (collection_path / "_briefing.md").exists()

    # Get last modified time of any file in collection
    latest_mtime = 0

    # Scan paper folders (exclude _ prefixed files/folders)
    for item in collection_path.iterdir():
        if item.is_dir() and not item.name.startswith('_'):
            paper_info = scan_paper_folder(item)
            info.papers.append(paper_info)
            info.total_tokens += paper_info.tokens_estimated

            # Aggregate topics
            for topic in paper_info.topics:
                info.topics_aggregated[topic] = info.topics_aggregated.get(topic, 0) + 1

            # Track latest modification
            index_path = item / "index.md"
            if index_path.exists():
                mtime = index_path.stat().st_mtime
                if mtime > latest_mtime:
                    latest_mtime = mtime

    # Calculate stats
    info.papers_total = len(info.papers)
    info.papers_analyzed = sum(1 for p in info.papers if p.status == "analyzed")
    info.papers_pending = info.papers_total - info.papers_analyzed

    # Set last updated
    if latest_mtime > 0:
        info.last_updated = datetime.fromtimestamp(latest_mtime).isoformat()

    return info


def list_collections(papers_root: Path, as_json: bool = False) -> list[CollectionInfo]:
    """List all collections in papers root."""
    collections = []

    if not papers_root.exists():
        return collections

    for item in sorted(papers_root.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            collection = scan_collection(item)
            collections.append(collection)

    if as_json:
        print(json.dumps([asdict(c) for c in collections], indent=2))
    else:
        print("\n" + "=" * 60)
        print("Paper Collections")
        print("=" * 60)

        if not collections:
            print("\nNo collections found in", papers_root)
            return collections

        print(f"\n{'Collection':<25} {'Papers':<10} {'Analyzed':<10} {'Pending':<10} {'Briefing'}")
        print("-" * 70)

        for c in collections:
            briefing = "Y" if c.has_briefing else "-"
            print(f"{c.name:<25} {c.papers_total:<10} {c.papers_analyzed:<10} {c.papers_pending:<10} {briefing}")

        total_papers = sum(c.papers_total for c in collections)
        total_analyzed = sum(c.papers_analyzed for c in collections)
        print("-" * 70)
        print(f"{'TOTAL':<25} {total_papers:<10} {total_analyzed:<10} {total_papers - total_analyzed:<10}")

    return collections


def collection_status(collection_path: Path, as_json: bool = False) -> Optional[CollectionInfo]:
    """Get detailed status for a collection."""
    if not collection_path.exists():
        print(f"Collection not found: {collection_path}")
        return None

    info = scan_collection(collection_path)

    if as_json:
        print(json.dumps(asdict(info), indent=2))
    else:
        print("\n" + "=" * 60)
        print(f"Collection: {info.name}")
        print("=" * 60)

        print(f"\nPath: {info.path}")
        print(f"Briefing: {'Yes' if info.has_briefing else 'No'}")
        print(f"Papers: {info.papers_total} total, {info.papers_analyzed} analyzed, {info.papers_pending} pending")
        print(f"Est. Tokens: {info.total_tokens:,}")
        if info.last_updated:
            print(f"Last Updated: {info.last_updated}")

        if info.papers_analyzed > 0:
            print("\n--- Analyzed Papers ---")
            for p in info.papers:
                if p.status == "analyzed":
                    year = f"({p.year})" if p.year else ""
                    topics = ", ".join(p.topics[:3]) if p.topics else "-"
                    print(f"  • {p.name} {year}")
                    print(f"    Topics: {topics}")

        if info.papers_pending > 0:
            print("\n--- Pending Papers ---")
            for p in info.papers:
                if p.status == "pending":
                    print(f"  • {p.name} ({p.chunks} chunks, ~{p.tokens_estimated:,} tokens)")

        if info.topics_aggregated:
            print("\n--- Topics (frequency) ---")
            sorted_topics = sorted(info.topics_aggregated.items(), key=lambda x: -x[1])
            for topic, count in sorted_topics[:10]:
                print(f"  • {topic}: {count} papers")

    return info


def rebuild_collection_index(collection_path: Path) -> bool:
    """Rebuild _collection.md for a collection."""
    if not collection_path.exists():
        print(f"Collection not found: {collection_path}")
        return False

    info = scan_collection(collection_path)

    # Generate markdown content
    content = f"""---
name: "{info.name}"
papers_total: {info.papers_total}
papers_analyzed: {info.papers_analyzed}
papers_pending: {info.papers_pending}
total_tokens: {info.total_tokens}
last_updated: "{datetime.now().isoformat()}"
---

# {info.name.replace('_', ' ').title()}

## Overview

- **Total Papers**: {info.papers_total}
- **Analyzed**: {info.papers_analyzed} ({int(info.papers_analyzed / info.papers_total * 100) if info.papers_total else 0}%)
- **Pending**: {info.papers_pending}
- **Est. Tokens**: {info.total_tokens:,}

## Papers

### Analyzed

| Paper | Year | Topics | Chunks |
|-------|------|--------|--------|
"""

    for p in sorted(info.papers, key=lambda x: (x.year or 0, x.name)):
        if p.status == "analyzed":
            year = p.year or "-"
            topics = ", ".join(p.topics[:3]) if p.topics else "-"
            content += f"| {p.name} | {year} | {topics} | {p.chunks} |\n"

    if info.papers_pending > 0:
        content += """
### Pending Analysis

| Paper | Chunks | Est. Tokens |
|-------|--------|-------------|
"""
        for p in sorted(info.papers, key=lambda x: x.name):
            if p.status == "pending":
                content += f"| {p.name} | {p.chunks} | ~{p.tokens_estimated:,} |\n"

    if info.topics_aggregated:
        content += "\n## Topics (Aggregated)\n\n"
        sorted_topics = sorted(info.topics_aggregated.items(), key=lambda x: -x[1])
        for topic, count in sorted_topics:
            content += f"- {topic} ({count} papers)\n"

    content += f"\n## Generated\n\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    # Write file
    output_path = collection_path / "_collection.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[OK] Rebuilt {output_path}")
    print(f"  Papers: {info.papers_analyzed}/{info.papers_total} analyzed")

    return True


def aggregate_stats(papers_root: Path, as_json: bool = False) -> dict:
    """Get aggregate stats across all collections."""
    collections = list_collections(papers_root, as_json=False) if not as_json else []

    if as_json:
        # Quiet scan
        collections = []
        for item in sorted(papers_root.iterdir()):
            if item.is_dir() and not item.name.startswith('.'):
                collections.append(scan_collection(item))

    stats = {
        "collections": len(collections),
        "papers_total": sum(c.papers_total for c in collections),
        "papers_analyzed": sum(c.papers_analyzed for c in collections),
        "papers_pending": sum(c.papers_pending for c in collections),
        "total_tokens": sum(c.total_tokens for c in collections),
        "collections_with_briefing": sum(1 for c in collections if c.has_briefing),
    }

    # Aggregate all topics
    all_topics = {}
    for c in collections:
        for topic, count in c.topics_aggregated.items():
            all_topics[topic] = all_topics.get(topic, 0) + count

    stats["topics"] = dict(sorted(all_topics.items(), key=lambda x: -x[1])[:20])

    if as_json:
        print(json.dumps(stats, indent=2))
    else:
        print("\n" + "=" * 60)
        print("Aggregate Stats")
        print("=" * 60)
        print(f"\nCollections: {stats['collections']}")
        print(f"  With Briefing: {stats['collections_with_briefing']}")
        print(f"\nPapers: {stats['papers_total']} total")
        print(f"  Analyzed: {stats['papers_analyzed']}")
        print(f"  Pending: {stats['papers_pending']}")
        print(f"\nEst. Tokens: {stats['total_tokens']:,}")

        if stats["topics"]:
            print("\nTop Topics:")
            for topic, count in list(stats["topics"].items())[:10]:
                print(f"  • {topic}: {count} papers")

    return stats


def main():
    parser = argparse.ArgumentParser(description="Paper collection management")
    parser.add_argument("--list", action="store_true", help="List all collections")
    parser.add_argument("--status", type=str, help="Get status for a collection")
    parser.add_argument("--rebuild", type=str, help="Rebuild _collection.md for a collection")
    parser.add_argument("--stats", action="store_true", help="Aggregate stats")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--root", type=str, default="04-workspace/papers", help="Papers root folder")

    args = parser.parse_args()

    # Find project root (look for CLAUDE.md)
    current = Path.cwd()
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            break
        current = current.parent

    papers_root = current / args.root

    if args.list:
        list_collections(papers_root, args.json)
    elif args.status:
        collection_path = papers_root / args.status
        collection_status(collection_path, args.json)
    elif args.rebuild:
        collection_path = papers_root / args.rebuild
        rebuild_collection_index(collection_path)
    elif args.stats:
        aggregate_stats(papers_root, args.json)
    else:
        # Default: list
        list_collections(papers_root, args.json)


if __name__ == "__main__":
    main()
