@echo off
setlocal
call "%~dp0..\sync-skills.bat" %*
exit /b %ERRORLEVEL%
