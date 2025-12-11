#!/usr/bin/env python3
"""
Research Topic Script
Conducts comprehensive web research on a topic and synthesizes findings.
"""

import json
import sys
from typing import Dict, List, Any


def research_topic(domain: str, focus_areas: List[str], api_type: str = "websearch") -> Dict[str, Any]:
    """
    Research a topic comprehensively.

    Args:
        domain: The domain to research (e.g., "UX design", "landing pages")
        focus_areas: Specific areas to focus on (e.g., ["principles", "anti-patterns"])
        api_type: API to use ("websearch", "perplexity")

    Returns:
        Dictionary containing research findings
    """

    research_queries = []

    # Generate search queries based on domain and focus areas
    for area in focus_areas:
        research_queries.append(f"{domain} {area} best practices")
        research_queries.append(f"{domain} {area} research studies")
        research_queries.append(f"{domain} {area} case studies")

    # Add general queries
    research_queries.extend([
        f"{domain} industry standards",
        f"{domain} common mistakes",
        f"{domain} benchmarking metrics",
        f"{domain} framework methodology"
    ])

    return {
        "domain": domain,
        "focus_areas": focus_areas,
        "queries": research_queries,
        "api_type": api_type,
        "instructions": [
            "Execute each query using WebSearch tool or specified API",
            "Synthesize findings into structured notes",
            "Group by: Principles, Frameworks, Anti-Patterns, Metrics, Case Studies",
            "Extract citations and sources for references section"
        ]
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python research_topic.py <domain> [focus_area1,focus_area2,...]")
        sys.exit(1)

    domain = sys.argv[1]
    focus_areas = sys.argv[2].split(",") if len(sys.argv) > 2 else [
        "principles", "frameworks", "anti-patterns", "metrics", "case studies"
    ]

    result = research_topic(domain, focus_areas)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
