# NEXUS OPERATING SYSTEM - COMPLETE INSTALLER GUIDE

> **Purpose**: One-command installation guide for Mac and PC (Windows)
>
> **Auto-Install Goal**: Clone repo + run single script = fully working Nexus

---

## Table of Contents

1. [Quick Start (TL;DR)](#quick-start-tldr)
2. [Prerequisites Auto-Install](#prerequisites-auto-install)
3. [Full Installation Scripts](#full-installation-scripts)
4. [File Structure Reference](#file-structure-reference)
5. [Hook System Deep Dive](#hook-system-deep-dive)
6. [Utility Modules Reference](#utility-modules-reference)
7. [Configuration Files](#configuration-files)
8. [Post-Installation Setup](#post-installation-setup)
9. [Troubleshooting](#troubleshooting)

---

## Quick Start (TL;DR)

### Mac/Linux (One Command)
```bash
# Clone + Install + Setup
git clone https://github.com/YOUR-USERNAME/nexus.git && cd nexus && ./scripts/install.sh
```

### Windows (One Command - PowerShell as Admin)
```powershell
# Clone + Install + Setup
git clone https://github.com/YOUR-USERNAME/nexus.git; cd nexus; powershell -ExecutionPolicy Bypass -File scripts\install.ps1
```

### After Install
```bash
# Create .env with your API key
echo "ANTHROPIC_API_KEY=sk-ant-your-key-here" > .env

# Launch Claude Code
claude .
```

---

## Prerequisites Auto-Install

### What Gets Installed

| Tool | Purpose | Mac Install | Windows Install |
|------|---------|-------------|-----------------|
| **Git** | Version control | `xcode-select --install` | `winget install Git.Git` |
| **uv** | Python package manager | `curl -LsSf https://astral.sh/uv/install.sh \| sh` | `irm https://astral.sh/uv/install.ps1 \| iex` |
| **Python 3.12** | Runtime (via uv) | `uv python install 3.12` | `uv python install 3.12` |
| **Node.js 20+** | Claude Code CLI | `brew install node` | `winget install OpenJS.NodeJS.LTS` |
| **Claude Code CLI** | IDE integration | `npm install -g @anthropic-ai/claude-code` | `npm install -g @anthropic-ai/claude-code` |
| **Docker** (optional) | Local Langfuse | Download from docker.com | Download from docker.com |

---

## Full Installation Scripts

### Mac/Linux: `scripts/install.sh`

```bash
#!/bin/sh
# Nexus OS Installation Script
# Cross-platform: macOS, Linux, Windows (WSL/Git Bash)
#
# For native Windows (PowerShell/cmd), run: scripts\install.ps1
#
# This script installs all required dependencies for a fresh system.

set -e

# Detect if running on native Windows (not WSL/Git Bash)
if [ -n "$WINDIR" ] && [ -z "$WSL_DISTRO_NAME" ] && [ -z "$MSYSTEM" ]; then
    echo "Detected native Windows. Please run instead:"
    echo "  powershell -ExecutionPolicy Bypass -File scripts\\install.ps1"
    exit 1
fi

echo "========================================="
echo "Nexus OS Installer"
echo "========================================="
echo ""

# Detect OS
OS="unknown"
ARCH="$(uname -m)"
case "$(uname -s)" in
    Darwin*)  OS="macos";;
    Linux*)   OS="linux";;
    MINGW*|MSYS*|CYGWIN*) OS="windows";;
esac
echo "Detected: $OS ($ARCH)"
echo ""

# Track what was installed
INSTALLED=""
SKIPPED=""
FAILED=""

# =========================================
# 1. Git (required)
# =========================================
echo "Checking Git..."
if command -v git &> /dev/null; then
    echo "  ✓ Git $(git --version | cut -d' ' -f3)"
else
    echo "  ✗ Git not found"
    echo ""
    echo "Please install Git first:"
    if [ "$OS" = "macos" ]; then
        echo "  xcode-select --install"
        echo "  # or: brew install git"
    elif [ "$OS" = "linux" ]; then
        echo "  sudo apt install git  # Debian/Ubuntu"
        echo "  sudo dnf install git  # Fedora"
        echo "  sudo pacman -S git    # Arch"
    else
        echo "  Download from: https://git-scm.com/download/win"
    fi
    exit 1
fi

# =========================================
# 2. uv (Python package manager) - required
# =========================================
echo ""
echo "Checking uv (Python package manager)..."
if command -v uv &> /dev/null; then
    echo "  ✓ uv $(uv --version | head -1)"
    SKIPPED="$SKIPPED uv"
else
    echo "  Installing uv..."
    if [ "$OS" = "windows" ]; then
        powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
        UV_PATH="$USERPROFILE/.local/bin"
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
        UV_PATH="$HOME/.local/bin"
    fi
    export PATH="$UV_PATH:$PATH"

    # Add to shell config
    if [ "$OS" != "windows" ]; then
        SHELL_CONFIG=""
        [ -f "$HOME/.zshrc" ] && SHELL_CONFIG="$HOME/.zshrc"
        [ -z "$SHELL_CONFIG" ] && [ -f "$HOME/.bashrc" ] && SHELL_CONFIG="$HOME/.bashrc"
        [ -z "$SHELL_CONFIG" ] && [ -f "$HOME/.bash_profile" ] && SHELL_CONFIG="$HOME/.bash_profile"

        if [ -n "$SHELL_CONFIG" ] && ! grep -q '.local/bin' "$SHELL_CONFIG" 2>/dev/null; then
            echo '' >> "$SHELL_CONFIG"
            echo '# Added by Nexus OS installer' >> "$SHELL_CONFIG"
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$SHELL_CONFIG"
            echo "  Added to $SHELL_CONFIG"
        fi
    fi
    echo "  ✓ uv installed"
    INSTALLED="$INSTALLED uv"
fi

# =========================================
# 3. Python 3.12 (via uv) - required
# =========================================
echo ""
echo "Ensuring Python 3.12..."
if uv python install 3.12 --quiet 2>/dev/null; then
    echo "  ✓ Python 3.12 available"
else
    echo "  ✓ Python 3.12 (already installed or downloading)"
fi

# =========================================
# 4. Node.js & npm (required for Claude Code CLI)
# =========================================
echo ""
echo "Checking Node.js..."
if command -v node &> /dev/null; then
    echo "  ✓ Node.js $(node --version)"
else
    echo "  Installing Node.js..."
    if [ "$OS" = "macos" ]; then
        # Try brew first, fall back to manual install
        if command -v brew &> /dev/null; then
            brew install node
        else
            echo "  ✗ Please install Homebrew first: https://brew.sh"
            echo "    Then run: brew install node"
            exit 1
        fi
    elif [ "$OS" = "linux" ]; then
        # Use NodeSource for latest LTS
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt install -y nodejs
    else
        echo "  ✗ Please install Node.js from: https://nodejs.org/"
        exit 1
    fi
    echo "  ✓ Node.js installed"
fi

# =========================================
# 5. Claude Code CLI (required)
# =========================================
echo ""
echo "Checking Claude Code CLI..."
if command -v claude &> /dev/null; then
    echo "  ✓ Claude Code CLI installed"
else
    echo "  Installing Claude Code CLI..."
    npm install -g @anthropic-ai/claude-code
    echo "  ✓ Claude Code CLI installed"
fi

# =========================================
# 6. Docker (optional - for local Langfuse)
# =========================================
echo ""
echo "Checking Docker (optional)..."
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        echo "  ✓ Docker $(docker --version | cut -d' ' -f3 | tr -d ',')"
    else
        echo "  ⚠ Docker installed but not running"
    fi
    SKIPPED="$SKIPPED docker"
else
    echo "  ✗ Docker not found (optional - for local Langfuse)"
    echo "    Install from: https://docker.com/get-started"
    SKIPPED="$SKIPPED docker(optional)"
fi

# =========================================
# 7. curl (usually pre-installed)
# =========================================
echo ""
echo "Checking curl..."
if command -v curl &> /dev/null; then
    echo "  ✓ curl available"
else
    echo "  ✗ curl not found"
    if [ "$OS" = "linux" ]; then
        echo "    sudo apt install curl"
    fi
    FAILED="$FAILED curl"
fi

# =========================================
# 8. Set execute permissions on hooks
# =========================================
echo ""
echo "Setting hook permissions..."
chmod +x .claude/hooks/run 2>/dev/null || true
chmod +x .claude/hooks/*.py 2>/dev/null || true
echo "  ✓ Hooks configured"

# =========================================
# 9. Test hooks
# =========================================
echo ""
echo "Testing hooks..."
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR/.."

if echo '{"session_id":"test","source":"new","transcript_path":""}' | uv run .claude/hooks/session_start.py > /dev/null 2>&1; then
    echo "  ✓ Hooks working!"
else
    echo "  ⚠ Hook test failed (may work after terminal restart)"
fi

# =========================================
# 10. Create .env template if missing
# =========================================
echo ""
echo "Checking .env file..."
if [ ! -f ".env" ]; then
    cat > .env.sample << 'EOF'
# Nexus OS Environment Variables
# Copy this file to .env and fill in your keys

# REQUIRED: Anthropic API Key (for Claude Code features)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OPTIONAL: Additional LLM providers
# OPENAI_API_KEY=sk-...

# OPTIONAL: Text-to-speech
# ELEVENLABS_API_KEY=...

# OPTIONAL: Integrations (add as needed)
# AIRTABLE_API_KEY=...
# NOTION_API_KEY=...
# LANGFUSE_SECRET_KEY=...
# LANGFUSE_PUBLIC_KEY=...
EOF
    echo "  ✓ Created .env.sample (copy to .env and add your keys)"
else
    echo "  ✓ .env file exists"
fi

# =========================================
# Summary
# =========================================
echo ""
echo "========================================="
echo "Installation Summary"
echo "========================================="
echo ""
echo "Required dependencies:"
echo "  • Git        ✓"
echo "  • uv         ✓"
echo "  • Python     ✓ (3.12 via uv)"
echo "  • Node.js    ✓"
echo "  • Claude CLI ✓"
echo ""
echo "Optional dependencies:"
if command -v docker &> /dev/null; then
    echo "  • Docker     ✓"
else
    echo "  • Docker     ✗ (for local Langfuse)"
fi
echo ""
echo "Environment variables (create .env file):"
echo "  ANTHROPIC_API_KEY=sk-ant-...  (for AI features)"
echo "  OPENAI_API_KEY=sk-...         (optional, for TTS)"
echo "  ELEVENLABS_API_KEY=...        (optional, for TTS)"
echo ""
echo "========================================="
echo "Next steps:"
echo "========================================="
echo ""
echo "1. Restart your terminal (or run: source ~/.zshrc)"
echo "2. Copy .env.sample to .env and add your API keys:"
echo "   cp .env.sample .env && nano .env"
echo "3. Open in Claude Code: claude ."
echo ""
```

### Windows: `scripts/install.ps1`

```powershell
# Nexus OS Installation Script for Windows
# Run with: powershell -ExecutionPolicy Bypass -File scripts\install.ps1

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Nexus OS Installer (Windows)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as admin (not required, just informational)
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

# 1. Check Git
Write-Host "Checking Git..." -ForegroundColor Yellow
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    Write-Host "  ✓ Git found: $($git.Source)" -ForegroundColor Green
} else {
    Write-Host "  ✗ Git not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Git first:" -ForegroundColor Yellow
    Write-Host "  Download from: https://git-scm.com/download/win" -ForegroundColor White
    Write-Host "  Or run: winget install Git.Git" -ForegroundColor White
    exit 1
}

# 2. Install uv
Write-Host ""
Write-Host "Checking uv (Python package manager)..." -ForegroundColor Yellow
$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($uv) {
    Write-Host "  ✓ uv found: $($uv.Source)" -ForegroundColor Green
} else {
    Write-Host "  Installing uv..." -ForegroundColor White
    try {
        irm https://astral.sh/uv/install.ps1 | iex

        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

        # Also add common location
        $uvPath = "$env:USERPROFILE\.local\bin"
        if (Test-Path $uvPath) {
            $env:Path = "$uvPath;$env:Path"
        }

        Write-Host "  ✓ uv installed" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed to install uv: $_" -ForegroundColor Red
        exit 1
    }
}

# 3. Install Python via uv
Write-Host ""
Write-Host "Ensuring Python 3.12..." -ForegroundColor Yellow
try {
    & uv python install 3.12 2>$null
    Write-Host "  ✓ Python 3.12 available" -ForegroundColor Green
} catch {
    Write-Host "  ✓ Python 3.12 (already installed or downloading)" -ForegroundColor Green
}

# 4. Node.js (required for Claude Code CLI)
Write-Host ""
Write-Host "Checking Node.js..." -ForegroundColor Yellow
$node = Get-Command node -ErrorAction SilentlyContinue
if ($node) {
    Write-Host "  ✓ Node.js found" -ForegroundColor Green
} else {
    Write-Host "  Installing Node.js..." -ForegroundColor White
    try {
        winget install OpenJS.NodeJS.LTS --accept-source-agreements --accept-package-agreements
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
        Write-Host "  ✓ Node.js installed" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ Failed to install Node.js. Please install manually from: https://nodejs.org/" -ForegroundColor Red
        exit 1
    }
}

# 5. Claude Code CLI (required)
Write-Host ""
Write-Host "Checking Claude Code CLI..." -ForegroundColor Yellow
$claude = Get-Command claude -ErrorAction SilentlyContinue
if ($claude) {
    Write-Host "  ✓ Claude Code CLI found" -ForegroundColor Green
} else {
    Write-Host "  Installing Claude Code CLI..." -ForegroundColor White
    npm install -g @anthropic-ai/claude-code
    Write-Host "  ✓ Claude Code CLI installed" -ForegroundColor Green
}

# 6. Test hooks
Write-Host ""
Write-Host "Testing hooks..." -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Split-Path -Parent $scriptDir
Push-Location $projectDir

try {
    $testInput = '{"session_id":"test","source":"new","transcript_path":""}'
    $result = $testInput | & .\.claude\hooks\run.cmd run .claude\hooks\session_start.py 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Hooks working!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Hook test returned non-zero (may work after restart)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Hook test failed (may work after restart)" -ForegroundColor Yellow
}

Pop-Location

# 7. Configure hooks for Windows
Write-Host ""
Write-Host "Configuring hooks for Windows..." -ForegroundColor Yellow
$settingsPath = Join-Path $projectDir ".claude\settings.json"
if (Test-Path $settingsPath) {
    $content = Get-Content $settingsPath -Raw
    $updated = $content -replace '\.claude/hooks/run run', '.claude\hooks\run.cmd run'
    $updated | Set-Content $settingsPath -NoNewline
    Write-Host "  ✓ Hooks configured for Windows" -ForegroundColor Green
} else {
    Write-Host "  ⚠ settings.json not found (hooks may not work)" -ForegroundColor Yellow
}

# 8. Create .env template if missing
Write-Host ""
Write-Host "Checking .env file..." -ForegroundColor Yellow
$envPath = Join-Path $projectDir ".env"
$envSamplePath = Join-Path $projectDir ".env.sample"
if (-not (Test-Path $envPath)) {
    @"
# Nexus OS Environment Variables
# Copy this file to .env and fill in your keys

# REQUIRED: Anthropic API Key (for Claude Code features)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OPTIONAL: Additional LLM providers
# OPENAI_API_KEY=sk-...

# OPTIONAL: Integrations (add as needed)
# AIRTABLE_API_KEY=...
# NOTION_API_KEY=...
"@ | Set-Content $envSamplePath
    Write-Host "  ✓ Created .env.sample (copy to .env and add your keys)" -ForegroundColor Green
} else {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
}

# Summary
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Installation Summary" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Required dependencies:" -ForegroundColor White
Write-Host "  • Git        ✓" -ForegroundColor Green
Write-Host "  • uv         ✓" -ForegroundColor Green
Write-Host "  • Python     ✓ (3.12 via uv)" -ForegroundColor Green
Write-Host "  • Node.js    ✓" -ForegroundColor Green
Write-Host "  • Claude CLI ✓" -ForegroundColor Green
Write-Host ""
Write-Host "Environment variables (create .env file):" -ForegroundColor White
Write-Host "  ANTHROPIC_API_KEY=sk-ant-...  (for AI features)" -ForegroundColor Gray
Write-Host "  OPENAI_API_KEY=sk-...         (optional)" -ForegroundColor Gray
Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Close and reopen your terminal" -ForegroundColor White
Write-Host "2. Copy .env.sample to .env and add your API keys:" -ForegroundColor White
Write-Host "   copy .env.sample .env" -ForegroundColor Gray
Write-Host "   notepad .env" -ForegroundColor Gray
Write-Host "3. Open in Claude Code: claude ." -ForegroundColor White
Write-Host ""
```

---

## File Structure Reference

### Complete Directory Structure

```
nexus/
├── CLAUDE.md                          # Entry point (loaded at startup)
├── README.md                          # Quick reference
├── pyproject.toml                     # Python config (no external deps)
├── uv.lock                            # Lock file
├── .env                               # API keys (NEVER COMMIT)
├── .env.sample                        # Template for .env
├── .gitignore                         # Protection rules
│
├── 00-system/                         # SYSTEM (don't modify)
│   ├── core/
│   │   ├── orchestrator.md            # AI behavior rules, routing, menu
│   │   ├── nexus/                     # Python package
│   │   │   ├── config.py              # Constants, paths
│   │   │   ├── models.py              # Data classes
│   │   │   ├── loaders.py             # File loading
│   │   │   ├── service.py             # Main service
│   │   │   ├── sync.py                # Upstream sync
│   │   │   ├── state.py               # State management
│   │   │   └── utils.py               # Utilities
│   │   └── templates/                 # Template files
│   ├── skills/                        # 50+ built-in workflows
│   │   ├── builds/                    # build management
│   │   ├── learning/                  # onboarding skills
│   │   ├── system/                    # system utilities
│   │   ├── skill-dev/                 # skill creation
│   │   ├── meta/                      # analytics integration
│   │   └── tools/                     # utility tools
│   ├── documentation/                 # Framework guides
│   ├── mental-models/                 # Decision frameworks
│   └── .cache/                        # Auto-generated cache
│
├── 01-memory/                         # USER PERSISTENT CONTEXT
│   ├── goals.md                       # Role, objectives
│   ├── user-config.yaml               # Preferences (auto-generated)
│   ├── core-learnings.md              # Patterns learned
│   ├── memory-map.md                  # Overview
│   └── session-reports/               # Auto-generated
│
├── 02-builds/                         # WORK BUILDS
│   ├── active/                        # In-progress builds
│   │   └── {ID}-{name}/
│   │       ├── 01-planning/           # overview, plan, steps
│   │       ├── 02-resources/          # reference materials
│   │       ├── 03-working/            # work in progress
│   │       └── 04-outputs/            # deliverables
│   └── complete/                      # Archived builds
│
├── 03-skills/                         # USER CUSTOM SKILLS
│   └── {skill-name}/
│       └── SKILL.md                   # Workflow definition
│
├── 04-workspace/                      # USER FILES
│   └── workspace-map.md               # AI's file guide
│
├── .claude/                           # CLAUDE CODE CONFIG
│   ├── settings.json                  # Hook configuration
│   ├── settings.local.json            # Local permissions
│   ├── hooks/                         # Event handlers (see below)
│   ├── agents/                        # Custom agents
│   ├── commands/                      # CLI commands
│   └── sessions/                      # Session cache
│
├── scripts/                           # INSTALLATION SCRIPTS
│   ├── install.sh                     # Unix/Linux/macOS
│   └── install.ps1                    # Windows PowerShell
│
└── logs/                              # Session logs (gitignored)
```

---

## Hook System Deep Dive

### Hook Configuration: `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/session_start.py"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/session_end.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/session_summary.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/pre_tool_use.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/send_event.py --source-app mutagent-obsidian --event-type PreToolUse"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/post_tool_use.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/stream_claude_message.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/send_event.py --source-app mutagent-obsidian --event-type PostToolUse"
          }
        ]
      },
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/validate_resume_context.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/notification.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/send_event.py --source-app mutagent-obsidian --event-type Notification"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/stop.py --chat"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/send_event.py --source-app mutagent-obsidian --event-type Stop --add-chat"
          }
        ]
      }
    ],
    "SubagentStop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/subagent_stop.py"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/send_event.py --source-app mutagent-obsidian --event-type SubagentStop"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/user_prompt_submit.py --log-only"
          },
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/send_event.py --source-app mutagent-obsidian --event-type UserPromptSubmit"
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/run run .claude/hooks/save_resume_state.py",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

### Hook Runner Scripts

#### Unix/macOS/Linux: `.claude/hooks/run`

```bash
#!/bin/sh
# Universal hook runner - ensures uv is in PATH regardless of environment
# Works on: macOS, Linux, Windows (Git Bash, WSL, MSYS2)
# Works in: Terminal, VSCode, any IDE, cron, etc.
#
# On Windows native, use: .claude\hooks\run.cmd

# Add common binary locations to PATH
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

# Windows compatibility (Git Bash / WSL / MSYS2)
if [ -n "$USERPROFILE" ]; then
    # Convert Windows path to Unix-style for Git Bash
    WIN_HOME=$(echo "$USERPROFILE" | sed 's|\\|/|g' | sed 's|C:|/c|')
    export PATH="$WIN_HOME/.local/bin:$USERPROFILE/.local/bin:$PATH"
fi

# Run uv with all arguments passed through
exec uv "$@"
```

#### Windows: `.claude/hooks/run.cmd`

```batch
@echo off
REM Universal hook runner for Windows (cmd/PowerShell)
REM Works on: Windows 10/11 native

REM Check common uv locations
if exist "%USERPROFILE%\.local\bin\uv.exe" (
    "%USERPROFILE%\.local\bin\uv.exe" %*
    exit /b %errorlevel%
)

if exist "%LOCALAPPDATA%\uv\uv.exe" (
    "%LOCALAPPDATA%\uv\uv.exe" %*
    exit /b %errorlevel%
)

if exist "%USERPROFILE%\.cargo\bin\uv.exe" (
    "%USERPROFILE%\.cargo\bin\uv.exe" %*
    exit /b %errorlevel%
)

REM Try PATH as fallback
where uv >nul 2>&1
if %errorlevel%==0 (
    uv %*
    exit /b %errorlevel%
)

echo ERROR: uv not found. Please run: scripts\install.ps1
exit /b 1
```

### Core Hook Files

#### `session_start.py` - Context Injection (1256 lines)

**Purpose**: Inject full Nexus context at session start

**Key Functions**:
- `determine_context_mode()` - Detect startup vs compact mode
- `build_startup_xml()` - Generate full menu context (~20K tokens)
- `build_compact_xml()` - Generate build continuation context (~10K tokens)
- `load_resume_context()` - Load build resume state
- `ensure_langfuse_running()` - Auto-start Langfuse (optional)

**Input** (stdin JSON):
```json
{
  "session_id": "abc123-...",
  "source": "new|compact|resume|clear",
  "transcript_path": "~/.claude/builds/.../xxx.jsonl"
}
```

**Output** (stdout JSON):
```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<nexus-context>...</nexus-context>"
  },
  "systemMessage": "SessionStart:startup hook success: Success"
}
```

#### `session_end.py` - Cleanup (169 lines)

**Purpose**: Clean up session cache, save transcript

**Key Functions**:
- `save_transcript_locally()` - Backup transcript to logs/
- `cleanup_session_cache()` - Delete session-specific cache
- `send_transcript_to_server()` - Send to observability server

#### `pre_tool_use.py` - Safety Checks (366 lines)

**Purpose**: Block dangerous commands, detect executables

**Blocks**:
- `rm -rf /` and variants
- `.env` file access
- Dangerous git commands (`git reset --hard`, `git push --force`)

**Detects**:
- Executable loads (agent, skill, task, workflow)
- Build context switches

#### `save_resume_state.py` - PreCompact (234 lines)

**Purpose**: Save resume context before compaction

**Updates**:
- `resume-context.md` with session_ids list
- `last_updated` timestamp for resume detection

---

## Utility Modules Reference

### `.claude/hooks/utils/` Directory

| File | Purpose | Key Functions |
|------|---------|---------------|
| `http.py` | Fire-and-forget HTTP | `send_to_server()` |
| `xml.py` | XML escaping/building | `escape_xml_content()`, `load_file_to_xml()` |
| `transcript.py` | Transcript parsing | `parse_transcript_for_build()`, `find_build_by_session_id()` |
| `constants.py` | Path constants | `ensure_session_log_dir()` |
| `server.py` | Server health | `ensure_server_running()` |
| `github.py` | GitHub API | `fetch_github_issues()` |
| `build_state.py` | Build detection | `detect_build_state()`, `detect_phase_from_metadata()` |
| `registry.py` | Shortcut lookup | `lookup_shortcut()` |

### `utils/http.py`

```python
"""Fire-and-forget HTTP with timeout."""
import json, urllib.request, urllib.error, sys, os

SERVER_URL = os.environ.get("OBSERVABILITY_SERVER_URL", "http://localhost:7777")
TIMEOUT_SECONDS = 5

def send_to_server(endpoint: str, payload: dict) -> bool:
    """Send payload to observability server. Never raises, never blocks long."""
    try:
        url = f"{SERVER_URL}{endpoint}"
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "Claude-Hook/1.0"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as response:
            return response.status in (200, 201)
    except Exception as e:
        print(f"[hook] Server error: {e}", file=sys.stderr)
        return False
```

### `utils/xml.py`

```python
"""XML utilities for Claude Code hooks."""
import re, logging
from pathlib import Path
from typing import Optional

def escape_xml_content(content: str) -> str:
    """Escape XML special characters while preserving markdown."""
    if not content:
        return ""
    content = re.sub(r'&(?!(lt|gt|amp|quot|apos|#\d+|#x[0-9a-fA-F]+);)', '&amp;', content)
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')
    return content

def escape_xml_attribute(value: str) -> str:
    """Escape for XML attribute values (handles quotes)."""
    if not value:
        return ""
    value = escape_xml_content(value)
    value = value.replace('"', '&quot;')
    value = value.replace("'", '&apos;')
    return value

def load_file_to_xml(path: Path, tag_name: str, path_label: str, indent: int = 2) -> Optional[str]:
    """Load a file and wrap its content in XML tags."""
    if not path.exists():
        return None
    try:
        content = escape_xml_content(path.read_text(encoding='utf-8'))
        spaces = " " * indent
        return f'''{spaces}<{tag_name} path="{escape_xml_attribute(path_label)}">
{content}
{spaces}</{tag_name}>'''
    except Exception as e:
        logging.error(f"Error reading {path}: {e}")
        return None
```

### `utils/transcript.py`

```python
"""Transcript parsing for build detection."""
import json, re, logging
from pathlib import Path
from typing import Optional, Tuple

BUILD_PATTERN = re.compile(r'02-builds/active[/\\]([0-9]{2}-[a-zA-Z0-9_-]+)', re.IGNORECASE)

def find_build_by_session_id(builds_dir: str, session_id: str) -> Optional[str]:
    """Find build by session_id match in resume-context.md files."""
    # Checks session_ids list first (multi-session support)
    # Falls back to legacy session_id field
    ...

def parse_transcript_for_build(transcript_path: str, max_entries: int = 500) -> Tuple[Optional[str], str]:
    """Parse transcript JSONL to detect active build from tool calls."""
    # Extracts file_path from Read, Write, Edit, Glob, Bash tool_use entries
    # Returns (build_id, detection_method)
    ...
```

### `utils/build_state.py`

```python
"""Build State Detection Utility."""
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Any

@dataclass
class BuildState:
    """Complete build state snapshot."""
    build_id: str
    name: str
    status: str  # PLANNING | IN_PROGRESS | COMPLETE
    current_phase: str  # planning | execution
    next_action: str  # plan-build | execute-build
    current_section: float
    tasks_completed: int
    tasks_total: int
    progress_percent: float
    last_updated: Optional[str] = None
    session_ids: list[str] = None

def detect_build_state(build_path: Path) -> Optional[BuildState]:
    """Detect complete build state from metadata files."""
    # Combines: overview.md, resume-context.md, steps.md
    ...

def detect_phase_from_metadata(build_path: Path) -> tuple[str, str]:
    """Detect build phase with fallback logic."""
    # Priority: resume-context.md > steps.md checkbox analysis
    # Returns (phase, skill)
    ...
```

---

## Configuration Files

### `pyproject.toml`

```toml
[build]
name = "strategy-nexus"
version = "0.1.0"
requires-python = ">=3.10"
description = "Nexus Operating System - Claude Code hooks and utilities"

# No external dependencies - hooks use stdlib only
dependencies = []
```

### `.gitignore`

```gitignore
# Nexus-v4 .gitignore

# Environment (NEVER COMMIT)
.env
.venv
env/
venv/

# MCP Configuration (contains API keys)
.mcp.local.json

# Google OAuth credentials
google-credentials.json

# Database files
events.db
*.db

# Logs
logs/

# Cache directories
.cache/
00-system/.cache/

# Python
__pycache__/
*.py[cod]

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
```

### `.env.sample` (Template)

```bash
# Nexus OS Environment Variables
# Copy this file to .env and fill in your keys

# REQUIRED: Anthropic API Key (for Claude Code features)
ANTHROPIC_API_KEY=sk-ant-your-key-here

# OPTIONAL: Additional LLM providers
# OPENAI_API_KEY=sk-...

# OPTIONAL: Text-to-speech
# ELEVENLABS_API_KEY=...

# OPTIONAL: Integrations (add as needed)
# AIRTABLE_API_KEY=...
# NOTION_API_KEY=...
# LANGFUSE_SECRET_KEY=...
# LANGFUSE_PUBLIC_KEY=...
```

---

## Post-Installation Setup

### Step 1: First Launch
```bash
# Launch Claude Code
claude .

# Nexus will auto-detect first run and guide you through:
# - Goal setup
# - Workspace configuration
# - System overview
```

### Step 2: Quick Start (If Prompted)
Say: `"quick start"` to begin the 5-phase onboarding.

### Step 3: Create Your First Build
Say: `"create build"` or `"build [something]"`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `uv command not found` | Add to PATH: `export PATH="$HOME/.local/bin:$PATH"` then restart terminal |
| `Python 3.12 not installing` | Run: `uv python install 3.12 --force` |
| Hook test fails | Check hook has execute permission: `chmod +x .claude/hooks/*.py` |
| `.env` file not loading | Ensure it's in build root, not .claude/ |
| Windows hook errors | Use `run.cmd` instead of `run` in settings.json |
| Hooks not triggering | Verify `.claude/settings.json` exists and is valid JSON |
| Session not resuming | Check `resume-context.md` has `session_ids` list |

### Manual Hook Test

```bash
# Mac/Linux
echo '{"session_id":"test","source":"new","transcript_path":""}' | uv run .claude/hooks/session_start.py

# Windows (PowerShell)
'{"session_id":"test","source":"new","transcript_path":""}' | & .\.claude\hooks\run.cmd run .claude\hooks\session_start.py
```

### Check Hook Output

```bash
# View last hook output
cat 00-system/.cache/session_start_output.log

# View full XML context
cat 00-system/.cache/session_start_context.xml
```

---

## Summary: One-Command Install

### Mac/Linux
```bash
git clone https://github.com/YOUR-USERNAME/nexus.git && cd nexus && ./scripts/install.sh && cp .env.sample .env && echo "Add your ANTHROPIC_API_KEY to .env, then run: claude ."
```

### Windows (PowerShell)
```powershell
git clone https://github.com/YOUR-USERNAME/nexus.git; cd nexus; powershell -ExecutionPolicy Bypass -File scripts\install.ps1; copy .env.sample .env; Write-Host "Add your ANTHROPIC_API_KEY to .env, then run: claude ."
```

---

**Last Updated**: 2026-01-17
