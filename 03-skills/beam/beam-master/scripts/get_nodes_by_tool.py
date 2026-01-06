#!/usr/bin/env python3
"""
Get Nodes by Tool

GET /agent-graphs/agent-task-nodes/{toolFunctionName}

Usage:
    python get_nodes_by_tool.py --tool send_email
    python get_nodes_by_tool.py --tool send_email --agent-id AGENT
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get nodes using a tool')
    parser.add_argument('--tool', required=True, help='Tool function name')
    parser.add_argument('--agent-id', help='Filter by agent ID')
    parser.add_argument('--rated', action='store_true', help='Only rated nodes')
    parser.add_argument('--page', type=int, default=1, help='Page number')
    parser.add_argument('--page-size', type=int, default=50, help='Items per page')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        params = {
            'pageNum': args.page,
            'pageSize': args.page_size
        }
        if args.agent_id:
            params['agentId'] = args.agent_id
        if args.rated:
            params['isRated'] = True

        result = client.get(f'/agent-graphs/agent-task-nodes/{args.tool}', params=params)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            nodes = result.get('agentTaskNodes', [])
            count = result.get('count', len(nodes))
            print(f"\nNodes using '{args.tool}': {count} total")
            print("-" * 50)
            for node in nodes[:10]:
                print(f"Task ID: {node.get('agentTaskId', 'N/A')}")
                print(f"  Status: {node.get('status', 'N/A')}")
                print(f"  Rating: {node.get('rating', 'N/A')}")
                print("-" * 30)

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
