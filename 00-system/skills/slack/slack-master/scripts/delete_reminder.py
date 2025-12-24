#!/usr/bin/env python3
"""
Delete Slack Reminder

Delete a reminder using reminders.delete.

Usage:
    python delete_reminder.py --reminder Rm12345678
    python delete_reminder.py --reminder Rm12345678 --yes
    python delete_reminder.py --reminder Rm12345678 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def delete_reminder(reminder_id):
    """Delete a reminder"""
    client = get_client()

    data = {'reminder': reminder_id}
    return client.post('reminders.delete', data)


def main():
    parser = argparse.ArgumentParser(description='Delete a Slack reminder')
    parser.add_argument('--reminder', '-r', required=True,
                        help='Reminder ID')
    parser.add_argument('--yes', '-y', action='store_true',
                        help='Skip confirmation prompt')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Confirmation prompt unless --yes flag is provided
        if not args.yes and not args.json:
            print(f"\n[!] WARNING: This will delete the reminder.")
            print(f"    Reminder ID: {args.reminder}")
            confirm = input("\n    Type 'delete' to confirm: ")
            if confirm.lower() != 'delete':
                print("\n[X] Aborted. Reminder was NOT deleted.\n")
                sys.exit(0)

        result = delete_reminder(args.reminder)

        if args.json:
            output = {
                'success': True,
                'reminder': args.reminder
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Reminder deleted!")
            print(f"    ID: {args.reminder}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to delete reminder: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'not_found':
                print("    Hint: Reminder ID not found. Use 'list reminders' to see your reminders.")
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
