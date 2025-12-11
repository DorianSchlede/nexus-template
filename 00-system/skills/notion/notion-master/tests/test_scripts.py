#!/usr/bin/env python3
"""
Script Integration Tests - Tests each Python script's actual functionality

Tests the scripts as they would be called from command line,
verifying correct output parsing, error handling, and edge cases.

Usage:
    python test_scripts.py              # Run all script tests
    python test_scripts.py --verbose    # Verbose output
"""

import sys
import os
import json
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


class ScriptTester:
    """Test each script's functionality"""

    def __init__(self, nexus_root: Path, verbose: bool = False):
        self.nexus_root = nexus_root
        self.scripts_dir = nexus_root / '00-system' / 'skills' / 'notion' / 'notion-master' / 'scripts'
        self.verbose = verbose
        self.results = []

    def _run(self, script: str, args: List[str] = None, timeout: int = 30) -> Tuple[int, str, str]:
        """Run a script and return (exit_code, stdout, stderr)"""
        script_path = self.scripts_dir / script
        cmd = [sys.executable, str(script_path)] + (args or [])

        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8',
                errors='replace'
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout"
        except Exception as e:
            return -2, "", str(e)

    def _log(self, status: str, test_name: str, details: str = ""):
        """Log test result"""
        color = Colors.GREEN if status == "PASS" else Colors.RED if status == "FAIL" else Colors.YELLOW
        print(f"  [{color}{status}{Colors.END}] {test_name}")
        if self.verbose and details:
            print(f"       {Colors.BLUE}{details}{Colors.END}")
        self.results.append({"status": status, "name": test_name, "details": details})

    # ========== CHECK_NOTION_CONFIG.PY ==========
    def test_check_notion_config(self):
        """Test check_notion_config.py script"""
        print(f"\n{Colors.BOLD}[check_notion_config.py]{Colors.END}")

        # Test 1: Script runs and returns valid exit code
        code, stdout, stderr = self._run('check_notion_config.py')
        if code in [0, 1, 2]:
            self._log("PASS", "Returns valid exit code", f"Exit code: {code}")
        else:
            self._log("FAIL", "Returns valid exit code", f"Got: {code}")

        # Test 2: Output contains expected sections
        output = stdout + stderr
        has_env_check = '[1/3]' in output or '.env' in output.lower()
        has_user_check = '[2/3]' in output or 'user-config' in output.lower()
        has_api_check = '[3/3]' in output or 'API' in output

        if has_env_check and has_user_check and has_api_check:
            self._log("PASS", "Contains all 3 check sections")
        else:
            self._log("FAIL", "Missing check sections", f"env:{has_env_check} user:{has_user_check} api:{has_api_check}")

        # Test 3: Output is parseable
        if 'CONFIGURATION' in output or 'PASS' in output or 'configured' in output.lower():
            self._log("PASS", "Output contains status information")
        else:
            self._log("WARN", "Output format may have changed")

    # ========== DISCOVER_DATABASES.PY ==========
    def test_discover_databases(self):
        """Test discover_databases.py script"""
        print(f"\n{Colors.BOLD}[discover_databases.py]{Colors.END}")

        # Test 1: Script with no args (should check for existing context)
        code, stdout, stderr = self._run('discover_databases.py')
        output = stdout + stderr

        if code == 0:
            self._log("PASS", "Runs successfully")
        else:
            self._log("FAIL", "Script failed", f"Exit: {code}")
            return

        # Test 2: Detects existing context file
        if 'Context file exists' in output or 'database' in output.lower():
            self._log("PASS", "Handles existing context")
        else:
            self._log("WARN", "Could not detect context handling")

        # Test 3: --refresh flag works
        code, stdout, stderr = self._run('discover_databases.py', ['--refresh'], timeout=60)
        output = stdout + stderr

        if code == 0 and ('Successfully' in output or 'database' in output.lower()):
            self._log("PASS", "--refresh flag works")
        else:
            self._log("FAIL", "--refresh flag failed", f"Exit: {code}")

    # ========== SEARCH_SKILL_DATABASE.PY ==========
    def test_search_skill_database(self):
        """Test search_skill_database.py script"""
        print(f"\n{Colors.BOLD}[search_skill_database.py]{Colors.END}")

        # Test 1: --skills mode basic query
        code, stdout, stderr = self._run('search_skill_database.py', ['--skills', '--limit', '2'])
        output = stdout + stderr

        if code == 0 and ('[RESULTS]' in output or 'Found' in output):
            self._log("PASS", "--skills basic query")
        else:
            self._log("FAIL", "--skills basic query", f"Exit: {code}")

        # Test 2: --skills with team filter
        code, stdout, stderr = self._run('search_skill_database.py', ['--skills', '--team', 'General', '--limit', '2'])
        output = stdout + stderr

        if code == 0:
            self._log("PASS", "--team filter")
        else:
            self._log("FAIL", "--team filter", f"Exit: {code}")

        # Test 3: --skills with multiple filters (AND)
        code, stdout, stderr = self._run('search_skill_database.py',
            ['--skills', '--team', 'General', '--integration', 'Notion', '--limit', '3'])
        output = stdout + stderr

        if code == 0 and 'and' in output.lower():
            self._log("PASS", "AND filter (--team + --integration)")
        else:
            self._log("WARN", "AND filter may not be showing in output")

        # Test 4: --skills with name search
        code, stdout, stderr = self._run('search_skill_database.py', ['--skills', '--name', 'notion', '--limit', '5'])
        output = stdout + stderr

        if code == 0:
            self._log("PASS", "--name partial match filter")
        else:
            self._log("FAIL", "--name filter", f"Exit: {code}")

        # Test 5: --format json output
        code, stdout, stderr = self._run('search_skill_database.py', ['--skills', '--limit', '1', '--format', 'json'])
        output = stdout + stderr

        try:
            # Try to find and parse JSON in output
            if '[' in stdout:
                json_start = stdout.index('[')
                json_str = stdout[json_start:]
                json.loads(json_str)
                self._log("PASS", "--format json output")
            else:
                self._log("WARN", "JSON output not detected")
        except json.JSONDecodeError:
            self._log("FAIL", "--format json output", "Invalid JSON")

        # Test 6: Error handling for invalid filter
        code, stdout, stderr = self._run('search_skill_database.py', ['--skills', '--team', 'InvalidTeamXYZ'])
        # Should still exit 0 but return empty results
        if code == 0:
            self._log("PASS", "Handles invalid filter gracefully")
        else:
            self._log("WARN", "Invalid filter handling", f"Exit: {code}")

    # ========== CREATE_PAGE.PY ==========
    def test_create_page(self):
        """Test create_page.py script"""
        print(f"\n{Colors.BOLD}[create_page.py]{Colors.END}")

        # Test 1: --help works
        code, stdout, stderr = self._run('create_page.py', ['--help'])
        output = stdout + stderr

        if code == 0 and '--db' in output:
            self._log("PASS", "--help output")
        else:
            self._log("FAIL", "--help output", f"Exit: {code}")

        # Test 2: Error on missing required args
        code, stdout, stderr = self._run('create_page.py', [])
        if code != 0:
            self._log("PASS", "Requires --db argument")
        else:
            self._log("FAIL", "Should require --db")

        # Note: Not testing actual page creation to avoid creating garbage data

    # ========== MANAGE_PAGE.PY ==========
    def test_manage_page(self):
        """Test manage_page.py script"""
        print(f"\n{Colors.BOLD}[manage_page.py]{Colors.END}")

        # Test 1: --help works
        code, stdout, stderr = self._run('manage_page.py', ['--help'])
        output = stdout + stderr

        if code == 0 and ('get' in output or 'update' in output or 'delete' in output):
            self._log("PASS", "--help shows subcommands")
        else:
            self._log("FAIL", "--help output", f"Exit: {code}")

        # Test 2: Error on invalid page ID
        code, stdout, stderr = self._run('manage_page.py', ['get', '--page', 'invalid-page-id'])
        output = stdout + stderr

        if code != 0 or 'error' in output.lower() or 'invalid' in output.lower():
            self._log("PASS", "Handles invalid page ID")
        else:
            self._log("WARN", "Invalid page ID handling uncertain")

    # ========== MANAGE_BLOCKS.PY ==========
    def test_manage_blocks(self):
        """Test manage_blocks.py script"""
        print(f"\n{Colors.BOLD}[manage_blocks.py]{Colors.END}")

        # Test 1: --help works
        code, stdout, stderr = self._run('manage_blocks.py', ['--help'])
        output = stdout + stderr

        if code == 0 and ('children' in output or 'append' in output):
            self._log("PASS", "--help shows subcommands")
        else:
            self._log("FAIL", "--help output", f"Exit: {code}")

    # ========== MANAGE_USERS.PY ==========
    def test_manage_users(self):
        """Test manage_users.py script"""
        print(f"\n{Colors.BOLD}[manage_users.py]{Colors.END}")

        # Test 1: 'me' subcommand
        code, stdout, stderr = self._run('manage_users.py', ['me'])
        output = stdout + stderr

        if code == 0 and ('Bot' in output or 'name' in output.lower() or 'id' in output.lower()):
            self._log("PASS", "'me' shows bot info")
        else:
            self._log("FAIL", "'me' subcommand", f"Exit: {code}")

        # Test 2: 'list' subcommand
        code, stdout, stderr = self._run('manage_users.py', ['list', '--limit', '5'])
        output = stdout + stderr

        if code == 0 and ('user' in output.lower() or 'person' in output.lower()):
            self._log("PASS", "'list' shows users")
        else:
            self._log("WARN", "'list' subcommand output unclear")

    # ========== MANAGE_COMMENTS.PY ==========
    def test_manage_comments(self):
        """Test manage_comments.py script"""
        print(f"\n{Colors.BOLD}[manage_comments.py]{Colors.END}")

        # Test 1: --help works
        code, stdout, stderr = self._run('manage_comments.py', ['--help'])
        output = stdout + stderr

        if code == 0 and ('list' in output or 'create' in output):
            self._log("PASS", "--help shows subcommands")
        else:
            self._log("FAIL", "--help output", f"Exit: {code}")

    # ========== MANAGE_DATABASE.PY ==========
    def test_manage_database(self):
        """Test manage_database.py script"""
        print(f"\n{Colors.BOLD}[manage_database.py]{Colors.END}")

        # Test 1: --help works
        code, stdout, stderr = self._run('manage_database.py', ['--help'])
        output = stdout + stderr

        if code == 0 and ('create' in output or 'update' in output):
            self._log("PASS", "--help shows subcommands")
        else:
            self._log("FAIL", "--help output", f"Exit: {code}")

    # ========== UPLOAD_SKILL.PY ==========
    def test_upload_skill(self):
        """Test upload_skill.py script"""
        print(f"\n{Colors.BOLD}[upload_skill.py]{Colors.END}")

        # Test skill path
        skill_path = self.nexus_root / '00-system' / 'skills' / 'notion-connect'

        # Test 1: --dry-run mode
        code, stdout, stderr = self._run('upload_skill.py',
            [str(skill_path), '--team', 'General', '--dry-run'])
        output = stdout + stderr

        if code == 0 and ('DRY-RUN' in output or 'dry_run' in output):
            self._log("PASS", "--dry-run mode works")
        else:
            self._log("FAIL", "--dry-run mode", f"Exit: {code}, Output: {output[:100]}")

        # Test 2: Validates SKILL.md
        if 'valid' in output.lower() or 'SKILL.md' in output:
            self._log("PASS", "Validates SKILL.md")
        else:
            self._log("WARN", "SKILL.md validation uncertain")

        # Test 3: Creates JSON bundle
        if 'bundle' in output.lower() or 'json' in output.lower():
            self._log("PASS", "Creates JSON bundle")
        else:
            self._log("WARN", "JSON bundle creation uncertain")

        # Test 4: Shows preview
        if 'PREVIEW' in output or 'Skill Name' in output:
            self._log("PASS", "Shows upload preview")
        else:
            self._log("WARN", "Preview output uncertain")

    # ========== DOWNLOAD_SKILL.PY ==========
    def test_download_skill(self):
        """Test download_skill.py script"""
        print(f"\n{Colors.BOLD}[download_skill.py]{Colors.END}")

        # Test 1: --help works
        code, stdout, stderr = self._run('download_skill.py', ['--help'])
        output = stdout + stderr

        if code == 0 and ('page_id' in output.lower() or 'output' in output.lower()):
            self._log("PASS", "--help shows usage")
        else:
            self._log("FAIL", "--help output", f"Exit: {code}")

        # Test 2: Error on missing page ID
        code, stdout, stderr = self._run('download_skill.py', [])
        if code != 0:
            self._log("PASS", "Requires page_id argument")
        else:
            self._log("FAIL", "Should require page_id")

        # Test 3: Error on invalid page ID
        code, stdout, stderr = self._run('download_skill.py', ['invalid-page-id-xyz'])
        output = stdout + stderr
        if code != 0 or 'error' in output.lower():
            self._log("PASS", "Handles invalid page ID")
        else:
            self._log("WARN", "Invalid page ID handling uncertain")

    # ========== SETUP_NOTION.PY ==========
    def test_setup_notion(self):
        """Test setup_notion.py script (non-interactive checks only)"""
        print(f"\n{Colors.BOLD}[setup_notion.py]{Colors.END}")

        # We can't test the interactive wizard, but we can check it exists and imports
        script_path = self.scripts_dir / 'setup_notion.py'

        if script_path.exists():
            self._log("PASS", "Script exists")
        else:
            self._log("FAIL", "Script not found")

        # Check it's importable (has valid Python syntax)
        try:
            import ast
            with open(script_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
            self._log("PASS", "Valid Python syntax")
        except SyntaxError as e:
            self._log("FAIL", "Syntax error", str(e))

    # ========== RATE_LIMITER.PY ==========
    def test_rate_limiter(self):
        """Test rate_limiter.py module"""
        print(f"\n{Colors.BOLD}[rate_limiter.py]{Colors.END}")

        # Test import
        try:
            sys.path.insert(0, str(self.scripts_dir))
            import rate_limiter

            if hasattr(rate_limiter, 'RateLimiter') or hasattr(rate_limiter, 'rate_limited_request'):
                self._log("PASS", "Module importable with expected exports")
            else:
                self._log("WARN", "Module importable but exports differ")

            # Test RateLimiter class if exists
            if hasattr(rate_limiter, 'RateLimiter'):
                limiter = rate_limiter.RateLimiter()
                self._log("PASS", "RateLimiter instantiable")
        except ImportError as e:
            self._log("FAIL", "Import failed", str(e))
        except Exception as e:
            self._log("WARN", "Unexpected error", str(e))

    # ========== RUN ALL ==========
    def run_all(self):
        """Run all script tests"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}  NOTION SCRIPT INTEGRATION TESTS{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")

        self.test_check_notion_config()
        self.test_discover_databases()
        self.test_search_skill_database()
        self.test_create_page()
        self.test_manage_page()
        self.test_manage_blocks()
        self.test_manage_users()
        self.test_manage_comments()
        self.test_manage_database()
        self.test_upload_skill()
        self.test_download_skill()
        self.test_setup_notion()
        self.test_rate_limiter()

        self._print_summary()

    def _print_summary(self):
        """Print test summary"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")

        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        warned = sum(1 for r in self.results if r['status'] == 'WARN')
        total = len(self.results)

        print(f"\n  {Colors.BOLD}SUMMARY{Colors.END}")
        print(f"  {Colors.GREEN}Passed:  {passed}{Colors.END}")
        if failed > 0:
            print(f"  {Colors.RED}Failed:  {failed}{Colors.END}")
        if warned > 0:
            print(f"  {Colors.YELLOW}Warned:  {warned}{Colors.END}")
        print(f"  Total:   {total}")

        if failed == 0:
            print(f"\n{Colors.GREEN}  [OK] All script tests passed!{Colors.END}")
        else:
            print(f"\n{Colors.RED}  [FAIL] Some script tests failed{Colors.END}")

        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}\n")

        return failed == 0


def find_nexus_root() -> Path:
    """Find Nexus root directory"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Notion Script Integration Tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    args = parser.parse_args()

    nexus_root = find_nexus_root()
    tester = ScriptTester(nexus_root, verbose=args.verbose)

    try:
        success = tester.run_all()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()
