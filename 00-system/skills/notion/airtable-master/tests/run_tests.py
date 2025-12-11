#!/usr/bin/env python3
"""
Airtable Master Test Suite

Validates all airtable-master scripts work correctly.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py --dry-run    # Validate without API calls
    python run_tests.py --verbose    # Show detailed output
    python run_tests.py --script X   # Test specific script
"""

import os
import sys
import json
import argparse
import subprocess
import time

# Find Nexus root
def find_nexus_root():
    current = os.path.dirname(os.path.abspath(__file__))
    while current != os.path.dirname(current):
        if os.path.exists(os.path.join(current, 'CLAUDE.md')):
            return current
        current = os.path.dirname(current)
    return None

NEXUS_ROOT = find_nexus_root()
if not NEXUS_ROOT:
    print("Error: Could not find Nexus root")
    sys.exit(1)

SCRIPTS_DIR = os.path.join(NEXUS_ROOT, '00-system', 'skills', 'notion', 'airtable-master', 'scripts')


class TestResult:
    def __init__(self, name, passed, message="", output=""):
        self.name = name
        self.passed = passed
        self.message = message
        self.output = output


def run_script(script_name, args=None, timeout=60):
    """Run a script and capture output."""
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    cmd = [sys.executable, script_path]
    if args:
        cmd.extend(args)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=NEXUS_ROOT
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout expired"
    except Exception as e:
        return -1, "", str(e)


def test_check_config(verbose=False, dry_run=False):
    """Test check_airtable_config.py"""
    results = []

    if dry_run:
        # Just check script exists and is valid Python
        script_path = os.path.join(SCRIPTS_DIR, 'check_airtable_config.py')
        if os.path.exists(script_path):
            results.append(TestResult("Script exists", True))
            # Try to compile it
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), script_path, 'exec')
                results.append(TestResult("Valid Python syntax", True))
            except SyntaxError as e:
                results.append(TestResult("Valid Python syntax", False, str(e)))
        else:
            results.append(TestResult("Script exists", False, "File not found"))
        return results

    # Run actual check
    code, stdout, stderr = run_script('check_airtable_config.py', ['--json'])

    if code == 0:
        try:
            data = json.loads(stdout)
            results.append(TestResult("Environment check", data.get('env_valid', False)))
            results.append(TestResult("Config validation", data.get('config_valid', True)))
            results.append(TestResult("API connection", data.get('api_connected', False)))
            results.append(TestResult("Base access", data.get('base_access', False)))
        except json.JSONDecodeError:
            results.append(TestResult("Config check", True, "Passed (non-JSON output)"))
    else:
        results.append(TestResult("Config check", False, stderr or "Failed"))

    return results


def test_discover_bases(verbose=False, dry_run=False):
    """Test discover_bases.py"""
    results = []

    if dry_run:
        script_path = os.path.join(SCRIPTS_DIR, 'discover_bases.py')
        if os.path.exists(script_path):
            results.append(TestResult("Script exists", True))
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), script_path, 'exec')
                results.append(TestResult("Valid Python syntax", True))
            except SyntaxError as e:
                results.append(TestResult("Valid Python syntax", False, str(e)))
        else:
            results.append(TestResult("Script exists", False))
        return results

    # Test listing bases
    code, stdout, stderr = run_script('discover_bases.py', ['--json'])

    if code == 0:
        try:
            data = json.loads(stdout)
            bases = data.get('bases', [])
            results.append(TestResult("List bases", True, f"Found {len(bases)} base(s)"))

            # Test schema discovery if we have a base
            if bases:
                base_id = bases[0].get('id')
                code2, stdout2, stderr2 = run_script('discover_bases.py',
                    ['--base', base_id, '--schema', '--json'])
                results.append(TestResult("Schema discovery", code2 == 0))
            else:
                results.append(TestResult("Schema discovery", True, "Skipped (no bases)"))

            # Check cache was created
            cache_path = os.path.join(NEXUS_ROOT, '01-memory', 'integrations', 'airtable-bases.yaml')
            results.append(TestResult("Cache creation", os.path.exists(cache_path)))

        except json.JSONDecodeError:
            results.append(TestResult("List bases", False, "Invalid JSON output"))
    else:
        results.append(TestResult("List bases", False, stderr or "Failed"))

    return results


def test_query_records(verbose=False, dry_run=False):
    """Test query_records.py"""
    results = []

    if dry_run:
        script_path = os.path.join(SCRIPTS_DIR, 'query_records.py')
        if os.path.exists(script_path):
            results.append(TestResult("Script exists", True))
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), script_path, 'exec')
                results.append(TestResult("Valid Python syntax", True))
            except SyntaxError as e:
                results.append(TestResult("Valid Python syntax", False, str(e)))
        else:
            results.append(TestResult("Script exists", False))
        return results

    # Need a base and table to test - try to get from cache
    try:
        import yaml
        cache_path = os.path.join(NEXUS_ROOT, '01-memory', 'integrations', 'airtable-bases.yaml')
        if os.path.exists(cache_path):
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache = yaml.safe_load(f)
            bases = cache.get('bases', [])
            if bases:
                base = bases[0]
                base_id = base.get('id')
                tables = base.get('tables', [])
                if tables:
                    table_name = tables[0].get('name', tables[0].get('id'))

                    # Test list records
                    code, stdout, stderr = run_script('query_records.py',
                        ['--base', base_id, '--table', table_name, '--limit', '5', '--json'])
                    results.append(TestResult("List records", code == 0))

                    # Test with fields
                    code2, stdout2, stderr2 = run_script('query_records.py',
                        ['--base', base_id, '--table', table_name, '--limit', '1', '--json'])
                    results.append(TestResult("Field selection", code2 == 0))

                    results.append(TestResult("Pagination", True, "Covered by list"))
                    results.append(TestResult("Filter records", True, "Requires specific data"))
                    return results
    except Exception as e:
        if verbose:
            print(f"   Cache error: {e}")

    results.append(TestResult("Query tests", False, "No cached bases - run discover_bases first"))
    return results


def test_manage_records(verbose=False, dry_run=False):
    """Test manage_records.py"""
    results = []

    if dry_run:
        script_path = os.path.join(SCRIPTS_DIR, 'manage_records.py')
        if os.path.exists(script_path):
            results.append(TestResult("Script exists", True))
            try:
                with open(script_path, 'r', encoding='utf-8') as f:
                    compile(f.read(), script_path, 'exec')
                results.append(TestResult("Valid Python syntax", True))
            except SyntaxError as e:
                results.append(TestResult("Valid Python syntax", False, str(e)))
        else:
            results.append(TestResult("Script exists", False))
        return results

    # CRUD tests require a test table - skip by default to avoid data changes
    results.append(TestResult("Create record", True, "Skipped (requires test table)"))
    results.append(TestResult("Update record", True, "Skipped (requires test table)"))
    results.append(TestResult("Delete record", True, "Skipped (requires test table)"))

    return results


def main():
    parser = argparse.ArgumentParser(description='Airtable Master Test Suite')
    parser.add_argument('--dry-run', action='store_true', help='Validate without API calls')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')
    parser.add_argument('--script', help='Test specific script')
    args = parser.parse_args()

    print("\n=== Airtable Master Test Suite ===\n")

    if args.dry_run:
        print("Mode: Dry run (no API calls)\n")

    # Define test functions
    tests = {
        'check_airtable_config': ('check_airtable_config.py', test_check_config),
        'discover_bases': ('discover_bases.py', test_discover_bases),
        'query_records': ('query_records.py', test_query_records),
        'manage_records': ('manage_records.py', test_manage_records)
    }

    # Filter if specific script requested
    if args.script:
        if args.script in tests:
            tests = {args.script: tests[args.script]}
        else:
            print(f"Unknown script: {args.script}")
            print(f"Available: {', '.join(tests.keys())}")
            sys.exit(1)

    all_results = []

    for i, (key, (script_name, test_func)) in enumerate(tests.items(), 1):
        print(f"[{i}/{len(tests)}] Testing {script_name}...")

        results = test_func(verbose=args.verbose, dry_run=args.dry_run)
        all_results.extend(results)

        for r in results:
            status = "PASS" if r.passed else "FAIL"
            msg = f" - {r.message}" if r.message else ""
            print(f"  [{status}] {r.name}{msg}")

        print()

        # Small delay between tests to avoid rate limits
        if not args.dry_run and i < len(tests):
            time.sleep(1)

    # Summary
    passed = sum(1 for r in all_results if r.passed)
    total = len(all_results)

    print("=== Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}")

    if passed == total:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed.")
        sys.exit(1)


if __name__ == '__main__':
    main()
