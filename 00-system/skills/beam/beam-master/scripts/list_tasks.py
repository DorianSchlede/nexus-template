#!/usr/bin/env python3
"""
List Tasks

GET /agent-tasks - List tasks with filtering.

Usage:
    python list_tasks.py
    python list_tasks.py --agent-id AGENT
    python list_tasks.py --status COMPLETED,FAILED
    python list_tasks.py --search "email"
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='List agent tasks')
    parser.add_argument('--agent-id', help='Filter by agent ID')
    parser.add_argument('--status', help='Comma-separated statuses')
    parser.add_argument('--search', help='Search query')
    parser.add_argument('--start-date', help='Start date (ISO 8601)')
    parser.add_argument('--end-date', help='End date (ISO 8601)')
    parser.add_argument('--page', type=int, default=1, help='Page number')
    parser.add_argument('--page-size', type=int, default=20, help='Items per page')
    parser.add_argument('--order', default='createdAt:desc', help='Sort order')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        params = {
            'pageNum': args.page,
            'pageSize': args.page_size,
            'ordering': args.order
        }
        if args.agent_id:
            params['agentId'] = args.agent_id
        if args.status:
            params['statuses'] = args.status
        if args.search:
            params['searchQuery'] = args.search
        if args.start_date:
            params['startDate'] = args.start_date
        if args.end_date:
            params['endDate'] = args.end_date

        result = client.get('/agent-tasks', params=params)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            data = result.get('data', [])
            total = result.get('totalCount', 0)
            print(f"\nTasks: {total} total (page {args.page})")
            print("-" * 60)

            for group in data:
                tasks = group.get('tasks', [])
                group_name = group.get('groupName', 'Tasks')
                print(f"\n{group_name} ({group.get('groupCount', len(tasks))})")
                for task in tasks[:5]:
                    print(f"  [{task.get('customId', task.get('id', 'N/A')[:8])}] "
                          f"{task.get('status', 'N/A')} - "
                          f"{task.get('taskQuery', task.get('originalTaskQuery', 'No query'))[:50]}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
