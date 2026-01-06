"""
Schema Validation Tests for Project 24 - Phase 0.3

Tests the JSON schemas for:
- precompact_state.json (FLAT schema)
- resume-context.md (YAML frontmatter)

Run with: python test_schemas.py
"""

import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple


# Schema validation functions
def validate_precompact_state(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate precompact_state.json against FLAT schema.

    Returns: (is_valid, error_message)
    """
    # Required fields
    required_fields = ["active_project_id", "confidence", "detection_method", "timestamp"]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Check for nested schema (WRONG)
    if "project_detection" in data:
        return False, "Schema must be FLAT - found nested 'project_detection' (WRONG)"

    # Validate active_project_id pattern (NN-kebab-case)
    project_id = data["active_project_id"]
    if project_id is not None:  # Can be null
        if not isinstance(project_id, str):
            return False, f"active_project_id must be string, got {type(project_id)}"
        parts = project_id.split("-", 1)
        if len(parts) < 2 or not parts[0].isdigit() or len(parts[0]) != 2:
            return False, f"active_project_id must match 'NN-*' pattern, got: {project_id}"

    # Validate confidence enum
    valid_confidence = ["high", "medium", "low"]
    if data["confidence"] not in valid_confidence:
        return False, f"confidence must be one of {valid_confidence}, got: {data['confidence']}"

    # Validate detection_method enum
    valid_methods = ["transcript", "cache", "fallback"]
    if data["detection_method"] not in valid_methods:
        return False, f"detection_method must be one of {valid_methods}, got: {data['detection_method']}"

    # Validate timestamp ISO-8601 format
    try:
        # Handle both with and without 'Z' suffix
        ts = data["timestamp"].replace("Z", "+00:00")
        datetime.fromisoformat(ts)
    except (ValueError, AttributeError) as e:
        return False, f"timestamp must be valid ISO-8601 format: {e}"

    # Validate file size (< 1KB)
    size = len(json.dumps(data).encode('utf-8'))
    if size > 1024:
        return False, f"JSON size {size} bytes exceeds 1KB limit"

    return True, "Valid"


def validate_resume_context(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate resume-context.md YAML frontmatter.

    Returns: (is_valid, error_message)
    """
    # Required fields
    required_fields = [
        "resume_schema_version", "project_id", "project_name",
        "current_phase", "next_action", "files_to_load", "last_updated"
    ]
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: {field}"

    # Validate resume_schema_version
    if data["resume_schema_version"] != "1.0":
        return False, f"resume_schema_version must be '1.0', got: {data['resume_schema_version']}"

    # Validate project_id pattern
    project_id = data["project_id"]
    parts = project_id.split("-", 1)
    if len(parts) < 2 or not parts[0].isdigit() or len(parts[0]) != 2:
        return False, f"project_id must match 'NN-*' pattern, got: {project_id}"

    # Validate current_phase enum
    valid_phases = ["research", "planning", "execution", "ready-for-implementation", "testing", "review"]
    if data["current_phase"] not in valid_phases:
        return False, f"current_phase must be one of {valid_phases}, got: {data['current_phase']}"

    # Validate files_to_load is array
    if not isinstance(data["files_to_load"], list):
        return False, f"files_to_load must be array, got: {type(data['files_to_load'])}"

    if len(data["files_to_load"]) < 1:
        return False, "files_to_load must have at least 1 file"

    # Validate timestamp
    try:
        ts = data["last_updated"].replace("Z", "+00:00")
        datetime.fromisoformat(ts)
    except (ValueError, AttributeError) as e:
        return False, f"last_updated must be valid ISO-8601 format: {e}"

    return True, "Valid"


def validate_legacy_resume(data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate old _resume.md format for backward compatibility.

    Returns: (is_valid, error_message)
    """
    # Old format uses 'resume_version' instead of 'resume_schema_version'
    if "resume_version" not in data and "resume_schema_version" not in data:
        return False, "Missing version field (resume_version or resume_schema_version)"

    # Must have project_id
    if "project_id" not in data:
        return False, "Missing required field: project_id"

    return True, "Valid (legacy format)"


# Test suite
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
        print("SCHEMA VALIDATION TEST RESULTS")
        print("="*80)
        for test in self.tests:
            status = "[PASS]" if test["passed"] else "[FAIL]"
            print(f"{status}: {test['name']}")
            if test["message"] and not test["passed"]:
                print(f"  -> {test['message']}")
        print("="*80)
        print(f"Total: {self.passed + self.failed} | Passed: {self.passed} | Failed: {self.failed}")
        print("="*80 + "\n")
        return self.failed == 0


# Test 1: precompact_state.json - Valid High Confidence
def test_1_precompact_valid_high_confidence(results: TestResults):
    """Test valid precompact_state with high confidence."""
    data = {
        "active_project_id": "24-project-skills-research-resume-expansion",
        "confidence": "high",
        "detection_method": "transcript",
        "timestamp": "2026-01-04T12:00:00Z"
    }
    is_valid, message = validate_precompact_state(data)
    results.add_result("Test 1: precompact_state valid (high confidence)", is_valid, message)


# Test 2: precompact_state.json - FLAT Schema Enforcement
def test_2_precompact_reject_nested(results: TestResults):
    """Test that nested schema is rejected (CRITICAL)."""
    data = {
        "project_detection": {  # NESTED - WRONG
            "project_id": "24-project-test",
            "confidence": "high"
        },
        "confidence": "high",
        "detection_method": "transcript",
        "timestamp": "2026-01-04T12:00:00Z"
    }
    is_valid, message = validate_precompact_state(data)
    # Should FAIL (nested schema)
    results.add_result("Test 2: precompact_state rejects NESTED schema", not is_valid, message)


# Test 3: precompact_state.json - Missing Required Fields
def test_3_precompact_missing_fields(results: TestResults):
    """Test validation fails when required fields missing."""
    data = {
        "active_project_id": "24-project-test"
        # Missing: confidence, detection_method, timestamp
    }
    is_valid, message = validate_precompact_state(data)
    # Should FAIL
    results.add_result("Test 3: precompact_state rejects missing fields", not is_valid, message)


# Test 4: precompact_state.json - Invalid Enum Values
def test_4_precompact_invalid_enum(results: TestResults):
    """Test validation fails for invalid enum values."""
    data = {
        "active_project_id": "24-project-test",
        "confidence": "very_high",  # Invalid enum
        "detection_method": "transcript",
        "timestamp": "2026-01-04T12:00:00Z"
    }
    is_valid, message = validate_precompact_state(data)
    # Should FAIL
    results.add_result("Test 4: precompact_state rejects invalid enum", not is_valid, message)


# Test 5: resume-context.md - Valid Execution Phase
def test_5_resume_context_valid(results: TestResults):
    """Test valid resume-context.md YAML."""
    data = {
        "resume_schema_version": "1.0",
        "project_id": "24-project-skills-research-resume-expansion",
        "project_name": "Project Skills Research & Resume Expansion",
        "current_phase": "execution",
        "next_action": "execute-project",
        "files_to_load": [
            "01-planning/overview.md",
            "01-planning/plan.md"
        ],
        "current_section": 0,
        "current_task": 1,
        "progress": "Phase 0 complete",
        "last_updated": "2026-01-04T12:00:00Z"
    }
    is_valid, message = validate_resume_context(data)
    results.add_result("Test 5: resume-context.md valid", is_valid, message)


# Test 6: resume-context.md - Invalid Phase Enum
def test_6_resume_context_invalid_phase(results: TestResults):
    """Test validation fails for invalid phase enum."""
    data = {
        "resume_schema_version": "1.0",
        "project_id": "24-project-test",
        "project_name": "Test",
        "current_phase": "debugging",  # Invalid enum
        "next_action": "execute-project",
        "files_to_load": ["01-planning/overview.md"],
        "last_updated": "2026-01-04T12:00:00Z"
    }
    is_valid, message = validate_resume_context(data)
    # Should FAIL
    results.add_result("Test 6: resume-context.md rejects invalid phase", not is_valid, message)


# Test 7: Backward Compatibility - Legacy _resume.md Format
def test_7_legacy_resume_compatibility(results: TestResults):
    """Test backward compatibility with old _resume.md format."""
    # Old format uses 'resume_version' instead of 'resume_schema_version'
    data = {
        "resume_version": "1.2",  # Old field name
        "project_id": "24-project-test",
        "phase": "execution",
        "files_to_load": ["01-planning/overview.md"]
    }
    is_valid, message = validate_legacy_resume(data)
    results.add_result("Test 7: Legacy _resume.md backward compatibility", is_valid, message)


def run_all_tests():
    """Run all schema validation tests."""
    results = TestResults()

    print("\nRunning Schema Validation Tests (Phase 0.3)...")
    print("-" * 80)

    test_1_precompact_valid_high_confidence(results)
    test_2_precompact_reject_nested(results)
    test_3_precompact_missing_fields(results)
    test_4_precompact_invalid_enum(results)
    test_5_resume_context_valid(results)
    test_6_resume_context_invalid_phase(results)
    test_7_legacy_resume_compatibility(results)

    all_passed = results.print_summary()
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
