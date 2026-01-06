#!/usr/bin/env python3
"""
Get Slack User Info

Get detailed information about a user using users.info.

Usage:
    python user_info.py --user U123
    python user_info.py --user U123 --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def get_user_info(user):
    """Get user information"""
    client = get_client()

    params = {'user': user}
    result = client.get('users.info', params)
    return result.get('user', {})


def main():
    parser = argparse.ArgumentParser(description='Get Slack user info')
    parser.add_argument('--user', '-u', required=True,
                        help='User ID')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        user = get_user_info(args.user)

        if args.json:
            profile = user.get('profile', {})
            output = {
                'success': True,
                'user': {
                    'id': user.get('id'),
                    'name': user.get('name'),
                    'real_name': user.get('real_name'),
                    'display_name': profile.get('display_name'),
                    'email': profile.get('email'),
                    'phone': profile.get('phone'),
                    'title': profile.get('title'),
                    'status_text': profile.get('status_text'),
                    'status_emoji': profile.get('status_emoji'),
                    'is_admin': user.get('is_admin', False),
                    'is_owner': user.get('is_owner', False),
                    'is_bot': user.get('is_bot', False),
                    'deleted': user.get('deleted', False),
                    'tz': user.get('tz'),
                    'tz_label': user.get('tz_label')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            profile = user.get('profile', {})

            print(f"\n{'='*60}")
            print(f"User: {user.get('real_name', user.get('name'))}")
            print(f"{'='*60}\n")

            print(f"ID: {user.get('id')}")
            print(f"Username: @{user.get('name')}")

            if profile.get('display_name'):
                print(f"Display Name: {profile['display_name']}")
            if profile.get('email'):
                print(f"Email: {profile['email']}")
            if profile.get('title'):
                print(f"Title: {profile['title']}")
            if profile.get('phone'):
                print(f"Phone: {profile['phone']}")

            # Status
            if profile.get('status_text') or profile.get('status_emoji'):
                status = f"{profile.get('status_emoji', '')} {profile.get('status_text', '')}".strip()
                print(f"\nStatus: {status}")

            # Roles
            roles = []
            if user.get('is_owner'):
                roles.append('Workspace Owner')
            if user.get('is_admin'):
                roles.append('Admin')
            if user.get('is_bot'):
                roles.append('Bot')
            if user.get('deleted'):
                roles.append('Deactivated')
            if roles:
                print(f"Roles: {', '.join(roles)}")

            # Timezone
            if user.get('tz_label'):
                print(f"\nTimezone: {user['tz_label']}")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to get user info: {e}")
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
