@echo off
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONUTF8=1
if exist "%~dp0runtime\python.exe" (
  "%~dp0runtime\python.exe" "%~dp0samtv.py" setup
) else (
  py -3 "%~dp0samtv.py" setup
)
set RESULT=%ERRORLEVEL%
echo.
if not "%RESULT%"=="0" echo Setup stopped. Read docs\INSTALL.fa.md or docs\INSTALL.en.md.
pause
exit /b %RESULT%
