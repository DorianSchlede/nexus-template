#!/usr/bin/env python3
"""
List Agents

GET /agent - List all agents in workspace.

Usage:
    python list_agents.py
    python list_agents.py --json
    python list_agents.py --filter "customer"
"""

import sys
import json
import argparse
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='List workspace agents')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--filter', help='Filter agents by name')
    args = parser.parse_args()

    try:
        client = get_client()
        result = client.get('/agent')

        agents = result if isinstance(result, list) else result.get('agents', [])

        # Apply filter if provided
        if args.filter:
            filter_lower = args.filter.lower()
            agents = [a for a in agents if filter_lower in a.get('name', '').lower()
                     or filter_lower in a.get('description', '').lower()]

        if args.json:
            print(json.dumps(agents, indent=2))
        else:
            if not agents:
                print("No agents found in workspace")
                return

            print(f"\nFound {len(agents)} agent(s):\n")
            print("-" * 60)
            for agent in agents:
                print(f"Name: {agent.get('name', 'Unnamed')}")
                print(f"  ID: {agent.get('id', 'N/A')}")
                print(f"  Description: {agent.get('description', 'No description')[:100]}")
                print(f"  Type: {agent.get('type', 'N/A')}")
                print(f"  Created: {agent.get('createdAt', 'N/A')}")
                print("-" * 60)

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
