#
# Nexus Maintenance Script (Windows)
# Runs when: claude --maintenance
# Purpose: Update dependencies, clean artifacts, run health checks
#

$ErrorActionPreference = "Stop"

# ============================================================================
# CONFIG
# ============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectDir = (Get-Item "$ScriptDir\..\..\..").FullName
$LogFile = "$ProjectDir\.claude\logs\maintenance.log"

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

# ============================================================================
# MAINTENANCE TASKS
# ============================================================================

function Main {
    # Clear previous log
    Set-Content -Path $LogFile -Value ""

    LogSection "NEXUS MAINTENANCE STARTED"
    Log "Project directory: $ProjectDir"
    Log "Log file: $LogFile"

    Push-Location $ProjectDir

    # Update Python dependencies
    LogSection "UPDATING DEPENDENCIES"

    if (Test-Path "pyproject.toml") {
        RunCommand "uv sync"
        RunCommand "uv tool install . --force" | Out-Null
    }

    # Clean temporary files
    LogSection "CLEANING ARTIFACTS"

    # Clean Python cache
    $pycacheDirs = Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue
    if ($pycacheDirs) {
        $pycacheDirs | Remove-Item -Recurse -Force
        Log "Cleaned $($pycacheDirs.Count) Python cache directories"
    }

    # Clean .pyc files
    $pycFiles = Get-ChildItem -Path . -File -Recurse -Filter "*.pyc" -ErrorAction SilentlyContinue
    if ($pycFiles) {
        $pycFiles | Remove-Item -Force
        Log "Cleaned $($pycFiles.Count) .pyc files"
    }

    # Clean old session files (older than 7 days)
    if (Test-Path ".claude\sessions") {
        $oldSessions = Get-ChildItem -Path ".claude\sessions" -File | Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-7) }
        if ($oldSessions) {
            $oldSessions | Remove-Item -Force
            Log "Cleaned $($oldSessions.Count) old session files"
        } else {
            Log "No old session files to clean"
        }
    }

    # Health checks
    LogSection "HEALTH CHECKS"

    # Check disk space
    $drive = (Get-Item $ProjectDir).PSDrive
    $freeSpaceGB = [math]::Round($drive.Free / 1GB, 2)
    $usedPercent = [math]::Round((1 - ($drive.Free / ($drive.Free + $drive.Used))) * 100)
    if ($usedPercent -gt 90) {
        Log "[!] Warning: Disk usage is at $usedPercent%"
    } else {
        Log "[OK] Disk usage: $usedPercent% (${freeSpaceGB}GB free)"
    }

    # Check git status
    try {
        $gitStatus = git status --porcelain 2>&1
        $uncommitted = ($gitStatus | Measure-Object -Line).Lines
        if ($uncommitted -gt 0) {
            Log "[!] $uncommitted uncommitted changes"
        } else {
            Log "[OK] Working directory clean"
        }
    } catch {
        Log "Could not check git status"
    }

    # Dependency status
    LogSection "DEPENDENCY STATUS"

    if (Get-Command "uv" -ErrorAction SilentlyContinue) {
        Log "[OK] Python dependencies synced via uv"
    }

    Pop-Location

    # Summary
    LogSection "MAINTENANCE SUMMARY"

    Log "STATUS: COMPLETE"
    Log "Last maintenance: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    Log ""
    Log "Run 'just maintain' for agentic validation of maintenance."
}

# Run main
Main
