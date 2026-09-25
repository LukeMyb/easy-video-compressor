@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Discord video compression from clipboard path...
echo ============================================================

set "CLIPBOARD_TEXT="
for /f "tokens=*" %%i in ('powershell -NoProfile -Command "Get-Clipboard"') do set "CLIPBOARD_TEXT=%%i"

if not defined CLIPBOARD_TEXT (
    echo Clipboard is empty or no text was copied.
    echo Please copy the path of the video first and run again.
    echo.
    pause
    exit /b
)

REM Remove double quotes from the path
set "CLIPBOARD_TEXT=%CLIPBOARD_TEXT:"=%"

python src\main.py "%CLIPBOARD_TEXT%"
echo.
pause
