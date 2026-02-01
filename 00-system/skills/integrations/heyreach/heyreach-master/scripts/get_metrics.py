#!/usr/bin/env python3
"""
Get HeyReach Campaign Metrics

Usage:
    python get_metrics.py --campaign-id ID [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def get_metrics(campaign_id):
    client = get_client()
    return client.post("/analytics/GetCampaignStats", {"campaignId": campaign_id})


def main():
    parser = argparse.ArgumentParser(description='Get campaign metrics')
    parser.add_argument('--campaign-id', required=True, help='Campaign ID')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    try:
        result = get_metrics(args.campaign_id)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"[STATS] Campaign Metrics: {args.campaign_id}\n")
            print("Lead Statistics:")
            print(f"  Total Leads: {result.get('totalLeads', 0)}")
            print(f"  Contacted: {result.get('contacted', 0)}")
            print(f"  Replied: {result.get('replied', 0)}")
            print("\nConnection Stats:")
            conn_req = result.get('connectionRequests', 0)
            conn_acc = result.get('connectionsAccepted', 0)
            print(f"  Requests Sent: {conn_req}")
            print(f"  Accepted: {conn_acc}")
            if conn_req > 0:
                print(f"  Acceptance Rate: {(conn_acc/conn_req)*100:.1f}%")
            print("\nMessage Stats:")
            print(f"  Messages Sent: {result.get('messagesSent', 0)}")
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
