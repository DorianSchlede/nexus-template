#!/usr/bin/env python3
"""
Create Task

POST /agent-tasks - Create new agent task.

Usage:
    python create_task.py --agent-id AGENT --query "Send email to john@example.com"
    python create_task.py --agent-id AGENT --query "Process file" --urls "http://example.com/file.pdf"
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Create agent task')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--query', required=True, help='Task query/instructions')
    parser.add_argument('--urls', help='Comma-separated URLs to parse')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()

        data = {
            "agentId": args.agent_id,
            "taskQuery": args.query
        }

        if args.urls:
            data["parsingUrls"] = [u.strip() for u in args.urls.split(',')]

        result = client.post('/agent-tasks', data=data)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("\nTask created successfully!")
            print("-" * 50)
            print(f"Task ID: {result.get('id', 'N/A')}")
            print(f"Custom ID: {result.get('customId', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Updates URL: {result.get('updatesUrl', 'N/A')}")
            print("\nUse get_task.py or get_task_updates.py to monitor progress")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
