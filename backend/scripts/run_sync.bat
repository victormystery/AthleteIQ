@echo off
REM Batch script to run Google Sheets sync
REM Can be scheduled with Windows Task Scheduler

echo ============================================
echo Google Sheets to CSV Sync
echo ============================================
echo.

cd /d "%~dp0"
cd ..\..

REM Activate Python environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

REM Run sync script
echo Running sync script...
python backend\scripts\sync_google_sheet.py

REM Check if successful
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Sync completed successfully!
) else (
    echo.
    echo ERROR: Sync failed with code %ERRORLEVEL%
)

echo.
echo ============================================
pause
