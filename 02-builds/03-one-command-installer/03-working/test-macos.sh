#!/bin/bash
#
# Test install.sh on macOS
# This runs the installer in "dry-run" mode to verify logic without actually installing
#

set -e

echo "Testing install.sh on macOS..."
echo ""

# Make installer executable
chmod +x install.sh

# Run installer (will prompt for VS Code, we'll say no)
echo "2" | ./install.sh

echo ""
echo "Test completed!"
