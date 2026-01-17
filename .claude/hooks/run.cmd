@echo off
setlocal EnableDelayedExpansion
REM Universal hook runner for Windows (cmd/PowerShell)
REM Works on: Windows 10/11 native
REM
REM Usage: .claude\hooks\run.cmd script.py [args...]
REM
REM Features:
REM - Searches common uv locations
REM - Outputs diagnostic JSON for Claude if hook fails
REM - For Unix systems, use: .claude/hooks/run

REM Get script name (first argument)
set "SCRIPT=%~1"
shift

REM Build remaining args
set "ARGS="
:argloop
if "%~1"=="" goto endargloop
set "ARGS=!ARGS! %1"
shift
goto argloop
:endargloop

REM Function to output error (inline since batch doesn't have real functions)
REM Check if this is session_start for special error handling
echo %SCRIPT% | findstr /i "session_start" >nul
if %errorlevel%==0 (
    set "IS_SESSION_START=1"
) else (
    set "IS_SESSION_START=0"
)

REM Try to find uv
set "UV_PATH="

if exist "%USERPROFILE%\.local\bin\uv.exe" (
    set "UV_PATH=%USERPROFILE%\.local\bin\uv.exe"
    goto found_uv
)

if exist "%LOCALAPPDATA%\uv\uv.exe" (
    set "UV_PATH=%LOCALAPPDATA%\uv\uv.exe"
    goto found_uv
)

if exist "%USERPROFILE%\.cargo\bin\uv.exe" (
    set "UV_PATH=%USERPROFILE%\.cargo\bin\uv.exe"
    goto found_uv
)

REM Try PATH as fallback
where uv >nul 2>&1
if %errorlevel%==0 (
    set "UV_PATH=uv"
    goto found_uv
)

REM uv not found - output error for Claude
if "%IS_SESSION_START%"=="1" (
    echo {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<nexus-context version=\"v4\" mode=\"error\">\n  <error type=\"hook_execution_failed\">\n    <message>uv not found on Windows. Install with: irm https://astral.sh/uv/install.ps1 ^| iex</message>\n    <script>%SCRIPT%</script>\n  </error>\n  <instruction importance=\"MANDATORY\">\n    HOOK EXECUTION FAILED. To fix:\n    1. Open PowerShell and run: irm https://astral.sh/uv/install.ps1 ^| iex\n    2. Restart your terminal/VSCode\n    3. Run /clear to reload context\n    \n    For now, read 00-system/core/orchestrator.md and display menu.\n  </instruction>\n</nexus-context>"}}
) else (
    echo {"error":"uv not found on Windows","script":"%SCRIPT%"}
)
exit /b 0

:found_uv
REM Run the hook
"%UV_PATH%" run %SCRIPT% %ARGS%
set "EXIT_CODE=%errorlevel%"

REM If failed, output diagnostic
if not "%EXIT_CODE%"=="0" (
    if "%IS_SESSION_START%"=="1" (
        echo {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"<nexus-context version=\"v4\" mode=\"error\">\n  <error type=\"hook_execution_failed\">\n    <message>Hook exited with code %EXIT_CODE%</message>\n    <script>%SCRIPT%</script>\n  </error>\n  <instruction importance=\"MANDATORY\">\n    HOOK EXECUTION FAILED. Check the hook script for errors.\n    For now, read 00-system/core/orchestrator.md and display menu.\n  </instruction>\n</nexus-context>"}}
    ) else (
        echo {"error":"Hook exited with code %EXIT_CODE%","script":"%SCRIPT%"}
    )
    exit /b 0
)

endlocal
