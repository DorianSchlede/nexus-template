#!/bin/bash
#
# get_nexus_context.sh - Output the same context the main agent receives from SessionStart hook
#
# Usage:
#   .claude/hooks/get_nexus_context.sh                    # Output cached context
#   .claude/hooks/get_nexus_context.sh --regenerate       # Regenerate fresh context
#
# For subagents: Include in your Task prompt:
#   "First run: bash .claude/hooks/get_nexus_context.sh | head -500"
#   or
#   "First read 00-system/.cache/session_start_context.xml"
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUILD_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
CACHE_FILE="$BUILD_DIR/00-system/.cache/session_start_context.xml"

# Check for --regenerate flag
if [[ "$1" == "--regenerate" ]]; then
    # Regenerate by calling the Python hook with mock input
    echo '{"session_id":"subagent-context","source":"startup","transcript_path":""}' | \
        CLAUDE_BUILD_DIR="$BUILD_DIR" python "$SCRIPT_DIR/session_start.py" 2>/dev/null

    # Now output the fresh cache
    if [[ -f "$CACHE_FILE" ]]; then
        cat "$CACHE_FILE"
    else
        echo "ERROR: Failed to regenerate context"
        exit 1
    fi
else
    # Just output the cached context (fast path)
    if [[ -f "$CACHE_FILE" ]]; then
        cat "$CACHE_FILE"
    else
        echo "ERROR: No cached context found at $CACHE_FILE"
        echo "Run with --regenerate to create it, or start a new session."
        exit 1
    fi
fi
