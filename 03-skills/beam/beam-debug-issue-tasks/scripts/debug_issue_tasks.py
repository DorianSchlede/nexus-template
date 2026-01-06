#!/usr/bin/env python3
"""
Beam Debug Issue Tasks

List failed/issue tasks from Beam.ai and fetch corresponding Langfuse traces
to diagnose why tasks failed.

Usage:
    # List issue tasks from last 1 day (default)
    python debug_issue_tasks.py <agent_id>

    # List issue tasks from last 7 days
    python debug_issue_tasks.py <agent_id> --days 7

    # Debug a specific task
    python debug_issue_tasks.py <agent_id> --task-id <task_id>

    # Group by status and show summary
    python debug_issue_tasks.py <agent_id> --days 7 --summary
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from collections import defaultdict

# Add parent directories to path for shared module import
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

try:
    from _shared.beam_api import BeamClient
    from _shared.langfuse_api import LangfuseClient, get_project_id, LANGFUSE_PROJECTS
except ImportError as e:
    print(f"Error: Could not import shared modules: {e}")
    print("Ensure 03-skills/_shared/beam_api.py and langfuse_api.py exist")
    sys.exit(1)


# Task statuses that indicate issues
ISSUE_STATUSES = ["FAILED", "ERROR", "ISSUE", "CANCELLED", "TIMEOUT", "STOPPED", "USER_INPUT_REQUIRED"]
# Statuses to exclude (normal operation)
EXCLUDE_STATUSES = ["IN_PROGRESS", "QUEUED", "COMPLETED", "COMPLETE", "RUNNING"]


def find_project_root() -> Path:
    """Find project root by looking for CLAUDE.md or .git directory."""
    current = Path(__file__).resolve().parent
    for _ in range(10):
        if (current / "CLAUDE.md").exists() or (current / ".git").exists():
            return current
        if current.parent == current:
            break
        current = current.parent
    # Fallback to 03-skills parent
    return Path(__file__).resolve().parent.parent.parent


def sanitize_folder_name(name: str) -> str:
    """Sanitize a name for use as folder name."""
    # Replace problematic characters with underscores
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', ' ']
    result = name
    for char in invalid_chars:
        result = result.replace(char, '_')
    # Remove multiple underscores
    while '__' in result:
        result = result.replace('__', '_')
    return result.strip('_')


def get_agent_debug_dir(agent_name: str) -> Path:
    """Get or create debug directory for an agent."""
    root = find_project_root()
    folder_name = sanitize_folder_name(agent_name)
    debug_dir = root / "04-workspace" / "agents" / folder_name / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    return debug_dir


def save_debug_report(
    agent_name: str,
    task_id: str,
    task: dict,
    trace_info: dict,
    workspace: str
) -> Path:
    """
    Save debug report as markdown file using Smart Brevity format.

    Args:
        agent_name: Agent name (used for folder)
        task_id: Task ID
        task: Task data from Beam API
        trace_info: Trace info from Langfuse
        workspace: Workspace name (prod/bid)

    Returns:
        Path to saved report
    """
    debug_dir = get_agent_debug_dir(agent_name)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}_{task_id[:8]}.md"
    filepath = debug_dir / filename

    status = task.get('status', 'UNKNOWN')
    custom_id = task.get('customId', '')
    created = task.get('createdAt', task.get('created_at', 'N/A'))

    # Determine root cause for headline and takeaway
    root_cause = None
    fix_suggestion = None

    if trace_info and trace_info.get("found"):
        analysis = trace_info.get("analysis", {})
        if analysis:
            root_cause = analysis.get("last_reasoning")
    else:
        # Check for parameter extraction issues
        task_nodes = task.get("agentTaskNodes", [])
        for node in task_nodes:
            user_questions = node.get("userQuestions", [])
            if user_questions:
                missing_params = [q.get("parameter") for q in user_questions if not q.get("answer")]
                if missing_params:
                    root_cause = f"Missing required parameter: {', '.join(missing_params)}"
                    fix_suggestion = "Provide the missing input data when starting the task."
                    break

    # Build Smart Brevity report
    lines = []

    # HEADLINE: 6 words or fewer
    if status == "USER_INPUT_REQUIRED":
        headline = f"Task blocked: missing input"
    elif status == "STOPPED":
        headline = f"Task stopped: condition failed"
    elif status == "FAILED":
        headline = f"Task failed: execution error"
    else:
        headline = f"Task {status.lower()}"

    lines.append(f"# {headline}")
    lines.append("")

    # ONE KEY TAKEAWAY: First sentence = the ONE thing to remember
    if root_cause:
        takeaway = root_cause[:200].replace('\n', ' ').strip()
        if len(root_cause) > 200:
            takeaway += "..."
    else:
        takeaway = f"Task {task_id[:8]} ended with status {status}."

    lines.append(takeaway)
    lines.append("")

    # WHY IT MATTERS
    lines.append("**Why it matters**: This task did not complete successfully and may need attention or retry.")
    lines.append("")

    # THE DETAILS: Bulleted, scannable
    lines.append("**The details**:")
    lines.append(f"- **Status**: `{status}`")
    lines.append(f"- **Task**: `{task_id}`")
    if custom_id:
        lines.append(f"- **Custom ID**: {custom_id}")
    lines.append(f"- **Created**: {created}")
    lines.append(f"- **Workspace**: {workspace}")
    lines.append("")

    # GO DEEPER: Trace info or task state
    if trace_info and trace_info.get("found"):
        lines.append("**Trace info**:")
        lines.append(f"- Traces: {trace_info.get('trace_count', 0)}")
        latency = trace_info.get('latency')
        if latency:
            lines.append(f"- Latency: {latency:.1f}s")
        cost = trace_info.get('total_cost', 0)
        if cost:
            lines.append(f"- Cost: ${cost:.4f}")
        lines.append(f"- [View Session]({trace_info.get('session_url')})")
        lines.append(f"- [View Trace]({trace_info.get('trace_url')})")
        lines.append("")

        analysis = trace_info.get("analysis", {})
        if analysis:
            # Key spans
            key_gens = analysis.get("key_generations", [])
            if key_gens:
                lines.append("**Key spans**:")
                for gen in key_gens[:5]:
                    name = gen.get("name", "unknown")
                    latency = gen.get("latency")
                    latency_str = f" ({latency:.1f}s)" if latency else ""
                    has_error = gen.get("error")
                    marker = "!" if has_error else "-"
                    lines.append(f"{marker} {name}{latency_str}")
                lines.append("")

            # Full reasoning
            last_reasoning = analysis.get("last_reasoning")
            if last_reasoning:
                lines.append("**Root cause**:")
                lines.append(f"> {last_reasoning.replace(chr(10), chr(10) + '> ')}")
                lines.append("")

            errors = analysis.get("errors", [])
            if errors:
                lines.append("**Errors found**:")
                for err in errors[:3]:
                    lines.append(f"- {err}")
                lines.append("")
    else:
        # No traces - show task state
        if trace_info:
            lines.append(f"**Session**: [View in Langfuse]({trace_info.get('session_url')})")
            lines.append("")

        graph_state = task.get("graphState", {})
        current_node = graph_state.get("current", {})
        if current_node:
            node_name = current_node.get("tool", {}).get("name", "Unknown")
            on_error = current_node.get("on_error", "N/A")
            lines.append("**Task state**:")
            lines.append(f"- Current node: {node_name}")
            lines.append(f"- On error: {on_error}")
            lines.append("")

        # User questions (missing parameters)
        task_nodes = task.get("agentTaskNodes", [])
        for node in task_nodes:
            user_questions = node.get("userQuestions", [])
            if user_questions:
                lines.append("**Missing inputs**:")
                for q in user_questions:
                    param = q.get("parameter", "unknown")
                    answer = q.get("answer")
                    status_mark = "Provided" if answer else "Awaiting"
                    lines.append(f"- `{param}`: {status_mark}")
                lines.append("")

            # Tool reasoning (condensed)
            tool_data = node.get("toolData", {})
            reasoning = tool_data.get("reasoning", {})
            if reasoning:
                lines.append("**Parameter reasoning**:")
                for param, reason in reasoning.items():
                    # Extract just the key insight
                    reason_short = reason[:150].replace('\n', ' ').strip()
                    if len(reason) > 150:
                        reason_short += "..."
                    lines.append(f"- `{param}`: {reason_short}")
                lines.append("")

    # BOTTOM LINE: Fix suggestion
    if fix_suggestion:
        lines.append(f"**Fix**: {fix_suggestion}")
    elif status == "USER_INPUT_REQUIRED":
        lines.append("**Fix**: Provide the missing input parameter to continue task execution.")
    elif status == "STOPPED":
        lines.append("**Fix**: Review the condition that stopped execution. Check if input data meets requirements.")
    elif status == "FAILED":
        lines.append("**Fix**: Review the error details above. Check logs and retry with corrected input.")
    lines.append("")

    # Metadata footer
    lines.append("---")
    lines.append(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

    # Write file
    filepath.write_text("\n".join(lines))
    return filepath


def list_agent_tasks(
    client: BeamClient,
    agent_id: str,
    start_date: str,
    end_date: str,
    status: str = None,
    limit: int = 100,
    page: int = 1
) -> dict:
    """
    List tasks for an agent with optional filters.

    Args:
        client: BeamClient instance
        agent_id: Agent ID
        start_date: ISO 8601 start date
        end_date: ISO 8601 end date
        status: Optional status filter
        limit: Items per page
        page: Page number

    Returns:
        API response with tasks array
    """
    params = {
        "agentId": agent_id,
        "startDate": start_date,
        "endDate": end_date,
        "limit": limit,
        "page": page
    }

    if status:
        params["status"] = status

    return client.get("/agent-tasks", params=params)


def fetch_all_tasks(
    client: BeamClient,
    agent_id: str,
    start_date: str,
    end_date: str,
    max_pages: int = 50
) -> list:
    """
    Fetch all tasks across pages.

    Args:
        client: BeamClient instance
        agent_id: Agent ID
        start_date: ISO 8601 start date
        end_date: ISO 8601 end date
        max_pages: Maximum pages to fetch

    Returns:
        List of all tasks
    """
    all_tasks = []
    page = 1

    while page <= max_pages:
        result = list_agent_tasks(client, agent_id, start_date, end_date, page=page)

        # Handle nested structure: {"data": [{"tasks": [...]}], "totalCount": N}
        data = result.get("data", [])
        if data and isinstance(data, list) and len(data) > 0:
            # New API format: tasks nested inside data[0].tasks
            first_item = data[0]
            if isinstance(first_item, dict) and "tasks" in first_item:
                tasks = first_item.get("tasks", [])
            else:
                tasks = data
        else:
            # Old format: tasks directly in response
            tasks = result.get("tasks", data)

        if not tasks:
            break

        all_tasks.extend(tasks)

        # Check if more pages
        total = result.get("totalCount", result.get("total", len(all_tasks)))
        if len(all_tasks) >= total:
            break

        page += 1

    return all_tasks


def filter_issue_tasks(tasks: list) -> list:
    """Filter tasks to only those with issue statuses."""
    return [
        t for t in tasks
        if t.get("status", "").upper() in ISSUE_STATUSES
    ]


def group_tasks_by_status(tasks: list) -> dict:
    """Group tasks by their status."""
    grouped = defaultdict(list)
    for task in tasks:
        status = task.get("status", "UNKNOWN").upper()
        grouped[status].append(task)
    return dict(grouped)


def group_tasks_by_day(tasks: list) -> dict:
    """Group tasks by creation date."""
    grouped = defaultdict(list)
    for task in tasks:
        created = task.get("createdAt", task.get("created_at", ""))
        if created:
            # Parse ISO date and extract day
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                day = dt.strftime("%Y-%m-%d")
            except ValueError:
                day = "unknown"
        else:
            day = "unknown"
        grouped[day].append(task)
    return dict(grouped)


def extract_reasoning_from_content(content: str) -> str:
    """Extract reasoning from JSON content."""
    if not content:
        return ""

    # Try to find common reasoning fields
    reasoning_fields = [
        "comprehensive_reasoning",
        "expert_reasoning",
        "reasoning",
        "action_description",
        "evaluation_reasoning"
    ]

    for field in reasoning_fields:
        if f'"{field}"' in content:
            try:
                # Find the field and extract its value
                start = content.find(f'"{field}"')
                # Find the colon after the field name
                colon_pos = content.find(':', start)
                if colon_pos == -1:
                    continue
                # Find the opening quote of the value
                quote_start = content.find('"', colon_pos)
                if quote_start == -1:
                    continue
                # Find the closing quote (handle escaped quotes)
                pos = quote_start + 1
                while pos < len(content):
                    if content[pos] == '"' and content[pos-1] != '\\':
                        break
                    pos += 1
                if pos < len(content):
                    value = content[quote_start+1:pos]
                    # Clean up escaped characters
                    value = value.replace('\\n', ' ').replace('\\"', '"')
                    return value[:500]
            except:
                continue

    return ""


def analyze_trace_for_errors(langfuse: LangfuseClient, trace_id: str) -> dict:
    """
    Analyze a trace for errors and issues by examining observations.
    Focuses on GENERATION spans: ParameterSelection, ExecuteGPT_Tool, NodeSelection:EdgeEvaluation

    Args:
        langfuse: LangfuseClient instance
        trace_id: Trace ID to analyze

    Returns:
        Dict with error analysis results
    """
    try:
        trace = langfuse.get_trace(trace_id)
        observations = trace.get("observations", [])

        errors = []
        warnings = []
        null_outputs = []
        key_generations = []

        # Key span types to focus on
        key_span_names = [
            "ParameterSelection",
            "ExecuteGPT_Tool",
            "NodeSelection:EdgeEvaluation",
            "NodeEvaluation",
            "GEval"
        ]

        # Sort observations by startTime to get chronological order
        sorted_obs = sorted(observations, key=lambda x: x.get("startTime", ""), reverse=True)

        # Find GENERATION type observations with key names
        generation_spans = []
        for obs in sorted_obs:
            obs_type = obs.get("type", "")
            name = obs.get("name", "")

            # Check if it's a GENERATION or matches key span names
            is_key_span = any(key in name for key in key_span_names)
            is_generation = obs_type == "GENERATION"

            if is_generation or is_key_span:
                generation_spans.append(obs)

        # Analyze the most recent generation spans (up to 3)
        for obs in generation_spans[:5]:
            name = obs.get("name", "")
            status_msg = obs.get("statusMessage")
            level = obs.get("level")
            output = obs.get("output")
            input_data = obs.get("input")
            metadata = obs.get("metadata")

            span_info = {
                "name": name,
                "type": obs.get("type"),
                "latency": obs.get("latency"),
                "reasoning": None,
                "error": None
            }

            # Check for status messages/errors
            if status_msg:
                span_info["error"] = status_msg
                errors.append(f"{name}: {status_msg}")

            if level and level.upper() in ["ERROR", "WARNING"]:
                span_info["error"] = f"Level={level}"
                errors.append(f"{name}: Level={level}")

            # Try to extract reasoning from output first
            content = ""
            if output:
                if isinstance(output, dict):
                    # Check for 'content' field (common in LLM responses)
                    content = output.get("content", "")
                    if not content:
                        content = json.dumps(output)
                else:
                    content = str(output)

                reasoning = extract_reasoning_from_content(content)
                if reasoning:
                    span_info["reasoning"] = reasoning

                # Check for error indicators
                content_lower = content.lower()
                if "null value" in content_lower or "absence of" in content_lower:
                    if not span_info.get("reasoning"):
                        span_info["reasoning"] = extract_reasoning_from_content(content) or content[:300]
                    null_outputs.append(span_info["reasoning"] or content[:200])

            # If no reasoning from output, check metadata
            if not span_info.get("reasoning") and metadata:
                meta_str = json.dumps(metadata) if isinstance(metadata, dict) else str(metadata)
                reasoning = extract_reasoning_from_content(meta_str)
                if reasoning:
                    span_info["reasoning"] = reasoning

            # If still no reasoning, check input for context
            if not span_info.get("reasoning") and input_data:
                input_str = json.dumps(input_data) if isinstance(input_data, dict) else str(input_data)
                # Look for task context in input
                if "node_context" in input_str or "task_query" in input_str:
                    # Extract task query for context
                    try:
                        if isinstance(input_data, dict) and "node_context" in input_data:
                            span_info["input_context"] = input_data["node_context"][:300]
                    except:
                        pass

            key_generations.append(span_info)

        # Get the last generation's reasoning as primary debug info
        last_reasoning = None
        for gen in key_generations:
            if gen.get("reasoning"):
                last_reasoning = gen["reasoning"]
                break

        return {
            "errors": errors,
            "warnings": warnings,
            "null_outputs": null_outputs,
            "observation_count": len(observations),
            "key_generations": key_generations,
            "last_reasoning": last_reasoning
        }

    except Exception as e:
        return {"error": str(e)}


def get_task_trace_info(
    langfuse: LangfuseClient,
    task_id: str,
    project_id: str,
    analyze_errors: bool = True
) -> dict:
    """
    Get Langfuse trace information for a task.

    Args:
        langfuse: LangfuseClient instance
        task_id: Beam task ID (= Langfuse session ID)
        project_id: Langfuse project ID
        analyze_errors: Whether to analyze observations for errors

    Returns:
        Dict with trace info and URLs
    """
    try:
        traces = langfuse.get_traces_by_session(task_id, limit=10)

        if not traces:
            return {
                "found": False,
                "session_url": langfuse.get_session_url(task_id, project_id),
                "message": "No traces found for this session"
            }

        # Get the most recent trace (last execution)
        latest_trace = traces[0]  # Already sorted by timestamp desc
        trace_id = latest_trace.get("id")

        result = {
            "found": True,
            "trace_count": len(traces),
            "latest_trace_id": trace_id,
            "latest_trace_name": latest_trace.get("name"),
            "latest_timestamp": latest_trace.get("timestamp"),
            "latency": latest_trace.get("latency"),
            "total_cost": latest_trace.get("totalCost"),
            "session_url": langfuse.get_session_url(task_id, project_id),
            "trace_url": langfuse.get_trace_url(trace_id, project_id),
            "input": latest_trace.get("input"),
            "output": latest_trace.get("output"),
            "metadata": latest_trace.get("metadata")
        }

        # Analyze for errors if requested
        if analyze_errors and trace_id:
            analysis = analyze_trace_for_errors(langfuse, trace_id)
            result["analysis"] = analysis

        return result

    except Exception as e:
        return {
            "found": False,
            "error": str(e),
            "session_url": langfuse.get_session_url(task_id, project_id)
        }


def format_task_summary(task: dict, trace_info: dict = None) -> str:
    """Format a task for display."""
    task_id = task.get("id", "unknown")
    status = task.get("status", "UNKNOWN")
    created = task.get("createdAt", task.get("created_at", ""))
    error = task.get("error", task.get("errorMessage", ""))

    lines = [
        f"Task ID: {task_id}",
        f"Status: {status}",
        f"Created: {created}"
    ]

    if error:
        lines.append(f"Error: {error[:200]}...")

    if trace_info:
        if trace_info.get("found"):
            lines.extend([
                f"Traces: {trace_info.get('trace_count', 0)}",
                f"Latency: {trace_info.get('latency', 'N/A')}s",
                f"Cost: ${trace_info.get('total_cost', 0):.4f}",
                f"View Session: {trace_info.get('session_url')}",
                f"View Trace: {trace_info.get('trace_url')}"
            ])

            # Add error analysis
            analysis = trace_info.get("analysis", {})
            if analysis:
                obs_count = analysis.get("observation_count", 0)
                lines.append(f"Observations: {obs_count}")

                # Show last reasoning (primary debug info)
                last_reasoning = analysis.get("last_reasoning")
                if last_reasoning:
                    lines.append(f"\n  REASONING (from trace):")
                    # Word wrap the reasoning for better readability
                    reasoning_clean = last_reasoning.replace('\\n', ' ').strip()
                    lines.append(f"    {reasoning_clean[:400]}{'...' if len(reasoning_clean) > 400 else ''}")

                # Show key generation spans
                key_gens = analysis.get("key_generations", [])
                if key_gens:
                    lines.append(f"\n  Key Spans ({len(key_gens)}):")
                    for gen in key_gens[:3]:
                        name = gen.get("name", "unknown")
                        latency = gen.get("latency")
                        has_error = gen.get("error")
                        has_reasoning = gen.get("reasoning")

                        status_indicator = "!" if has_error else ("*" if has_reasoning else " ")
                        latency_str = f" ({latency:.1f}s)" if latency else ""
                        lines.append(f"    {status_indicator} {name}{latency_str}")

                        if has_error:
                            lines.append(f"        Error: {has_error[:100]}")

                # Show explicit errors
                errors = analysis.get("errors", [])
                if errors:
                    lines.append(f"\n  Errors Found: {len(errors)}")
                    for err in errors[:3]:
                        lines.append(f"    ! {err[:100]}")

                # Show data issues (null outputs)
                null_outputs = analysis.get("null_outputs", [])
                if null_outputs and not last_reasoning:
                    lines.append(f"\n  Data Issues:")
                    for issue in null_outputs[:2]:
                        issue_clean = issue.replace('\\n', ' ')
                        lines.append(f"    > {issue_clean[:200]}...")
        else:
            lines.append(f"Langfuse: {trace_info.get('message', trace_info.get('error', 'Not found'))}")
            lines.append(f"Session URL: {trace_info.get('session_url')}")

    return "\n  ".join(lines)


def print_summary(
    all_tasks: list,
    issue_tasks: list,
    by_status: dict,
    by_day: dict,
    days: int
):
    """Print a summary of tasks."""
    print(f"\n{'='*60}")
    print(f"TASK SUMMARY (Last {days} day{'s' if days > 1 else ''})")
    print(f"{'='*60}")

    print(f"\nTotal tasks: {len(all_tasks)}")
    print(f"Issue tasks: {len(issue_tasks)}")

    print(f"\n--- By Status ---")
    for status, tasks in sorted(by_status.items()):
        is_issue = status in ISSUE_STATUSES
        marker = "!" if is_issue else " "
        print(f"  {marker} {status}: {len(tasks)}")

    print(f"\n--- Issue Tasks by Day ---")
    issue_by_day = group_tasks_by_day(issue_tasks)
    for day, tasks in sorted(issue_by_day.items(), reverse=True):
        print(f"  {day}: {len(tasks)} issue task(s)")
        for t in tasks[:3]:  # Show first 3
            print(f"    - {t.get('id', 'unknown')[:8]}... ({t.get('status')})")
        if len(tasks) > 3:
            print(f"    ...and {len(tasks) - 3} more")

    print(f"\n{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="Debug Beam.ai issue/failed tasks using Langfuse traces",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List issue tasks from last 1 day
    python debug_issue_tasks.py abc123

    # List issue tasks from last 7 days with summary
    python debug_issue_tasks.py abc123 --days 7 --summary

    # Debug specific task with Langfuse trace
    python debug_issue_tasks.py abc123 --task-id xyz789

    # Use different Langfuse project
    python debug_issue_tasks.py abc123 --project other

Environment Variables (in .env):
    BEAM_API_KEY           Beam.ai API key
    BEAM_WORKSPACE_ID      Beam.ai workspace ID
    LANGFUSE_PUBLIC_KEY    Langfuse public key
    LANGFUSE_SECRET_KEY    Langfuse secret key
    LANGFUSE_HOST          Langfuse host (default: https://tracing.beamstudio.ai)
        """
    )
    parser.add_argument("agent_id", help="Beam agent ID")
    parser.add_argument("--days", "-d", type=int, default=1, choices=[1, 3, 7, 14, 30],
                        help="Look back N days (default: 1)")
    parser.add_argument("--task-id", "-t", help="Debug specific task ID")
    parser.add_argument("--summary", "-s", action="store_true",
                        help="Show summary grouped by status and day")
    parser.add_argument("--project", "-p", default="prod", choices=["prod", "bid"],
                        help="Langfuse project (default: prod)")
    parser.add_argument("--workspace", "-w", default="prod", choices=["prod", "bid"],
                        help="Beam workspace (default: prod)")
    parser.add_argument("--limit", "-l", type=int, default=10,
                        help="Max tasks to show details for (default: 10)")
    parser.add_argument("--output", "-o", help="Output file path (JSON)")
    parser.add_argument("--no-trace", action="store_true",
                        help="Skip Langfuse trace lookup")
    parser.add_argument("--save", action="store_true",
                        help="Save debug report to 04-workspace/agents/{agent_name}/debug/")

    args = parser.parse_args()

    try:
        # Initialize clients
        beam = BeamClient(workspace=args.workspace)
        project_id = get_project_id(args.project)
        langfuse = LangfuseClient(project_id=project_id)

        # Calculate date range
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=args.days)
        start_str = start_date.strftime("%Y-%m-%dT00:00:00Z")
        end_str = end_date.strftime("%Y-%m-%dT23:59:59Z")

        # Fetch agent info to get name
        agent_info = beam.get(f"/agent/{args.agent_id}")
        agent_name = agent_info.get("name", args.agent_id)

        print(f"Agent: {agent_name} ({args.agent_id})")
        print(f"Date range: {start_str} to {end_str}")

        # Debug specific task
        if args.task_id:
            print(f"\n--- Debugging Task: {args.task_id} ---\n")

            # Get task details
            task = beam.get(f"/agent-tasks/{args.task_id}")
            print(f"Task Status: {task.get('status')}")
            print(f"Created: {task.get('createdAt', task.get('created_at'))}")

            if task.get("error") or task.get("errorMessage"):
                print(f"Error: {task.get('error', task.get('errorMessage'))}")

            # Get Langfuse traces
            if not args.no_trace:
                print(f"\n--- Langfuse Trace Info ---")
                trace_info = get_task_trace_info(langfuse, args.task_id, project_id)

                if trace_info.get("found"):
                    print(f"Traces found: {trace_info.get('trace_count')}")
                    print(f"Latest trace: {trace_info.get('latest_trace_name')}")
                    print(f"Timestamp: {trace_info.get('latest_timestamp')}")
                    print(f"Latency: {trace_info.get('latency')}s")
                    print(f"Cost: ${trace_info.get('total_cost', 0):.4f}")
                    print(f"\nView Session: {trace_info.get('session_url')}")
                    print(f"View Trace: {trace_info.get('trace_url')}")

                    # Show analysis results
                    analysis = trace_info.get("analysis", {})
                    if analysis:
                        last_reasoning = analysis.get("last_reasoning")
                        if last_reasoning:
                            print(f"\n--- Debug Reasoning ---")
                            reasoning_clean = last_reasoning.replace('\\n', ' ').strip()
                            print(f"{reasoning_clean[:600]}{'...' if len(reasoning_clean) > 600 else ''}")

                        key_gens = analysis.get("key_generations", [])
                        if key_gens:
                            print(f"\n--- Key Spans ({len(key_gens)}) ---")
                            for gen in key_gens[:5]:
                                name = gen.get("name", "unknown")
                                latency = gen.get("latency")
                                has_error = gen.get("error")
                                latency_str = f" ({latency:.1f}s)" if latency else ""
                                print(f"  {'!' if has_error else '*'} {name}{latency_str}")
                                if has_error:
                                    print(f"      Error: {has_error[:150]}")

                    if trace_info.get("output"):
                        print(f"\nOutput preview:")
                        output = trace_info.get("output")
                        if isinstance(output, dict):
                            print(json.dumps(output, indent=2)[:500])
                        else:
                            print(str(output)[:500])
                else:
                    print(f"No traces found: {trace_info.get('message', trace_info.get('error'))}")
                    print(f"Session URL: {trace_info.get('session_url')}")

                    # Show Beam task details when no traces available
                    print(f"\n--- Beam Task Details (no traces) ---")
                    graph_state = task.get("graphState", {})
                    current_node = graph_state.get("current", {})

                    if current_node:
                        node_name = current_node.get("tool", {}).get("name", "Unknown")
                        on_error = current_node.get("on_error", "N/A")
                        print(f"Current Node: {node_name}")
                        print(f"On Error: {on_error}")

                    # Check for user questions (parameter extraction issues)
                    task_nodes = task.get("agentTaskNodes", [])
                    for node in task_nodes:
                        user_questions = node.get("userQuestions", [])
                        if user_questions:
                            print(f"\n--- User Input Required ---")
                            for q in user_questions:
                                param = q.get("parameter", "unknown")
                                question = q.get("question", "")
                                answer = q.get("answer")
                                print(f"  Parameter: {param}")
                                print(f"  Question: {question[:200]}")
                                print(f"  Answer: {answer if answer else '(awaiting input)'}")

                        # Show tool reasoning
                        tool_data = node.get("toolData", {})
                        reasoning = tool_data.get("reasoning", {})
                        if reasoning:
                            print(f"\n--- Parameter Extraction Reasoning ---")
                            for param, reason in reasoning.items():
                                print(f"  {param}:")
                                print(f"    {reason[:300]}...")

            # Save debug report if requested
            if args.save:
                report_path = save_debug_report(
                    agent_name,
                    args.task_id,
                    task,
                    trace_info,
                    args.workspace
                )
                print(f"\nDebug report saved: {report_path}")

            return

        # Fetch all tasks
        all_tasks = fetch_all_tasks(beam, args.agent_id, start_str, end_str)
        print(f"Found {len(all_tasks)} total tasks")

        # Filter and group
        issue_tasks = filter_issue_tasks(all_tasks)
        by_status = group_tasks_by_status(all_tasks)

        if args.summary:
            by_day = group_tasks_by_day(all_tasks)
            print_summary(all_tasks, issue_tasks, by_status, by_day, args.days)

        # Show issue task details
        if issue_tasks:
            print(f"\n--- Issue Tasks ({len(issue_tasks)} found) ---\n")

            tasks_to_show = issue_tasks[:args.limit]
            for i, task in enumerate(tasks_to_show, 1):
                task_id = task.get("id")
                print(f"[{i}/{len(tasks_to_show)}] {'-'*50}")

                trace_info = None
                if not args.no_trace:
                    trace_info = get_task_trace_info(langfuse, task_id, project_id)

                print(f"  {format_task_summary(task, trace_info)}")
                print()

            if len(issue_tasks) > args.limit:
                print(f"...and {len(issue_tasks) - args.limit} more issue tasks")
                print(f"Use --limit to show more, or --task-id to debug specific task")

        else:
            print(f"\nNo issue tasks found in the last {args.days} day(s)")

        # Output to file
        if args.output:
            output_data = {
                "agent_id": args.agent_id,
                "date_range": {"start": start_str, "end": end_str},
                "total_tasks": len(all_tasks),
                "issue_tasks_count": len(issue_tasks),
                "by_status": {k: len(v) for k, v in by_status.items()},
                "issue_tasks": issue_tasks
            }
            Path(args.output).write_text(json.dumps(output_data, indent=2))
            print(f"\nResults written to: {args.output}")

    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        if hasattr(e, 'response'):
            print(f"API error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
