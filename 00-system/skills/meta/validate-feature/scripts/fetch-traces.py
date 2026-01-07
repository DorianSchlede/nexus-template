#!/usr/bin/env python3
"""
Fetch Traces from Langfuse for Subagent Validation

This script fetches traces from Langfuse for given agent IDs,
handling ingestion delay and formatting for analyzer consumption.

CRITICAL FEATURES:
- Retry logic with exponential backoff (5s, 10s, 15s)
- Fetches observations for each trace (GET /traces/{id})
- Formats output for test-case-analyzer consumption

Usage:
    python fetch-traces.py --agent-ids "ad059c8,aa1c33c,aae376a"
    python fetch-traces.py --session-ids "sess1,sess2,sess3"  # Manual mode

Requires: LANGFUSE_HOST environment variable to be set
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add langfuse-master scripts to path for shared client
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent.parent / "03-skills/langfuse/langfuse-master/scripts"))

try:
    from langfuse_client import get_client
except ImportError:
    print("Error: Could not import langfuse_client. Ensure 03-skills/langfuse/langfuse-master/scripts exists.")
    sys.exit(1)


def get_trace_with_observations(client, trace_id: str) -> Optional[Dict[str, Any]]:
    """
    Fetch a single trace WITH its observations.

    CRITICAL: GET /traces/{id} returns observations, GET /traces does NOT.

    Returns:
        Full trace data with observations, or None on error
    """
    try:
        response = client.get(f"/traces/{trace_id}")
        return response
    except Exception as e:
        print(f"  Error fetching trace {trace_id}: {e}")
        return None


def find_traces_by_agent_id(client, agent_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Find Langfuse traces for a given agent_id.

    The agent_id appears in Langfuse as metadata.conversationId = "agent-{agent_id}"

    Returns:
        List of trace IDs matching the agent_id (without observations)
    """
    conversation_id = f"agent-{agent_id}"

    try:
        # Fetch recent traces
        response = client.get("/traces", params={"limit": limit})
        traces = response.get('data', [])

        # Filter by conversationId in metadata
        matching = []
        for trace in traces:
            metadata = trace.get('metadata', {}) or {}
            if metadata.get('conversationId') == conversation_id:
                matching.append(trace)

        return matching

    except Exception as e:
        print(f"  Error fetching traces: {e}")
        return []


def find_traces_with_retry(client, agent_id: str, max_retries: int = 3) -> List[Dict[str, Any]]:
    """
    Find traces for an agent with exponential backoff retry.

    Retry delays: 5s, 10s, 15s (exponential)

    Returns:
        List of traces with observations
    """
    retry_delays = [5, 10, 15]  # Exponential backoff

    for attempt in range(max_retries):
        print(f"  Attempt {attempt + 1}/{max_retries} for agent {agent_id}")

        # Find matching traces (without observations)
        trace_summaries = find_traces_by_agent_id(client, agent_id)

        if trace_summaries:
            print(f"  Found {len(trace_summaries)} traces, fetching observations...")

            # CRITICAL: Fetch full trace with observations for each
            full_traces = []
            for trace in trace_summaries:
                trace_id = trace.get('id')
                if trace_id:
                    full_trace = get_trace_with_observations(client, trace_id)
                    if full_trace:
                        full_traces.append(full_trace)

            if full_traces:
                return full_traces

        # Not found, wait and retry
        if attempt < max_retries - 1:
            delay = retry_delays[attempt]
            print(f"  Traces not ready, retrying in {delay}s...")
            time.sleep(delay)

    return []


def fetch_traces_for_session(client, session_id: str) -> List[Dict[str, Any]]:
    """
    Fetch all traces for a given sessionId WITH observations.

    Returns:
        List of trace data dictionaries with observations
    """
    try:
        # Get trace list
        response = client.get("/traces", params={"sessionId": session_id, "limit": 50})
        trace_summaries = response.get('data', [])

        # Fetch full traces with observations
        full_traces = []
        for trace in trace_summaries:
            trace_id = trace.get('id')
            if trace_id:
                full_trace = get_trace_with_observations(client, trace_id)
                if full_trace:
                    full_traces.append(full_trace)

        return full_traces

    except Exception as e:
        print(f"Error fetching traces for session {session_id}: {e}")
        return []


def format_observation(obs: Dict[str, Any]) -> Dict[str, Any]:
    """Format a single observation for analyzer consumption."""
    formatted = {
        "name": obs.get("name", "Unknown"),
        "type": obs.get("type", "Unknown"),
        "level": obs.get("level", "DEFAULT"),
    }

    # Include input (truncated if too long)
    if obs.get("input"):
        input_data = obs["input"]
        if isinstance(input_data, str) and len(input_data) > 2000:
            input_data = input_data[:2000] + "...[truncated]"
        formatted["input"] = input_data

    # Include output (truncated if too long)
    if obs.get("output"):
        output_data = obs["output"]
        if isinstance(output_data, str) and len(output_data) > 2000:
            output_data = output_data[:2000] + "...[truncated]"
        formatted["output"] = output_data

    # Include status and error info
    if obs.get("statusMessage"):
        formatted["status_message"] = obs["statusMessage"]

    return formatted


def format_traces_for_analyzer(traces: List[Dict[str, Any]], agent_id: str) -> Dict[str, Any]:
    """
    Format traces into structured format for test-case-analyzer.

    Returns:
        Dictionary with trace data for YAML/JSON output
    """
    formatted = {
        "agent_id": agent_id,
        "conversation_id": f"agent-{agent_id}",
        "traces_count": len(traces),
        "traces": []
    }

    if not traces:
        return formatted

    for trace in traces:
        trace_data = {
            "trace_id": trace.get("id", "N/A"),
            "session_id": trace.get("sessionId", "N/A"),
            "name": trace.get("name", "Unknown"),
            "timestamp": trace.get("timestamp", "N/A"),
            "observations": []
        }

        # Process observations (tool calls)
        observations = trace.get("observations", [])
        for obs in observations:
            formatted_obs = format_observation(obs)
            trace_data["observations"].append(formatted_obs)

        trace_data["observation_count"] = len(trace_data["observations"])
        formatted["traces"].append(trace_data)

    return formatted


def format_traces_markdown(traces: List[Dict[str, Any]], agent_id: str) -> str:
    """
    Format traces as markdown for human readability.

    Returns:
        Markdown-formatted trace summary
    """
    output = []
    output.append(f"## Traces for Agent: {agent_id}\n")

    if not traces:
        output.append("*No traces found*\n")
        return "\n".join(output)

    for i, trace in enumerate(traces, 1):
        output.append(f"### Trace {i}: {trace.get('name', 'Unknown')}")
        output.append(f"- **ID**: {trace.get('id', 'N/A')}")
        output.append(f"- **Session ID**: {trace.get('sessionId', 'N/A')}")
        output.append(f"- **Timestamp**: {trace.get('timestamp', 'N/A')}")
        output.append("")

        # Observations (tool calls)
        observations = trace.get('observations', [])
        if observations:
            output.append(f"**Observations ({len(observations)} tool calls)**:\n")
            for j, obs in enumerate(observations, 1):
                obs_name = obs.get('name', 'Unknown')
                obs_type = obs.get('type', 'Unknown')
                output.append(f"{j}. **{obs_name}** ({obs_type})")

                # Show input summary
                if obs.get('input'):
                    input_str = str(obs['input'])
                    if len(input_str) > 200:
                        input_str = input_str[:200] + "..."
                    output.append(f"   - Input: `{input_str}`")

                # Show output summary
                if obs.get('output'):
                    output_str = str(obs['output'])
                    if len(output_str) > 300:
                        output_str = output_str[:300] + "..."
                    output.append(f"   - Output: `{output_str}`")

            output.append("")
        else:
            output.append("*No observations (tool calls) found*\n")

        output.append("---\n")

    return "\n".join(output)


def collect_traces_for_agents(agent_ids: List[str], wait_for_ingestion: int = 10) -> Dict[str, Any]:
    """
    Main function to collect traces for multiple agent IDs.

    Args:
        agent_ids: List of agent IDs from Task tool responses
        wait_for_ingestion: Seconds to wait before first query (default 10)

    Returns:
        Dictionary with structured trace data for test-case-analyzer
    """
    print(f"Waiting {wait_for_ingestion}s for Langfuse ingestion...")
    time.sleep(wait_for_ingestion)

    client = get_client()
    results = {
        "timestamp": datetime.now().isoformat(),
        "agent_count": len(agent_ids),
        "agents": [],
        "formatted_traces": [],  # Markdown for human readability
        "structured_traces": []  # Structured data for analyzer
    }

    for agent_id in agent_ids:
        print(f"\nProcessing agent: {agent_id}")

        # Find traces with retry logic
        traces = find_traces_with_retry(client, agent_id)

        session_id = traces[0].get('sessionId') if traces else None
        observation_count = sum(len(t.get('observations', [])) for t in traces)

        agent_result = {
            "agent_id": agent_id,
            "conversation_id": f"agent-{agent_id}",
            "session_id": session_id,
            "composite_key": f"{session_id}:{agent_id}" if session_id else None,
            "traces_found": len(traces) > 0,
            "trace_count": len(traces),
            "observation_count": observation_count
        }

        if traces:
            # Format for analyzer (structured)
            structured = format_traces_for_analyzer(traces, agent_id)
            results["structured_traces"].append(structured)

            # Format for human readability (markdown)
            markdown = format_traces_markdown(traces, agent_id)
            results["formatted_traces"].append(markdown)

            print(f"  Found {len(traces)} traces with {observation_count} observations")
        else:
            print(f"  Warning: Could not find traces for agent {agent_id}")
            results["structured_traces"].append({
                "agent_id": agent_id,
                "traces_count": 0,
                "traces": []
            })
            results["formatted_traces"].append(f"## Traces for Agent: {agent_id}\n*No traces found in Langfuse*\n")

        results["agents"].append(agent_result)

    # Summary
    found_count = sum(1 for a in results["agents"] if a["traces_found"])
    total_observations = sum(a["observation_count"] for a in results["agents"])
    print(f"\nResults: {found_count}/{len(agent_ids)} agents have traces")
    print(f"Total observations: {total_observations}")

    return results


def main():
    parser = argparse.ArgumentParser(description='Fetch Langfuse traces for validation')
    parser.add_argument('--agent-ids', type=str, help='Comma-separated agent IDs')
    parser.add_argument('--session-ids', type=str, help='Comma-separated session IDs (manual mode)')
    parser.add_argument('--wait', type=int, default=10, help='Seconds to wait for ingestion (default: 10)')
    parser.add_argument('--output', type=str, help='Output file path (JSON)')
    parser.add_argument('--format', choices=['json', 'yaml', 'markdown'], default='json',
                        help='Output format (default: json)')

    args = parser.parse_args()

    if args.agent_ids:
        agent_ids = [a.strip() for a in args.agent_ids.split(',')]
        results = collect_traces_for_agents(agent_ids, wait_for_ingestion=args.wait)
    elif args.session_ids:
        # Manual mode - direct session ID lookup
        session_ids = [s.strip() for s in args.session_ids.split(',')]
        client = get_client()
        results = {
            "timestamp": datetime.now().isoformat(),
            "mode": "manual",
            "session_count": len(session_ids),
            "structured_traces": [],
            "formatted_traces": []
        }
        for sid in session_ids:
            traces = fetch_traces_for_session(client, sid)
            agent_id = f"session-{sid[:8]}"

            structured = format_traces_for_analyzer(traces, agent_id)
            results["structured_traces"].append(structured)

            markdown = format_traces_markdown(traces, agent_id)
            results["formatted_traces"].append(markdown)
    else:
        parser.error("Either --agent-ids or --session-ids is required")
        return

    # Output results
    if args.output:
        output_path = Path(args.output)

        if args.format == 'yaml':
            import yaml
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(results, f, default_flow_style=False, allow_unicode=True)
        elif args.format == 'markdown':
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Trace Collection Results\n\n")
                f.write(f"**Timestamp**: {results['timestamp']}\n\n")
                for markdown in results['formatted_traces']:
                    f.write(markdown)
                    f.write("\n\n")
        else:  # json
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, default=str, ensure_ascii=False)

        print(f"Results saved to {args.output}")
    else:
        # Print formatted traces (markdown)
        print("\n" + "=" * 60)
        print("FORMATTED TRACES FOR ANALYZER")
        print("=" * 60 + "\n")
        for trace in results['formatted_traces']:
            print(trace)


if __name__ == "__main__":
    main()
