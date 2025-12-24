#!/usr/bin/env python3
"""
Get HeyReach Conversations

Usage:
    python get_conversations.py [--campaign-id ID] [--limit N] [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def get_conversations(campaign_id=None, limit=100, offset=0):
    client = get_client()
    payload = {"offset": offset, "limit": limit}
    if campaign_id:
        payload["campaignId"] = campaign_id
    return client.post("/conversation/GetAll", payload)


def main():
    parser = argparse.ArgumentParser(description='Get conversations')
    parser.add_argument('--campaign-id', help='Filter by campaign')
    parser.add_argument('--limit', type=int, default=100, help='Max results')
    parser.add_argument('--offset', type=int, default=0, help='Pagination offset')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = get_conversations(args.campaign_id, args.limit, args.offset)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            conversations = result.get("items", [])
            total = result.get("totalCount", len(conversations))
            print(f"Found {total} conversations:\n")

            for i, conv in enumerate(conversations, 1):
                messages = conv.get("messages", [])
                last_preview = ""
                if messages:
                    last = messages[-1]
                    direction = "→" if last.get("direction") == "OUTBOUND" else "←"
                    last_preview = f"{direction} {last.get('content', '')[:40]}..."

                print(f"{i}. Conversation {conv.get('id', 'N/A')}")
                print(f"   Lead ID: {conv.get('leadId', 'N/A')}")
                print(f"   Messages: {len(messages)}")
                if last_preview:
                    print(f"   Last: {last_preview}")
                print()

    except HeyReachError as e:
        if args.json:
            print(json.dumps({"error": True, "status_code": e.status_code, "message": e.message}, indent=2))
        else:
            print(f"Error ({e.status_code}): {e.message}")
        sys.exit(1)
    except ValueError as e:
        if args.json:
            print(json.dumps({"error": True, "message": str(e)}, indent=2))
        else:
            print(f"Config Error: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()
