#!/usr/bin/env python3
"""
Provide User Input

PATCH /agent-tasks/execution/{taskId}/user-input

Usage:
    python provide_user_input.py --task-id TASK --input "User response"
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Provide user input for HITL task')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--input', required=True, help='User input/response')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.patch(
            f'/agent-tasks/execution/{args.task_id}/user-input',
            data={"input": args.input}
        )

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"User input provided for task {args.task_id}")
            print("Task will continue processing")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
