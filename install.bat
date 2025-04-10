@echo off
echo ================================
echo Installing required libraries...
echo ================================

:: Check if pip is available
pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: pip is not installed or not in your PATH.
    echo Please install Python from https://www.python.org and make sure to check the "Add Python to PATH" option.
    pause
    exit /b
)

pip install -r requirements.txt

IF %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo Installation successful!
    echo You can now run the app by double-clicking run.bat
    echo ====================================
) ELSE (
    echo.
    echo ================================
    echo ERROR: Something went wrong during installation.
    echo Please check the error message above.
    echo ================================
)

pause
