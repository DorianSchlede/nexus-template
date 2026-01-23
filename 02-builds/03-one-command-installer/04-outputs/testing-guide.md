# Testing Guide for Installers

**Purpose**: How to test install.sh (macOS) and install.ps1 (Windows)

---

## macOS Testing (install.sh)

### Option 1: Test on Your Current macOS System

**⚠️ Warning**: This will actually install Claude Code, uv, and Git if not present

```bash
# 1. Navigate to repo
cd /path/to/nexus-template

# 2. Run installer
./install.sh

# 3. Answer prompts:
#    - VS Code? → Choose 1 (yes) or 2 (no)
#    - Nexus directory? → Enter path (default: ~/nexus)

# 4. Verify installations
claude --version
uv --version
git --version
```

### Option 2: Dry-Run Test (Safe)

Test without installing (just checks logic):

```bash
# Check syntax
bash -n install.sh

# View what would happen (read the script)
less install.sh

# Test individual functions manually
source install.sh
detect_platform
check_tool claude "Claude Code"
```

### Option 3: macOS Virtual Machine (Safest)

Use UTM or Parallels to create a fresh macOS VM:

1. Create macOS VM
2. Copy install.sh to VM
3. Run installer
4. Verify tools installed
5. Delete VM

---

## Windows Testing (install.ps1)

### Option 1: Test on Your Windows System

**⚠️ Warning**: This will actually install Claude Code, uv, Git, and optionally VS Code

```powershell
# 1. Open PowerShell as Administrator

# 2. Allow script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 3. Navigate to repo
cd C:\path\to\nexus-template

# 4. Run installer
.\install.ps1

# 5. Answer prompts:
#    - VS Code? → Choose 1 (yes) or 2 (no)
#    - Nexus directory? → Enter path (default: C:\Users\YourName\nexus)

# 6. RESTART TERMINAL (important for PATH)

# 7. Verify installations
claude --version
uv --version
git --version
```

### Option 2: Windows Sandbox (Safe)

Use Windows Sandbox for testing:

1. Enable Windows Sandbox (Windows 11 Pro/Enterprise)
2. Start Sandbox
3. Copy install.ps1 to Sandbox
4. Run installer
5. Close Sandbox (auto-deletes everything)

**How to enable Windows Sandbox**:
```powershell
# Run as Administrator
Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online
```

### Option 3: Syntax Check (No Installation)

Test without installing:

```powershell
# Check PowerShell syntax
Get-Command -Syntax .\install.ps1

# View script content
Get-Content .\install.ps1 | Select-Object -First 50

# Test individual functions manually
. .\install.ps1
Get-PlatformInfo
Test-CommandExists "git" "Git"
```

---

## Full Test Matrix

| Platform | Test Method | Installation | Time | Safety |
|----------|-------------|--------------|------|--------|
| **macOS** | Run ./install.sh | ✅ Real | 3-5 min | ⚠️ Modifies system |
| **macOS** | Syntax check | ❌ None | 5 sec | ✅ Safe |
| **macOS** | UTM VM | ✅ Real | 10 min | ✅ Safe (isolated) |
| **Windows** | Run install.ps1 | ✅ Real | 3-5 min | ⚠️ Modifies system |
| **Windows** | Windows Sandbox | ✅ Real | 5 min | ✅ Safe (auto-delete) |
| **Windows** | Syntax check | ❌ None | 5 sec | ✅ Safe |

---

## What to Test

### ✅ Must Test

1. **Fresh Install** (no tools installed)
   - Installer detects missing tools
   - Downloads and installs all components
   - PATH updated correctly
   - Nexus cloned successfully

2. **Existing Tools** (Claude/uv/Git already installed)
   - Installer detects existing installations
   - Skips re-installation
   - No errors or conflicts

3. **VS Code Prompt**
   - Choosing "Yes" installs VS Code
   - Choosing "No" skips VS Code
   - VS Code opens Nexus directory (if installed)

4. **PATH Updates**
   - Tools accessible after terminal restart
   - Warning message displayed if PATH changed

5. **Idempotency** (run twice)
   - Second run detects existing installations
   - No errors or duplicate installations
   - Safe to run multiple times

### 🔍 Nice to Test

6. **Error Handling**
   - Network failure (disconnect WiFi mid-install)
   - Permission denied (non-admin on Windows)
   - Disk full
   - Invalid directory path

7. **User Input**
   - Cancel/abort during prompts
   - Invalid directory names
   - Overwrite existing Nexus directory

---

## Recommended Testing Flow

### For macOS:

```bash
# 1. Quick validation (safe)
bash -n install.sh
./02-builds/03-one-command-installer/03-working/quick-test.sh

# 2. Real test (your system or VM)
./install.sh

# 3. Verify
claude --version
uv --version
git --version
ls ~/nexus

# 4. Test idempotency
./install.sh  # Run again, should skip installed tools
```

### For Windows:

```powershell
# 1. Quick validation (safe)
Get-Command -Syntax .\install.ps1

# 2. Real test (Windows Sandbox recommended)
.\install.ps1

# 3. RESTART PowerShell

# 4. Verify
claude --version
uv --version
git --version
ls $env:USERPROFILE\nexus

# 5. Test idempotency
.\install.ps1  # Run again, should skip installed tools
```

---

## Expected Results

### Success Indicators:

✅ All tools report versions:
```
claude 2.x.x
uv 0.9.x
git 2.x.x
```

✅ Nexus directory created:
```
~/nexus/  (macOS/Linux)
C:\Users\YourName\nexus\  (Windows)
```

✅ VS Code opens (if chosen)

✅ Summary displays installed components

✅ Next steps shown

### Common Issues:

❌ **"Command not found" after install**
- Solution: Restart terminal to load new PATH

❌ **"Permission denied" (macOS)**
- Solution: Run `chmod +x install.sh`

❌ **"Execution policy" error (Windows)**
- Solution: `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`

❌ **Git Bash missing on Windows**
- Expected: Installer uses winget to install Git for Windows

---

## Quick Test Commands

### macOS:
```bash
# Syntax only
bash -n install.sh && echo "✓ Syntax valid"

# Quick mock test
./02-builds/03-one-command-installer/03-working/quick-test.sh
```

### Windows:
```powershell
# Syntax only
$null = [scriptblock]::Create((Get-Content .\install.ps1 -Raw))
Write-Host "✓ Syntax valid"
```

---

## Final Recommendation

**Best testing approach**:

1. **Syntax validation** (5 seconds, safe)
2. **Windows Sandbox** (5 min, safe) OR **macOS VM** (10 min, safe)
3. **Real system** (3-5 min, only after VM test succeeds)

This ensures thorough testing without risk to your development environment.
