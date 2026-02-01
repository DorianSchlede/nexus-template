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

# NOTE: Git installation removed - we use ZIP download instead of git clone
# This means no Git dependency for installation

# ============================================================================
# VS CODE INSTALLATION
# ============================================================================

function Install-VsCode {
    Write-Header "Installing VS Code"

    if (Get-Command code -ErrorAction SilentlyContinue) {
        Write-Success "VS Code is already installed"
        return $true
    }

    Write-Warning "VS Code is not installed"

    # Try to install with winget (built into Windows 10/11)
    if (Get-Command winget -ErrorAction SilentlyContinue) {
        Write-Info "Installing VS Code via winget..."
        try {
            winget install Microsoft.VisualStudioCode --accept-package-agreements --accept-source-agreements -e

            # Refresh PATH to pick up VS Code
            $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

            if (Get-Command code -ErrorAction SilentlyContinue) {
                Write-Success "VS Code installed successfully"
                return $true
            }
        } catch {
            Write-Warning "winget installation failed: $_"
        }
    }

    # Fallback: direct download
    Write-Info "Downloading VS Code installer..."
    $installerUrl = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
    $installerPath = Join-Path $env:TEMP "VSCodeUserSetup.exe"

    try {
        Invoke-WebRequest -Uri $installerUrl -OutFile $installerPath -UseBasicParsing
        Write-Info "Running VS Code installer (silent)..."
        Start-Process -FilePath $installerPath -ArgumentList "/verysilent /mergetasks=!runcode,addcontextmenufiles,addcontextmenufolders,addtopath" -Wait

        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

        # Cleanup
        Remove-Item $installerPath -Force -ErrorAction SilentlyContinue

        if (Get-Command code -ErrorAction SilentlyContinue) {
            Write-Success "VS Code installed successfully"
            return $true
        }
    } catch {
        Write-Warning "Direct download failed: $_"
    }

    # Final fallback: manual
    Write-Error "Could not install VS Code automatically"
    Write-Info "Please install VS Code manually from: https://code.visualstudio.com/download"
    Start-Process "https://code.visualstudio.com/download"
    return $false
}

# ============================================================================
# NEXUS DOWNLOAD (ZIP - no Git required)
# ============================================================================

$script:NexusRepoUrl = "https://github.com/DorianSchlede/nexus-template"
$script:NexusZipUrl = "$($script:NexusRepoUrl)/archive/refs/heads/main.zip"

function Get-NexusDownload {
    Write-Header "Downloading Nexus"

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
        $confirm = Read-Host "Do you want to remove it and start fresh? (y/N)"

        if ($confirm -eq "y" -or $confirm -eq "Y") {
            Remove-Item -Recurse -Force $nexusDir
        } else {
            Write-Warning "Skipping Nexus download"
            return $null
        }
    }

    # Create temp directory for download
    $tempDir = Join-Path $env:TEMP "nexus-install-$([Guid]::NewGuid().ToString().Substring(0,8))"
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    $zipFile = Join-Path $tempDir "nexus.zip"

    Write-Info "Downloading Nexus from GitHub..."

    try {
        # Download ZIP (no Git required, no auth required)
        Invoke-WebRequest -Uri $script:NexusZipUrl -OutFile $zipFile -UseBasicParsing
        Write-Success "Downloaded Nexus archive"
    } catch {
        Write-Error "Failed to download Nexus: $_"
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
        return $null
    }

    Write-Info "Extracting..."

    try {
        # Extract ZIP
        Expand-Archive -Path $zipFile -DestinationPath $tempDir -Force

        # Move extracted folder to destination
        # GitHub ZIP extracts to nexus-template-main/
        $extractedDir = Join-Path $tempDir "nexus-template-main"

        # Ensure parent directory exists
        $parentDir = Split-Path -Parent $nexusDir
        if ($parentDir -and -not (Test-Path $parentDir)) {
            New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
        }

        Move-Item -Path $extractedDir -Destination $nexusDir -Force

        # Cleanup
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue

        Write-Success "Nexus installed to $nexusDir"
        return $nexusDir
    } catch {
        Write-Error "Failed to extract Nexus: $_"
        Remove-Item -Recurse -Force $tempDir -ErrorAction SilentlyContinue
        return $null
    }
}

# NOTE: Claude settings (permission bypass) and VS Code settings (markdown preview)
# are now configured interactively via Claude chat after installation.
# See /setup skill for the interactive configuration workflow.

# ============================================================================
# INSTALL NEXUS CLI
# ============================================================================

function Install-NexusCli {
    param([string]$NexusDir)

    Write-Header "Installing Nexus CLI Tools"

    if (-not $NexusDir) {
        Write-Warning "Nexus not cloned, skipping CLI installation"
        return
    }

    # Refresh PATH to pick up newly installed uv
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

    # Verify uv is now available
    if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
        Write-Warning "uv not found in PATH after refresh"
        Write-Info "You can install CLI tools manually later: cd $NexusDir; uv tool install ."
        return
    }

    Write-Info "Installing Nexus CLI tools globally..."

    try {
        Push-Location $NexusDir
        uv tool install . --force
        Pop-Location

        # Refresh PATH again to pick up newly installed CLI tools
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

        Write-Success "Nexus CLI tools installed"
    } catch {
        Pop-Location
        Write-Warning "Failed to install Nexus CLI tools: $_"
        Write-Info "You can install manually later: cd $NexusDir; uv tool install ."
    }
}

# ============================================================================
# CLAUDE EXTENSION INSTALLATION
# ============================================================================

function Install-ClaudeExtension {
    Write-Header "Installing Claude Extension"

    if (-not (Get-Command code -ErrorAction SilentlyContinue)) {
        Write-Warning "VS Code not found, skipping extension installation"
        return
    }

    Write-Info "Installing Claude extension for VS Code..."

    try {
        & code --install-extension anthropic.claude-code --force 2>&1 | Out-Null
        Write-Success "Claude extension installed"
    } catch {
        Write-Warning "Failed to install Claude extension: $_"
        Write-Info "You can install it manually from the VS Code Extensions marketplace"
    }
}

# ============================================================================
# VS CODE LAUNCH
# ============================================================================

function Start-VsCode {
    param([string]$NexusDir)

    if ($NexusDir) {
        Write-Header "Opening VS Code"

        if (Get-Command code -ErrorAction SilentlyContinue) {
            Write-Info "Opening $NexusDir in VS Code..."
            & code $NexusDir
            Write-Success "VS Code opened - click the Claude icon in the sidebar and say 'hi'!"
        } else {
            Write-Warning "VS Code command not found."
            Write-Info "Please open VS Code manually and open the folder: $NexusDir"
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

    if (Get-Command code -ErrorAction SilentlyContinue) {
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

    if ((Get-Command code -ErrorAction SilentlyContinue) -and $NexusDir) {
        Write-Host "  VS Code should have opened automatically."
        Write-Host ""
        Write-Host "  1. Click the Claude icon in the sidebar"
        Write-Host "  2. Say 'hi'"
        Write-Host "  3. Claude will guide you from there!"
    } else {
        Write-Host "  1. Open VS Code"
        Write-Host "  2. Open the folder: $NexusDir"
        Write-Host "  3. Click the Claude icon in the sidebar"
        Write-Host "  4. Say 'hi'"
    }

    Write-Host ""
    Write-Success "Installation complete! Enjoy Nexus!"
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

    # Install VS Code (if not already installed)
    if (-not (Install-VsCode)) {
        Write-Warning "VS Code is required. Please install it and re-run this installer."
        exit 1
    }

    # Download Nexus (ZIP - no Git required)
    $nexusDir = Get-NexusDownload

    # Install Nexus CLI tools
    Install-NexusCli -NexusDir $nexusDir

    # Install Claude extension for VS Code
    Install-ClaudeExtension

    # Launch VS Code
    Start-VsCode -NexusDir $nexusDir

    # Show summary
    Show-Summary -NexusDir $nexusDir
}

# Run main
Main
