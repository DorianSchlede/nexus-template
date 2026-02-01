#!/usr/bin/env python3
"""
Toggle HeyReach Campaign Status

Usage:
    python toggle_campaign.py --campaign-id ID --status ACTIVE|PAUSED [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def toggle_campaign(campaign_id, status):
    client = get_client()
    # Status should be 'Pause' or 'Resume' action
    action = "Pause" if status.upper() == "PAUSED" else "Resume"
    return client.post(f"/campaign/{action}", {"campaignId": campaign_id})


def main():
    parser = argparse.ArgumentParser(description='Toggle campaign status')
    parser.add_argument('--campaign-id', required=True, help='Campaign ID')
    parser.add_argument('--status', required=True, choices=['ACTIVE', 'PAUSED', 'active', 'paused'], help='New status')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = toggle_campaign(args.campaign_id, args.status)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            action = "resumed" if args.status.upper() == "ACTIVE" else "paused"
            print(f"[OK] Campaign {action} successfully!")
            print(f"   Campaign ID: {args.campaign_id}")
            print(f"   New Status: {args.status.upper()}")

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
