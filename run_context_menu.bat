@echo off
cd /d "%~dp0"
echo ============================================================
echo Starting Discord video compression from context menu...
echo ============================================================

if "%~1"=="" (
    echo Error: No file path provided.
    echo.
    pause
    exit /b
)

python src\main.py "%~1"
echo.
pause
