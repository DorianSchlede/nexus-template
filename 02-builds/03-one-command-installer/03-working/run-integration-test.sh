#!/bin/bash
#
# Integration Test Runner
# Actually runs install.sh in a fresh Ubuntu container
#

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 INTEGRATION TEST: install.sh on Ubuntu 22.04"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "This test will:"
echo "  1. Create a fresh Ubuntu 22.04 container"
echo "  2. Install ONLY curl (simulating fresh system)"
echo "  3. Run install.sh with automated inputs"
echo "  4. Verify Claude Code, uv, and Git are installed"
echo ""
echo "Expected duration: 2-3 minutes"
echo ""

read -p "Continue? (y/N): " confirm
if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
    echo "Test cancelled."
    exit 0
fi

echo ""
echo "Building test image..."
docker build -t nexus-installer-integration-test \
    -f 02-builds/03-one-command-installer/03-working/integration-test.Dockerfile .

echo ""
echo "Running installer in container..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
docker run --rm -it nexus-installer-integration-test

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Integration test completed!"
echo ""
echo "To test idempotency (run installer twice):"
echo "  docker run --rm -it nexus-installer-integration-test"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
