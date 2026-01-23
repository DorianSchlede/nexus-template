# Nexus One-Command Installer - PowerShell
# Install Claude Code, uv, Git, and Nexus template in one command
#
# Usage:
#   irm https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.ps1 | iex
#

#Requires -Version 5.1

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# ============================================================================
# COLORS & OUTPUT
# ============================================================================

function Write-Info {
    param([string]$Message)
    Write-Host "[i] " -ForegroundColor Blue -NoNewline
    Write-Host $Message
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] " -ForegroundColor Green -NoNewline
    Write-Host $Message
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[!] " -ForegroundColor Yellow -NoNewline
    Write-Host $Message
}

function Write-Error {
    param([string]$Message)
    Write-Host "[X] " -ForegroundColor Red -NoNewline
    Write-Host $Message
}

function Write-Header {
    param([string]$Message)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor White
    Write-Host $Message -ForegroundColor White
    Write-Host "========================================" -ForegroundColor White
    Write-Host ""
}

# ============================================================================
# PLATFORM DETECTION
# ============================================================================

function Get-PlatformInfo {
    $arch = if ([Environment]::Is64BitProcess) { "x64" } else { "x86" }
    $os = "Windows $([Environment]::OSVersion.Version.Major).$([Environment]::OSVersion.Version.Minor)"

    Write-Info "Platform: $os ($arch)"

    if (-not [Environment]::Is64BitProcess) {
        Write-Error "Claude Code requires 64-bit Windows"
        exit 1
    }
}

# ============================================================================
# TOOL CHECKS
# ============================================================================

$script:PathUpdated = $false

function Test-CommandExists {
    param(
        [string]$Command,
        [string]$Name
    )

    try {
        if (Get-Command $Command -ErrorAction SilentlyContinue) {
            Write-Success "$Name is already installed"
            return $true
        } else {
            Write-Warning "$Name is not installed"
            return $false
        }
    } catch {
        Write-Warning "$Name is not installed"
        return $false
    }
}

# ============================================================================
# INSTALLATIONS
# ============================================================================

function Install-ClaudeCode {
    Write-Header "Installing Claude Code"

    if (Test-CommandExists "claude" "Claude Code") {
        return
    }

    Write-Info "Downloading and installing Claude Code..."

    try {
        # Call official installer
        Invoke-Expression (Invoke-RestMethod https://claude.ai/install.ps1)

        $script:PathUpdated = $true

        # Verify installation
        if (Get-Command claude -ErrorAction SilentlyContinue) {
            Write-Success "Claude Code installed successfully"
        } else {
            Write-Warning "Claude Code installed but not in PATH yet (restart terminal after installation)"
        }
    } catch {
        Write-Error "Failed to install Claude Code: $_"
        throw
    }
}

function Install-Uv {
    Write-Header "Installing uv"

    if (Test-CommandExists "uv" "uv") {
        return
    }

    Write-Info "Downloading and installing uv..."

    try {
        # Call official installer
        Invoke-Expression (Invoke-RestMethod https://astral.sh/uv/install.ps1)

        $script:PathUpdated = $true

        # Verify installation
        if (Get-Command uv -ErrorAction SilentlyContinue) {
            Write-Success "uv installed successfully"
        } else {
            Write-Warning "uv installed but not in PATH yet (restart terminal after installation)"
        }
    } catch {
        Write-Error "Failed to install uv: $_"
        throw
    }
}

function Install-Git {
    Write-Header "Installing Git"

    if (Test-CommandExists "git" "Git") {
        return
    }

    Write-Info "Installing Git for Windows..."

    # Check if winget is available
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        try {
            Write-Info "Using winget to install Git..."
            winget install --id Git.Git -e --source winget --silent --accept-package-agreements --accept-source-agreements

            $script:PathUpdated = $true
            Write-Success "Git installed successfully"
        } catch {
            Write-Error "Failed to install Git via winget: $_"
            Write-Info "Please install Git manually from https://git-scm.com/download/win"
            throw
        }
    } else {
        # Fallback: Try chocolatey
        if (Get-Command choco -ErrorAction SilentlyContinue) {
            try {
                Write-Info "Using Chocolatey to install Git..."
                choco install git -y

                $script:PathUpdated = $true
                Write-Success "Git installed successfully"
            } catch {
                Write-Error "Failed to install Git via Chocolatey: $_"
                Write-Info "Please install Git manually from https://git-scm.com/download/win"
                throw
            }
        } else {
            Write-Error "Neither winget nor Chocolatey found. Please install Git manually."
            Write-Info "Download from: https://git-scm.com/download/win"
            Start-Process "https://git-scm.com/download/win"
            throw
        }
    }
}

# ============================================================================
# VS CODE PROMPT
# ============================================================================

function Invoke-VsCodePrompt {
    Write-Header "VS Code Installation"

    if (Test-CommandExists "code" "VS Code") {
        $script:VsCodeInstalled = $true
        return
    }

    Write-Host "Do you want to install VS Code?"
    Write-Host ""
    Write-Host "  1. Yes - Install VS Code"
    Write-Host "  2. No - Skip VS Code"
    Write-Host ""
    $choice = Read-Host "Your choice (1 or 2)"

    switch ($choice) {
        "1" { Install-VsCode }
        "2" {
            Write-Info "Skipping VS Code installation"
            $script:VsCodeInstalled = $false
        }
        default {
            Write-Warning "Invalid choice. Skipping VS Code installation"
            $script:VsCodeInstalled = $false
        }
    }
}

function Install-VsCode {
    Write-Info "Installing VS Code..."

    if (Get-Command winget -ErrorAction SilentlyContinue) {
        try {
            winget install --id Microsoft.VisualStudioCode -e --source winget --silent --accept-package-agreements --accept-source-agreements

            $script:PathUpdated = $true
            $script:VsCodeInstalled = $true
            Write-Success "VS Code installed successfully"
        } catch {
            Write-Warning "Failed to install VS Code via winget"
            Write-Info "Opening VS Code download page..."
            Start-Process "https://code.visualstudio.com/download"
            $script:VsCodeInstalled = $false
        }
    } else {
        Write-Info "Opening VS Code download page..."
        Start-Process "https://code.visualstudio.com/download"
        Write-Warning "Please install VS Code and re-run this script to complete setup"
        $script:VsCodeInstalled = $false
    }
}

# ============================================================================
# NEXUS CLONE
# ============================================================================

function Invoke-NexusClone {
    Write-Header "Cloning Nexus Template"

    Write-Host "Where do you want to install Nexus?"
    Write-Host ""
    $nexusDir = Read-Host "Directory path (default: $env:USERPROFILE\nexus)"

    if ([string]::IsNullOrWhiteSpace($nexusDir)) {
        $nexusDir = "$env:USERPROFILE\nexus"
    }

    # Expand environment variables
    $nexusDir = [System.Environment]::ExpandEnvironmentVariables($nexusDir)

    # Check if directory exists
    if (Test-Path $nexusDir) {
        Write-Error "Directory $nexusDir already exists"
        $confirm = Read-Host "Do you want to remove it and clone fresh? (y/N)"

        if ($confirm -eq "y" -or $confirm -eq "Y") {
            Remove-Item -Recurse -Force $nexusDir
        } else {
            Write-Warning "Skipping Nexus clone"
            return $null
        }
    }

    Write-Info "Cloning Nexus to $nexusDir..."

    try {
        git clone https://github.com/DorianSchlede/nexus-template.git $nexusDir
        Write-Success "Nexus cloned successfully to $nexusDir"
        return $nexusDir
    } catch {
        Write-Error "Failed to clone Nexus: $_"
        return $null
    }
}

# ============================================================================
# VS CODE LAUNCH
# ============================================================================

function Start-VsCode {
    param([string]$NexusDir)

    if ($script:VsCodeInstalled -and $NexusDir) {
        Write-Header "Opening VS Code"

        if (Get-Command code -ErrorAction SilentlyContinue) {
            Write-Info "Opening $NexusDir in VS Code..."
            & code $NexusDir
            Write-Success "VS Code opened"
        } else {
            Write-Warning "VS Code command not found. Please open $NexusDir manually."
        }
    }
}

# ============================================================================
# SUMMARY
# ============================================================================

function Show-Summary {
    param([string]$NexusDir)

    Write-Header "Installation Summary"

    Write-Host ""
    Write-Host "Installed:" -ForegroundColor White
    Write-Host ""

    if (Get-Command claude -ErrorAction SilentlyContinue) {
        Write-Host "  " -NoNewline
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Claude Code"
    } else {
        Write-Host "  " -NoNewline
        Write-Host "[!]" -ForegroundColor Yellow -NoNewline
        Write-Host " Claude Code (not in PATH)"
    }

    if (Get-Command uv -ErrorAction SilentlyContinue) {
        Write-Host "  " -NoNewline
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " uv"
    } else {
        Write-Host "  " -NoNewline
        Write-Host "[!]" -ForegroundColor Yellow -NoNewline
        Write-Host " uv (not in PATH)"
    }

    if (Get-Command git -ErrorAction SilentlyContinue) {
        Write-Host "  " -NoNewline
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Git"
    } else {
        Write-Host "  " -NoNewline
        Write-Host "[X]" -ForegroundColor Red -NoNewline
        Write-Host " Git"
    }

    if ($script:VsCodeInstalled) {
        Write-Host "  " -NoNewline
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " VS Code"
    }

    if ($NexusDir) {
        Write-Host "  " -NoNewline
        Write-Host "[OK]" -ForegroundColor Green -NoNewline
        Write-Host " Nexus Template ($NexusDir)"
    }

    Write-Host ""

    # PATH warning
    if ($script:PathUpdated) {
        Write-Host "[!] PATH was updated during installation" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "To apply changes:" -ForegroundColor White
        Write-Host "  Restart your terminal (PowerShell/Command Prompt)"
        Write-Host ""
        Write-Host "========================================" -ForegroundColor White
        Write-Host ""
    }

    # Next steps
    Write-Host "Next Steps:" -ForegroundColor White
    Write-Host ""

    $step = 1
    if ($script:PathUpdated) {
        Write-Host "  $step. Restart your terminal"
        $step++
    }

    if ($NexusDir) {
        Write-Host "  $step. cd $NexusDir"
        $step++
        Write-Host "  $step. claude"
    } else {
        Write-Host "  $step. Clone Nexus: git clone https://github.com/DorianSchlede/nexus-template.git"
        $step++
        Write-Host "  $step. cd nexus-template"
        $step++
        Write-Host "  $step. claude"
    }

    Write-Host ""
    Write-Success "Installation complete!"
    Write-Host ""
}

# ============================================================================
# MAIN
# ============================================================================

function Main {
    Clear-Host

    Write-Host ""
    Write-Host "    ========================================" -ForegroundColor White
    Write-Host "              NEXUS INSTALLER               " -ForegroundColor White
    Write-Host "         One-Command Setup for All          " -ForegroundColor White
    Write-Host "    ========================================" -ForegroundColor White
    Write-Host ""

    Get-PlatformInfo

    # Install tools
    Install-ClaudeCode
    Install-Uv
    Install-Git

    # VS Code prompt
    Invoke-VsCodePrompt

    # Clone Nexus
    $nexusDir = Invoke-NexusClone

    # Launch VS Code if installed
    Start-VsCode -NexusDir $nexusDir

    # Show summary
    Show-Summary -NexusDir $nexusDir
}

# Run main
Main
