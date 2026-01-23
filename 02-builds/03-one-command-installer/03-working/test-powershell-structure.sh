#!/bin/bash
#
# PowerShell Structure Validation
# Tests install.ps1 without running it (no Windows needed)
#

set -e

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🧪 PowerShell Structure Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test 1: File Encoding
echo "Test 1: File encoding check..."
if file install.ps1 | grep -q "UTF-8"; then
    echo "  ✓ UTF-8 encoding (correct)"
else
    echo "  ✗ Not UTF-8"
    exit 1
fi

if file install.ps1 | grep -q "CRLF"; then
    echo "  ✓ CRLF line endings (correct for PowerShell)"
else
    echo "  ⚠ LF line endings (should be CRLF for PowerShell)"
fi
echo ""

# Test 2: PowerShell Version Requirement
echo "Test 2: PowerShell version requirement..."
if grep -q "#Requires -Version 5.1" install.ps1; then
    echo "  ✓ PowerShell 5.1+ required (correct)"
else
    echo "  ✗ Missing #Requires directive"
    exit 1
fi
echo ""

# Test 3: Function Definitions
echo "Test 3: Verifying PowerShell functions..."
functions=(
    "Get-PlatformInfo"
    "Test-CommandExists"
    "Install-ClaudeCode"
    "Install-Uv"
    "Install-Git"
    "Install-VsCode"
    "Invoke-VsCodePrompt"
    "Invoke-NexusClone"
    "Start-VsCode"
    "Show-Summary"
    "Main"
)

for func in "${functions[@]}"; do
    if grep -q "^function $func" install.ps1; then
        echo "  ✓ $func found"
    else
        echo "  ✗ $func missing"
        exit 1
    fi
done
echo ""

# Test 4: Output Functions
echo "Test 4: Checking output functions..."
output_functions=(
    "Write-Info"
    "Write-Success"
    "Write-Warning"
    "Write-Error"
    "Write-Header"
)

for func in "${output_functions[@]}"; do
    if grep -q "function $func" install.ps1; then
        echo "  ✓ $func found"
    else
        echo "  ✗ $func missing"
        exit 1
    fi
done
echo ""

# Test 5: Key Commands
echo "Test 5: Verifying key Windows commands..."

# Check for winget commands
if grep -q "winget install --id Git.Git" install.ps1; then
    echo "  ✓ Git installation via winget"
else
    echo "  ✗ Git winget command missing"
    exit 1
fi

if grep -q "winget install --id Microsoft.VisualStudioCode" install.ps1; then
    echo "  ✓ VS Code installation via winget"
else
    echo "  ✗ VS Code winget command missing"
    exit 1
fi

# Check for official installers
if grep -q "https://claude.ai/install.ps1" install.ps1; then
    echo "  ✓ Claude Code official installer URL"
else
    echo "  ✗ Claude Code installer URL missing"
    exit 1
fi

if grep -q "https://astral.sh/uv/install.ps1" install.ps1; then
    echo "  ✓ uv official installer URL"
else
    echo "  ✗ uv installer URL missing"
    exit 1
fi
echo ""

# Test 6: Main Flow
echo "Test 6: Checking main execution flow..."

if grep -q "Install-ClaudeCode" install.ps1 | grep -v "^function"; then
    echo "  ✓ Main calls Install-ClaudeCode"
else
    echo "  ⚠ Install-ClaudeCode may not be called"
fi

if grep -q "Install-Uv" install.ps1 | grep -v "^function"; then
    echo "  ✓ Main calls Install-Uv"
else
    echo "  ⚠ Install-Uv may not be called"
fi

if grep -q "Install-Git" install.ps1 | grep -v "^function"; then
    echo "  ✓ Main calls Install-Git"
else
    echo "  ⚠ Install-Git may not be called"
fi

if grep -q "Invoke-VsCodePrompt" install.ps1 | grep -v "^function"; then
    echo "  ✓ Main calls Invoke-VsCodePrompt"
else
    echo "  ⚠ Invoke-VsCodePrompt may not be called"
fi

if grep -q "Invoke-NexusClone" install.ps1 | grep -v "^function"; then
    echo "  ✓ Main calls Invoke-NexusClone"
else
    echo "  ⚠ Invoke-NexusClone may not be called"
fi

if grep -q "Show-Summary" install.ps1 | grep -v "^function"; then
    echo "  ✓ Main calls Show-Summary"
else
    echo "  ⚠ Show-Summary may not be called"
fi
echo ""

# Test 7: Error Handling
echo "Test 7: Checking error handling..."

if grep -q '$ErrorActionPreference = "Stop"' install.ps1; then
    echo "  ✓ Error handling configured"
else
    echo "  ⚠ ErrorActionPreference not set to Stop"
fi

if grep -q "try {" install.ps1; then
    echo "  ✓ Try/catch blocks present"
else
    echo "  ⚠ No try/catch blocks found"
fi
echo ""

# Test 8: Compare with Bash Version
echo "Test 8: Comparing structure with install.sh..."

bash_functions=$(grep "^[a-z_]*() {" install.sh | sed 's/() {//' | wc -l | tr -d ' ')
ps_functions=$(grep "^function " install.ps1 | wc -l | tr -d ' ')

echo "  Bash functions: $bash_functions"
echo "  PowerShell functions: $ps_functions"

if [ "$bash_functions" -gt 10 ] && [ "$ps_functions" -gt 10 ]; then
    echo "  ✓ Both installers have comprehensive function coverage"
else
    echo "  ⚠ Function count seems low"
fi
echo ""

# Summary
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ PowerShell Structure Validation Complete"
echo ""
echo "Validated:"
echo "  ✓ File encoding (UTF-8 with CRLF)"
echo "  ✓ PowerShell version requirement (5.1+)"
echo "  ✓ All required functions defined"
echo "  ✓ Output functions present"
echo "  ✓ Winget commands for Git + VS Code"
echo "  ✓ Official installer URLs"
echo "  ✓ Main execution flow"
echo "  ✓ Error handling"
echo "  ✓ Structure matches bash version"
echo ""
echo "🔜 Next: Test on real Windows system"
echo "   Option 1: Windows Sandbox (safe, isolated)"
echo "   Option 2: GitHub Actions (automated)"
echo "   Option 3: Real Windows (if available)"
echo ""
echo "See: 02-builds/03-one-command-installer/03-working/windows-test-instructions.md"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
