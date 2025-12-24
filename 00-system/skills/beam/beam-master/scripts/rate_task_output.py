#!/usr/bin/env python3
"""
Rate Task Output

PATCH /agent-tasks/execution/{taskId}/output-rating

Usage:
    python rate_task_output.py --task-id TASK --node-id NODE --rating positive
    python rate_task_output.py --task-id TASK --node-id NODE --rating negative --feedback "Issue description"
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Rate task output')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--node-id', required=True, help='Task node ID')
    parser.add_argument('--rating', required=True, choices=['positive', 'negative', 'excellent'], help='Rating')
    parser.add_argument('--feedback', help='User feedback')
    parser.add_argument('--expected-output', help='Expected output for comparison')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        data = {
            "taskNodeId": args.node_id,
            "rating": args.rating
        }
        if args.feedback:
            data["userFeedback"] = args.feedback
        if args.expected_output:
            data["expectedOutput"] = args.expected_output

        result = client.patch(f'/agent-tasks/execution/{args.task_id}/output-rating', data=data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Task {args.task_id} rated: {args.rating}")
            print("Rating will help improve agent performance")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
