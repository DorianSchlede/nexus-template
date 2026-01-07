#!/usr/bin/env python3
"""
Hybrid Test Runner: plan-project Router v2.4

Runs both code-based unit tests and prepares subagent test scenarios.

Usage:
    # Run all code-based tests
    python run_tests.py --code

    # List subagent scenarios (for manual execution)
    python run_tests.py --subagent --list

    # Generate subagent test prompts
    python run_tests.py --subagent --generate

    # Run everything
    python run_tests.py --all
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_DIR = SCRIPT_DIR.parent.parent
RESOURCES_DIR = PROJECT_DIR / "02-resources"
SCENARIOS_FILE = RESOURCES_DIR / "validation-scenarios.yaml"
REPORT_DIR = PROJECT_DIR / "03-working"


def run_code_tests(verbose: bool = True) -> Dict[str, Any]:
    """
    Run pytest on test_plan_project.py

    Returns:
        Dict with test results
    """
    print("\n" + "=" * 60)
    print("PHASE 1: CODE-BASED UNIT TESTS")
    print("=" * 60 + "\n")

    test_file = SCRIPT_DIR / "test_plan_project.py"

    if not test_file.exists():
        print(f"ERROR: Test file not found: {test_file}")
        return {"status": "error", "message": "Test file not found"}

    # Run pytest
    cmd = [sys.executable, "-m", "pytest", str(test_file)]
    if verbose:
        cmd.extend(["-v", "--tb=short"])

    print(f"Running: {' '.join(cmd)}\n")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(SCRIPT_DIR)
        )

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:
        print(f"ERROR: {e}")
        return {"status": "error", "message": str(e)}


def parse_scenarios_yaml(file_path: Path) -> Dict[str, Any]:
    """
    Simple YAML parser for scenarios file (no external dependencies)

    Returns:
        Parsed scenarios structure
    """
    if not file_path.exists():
        return {"error": f"File not found: {file_path}"}

    content = file_path.read_text(encoding='utf-8')

    # Extract scenarios section (simple parsing)
    scenarios = []
    current_scenario = None
    in_scenarios = False
    in_prompt = False
    prompt_lines = []
    in_test_inputs = False
    test_inputs = []
    in_pass_criteria = False
    pass_criteria = []

    for line in content.split('\n'):
        stripped = line.strip()

        # Track scenarios section
        if stripped == "scenarios:":
            in_scenarios = True
            continue

        if not in_scenarios:
            continue

        # New scenario starts with "- name:"
        if stripped.startswith("- name:"):
            # Save previous scenario
            if current_scenario:
                if prompt_lines:
                    current_scenario['prompt'] = '\n'.join(prompt_lines)
                if test_inputs:
                    current_scenario['test_inputs'] = test_inputs
                if pass_criteria:
                    current_scenario['pass_criteria'] = pass_criteria
                scenarios.append(current_scenario)

            # Start new scenario
            name = stripped.replace("- name:", "").strip().strip('"\'')
            current_scenario = {"name": name}
            prompt_lines = []
            test_inputs = []
            pass_criteria = []
            in_prompt = False
            in_test_inputs = False
            in_pass_criteria = False
            continue

        if current_scenario is None:
            continue

        # Parse scenario fields
        if stripped.startswith("description:"):
            current_scenario['description'] = stripped.replace("description:", "").strip().strip('"\'')
        elif stripped.startswith("category:"):
            current_scenario['category'] = stripped.replace("category:", "").strip().strip('"\'')
        elif stripped.startswith("runs:"):
            current_scenario['runs'] = int(stripped.replace("runs:", "").strip())
        elif stripped.startswith("mode:"):
            current_scenario['mode'] = stripped.replace("mode:", "").strip().strip('"\'')
        elif stripped.startswith("type:"):
            current_scenario['type'] = stripped.replace("type:", "").strip().strip('"\'')
        elif stripped.startswith("prompt: |"):
            in_prompt = True
            in_test_inputs = False
            in_pass_criteria = False
        elif stripped.startswith("test_inputs:"):
            in_test_inputs = True
            in_prompt = False
            in_pass_criteria = False
        elif stripped.startswith("pass_criteria:"):
            in_pass_criteria = True
            in_prompt = False
            in_test_inputs = False
        elif stripped.startswith("validates:"):
            in_prompt = False
            in_test_inputs = False
            in_pass_criteria = False
        elif in_prompt and line.startswith("      "):
            prompt_lines.append(line[6:])  # Remove leading spaces
        elif in_test_inputs and stripped.startswith("- "):
            test_inputs.append(stripped[2:].strip('"\''))
        elif in_pass_criteria and stripped.startswith("- "):
            pass_criteria.append(stripped[2:].strip('"\''))

    # Save last scenario
    if current_scenario:
        if prompt_lines:
            current_scenario['prompt'] = '\n'.join(prompt_lines)
        if test_inputs:
            current_scenario['test_inputs'] = test_inputs
        if pass_criteria:
            current_scenario['pass_criteria'] = pass_criteria
        scenarios.append(current_scenario)

    return {"scenarios": scenarios, "count": len(scenarios)}


def list_subagent_scenarios():
    """
    List all subagent test scenarios
    """
    print("\n" + "=" * 60)
    print("PHASE 2: SUBAGENT TEST SCENARIOS")
    print("=" * 60 + "\n")

    data = parse_scenarios_yaml(SCENARIOS_FILE)

    if "error" in data:
        print(f"ERROR: {data['error']}")
        return

    scenarios = data.get("scenarios", [])
    print(f"Total scenarios: {len(scenarios)}\n")

    # Group by category
    by_category = {}
    for s in scenarios:
        cat = s.get('category', 'unknown')
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(s)

    for category, items in by_category.items():
        print(f"\n{category.upper()} ({len(items)} scenarios)")
        print("-" * 40)
        for s in items:
            name = s.get('name', 'unnamed')
            desc = s.get('description', '')[:50]
            runs = s.get('runs', 1)
            mode = s.get('mode', 'automated')
            print(f"  {name}")
            print(f"    {desc}...")
            print(f"    Runs: {runs}, Mode: {mode}")


def generate_subagent_prompts(output_dir: Path = None):
    """
    Generate ready-to-use prompts for subagent testing
    """
    print("\n" + "=" * 60)
    print("GENERATING SUBAGENT TEST PROMPTS")
    print("=" * 60 + "\n")

    if output_dir is None:
        output_dir = REPORT_DIR / "subagent-prompts"
    output_dir.mkdir(parents=True, exist_ok=True)

    data = parse_scenarios_yaml(SCENARIOS_FILE)

    if "error" in data:
        print(f"ERROR: {data['error']}")
        return

    scenarios = data.get("scenarios", [])

    for s in scenarios:
        name = s.get('name', 'unnamed')
        prompt = s.get('prompt', '')
        runs = s.get('runs', 1)
        pass_criteria = s.get('pass_criteria', [])
        test_inputs = s.get('test_inputs', [])

        # Generate prompt file
        filename = f"{name}.md"
        filepath = output_dir / filename

        # Generate analysis notes (kept separate from prompt - for validator only)
        content = f"""# Scenario: {name}

## FOR VALIDATOR ONLY (Do not share with subagent)

**Expected Outcome**: {s.get('description', '')}
**Category**: {s.get('category', '')}
**Runs Required**: {runs}
**Mode**: {s.get('mode', 'automated')}

### Pass Criteria (Check after subagent completes)

{chr(10).join(f'- [ ] {c}' for c in pass_criteria)}

### What to Observe

{chr(10).join(f'- {o}' for o in s.get('observe', ['Observe subagent behavior']))}

---

## SUBAGENT PROMPT (Copy this exactly)

```
{prompt}
```

---

## Execution

### Single Run

```python
result = Task(
    prompt=\"\"\"{prompt}\"\"\",
    subagent_type="general-purpose",
    model="sonnet",
    description="{name[:30]}"
)
# Then analyze result against pass_criteria above
```

### Multiple Runs (for determinism/consistency checks)

```python
agents = []
for i in range({runs}):
    r = Task(
        prompt=\"\"\"{prompt}\"\"\",
        subagent_type="general-purpose",
        model="sonnet",
        run_in_background=True,
        description="{name[:30]} run {{i+1}}"
    )
    agents.append(r)

# Wait for completion, then analyze each result
```

### Interactive Mode (if applicable)

{f'''
Interactive answers to provide when subagent asks:
{chr(10).join(f"- When asked about '{a.get('trigger', 'question')}': {a.get('answer', '')}" for a in s.get('interactive_answers', []))}
''' if s.get('interactive_answers') else 'N/A - automated scenario'}

---

*Generated: {datetime.now().isoformat()}*
*REMINDER: The subagent prompt contains NO test-awareness language*
"""

        filepath.write_text(content, encoding='utf-8')
        print(f"Generated: {filepath.name}")

    print(f"\n{len(scenarios)} prompts generated in: {output_dir}")


def generate_report(code_results: Dict[str, Any]) -> str:
    """
    Generate combined test report
    """
    timestamp = datetime.now().isoformat()

    report = f"""# Test Report: plan-project Router v2.4

**Generated**: {timestamp}

---

## Phase 1: Code-Based Tests

**Status**: {code_results.get('status', 'unknown').upper()}
**Return Code**: {code_results.get('returncode', 'N/A')}

### Output

```
{code_results.get('stdout', 'No output')[:3000]}
```

---

## Phase 2: Subagent Tests

**Status**: PENDING (Manual execution required)

See generated prompts in: `03-working/subagent-prompts/`

### Execution Instructions

1. Open a NEW Claude Code session (to avoid context pollution)
2. For each prompt file in `03-working/subagent-prompts/`:
   - Copy the prompt
   - Execute via Task tool or direct input
   - Record results
3. Update this report with subagent results

---

## Summary

| Category | Tests | Status |
|----------|-------|--------|
| Code-based (pytest) | ~50 | {code_results.get('status', 'unknown').upper()} |
| Subagent (property) | 10 | PENDING |
| Subagent (type detection) | 8 | PENDING |
| Subagent (workflow) | 2 | PENDING |
| Subagent (interactive) | 4 | PENDING |

---

*Report generated by run_tests.py*
"""

    return report


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Hybrid Test Runner for plan-project Router",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python run_tests.py --code              # Run pytest unit tests
    python run_tests.py --subagent --list   # List subagent scenarios
    python run_tests.py --subagent --generate  # Generate prompt files
    python run_tests.py --all               # Run code tests + generate prompts
"""
    )

    parser.add_argument('--code', action='store_true',
                        help='Run code-based unit tests (pytest)')
    parser.add_argument('--subagent', action='store_true',
                        help='Work with subagent tests')
    parser.add_argument('--list', action='store_true',
                        help='List scenarios (use with --subagent)')
    parser.add_argument('--generate', action='store_true',
                        help='Generate prompt files (use with --subagent)')
    parser.add_argument('--all', action='store_true',
                        help='Run all tests and generate prompts')
    parser.add_argument('--report', action='store_true',
                        help='Generate combined report')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    # Default to showing help if no args
    if not any([args.code, args.subagent, args.all, args.report]):
        parser.print_help()
        return

    code_results = {}

    # Run code tests
    if args.code or args.all:
        code_results = run_code_tests(verbose=args.verbose)

    # Handle subagent tests
    if args.subagent:
        if args.list:
            list_subagent_scenarios()
        if args.generate:
            generate_subagent_prompts()

    if args.all:
        generate_subagent_prompts()

    # Generate report
    if args.report or args.all:
        report = generate_report(code_results)
        report_path = REPORT_DIR / f"test-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(report, encoding='utf-8')
        print(f"\nReport saved to: {report_path}")


if __name__ == "__main__":
    main()
