#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# ///

"""
Session Summary Hook - DISABLED (observability server removed).

This hook previously generated session summaries and sent them to an
observability server. The observability server has been removed from Nexus.
"""

import json
import sys


def main():
    """No-op hook - observability server removed."""
    try:
        # Read input to prevent pipe errors
        json.load(sys.stdin)
    except Exception:
        pass

    # Exit cleanly without doing anything
    sys.exit(0)


if __name__ == "__main__":
    main()
