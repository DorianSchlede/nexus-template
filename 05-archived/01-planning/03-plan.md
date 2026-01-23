# One-Command Installer - Plan

**Build Type**: Build
**Status**: Planning

---

## Context

**Load Before Reading**:
- [01-planning/02-discovery.md](02-discovery.md) - Requirements and dependencies

---

## Approach

**Strategy**: Create two separate installer scripts (bash + PowerShell) that chain official installers and handle platform-specific edge cases.

**Flow**:
```
User runs curl/irm command
    ↓
Script downloads and runs
    ↓
1. Platform Detection (macOS/Linux/Windows)
2. Check Prerequisites (claude, uv, git)
3. Install Missing Tools (via official installers)
4. Verify PATH (warn if restart needed)
5. Interactive VS Code Prompt
6. Clone Nexus Template
7. Open VS Code (if installed)
8. Display Summary + Next Steps
```

**Key Insight from Pre-Mortem**: Most failures come from PATH not refreshing. Script MUST warn users to restart terminal after installations.

---

## Success Criteria (from Mental Models)

**Pre-Mortem Applied**: "Imagine the installer is live and fails catastrophically. What happened?"

- [ ] Script runs successfully on fresh macOS (no dev tools)
- [ ] Script runs successfully on fresh Linux (no dev tools)
- [ ] Script runs successfully on fresh Windows (PowerShell)
- [ ] Script detects existing tools and skips re-installation
- [ ] User is warned about terminal restart when PATH changes
- [ ] Idempotent - safe to run multiple times
- [ ] Clear error messages for all failure modes
- [ ] Git Bash available on Windows after completion
- [ ] Nexus repo cloned and VS Code opened (if user confirmed)

---

## Risks & Mitigations (from Pre-Mortem)

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| PATH not updated after install | High | Critical | Display "⚠️ RESTART TERMINAL" warning prominently |
| Git Bash missing on Windows | Medium | Critical | Auto-install Git for Windows via winget/chocolatey |
| PowerShell execution policy blocks script | Medium | High | Add `-ExecutionPolicy Bypass` to irm command in docs |
| User runs script multiple times | Medium | Low | Add checks for existing installations before installing |
| VS Code `code` command not in PATH | Medium | Low | Test for `code` command, guide user to add manually |

---

## Key Decisions

| Decision | Choice | Rationale | Validates |
|----------|--------|-----------|-----------|
| File hosting | GitHub Raw URL | Free, reliable, no infra needed | REQ-NF-2 |
| File location | Repo root (install.sh, install.ps1) | Easy to reference, standard location | REQ-NF-2 |
| Git Windows install | winget or chocolatey | Native Windows package managers, silent install | REQ-4 |
| VS Code detection | Ask user, not auto-detect | Too many IDEs/paths, simpler to ask | REQ-5 |
| **PATH handling** | **Warn + provide both options** | **Following Homebrew/Rust pattern: offer `source` for speed OR restart for reliability** | **REQ-8** |
| Nexus clone timing | After tools installed, before restart warning | Installer is idempotent - user can re-run if PATH not refreshed | REQ-6 |

### PATH Update Strategy (Critical Decision)

**Problem**: After installing Claude/uv/Git, current terminal session doesn't see updated PATH.

**Solution** (following industry best practices from Homebrew, Rust):

```bash
# After each tool installation:
if ! command -v <tool> &> /dev/null; then
    PATH_UPDATED=true
fi

# At the end, if PATH_UPDATED:
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  PATH was updated during installation"
echo ""
echo "Choose one option to apply changes:"
echo "  1. Quick (current session only):"
echo "     source ~/.zshrc   # or ~/.bashrc"
echo ""
echo "  2. Reliable (all sessions):"
echo "     Restart your terminal"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Why this approach:**
- **User choice**: Some prefer speed (`source`), others prefer reliability (restart)
- **Industry standard**: Homebrew, Rust, Node installers all do this
- **Works with idempotency**: User can re-run installer after restart if needed
- **No magic**: Transparent about what's happening

**Sources**: [Homebrew Installation Docs](https://docs.brew.sh/Installation), [Rust Install Guide](https://rust-lang.org/tools/install/)

---

## Dependencies & Links

*From [02-discovery.md](02-discovery.md)*

**Files to Modify**:
| File | Changes | Validates |
|------|---------|-----------|
| README.md | Add one-command install at top | REQ-NF-2 |

**Files to Create**:
| File | Purpose | Validates |
|------|---------|-----------|
| install.sh | Bash installer (macOS/Linux/WSL) | REQ-1, REQ-2, REQ-3 |
| install.ps1 | PowerShell installer (Windows) | REQ-1, REQ-2, REQ-3 |

**External Systems**:
- **claude.ai/install.sh** - Official Claude Code bash installer
- **claude.ai/install.ps1** - Official Claude Code PowerShell installer
- **astral.sh/uv/install.sh** - uv bash installer
- **astral.sh/uv/install.ps1** - uv PowerShell installer
- **winget** - Windows package manager for Git
- **raw.githubusercontent.com** - Hosting for install scripts

---

## Testing Strategy

**Manual Testing Required** (no automated tests for installers):

| Platform | Test Scenario | Expected Outcome |
|----------|---------------|------------------|
| macOS (fresh) | Run install.sh on system with no dev tools | All tools install, Nexus cloned, VS Code opens |
| macOS (existing) | Run install.sh with Claude/uv already installed | Script skips existing, installs missing only |
| Linux (Ubuntu) | Run install.sh on fresh Ubuntu | All tools install correctly |
| Windows (PowerShell) | Run install.ps1 on fresh Windows | Git+Claude+uv install, Nexus cloned |
| Windows (WSL) | Run install.sh in WSL | Works like Linux |
| All platforms | Run script twice | Idempotent - no errors, skips installed tools |

---

## Open Questions

| Question | Resolution | Validates |
|----------|------------|-----------|
| Git for Windows silent install command | Use `winget install Git.Git` | REQ-4 |
| VS Code detection method | Ask user, don't auto-detect | REQ-5 |
| How to handle PowerShell execution policy | Document `-ExecutionPolicy Bypass` in README | REQ-NF-2 |

---

*Execution steps in 04-steps.md*
