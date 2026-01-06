#!/usr/bin/env python3
"""
Create Slack Channel

Create a new channel using conversations.create.

Usage:
    python create_channel.py --name "new-channel"
    python create_channel.py --name "private-channel" --is-private
    python create_channel.py --name "new-channel" --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def create_channel(name, is_private=False):
    """Create a new channel"""
    client = get_client()

    data = {
        'name': name,
        'is_private': is_private
    }

    result = client.post('conversations.create', data)
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Create a Slack channel')
    parser.add_argument('--name', '-n', required=True,
                        help='Channel name (lowercase, no spaces, max 80 chars)')
    parser.add_argument('--is-private', action='store_true',
                        help='Create private channel')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview channel creation without creating')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    try:
        # Dry-run mode
        if args.dry_run:
            channel_type = 'Private' if args.is_private else 'Public'
            prefix = '🔒' if args.is_private else '#'
            if args.json:
                output = {
                    'dry_run': True,
                    'would_create': {
                        'name': args.name,
                        'is_private': args.is_private,
                        'type': channel_type
                    }
                }
                print(json.dumps(output, indent=2))
            else:
                print(f"\n[DRY-RUN] Channel would be created (not actually created):")
                print(f"    Name: {prefix}{args.name}")
                print(f"    Type: {channel_type}")
                print()
            sys.exit(0)

        channel = create_channel(
            name=args.name,
            is_private=args.is_private
        )

        if args.json:
            output = {
                'success': True,
                'channel': {
                    'id': channel.get('id'),
                    'name': channel.get('name'),
                    'is_private': channel.get('is_private', False),
                    'creator': channel.get('creator'),
                    'created': channel.get('created')
                }
            }
            print(json.dumps(output, indent=2))
        else:
            prefix = "🔒" if channel.get('is_private') else "#"
            print(f"\n[OK] Channel created!")
            print(f"    Name: {prefix}{channel.get('name')}")
            print(f"    ID: {channel.get('id')}")
            print(f"    Type: {'Private' if channel.get('is_private') else 'Public'}")
            print()

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to create channel: {e}")
            print(f"    {explain_error(e.error_code)}")

            if e.error_code == 'name_taken':
                print("    Hint: Channel name already exists. Try a different name.")
            elif e.error_code == 'invalid_name':
                print("    Hint: Channel names must be lowercase, no spaces, max 80 chars.")
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
