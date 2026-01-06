#!/usr/bin/env python3
"""
Set Slack Channel Topic

Set the topic/description of a channel using conversations.setTopic.

Usage:
    python set_channel_topic.py #channel "New topic"
    python set_channel_topic.py C12345678 "New topic"
    python set_channel_topic.py #channel --clear
    python set_channel_topic.py #channel "New topic" --json
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from slack_client import get_client, SlackAPIError, explain_error


def find_channel(client, identifier):
    """Find channel by #name or channel ID"""
    # If it's already a channel ID
    if identifier.startswith('C') and len(identifier) == 11:
        return identifier

    # Remove # prefix if present
    channel_name = identifier.lstrip('#').lower()

    # Search for channel
    result = client.get('conversations.list', {
        'types': 'public_channel,private_channel',
        'limit': 1000
    })
    channels = result.get('channels', [])

    for channel in channels:
        if channel.get('name', '').lower() == channel_name:
            return channel.get('id')

    return None


def set_channel_topic(channel_id, topic):
    """Set channel topic"""
    client = get_client()

    result = client.post('conversations.setTopic', {
        'channel': channel_id,
        'topic': topic
    })
    return result.get('channel', {})


def main():
    parser = argparse.ArgumentParser(description='Set channel topic/description')
    parser.add_argument('channel',
                        help='Channel (#name or ID)')
    parser.add_argument('topic', nargs='?', default='',
                        help='New topic text')
    parser.add_argument('--clear', action='store_true',
                        help='Clear the topic')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview topic change without applying')
    parser.add_argument('--json', action='store_true',
                        help='Output as JSON')
    args = parser.parse_args()

    if not args.topic and not args.clear:
        parser.error('Please provide a topic or use --clear')

    topic = '' if args.clear else args.topic

    try:
        # Dry-run mode
        if args.dry_run:
            if args.json:
                output = {
                    'dry_run': True,
                    'would_update': {
                        'channel': args.channel,
                        'topic': topic,
                        'clear': args.clear
                    }
                }
                print(json.dumps(output, indent=2))
            else:
                if args.clear:
                    print(f"\n[DRY-RUN] Topic would be cleared (not actually cleared):")
                else:
                    print(f"\n[DRY-RUN] Topic would be set (not actually set):")
                print(f"    Channel: {args.channel}")
                print(f"    Topic: {topic if topic else '(cleared)'}")
                print()
            sys.exit(0)

        client = get_client()

        # Find the channel
        channel_id = find_channel(client, args.channel)
        if not channel_id:
            if args.json:
                print(json.dumps({
                    'success': False,
                    'error': {'message': f'Channel not found: {args.channel}'}
                }, indent=2))
            else:
                print(f"\n[X] Channel not found: {args.channel}")
            sys.exit(1)

        # Get channel info for display
        channel_info = client.get('conversations.info', {'channel': channel_id}).get('channel', {})
        channel_name = channel_info.get('name')

        # Set the topic
        result = set_channel_topic(channel_id, topic)

        if args.json:
            output = {
                'success': True,
                'channel_id': channel_id,
                'channel_name': channel_name,
                'topic': topic,
                'cleared': args.clear
            }
            print(json.dumps(output, indent=2))
        else:
            if args.clear:
                print(f"\n[OK] Cleared topic for #{channel_name}")
            else:
                print(f"\n[OK] Set topic for #{channel_name}")
                print(f"     Topic: {topic}\n")

    except SlackAPIError as e:
        if args.json:
            print(json.dumps({
                'success': False,
                'error': e.to_dict()
            }, indent=2))
        else:
            print(f"\n[X] Failed to set topic: {e}")
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
