#!/usr/bin/env python3
"""
Get Task

GET /agent-tasks/{taskId} - Get task details.

Usage:
    python get_task.py --task-id TASK_ID
    python get_task.py --task-id TASK_ID --json
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get task details')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get(f'/agent-tasks/{args.task_id}')

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"\nTask: {result.get('customId', args.task_id)}")
            print("-" * 50)
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Success: {result.get('isSuccess', 'N/A')}")
            print(f"Query: {result.get('taskQuery', result.get('originalTaskQuery', 'N/A'))}")
            print(f"Started: {result.get('startedAt', 'N/A')}")
            print(f"Ended: {result.get('endedAt', 'N/A')}")
            print(f"Runtime: {result.get('totalExecutionTime', 'N/A')}s")
            print(f"Eval Score: {result.get('averageEvaluationScore', 'N/A')}")

            nodes = result.get('agentTaskNodes', [])
            if nodes:
                print(f"\nNodes ({len(nodes)}):")
                for node in nodes[:5]:
                    print(f"  - {node.get('status', 'N/A')}: Score {node.get('evaluationScore', 'N/A')}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
