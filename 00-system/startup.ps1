
# startup.ps1 - Robust Nexus Startup Script
# Usage: ./00-system/startup.ps1

# 1. Force UTF-8 Encoding globally for this session
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 1. Force UTF-8 Encoding globally for this session
$env:PYTHONUTF8 = "1"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Ensure cache directory exists
$cacheDir = "00-system/.cache"
if (-not (Test-Path $cacheDir)) {
    New-Item -ItemType Directory -Force -Path $cacheDir | Out-Null
}

Write-Host "🚀 Nexus-v4 Startup Sequence..." -ForegroundColor Cyan

# 2. Run Core Context Load (Fast, Essential)
# We capture to file to avoid ANY terminal buffer truncation risks
Write-Host "1/2 Loading Core System Context..." -NoNewline
python 00-system/core/nexus-loader.py --startup --no-metadata > "$cacheDir/context_core.json"
if ($LASTEXITCODE -eq 0) { Write-Host " OK" -ForegroundColor Green } else { Write-Host " FAILED" -ForegroundColor Red; exit }

# 3. Run Metadata Load (Full Project/Skill Register)
# This is the heavy part that usually causes truncation
Write-Host "2/2 Loading Metadata Registry..." -NoNewline
python 00-system/core/nexus-loader.py --metadata > "$cacheDir/context_metadata.json"
if ($LASTEXITCODE -eq 0) { Write-Host " OK" -ForegroundColor Green } else { Write-Host " FAILED" -ForegroundColor Red; exit }

# 4. Display the System Menu from Core Context
# We read the JSON file directly in PowerShell to avoid Python printing issues
$core = Get-Content -Raw -Encoding UTF8 "$cacheDir/context_core.json" | ConvertFrom-Json

# Quick check for update banner or other hints
if ($core.stats.display_hints) {
    echo ""
    $core.stats.display_hints | ForEach-Object { Write-Host "⚠️  $_" -ForegroundColor Yellow }
}

# The Menu is buried in the 'instructions.message' or we can trigger the display
# But actually, the cleanest way is to let Python render JUST the menu if we want visual confirmation
# OR we simply tell the user "System Loaded. Read 'context_core.json' for state."

# However, for the AI Agent (me), I just need to read the files I just created.
Write-Host "`n✅ System Ready." -ForegroundColor Green
Write-Host "   Core Context:   $PWD/$cacheDir/context_core.json" -ForegroundColor Gray
Write-Host "   Metadata:       $PWD/$cacheDir/context_metadata.json" -ForegroundColor Gray
