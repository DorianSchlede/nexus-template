#
# Nexus Setup Init Script (Windows)
# Runs when: claude --init
# Purpose: Install dependencies and set up the codebase
#

$ErrorActionPreference = "Stop"

# ============================================================================
# CONFIG
# ============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = (Get-Item "$ScriptDir\..\..\..").FullName
$LogFile = "$ProjectDir\.claude\logs\install.log"

# Ensure log directory exists
$LogDir = Split-Path -Parent $LogFile
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
}

# ============================================================================
# LOGGING
# ============================================================================

function Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$timestamp] $Message"
    Write-Host $line
    Add-Content -Path $LogFile -Value $line
}

function LogSection {
    param([string]$Title)
    $separator = "━" * 36
    Log ""
    Log $separator
    Log $Title
    Log $separator
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

function RunCommand {
    param([string]$Command)
    Log "Running: $Command"
    try {
        $output = Invoke-Expression $Command 2>&1 | Out-String
        Add-Content -Path $LogFile -Value $output
        Log "[OK] Success: $Command"
        return $true
    } catch {
        Add-Content -Path $LogFile -Value $_.Exception.Message
        Log "✗ Failed: $Command"
        return $false
    }
}

function CheckCommand {
    param([string]$Name)
    if (Get-Command $Name -ErrorAction SilentlyContinue) {
        Log "[OK] Found: $Name"
        return $true
    } else {
        Log "✗ Missing: $Name"
        return $false
    }
}

# ============================================================================
# MAIN INSTALLATION
# ============================================================================

function Main {
    # Clear previous log
    Set-Content -Path $LogFile -Value ""

    LogSection "NEXUS INSTALLATION STARTED"
    Log "Project directory: $ProjectDir"
    Log "Log file: $LogFile"

    # Check prerequisites
    LogSection "CHECKING PREREQUISITES"

    $prereqsOk = $true

    if (-not (CheckCommand "python")) {
        $prereqsOk = $false
    }

    if (-not (CheckCommand "uv")) {
        $prereqsOk = $false
    }

    if (-not (CheckCommand "git")) {
        $prereqsOk = $false
    }

    if (-not $prereqsOk) {
        Log "Some prerequisites are missing. See log for details."
    }

    # Install Python dependencies
    LogSection "INSTALLING PYTHON DEPENDENCIES"

    Push-Location $ProjectDir

    if (Test-Path "pyproject.toml") {
        RunCommand "uv sync"
    } else {
        Log "No pyproject.toml found, skipping Python dependencies"
    }

    # Install Nexus CLI tools
    LogSection "INSTALLING NEXUS CLI TOOLS"

    if (Test-Path "pyproject.toml") {
        RunCommand "uv tool install . --force" | Out-Null
    }

    # Verify core files exist
    LogSection "VERIFYING NEXUS STRUCTURE"

    $structureOk = $true

    if (Test-Path "$ProjectDir\00-system\core\orchestrator.md") {
        Log "[OK] Orchestrator found"
    } else {
        Log "✗ Orchestrator missing"
        $structureOk = $false
    }

    if (Test-Path "$ProjectDir\01-memory") {
        Log "[OK] Memory directory found"
    } else {
        Log "✗ Memory directory missing"
        $structureOk = $false
    }

    if (Test-Path "$ProjectDir\02-builds") {
        Log "[OK] Builds directory found"
    } else {
        Log "✗ Builds directory missing"
        $structureOk = $false
    }

    Pop-Location

    # Summary
    LogSection "INSTALLATION SUMMARY"

    if ($prereqsOk -and $structureOk) {
        Log "STATUS: SUCCESS"
        Log "Nexus is ready to use."
    } else {
        Log "STATUS: PARTIAL"
        Log "Some components may need attention. Review the log above."
    }

    Log ""
    Log "Run 'just cli' or 'claude' to start Nexus."
    Log "Run 'just install' for agentic validation of this installation."
}

# Run main
Main
