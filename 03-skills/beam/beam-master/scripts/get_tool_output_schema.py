#!/usr/bin/env python3
"""
Get Tool Output Schema

GET /agent-tasks/tool-output-schema/{graphNodeId}

Usage:
    python get_tool_output_schema.py --node-id NODE_ID
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get tool output schema')
    parser.add_argument('--node-id', required=True, help='Graph node ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get(f'/agent-tasks/tool-output-schema/{args.node_id}')

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            schema = result if isinstance(result, list) else [result]
            print(f"\nOutput Schema for node {args.node_id}:")
            print("-" * 50)
            for param in schema:
                print(f"  {param.get('paramName', 'N/A')}: {param.get('dataType', 'N/A')}")
                if param.get('paramDescription'):
                    print(f"    Description: {param['paramDescription']}")
                if param.get('outputExample'):
                    print(f"    Example: {param['outputExample']}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
