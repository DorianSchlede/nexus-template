"""
Langfuse Configuration Checker

Validates environment variables and returns actionable JSON for AI.
"""

import os
import sys
import json
import argparse
from dotenv import load_dotenv

load_dotenv()


def check_config() -> dict:
    """Check Langfuse configuration and return status."""
    required_vars = {
        "LANGFUSE_PUBLIC_KEY": os.getenv("LANGFUSE_PUBLIC_KEY"),
        "LANGFUSE_SECRET_KEY": os.getenv("LANGFUSE_SECRET_KEY"),
        "LANGFUSE_HOST": os.getenv("LANGFUSE_HOST")
    }

    missing = [k for k, v in required_vars.items() if not v]

    if missing:
        return {
            "status": "not_configured",
            "ai_action": "prompt_for_api_key",
            "missing": missing,
            "configured": [k for k, v in required_vars.items() if v],
            "fix_instructions": [
                f"Add {var} to .env file" for var in missing
            ],
            "example": {
                "LANGFUSE_PUBLIC_KEY": "pk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "LANGFUSE_SECRET_KEY": "sk-lf-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
                "LANGFUSE_HOST": "https://cloud.langfuse.com"
            }
        }

    # Validate format
    public_key = required_vars["LANGFUSE_PUBLIC_KEY"]
    secret_key = required_vars["LANGFUSE_SECRET_KEY"]
    host = required_vars["LANGFUSE_HOST"]

    warnings = []

    if not public_key.startswith("pk-lf-"):
        warnings.append("LANGFUSE_PUBLIC_KEY should start with 'pk-lf-'")

    if not secret_key.startswith("sk-lf-"):
        warnings.append("LANGFUSE_SECRET_KEY should start with 'sk-lf-'")

    if not host.startswith("http"):
        warnings.append("LANGFUSE_HOST should be a full URL (https://...)")

    return {
        "status": "configured",
        "ai_action": "proceed_with_operation",
        "missing": [],
        "configured": list(required_vars.keys()),
        "host": host,
        "warnings": warnings if warnings else None
    }


def test_connection() -> dict:
    """Test actual API connection."""
    try:
        from langfuse_client import get_client
        client = get_client()
        result = client.get("/projects")
        return {
            "connection": "success",
            "project": result.get("name", "Unknown")
        }
    except Exception as e:
        return {
            "connection": "failed",
            "error": str(e)
        }


def main():
    parser = argparse.ArgumentParser(description="Check Langfuse configuration")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    args = parser.parse_args()

    result = check_config()

    if args.test and result["status"] == "configured":
        result["connection_test"] = test_connection()

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if result["status"] == "configured":
            print("[OK] Langfuse configuration valid")
            print(f"     Host: {result['host']}")
            if result.get("warnings"):
                for w in result["warnings"]:
                    print(f"     [WARN] {w}")
            if result.get("connection_test"):
                ct = result["connection_test"]
                if ct["connection"] == "success":
                    print(f"     [OK] Connection test passed - Project: {ct['project']}")
                else:
                    print(f"     [FAIL] Connection test failed: {ct['error']}")
        else:
            print("[FAIL] Langfuse configuration incomplete")
            print(f"       Missing: {', '.join(result['missing'])}")
            for fix in result["fix_instructions"]:
                print(f"       → {fix}")

    sys.exit(0 if result["status"] == "configured" else 1)


if __name__ == "__main__":
    main()
