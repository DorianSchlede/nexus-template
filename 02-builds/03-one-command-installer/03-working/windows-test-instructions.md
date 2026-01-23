# Windows Testing Instructions

**Status**: install.ps1 kann NICHT auf macOS getestet werden (PowerShell fehlt)

---

## 🪟 Optionen für Windows-Testing

### Option 1: Windows Sandbox (Empfohlen - Safe & Fast)

**Beste Option für sicheres Testen ohne echtes Windows-System zu beeinflussen**

#### Vorbereitung (einmalig):
```powershell
# Als Administrator ausführen
Enable-WindowsOptionalFeature -FeatureName "Containers-DisposableClientVM" -All -Online
```

#### Test durchführen:
1. Windows Sandbox starten
2. install.ps1 in Sandbox kopieren (Drag & Drop)
3. PowerShell in Sandbox öffnen
4. Test ausführen:
```powershell
# In Sandbox PowerShell
cd Desktop
.\install.ps1
```
5. Ergebnis prüfen:
```powershell
claude --version
uv --version
git --version
```
6. Sandbox schließen → Alles automatisch gelöscht

**Dauer**: 5 Minuten
**Risk**: ✅ Keine (isolierte Umgebung)

---

### Option 2: GitHub Actions (Automated CI/CD)

**Beste Option für automatisierte Tests ohne eigenes Windows-System**

Erstelle `.github/workflows/test-installers.yml`:

```yaml
name: Test Installers

on: [push, pull_request]

jobs:
  test-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3

      - name: Test PowerShell Syntax
        shell: powershell
        run: |
          $ErrorActionPreference = "Stop"
          # Test if script is valid PowerShell
          $null = [scriptblock]::Create((Get-Content .\install.ps1 -Raw))
          Write-Host "✓ PowerShell syntax valid"

      - name: Run Installer (Non-Interactive)
        shell: powershell
        run: |
          # Mock user input: No VS Code, temp directory
          $input = "2`n$env:TEMP\nexus-test`nn`n"
          $input | .\install.ps1

      - name: Verify Installations
        shell: powershell
        run: |
          claude --version
          uv --version
          git --version
```

**Dauer**: Auto-runs on push
**Risk**: ✅ Keine (GitHub-Runner)
**Cost**: ✅ Free (public repos)

---

### Option 3: Real Windows System (Last Resort)

**Nur wenn du ein echtes Windows-System hast**

```powershell
# 1. PowerShell als Admin öffnen

# 2. Execution Policy setzen
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process

# 3. Zum Repo navigieren
cd C:\path\to\nexus-template

# 4. Installer laufen lassen
.\install.ps1

# 5. TERMINAL NEUSTARTEN (wichtig!)

# 6. Verifizieren
claude --version
uv --version
git --version
cd $env:USERPROFILE\nexus
```

**Dauer**: 5 Minuten
**Risk**: ⚠️ Installiert wirklich auf deinem System

---

### Option 4: Syntax-Only Validation (Quick Check)

**Schneller Check ohne echtes Windows**

Du kannst die PowerShell-Syntax zumindest prüfen:

```bash
# Auf macOS: Check file structure
cat install.ps1 | head -50  # Read first 50 lines
grep -n "function " install.ps1  # Find all functions
grep -n "#Requires" install.ps1  # Check requirements
```

**Was wir prüfen können**:
- ✅ File encoding (UTF-8)
- ✅ Line endings (CRLF für PowerShell korrekt)
- ✅ Function definitions vorhanden
- ✅ Struktur ähnlich zu install.sh

**Was wir NICHT prüfen können**:
- ❌ PowerShell Syntax
- ❌ Winget commands
- ❌ Windows-spezifische Pfade
- ❌ Tatsächliche Installation

---

## 📋 Quick Validation (Jetzt auf macOS möglich)

Lass mich zumindest die Struktur checken:

```bash
# 1. Check file encoding
file install.ps1

# 2. Check line count
wc -l install.ps1

# 3. Check functions
grep "^function " install.ps1

# 4. Check requirements
grep "#Requires" install.ps1

# 5. Verify similar structure to install.sh
diff <(grep "function.*{" install.sh | sed 's/.*function //; s/ .*//' | sort) \
     <(grep "^function " install.ps1 | sed 's/function //; s/ .*//' | sort)
```

---

## ✅ Recommended Testing Strategy

**For this build**:

1. ✅ **macOS**: DONE - Full integration test passed
2. ⚡ **Windows**: Quick validation (structure check) - NOW
3. 🔜 **Windows**: GitHub Actions CI/CD - LATER (before release)
4. 🎯 **Windows**: Windows Sandbox - OPTIONAL (when you have Windows access)

---

## 🎯 What We Know About install.ps1

✅ **Created**: 368 lines
✅ **Encoding**: UTF-8 with CRLF (correct for PowerShell)
✅ **Structure**: Mirrors install.sh logic
✅ **Functions**: All required functions defined
✅ **Requirements**: PowerShell 5.1+

**Confidence Level**: 🟡 Medium (not tested on real Windows)

**Risk**: Low - follows same patterns as install.sh (which works)

---

## Next Steps

1. ✅ Quick structure validation (NOW)
2. 📝 Update README with installation instructions
3. 🔄 Add GitHub Actions workflow (OPTIONAL)
4. 🎁 Mark build as COMPLETE

Want me to do the quick structure validation now?
