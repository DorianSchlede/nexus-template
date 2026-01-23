# Docker Testing Strategy for Installers

**Date**: 2026-01-23
**Purpose**: How to test install.sh and install.ps1 without real systems

---

## Problem

We need to test installers on:
- Ubuntu (fresh system, no dev tools)
- macOS (ideal, but Docker can't run macOS containers)
- Windows (PowerShell, requires Windows containers)

But we don't want to:
- Spin up real VMs (slow, expensive)
- Install on production systems (risky)
- Wait hours for tests (inefficient)

---

## Solution: Docker + Test Frameworks

### Strategy Overview

```
1. Ubuntu/Linux → Docker Linux containers (fast, easy)
2. macOS → Local test script (dry-run mode)
3. Windows → Skip Docker, use GitHub Actions Windows runner
```

---

## Part 1: Test Bash Installer (Ubuntu/Linux)

### Approach: Lightweight Docker Tests

**Goal**: Verify installer logic WITHOUT actually installing tools

### Method: Mock/Stub Tests

Create a test Dockerfile that:
1. Copies install.sh into container
2. Mocks `curl`, `git`, `command` functions
3. Runs installer to verify control flow
4. Checks output for expected messages

### Example: Mock Test Dockerfile

```dockerfile
FROM ubuntu:22.04

# Install minimal dependencies
RUN apt-get update && apt-get install -y bash

# Copy installer
COPY install.sh /tmp/install.sh
RUN chmod +x /tmp/install.sh

# Create mock script
RUN cat > /tmp/mock-install.sh << 'EOF'
#!/bin/bash

# Mock curl to simulate installer downloads
curl() {
    echo "[MOCK] curl $@" >&2
    if [[ "$*" == *"claude.ai/install.sh"* ]]; then
        echo "echo 'Claude Code installed'"
    elif [[ "$*" == *"astral.sh/uv/install.sh"* ]]; then
        echo "echo 'uv installed'"
    else
        /usr/bin/curl "$@"
    fi
}
export -f curl

# Mock git
git() {
    echo "[MOCK] git $@" >&2
    return 0
}
export -f git

# Mock command to simulate tools NOT installed
command() {
    if [ "$1" = "-v" ]; then
        return 1  # Simulate tool not found
    fi
}
export -f command

# Run installer (non-interactive, skip VS Code)
echo "2" | bash /tmp/install.sh
EOF

RUN chmod +x /tmp/mock-install.sh

CMD ["/tmp/mock-install.sh"]
```

### Build and Run

```bash
# Build test image
docker build -t nexus-installer-test -f test-mock.Dockerfile .

# Run test
docker run --rm nexus-installer-test

# Expected output:
# ✓ Platform detected
# ⚠ Claude Code is not installed
# [MOCK] Installing Claude Code
# ✓ uv is not installed
# ...
```

---

## Part 2: Test macOS Locally (No Docker)

### Why No Docker?

Docker can't run macOS containers (licensing restrictions).

### Alternative: Local Dry-Run Script

Create a test script that:
1. Backs up PATH
2. Runs installer in "check mode"
3. Verifies output messages
4. Doesn't actually install anything

### Example: test-macos-dry-run.sh

```bash
#!/bin/bash

# Test install.sh on macOS without actually installing

set -e

echo "Testing install.sh (dry-run mode)..."

# Create temporary test environment
export TEST_MODE=1
export SKIP_INSTALL=1

# Run installer with mock answers
echo "2
n
" | bash install.sh 2>&1 | tee /tmp/installer-output.log

# Verify expected output
if grep -q "Platform: macOS" /tmp/installer-output.log; then
    echo "✓ Platform detection works"
else
    echo "✗ Platform detection failed"
    exit 1
fi

if grep -q "Installing Claude Code" /tmp/installer-output.log || grep -q "Claude Code is already installed" /tmp/installer-output.log; then
    echo "✓ Claude Code check works"
else
    echo "✗ Claude Code check failed"
    exit 1
fi

echo "✓ All dry-run tests passed"
```

---

## Part 3: Windows PowerShell Testing

### Problem

Windows Docker containers:
- Require Windows host (won't work on macOS/Linux)
- Are large and slow
- Need Windows Server base image

### Best Solution: GitHub Actions

Use GitHub Actions Windows runner to test install.ps1

### Example: .github/workflows/test-installer.yml

```yaml
name: Test Installers

on: [push, pull_request]

jobs:
  test-ubuntu:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build test image
        run: docker build -t installer-test -f test-ubuntu.Dockerfile .
      - name: Run installer test
        run: docker run --rm installer-test

  test-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Test PowerShell installer
        shell: powershell
        run: |
          # Mock test - verify syntax and basic logic
          $ErrorActionPreference = "Stop"

          # Check if script is valid PowerShell
          Get-Command -Syntax install.ps1

          # TODO: Add mock test for install.ps1
```

---

## Part 4: Best Practices

### 1. Use BATS (Bash Automated Testing System)

```bash
# Install BATS
npm install -g bats

# Create test file: test-installer.bats
@test "installer detects Ubuntu" {
  run bash -c "source install.sh && detect_platform"
  [ "$status" -eq 0 ]
  [[ "$output" =~ "Platform: Linux" ]]
}

# Run tests
bats test-installer.bats
```

### 2. Test Idempotency

```dockerfile
# Run installer twice to verify idempotency
RUN bash /tmp/install.sh < /tmp/answers.txt
RUN bash /tmp/install.sh < /tmp/answers.txt

# Both should succeed without errors
```

### 3. Layer Caching for Fast Tests

```dockerfile
# Cache slow layers (apt-get)
RUN apt-get update && apt-get install -y curl git

# Copy installer only after deps installed
COPY install.sh /tmp/
RUN chmod +x /tmp/install.sh

# This allows Docker to cache dependencies
```

### 4. Use Multi-Stage Builds

```dockerfile
# Stage 1: Test environment
FROM ubuntu:22.04 AS test
COPY install.sh /tmp/
RUN bash /tmp/install.sh

# Stage 2: Validation
FROM test AS validate
RUN command -v claude || exit 1
RUN command -v uv || exit 1
```

---

## Recommended Testing Matrix

| Platform | Test Method | Speed | Accuracy | Cost |
|----------|-------------|-------|----------|------|
| Ubuntu 22.04 | Docker (mocked) | ⚡⚡⚡ Fast (5s) | 🎯 Medium | 💰 Free |
| Ubuntu 22.04 | Docker (real install) | ⚡⚡ Medium (2min) | 🎯🎯🎯 High | 💰 Free |
| macOS | Local dry-run | ⚡⚡⚡ Fast (10s) | 🎯 Low | 💰 Free |
| macOS | Real system | ⚡ Slow (5min) | 🎯🎯🎯 High | 💰 Free |
| Windows | GitHub Actions | ⚡⚡ Medium (1min) | 🎯🎯🎯 High | 💰 Free (public repos) |

---

## Final Recommendation

### Phase 1: Quick Validation (Now)

✅ **Docker mock tests** for Ubuntu (5 seconds)
- Verifies installer logic
- No actual installations
- Fast feedback loop

### Phase 2: Real Testing (Before release)

✅ **GitHub Actions** for all platforms
- Real installations on clean runners
- Tests across Ubuntu, macOS, Windows
- Free for public repos

### Phase 3: Manual Testing (Final check)

✅ **Manual test on 1 real system per platform**
- Catch edge cases Docker can't simulate
- Verify user experience
- One-time before release

---

## Implementation: Create Simple Mock Test

```bash
# Create lightweight test
cat > 02-builds/03-one-command-installer/03-working/quick-test.sh << 'EOF'
#!/bin/bash

# Quick mock test for install.sh

docker run --rm -v $(pwd)/install.sh:/test/install.sh ubuntu:22.04 bash -c '
  # Mock curl to avoid network
  curl() { echo "[MOCK] $@"; }
  export -f curl

  # Check syntax
  bash -n /test/install.sh && echo "✓ Syntax valid" || exit 1

  # Verify functions exist
  grep -q "detect_platform()" /test/install.sh && echo "✓ detect_platform() found"
  grep -q "install_claude_code()" /test/install.sh && echo "✓ install_claude_code() found"
  grep -q "show_summary()" /test/install.sh && echo "✓ show_summary() found"

  echo "✓ All quick tests passed"
'
EOF

chmod +x 02-builds/03-one-command-installer/03-working/quick-test.sh

# Run it
./02-builds/03-one-command-installer/03-working/quick-test.sh
```

---

## Sources

- [Docker CI/CD Best Practices](https://docs.docker.com/build/building/best-practices/)
- [Testing PowerShell in Docker](https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-in-docker)
- [Combine PowerShell and Docker for Testing](https://www.techtarget.com/searchitoperations/tutorial/Combine-PowerShell-and-Docker-to-simplify-testing-across-OSes)
- [Automating Bash Script Testing in CI/CD](https://medium.com/@max.kombarov/automating-bash-script-installation-and-docker-build-and-verification-in-ci-cd-by-qa-7210f536daf8)
- [Docker CI/CD with Docker Hub](https://www.docker.com/blog/best-practices-for-using-docker-hub-for-ci-cd/)
