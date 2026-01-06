#!/usr/bin/env python3
"""Test 20K token output for session_start.py"""
import os
import sys
import json

# Set env var for 20K tokens
os.environ["TEST_ADDITIONAL_CONTEXT_TOKENS"] = "25000"

# Import after setting env
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from session_start import build_startup_context, generate_test_padding

# Build context
context = build_startup_context(os.getcwd())

# Add test padding
test_padding = generate_test_padding()
if test_padding:
    context["_test_padding"] = test_padding
    context["_test_info"] = {
        "target_tokens": 20000,
        "actual_chars": len(test_padding),
        "estimated_tokens": len(test_padding) // 4
    }

# Create hook output
hook_output = {
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": json.dumps(context, ensure_ascii=False)
    }
}

# Output stats
ctx = hook_output["hookSpecificOutput"]["additionalContext"]
print(f"Total chars: {len(ctx)}")
print(f"Estimated tokens: {len(ctx) // 4}")
print(f"Has padding: {'_test_padding' in context}")
print(f"Test info: {context.get('_test_info', 'none')}")
print(f"\nFull hook output length: {len(json.dumps(hook_output))} chars")
