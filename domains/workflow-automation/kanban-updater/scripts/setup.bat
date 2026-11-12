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

:: 3. Settings file (URLs, PersonID, credentials, repos, schedule) - one JSON file outside the repo
echo.
echo ----------------------------------------------------------------
echo [?] Settings file: %%USERPROFILE%%\.config\kanban-updater\config.json
echo ----------------------------------------------------------------
python "%~dp0setup_environment.py" --init-config
for /f "usebackq delims=" %%P in (`python "%~dp0kanban_config.py" --path`) do set "CFG=%%P"
echo.
echo Remember: backslashes are doubled in JSON, for example DOMAIN\\name and D:\\work\\505\\*
set "OPEN_CFG="
set /p "OPEN_CFG=Open it in Notepad now to fill in your values? [Y/n]: "
if /i not "!OPEN_CFG!"=="n" (
    start "" /wait notepad "!CFG!"
)
echo To find your PersonID: run "python %~dp0synergy_fill.py check" (it detects it), or right-click
echo your name in Synergy -^> Open in new tab, and copy the number after HRMResourceCard.aspx?ID=

:: 3b. Weekday schedule from config.json (schedule block)
echo.
echo [*] Registering the weekday work-log schedule (Windows Task Scheduler)...
python "%~dp0schedule.py" sync

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
