@echo off
setlocal enabledelayedexpansion
title jinkou-chinou - Sync AI Skills

:: Check if Python is installed and on PATH
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python was not found on your PATH.
    echo Please install Python 3.10+ and make sure it is added to your environment PATH.
    echo.
    pause
    exit /b 1
)

:: Run the smart synchronization engine
python "%~dp0tools\sync_skills.py" %*
set "SYNC_EXIT=%ERRORLEVEL%"

echo.
:: If not run with --no-pause or /no-pause, pause so Explorer window doesn't close
echo %* | findstr /i "no-pause" >nul
if %ERRORLEVEL% NEQ 0 (
    pause
)

exit /b %SYNC_EXIT%
