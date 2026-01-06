#!/usr/bin/env python3
"""
Get HeyReach Campaign Details

Usage:
    python get_campaign.py --campaign-id ID [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def get_campaign(campaign_id):
    client = get_client()
    return client.post("/campaign/GetById", {"campaignId": campaign_id})


def main():
    parser = argparse.ArgumentParser(description='Get campaign details')
    parser.add_argument('--campaign-id', required=True, help='Campaign ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = get_campaign(args.campaign_id)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Campaign: {result.get('name', 'Unnamed')}")
            print(f"Status: {result.get('status', 'UNKNOWN')}")
            print(f"ID: {result.get('id', args.campaign_id)}")
            print(f"Created: {result.get('createdAt', 'N/A')}")

            accounts = result.get("linkedInAccountIds", [])
            if accounts:
                print(f"LinkedIn Accounts: {len(accounts)}")

            stats = result.get("stats", {})
            if stats:
                print(f"\nStatistics:")
                print(f"  Total Leads: {stats.get('totalLeads', 0)}")
                print(f"  Contacted: {stats.get('contacted', 0)}")
                print(f"  Replied: {stats.get('replied', 0)}")

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
