#!/usr/bin/env python3
"""
Reject Task

POST /agent-tasks/execution/{taskId}/rejection

Usage:
    python reject_task.py --task-id TASK
    python reject_task.py --task-id TASK --reason "Output not acceptable"
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Reject task execution')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--reason', help='Rejection reason')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        data = {}
        if args.reason:
            data['reason'] = args.reason

        result = client.post(f'/agent-tasks/execution/{args.task_id}/rejection', data=data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Task {args.task_id} rejected")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
