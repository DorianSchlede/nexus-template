#!/usr/bin/env python3
"""
NotebookLM Enterprise Setup Wizard

Interactive setup for NotebookLM Enterprise integration.
Guides through Google Cloud configuration and tests connection.
"""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"


def print_banner():
    print()
    print("=" * 50)
    print("  NotebookLM Enterprise Setup Wizard")
    print("=" * 50)
    print()


def check_gcloud():
    """Check if gcloud CLI is installed"""
    try:
        result = subprocess.run(['gcloud', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


def check_gcloud_auth():
    """Check if gcloud is authenticated"""
    try:
        result = subprocess.run(
            ['gcloud', 'auth', 'print-access-token'],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False


def get_project_number():
    """Get project number from gcloud"""
    try:
        # Get current project ID
        result = subprocess.run(
            ['gcloud', 'config', 'get-value', 'project'],
            capture_output=True,
            text=True,
            check=True
        )
        project_id = result.stdout.strip()

        if not project_id:
            return None, None

        # Get project number from project ID
        result = subprocess.run(
            ['gcloud', 'projects', 'describe', project_id, '--format=value(projectNumber)'],
            capture_output=True,
            text=True,
            check=True
        )
        project_number = result.stdout.strip()

        return project_id, project_number
    except:
        return None, None


def load_env():
    """Load existing .env file"""
    env_vars = {}
    if ENV_FILE.exists():
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, _, value = line.partition('=')
                    env_vars[key.strip()] = value.strip().strip('"\'')
    return env_vars


def save_env(env_vars):
    """Save environment variables to .env"""
    existing = load_env()
    existing.update(env_vars)

    with open(ENV_FILE, 'w') as f:
        for key, value in sorted(existing.items()):
            f.write(f'{key}={value}\n')

    print(f"Configuration saved to {ENV_FILE}")


def test_connection(project_number, location, endpoint_location):
    """Test API connection"""
    try:
        import requests

        result = subprocess.run(
            ['gcloud', 'auth', 'print-access-token'],
            capture_output=True,
            text=True,
            check=True
        )
        token = result.stdout.strip()

        prefix = f"{endpoint_location}-" if endpoint_location != 'global' else 'global-'
        url = f"https://{prefix}discoveryengine.googleapis.com/v1alpha/projects/{project_number}/locations/{location}/notebooks:listRecentlyViewed"

        response = requests.get(
            url,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            },
            timeout=30
        )

        return response.status_code == 200, response.status_code, response.text[:200]

    except Exception as e:
        return False, 0, str(e)


def main():
    print_banner()

    # Step 1: Check gcloud CLI
    print("Step 1: Checking Google Cloud SDK...")
    if not check_gcloud():
        print()
        print("ERROR: Google Cloud SDK (gcloud) is not installed.")
        print()
        print("Please install it from:")
        print("  https://cloud.google.com/sdk/docs/install")
        print()
        print("After installation, run: gcloud init")
        sys.exit(1)
    print("  gcloud CLI found")

    # Step 2: Check authentication
    print()
    print("Step 2: Checking authentication...")
    if not check_gcloud_auth():
        print()
        print("You need to authenticate with Google Cloud.")
        print("Running: gcloud auth login")
        print()
        subprocess.run(['gcloud', 'auth', 'login'])

        if not check_gcloud_auth():
            print("ERROR: Authentication failed.")
            sys.exit(1)
    print("  Authenticated with Google Cloud")

    # Step 3: Get project configuration
    print()
    print("Step 3: Configuring project...")

    project_id, project_number = get_project_number()

    if project_id:
        print(f"  Current project: {project_id}")
        print(f"  Project number: {project_number}")
        use_current = input("  Use this project? [Y/n]: ").strip().lower()
        if use_current == 'n':
            project_number = None
    else:
        print("  No project configured in gcloud")

    if not project_number:
        print()
        print("Enter your Google Cloud project number.")
        print("(Find it at: https://console.cloud.google.com/home/dashboard)")
        project_number = input("Project number: ").strip()

    if not project_number:
        print("ERROR: Project number is required.")
        sys.exit(1)

    # Step 4: Configure location
    print()
    print("Step 4: Configuring location...")
    print("  Options: global (default), us, eu")
    location = input("  Location [global]: ").strip() or "global"
    endpoint_location = input("  Endpoint location [global]: ").strip() or "global"

    # Step 5: Test connection
    print()
    print("Step 5: Testing API connection...")
    success, status_code, message = test_connection(project_number, location, endpoint_location)

    if success:
        print("  Connection successful!")
    else:
        print(f"  Connection failed (HTTP {status_code})")
        print(f"  Message: {message}")
        print()
        if status_code == 403:
            print("  Make sure NotebookLM Enterprise API is enabled:")
            print("  https://console.cloud.google.com/apis/library")
        print()
        proceed = input("  Save configuration anyway? [y/N]: ").strip().lower()
        if proceed != 'y':
            print("Setup cancelled.")
            sys.exit(1)

    # Step 6: Save configuration
    print()
    print("Step 6: Saving configuration...")
    save_env({
        "GOOGLE_CLOUD_PROJECT_NUMBER": project_number,
        "NOTEBOOKLM_LOCATION": location,
        "NOTEBOOKLM_ENDPOINT_LOCATION": endpoint_location
    })

    print()
    print("=" * 50)
    print("  Setup Complete!")
    print("=" * 50)
    print()
    print("You can now use NotebookLM commands:")
    print("  - 'create notebook'")
    print("  - 'add sources to notebook'")
    print("  - 'create audio overview'")
    print()


if __name__ == "__main__":
    main()
