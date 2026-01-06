#!/usr/bin/env python3
"""
Get HeyReach Overall Stats

Usage:
    python get_stats.py [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def get_stats():
    client = get_client()
    return client.post("/analytics/GetOverallStats", {})


def main():
    parser = argparse.ArgumentParser(description='Get overall stats')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = get_stats()

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("📊 HeyReach Analytics Overview\n")
            print(f"Total Campaigns: {result.get('totalCampaigns', 0)}")
            print(f"Active Campaigns: {result.get('activeCampaigns', 0)}")
            print(f"\nOverall Performance:")
            print(f"  Total Leads: {result.get('totalLeads', 0)}")
            print(f"  Contacted: {result.get('contactedLeads', 0)}")
            print(f"  Replied: {result.get('repliedLeads', 0)}")
            print(f"\nRates:")
            print(f"  Connection Rate: {result.get('connectionRate', 0):.1f}%")
            print(f"  Reply Rate: {result.get('replyRate', 0):.1f}%")

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
