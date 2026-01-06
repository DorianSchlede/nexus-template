#!/usr/bin/env python3
"""
Get Latest Executions

GET /agent-tasks/latest-executions - Get recent task executions.

Usage:
    python get_latest_executions.py
    python get_latest_executions.py --agent-id AGENT
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get latest executions')
    parser.add_argument('--agent-id', help='Filter by agent ID')
    parser.add_argument('--limit', type=int, default=10, help='Number of results')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        params = {'limit': args.limit}
        if args.agent_id:
            params['agentId'] = args.agent_id

        result = client.get('/agent-tasks/latest-executions', params=params)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            executions = result if isinstance(result, list) else result.get('executions', [])
            print(f"\nLatest {len(executions)} Executions:")
            print("-" * 60)
            for ex in executions:
                print(f"[{ex.get('customId', ex.get('id', 'N/A')[:8])}] "
                      f"{ex.get('status', 'N/A')} - "
                      f"{ex.get('createdAt', 'N/A')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
