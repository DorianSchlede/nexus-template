#!/usr/bin/env python3
"""
Get Analytics

GET /agent-tasks/analytics - Get agent performance analytics.

Usage:
    python get_analytics.py --agent-id AGENT
    python get_analytics.py --agent-id AGENT --start-date 2024-01-01 --end-date 2024-01-31
"""

import sys
import json
import argparse
from datetime import datetime, timedelta
from beam_client import get_client


def main():
    parser = argparse.ArgumentParser(description='Get agent analytics')
    parser.add_argument('--agent-id', required=True, help='Agent ID')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    # Default to last 30 days
    end = datetime.now()
    start = end - timedelta(days=30)

    try:
        client = get_client()

        params = {
            'agentId': args.agent_id,
            'startDate': args.start_date or start.strftime('%Y-%m-%dT00:00:00Z'),
            'endDate': args.end_date or end.strftime('%Y-%m-%dT23:59:59Z')
        }

        result = client.get('/agent-tasks/analytics', params=params)

        if args.json:
            print(json.dumps(result, indent=2))
        else:
            current = result.get('currentPeriod', {})
            delta = result.get('metricsDelta', {})

            print(f"\nAnalytics for Agent: {args.agent_id}")
            print("-" * 50)
            print(f"Total Tasks: {current.get('totalTasks', 0)} ({delta.get('totalTasksDelta', 'N/A')})")
            print(f"Completed: {current.get('completedTasks', 0)} ({delta.get('completedTasksDelta', 'N/A')})")
            print(f"Failed: {current.get('failedTasks', 0)} ({delta.get('failedTasksDelta', 'N/A')})")
            print(f"Avg Eval Score: {current.get('averageEvaluationScore', 0):.1f} ({delta.get('averageEvaluationScoreDelta', 'N/A')})")
            print(f"Avg Runtime: {current.get('averageRuntimeSeconds', 0):.1f}s ({delta.get('averageRuntimeSecondsDelta', 'N/A')})")
            print(f"Positive Feedback: {current.get('positiveFeedbackCount', 0)}")
            print(f"Negative Feedback: {current.get('negativeFeedbackCount', 0)}")

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
