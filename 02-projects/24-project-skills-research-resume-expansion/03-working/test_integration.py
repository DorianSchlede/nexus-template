"""
Integration Tests for Project 24 - Phase 0.3

Tests the integration between:
- PreCompact hook → precompact_state.json → SessionStart hook
- resume-context.md file loading and validation
- Session source detection
- File path resolution

Run with: python test_integration.py
"""

import json
import yaml
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List


# Integration helper functions
def simulate_precompact_write(project_id: str, confidence: str) -> Dict[str, Any]:
    """Simulate PreCompact hook writing precompact_state.json."""
    from datetime import timezone
    state = {
        "active_project_id": project_id,
        "confidence": confidence,
        "detection_method": "transcript",
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }
    return state


def simulate_session_start_read(state_data: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate SessionStart hook reading precompact_state.json."""
    # SessionStart reads FLAT schema
    return {
        "project_id": state_data.get("active_project_id"),  # FLAT access
        "confidence": state_data.get("confidence"),
        "method": state_data.get("detection_method")
    }


def should_load_resume(source: str) -> bool:
    """Determine if resume should be loaded based on session source."""
    # CRITICAL: Do NOT load resume when source="clear"
    return source in ("resume", "compact")


def validate_files_exist(resume_yaml: Dict[str, Any], project_path: str) -> bool:
    """Validate all files in files_to_load array exist."""
    files_to_load = resume_yaml.get("files_to_load", [])
    project_root = Path(project_path)

    for file_path in files_to_load:
        full_path = project_root / file_path
        if not full_path.exists():
            return False

    return True


def parse_resume_yaml(yaml_content: str) -> Dict[str, Any]:
    """Parse resume-context.md YAML frontmatter."""
    # Extract YAML frontmatter between --- delimiters
    lines = yaml_content.strip().split('\n')
    if lines[0] != '---':
        raise ValueError("Missing YAML frontmatter start delimiter")

    yaml_lines = []
    for i, line in enumerate(lines[1:], 1):
        if line == '---':
            break
        yaml_lines.append(line)

    yaml_content = '\n'.join(yaml_lines)
    return yaml.safe_load(yaml_content)


# Test results tracking
class TestResults:
    """Track test results."""
    def __init__(self):
        self.tests: List[Dict[str, Any]] = []
        self.passed = 0
        self.failed = 0

    def add_result(self, test_name: str, passed: bool, message: str = ""):
        self.tests.append({
            "name": test_name,
            "passed": passed,
            "message": message
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1

    def print_summary(self):
        print("\n" + "="*80)
        print("INTEGRATION TEST RESULTS")
        print("="*80)
        for test in self.tests:
            status = "[PASS]" if test["passed"] else "[FAIL]"
            print(f"{status}: {test['name']}")
            if test["message"]:
                print(f"  -> {test['message']}")
        print("="*80)
        print(f"Total: {self.passed + self.failed} | Passed: {self.passed} | Failed: {self.failed}")
        print("="*80 + "\n")
        return self.failed == 0


# Test 1: PreCompact -> SessionStart Flow (FLAT Schema)
def test_1_precompact_to_session_start(results: TestResults):
    """Test full flow: PreCompact writes FLAT schema, SessionStart reads it."""
    # Simulate PreCompact hook
    state = simulate_precompact_write("24-project-test", "high")

    # Verify FLAT schema (NOT nested)
    if "project_detection" in state:
        results.add_result(
            "Test 1: PreCompact -> SessionStart (FLAT schema)",
            False,
            "ERROR: Found nested 'project_detection' - schema must be FLAT"
        )
        return

    # Simulate SessionStart hook
    loaded = simulate_session_start_read(state)

    # Verify SessionStart can read FLAT schema
    passed = (
        loaded["project_id"] == "24-project-test" and
        loaded["confidence"] == "high" and
        loaded["method"] == "transcript"
    )

    results.add_result(
        "Test 1: PreCompact -> SessionStart (FLAT schema)",
        passed,
        "FLAT schema round-trip successful" if passed else "Round-trip failed"
    )


# Test 2: Session Source Detection (CRITICAL)
def test_2_session_source_detection(results: TestResults):
    """Test SessionStart respects source field (excludes 'clear')."""
    test_cases = [
        {"source": "resume", "expected": True, "desc": "resume source"},
        {"source": "compact", "expected": True, "desc": "compact source"},
        {"source": "clear", "expected": False, "desc": "clear source (MUST NOT LOAD)"},
        {"source": "startup", "expected": False, "desc": "startup source"}
    ]

    all_passed = True
    for case in test_cases:
        result = should_load_resume(case["source"])
        passed = result == case["expected"]
        if not passed:
            all_passed = False
            results.add_result(
                f"Test 2: Source detection - {case['desc']}",
                False,
                f"Expected {case['expected']}, got {result}"
            )

    if all_passed:
        results.add_result(
            "Test 2: Session source detection (all cases)",
            True,
            "All 4 source cases handled correctly"
        )


# Test 3: YAML Frontmatter Parsing
def test_3_yaml_frontmatter_parsing(results: TestResults):
    """Test resume-context.md YAML parsing."""
    yaml_content = """---
resume_schema_version: "1.0"
project_id: "24-project-test"
project_name: "Test Project"
current_phase: "execution"
next_action: "execute-project"
files_to_load:
  - "01-planning/overview.md"
  - "01-planning/plan.md"
last_updated: "2026-01-04T12:00:00Z"
---

# Validation Gate

Questions here...
"""

    try:
        data = parse_resume_yaml(yaml_content)
        passed = (
            data["resume_schema_version"] == "1.0" and
            data["project_id"] == "24-project-test" and
            len(data["files_to_load"]) == 2
        )
        results.add_result(
            "Test 3: YAML frontmatter parsing",
            passed,
            "Parsed successfully" if passed else "Parse succeeded but data incorrect"
        )
    except Exception as e:
        results.add_result(
            "Test 3: YAML frontmatter parsing",
            False,
            f"Parse failed: {e}"
        )


# Test 4: File Path Resolution (Valid Paths)
def test_4_file_path_resolution_valid(results: TestResults):
    """Test files_to_load validation with existing files."""
    # Use this project's actual files
    project_path = "c:/Users/dsber/infinite/auto-company/strategy-nexus/02-projects/24-project-skills-research-resume-expansion"

    resume_yaml = {
        "files_to_load": [
            "01-planning/overview.md",
            "01-planning/plan.md",
            "01-planning/steps.md"
        ]
    }

    # Check if files exist
    all_exist = validate_files_exist(resume_yaml, project_path)

    results.add_result(
        "Test 4: File path resolution (valid paths)",
        all_exist,
        "All files exist" if all_exist else "Some files missing"
    )


# Test 5: File Path Resolution (Missing File)
def test_5_file_path_resolution_missing(results: TestResults):
    """Test files_to_load validation detects missing files."""
    project_path = "c:/Users/dsber/infinite/auto-company/strategy-nexus/02-projects/24-project-skills-research-resume-expansion"

    resume_yaml = {
        "files_to_load": [
            "01-planning/overview.md",
            "01-planning/nonexistent.md"  # This should fail
        ]
    }

    # Should return False (missing file detected)
    all_exist = validate_files_exist(resume_yaml, project_path)

    results.add_result(
        "Test 5: File path resolution (missing file detection)",
        not all_exist,  # Should be False (missing file)
        "Correctly detected missing file" if not all_exist else "Failed to detect missing file"
    )


# Test 6: Timestamp Validation
def test_6_timestamp_validation(results: TestResults):
    """Test ISO-8601 timestamp format validation."""
    valid_timestamps = [
        "2026-01-04T12:00:00Z",
        "2026-01-04T12:00:00+00:00",
        "2026-01-04T12:00:00.123456Z"
    ]

    invalid_timestamps = [
        "2026/01/04T12:00:00Z",  # Slashes instead of dashes
        "not-a-timestamp",  # Completely invalid
        "2026-13-01T12:00:00Z"  # Invalid month (13)
    ]

    all_passed = True

    # Test valid timestamps
    for ts in valid_timestamps:
        try:
            ts_clean = ts.replace("Z", "+00:00")
            datetime.fromisoformat(ts_clean)
        except Exception as e:
            all_passed = False
            results.add_result(
                f"Test 6: Timestamp validation - {ts}",
                False,
                f"Valid timestamp rejected: {e}"
            )

    # Test invalid timestamps
    for ts in invalid_timestamps:
        try:
            ts_clean = ts.replace("Z", "+00:00")
            datetime.fromisoformat(ts_clean)
            all_passed = False
            results.add_result(
                f"Test 6: Timestamp validation - {ts}",
                False,
                f"Invalid timestamp accepted"
            )
        except Exception:
            pass  # Expected to fail

    if all_passed:
        results.add_result(
            "Test 6: Timestamp validation (all cases)",
            True,
            "All valid/invalid timestamps handled correctly"
        )


# Test 7: Schema Compatibility (Round-Trip)
def test_7_schema_compatibility(results: TestResults):
    """Test PreCompact output is compatible with SessionStart input."""
    # Full round-trip test:
    # 1. PreCompact writes state
    state = {
        "active_project_id": "24-project-skills-research-resume-expansion",
        "confidence": "high",
        "detection_method": "transcript",
        "timestamp": "2026-01-04T12:00:00Z",
        "metadata": {
            "transcript_lines": 1234,
            "mentions_count": 42,
            "last_mention_line": 1200
        }
    }

    # 2. Serialize to JSON (what PreCompact does)
    json_str = json.dumps(state, indent=2)

    # 3. Deserialize (what SessionStart does)
    loaded_state = json.loads(json_str)

    # 4. Verify SessionStart can access all fields with FLAT schema
    try:
        project_id = loaded_state["active_project_id"]  # FLAT access
        confidence = loaded_state["confidence"]
        method = loaded_state["detection_method"]
        timestamp = loaded_state["timestamp"]

        # Verify optional metadata
        metadata = loaded_state.get("metadata", {})
        mentions = metadata.get("mentions_count", 0)

        passed = (
            project_id == "24-project-skills-research-resume-expansion" and
            confidence == "high" and
            method == "transcript" and
            mentions == 42
        )

        results.add_result(
            "Test 7: Schema compatibility (round-trip)",
            passed,
            "Full round-trip successful" if passed else "Data mismatch after round-trip"
        )
    except Exception as e:
        results.add_result(
            "Test 7: Schema compatibility (round-trip)",
            False,
            f"Round-trip failed: {e}"
        )


def run_all_tests():
    """Run all integration tests."""
    results = TestResults()

    print("\nRunning Integration Tests (Phase 0.3)...")
    print("-" * 80)

    test_1_precompact_to_session_start(results)
    test_2_session_source_detection(results)
    test_3_yaml_frontmatter_parsing(results)
    test_4_file_path_resolution_valid(results)
    test_5_file_path_resolution_missing(results)
    test_6_timestamp_validation(results)
    test_7_schema_compatibility(results)

    all_passed = results.print_summary()
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
