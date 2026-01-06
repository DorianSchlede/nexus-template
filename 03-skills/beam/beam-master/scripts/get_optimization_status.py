#!/usr/bin/env python3
"""
Get Optimization Status

POST /tool/optimization-status/thread/{threadId}

Usage:
    python get_optimization_status.py --thread-id THREAD
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Check optimization status')
    parser.add_argument('--thread-id', required=True, help='Optimization thread ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.post(f'/tool/optimization-status/thread/{args.thread_id}')

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            status = result.get('status', 'unknown')
            progress = result.get('progress', 0)
            print(f"Optimization Status: {status}")
            print(f"Progress: {progress}%")
            if result.get('message'):
                print(f"Message: {result['message']}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
