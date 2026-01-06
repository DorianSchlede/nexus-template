#!/usr/bin/env python3
"""
Get Agent Graph

GET /agent-graphs/{agentId} - Retrieve agent workflow graph.

Usage:
    python get_agent_graph.py --agent-id AGENT_ID
    python get_agent_graph.py --agent-id AGENT_ID --json
    python get_agent_graph.py --agent-id AGENT_ID --graph-id GRAPH_ID
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get agent workflow graph')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--graph-id', help='Specific graph version ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        params = {}
        if args.graph_id:
            params['graphId'] = args.graph_id

        result = client.get(f'/agent-graphs/{args.agent_id}', params=params)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            graph = result.get('graph', result)
            print(f"\nAgent Graph for: {args.agent_id}")
            print("-" * 50)
            print(f"Active: {graph.get('isActive', 'N/A')}")
            print(f"Published: {graph.get('isPublished', 'N/A')}")
            print(f"Draft: {graph.get('isDraft', 'N/A')}")

            nodes = graph.get('nodes', [])
            print(f"\nNodes ({len(nodes)}):")
            for node in nodes[:10]:  # Show first 10
                print(f"  - {node.get('objective', node.get('id', 'Unknown'))}")
            if len(nodes) > 10:
                print(f"  ... and {len(nodes) - 10} more nodes")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
