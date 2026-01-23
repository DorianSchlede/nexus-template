# One-Command Installer - Execution Steps

**Build Type**: Build
**Status**: Planning

---

## Context Requirements

**Build Location**: `02-builds/03-one-command-installer/`

**Files to Load for Execution**:
- [01-planning/02-discovery.md](02-discovery.md) - Requirements
- [01-planning/03-plan.md](03-plan.md) - Approach and decisions

**Output Location**: Repo root for install.sh and install.ps1

**Update Resume After Each Section**: Update `resume-context.md` with current_section, tasks_completed

---

## Phase 1: Research & Verification

**Goal**: Verify external installer endpoints work
**Context**: Load [02-discovery.md](02-discovery.md)

- [x] Test Claude Code install endpoints (bash + PowerShell) **[REQ-3]**
- [x] Test uv install endpoints (bash + PowerShell) **[REQ-3]**
- [x] Research Git for Windows silent install (winget command) **[REQ-4]**
- [x] **CHECKPOINT**: All official installers accessible and working

**Results**: See [02-resources/installer-endpoints-verification.md](../02-resources/installer-endpoints-verification.md)

---

## Phase 2: Bash Installer (install.sh)

**Goal**: Create macOS/Linux/WSL/Git Bash installer
**Context**: Load [03-plan.md](03-plan.md) approach section

### 2.1 Detection & Checks **[REQ-1, REQ-2]**

- [x] Add platform detection (uname for macOS vs Linux)
- [x] Add tool existence checks (which claude, which uv, which git)
- [x] Add colored output functions (success/warning/error messages)
- [x] **CHECKPOINT**: Script detects platform and existing tools correctly

### 2.2 Tool Installation **[REQ-3, REQ-4]**

- [x] Add Claude Code installation (curl official installer)
- [x] Add uv installation (curl official installer)
- [x] Add Git installation (Linux package manager: apt/yum)
- [x] Add PATH verification after each install **[REQ-8]**
- [x] Add terminal restart warning if PATH changed **[REQ-9]**

### 2.3 Post-Install Steps **[REQ-5, REQ-6, REQ-7]**

- [x] Add interactive VS Code prompt
- [x] Add Nexus clone step (prompt for directory)
- [x] Add VS Code launch (if installed and user confirmed)
- [x] Add installation summary display **[REQ-10]**
- [x] Fix CRLF line ending issue (convert to LF)

---

## Phase 3: PowerShell Installer (install.ps1)

**Goal**: Create Windows PowerShell installer
**Context**: Same logic as bash, different syntax

### 3.1 Detection & Checks **[REQ-1, REQ-2]**

- [x] Add Windows detection and version check
- [x] Add tool existence checks (Get-Command)
- [x] Add colored output functions (Write-Host -ForegroundColor)
- [x] **CHECKPOINT**: Script detects existing tools on Windows

### 3.2 Tool Installation **[REQ-3, REQ-4]**

- [x] Add Claude Code installation (irm official installer)
- [x] Add uv installation (irm official installer)
- [x] Add Git for Windows installation (winget install Git.Git) **[REQ-4]**
- [x] Add PATH verification (refreshenv or warn user)
- [x] Add terminal restart warning

### 3.3 Post-Install Steps **[REQ-5, REQ-6, REQ-7]**

- [x] Add VS Code prompt (Read-Host)
- [x] Add Nexus clone (git clone with directory prompt)
- [x] Add VS Code launch (Start-Process code)
- [x] Add installation summary

---

## Phase 4: Testing

**Goal**: Verify installers work on all platforms
**Context**: Scripts complete

- [ ] Test install.sh on macOS (fresh system) **[REQ-NF-1]**
- [ ] Test install.sh on Linux (fresh Ubuntu) **[REQ-NF-1]**
- [ ] Test install.ps1 on Windows (fresh system) **[REQ-NF-1]**
- [ ] Test idempotency (run twice, no errors) **[REQ-NF-3]**
- [ ] **CHECKPOINT**: All platforms working

---

## Phase 5: Documentation

**Goal**: Update README with one-command install
**Context**: Scripts tested and working

- [x] Add "Quick Install" section to README top
- [x] Add curl command for macOS/Linux
- [x] Add irm command for Windows
- [x] Add system requirements (Windows 10 1809+)
- [x] Move old installation to collapsible "Manual Installation"
- [x] Create GitHub Actions workflow (.github/workflows/test-installers.yml)
- [x] Update resume-context.md: current_phase: "complete"
- [x] Update 01-overview.md: status: "COMPLETE"

---

## Summary

| Phase | Tasks | Checkpoints |
|-------|-------|-------------|
| Phase 1: Research | 4 | 1 |
| Phase 2: Bash Installer | 12 | 2 |
| Phase 3: PowerShell Installer | 11 | 1 |
| Phase 4: Testing | 5 | 1 |
| Phase 5: Documentation | 5 | 0 |
| **Total** | **37** | **5** |

---

*Mark tasks complete with [x] as you finish them*
*Optional tasks marked with `*` can be skipped for faster MVP*
