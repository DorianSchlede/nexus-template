"""Get Langfuse project info."""

import sys
import json
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "langfuse-master" / "scripts"))
from langfuse_client import get_client


def get_project() -> dict:
    """
    Get the project associated with the API key.

    Returns:
        dict: Project details
    """
    client = get_client()
    return client.get("/projects")


def main():
    parser = argparse.ArgumentParser(description="Get Langfuse project")
    parser.parse_args()

    result = get_project()
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    main()
