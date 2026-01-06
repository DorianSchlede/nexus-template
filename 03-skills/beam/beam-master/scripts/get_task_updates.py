#!/usr/bin/env python3
"""
Get Task Updates (SSE)

GET /agent-tasks/{taskId}/updates - Stream real-time task updates.

Usage:
    python get_task_updates.py --task-id TASK_ID
    python get_task_updates.py --task-id TASK_ID --timeout 60
"""

import sys
import json
import argparse
from beam_client import get_client, BASE_URL


def main():
    parser = argparse.ArgumentParser(description='Stream task updates')
    parser.add_argument('--task-id', required=True, help='Task ID')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds')
    parser.add_argument('--json', action='store_true', help='Output as JSON lines')
    args = parser.parse_args()

    try:
        import requests
        client = get_client()
        headers = client.get_headers()
        headers['Accept'] = 'text/event-stream'

        url = f"{BASE_URL}/agent-tasks/{args.task_id}/updates"

        print(f"Streaming updates for task {args.task_id}...")
        print("Press Ctrl+C to stop\n")

        with requests.get(url, headers=headers, stream=True, timeout=args.timeout) as response:
            if response.status_code != 200:
                raise Exception(f"Failed to connect: {response.status_code}")

            for line in response.iter_lines():
                if line:
                    decoded = line.decode('utf-8')
                    if decoded.startswith('data:'):
                        data = decoded[5:].strip()
                        if data:
                            try:
                                event = json.loads(data)
                                if args.json:
                                    print(json.dumps(event))
                                else:
                                    status = event.get('status', 'UPDATE')
                                    msg = event.get('message', str(event))
                                    print(f"[{status}] {msg}")
                            except json.JSONDecodeError:
                                print(f"[RAW] {data}")

    except KeyboardInterrupt:
        print("\nStream stopped by user")
    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
