#!/usr/bin/env python3
"""
Test Graph Node

POST /agent-graphs/test-node - Test a specific node.

Usage:
    python test_graph_node.py --agent-id AGENT --node-id NODE --graph-id GRAPH
    python test_graph_node.py --agent-id AGENT --node-id NODE --graph-id GRAPH --input '{"key": "value"}'
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Test a graph node')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--node-id', required=True, help='Node ID')
    parser.add_argument('--graph-id', required=True, help='Graph ID')
    parser.add_argument('--input', help='JSON input params', default='{}')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        input_params = json.loads(args.input)

        data = {
            "agentId": args.agent_id,
            "nodeId": args.node_id,
            "graphId": args.graph_id,
            "params": input_params
        }

        result = client.post('/agent-graphs/test-node', data=data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\nNode Test Result:")
            print("-" * 50)
            print(f"Objective: {result.get('objective', 'N/A')}")
            print(f"Evaluation Criteria: {result.get('evaluationCriteria', [])}")
            print(f"\nFull response saved - use --json for details")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in --input", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
