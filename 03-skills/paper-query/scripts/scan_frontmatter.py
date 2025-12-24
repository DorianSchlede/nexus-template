#!/usr/bin/env python3
"""
Lightweight frontmatter scanner for paper query (Level 1).

Scans all index.md files in a collection and ranks papers by query relevance.
This is the first level of progressive disclosure - no AI needed, just fast matching.

Usage:
    python scan_frontmatter.py --query "thematic analysis"
    python scan_frontmatter.py --collection TA_LLM --query "coding methods"
    python scan_frontmatter.py --query "LLM" --all --json
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class PaperMatch:
    """A paper matching the query with relevance score."""
    name: str
    collection: str
    score: float
    title: str = ""
    year: Optional[int] = None
    topics: list = field(default_factory=list)
    methods: list = field(default_factory=list)
    key_findings: list = field(default_factory=list)
    relevance_triggers: list = field(default_factory=list)
    chunks: int = 0
    match_details: dict = field(default_factory=dict)


def parse_yaml_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith('---'):
        return {}

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {}

    yaml_content = content[4:end_match.start() + 3]

    result = {}
    current_key = None
    current_list = None

    for line in yaml_content.split('\n'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue

        if line.startswith('  - ') and current_key:
            if current_list is None:
                current_list = []
            current_list.append(line[4:].strip().strip('"\''))
            result[current_key] = current_list
            continue

        if ':' in line:
            if current_list is not None:
                current_list = None

            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            current_key = key

            if value.startswith('[') and value.endswith(']'):
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


def calculate_score(frontmatter: dict, query_terms: list[str]) -> tuple[float, dict]:
    """Calculate relevance score based on query terms matching frontmatter fields."""
    score = 0.0
    match_details = {}

    # Weight factors
    weights = {
        'relevance_triggers': 3.0,
        'topics': 2.0,
        'methods': 2.0,
        'key_findings': 1.0,
        'title': 1.5,
    }

    for field_name, weight in weights.items():
        field_value = frontmatter.get(field_name, [])
        if isinstance(field_value, str):
            field_value = [field_value]

        field_text = ' '.join(str(v).lower() for v in field_value)
        matches = []

        for term in query_terms:
            if term.lower() in field_text:
                matches.append(term)
                score += weight

        if matches:
            match_details[field_name] = matches

    # Year bonus (newer papers slightly preferred)
    year = frontmatter.get('year')
    if year and isinstance(year, int):
        current_year = datetime.now().year
        age = current_year - year
        if age <= 2:
            score += 0.5
        elif age <= 5:
            score += 0.25

    return score, match_details


def scan_collection(collection_path: Path, query_terms: list[str]) -> list[PaperMatch]:
    """Scan all index.md files in a collection for query matches."""
    matches = []
    collection_name = collection_path.name

    for paper_folder in collection_path.iterdir():
        if not paper_folder.is_dir() or paper_folder.name.startswith('_'):
            continue

        index_path = paper_folder / "index.md"
        if not index_path.exists():
            continue

        try:
            content = index_path.read_text(encoding='utf-8')
            frontmatter = parse_yaml_frontmatter(content)

            if not frontmatter:
                continue

            score, match_details = calculate_score(frontmatter, query_terms)

            if score > 0:
                match = PaperMatch(
                    name=paper_folder.name,
                    collection=collection_name,
                    score=score,
                    title=frontmatter.get('title', paper_folder.name),
                    year=frontmatter.get('year'),
                    topics=frontmatter.get('topics', []),
                    methods=frontmatter.get('methods', []),
                    key_findings=frontmatter.get('key_findings', []),
                    relevance_triggers=frontmatter.get('relevance_triggers', []),
                    chunks=frontmatter.get('chunks', 0),
                    match_details=match_details,
                )
                matches.append(match)

        except (IOError, UnicodeDecodeError):
            continue

    return matches


def find_papers_root() -> Path:
    """Find the papers root directory."""
    current = Path.cwd()
    while current != current.parent:
        if (current / "CLAUDE.md").exists():
            return current / "04-workspace" / "papers"
        current = current.parent
    return Path("04-workspace/papers")


def main():
    parser = argparse.ArgumentParser(description="Query paper collections via frontmatter scan")
    parser.add_argument("--query", "-q", type=str, required=True, help="Search query")
    parser.add_argument("--collection", "-c", type=str, help="Specific collection to search")
    parser.add_argument("--all", "-a", action="store_true", help="Search all collections")
    parser.add_argument("--limit", "-l", type=int, default=10, help="Max results to return")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--root", type=str, default=None, help="Papers root folder")

    args = parser.parse_args()

    # Find papers root
    if args.root:
        papers_root = Path(args.root)
    else:
        papers_root = find_papers_root()

    if not papers_root.exists():
        print(f"Papers root not found: {papers_root}", file=sys.stderr)
        sys.exit(1)

    # Parse query into terms
    query_terms = [t.strip() for t in args.query.split() if t.strip()]

    # Collect matches
    all_matches = []

    if args.collection:
        # Search specific collection
        collection_path = papers_root / args.collection
        if not collection_path.exists():
            print(f"Collection not found: {args.collection}", file=sys.stderr)
            print("Available collections:", file=sys.stderr)
            for c in papers_root.iterdir():
                if c.is_dir() and not c.name.startswith('.'):
                    print(f"  - {c.name}", file=sys.stderr)
            sys.exit(1)
        all_matches = scan_collection(collection_path, query_terms)
    else:
        # Search all collections
        for collection_path in papers_root.iterdir():
            if collection_path.is_dir() and not collection_path.name.startswith('.'):
                matches = scan_collection(collection_path, query_terms)
                all_matches.extend(matches)

    # Sort by score descending
    all_matches.sort(key=lambda x: -x.score)

    # Limit results
    all_matches = all_matches[:args.limit]

    # Output
    if args.json:
        print(json.dumps([asdict(m) for m in all_matches], indent=2))
    else:
        if not all_matches:
            print(f"No papers match query: {args.query}")
            print("Try broader search terms or check that papers are analyzed (have index.md)")
            sys.exit(0)

        print(f"\nQuery: {args.query}")
        print(f"Results: {len(all_matches)} papers\n")
        print("-" * 70)

        for i, m in enumerate(all_matches, 1):
            year_str = f" ({m.year})" if m.year else ""
            print(f"{i}. [{m.collection}] {m.title}{year_str}")
            print(f"   Score: {m.score:.1f} | Chunks: {m.chunks}")

            if m.match_details:
                details = []
                for field, terms in m.match_details.items():
                    details.append(f"{field}: {', '.join(terms)}")
                print(f"   Matches: {' | '.join(details)}")

            if m.topics:
                print(f"   Topics: {', '.join(m.topics[:3])}")

            print()


if __name__ == "__main__":
    main()
