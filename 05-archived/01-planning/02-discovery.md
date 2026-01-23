# One-Command Installer - Discovery

**Build Type**: Build
**Purpose**: Create unified curl/PowerShell installer for Nexus that works across all platforms with zero coding tools

---

## Requirements (EARS Format)

*All requirements MUST follow EARS patterns. See references/ears-patterns.md for templates.*

### Functional Requirements

**REQ-1 (Platform Detection)**: WHEN the installer script is executed, THE system SHALL detect the operating system (macOS/Linux/Windows) and shell environment (bash/PowerShell/WSL/Git Bash).

**REQ-2 (Smart Prerequisites Check)**: THE installer SHALL check for existing installations of Claude Code, uv, and Git (Windows only) before attempting any installations.

**REQ-3 (Selective Installation)**: WHEN a required tool is missing, THE installer SHALL download and install only the missing component using the official installation method for that platform.

**REQ-4 (Windows Git Bash Requirement)**: WHEN the system is Windows AND Git is not installed, THE installer SHALL install Git for Windows to provide Git Bash for Claude Code hooks.

**REQ-5 (Interactive VS Code Prompt)**: AFTER all prerequisites are installed, THE installer SHALL ask the user "Do you want to install VS Code?" and proceed based on user input (yes/no).

**REQ-6 (Nexus Clone)**: AFTER prerequisites installation, THE installer SHALL prompt for a target directory and clone the Nexus template repository to that location.

**REQ-7 (VS Code Launch)**: WHEN Nexus cloning is complete AND VS Code is installed, THE installer SHALL open VS Code with the cloned Nexus directory.

**REQ-8 (Path Verification)**: AFTER each tool installation, THE installer SHALL verify the tool is accessible in PATH before proceeding to next step.

**REQ-9 (Error Handling)**: IF any installation step fails, THE installer SHALL display a clear error message with troubleshooting steps and exit gracefully.

**REQ-10 (Installation Summary)**: WHEN all steps complete, THE installer SHALL display a summary showing what was installed, what was skipped, and next steps.

### Non-Functional Requirements

**REQ-NF-1 (Zero Dependencies)**: THE installer SHALL run on systems with ONLY curl (macOS/Linux) or PowerShell (Windows) pre-installed, with no other developer tools required.

**REQ-NF-2 (Single Command)**: THE installer SHALL be executable via a single curl/PowerShell command that users can copy-paste into terminal.

**REQ-NF-3 (Idempotency)**: THE installer SHALL be safe to run multiple times without corrupting existing installations or configurations.

**REQ-NF-4 (Clear Progress)**: THE installer SHALL display clear progress indicators for each step (checking, downloading, installing, verifying).

**REQ-NF-5 (User Confirmation)**: THE installer SHALL require explicit user confirmation before making any system changes (installations, PATH modifications).

### Quality Checklist (INCOSE)

*Verify each requirement meets INCOSE quality rules:*

- [ ] All requirements use EARS patterns (THE/WHEN/WHILE/IF/WHERE)
- [ ] No vague terms (quickly, adequate, reasonable, user-friendly)
- [ ] No pronouns (it, them, they) - specific names used
- [ ] Each requirement independently testable
- [ ] Active voice throughout
- [ ] No escape clauses (where possible, if feasible)
- [ ] Solution-free (what, not how)

---

## Dependencies

*Files, systems, APIs this build will touch*

### Files to Modify

| File | Changes Needed |
|------|----------------|
| README.md | Add one-command install section at top, replace multi-step installation instructions |

### Files to Create

| File | Purpose |
|------|---------|
| install.sh | Bash installer for macOS/Linux/WSL/Git Bash (curl-downloadable) |
| install.ps1 | PowerShell installer for Windows (irm-downloadable) |
| 04-outputs/install-docs.md | Documentation of installer behavior, troubleshooting, edge cases |

### External Systems

- **Claude AI install endpoint** (https://claude.ai/install.sh): Official Claude Code installer for Unix systems
- **Claude AI PowerShell endpoint** (https://claude.ai/install.ps1): Official Claude Code installer for Windows
- **astral.sh/uv/install.sh**: Official uv installer for Unix
- **astral.sh/uv/install.ps1**: Official uv installer for Windows
- **git-scm.com**: Git for Windows download (may need direct download URL or winget)
- **GitHub API** (optional): To check latest Nexus template version
- **Nexus Template Repo** (https://github.com/DorianSchlede/nexus-template): Source to clone

---

## Existing Patterns

*Skills, templates, code to reuse*

| Pattern | Location | Reuse Strategy |
|---------|----------|----------------|
| Official installers | Claude AI, astral.sh endpoints | Chain existing installers rather than rewriting installation logic |
| Bash detection patterns | Common Unix scripts | Use `uname` for OS detection, `which` for tool checks |
| PowerShell module patterns | Microsoft docs | Use `Get-Command` for tool checks, `Test-Path` for file verification |
| Git Bash detection | Windows env var `PROGRAMFILES` | Check for Git Bash in standard Windows install locations |

---

## Risks & Unknowns

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| GitHub Raw URL rate limiting | Low | Medium | Add fallback to GitHub Releases, document issue |
| Windows PATH not updated after uv install | Medium | High | Require terminal restart, add PATH verification step |
| Git for Windows silent install fails | Low | High | Provide manual download link as fallback |
| User has incompatible shell on Windows | Low | Medium | Detect and recommend Git Bash/WSL |
| VS Code not in PATH after install | Medium | Low | Use `code` command with full path verification |

### Open Questions

- [x] **Hosting location** → GitHub Raw URL (raw.githubusercontent.com)
- [x] **File location in repo** → Root directory (install.sh, install.ps1)
- [ ] **Git for Windows silent install command** → Research winget vs direct .exe download
- [ ] **VS Code silent install command** → Check if `code` CLI works across all platforms
- [ ] **How to detect VS Code installation** → Check common install paths vs ask user

---

*This discovery document is MANDATORY. It preserves intelligence across compaction.*
*Auto-populate 03-plan.md Dependencies section from findings above.*
