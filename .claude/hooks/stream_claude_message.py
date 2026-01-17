#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///
from __future__ import annotations
"""
Stream Claude's messages to the observability server after each tool call.

This hook reads the transcript file and extracts Claude's latest text content,
then streams it to the server for analysis and storage.

Hook Event: PostToolUse
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory for utils imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.http import send_to_server


def parse_transcript(transcript_path: str) -> list[dict]:
    """Parse JSONL transcript file into list of entries."""
    entries = []
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
    except (FileNotFoundError, PermissionError):
        pass
    return entries


def extract_latest_claude_message(entries: list[dict]) -> dict | None:
    """
    Extract Claude's most recent message with text content.

    Claude Code transcript format:
    - entry.type == "assistant" (not entry.role)
    - entry.message.role == "assistant"
    - entry.message.content[] contains text blocks

    Returns dict with:
        - text: The text content
        - tool_calls: List of tool names called in same message
        - message_index: Position in conversation
    """
    # Find the last assistant message
    for i in range(len(entries) - 1, -1, -1):
        entry = entries[i]

        # Claude Code transcript format: type="assistant" with message object
        if entry.get("type") == "assistant":
            message = entry.get("message", {})
            content = message.get("content", [])

            text_parts = []
            tool_calls = []

            for block in content:
                if isinstance(block, dict):
                    if block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                    elif block.get("type") == "tool_use":
                        tool_calls.append(block.get("name", "unknown"))
                elif isinstance(block, str):
                    text_parts.append(block)

            if text_parts:
                return {
                    "text": "\n".join(text_parts),
                    "tool_calls": tool_calls,
                    "message_index": i
                }

    return None


def count_messages_by_type(entries: list[dict]) -> dict:
    """Count messages by type for context (Claude Code transcript format)."""
    counts = {"user": 0, "assistant": 0, "system": 0}
    for entry in entries:
        entry_type = entry.get("type", "unknown")
        if entry_type in counts:
            counts[entry_type] += 1
    return counts


def main():
    try:
        input_data = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)

    session_id = input_data.get("session_id", "unknown")
    transcript_path = input_data.get("transcript_path")
    tool_name = input_data.get("tool_name", "")
    tool_use_id = input_data.get("tool_use_id", "")

    # Skip if no transcript path
    if not transcript_path:
        sys.exit(0)

    # Parse transcript
    entries = parse_transcript(transcript_path)
    if not entries:
        sys.exit(0)

    # Extract Claude's latest message
    latest = extract_latest_claude_message(entries)
    if not latest or not latest["text"]:
        sys.exit(0)

    # Get conversation stats
    message_counts = count_messages_by_type(entries)

    # Build payload for server
    payload = {
        "type": "claude_message",
        "content": latest["text"],
        "content_length": len(latest["text"]),
        "after_tool": tool_name,
        "tool_use_id": tool_use_id,
        "tool_calls_in_message": latest["tool_calls"],
        "message_index": latest["message_index"],
        "conversation_stats": message_counts,
        "total_entries": len(entries),
        "timestamp": datetime.now().isoformat()
    }

    # Stream to server using existing events endpoint
    # Using /events endpoint which already supports message content
    event_payload = {
        "source_app": "claude-code",
        "session_id": session_id,
        "hook_event_type": "claude_message",
        "payload": payload,
        "chat": [{"role": "assistant", "content": latest["text"][:5000]}],  # Truncate for storage
    }

    send_to_server("/events", event_payload)

    sys.exit(0)


if __name__ == "__main__":
    main()
