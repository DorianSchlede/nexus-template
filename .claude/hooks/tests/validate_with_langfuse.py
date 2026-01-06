"""
Validate multi-session handover using Langfuse trace data.

This script:
1. Instruments session hooks with Langfuse tracing
2. Queries Langfuse for handover traces
3. Analyzes session transitions and detection patterns
4. Validates multi-session tracking behavior
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

# Set up Langfuse environment
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-49a255c7-0639-426e-9dad-2908881402ca"
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-226d37cd-4d4d-4411-b4c1-90d8e87954a8"
os.environ["LANGFUSE_HOST"] = "http://localhost:3002"

try:
    from langfuse import Langfuse
    LANGFUSE_AVAILABLE = True
except ImportError:
    LANGFUSE_AVAILABLE = False
    print("WARNING: Langfuse not installed. Install with: pip install langfuse")

# Add hooks to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def query_handover_traces(hours_back=24):
    """Query Langfuse for session handover traces."""
    if not LANGFUSE_AVAILABLE:
        print("Langfuse not available, skipping trace query")
        return []

    try:
        langfuse = Langfuse()
        print(f"Connected to Langfuse: {os.getenv('LANGFUSE_HOST')}")

        # Fetch recent traces
        print(f"\nFetching traces from last {hours_back} hours...")

        # Get traces with session_handover tag
        traces = langfuse.fetch_traces(
            name="session_handover",
            limit=50
        )

        print(f"Found {len(traces.data)} handover traces\n")
        return traces.data

    except Exception as e:
        print(f"Error querying Langfuse: {e}")
        return []


def analyze_trace(trace):
    """Analyze a single handover trace."""
    print("=" * 80)
    print(f"Trace: {trace.id}")
    print("-" * 80)

    # Basic info
    print(f"Timestamp: {trace.timestamp}")
    print(f"Session ID: {trace.session_id}")

    # Metadata
    if hasattr(trace, 'metadata') and trace.metadata:
        print(f"\nMetadata:")
        for key, value in trace.metadata.items():
            print(f"  {key}: {value}")

    # Input/Output
    if hasattr(trace, 'input') and trace.input:
        print(f"\nInput:")
        print(f"  {json.dumps(trace.input, indent=2)[:200]}...")

    if hasattr(trace, 'output') and trace.output:
        print(f"\nOutput:")
        print(f"  {json.dumps(trace.output, indent=2)[:200]}...")

    # Observations (spans)
    if hasattr(trace, 'observations'):
        print(f"\nObservations: {len(trace.observations)}")
        for obs in trace.observations[:5]:  # Show first 5
            print(f"  - {obs.name} ({obs.type})")

    print()


def analyze_session_patterns(traces):
    """Analyze patterns across multiple session traces."""
    if not traces:
        print("No traces to analyze")
        return

    print("=" * 80)
    print("SESSION PATTERN ANALYSIS")
    print("=" * 80)

    # Group by session_id
    sessions = {}
    for trace in traces:
        sid = trace.session_id
        if sid not in sessions:
            sessions[sid] = []
        sessions[sid].append(trace)

    print(f"\nTotal unique sessions: {len(sessions)}")

    # Analyze each session
    for sid, session_traces in sessions.items():
        print(f"\nSession: {sid[:32]}...")
        print(f"  Traces: {len(session_traces)}")

        # Sort by timestamp
        sorted_traces = sorted(session_traces, key=lambda t: t.timestamp)

        # Show trace sequence
        for i, trace in enumerate(sorted_traces, 1):
            source = trace.metadata.get('source', 'unknown') if hasattr(trace, 'metadata') and trace.metadata else 'unknown'
            project = trace.metadata.get('detected_project', 'none') if hasattr(trace, 'metadata') and trace.metadata else 'none'
            print(f"    {i}. {trace.timestamp.strftime('%H:%M:%S')} | {source:8} | project: {project}")


def create_handover_trace_example():
    """Create example trace to demonstrate instrumentation."""
    if not LANGFUSE_AVAILABLE:
        print("Langfuse not available")
        return

    print("=" * 80)
    print("CREATING EXAMPLE HANDOVER TRACE")
    print("=" * 80)

    langfuse = Langfuse()

    # Simulate a session handover scenario
    session_id = "example-session-" + datetime.now().strftime("%H%M%S")

    # Create trace
    trace = langfuse.trace(
        name="session_handover",
        session_id=session_id,
        metadata={
            "source": "compact",
            "nexus_root": str(Path.cwd()),
            "hook_version": "v3.2_multi_session"
        },
        input={
            "session_id": session_id,
            "source": "compact",
            "current_projects": ["28-handover-test-suite"]
        }
    )

    # Add detection spans
    detect_span = trace.span(
        name="detect_project",
        input={
            "method": "session_id_match",
            "session_id": session_id
        },
        output={
            "project_id": "28-handover-test-suite",
            "found_via": "session_ids_list",
            "total_sessions_tracked": 4
        },
        metadata={
            "detection_time_ms": 15
        }
    )

    phase_span = trace.span(
        name="detect_phase",
        input={
            "project_id": "28-handover-test-suite",
            "method": "metadata_first"
        },
        output={
            "phase": "execution",
            "skill": "execute-project",
            "source": "resume-context.md"
        },
        metadata={
            "detection_time_ms": 8
        }
    )

    # Finalize trace
    trace.update(
        output={
            "context_mode": "compact",
            "detected_project": "28-handover-test-suite",
            "phase": "execution",
            "skill": "execute-project",
            "session_ids_count": 4
        },
        metadata={
            "total_time_ms": 150
        }
    )

    print(f"\nCreated trace: {trace.id}")
    print(f"Session: {session_id}")
    print(f"View in Langfuse: {os.getenv('LANGFUSE_HOST')}/traces/{trace.id}")
    print()

    # Flush to ensure it's sent
    langfuse.flush()

    return trace


def query_project_traces(project_id="28-handover-test-suite"):
    """Query traces related to a specific project."""
    if not LANGFUSE_AVAILABLE:
        return []

    print("=" * 80)
    print(f"PROJECT-SPECIFIC TRACE ANALYSIS: {project_id}")
    print("=" * 80)

    langfuse = Langfuse()

    # Fetch traces
    # Note: Langfuse doesn't support filtering by metadata in fetch_traces
    # We'll fetch all and filter manually
    all_traces = langfuse.fetch_traces(limit=100)

    # Filter by project
    project_traces = []
    for trace in all_traces.data:
        if hasattr(trace, 'metadata') and trace.metadata:
            if trace.metadata.get('detected_project') == project_id:
                project_traces.append(trace)

    print(f"\nFound {len(project_traces)} traces for project {project_id}")

    # Analyze session IDs
    session_ids = set()
    for trace in project_traces:
        if trace.session_id:
            session_ids.add(trace.session_id)

    print(f"Unique sessions that worked on this project: {len(session_ids)}")

    for sid in sorted(session_ids):
        print(f"  - {sid[:40]}...")

    return project_traces


def validate_multi_session_behavior():
    """Validate that multi-session tracking is working correctly."""
    print("=" * 80)
    print("MULTI-SESSION VALIDATION")
    print("=" * 80)

    # Check current project state
    sys.path.insert(0, '.claude/hooks')
    from save_resume_state import find_nexus_root
    from utils.project_state import detect_project_state

    nexus_root = find_nexus_root()
    project_path = nexus_root / "02-projects" / "28-handover-test-suite"

    state = detect_project_state(project_path)

    if not state:
        print("Could not detect project state")
        return False

    print(f"\nCurrent Project State:")
    print(f"  Project: {state.project_id} - {state.name}")
    print(f"  Status: {state.status}")
    print(f"  Progress: {state.progress_percent}%")
    print(f"  Sessions tracked: {len(state.session_ids)}")

    print(f"\nSession IDs in resume-context.md:")
    for i, sid in enumerate(state.session_ids, 1):
        print(f"    {i}. {sid}")

    # If Langfuse available, compare with traces
    if LANGFUSE_AVAILABLE:
        print(f"\nComparing with Langfuse traces...")
        project_traces = query_project_traces("28-handover-test-suite")

        if project_traces:
            trace_sessions = set(t.session_id for t in project_traces if t.session_id)
            file_sessions = set(state.session_ids)

            print(f"\nSession comparison:")
            print(f"  In resume-context.md: {len(file_sessions)}")
            print(f"  In Langfuse traces:   {len(trace_sessions)}")

            # Sessions in traces but not in file
            missing_from_file = trace_sessions - file_sessions
            if missing_from_file:
                print(f"\n  Sessions in traces but not in file ({len(missing_from_file)}):")
                for sid in list(missing_from_file)[:5]:
                    print(f"    - {sid[:40]}...")

            # Sessions in file but not in traces
            missing_from_traces = file_sessions - trace_sessions
            if missing_from_traces:
                print(f"\n  Sessions in file but not in traces ({len(missing_from_traces)}):")
                for sid in list(missing_from_traces)[:5]:
                    print(f"    - {sid[:40]}...")

    print("\nValidation complete")
    return True


def main():
    """Main validation workflow."""
    print("\n")
    print("+" + "=" * 78 + "+")
    print("|" + " " * 22 + "LANGFUSE TRACE VALIDATION" + " " * 31 + "|")
    print("+" + "=" * 78 + "+")
    print()

    if not LANGFUSE_AVAILABLE:
        print("Langfuse SDK not installed. Install with:")
        print("  pip install langfuse")
        print("\nContinuing with local validation only...\n")

    # 1. Validate current multi-session state
    validate_multi_session_behavior()

    if LANGFUSE_AVAILABLE:
        # 2. Create example trace
        print("\n")
        create_handover_trace_example()

        # 3. Query recent traces
        print("\n")
        traces = query_handover_traces(hours_back=24)

        if traces:
            # Analyze first few traces
            for trace in traces[:3]:
                analyze_trace(trace)

            # Pattern analysis
            analyze_session_patterns(traces)
        else:
            print("No handover traces found in Langfuse")
            print("\nTo start collecting traces:")
            print("1. Add Langfuse instrumentation to session_start.py")
            print("2. Run Claude Code sessions")
            print("3. Re-run this script to analyze")

    print("\n" + "=" * 80)
    print("VALIDATION COMPLETE")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
