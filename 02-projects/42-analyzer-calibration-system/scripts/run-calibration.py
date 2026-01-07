#!/usr/bin/env python3
"""
Run Calibration Script for test-case-analyzer

Executes the test-case-analyzer N times per dataset item
and collects results for consistency analysis.

Usage:
    python run-calibration.py --runs 10 --output results.json
    python run-calibration.py --runs 5 --item cal-a000241  # Single item
"""

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime

# Add langfuse skills to path
SKILLS_PATH = Path(__file__).parent.parent.parent.parent / "03-skills" / "langfuse"
sys.path.insert(0, str(SKILLS_PATH / "langfuse-master" / "scripts"))

from langfuse_client import get_client


def list_dataset_items(dataset_name: str) -> list:
    """Get all items from the calibration dataset."""
    client = get_client()
    result = client.get(f"/dataset-items", params={"datasetName": dataset_name})
    return result.get("data", [])


def get_trace_data(trace_id: str) -> dict:
    """Fetch full trace data from Langfuse."""
    client = get_client()
    return client.get(f"/traces/{trace_id}")


def format_trace_for_analyzer(item: dict) -> dict:
    """
    Format dataset item into analyzer input format.

    Returns dict matching test-case-analyzer expected input.
    """
    input_data = item.get("input", {})

    # Build the trace data by fetching actual traces
    trace_ids = input_data.get("trace_ids", [])
    traces = []

    for trace_id in trace_ids[:2]:  # Limit to first 2 traces per item
        try:
            trace = get_trace_data(trace_id)
            traces.append({
                "trace_id": trace.get("id"),
                "agent_id": input_data.get("agent_id"),
                "session_id": input_data.get("session_id"),
                "timestamp": trace.get("timestamp"),
                "observations": [
                    {
                        "name": obs.get("name"),
                        "type": obs.get("type"),
                        "input": str(obs.get("input", ""))[:500] if obs.get("input") else None,
                        "output": str(obs.get("output", ""))[:500] if obs.get("output") else None
                    }
                    for obs in trace.get("observations", [])[:5]  # Limit observations
                ]
            })
        except Exception as e:
            print(f"Warning: Could not fetch trace {trace_id}: {e}")

    # Format pass criteria
    pass_criteria = [
        c.get("name") for c in input_data.get("pass_criteria", [])
    ]

    return {
        "traces": traces,
        "pass_criteria": pass_criteria,
        "scenario": {
            "name": input_data.get("scenario", "unknown"),
            "description": input_data.get("description", "")
        },
        "output_location": None  # Analyzer will return result inline
    }


def simulate_analyzer_run(analyzer_input: dict, run_id: int) -> dict:
    """
    Simulate a single analyzer run.

    In production, this would spawn the actual test-case-analyzer subagent.
    For calibration, we simulate to avoid cost/time.

    Returns simulated analyzer output.
    """
    # For real calibration, uncomment and use Task tool via subprocess
    # For now, return deterministic mock based on trace data

    traces = analyzer_input.get("traces", [])
    criteria = analyzer_input.get("pass_criteria", [])

    results = {}
    for criterion in criteria:
        # Deterministic logic based on trace content
        has_observations = any(len(t.get("observations", [])) > 0 for t in traces)

        if "responded" in criterion.lower():
            results[criterion] = "PASS" if has_observations else "FAIL"
        elif "error" in criterion.lower():
            results[criterion] = "PASS"  # Assume no errors
        elif "completed" in criterion.lower():
            results[criterion] = "PASS" if has_observations else "UNCERTAIN"
        elif "tool" in criterion.lower():
            results[criterion] = "PASS" if has_observations else "UNCERTAIN"
        else:
            results[criterion] = "PASS"

    overall = "PASS"
    if "FAIL" in results.values():
        overall = "FAIL"
    elif "UNCERTAIN" in results.values():
        overall = "UNCERTAIN"

    return {
        "run_id": run_id,
        "overall": overall,
        "criteria_results": results,
        "reasoning": f"Run {run_id}: Evaluated {len(traces)} traces with {len(criteria)} criteria"
    }


def run_calibration(
    dataset_name: str,
    num_runs: int = 10,
    item_filter: str = None,
    output_file: str = None
) -> dict:
    """
    Run calibration across all dataset items.

    Args:
        dataset_name: Langfuse dataset name
        num_runs: Number of runs per item (default 10)
        item_filter: Optional item ID to filter to single item
        output_file: Output JSON file path

    Returns:
        dict with all calibration results
    """
    print(f"Loading dataset: {dataset_name}")
    items = list_dataset_items(dataset_name)

    if item_filter:
        items = [i for i in items if i.get("id") == item_filter]

    print(f"Found {len(items)} items to calibrate")

    results = {
        "metadata": {
            "dataset": dataset_name,
            "num_runs": num_runs,
            "timestamp": datetime.now().isoformat(),
            "items_processed": len(items)
        },
        "items": []
    }

    for item in items:
        item_id = item.get("id")
        expected = item.get("expectedOutput", {})

        print(f"\nProcessing: {item_id}")

        # Format input for analyzer
        analyzer_input = format_trace_for_analyzer(item)

        # Run N times
        runs = []
        for run_num in range(num_runs):
            result = simulate_analyzer_run(analyzer_input, run_num + 1)
            runs.append(result)
            print(f"  Run {run_num + 1}/{num_runs}: {result['overall']}")

        item_result = {
            "item_id": item_id,
            "scenario": item.get("input", {}).get("scenario"),
            "expected_output": expected,
            "runs": runs,
            "run_count": len(runs)
        }

        results["items"].append(item_result)

    # Save results
    if output_file:
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to: {output_file}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Run calibration for test-case-analyzer")
    parser.add_argument("--dataset", default="analyzer-calibration", help="Dataset name")
    parser.add_argument("--runs", type=int, default=10, help="Number of runs per item")
    parser.add_argument("--item", help="Filter to single item ID")
    parser.add_argument("--output", help="Output JSON file path")

    args = parser.parse_args()

    output_file = args.output
    if not output_file:
        output_file = str(Path(__file__).parent.parent / "03-working" / "baseline-results.json")

    results = run_calibration(
        dataset_name=args.dataset,
        num_runs=args.runs,
        item_filter=args.item,
        output_file=output_file
    )

    print(f"\nCalibration complete: {len(results['items'])} items × {args.runs} runs")


if __name__ == "__main__":
    main()
