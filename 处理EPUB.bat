@echo off
echo ======================================
echo EPUB Japanese Brightness
echo Drag an EPUB file onto this BAT file.
echo ======================================
echo.

if "%~1"=="" (
    echo Please drag an EPUB file onto this BAT file.
    echo.
    pause
    exit /b
)

set "PY_SCRIPT=%~dp0epub_language_brightness.py"

if not exist "%PY_SCRIPT%" (
    echo ERROR: Python script not found: %PY_SCRIPT%
    echo Keep this BAT file and epub_language_brightness.py in the same folder.
    pause
    exit /b
)

echo Processing: %~1
echo.
python "%PY_SCRIPT%" "%~1"
if errorlevel 1 (
    echo.
    echo FAILED. See the error message above.
    pause
    exit /b 1
)

echo.
echo --------------------------
echo Completed successfully.
echo The output EPUB is beside the input file.
echo --------------------------
pause
