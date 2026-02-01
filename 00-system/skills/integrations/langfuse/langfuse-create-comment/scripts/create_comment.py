#!/usr/bin/env python3
"""Langfuse Create Comment - Add comment to a trace or observation."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client, LangfuseAPIError


def create_comment(object_type: str, object_id: str, content: str, author_user_id: str = None) -> dict:
    """Create a comment on a trace or observation.

    Args:
        object_type: TRACE or OBSERVATION
        object_id: The trace or observation ID
        content: Comment text
        author_user_id: Optional author ID
    """
    if not content.strip():
        raise ValueError("Comment content cannot be empty")

    client = get_client()
    data = {
        "objectType": object_type,
        "objectId": object_id,
        "content": content
    }
    if author_user_id:
        data["authorUserId"] = author_user_id
    return client.post("/comments", data=data)


def main():
    parser = argparse.ArgumentParser(
        description="Add a comment to a trace or observation"
    )
    parser.add_argument("--type", type=str, required=True, choices=["TRACE", "OBSERVATION"],
                        help="Object type to comment on")
    parser.add_argument("--id", type=str, required=True, help="Object ID")
    parser.add_argument("--content", type=str, required=True, help="Comment text")
    parser.add_argument("--author", type=str, default=None, help="Author user ID (optional)")
    args = parser.parse_args()

    try:
        result = create_comment(
            object_type=args.type,
            object_id=args.id,
            content=args.content,
            author_user_id=args.author
        )
        print(json.dumps(result, indent=2, default=str))
    except ValueError as e:
        print(f"VALIDATION ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    except LangfuseAPIError as e:
        print(f"API ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
