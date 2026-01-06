#!/usr/bin/env python
"""Validate evaluation metrics consistency across all datasets."""

import json
import os
from pathlib import Path

DATASETS_DIR = Path(__file__).parent.parent / "04-outputs" / "datasets" / "final"


def validate_metrics_consistency(data, filename):
    """Check that evaluation metrics are consistent."""
    issues = []

    metadata = data.get('metadata', {})
    prompt_dataset = data.get('promptDataset', {})
    prompt_executions = data.get('PromptExecutions', {})

    items = prompt_dataset.get('items', [])
    executions = prompt_executions.get('executions', [])

    # 1. Check metadata counts match actual data
    item_count = metadata.get('itemCount', 0)
    if item_count != len(items):
        issues.append(f"metadata.itemCount ({item_count}) != actual items ({len(items)})")

    succeeded = metadata.get('succeededCount', 0)
    failed = metadata.get('failedCount', 0)
    if succeeded + failed != len(items):
        issues.append(f"succeeded ({succeeded}) + failed ({failed}) != items ({len(items)})")

    # 2. Check executions match items
    if len(executions) != len(items):
        issues.append(f"executions ({len(executions)}) != items ({len(items)})")

    # 3. Check each execution has consistent evaluation
    actual_succeeded = 0
    actual_failed = 0
    score_sum = 0

    for i, ex in enumerate(executions):
        eval_result = ex.get('evaluation', {})

        # Check evaluation structure
        if not eval_result:
            issues.append(f"execution[{i}] missing evaluation")
            continue

        success = eval_result.get('success', False)
        score = eval_result.get('score', 0)

        if success:
            actual_succeeded += 1
        else:
            actual_failed += 1

        score_sum += score

        # Check evaluations array exists
        evals = eval_result.get('evaluations', [])
        if not evals:
            issues.append(f"execution[{i}] has no evaluation metrics")

        # Check score matches success
        if success and score < 0.5:
            issues.append(f"execution[{i}] success=True but score={score}")
        if not success and score >= 1.0:
            issues.append(f"execution[{i}] success=False but score={score}")

    # 4. Check metadata counts match actual
    if actual_succeeded != succeeded:
        issues.append(f"actual succeeded ({actual_succeeded}) != metadata ({succeeded})")
    if actual_failed != failed:
        issues.append(f"actual failed ({actual_failed}) != metadata ({failed})")

    # 5. Check average score
    if executions:
        actual_avg = score_sum / len(executions)
        metadata_avg = metadata.get('averageScore', 0)
        if abs(actual_avg - metadata_avg) > 0.01:
            issues.append(f"actual avgScore ({actual_avg:.4f}) != metadata ({metadata_avg})")

    # 6. Check evals in metatunerPromptInput match output schema
    metatuner = data.get('metatunerPromptInput', {})
    output_schema = metatuner.get('outputSchema', {})
    evals = metatuner.get('evals', [])

    output_props = output_schema.get('properties', {})
    eval_params = set()
    for ev in evals:
        for p in ev.get('evaluationParams', []):
            eval_params.add(p)

    for prop in output_props:
        if prop not in eval_params:
            issues.append(f"output property '{prop}' has no matching eval")

    return issues


def main():
    print("=" * 60)
    print("EVALUATION METRICS CONSISTENCY CHECK")
    print("=" * 60)

    all_valid = True

    for filepath in sorted(DATASETS_DIR.glob("*.json")):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        issues = validate_metrics_consistency(data, filepath.name)

        if issues:
            print(f"\n[ISSUES] {filepath.name}")
            for issue in issues:
                print(f"  - {issue}")
            all_valid = False
        else:
            metadata = data.get('metadata', {})
            print(f"[OK] {filepath.name}: avgScore={metadata.get('averageScore', 0):.2f}, {len(data.get('metatunerPromptInput', {}).get('evals', []))} evals")

    print("\n" + "=" * 60)
    if all_valid:
        print("ALL DATASETS PASSED METRICS VALIDATION")
    else:
        print("SOME DATASETS HAVE ISSUES")
    print("=" * 60)


if __name__ == "__main__":
    main()
