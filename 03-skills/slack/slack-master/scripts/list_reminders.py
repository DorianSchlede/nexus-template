#!/usr/bin/env python3
"""
List Slack Reminders

List your reminders using reminders.list.

Usage:
    python list_reminders.py
    python list_reminders.py --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def list_reminders():
    """List reminders"""
    client = get_client()

    result = client.get('reminders.list')
    return result.get('reminders', [])


def main():
    parser = argparse.ArgumentParser(description='List Slack reminders')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        reminders = list_reminders()

        if args.json:
            output = {
                'success': True,
                'count': len(reminders),
                'reminders': [{
                    'id': r.get('id'),
                    'text': r.get('text'),
                    'time': r.get('time'),
                    'complete_ts': r.get('complete_ts'),
                    'recurring': r.get('recurring', False)
                } for r in reminders]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"Your Reminders ({len(reminders)} found)")
            print(f"{'='*60}\n")

            from datetime import datetime

            if reminders:
                # Sort by time
                reminders_sorted = sorted(reminders, key=lambda x: x.get('time', 0))

                for r in reminders_sorted:
                    remind_time = datetime.fromtimestamp(r.get('time', 0))
                    time_str = remind_time.strftime('%Y-%m-%d %H:%M')

                    status = ""
                    if r.get('complete_ts'):
                        status = " [completed]"
                    elif r.get('recurring'):
                        status = " [recurring]"

                    print(f"  [{time_str}] {r.get('text')}{status}")
                    print(f"       ID: {r.get('id')}")
                    print()
            else:
                print("No reminders set.")
                print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to list reminders: {e}")
            print(f"    {explain_error(e.error_code)}")
        sys.exit(1)
    except Exception as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': {'message': str(e)}
            }, indent=2))
        else:
            print(f"\n[X] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
