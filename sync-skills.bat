@echo off
setlocal enabledelayedexpansion
title jinkou-chinou - Sync AI Skills

:: Check if user explicitly requested the PowerShell engine (--powershell / --use-ps1)
set "FORCE_PS1=0"
echo %* | findstr /i "powershell use-ps1" >nul
if %ERRORLEVEL% EQU 0 (
    set "FORCE_PS1=1"
)

:: Check if a real Python interpreter is installed (python --version avoids Windows Store stub traps)
set "HAS_PYTHON=0"
if "%FORCE_PS1%"=="0" (
    python --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "HAS_PYTHON=1"
    )
)

if "%HAS_PYTHON%"=="1" (
    :: Run the Python smart synchronization engine
    python "%~dp0tools\sync_skills.py" %*
    set "SYNC_EXIT=!ERRORLEVEL!"
) else (
    if "%FORCE_PS1%"=="0" (
        echo [INFO] Python was not found on PATH. Falling back to native PowerShell engine...
        echo.
    )
    :: Run the zero-dependency PowerShell smart synchronization engine
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0tools\sync_skills.ps1" --no-pause %*
    set "SYNC_EXIT=!ERRORLEVEL!"
)

echo.
:: If not run with --no-pause or /no-pause, pause so Explorer window doesn't close
echo %* | findstr /i "no-pause" >nul
if %ERRORLEVEL% NEQ 0 (
    pause
)

exit /b %SYNC_EXIT%
