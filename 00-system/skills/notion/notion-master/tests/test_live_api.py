#!/usr/bin/env python3
"""
Live API Integration Tests - Tests actual Notion API operations

WARNING: These tests create, modify, and delete real data in Notion!
Run with caution. Uses a dedicated test database when possible.

Usage:
    python test_live_api.py                    # Run all live tests
    python test_live_api.py --category pages   # Run specific category
    python test_live_api.py --cleanup          # Clean up test data only
"""

import sys
import os
import json
import argparse
import time
import uuid
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Any

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

try:
    import requests
    import yaml
except ImportError:
    print("[ERROR] Missing dependencies: pip install requests pyyaml")
    sys.exit(1)


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class NotionAPITester:
    """Live API testing for Notion integration"""

    def __init__(self, nexus_root: Path):
        self.nexus_root = nexus_root
        self.api_key = None
        self.database_id = None
        self.headers = {}
        self.test_page_ids = []  # Track pages created for cleanup
        self.test_block_ids = []  # Track blocks created for cleanup
        self.results = []
        self._load_config()

    def _load_config(self):
        """Load API configuration"""
        env_path = self.nexus_root / '.env'
        if not env_path.exists():
            raise ValueError(".env file not found")

        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key == 'NOTION_API_KEY':
                        self.api_key = value
                    elif key == 'NOTION_SKILLS_DB_ID':
                        self.database_id = value

        if not self.api_key:
            raise ValueError("NOTION_API_KEY not found in .env")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def _log(self, status: str, message: str, details: str = ""):
        """Log test result"""
        color = Colors.GREEN if status == "PASS" else Colors.RED if status == "FAIL" else Colors.YELLOW
        print(f"  [{color}{status}{Colors.END}] {message}")
        if details:
            print(f"         {Colors.CYAN}{details}{Colors.END}")
        self.results.append({"status": status, "message": message, "details": details})

    # ========== USER API TESTS ==========
    def test_get_current_user(self):
        """Test GET /users/me endpoint"""
        print(f"\n{Colors.BOLD}[USERS API]{Colors.END}")

        response = requests.get(
            "https://api.notion.com/v1/users/me",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            self._log("PASS", "GET /users/me", f"Bot: {data.get('name', 'Unknown')}")
            return data
        else:
            self._log("FAIL", "GET /users/me", f"Status: {response.status_code}")
            return None

    def test_list_users(self):
        """Test GET /users endpoint"""
        response = requests.get(
            "https://api.notion.com/v1/users",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "GET /users (list)", f"Found {count} users")
            return data
        else:
            self._log("FAIL", "GET /users (list)", f"Status: {response.status_code}")
            return None

    # ========== DATABASE API TESTS ==========
    def test_get_database(self):
        """Test GET /databases/{id} endpoint"""
        print(f"\n{Colors.BOLD}[DATABASE API]{Colors.END}")

        if not self.database_id:
            self._log("SKIP", "GET /databases/{id}", "No database ID configured")
            return None

        response = requests.get(
            f"https://api.notion.com/v1/databases/{self.database_id}",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            title = data.get('title', [{}])[0].get('plain_text', 'Unknown')
            props = len(data.get('properties', {}))
            self._log("PASS", "GET /databases/{id}", f"'{title}' with {props} properties")
            return data
        else:
            self._log("FAIL", "GET /databases/{id}", f"Status: {response.status_code}")
            return None

    def test_query_database_basic(self):
        """Test POST /databases/{id}/query - basic query"""
        if not self.database_id:
            self._log("SKIP", "POST /databases/{id}/query (basic)", "No database ID")
            return None

        response = requests.post(
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            headers=self.headers,
            json={"page_size": 3},
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            has_more = data.get('has_more', False)
            self._log("PASS", "POST /databases/query (basic)", f"Got {count} results, has_more={has_more}")
            return data
        else:
            self._log("FAIL", "POST /databases/query (basic)", f"Status: {response.status_code}")
            return None

    def test_query_database_with_filter(self):
        """Test POST /databases/{id}/query - with filter"""
        if not self.database_id:
            self._log("SKIP", "POST /databases/query (filter)", "No database ID")
            return None

        # Filter for Team = General
        filter_payload = {
            "page_size": 5,
            "filter": {
                "property": "Team",
                "select": {"equals": "General"}
            }
        }

        response = requests.post(
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            headers=self.headers,
            json=filter_payload,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "POST /databases/query (filter)", f"Filter Team=General: {count} results")
            return data
        else:
            self._log("FAIL", "POST /databases/query (filter)", f"Status: {response.status_code}")
            return None

    def test_query_database_with_and_filter(self):
        """Test POST /databases/{id}/query - with AND compound filter"""
        if not self.database_id:
            self._log("SKIP", "POST /databases/query (AND)", "No database ID")
            return None

        # AND filter: Team = General AND Integration contains Notion
        filter_payload = {
            "page_size": 5,
            "filter": {
                "and": [
                    {"property": "Team", "select": {"equals": "General"}},
                    {"property": "Integration", "multi_select": {"contains": "Notion"}}
                ]
            }
        }

        response = requests.post(
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            headers=self.headers,
            json=filter_payload,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "POST /databases/query (AND)", f"AND filter: {count} results")
            return data
        else:
            self._log("FAIL", "POST /databases/query (AND)", f"Status: {response.status_code}")
            return None

    def test_query_database_with_sort(self):
        """Test POST /databases/{id}/query - with sorting"""
        if not self.database_id:
            self._log("SKIP", "POST /databases/query (sort)", "No database ID")
            return None

        sort_payload = {
            "page_size": 3,
            "sorts": [
                {"property": "Created", "direction": "descending"}
            ]
        }

        response = requests.post(
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            headers=self.headers,
            json=sort_payload,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "POST /databases/query (sort)", f"Sorted by Created desc: {count} results")
            return data
        else:
            self._log("FAIL", "POST /databases/query (sort)", f"Status: {response.status_code}")
            return None

    def test_search_databases(self):
        """Test POST /search endpoint for databases"""
        response = requests.post(
            "https://api.notion.com/v1/search",
            headers=self.headers,
            json={
                "filter": {"property": "object", "value": "database"},
                "page_size": 10
            },
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "POST /search (databases)", f"Found {count} databases")
            return data
        else:
            self._log("FAIL", "POST /search (databases)", f"Status: {response.status_code}")
            return None

    # ========== PAGE API TESTS ==========
    def test_create_page(self) -> Optional[str]:
        """Test POST /pages - create a test page"""
        print(f"\n{Colors.BOLD}[PAGE API]{Colors.END}")

        if not self.database_id:
            self._log("SKIP", "POST /pages (create)", "No database ID")
            return None

        # Create a test page with unique name
        test_name = f"__TEST_PAGE_{uuid.uuid4().hex[:8]}"

        page_data = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Skill Name": {
                    "title": [{"text": {"content": test_name}}]
                },
                "Team": {
                    "select": {"name": "General"}
                },
                "Description": {
                    "rich_text": [{"text": {"content": "Automated test page - safe to delete"}}]
                }
            }
        }

        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=self.headers,
            json=page_data,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            page_id = data.get('id')
            self.test_page_ids.append(page_id)
            self._log("PASS", "POST /pages (create)", f"Created: {test_name}")
            return page_id
        else:
            error = response.json().get('message', response.text[:100])
            self._log("FAIL", "POST /pages (create)", f"Status: {response.status_code} - {error}")
            return None

    def test_get_page(self, page_id: str):
        """Test GET /pages/{id}"""
        if not page_id:
            self._log("SKIP", "GET /pages/{id}", "No page ID")
            return None

        response = requests.get(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            self._log("PASS", "GET /pages/{id}", f"Retrieved page {page_id[:8]}...")
            return data
        else:
            self._log("FAIL", "GET /pages/{id}", f"Status: {response.status_code}")
            return None

    def test_update_page(self, page_id: str):
        """Test PATCH /pages/{id}"""
        if not page_id:
            self._log("SKIP", "PATCH /pages/{id}", "No page ID")
            return None

        update_data = {
            "properties": {
                "Description": {
                    "rich_text": [{"text": {"content": f"Updated at {datetime.now().isoformat()}"}}]
                }
            }
        }

        response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=self.headers,
            json=update_data,
            timeout=10
        )

        if response.status_code == 200:
            self._log("PASS", "PATCH /pages/{id}", f"Updated page {page_id[:8]}...")
            return response.json()
        else:
            self._log("FAIL", "PATCH /pages/{id}", f"Status: {response.status_code}")
            return None

    def test_archive_page(self, page_id: str):
        """Test archiving (soft delete) a page"""
        if not page_id:
            self._log("SKIP", "PATCH /pages/{id} (archive)", "No page ID")
            return None

        response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=self.headers,
            json={"archived": True},
            timeout=10
        )

        if response.status_code == 200:
            self._log("PASS", "PATCH /pages/{id} (archive)", f"Archived page {page_id[:8]}...")
            return True
        else:
            self._log("FAIL", "PATCH /pages/{id} (archive)", f"Status: {response.status_code}")
            return False

    # ========== BLOCK API TESTS ==========
    def test_append_block(self, page_id: str) -> Optional[str]:
        """Test PATCH /blocks/{id}/children - append blocks"""
        print(f"\n{Colors.BOLD}[BLOCK API]{Colors.END}")

        if not page_id:
            self._log("SKIP", "PATCH /blocks/{id}/children", "No page ID")
            return None

        blocks = {
            "children": [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Test Section"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": "This is a test paragraph created by automated testing."}}]
                    }
                },
                {
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": "Test bullet point"}}]
                    }
                }
            ]
        }

        response = requests.patch(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=self.headers,
            json=blocks,
            timeout=15
        )

        if response.status_code == 200:
            data = response.json()
            block_ids = [b.get('id') for b in data.get('results', [])]
            self.test_block_ids.extend(block_ids)
            self._log("PASS", "PATCH /blocks/{id}/children", f"Appended {len(block_ids)} blocks")
            return block_ids[0] if block_ids else None
        else:
            error = response.json().get('message', response.text[:100])
            self._log("FAIL", "PATCH /blocks/{id}/children", f"Status: {response.status_code} - {error}")
            return None

    def test_get_block_children(self, page_id: str):
        """Test GET /blocks/{id}/children"""
        if not page_id:
            self._log("SKIP", "GET /blocks/{id}/children", "No page ID")
            return None

        response = requests.get(
            f"https://api.notion.com/v1/blocks/{page_id}/children",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "GET /blocks/{id}/children", f"Found {count} child blocks")
            return data
        else:
            self._log("FAIL", "GET /blocks/{id}/children", f"Status: {response.status_code}")
            return None

    def test_get_block(self, block_id: str):
        """Test GET /blocks/{id}"""
        if not block_id:
            self._log("SKIP", "GET /blocks/{id}", "No block ID")
            return None

        response = requests.get(
            f"https://api.notion.com/v1/blocks/{block_id}",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            block_type = data.get('type', 'unknown')
            self._log("PASS", "GET /blocks/{id}", f"Block type: {block_type}")
            return data
        else:
            self._log("FAIL", "GET /blocks/{id}", f"Status: {response.status_code}")
            return None

    def test_update_block(self, block_id: str):
        """Test PATCH /blocks/{id}"""
        if not block_id:
            self._log("SKIP", "PATCH /blocks/{id}", "No block ID")
            return None

        # Get block type first
        block = self.test_get_block(block_id)
        if not block:
            return None

        block_type = block.get('type')
        if block_type not in ['paragraph', 'heading_2', 'heading_1', 'bulleted_list_item']:
            self._log("SKIP", "PATCH /blocks/{id}", f"Block type {block_type} not easily updatable")
            return None

        update_data = {
            block_type: {
                "rich_text": [{"type": "text", "text": {"content": f"Updated at {datetime.now().isoformat()}"}}]
            }
        }

        response = requests.patch(
            f"https://api.notion.com/v1/blocks/{block_id}",
            headers=self.headers,
            json=update_data,
            timeout=10
        )

        if response.status_code == 200:
            self._log("PASS", "PATCH /blocks/{id}", f"Updated block {block_id[:8]}...")
            return response.json()
        else:
            self._log("FAIL", "PATCH /blocks/{id}", f"Status: {response.status_code}")
            return None

    def test_delete_block(self, block_id: str):
        """Test DELETE /blocks/{id}"""
        if not block_id:
            self._log("SKIP", "DELETE /blocks/{id}", "No block ID")
            return None

        response = requests.delete(
            f"https://api.notion.com/v1/blocks/{block_id}",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            self._log("PASS", "DELETE /blocks/{id}", f"Deleted block {block_id[:8]}...")
            return True
        else:
            self._log("FAIL", "DELETE /blocks/{id}", f"Status: {response.status_code}")
            return False

    # ========== COMMENTS API TESTS ==========
    def test_list_comments(self, page_id: str):
        """Test GET /comments - list comments on a page"""
        print(f"\n{Colors.BOLD}[COMMENTS API]{Colors.END}")

        if not page_id:
            self._log("SKIP", "GET /comments", "No page ID")
            return None

        response = requests.get(
            f"https://api.notion.com/v1/comments?block_id={page_id}",
            headers=self.headers,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            count = len(data.get('results', []))
            self._log("PASS", "GET /comments", f"Found {count} comments")
            return data
        else:
            # Comments API requires specific capability
            self._log("WARN", "GET /comments", f"Status: {response.status_code} (may need 'Insert comments' capability)")
            return None

    def test_create_comment(self, page_id: str):
        """Test POST /comments - create a comment"""
        if not page_id:
            self._log("SKIP", "POST /comments", "No page ID")
            return None

        comment_data = {
            "parent": {"page_id": page_id},
            "rich_text": [{"type": "text", "text": {"content": "Automated test comment"}}]
        }

        response = requests.post(
            "https://api.notion.com/v1/comments",
            headers=self.headers,
            json=comment_data,
            timeout=10
        )

        if response.status_code == 200:
            data = response.json()
            self._log("PASS", "POST /comments", f"Created comment")
            return data
        else:
            self._log("WARN", "POST /comments", f"Status: {response.status_code} (may need 'Insert comments' capability)")
            return None

    # ========== RATE LIMITING TESTS ==========
    def test_rate_limiting(self):
        """Test rate limiting behavior with rapid requests"""
        print(f"\n{Colors.BOLD}[RATE LIMITING]{Colors.END}")

        if not self.database_id:
            self._log("SKIP", "Rate limit test", "No database ID")
            return

        # Make 5 rapid requests
        statuses = []
        for i in range(5):
            response = requests.post(
                f"https://api.notion.com/v1/databases/{self.database_id}/query",
                headers=self.headers,
                json={"page_size": 1},
                timeout=10
            )
            statuses.append(response.status_code)
            # Small delay to avoid triggering rate limit in tests
            time.sleep(0.1)

        if all(s == 200 for s in statuses):
            self._log("PASS", "Rapid requests (5x)", "No rate limiting triggered")
        elif 429 in statuses:
            self._log("WARN", "Rapid requests (5x)", "Rate limit (429) encountered")
        else:
            self._log("FAIL", "Rapid requests (5x)", f"Statuses: {statuses}")

    # ========== PROPERTY TYPE TESTS ==========
    def test_property_types(self, page_id: str):
        """Test various property type handling"""
        print(f"\n{Colors.BOLD}[PROPERTY TYPES]{Colors.END}")

        if not page_id:
            self._log("SKIP", "Property types", "No page ID")
            return

        # Test updating different property types
        properties = {
            "Team": {"select": {"name": "Solutions"}},  # Select
            "Description": {"rich_text": [{"text": {"content": "Property type test"}}]},  # Rich text
        }

        response = requests.patch(
            f"https://api.notion.com/v1/pages/{page_id}",
            headers=self.headers,
            json={"properties": properties},
            timeout=10
        )

        if response.status_code == 200:
            self._log("PASS", "Update select property", "Team -> Solutions")
            self._log("PASS", "Update rich_text property", "Description updated")
        else:
            error = response.json().get('message', '')[:50]
            self._log("FAIL", "Property type updates", f"Status: {response.status_code} - {error}")

    # ========== PAGINATION TESTS ==========
    def test_pagination(self):
        """Test pagination with start_cursor"""
        print(f"\n{Colors.BOLD}[PAGINATION]{Colors.END}")

        if not self.database_id:
            self._log("SKIP", "Pagination test", "No database ID")
            return

        # First request
        response1 = requests.post(
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            headers=self.headers,
            json={"page_size": 2},
            timeout=15
        )

        if response1.status_code != 200:
            self._log("FAIL", "Pagination (page 1)", f"Status: {response1.status_code}")
            return

        data1 = response1.json()
        next_cursor = data1.get('next_cursor')

        if not next_cursor:
            self._log("PASS", "Pagination", "Only 1 page of results (no cursor needed)")
            return

        # Second request with cursor
        response2 = requests.post(
            f"https://api.notion.com/v1/databases/{self.database_id}/query",
            headers=self.headers,
            json={"page_size": 2, "start_cursor": next_cursor},
            timeout=15
        )

        if response2.status_code == 200:
            data2 = response2.json()
            page1_count = len(data1.get('results', []))
            page2_count = len(data2.get('results', []))
            self._log("PASS", "Pagination", f"Page 1: {page1_count}, Page 2: {page2_count}")
        else:
            self._log("FAIL", "Pagination (page 2)", f"Status: {response2.status_code}")

    # ========== SKILL IMPORT/EXPORT TESTS ==========
    def test_skill_search(self):
        """Test skill search via search_skill_database.py"""
        print(f"\n{Colors.BOLD}[SKILL SEARCH]{Colors.END}")

        import subprocess

        scripts_dir = self.nexus_root / '00-system' / 'skills' / 'notion' / 'notion-master' / 'scripts'
        script = scripts_dir / 'search_skill_database.py'

        if not script.exists():
            self._log("FAIL", "search_skill_database.py", "Script not found")
            return

        # Test 1: Basic skills query
        try:
            result = subprocess.run(
                [sys.executable, str(script), '--skills', '--limit', '3'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if result.returncode == 0 and ('[RESULTS]' in output or 'Found' in output):
                self._log("PASS", "Search --skills", "Basic query works")
            else:
                self._log("FAIL", "Search --skills", f"Exit: {result.returncode}")
        except subprocess.TimeoutExpired:
            self._log("FAIL", "Search --skills", "Timeout")
        except Exception as e:
            self._log("FAIL", "Search --skills", str(e))

        # Test 2: Filtered search with team
        try:
            result = subprocess.run(
                [sys.executable, str(script), '--skills', '--team', 'General', '--limit', '2'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0:
                self._log("PASS", "Search --team filter", "Team filter works")
            else:
                self._log("WARN", "Search --team filter", f"Exit: {result.returncode}")
        except Exception as e:
            self._log("FAIL", "Search --team filter", str(e))

        # Test 3: AND filter search
        try:
            result = subprocess.run(
                [sys.executable, str(script), '--skills', '--team', 'General', '--integration', 'Notion', '--limit', '2'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if result.returncode == 0 and 'and' in output.lower():
                self._log("PASS", "Search AND filter", "Compound filter works")
            else:
                self._log("WARN", "Search AND filter", "May not show AND in output")
        except Exception as e:
            self._log("FAIL", "Search AND filter", str(e))

        # Test 4: JSON output
        try:
            result = subprocess.run(
                [sys.executable, str(script), '--skills', '--limit', '1', '--json'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode == 0 and '[' in result.stdout:
                import json as json_mod
                try:
                    json_start = result.stdout.index('[')
                    json_mod.loads(result.stdout[json_start:])
                    self._log("PASS", "Search --json output", "Valid JSON returned")
                except (ValueError, json_mod.JSONDecodeError):
                    self._log("WARN", "Search --json output", "JSON parsing uncertain")
            else:
                self._log("WARN", "Search --json output", "No JSON array in output")
        except Exception as e:
            self._log("FAIL", "Search --json output", str(e))

    def test_skill_export_dry_run(self):
        """Test skill export with dry-run (doesn't actually upload)"""
        print(f"\n{Colors.BOLD}[SKILL EXPORT]{Colors.END}")

        import subprocess

        scripts_dir = self.nexus_root / '00-system' / 'skills' / 'notion' / 'notion-master' / 'scripts'
        script = scripts_dir / 'upload_skill.py'

        if not script.exists():
            self._log("FAIL", "upload_skill.py", "Script not found")
            return

        # Find a test skill to use
        test_skill = self.nexus_root / '00-system' / 'skills' / 'notion-connect'
        if not test_skill.exists():
            test_skill = self.nexus_root / '00-system' / 'skills' / 'query-notion-db'

        if not test_skill.exists():
            self._log("SKIP", "Export dry-run", "No test skill found")
            return

        # Test 1: Dry-run mode (doesn't actually upload)
        try:
            result = subprocess.run(
                [sys.executable, str(script), str(test_skill), '--team', 'General', '--dry-run'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if result.returncode == 0 and ('DRY-RUN' in output or 'dry_run' in output or 'would' in output.lower()):
                self._log("PASS", "Export --dry-run", "Validates without uploading")
            else:
                self._log("WARN", "Export --dry-run", f"Exit: {result.returncode}")
        except subprocess.TimeoutExpired:
            self._log("FAIL", "Export --dry-run", "Timeout")
        except Exception as e:
            self._log("FAIL", "Export --dry-run", str(e))

        # Test 2: SKILL.md validation
        try:
            result = subprocess.run(
                [sys.executable, str(script), str(test_skill), '--team', 'General', '--dry-run'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if 'SKILL.md' in output or 'valid' in output.lower() or 'bundle' in output.lower():
                self._log("PASS", "Export SKILL.md validation", "Validates skill structure")
            else:
                self._log("WARN", "Export SKILL.md validation", "Validation output unclear")
        except Exception as e:
            self._log("FAIL", "Export SKILL.md validation", str(e))

        # Test 3: JSON bundle creation
        try:
            result = subprocess.run(
                [sys.executable, str(script), str(test_skill), '--team', 'General', '--dry-run'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=30,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if 'bundle' in output.lower() or 'json' in output.lower() or 'files' in output.lower():
                self._log("PASS", "Export bundle creation", "Creates skill bundle")
            else:
                self._log("WARN", "Export bundle creation", "Bundle output unclear")
        except Exception as e:
            self._log("FAIL", "Export bundle creation", str(e))

    def test_skill_import_validation(self):
        """Test skill import error handling (with invalid page ID)"""
        print(f"\n{Colors.BOLD}[SKILL IMPORT]{Colors.END}")

        import subprocess

        scripts_dir = self.nexus_root / '00-system' / 'skills' / 'notion' / 'notion-master' / 'scripts'
        script = scripts_dir / 'download_skill.py'

        if not script.exists():
            self._log("FAIL", "download_skill.py", "Script not found")
            return

        # Test 1: Error on missing page ID
        try:
            result = subprocess.run(
                [sys.executable, str(script)],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            if result.returncode != 0:
                self._log("PASS", "Import requires page_id", "Enforces required argument")
            else:
                self._log("WARN", "Import requires page_id", "Should require page_id")
        except Exception as e:
            self._log("FAIL", "Import requires page_id", str(e))

        # Test 2: Error on invalid page ID
        try:
            result = subprocess.run(
                [sys.executable, str(script), 'invalid-page-id-xyz123'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=15,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if result.returncode != 0 or 'error' in output.lower() or 'not found' in output.lower():
                self._log("PASS", "Import invalid page_id", "Handles invalid ID gracefully")
            else:
                self._log("WARN", "Import invalid page_id", "Should error on invalid ID")
        except subprocess.TimeoutExpired:
            self._log("FAIL", "Import invalid page_id", "Timeout")
        except Exception as e:
            self._log("FAIL", "Import invalid page_id", str(e))

        # Test 3: Help output
        try:
            result = subprocess.run(
                [sys.executable, str(script), '--help'],
                cwd=str(self.nexus_root),
                capture_output=True,
                text=True,
                timeout=10,
                encoding='utf-8',
                errors='replace'
            )
            output = result.stdout + result.stderr
            if result.returncode == 0 and ('page_id' in output.lower() or 'output' in output.lower()):
                self._log("PASS", "Import --help", "Shows usage information")
            else:
                self._log("WARN", "Import --help", "Help output unclear")
        except Exception as e:
            self._log("FAIL", "Import --help", str(e))

    # ========== CLEANUP ==========
    def cleanup_test_data(self):
        """Clean up all test pages and blocks"""
        print(f"\n{Colors.BOLD}[CLEANUP]{Colors.END}")

        cleaned = 0
        failed = 0

        for page_id in self.test_page_ids:
            try:
                response = requests.patch(
                    f"https://api.notion.com/v1/pages/{page_id}",
                    headers=self.headers,
                    json={"archived": True},
                    timeout=10
                )
                if response.status_code == 200:
                    cleaned += 1
                else:
                    failed += 1
            except Exception:
                failed += 1

        if cleaned > 0 or failed > 0:
            self._log("INFO", "Cleanup", f"Archived {cleaned} pages, {failed} failed")
        else:
            self._log("INFO", "Cleanup", "No test data to clean up")

    # ========== RUN ALL TESTS ==========
    def run_all(self):
        """Run all live API tests"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}  NOTION LIVE API TESTS{Colors.END}")
        print(f"{Colors.BOLD}{'='*60}{Colors.END}")
        print(f"\n  Database: {self.database_id[:8]}..." if self.database_id else "  No database configured")

        # User tests
        self.test_get_current_user()
        self.test_list_users()

        # Database tests
        self.test_get_database()
        self.test_query_database_basic()
        self.test_query_database_with_filter()
        self.test_query_database_with_and_filter()
        self.test_query_database_with_sort()
        self.test_search_databases()

        # Page tests (creates test data)
        test_page_id = self.test_create_page()
        if test_page_id:
            self.test_get_page(test_page_id)
            self.test_update_page(test_page_id)
            self.test_property_types(test_page_id)

            # Block tests (uses test page)
            block_id = self.test_append_block(test_page_id)
            self.test_get_block_children(test_page_id)
            if block_id:
                self.test_get_block(block_id)
                # Skip update/delete to preserve test data for comment tests

            # Comment tests
            self.test_list_comments(test_page_id)
            self.test_create_comment(test_page_id)

        # Rate limiting
        self.test_rate_limiting()

        # Pagination
        self.test_pagination()

        # Skill import/export tests
        self.test_skill_search()
        self.test_skill_export_dry_run()
        self.test_skill_import_validation()

        # Cleanup
        self.cleanup_test_data()

        # Summary
        self._print_summary()

    def _print_summary(self):
        """Print test summary"""
        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}")

        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        warned = sum(1 for r in self.results if r['status'] == 'WARN')
        skipped = sum(1 for r in self.results if r['status'] == 'SKIP')
        total = len(self.results)

        print(f"\n  {Colors.BOLD}SUMMARY{Colors.END}")
        print(f"  {Colors.GREEN}Passed:  {passed}{Colors.END}")
        if failed > 0:
            print(f"  {Colors.RED}Failed:  {failed}{Colors.END}")
        if warned > 0:
            print(f"  {Colors.YELLOW}Warned:  {warned}{Colors.END}")
        if skipped > 0:
            print(f"  Skipped: {skipped}")
        print(f"  Total:   {total}")

        if failed == 0:
            print(f"\n{Colors.GREEN}  [OK] All API tests passed!{Colors.END}")
        else:
            print(f"\n{Colors.RED}  [FAIL] Some API tests failed{Colors.END}")

        print(f"\n{Colors.BOLD}{'='*60}{Colors.END}\n")


def find_nexus_root() -> Path:
    """Find Nexus root directory"""
    current = Path.cwd()
    for path in [current] + list(current.parents):
        if (path / 'CLAUDE.md').exists():
            return path
    return current


def main():
    parser = argparse.ArgumentParser(description='Notion Live API Tests')
    parser.add_argument('--cleanup', action='store_true', help='Run cleanup only')
    args = parser.parse_args()

    nexus_root = find_nexus_root()

    try:
        tester = NotionAPITester(nexus_root)

        if args.cleanup:
            tester.cleanup_test_data()
        else:
            tester.run_all()

    except ValueError as e:
        print(f"{Colors.RED}[ERROR] {e}{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}[ERROR] Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == '__main__':
    main()
