#!/usr/bin/env python3
"""
Retry Task

POST /agent-tasks/retry - Retry a failed task.

Usage:
    python retry_task.py --task-id TASK_ID
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Retry failed task')
    parser.add_argument('--task-id', required=True, help='Task ID to retry')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.post('/agent-tasks/retry', data={"taskId": args.task_id})

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Task {args.task_id} retry initiated!")
            print(f"New status: {result.get('status', 'QUEUED')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
