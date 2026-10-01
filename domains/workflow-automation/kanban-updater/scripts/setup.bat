@echo off
setlocal enabledelayedexpansion
title kanban-updater - Environment & Playwright Setup

echo ================================================================
echo       kanban-updater - Environment ^& Dependency Setup
echo ================================================================
echo.

:: 1. Check if Python is installed
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python 3.10+ was not found on your PATH.
    echo Please install Python from https://www.python.org/ or the Microsoft Store,
    echo and ensure "Add Python to PATH" is checked.
    echo.
    pause
    exit /b 1
)

:: 2. Run dependency installer via setup_environment.py
echo [*] Installing Playwright and verifying browser requirements...
python "%~dp0setup_environment.py" --install
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [FAILED] Playwright installation encountered an error.
    echo Please check your internet connection or Python pip permissions.
    echo.
    pause
    exit /b 1
)

:: 2b. Ensure shared profile junctions across all AI folders
echo.
echo [*] Linking shared Edge profile across all local AI agent folders...
python "%~dp0setup_environment.py" --link-profiles

:: 3. Optional PersonID configuration
echo.
echo ----------------------------------------------------------------
echo [?] Exact Synergy PersonID Configuration
echo ----------------------------------------------------------------
echo To find your PersonID:
echo   1. Log in to https://synergy.glmsystems.com/
echo   2. Right-click your name link at top-right -^> Open in new tab
echo   3. Look at the URL: HRMResourceCard.aspx?ID=^<PersonID^>
echo.
set "USER_PID="
set /p "USER_PID=Enter your numeric PersonID (or press Enter to skip / auto-discover): "
if not "!USER_PID!"=="" (
    python "%~dp0setup_environment.py" --set-person-id "!USER_PID!"
)

:: 4. Final Environment Diagnostic Check
echo.
echo ================================================================
echo               FINAL ENVIRONMENT DIAGNOSTIC CHECK
echo ================================================================
python "%~dp0setup_environment.py" --check

echo.
echo ================================================================
echo Setup completed!
echo - You can now invoke /kanban-updater in your AI agent.
echo - To re-run diagnostics anytime: python "%~dp0setup_environment.py" --check
echo ================================================================
echo.
pause
exit /b 0
