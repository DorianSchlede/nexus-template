#!/usr/bin/env python3
"""
Add Leads to HeyReach Campaign

Usage:
    python add_leads.py --campaign-id ID --leads JSON [--json]
    python add_leads.py --campaign-id ID --linkedin-urls URL1,URL2 [--json]
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from heyreach_client import get_client, HeyReachError


def add_leads(campaign_id, leads):
    client = get_client()
    # Format leads for HeyReach API
    formatted_leads = []
    for lead in leads:
        if isinstance(lead, str):
            formatted_leads.append({"profileUrl": lead})
        elif isinstance(lead, dict):
            formatted_leads.append({
                "profileUrl": lead.get("linkedInUrl", lead.get("profileUrl", "")),
                "firstName": lead.get("firstName", ""),
                "lastName": lead.get("lastName", ""),
                "email": lead.get("email", "")
            })
    return client.post("/campaign/AddLeadsToCampaign", {
        "campaignId": campaign_id,
        "leads": formatted_leads
    })


def main():
    parser = argparse.ArgumentParser(description='Add leads to campaign')
    parser.add_argument('--campaign-id', required=True, help='Campaign ID')
    parser.add_argument('--leads', help='JSON array of lead objects')
    parser.add_argument('--linkedin-urls', help='Comma-separated LinkedIn URLs')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    leads = []
    if args.leads:
        try:
            leads = json.loads(args.leads)
        except json.JSONDecodeError:
            print("Error: --leads must be valid JSON")
            sys.exit(2)
    elif args.linkedin_urls:
        urls = [u.strip() for u in args.linkedin_urls.split(',')]
        leads = [{"linkedInUrl": url} for url in urls if url]
    else:
        print("Error: Either --leads or --linkedin-urls required")
        sys.exit(2)

    try:
        result = add_leads(args.campaign_id, leads)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"[OK] Leads added to campaign!")
            print(f"   Campaign ID: {args.campaign_id}")
            print(f"   Added: {result.get('added', len(leads))}")
            if result.get('duplicates'):
                print(f"   Duplicates: {result.get('duplicates')}")

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
