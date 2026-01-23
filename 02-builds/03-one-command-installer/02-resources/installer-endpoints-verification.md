# Installer Endpoints Verification

**Date**: 2026-01-23
**Phase**: Phase 1 - Research & Verification

---

## Claude Code Installers

### Bash Installer
- **URL**: `https://claude.ai/install.sh`
- **Status**: ✅ Working
- **Redirects to**: `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/bootstrap.sh`
- **Usage**: `curl -fsSL https://claude.ai/install.sh | bash`
- **Features**:
  - Supports `stable`, `latest`, or specific version as argument
  - Works with both `curl` and `wget`
  - Downloads to `~/.claude/downloads`

### PowerShell Installer
- **URL**: `https://claude.ai/install.ps1`
- **Status**: ✅ Working
- **Redirects to**: `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/bootstrap.ps1`
- **Usage**: `irm https://claude.ai/install.ps1 | iex`
- **Features**:
  - x64 only (no 32-bit support)
  - ARM64 Windows supported via x64 emulation
  - Downloads to `$env:USERPROFILE\.claude\downloads`

---

## uv Installers

### Bash Installer
- **URL**: `https://astral.sh/uv/install.sh`
- **Status**: ✅ Working
- **Redirects to**: `https://github.com/astral-sh/uv/releases/latest/download/uv-installer.sh`
- **Usage**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Current Version**: 0.9.26
- **Install Locations** (priority order):
  1. `$XDG_BIN_HOME`
  2. `$XDG_DATA_HOME/../bin`
  3. `$HOME/.local/bin`

### PowerShell Installer
- **URL**: `https://astral.sh/uv/install.ps1`
- **Status**: ✅ Working
- **Redirects to**: `https://github.com/astral-sh/uv/releases/latest/download/uv-installer.ps1`
- **Usage**: `irm https://astral.sh/uv/install.ps1 | iex`
- **Current Version**: 0.9.26
- **Features**:
  - Adds to PATH via Environment.Path registry key
  - Optional `-NoModifyPath` parameter

---

## Git for Windows

### Installation Method
- **Tool**: `winget` (Windows Package Manager)
- **Package ID**: `Git.Git`
- **Command**: `winget install --id Git.Git -e --source winget --silent`
- **Status**: ✅ Verified (winget available on Windows 10+)

### Why Git Bash is Critical
- Claude Code hooks require bash environment on Windows
- Git for Windows includes Git Bash
- Alternative: WSL (but requires more setup)

### Fallback Options
If winget fails:
1. **Chocolatey**: `choco install git -y`
2. **Direct Download**: https://git-scm.com/download/win (requires manual install)

---

## Key Findings

### PATH Update Behavior

All installers modify PATH, but current terminal session doesn't see changes:

| Installer | PATH Modified | Requires Restart |
|-----------|---------------|------------------|
| Claude Code (bash) | ✅ ~/.zshrc or ~/.bashrc | Yes or `source` |
| Claude Code (PS1) | ✅ User PATH registry | Yes (new terminal) |
| uv (bash) | ✅ Shell config | Yes or `source` |
| uv (PS1) | ✅ User PATH registry | Yes (new terminal) |
| Git (winget) | ✅ System PATH | Yes (new terminal) |

**Implication**: Our installer MUST warn users to restart terminal or source config.

### Command Patterns

**Bash (macOS/Linux/WSL)**:
```bash
curl -fsSL https://claude.ai/install.sh | bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**PowerShell (Windows)**:
```powershell
irm https://claude.ai/install.ps1 | iex
irm https://astral.sh/uv/install.ps1 | iex
winget install --id Git.Git -e --silent
```

### Idempotency
- ✅ Claude Code installer: Checks for existing installation
- ✅ uv installer: Overwrites with latest (safe)
- ⚠️ Git via winget: Will skip if already installed

---

## Recommendations for Our Installer

1. **Chain Official Installers**: Don't reimplement - just call them
2. **Check Before Install**: Use `command -v` (bash) or `Get-Command` (PS1)
3. **PATH Warning**: Display prominent restart message after installations
4. **Error Handling**: Wrap each installer call in try/catch with clear error messages
5. **Silent Flags**: Use `--silent` for winget to avoid GUI prompts

---

## Next Steps

- [x] Verified all installer endpoints work
- [ ] Build bash installer (install.sh)
- [ ] Build PowerShell installer (install.ps1)
- [ ] Test on real systems
