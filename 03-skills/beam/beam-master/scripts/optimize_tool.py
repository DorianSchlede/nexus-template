#!/usr/bin/env python3
"""
Optimize Tool

POST /tool/optimize/{toolFunctionName}

Usage:
    python optimize_tool.py --tool send_email
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Start tool optimization')
    parser.add_argument('--tool', required=True, help='Tool function name')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.post(f'/tool/optimize/{args.tool}')

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            thread_id = result.get('threadId', result.get('id', 'N/A'))
            print(f"Optimization started for tool: {args.tool}")
            print(f"Thread ID: {thread_id}")
            print("\nUse get_optimization_status.py to check progress")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
