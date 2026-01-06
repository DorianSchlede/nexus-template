#!/usr/bin/env python3
"""
Update Graph Node

PATCH /agent-graphs/update-node - Update node configuration.

Usage:
    python update_graph_node.py --node-id NODE --objective "New objective"
    python update_graph_node.py --node-id NODE --config '{"key": "value"}'
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Update graph node')
    parser.add_argument('--node-id', required=True, help='Node ID')
    parser.add_argument('--objective', help='New objective')
    parser.add_argument('--on-error', choices=['STOP', 'CONTINUE'], help='Error behavior')
    parser.add_argument('--auto-retry', type=bool, help='Enable auto retry')
    parser.add_argument('--config', help='JSON config object')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        data = {"nodeId": args.node_id}

        if args.objective:
            data["objective"] = args.objective
        if args.on_error:
            data["onError"] = args.on_error
        if args.auto_retry is not None:
            data["autoRetry"] = args.auto_retry
        if args.config:
            config = json.loads(args.config)
            data.update(config)

        result = client.patch('/agent-graphs/update-node', data=data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("Node updated successfully!")
            print(f"Node ID: {args.node_id}")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in --config", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
