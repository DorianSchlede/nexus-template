#!/usr/bin/env python
"""Verify all prompts are complete and have all variable inputs."""

import json
import re
from pathlib import Path

DATASETS_DIR = Path(__file__).parent.parent / "04-outputs" / "datasets" / "final"


def extract_placeholders(prompt_text):
    """Extract {placeholder} variables from prompt template."""
    # Match {variable_name} patterns
    placeholders = set(re.findall(r'\{(\w+)\}', prompt_text))
    return placeholders


def verify_prompt_completeness(data, filename):
    """Verify prompts have all required inputs."""
    issues = []

    metatuner = data.get('metatunerPromptInput', {})
    prompt_template = metatuner.get('prompt', '')
    input_schema = metatuner.get('inputSchema', {})
    output_schema = metatuner.get('outputSchema', {})

    prompt_dataset = data.get('promptDataset', {})
    items = prompt_dataset.get('items', [])

    # Extract placeholders from prompt
    placeholders = extract_placeholders(prompt_template)

    # Get input schema properties
    input_props = set(input_schema.get('properties', {}).keys())
    required_inputs = set(input_schema.get('required', []))

    # Get output schema properties
    output_props = set(output_schema.get('properties', {}).keys())

    # 1. Check that placeholders match input schema
    missing_in_schema = placeholders - input_props
    extra_in_schema = input_props - placeholders

    if missing_in_schema:
        issues.append(f"Placeholders not in inputSchema: {missing_in_schema}")
    if extra_in_schema:
        # This is OK - schema can have more than placeholders
        pass

    # 2. Check each item has all required inputs
    items_missing_inputs = []
    items_missing_outputs = []

    for i, item in enumerate(items):
        item_input = item.get('input', {})
        item_expected = item.get('expectedOutput', {})
        item_actual = item.get('actualOutput', {})

        # Check required inputs
        missing_required = required_inputs - set(item_input.keys())
        if missing_required:
            items_missing_inputs.append((i, item.get('id', f'item-{i}'), list(missing_required)))

        # Check outputs have all variables
        missing_expected = output_props - set(item_expected.keys())
        if missing_expected and item_expected:  # Only check if expectedOutput exists
            items_missing_outputs.append((i, item.get('id', f'item-{i}'), 'expected', list(missing_expected)))

        missing_actual = output_props - set(item_actual.keys())
        if missing_actual and item_actual:  # Only check if actualOutput exists
            items_missing_outputs.append((i, item.get('id', f'item-{i}'), 'actual', list(missing_actual)))

    if items_missing_inputs:
        if len(items_missing_inputs) <= 3:
            for idx, item_id, missing in items_missing_inputs:
                issues.append(f"Item {idx} ({item_id}) missing required inputs: {missing}")
        else:
            issues.append(f"{len(items_missing_inputs)} items missing required inputs")

    # Note: Missing outputs is informational, not a critical issue
    # Output schema is derived from union of all outputs, so some items may have fewer

    # 3. Check prompt template is not empty
    if not prompt_template or len(prompt_template) < 50:
        issues.append(f"Prompt template too short or empty: {len(prompt_template)} chars")

    # 4. Check for unfilled placeholders in items (evidence of incomplete parsing)
    # Only flag if the pattern looks like a template variable {variable_name}
    # Ignore JSON-like content with escaped braces or data content
    unfilled_count = 0
    for item in items:
        item_input = item.get('input', {})
        for key, value in item_input.items():
            if isinstance(value, str):
                # Look for actual template placeholders like {pdf_content}
                # Exclude JSON-escaped content and data
                template_matches = re.findall(r'(?<![\\"])\{([a-z_]+)\}(?![\\"])', value)
                if template_matches:
                    unfilled_count += 1
                    break

    if unfilled_count > 0:
        issues.append(f"{unfilled_count} items have unfilled placeholders in input values")

    return {
        'placeholders': len(placeholders),
        'input_props': len(input_props),
        'required_inputs': len(required_inputs),
        'output_props': len(output_props),
        'items': len(items),
        'prompt_length': len(prompt_template),
        'issues': issues
    }


def main():
    print("=" * 70)
    print("PROMPT COMPLETENESS VERIFICATION")
    print("=" * 70)

    all_valid = True
    summary = []

    for filepath in sorted(DATASETS_DIR.glob("*.json")):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)

        result = verify_prompt_completeness(data, filepath.name)

        # Get metadata for output
        metadata = data.get('metadata', {})
        output_var_count = metadata.get('outputVariableCount', result['output_props'])

        summary.append({
            'name': filepath.name,
            'items': result['items'],
            'placeholders': result['placeholders'],
            'input_props': result['input_props'],
            'required': result['required_inputs'],
            'outputs': result['output_props'],
            'prompt_length': result['prompt_length'],
            'issues': result['issues']
        })

        if result['issues']:
            print(f"\n[ISSUES] {filepath.name}")
            print(f"  Items: {result['items']}, Placeholders: {result['placeholders']}, Inputs: {result['input_props']}, Outputs: {result['output_props']}")
            for issue in result['issues']:
                print(f"  - {issue}")
            all_valid = False
        else:
            print(f"[OK] {filepath.name}: {result['items']} items, {result['placeholders']} placeholders, {result['input_props']} inputs, {result['output_props']} outputs")

    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Dataset':<40} {'Items':>6} {'In':>4} {'Out':>4} {'Prompt':>8} {'OK':>4}")
    print("-" * 80)

    for s in summary:
        name = s['name'].replace('metatuner-', '').replace('-gold.json', '')
        status = 'Yes' if not s['issues'] else 'No'
        print(f"{name:<40} {s['items']:>6} {s['input_props']:>4} {s['outputs']:>4} {s['prompt_length']:>8} {status:>4}")

    print("-" * 80)
    total_items = sum(s['items'] for s in summary)
    total_outputs = sum(s['outputs'] for s in summary)
    avg_prompt = sum(s['prompt_length'] for s in summary) // len(summary) if summary else 0
    print(f"{'TOTAL/AVG':<40} {total_items:>6} {'':>4} {total_outputs:>4} {avg_prompt:>8}")

    print("\n" + "=" * 70)
    if all_valid:
        print("ALL PROMPTS COMPLETE AND VALID")
    else:
        print("SOME PROMPTS HAVE ISSUES - REVIEW ABOVE")
    print("=" * 70)


if __name__ == "__main__":
    main()
