@echo off
setlocal
call "%~dp0domains\workflow-automation\kanban-updater\scripts\setup.bat" %*
exit /b %ERRORLEVEL%
