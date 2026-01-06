#!/usr/bin/env python3
"""
Create Slack Reminder

Create a reminder using reminders.add.

Usage:
    python create_reminder.py --text "Review PR" --time 1735689600
    python create_reminder.py --text "Team meeting" --time "in 2 hours"
    python create_reminder.py --text "Submit report" --time "tomorrow at 9am" --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def create_reminder(text, time, user=None):
    """Create a reminder"""
    client = get_client()

    data = {
        'text': text,
        'time': time
    }

    if user:
        data['user'] = user

    result = client.post('reminders.add', data)
    return result.get('reminder', {})


def main():
    parser = argparse.ArgumentParser(description='Create a Slack reminder')
    parser.add_argument('--text', '-t', required=True,
                        help='Reminder text')
    parser.add_argument('--time', required=True,
                        help='When to remind (Unix timestamp or natural language like "in 2 hours")')
    parser.add_argument('--user', '-u',
                        help='User ID to remind (default: yourself)')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    # Try to convert time to integer if it looks like a timestamp
    time_value = args.time
    try:
        time_value = int(args.time)
    except ValueError:
        pass  # Keep as string (natural language)

    try:
        reminder = create_reminder(
            text=args.text,
            time=time_value,
            user=args.user
        )

        if args.json:
            output = {
                'success': True,
                'reminder': {
                    'id': reminder.get('id'),
                    'text': reminder.get('text'),
                    'time': reminder.get('time'),
                    'complete_ts': reminder.get('complete_ts'),
                    'creator': reminder.get('creator'),
                    'user': reminder.get('user')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            from datetime import datetime
            remind_time = datetime.fromtimestamp(reminder.get('time', 0))

            print(f"\n[OK] Reminder created!")
            print(f"    ID: {reminder.get('id')}")
            print(f"    Text: {reminder.get('text')}")
            print(f"    When: {remind_time.strftime('%Y-%m-%d %H:%M')}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to create reminder: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'cannot_parse':
                print("    Hint: Time format not recognized. Try Unix timestamp or 'in 2 hours'.")
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
