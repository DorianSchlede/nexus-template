#!/usr/bin/env python3
"""
Get Slack Team/Workspace Info

Get information about the current workspace using team.info.

Usage:
    python team_info.py
    python team_info.py --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def get_team_info():
    """Get workspace/team information"""
    client = get_client()

    result = client.get('team.info')
    return result.get('team', {})


def main():
    parser = argparse.ArgumentParser(description='Get Slack workspace information')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        team = get_team_info()

        if args.json:
            output = {
                'success': True,
                'team': {
                    'id': team.get('id'),
                    'name': team.get('name'),
                    'domain': team.get('domain'),
                    'email_domain': team.get('email_domain'),
                    'icon': team.get('icon', {}).get('image_132'),
                    'enterprise_id': team.get('enterprise_id'),
                    'enterprise_name': team.get('enterprise_name')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print("Workspace Information")
            print(f"{'='*60}\n")

            print(f"  Name: {team.get('name')}")
            print(f"  ID: {team.get('id')}")
            print(f"  Domain: {team.get('domain')}.slack.com")

            email_domain = team.get('email_domain')
            if email_domain:
                print(f"  Email Domain: {email_domain}")

            enterprise_name = team.get('enterprise_name')
            if enterprise_name:
                print(f"  Enterprise: {enterprise_name} ({team.get('enterprise_id')})")

            icon_url = team.get('icon', {}).get('image_132')
            if icon_url:
                print(f"  Icon: {icon_url}")

            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to get team info: {e}")
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
