#!/bin/bash
#
# Fast Integration Test
# Tests installer flow WITHOUT waiting for full downloads
#

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚡ FAST TEST: install.sh logic"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create minimal test container
docker run --rm -v "$(pwd)/install.sh":/test/install.sh ubuntu:22.04 bash -c '
set -e

echo "Test Environment: Ubuntu 22.04"
echo ""

# Install minimal deps for test
apt-get update -qq && apt-get install -y -qq curl git > /dev/null 2>&1

echo "1. Testing platform detection..."
source /test/install.sh

# Mock uname for test
detect_platform > /dev/null 2>&1
if [ "$PLATFORM" = "Linux" ]; then
  echo "   ✓ Platform detected: Linux"
else
  echo "   ✗ Platform detection failed"
  exit 1
fi

echo ""
echo "2. Testing tool check function..."

# Test with installed tool (git)
if check_tool git Git 2>&1 | grep -q "already installed"; then
  echo "   ✓ check_tool correctly detects installed tools"
else
  echo "   ✗ check_tool failed"
  exit 1
fi

# Test with non-installed tool
if check_tool nonexistent Test 2>&1 | grep -q "not installed"; then
  echo "   ✓ check_tool correctly detects missing tools"
else
  echo "   ✗ check_tool failed"
  exit 1
fi

echo ""
echo "3. Testing color output functions..."

# Test info function
if info "test message" 2>&1 | grep -q "test message"; then
  echo "   ✓ info() works"
else
  echo "   ✗ info() failed"
  exit 1
fi

# Test success function
if success "test success" 2>&1 | grep -q "test success"; then
  echo "   ✓ success() works"
else
  echo "   ✗ success() failed"
  exit 1
fi

echo ""
echo "4. Testing installer control flow..."

# Create mock curl that just logs calls
curl_orig=$(which curl)
cat > /tmp/mock-curl << "MOCK_EOF"
#!/bin/bash
echo "[MOCK CURL] $@" >&2
if [[ "$*" == *"claude.ai/install.sh"* ]]; then
  echo "#!/bin/bash"
  echo "echo \"Mock Claude Code installed\""
  echo "exit 0"
elif [[ "$*" == *"astral.sh/uv/install.sh"* ]]; then
  echo "#!/bin/bash"
  echo "echo \"Mock uv installed\""
  echo "exit 0"
else
  $curl_orig "$@"
fi
MOCK_EOF
chmod +x /tmp/mock-curl

# Temporarily use mock curl
export PATH="/tmp:$PATH"

# Test install functions (dry run with mock)
echo "   Testing install_claude_code..."
if install_claude_code 2>&1 | grep -qE "(already installed|Mock Claude|installed successfully)"; then
  echo "   ✓ install_claude_code() executes"
else
  echo "   ✗ install_claude_code() failed"
  exit 1
fi

echo "   Testing install_uv..."
if install_uv 2>&1 | grep -qE "(already installed|Mock uv|installed successfully)"; then
  echo "   ✓ install_uv() executes"
else
  echo "   ✗ install_uv() failed"
  exit 1
fi

echo "   Testing install_git..."
if install_git 2>&1 | grep -qE "(already installed|installed successfully)"; then
  echo "   ✓ install_git() executes"
else
  echo "   ✗ install_git() failed"
  exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All fast tests passed!"
echo ""
echo "Tested:"
echo "  ✓ Platform detection"
echo "  ✓ Tool checking logic"
echo "  ✓ Color output functions"
echo "  ✓ Installation functions"
echo ""
echo "For FULL integration test (actual installations):"
echo "  Run: docker run --rm -it nexus-installer-integration-test"
echo "  (Takes 3-5 minutes)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
'
