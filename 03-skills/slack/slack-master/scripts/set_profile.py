#!/usr/bin/env python3
"""
Set Slack Profile

Update your Slack profile status and fields using users.profile.set.

Usage:
    python set_profile.py --status "In a meeting" --emoji ":calendar:"
    python set_profile.py --status "Working from home" --emoji ":house:"
    python set_profile.py --clear-status
    python set_profile.py --display-name "Fred"
    python set_profile.py --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def set_profile(profile_data):
    """Update user profile"""
    client = get_client()

    result = client.post('users.profile.set', {
        'profile': json.dumps(profile_data)
    })
    return result.get('profile', {})


def get_current_profile():
    """Get current user profile"""
    client = get_client()

    result = client.get('users.profile.get')
    return result.get('profile', {})


def main():
    parser = argparse.ArgumentParser(description='Update your Slack profile')
    parser.add_argument('--status', '-s',
                        help='Status text')
    parser.add_argument('--emoji', '-e',
                        help='Status emoji (e.g., :house:)')
    parser.add_argument('--clear-status', action='store_true',
                        help='Clear your status')
    parser.add_argument('--display-name',
                        help='Set display name')
    parser.add_argument('--first-name',
                        help='Set first name')
    parser.add_argument('--last-name',
                        help='Set last name')
    parser.add_argument('--title',
                        help='Set job title')
    parser.add_argument('--phone',
                        help='Set phone number')
    parser.add_argument('--show', action='store_true',
                        help='Show current profile')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview profile changes without applying')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Show current profile
        if args.show:
            profile = get_current_profile()

            if args.json:
                print(json.dumps({
                    'success': True,
                    'profile': profile
                }, indent=2))
            else:
                print(f"\n{'='*60}")
                print("Current Profile")
                print(f"{'='*60}\n")
                print(f"  Display Name: {profile.get('display_name', 'Not set')}")
                print(f"  Real Name: {profile.get('real_name', 'Not set')}")
                print(f"  Title: {profile.get('title', 'Not set')}")
                print(f"  Phone: {profile.get('phone', 'Not set')}")
                print(f"  Email: {profile.get('email', 'Not set')}")
                status_emoji = profile.get('status_emoji', '')
                status_text = profile.get('status_text', '')
                if status_emoji or status_text:
                    print(f"  Status: {status_emoji} {status_text}")
                else:
                    print(f"  Status: Not set")
                print()
            return

        # Build profile update
        profile_data = {}

        if args.clear_status:
            profile_data['status_text'] = ''
            profile_data['status_emoji'] = ''
        else:
            if args.status is not None:
                profile_data['status_text'] = args.status
            if args.emoji is not None:
                profile_data['status_emoji'] = args.emoji

        if args.display_name is not None:
            profile_data['display_name'] = args.display_name
        if args.first_name is not None:
            profile_data['first_name'] = args.first_name
        if args.last_name is not None:
            profile_data['last_name'] = args.last_name
        if args.title is not None:
            profile_data['title'] = args.title
        if args.phone is not None:
            profile_data['phone'] = args.phone

        if not profile_data:
            parser.error('Please specify at least one profile field to update')

        # Dry-run mode
        if args.dry_run:
            if args.json:
                output = {
                    'dry_run': True,
                    'would_update': profile_data
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\n[DRY-RUN] Profile would be updated (not actually updated):")
                for key, value in profile_data.items():
                    print(f"    {key}: {value}")
                print()
            sys.exit(0)

        # Update profile
        updated = set_profile(profile_data)

        if args.json:
            output = {
                'success': True,
                'updated_fields': list(profile_data.keys()),
                'profile': updated
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n[OK] Profile updated")

            if args.clear_status:
                print("     Status cleared")
            elif args.status or args.emoji:
                emoji = updated.get('status_emoji', '')
                text = updated.get('status_text', '')
                print(f"     Status: {emoji} {text}")

            if args.display_name:
                print(f"     Display Name: {updated.get('display_name')}")
            if args.title:
                print(f"     Title: {updated.get('title')}")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to update profile: {e}")
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
