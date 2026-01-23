# Windows Version Requirements Research

**Date**: 2026-01-23
**Purpose**: Determine minimum Windows versions for installer components

---

## Summary

**Minimum Windows Version**: **Windows 10 Version 1809 (Build 17763)** or higher

This is the most restrictive requirement (winget), which sets the baseline for the entire installer.

---

## Component Requirements

### 1. Claude Code

**Minimum**: Windows 10+ (any version)

**Details**:
- Claude Code v2.x (2025+) runs **natively on Windows** via PowerShell/CMD
- No WSL required (unlike earlier versions)
- Supports Windows 10 and Windows 11

**Sources**:
- [Claude Code Setup Docs](https://code.claude.com/docs/en/setup)
- [Native Windows Installation Guide](https://smartscope.blog/en/generative-ai/claude/claude-code-windows-native-installation/)

---

### 2. winget (Windows Package Manager)

**Minimum**: **Windows 10 Version 1809 (Build 17763)** ⚠️ **MOST RESTRICTIVE**

**Details**:
- Included by default on Windows 11
- Available on Windows 10 1809+ via App Installer
- **NOT supported** on Windows Server 2019
- Experimental support on Windows Server 2022

**Sources**:
- [Microsoft Learn: Use WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
- [GitHub: winget-cli](https://github.com/microsoft/winget-cli)

---

### 3. PowerShell 5.1

**Minimum**: Windows 7 SP1 / Windows Server 2008 R2 SP1 (with WMF 5.1)

**Default Installation**:
- Windows 10 Version 1607+ (Anniversary Update)
- Windows Server 2016+

**Older OS Support**:
- Can be installed on Windows 7 SP1, 8.1, Server 2008 R2 SP1, Server 2012, Server 2012 R2
- Requires .NET Framework 4.5.2+

**Sources**:
- [Microsoft Learn: About Windows PowerShell 5.1](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_windows_powershell_5.1)
- [Download WMF 5.1](https://www.microsoft.com/en-us/download/details.aspx?id=54616)

---

## Installer Implications

### Our PowerShell Installer (install.ps1)

**Minimum Supported**: Windows 10 Version 1809 (Build 17763)

**Why**:
- Requires winget for Git installation
- PowerShell 5.1 already available on Win10 1809+
- Claude Code supports any Windows 10+

### Version Detection

Add to install.ps1:

```powershell
# Check Windows version
$osVersion = [System.Environment]::OSVersion.Version
$build = $osVersion.Build

if ($build -lt 17763) {
    Write-Error "This installer requires Windows 10 Version 1809 (Build 17763) or higher"
    Write-Info "Current build: $build"
    Write-Info "winget is not available on your Windows version"
    exit 1
}
```

### Fallback Strategy

If user is on older Windows (<1809):
1. Detect build number
2. Show error with current version
3. Provide manual installation links:
   - Claude Code: https://claude.com/download
   - Git: https://git-scm.com/download/win
   - uv: https://astral.sh/uv/install.ps1 (may work without winget)

---

## Windows Version Timeline

| Windows Version | Build Number | winget Support | PowerShell 5.1 | Claude Code |
|----------------|--------------|----------------|----------------|-------------|
| Windows 7 SP1 | 7601 | ❌ | ✅ (via WMF) | ❌ |
| Windows 8.1 | 9600 | ❌ | ✅ (via WMF) | ❌ |
| Windows 10 1607 | 14393 | ❌ | ✅ (default) | ✅ |
| Windows 10 1809 | 17763 | ✅ | ✅ | ✅ |
| Windows 10 21H2 | 19044 | ✅ | ✅ | ✅ |
| Windows 11 | 22000+ | ✅ | ✅ | ✅ |

---

## Recommendations

### 1. Update install.ps1 Header

```powershell
#Requires -Version 5.1

# Nexus One-Command Installer - PowerShell
# Minimum Windows Version: Windows 10 Version 1809 (Build 17763)
```

### 2. Add Version Check

Add OS version check at start of Main() function.

### 3. Update Documentation

Add to README.md:

**System Requirements (Windows)**:
- Windows 10 Version 1809 (Build 17763) or higher
- Windows 11 (all versions)
- PowerShell 5.1+ (included in supported Windows versions)

---

## Sources

- [Claude Code Setup Docs](https://code.claude.com/docs/en/setup)
- [Native Windows Installation Guide](https://smartscope.blog/en/generative-ai/claude/claude-code-windows-native-installation/)
- [Microsoft Learn: Use WinGet](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
- [GitHub: winget-cli](https://github.com/microsoft/winget-cli)
- [Microsoft Learn: About Windows PowerShell 5.1](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_windows_powershell_5.1)
- [Download WMF 5.1](https://www.microsoft.com/en-us/download/details.aspx?id=54616)
