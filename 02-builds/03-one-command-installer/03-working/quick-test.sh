#!/bin/bash
#
# Quick Mock Test for install.sh
# Tests installer logic WITHOUT actually installing anything
#

set -e

echo "🧪 Running quick mock tests for install.sh..."
echo ""

# Test 1: Syntax Check
echo "Test 1: Bash syntax validation..."
docker run --rm -v "$(pwd)/install.sh":/test/install.sh ubuntu:22.04 bash -n /test/install.sh
echo "✓ Syntax valid"
echo ""

# Test 2: Function Existence
echo "Test 2: Checking required functions..."
docker run --rm -v "$(pwd)/install.sh":/test/install.sh ubuntu:22.04 bash -c '
  functions=(
    "detect_platform"
    "check_tool"
    "install_claude_code"
    "install_uv"
    "install_git"
    "prompt_vscode"
    "clone_nexus"
    "show_summary"
    "main"
  )

  for func in "${functions[@]}"; do
    if grep -q "${func}()" /test/install.sh; then
      echo "  ✓ ${func}() found"
    else
      echo "  ✗ ${func}() missing"
      exit 1
    fi
  done
'
echo ""

# Test 3: Color Output Check
echo "Test 3: Checking color output functions..."
docker run --rm -v "$(pwd)/install.sh":/test/install.sh ubuntu:22.04 bash -c '
  if grep -q "RED=" /test/install.sh && grep -q "GREEN=" /test/install.sh; then
    echo "  ✓ Color variables defined"
  else
    echo "  ✗ Color variables missing"
    exit 1
  fi

  if grep -q "info()" /test/install.sh && grep -q "success()" /test/install.sh; then
    echo "  ✓ Output functions defined"
  else
    echo "  ✗ Output functions missing"
    exit 1
  fi
'
echo ""

# Test 4: Line Endings
echo "Test 4: Checking line endings (must be LF, not CRLF)..."
if file install.sh | grep -q "CRLF"; then
  echo "  ✗ CRLF line endings detected (Windows style)"
  echo "    Run: sed -i '' 's/\r$//' install.sh"
  exit 1
else
  echo "  ✓ LF line endings (Unix style)"
fi
echo ""

# Test 5: Executable Permission
echo "Test 5: Checking executable permission..."
if [ -x install.sh ]; then
  echo "  ✓ install.sh is executable"
else
  echo "  ⚠ install.sh is not executable"
  echo "    Run: chmod +x install.sh"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ All quick tests passed!"
echo ""
echo "Next steps:"
echo "  • Test on real Ubuntu: docker run -it ubuntu:22.04"
echo "  • Test on macOS: ./install.sh"
echo "  • Test on Windows: run install.ps1 in PowerShell"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
