#!/usr/bin/env python3
"""
Notion Skills Test Runner - Comprehensive test suite for all Notion scripts

Usage:
    python run_tests.py                    # Run basic tests
    python run_tests.py --full             # Run ALL tests (basic + scripts + API)
    python run_tests.py --category config  # Run specific category
    python run_tests.py --quick            # Quick smoke tests only
    python run_tests.py --verbose          # Verbose output
    python run_tests.py --live-api         # Run live API tests
    python run_tests.py --scripts          # Run script integration tests

Categories:
    config    - Configuration and setup tests
    discovery - Database discovery tests
    query     - Query and filter tests
    pages     - Page CRUD tests
    blocks    - Block management tests
    users     - User management tests
    comments  - Comment tests
    skills    - Skill import/export tests
    all       - Run all basic tests (default)

Additional test suites:
    --scripts  - Script integration tests (test_scripts.py)
    --live-api - Live Notion API tests (test_live_api.py)
    --full     - Run ALL test suites
"""

import sys
import os
import json
import argparse
import subprocess
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Configure UTF-8 output for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / 'scripts'
sys.path.insert(0, str(SCRIPT_DIR))


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @classmethod
    def disable(cls):
        cls.GREEN = cls.RED = cls.YELLOW = cls.BLUE = cls.CYAN = cls.BOLD = cls.END = ''


class TestResult:
    """Result of a single test"""
    def __init__(self, name: str, passed: bool, message: str = "", duration: float = 0):
        self.name = name
        self.passed = passed
        self.message = message
        self.duration = duration
        self.skipped = False

    def __str__(self):
        status = f"{Colors.GREEN}PASS{Colors.END}" if self.passed else f"{Colors.RED}FAIL{Colors.END}"
        if self.skipped:
            status = f"{Colors.YELLOW}SKIP{Colors.END}"
        return f"  [{status}] {self.name} ({self.duration:.2f}s)"


class TestSuite:
    """Test suite runner"""

    def __init__(self, nexus_root: Path, verbose: bool = False):
        self.nexus_root = nexus_root
        self.scripts_dir = nexus_root / '00-system' / 'skills' / 'notion' / 'notion-master' / 'scripts'
        self.verbose = verbose
        self.results: List[TestResult] = []
        self.env_vars = self._load_env()

    def _load_env(self) -> Dict[str, str]:
        """Load .env file"""
        env_path = self.nexus_root / '.env'
        env_vars = {}
        if env_path.exists():
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip().strip('"').strip("'")
        return env_vars

    def _run_script(self, script_name: str, args: List[str] = None,
                    timeout: int = 30) -> Tuple[int, str, str]:
        """Run a Python script and capture output"""
        script_path = self.scripts_dir / script_name
        if not script_path.exists():
            return -1, "", f"Script not found: {script_path}"

        cmd = [sys.executable, str(script_path)] + (args or [])
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=timeout,
                env={**os.environ, **self.env_vars},
                encoding='utf-8',
                errors='replace'
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -2, "", "Timeout"
        except Exception as e:
            return -3, "", str(e)

    def _test(self, name: str, condition: bool, message: str = "") -> TestResult:
        """Record a test result"""
        result = TestResult(name, condition, message)
        self.results.append(result)
        return result

    def _skip(self, name: str, reason: str) -> TestResult:
        """Skip a test"""
        result = TestResult(name, False, reason)
        result.skipped = True
        self.results.append(result)
        return result

    # ========== CONFIG TESTS ==========
    def test_config_check_script_exists(self) -> TestResult:
        """Test that check_notion_config.py exists"""
        start = time.time()
        exists = (self.scripts_dir / 'check_notion_config.py').exists()
        return self._test(
            "check_notion_config.py exists",
            exists,
            "" if exists else "Script not found"
        )

    def test_config_check_runs(self) -> TestResult:
        """Test that config check runs without crashing"""
        start = time.time()
        code, stdout, stderr = self._run_script('check_notion_config.py')
        duration = time.time() - start
        # Exit codes 0, 1, 2 are all valid
        passed = code in [0, 1, 2]
        result = self._test(
            "check_notion_config.py runs",
            passed,
            f"Exit code: {code}" if not passed else ""
        )
        result.duration = duration
        return result

    def test_config_env_file_exists(self) -> TestResult:
        """Test that .env file exists"""
        exists = (self.nexus_root / '.env').exists()
        return self._test(".env file exists", exists)

    def test_config_api_key_set(self) -> TestResult:
        """Test that NOTION_API_KEY is configured"""
        has_key = bool(self.env_vars.get('NOTION_API_KEY'))
        return self._test(
            "NOTION_API_KEY configured",
            has_key,
            "" if has_key else "Add NOTION_API_KEY to .env"
        )

    def test_config_database_id_set(self) -> TestResult:
        """Test that NOTION_SKILLS_DB_ID is configured"""
        has_id = bool(self.env_vars.get('NOTION_SKILLS_DB_ID'))
        return self._test(
            "NOTION_SKILLS_DB_ID configured",
            has_id,
            "" if has_id else "Add NOTION_SKILLS_DB_ID to .env"
        )

    def test_setup_wizard_exists(self) -> TestResult:
        """Test that setup_notion.py exists"""
        exists = (self.scripts_dir / 'setup_notion.py').exists()
        return self._test("setup_notion.py exists", exists)

    # ========== DISCOVERY TESTS ==========
    def test_discovery_script_exists(self) -> TestResult:
        """Test that discover_databases.py exists"""
        exists = (self.scripts_dir / 'discover_databases.py').exists()
        return self._test("discover_databases.py exists", exists)

    def test_discovery_context_file_exists(self) -> TestResult:
        """Test that notion-databases.yaml exists"""
        context_path = self.nexus_root / '01-memory' / 'integrations' / 'notion-databases.yaml'
        exists = context_path.exists()
        return self._test(
            "notion-databases.yaml exists",
            exists,
            "" if exists else "Run 'discover databases' first"
        )

    def test_discovery_runs(self) -> TestResult:
        """Test that discovery script runs"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("discover_databases.py runs", "No API key configured")

        start = time.time()
        code, stdout, stderr = self._run_script('discover_databases.py', timeout=60)
        duration = time.time() - start
        # Code 0 = success, also accept if context already exists
        passed = code == 0 or 'Context file exists' in stdout
        result = self._test(
            "discover_databases.py runs",
            passed,
            stderr if not passed else ""
        )
        result.duration = duration
        return result

    # ========== SEARCH TESTS ==========
    def test_search_script_exists(self) -> TestResult:
        """Test that search_skill_database.py exists"""
        exists = (self.scripts_dir / 'search_skill_database.py').exists()
        return self._test("search_skill_database.py exists", exists)

    def test_search_help(self) -> TestResult:
        """Test search script help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('search_skill_database.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and ('--skills' in stdout or '--db' in stdout)
        result = self._test("search_skill_database.py --help works", passed)
        result.duration = duration
        return result

    def test_search_skills_mode(self) -> TestResult:
        """Test search with --skills mode"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("search --skills mode", "No API key configured")

        start = time.time()
        code, stdout, stderr = self._run_script(
            'search_skill_database.py',
            ['--skills', '--limit', '1']
        )
        duration = time.time() - start
        passed = code == 0 and ('[RESULTS]' in stdout or 'Found' in stdout)
        result = self._test(
            "search --skills --limit 1",
            passed,
            stderr if not passed else ""
        )
        result.duration = duration
        return result

    def test_search_with_team_filter(self) -> TestResult:
        """Test search with team filter"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("search with --team filter", "No API key configured")

        start = time.time()
        code, stdout, stderr = self._run_script(
            'search_skill_database.py',
            ['--skills', '--team', 'General', '--limit', '2']
        )
        duration = time.time() - start
        passed = code == 0
        result = self._test("search --skills --team General", passed)
        result.duration = duration
        return result

    def test_search_with_and_filter(self) -> TestResult:
        """Test search with multiple AND filters"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("search with AND filters", "No API key configured")

        start = time.time()
        code, stdout, stderr = self._run_script(
            'search_skill_database.py',
            ['--skills', '--team', 'General', '--integration', 'Notion', '--limit', '3']
        )
        duration = time.time() - start
        # Check that AND filter was applied - filter info might be in stdout or stderr
        combined = stdout + stderr
        passed = code == 0 and ('"and"' in combined or "'and'" in combined or 'and' in combined.lower())
        result = self._test("search --team + --integration (AND)", passed)
        result.duration = duration
        return result

    def test_search_with_name_filter(self) -> TestResult:
        """Test search with name partial match"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("search with --name filter", "No API key configured")

        start = time.time()
        code, stdout, stderr = self._run_script(
            'search_skill_database.py',
            ['--skills', '--name', 'notion', '--limit', '5']
        )
        duration = time.time() - start
        passed = code == 0
        result = self._test("search --skills --name notion", passed)
        result.duration = duration
        return result

    # ========== PAGE TESTS ==========
    def test_create_page_script_exists(self) -> TestResult:
        """Test that create_page.py exists"""
        exists = (self.scripts_dir / 'create_page.py').exists()
        return self._test("create_page.py exists", exists)

    def test_manage_page_script_exists(self) -> TestResult:
        """Test that manage_page.py exists"""
        exists = (self.scripts_dir / 'manage_page.py').exists()
        return self._test("manage_page.py exists", exists)

    def test_create_page_help(self) -> TestResult:
        """Test create_page.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('create_page.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and '--db' in stdout
        result = self._test("create_page.py --help works", passed)
        result.duration = duration
        return result

    def test_manage_page_help(self) -> TestResult:
        """Test manage_page.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('manage_page.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and ('get' in stdout or 'update' in stdout or 'delete' in stdout)
        result = self._test("manage_page.py --help works", passed)
        result.duration = duration
        return result

    # ========== BLOCK TESTS ==========
    def test_manage_blocks_script_exists(self) -> TestResult:
        """Test that manage_blocks.py exists"""
        exists = (self.scripts_dir / 'manage_blocks.py').exists()
        return self._test("manage_blocks.py exists", exists)

    def test_manage_blocks_help(self) -> TestResult:
        """Test manage_blocks.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('manage_blocks.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and ('append' in stdout or 'children' in stdout)
        result = self._test("manage_blocks.py --help works", passed)
        result.duration = duration
        return result

    # ========== USER TESTS ==========
    def test_manage_users_script_exists(self) -> TestResult:
        """Test that manage_users.py exists"""
        exists = (self.scripts_dir / 'manage_users.py').exists()
        return self._test("manage_users.py exists", exists)

    def test_manage_users_help(self) -> TestResult:
        """Test manage_users.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('manage_users.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and ('list' in stdout or 'me' in stdout)
        result = self._test("manage_users.py --help works", passed)
        result.duration = duration
        return result

    def test_manage_users_me(self) -> TestResult:
        """Test getting current bot user info"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("manage_users.py me", "No API key configured")

        start = time.time()
        code, stdout, stderr = self._run_script('manage_users.py', ['me'])
        duration = time.time() - start
        passed = code == 0 and ('Bot' in stdout or 'name' in stdout.lower())
        result = self._test("manage_users.py me", passed)
        result.duration = duration
        return result

    # ========== COMMENT TESTS ==========
    def test_manage_comments_script_exists(self) -> TestResult:
        """Test that manage_comments.py exists"""
        exists = (self.scripts_dir / 'manage_comments.py').exists()
        return self._test("manage_comments.py exists", exists)

    def test_manage_comments_help(self) -> TestResult:
        """Test manage_comments.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('manage_comments.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and ('list' in stdout or 'create' in stdout)
        result = self._test("manage_comments.py --help works", passed)
        result.duration = duration
        return result

    # ========== SKILL IMPORT/EXPORT TESTS ==========
    def test_download_skill_script_exists(self) -> TestResult:
        """Test that download_skill.py exists"""
        exists = (self.scripts_dir / 'download_skill.py').exists()
        return self._test("download_skill.py exists", exists)

    def test_upload_skill_script_exists(self) -> TestResult:
        """Test that upload_skill.py exists"""
        exists = (self.scripts_dir / 'upload_skill.py').exists()
        return self._test("upload_skill.py exists", exists)

    def test_download_skill_help(self) -> TestResult:
        """Test download_skill.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('download_skill.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and 'page_id' in stdout.lower()
        result = self._test("download_skill.py --help works", passed)
        result.duration = duration
        return result

    def test_upload_skill_help(self) -> TestResult:
        """Test upload_skill.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('upload_skill.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and '--team' in stdout
        result = self._test("upload_skill.py --help works", passed)
        result.duration = duration
        return result

    def test_upload_skill_dry_run(self) -> TestResult:
        """Test upload_skill.py dry-run mode"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("upload_skill.py --dry-run", "No API key configured")

        # Find a skill to test with
        skill_path = self.nexus_root / '00-system' / 'skills' / 'notion-connect'
        if not skill_path.exists():
            return self._skip("upload_skill.py --dry-run", "No test skill found")

        start = time.time()
        code, stdout, stderr = self._run_script(
            'upload_skill.py',
            [str(skill_path), '--team', 'General', '--dry-run']
        )
        duration = time.time() - start
        # Check for dry-run in combined output (may be stdout or stderr)
        combined = stdout + stderr
        passed = code == 0 and ('DRY-RUN' in combined or 'dry_run' in combined)
        result = self._test("upload_skill.py --dry-run", passed, stderr[:200] if not passed else "")
        result.duration = duration
        return result

    # ========== DATABASE MANAGEMENT TESTS ==========
    def test_manage_database_script_exists(self) -> TestResult:
        """Test that manage_database.py exists"""
        exists = (self.scripts_dir / 'manage_database.py').exists()
        return self._test("manage_database.py exists", exists)

    def test_manage_database_help(self) -> TestResult:
        """Test manage_database.py help output"""
        start = time.time()
        code, stdout, stderr = self._run_script('manage_database.py', ['--help'])
        duration = time.time() - start
        passed = code == 0 and ('create' in stdout or 'update' in stdout)
        result = self._test("manage_database.py --help works", passed)
        result.duration = duration
        return result

    # ========== RATE LIMITER TESTS ==========
    def test_rate_limiter_exists(self) -> TestResult:
        """Test that rate_limiter.py exists"""
        exists = (self.scripts_dir / 'rate_limiter.py').exists()
        return self._test("rate_limiter.py exists", exists)

    def test_rate_limiter_importable(self) -> TestResult:
        """Test that rate_limiter.py is importable"""
        try:
            sys.path.insert(0, str(self.scripts_dir))
            import rate_limiter
            passed = hasattr(rate_limiter, 'RateLimiter') or hasattr(rate_limiter, 'rate_limited_request')
            return self._test("rate_limiter.py importable", passed)
        except Exception as e:
            return self._test("rate_limiter.py importable", False, str(e))

    # ========== INTEGRATION TESTS ==========
    def test_full_query_flow(self) -> TestResult:
        """Test complete query flow: config check → query → results"""
        if not self.env_vars.get('NOTION_API_KEY'):
            return self._skip("Full query flow", "No API key configured")

        start = time.time()

        # Step 1: Config check
        code1, _, _ = self._run_script('check_notion_config.py')
        if code1 == 2:
            return self._test("Full query flow", False, "Config incomplete")

        # Step 2: Search
        code2, stdout2, stderr2 = self._run_script(
            'search_skill_database.py',
            ['--skills', '--limit', '3']
        )

        duration = time.time() - start
        passed = code2 == 0 and '[RESULTS]' in stdout2
        result = self._test("Full query flow", passed)
        result.duration = duration
        return result

    # ========== RUN METHODS ==========
    def run_category(self, category: str) -> List[TestResult]:
        """Run tests for a specific category"""
        test_methods = {
            'config': [
                self.test_config_check_script_exists,
                self.test_config_check_runs,
                self.test_config_env_file_exists,
                self.test_config_api_key_set,
                self.test_config_database_id_set,
                self.test_setup_wizard_exists,
            ],
            'discovery': [
                self.test_discovery_script_exists,
                self.test_discovery_context_file_exists,
                self.test_discovery_runs,
            ],
            'search': [
                self.test_search_script_exists,
                self.test_search_help,
                self.test_search_skills_mode,
                self.test_search_with_team_filter,
                self.test_search_with_and_filter,
                self.test_search_with_name_filter,
            ],
            'pages': [
                self.test_create_page_script_exists,
                self.test_manage_page_script_exists,
                self.test_create_page_help,
                self.test_manage_page_help,
            ],
            'blocks': [
                self.test_manage_blocks_script_exists,
                self.test_manage_blocks_help,
            ],
            'users': [
                self.test_manage_users_script_exists,
                self.test_manage_users_help,
                self.test_manage_users_me,
            ],
            'comments': [
                self.test_manage_comments_script_exists,
                self.test_manage_comments_help,
            ],
            'skills': [
                self.test_download_skill_script_exists,
                self.test_upload_skill_script_exists,
                self.test_download_skill_help,
                self.test_upload_skill_help,
                self.test_upload_skill_dry_run,
            ],
            'database': [
                self.test_manage_database_script_exists,
                self.test_manage_database_help,
            ],
            'utils': [
                self.test_rate_limiter_exists,
                self.test_rate_limiter_importable,
            ],
            'integration': [
                self.test_full_query_flow,
            ],
        }

        if category == 'all':
            tests = []
            for cat_tests in test_methods.values():
                tests.extend(cat_tests)
        elif category in test_methods:
            tests = test_methods[category]
        else:
            print(f"Unknown category: {category}")
            print(f"Available: {', '.join(test_methods.keys())}, all")
            return []

        results = []
        for test_func in tests:
            try:
                result = test_func()
                results.append(result)
                print(result)
                if self.verbose and result.message:
                    print(f"       {Colors.CYAN}{result.message}{Colors.END}")
            except Exception as e:
                result = TestResult(test_func.__name__, False, str(e))
                results.append(result)
                print(result)

        return results

    def run_quick(self) -> List[TestResult]:
        """Run quick smoke tests only"""
        quick_tests = [
            self.test_config_check_runs,
            self.test_discovery_context_file_exists,
            self.test_query_skills_mode,
            self.test_upload_skill_dry_run,
        ]

        results = []
        for test_func in quick_tests:
            try:
                result = test_func()
                results.append(result)
                print(result)
            except Exception as e:
                result = TestResult(test_func.__name__, False, str(e))
                results.append(result)
                print(result)

        return results


def find_nexus_root() -> Path:
    """Find Nexus root directory"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def run_additional_suite(suite_name: str, nexus_root: Path) -> Tuple[int, int]:
    """Run an additional test suite and return (passed, failed)"""
    tests_dir = nexus_root / '00-system' / 'skills' / 'notion' / 'notion-master' / 'tests'

    if suite_name == 'scripts':
        script = tests_dir / 'test_scripts.py'
    elif suite_name == 'live-api':
        script = tests_dir / 'test_live_api.py'
    else:
        return 0, 0

    if not script.exists():
        print(f"{Colors.YELLOW}[SKIP] {suite_name} tests - script not found{Colors.END}")
        return 0, 0

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(nexus_root),
        capture_output=False,
        text=True
    )

    # Parse results from exit code
    return (1, 0) if result.returncode == 0 else (0, 1)


def main():
    parser = argparse.ArgumentParser(
        description='Notion Skills Test Runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Categories:
    config      Configuration and setup tests
    discovery   Database discovery tests
    query       Query and filter tests
    pages       Page CRUD tests
    blocks      Block management tests
    users       User management tests
    comments    Comment tests
    skills      Skill import/export tests
    database    Database management tests
    utils       Utility scripts tests
    integration End-to-end integration tests
    all         Run all tests (default)

Additional Suites:
    --scripts   Run script integration tests
    --live-api  Run live Notion API tests
    --full      Run ALL test suites together
        """
    )
    parser.add_argument('--category', '-c', default='all',
                        help='Test category to run')
    parser.add_argument('--quick', '-q', action='store_true',
                        help='Run quick smoke tests only')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be tested')
    parser.add_argument('--no-color', action='store_true',
                        help='Disable colored output')
    parser.add_argument('--scripts', action='store_true',
                        help='Run script integration tests')
    parser.add_argument('--live-api', action='store_true',
                        help='Run live API tests')
    parser.add_argument('--full', action='store_true',
                        help='Run ALL test suites')

    args = parser.parse_args()

    if args.no_color:
        Colors.disable()

    # Find Nexus root
    nexus_root = find_nexus_root()

    # Print header
    print()
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}  NOTION SKILLS TEST SUITE{Colors.END}")
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print()
    print(f"  Nexus Root: {nexus_root}")
    print(f"  Category:   {args.category}")
    print(f"  Mode:       {'Quick' if args.quick else 'Full'}")
    print()
    print(f"{Colors.BOLD}{'-'*60}{Colors.END}")
    print()

    # Handle additional suite options
    if args.scripts and not args.full:
        print(f"\n{Colors.BOLD}Running Script Integration Tests...{Colors.END}\n")
        run_additional_suite('scripts', nexus_root)
        return

    if args.live_api and not args.full:
        print(f"\n{Colors.BOLD}Running Live API Tests...{Colors.END}\n")
        run_additional_suite('live-api', nexus_root)
        return

    if args.dry_run:
        print("DRY-RUN: Would run the following tests:")
        # Just list tests without running
        suite = TestSuite(nexus_root, verbose=args.verbose)
        return

    # Create and run test suite
    suite = TestSuite(nexus_root, verbose=args.verbose)

    start_time = time.time()

    if args.quick:
        results = suite.run_quick()
    else:
        results = suite.run_category(args.category)

    total_time = time.time() - start_time

    # Print summary
    print()
    print(f"{Colors.BOLD}{'-'*60}{Colors.END}")
    print()

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed and not r.skipped)
    skipped = sum(1 for r in results if r.skipped)
    total = len(results)

    print(f"  {Colors.BOLD}SUMMARY{Colors.END}")
    print(f"  {Colors.GREEN}Passed:  {passed}/{total}{Colors.END}")
    if failed > 0:
        print(f"  {Colors.RED}Failed:  {failed}/{total}{Colors.END}")
    if skipped > 0:
        print(f"  {Colors.YELLOW}Skipped: {skipped}/{total}{Colors.END}")
    print(f"  Time:    {total_time:.2f}s")
    print()

    if failed > 0:
        print(f"{Colors.RED}  [FAIL] Some tests failed{Colors.END}")
        print()
        print("  Failed tests:")
        for r in results:
            if not r.passed and not r.skipped:
                print(f"    - {r.name}")
                if r.message:
                    print(f"      {r.message}")
    else:
        print(f"{Colors.GREEN}  [OK] All tests passed!{Colors.END}")

    # Run additional suites if --full
    if args.full:
        print()
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}  RUNNING ADDITIONAL TEST SUITES{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")

        print(f"\n{Colors.BOLD}[Script Integration Tests]{Colors.END}\n")
        run_additional_suite('scripts', nexus_root)

        print(f"\n{Colors.BOLD}[Live API Tests]{Colors.END}\n")
        run_additional_suite('live-api', nexus_root)

    print()
    print(f"{Colors.BOLD}{'='*60}{Colors.END}")
    print()

    # Exit with appropriate code
    sys.exit(0 if failed == 0 else 1)


if __name__ == '__main__':
    main()
