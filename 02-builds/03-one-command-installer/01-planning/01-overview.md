---
id: 03-one-command-installer
name: One-Command Installer
status: COMPLETE
description: "Build: One-Command Installer"
created: 2026-01-23
completed: 2026-01-23
build_path: 02-builds/03-one-command-installer/
---

# One-Command Installer

## Build Files

| File | Purpose |
|------|---------|
| 01-overview.md | This file - purpose, success criteria |
| 02-discovery.md | Dependencies, patterns, risks |
| 03-plan.md | Approach, decisions |
| 04-steps.md | Execution tasks |
| 02-resources/ | Reference materials |
| 03-working/ | Work in progress |
| 04-outputs/ | Final deliverables |

---

## Purpose

Create unified one-command installers (bash + PowerShell) that install Claude Code, uv, Git, and Nexus template across all platforms with zero coding tools required.

---

## Success Criteria

**Must achieve**:
- [x] Bash installer (install.sh) created and tested on macOS
- [x] PowerShell installer (install.ps1) created and structurally validated
- [x] All 15 requirements (REQ-1 to REQ-NF-5) met
- [x] README.md updated with one-command installation instructions
- [x] Testing infrastructure created (quick-test.sh, integration tests)

**Nice to have**:
- [x] GitHub Actions CI/CD workflow for automated testing
- [x] Comprehensive documentation (testing guide, Windows instructions)
- [x] .gitattributes to prevent line-ending issues

---

## Context

**Background**: Nexus requires Claude Code, uv, and Git to function. Current installation requires users to manually install each tool separately following multi-step instructions, leading to setup friction and PATH issues.

**Stakeholders**: New Nexus users wanting quick setup, existing users helping others onboard

**Constraints**:
- Must work on systems with only curl (macOS/Linux) or PowerShell (Windows)
- Cannot require admin/sudo for basic functionality
- Must handle existing installations gracefully (idempotency)

---

## Deliverables

**Core Files**:
- ✅ [install.sh](../../../install.sh) - 445 lines, tested on macOS
- ✅ [install.ps1](../../../install.ps1) - 448 lines, structure validated
- ✅ [.gitattributes](../../../.gitattributes) - Line ending configuration

**Documentation**:
- ✅ [installer-implementation-summary.md](../04-outputs/installer-implementation-summary.md)
- ✅ [testing-guide.md](../04-outputs/testing-guide.md)
- ✅ [windows-test-instructions.md](../03-working/windows-test-instructions.md)
- ✅ [docker-testing-strategy.md](../02-resources/docker-testing-strategy.md)
- ✅ [windows-version-requirements.md](../02-resources/windows-version-requirements.md)
- ✅ [installer-endpoints-verification.md](../02-resources/installer-endpoints-verification.md)

**Testing**:
- ✅ [quick-test.sh](../03-working/quick-test.sh) - Syntax validation
- ✅ [integration-test.Dockerfile](../03-working/integration-test.Dockerfile)
- ✅ [.github/workflows/test-installers.yml](../../../.github/workflows/test-installers.yml) - CI/CD

---

*Build completed: 2026-01-23*
