#!/usr/bin/env python3
"""
Iterate Tasks

GET /agent-tasks/iterate - Paginated task iteration.

Usage:
    python iterate_tasks.py
    python iterate_tasks.py --agent-id AGENT
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Iterate through tasks')
    parser.add_argument('--agent-id', help='Filter by agent ID')
    parser.add_argument('--cursor', help='Pagination cursor')
    parser.add_argument('--limit', type=int, default=50, help='Items per page')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        params = {'limit': args.limit}
        if args.agent_id:
            params['agentId'] = args.agent_id
        if args.cursor:
            params['cursor'] = args.cursor

        result = client.get('/agent-tasks/iterate', params=params)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            tasks = result.get('tasks', result.get('data', []))
            next_cursor = result.get('nextCursor', result.get('cursor'))

            print(f"\nTasks ({len(tasks)}):")
            print("-" * 50)
            for task in tasks[:10]:
                print(f"[{task.get('customId', task.get('id', 'N/A')[:8])}] {task.get('status', 'N/A')}")

            if next_cursor:
                print(f"\nNext cursor: {next_cursor}")
                print("Use --cursor to get next page")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
