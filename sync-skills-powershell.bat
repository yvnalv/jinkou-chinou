@echo off
setlocal
call "%~dp0sync-skills.bat" --powershell %*
exit /b %ERRORLEVEL%

