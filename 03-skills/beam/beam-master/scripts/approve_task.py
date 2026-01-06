#!/usr/bin/env python3
"""
Approve Task

POST /agent-tasks/execution/{taskId}/user-consent

Usage:
    python approve_task.py --task-id TASK
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Approve HITL task')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.post(f'/agent-tasks/execution/{args.task_id}/user-consent')

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Task {args.task_id} approved")
            print("Task will continue processing")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
