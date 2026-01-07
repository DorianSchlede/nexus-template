#!/usr/bin/env python3
"""
Analyze Consistency Script for test-case-analyzer calibration

Calculates per-criterion consistency scores and accuracy vs ground truth.

Usage:
    python analyze-consistency.py --input baseline-results.json
    python analyze-consistency.py --input baseline-results.json --output metrics.md
"""

import argparse
import json
from pathlib import Path
from collections import Counter
from datetime import datetime


def calculate_consistency(runs: list) -> dict:
    """
    Calculate consistency score for a set of runs.

    Consistency = proportion of runs that agree on each criterion.

    Returns dict with per-criterion and overall consistency.
    """
    if not runs:
        return {"overall": 0.0, "per_criterion": {}}

    num_runs = len(runs)

    # Collect all criteria results across runs
    criteria_results = {}
    for run in runs:
        for criterion, status in run.get("criteria_results", {}).items():
            if criterion not in criteria_results:
                criteria_results[criterion] = []
            criteria_results[criterion].append(status)

    # Calculate per-criterion consistency
    per_criterion = {}
    for criterion, statuses in criteria_results.items():
        # Count most common status
        counter = Counter(statuses)
        most_common_count = counter.most_common(1)[0][1]
        consistency = most_common_count / num_runs
        per_criterion[criterion] = {
            "consistency": consistency,
            "distribution": dict(counter),
            "most_common": counter.most_common(1)[0][0]
        }

    # Overall consistency = average of per-criterion
    overall_consistency = sum(c["consistency"] for c in per_criterion.values()) / len(per_criterion) if per_criterion else 0.0

    # Also check overall status consistency
    overall_statuses = [run.get("overall") for run in runs]
    overall_counter = Counter(overall_statuses)
    overall_status_consistency = overall_counter.most_common(1)[0][1] / num_runs if overall_statuses else 0.0

    return {
        "overall": overall_consistency,
        "overall_status_consistency": overall_status_consistency,
        "per_criterion": per_criterion
    }


def calculate_accuracy(runs: list, expected: dict) -> dict:
    """
    Calculate accuracy vs ground truth.

    Accuracy = proportion of criteria that match expected outcome.

    Returns dict with per-criterion and overall accuracy.
    """
    if not runs or not expected:
        return {"overall": 0.0, "per_criterion": {}}

    expected_criteria = expected.get("criteria_results", {})
    expected_overall = expected.get("overall")

    # Use first run (or mode of runs) for accuracy check
    # In consistent system, all runs should produce same result
    first_run = runs[0]
    run_criteria = first_run.get("criteria_results", {})
    run_overall = first_run.get("overall")

    # Build mapping from criterion ID (C1, C2, etc.) to criterion names
    criterion_id_to_name = {
        "C1": "Agent responded to task",
        "C2": "No errors in execution",
        "C3": "Task completed",
        "C4": "Used appropriate tools"
    }

    per_criterion = {}
    matches = 0
    total = 0

    # Match by criterion ID if expected uses IDs, otherwise by name
    for criterion_id, expected_status in expected_criteria.items():
        exp_status = expected_status.get("status") if isinstance(expected_status, dict) else expected_status

        # Get the criterion name for matching
        criterion_name = criterion_id_to_name.get(criterion_id, criterion_id)
        actual_status = run_criteria.get(criterion_name)

        # Handle UNCERTAIN - if expected is UNCERTAIN, accept any answer
        if exp_status == "UNCERTAIN":
            match = True  # Don't penalize for uncertain ground truth
        else:
            match = actual_status == exp_status

        per_criterion[criterion_name] = {
            "expected": exp_status,
            "actual": actual_status,
            "match": match
        }

        if match:
            matches += 1
        total += 1

    overall_accuracy = matches / total if total > 0 else 0.0

    # Overall status match (handle UNCERTAIN)
    if expected_overall == "UNCERTAIN":
        overall_match = True  # Accept any result for uncertain ground truth
    else:
        overall_match = run_overall == expected_overall

    return {
        "overall": overall_accuracy,
        "overall_status_match": overall_match,
        "matches": matches,
        "total": total,
        "per_criterion": per_criterion
    }


def analyze_results(results_file: str) -> dict:
    """
    Analyze calibration results and calculate all metrics.
    """
    with open(results_file, "r") as f:
        results = json.load(f)

    analysis = {
        "metadata": {
            "source_file": results_file,
            "analyzed_at": datetime.now().isoformat(),
            "num_items": len(results.get("items", [])),
            "runs_per_item": results.get("metadata", {}).get("num_runs", 0)
        },
        "items": [],
        "summary": {}
    }

    total_consistency = 0
    total_accuracy = 0
    total_criteria_consistency = {}

    for item in results.get("items", []):
        item_id = item.get("item_id")
        runs = item.get("runs", [])
        expected = item.get("expected_output", {})

        # Calculate metrics
        consistency = calculate_consistency(runs)
        accuracy = calculate_accuracy(runs, expected)

        item_analysis = {
            "item_id": item_id,
            "scenario": item.get("scenario"),
            "run_count": len(runs),
            "consistency": consistency,
            "accuracy": accuracy
        }

        analysis["items"].append(item_analysis)

        # Accumulate for summary
        total_consistency += consistency["overall"]
        total_accuracy += accuracy["overall"]

        for criterion, data in consistency["per_criterion"].items():
            if criterion not in total_criteria_consistency:
                total_criteria_consistency[criterion] = []
            total_criteria_consistency[criterion].append(data["consistency"])

    # Summary statistics
    num_items = len(analysis["items"])
    analysis["summary"] = {
        "avg_consistency": total_consistency / num_items if num_items > 0 else 0.0,
        "avg_accuracy": total_accuracy / num_items if num_items > 0 else 0.0,
        "target_consistency": 0.95,
        "target_accuracy": 0.90,
        "consistency_met": (total_consistency / num_items if num_items > 0 else 0.0) >= 0.95,
        "accuracy_met": (total_accuracy / num_items if num_items > 0 else 0.0) >= 0.90,
        "per_criterion_avg": {
            criterion: sum(scores) / len(scores)
            for criterion, scores in total_criteria_consistency.items()
        }
    }

    return analysis


def generate_report(analysis: dict, output_file: str = None) -> str:
    """
    Generate markdown report from analysis.
    """
    summary = analysis.get("summary", {})
    items = analysis.get("items", [])
    metadata = analysis.get("metadata", {})

    report = f"""# Calibration Analysis Report

**Generated**: {metadata.get('analyzed_at', 'unknown')}
**Source**: {metadata.get('source_file', 'unknown')}
**Items Analyzed**: {metadata.get('num_items', 0)}
**Runs Per Item**: {metadata.get('runs_per_item', 0)}

---

## Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Avg Consistency | {summary.get('avg_consistency', 0):.2%} | >= 95% | {'PASS' if summary.get('consistency_met') else 'FAIL'} |
| Avg Accuracy | {summary.get('avg_accuracy', 0):.2%} | >= 90% | {'PASS' if summary.get('accuracy_met') else 'FAIL'} |

---

## Per-Criterion Consistency

| Criterion | Avg Consistency |
|-----------|-----------------|
"""

    for criterion, avg in summary.get("per_criterion_avg", {}).items():
        report += f"| {criterion} | {avg:.2%} |\n"

    report += """
---

## Per-Item Analysis

"""

    for item in items:
        item_id = item.get("item_id")
        scenario = item.get("scenario")
        consistency = item.get("consistency", {})
        accuracy = item.get("accuracy", {})

        report += f"""### {item_id} ({scenario})

**Consistency**: {consistency.get('overall', 0):.2%}
**Accuracy**: {accuracy.get('overall', 0):.2%}

| Criterion | Consistency | Expected | Actual | Match |
|-----------|-------------|----------|--------|-------|
"""

        for criterion, c_data in consistency.get("per_criterion", {}).items():
            a_data = accuracy.get("per_criterion", {}).get(criterion, {})
            report += f"| {criterion} | {c_data.get('consistency', 0):.2%} | {a_data.get('expected', 'N/A')} | {a_data.get('actual', 'N/A')} | {'Y' if a_data.get('match') else 'N'} |\n"

        report += "\n"

    report += """---

## Next Steps

"""

    if summary.get("consistency_met") and summary.get("accuracy_met"):
        report += """**TARGETS MET**

The test-case-analyzer meets both consistency (>= 95%) and accuracy (>= 90%) targets.
No tuning required at this time.

Recommended:
- [ ] Document current analyzer configuration as baseline
- [ ] Create synthetic FAIL cases to stress-test analyzer
- [ ] Consider more complex criteria for future calibration
"""
    else:
        report += """**TUNING REQUIRED**

One or more targets not met:
"""
        if not summary.get("consistency_met"):
            report += f"- Consistency at {summary.get('avg_consistency', 0):.2%} (target: >= 95%)\n"
        if not summary.get("accuracy_met"):
            report += f"- Accuracy at {summary.get('avg_accuracy', 0):.2%} (target: >= 90%)\n"

        report += """
Recommended:
- [ ] Analyze divergence points for inconsistent criteria
- [ ] Update analyzer prompt with explicit evaluation rules
- [ ] Rewrite ambiguous criteria in MECE format
- [ ] Re-run calibration after tuning
"""

    if output_file:
        with open(output_file, "w") as f:
            f.write(report)
        print(f"Report saved to: {output_file}")

    return report


def main():
    parser = argparse.ArgumentParser(description="Analyze calibration consistency")
    parser.add_argument("--input", required=True, help="Input results JSON file")
    parser.add_argument("--output", help="Output markdown report file")
    parser.add_argument("--json-output", help="Output analysis as JSON")

    args = parser.parse_args()

    # Run analysis
    analysis = analyze_results(args.input)

    # Save JSON if requested
    if args.json_output:
        with open(args.json_output, "w") as f:
            json.dump(analysis, f, indent=2, default=str)
        print(f"JSON analysis saved to: {args.json_output}")

    # Generate and save report
    output_file = args.output
    if not output_file:
        output_file = str(Path(args.input).parent / "baseline-metrics.md")

    report = generate_report(analysis, output_file)

    # Print summary to stdout
    summary = analysis.get("summary", {})
    print(f"\n=== CALIBRATION SUMMARY ===")
    print(f"Consistency: {summary.get('avg_consistency', 0):.2%} (target: >= 95%)")
    print(f"Accuracy: {summary.get('avg_accuracy', 0):.2%} (target: >= 90%)")
    print(f"Status: {'TARGETS MET' if summary.get('consistency_met') and summary.get('accuracy_met') else 'TUNING REQUIRED'}")


if __name__ == "__main__":
    main()
