@echo off
echo SHI Desktop App - Windows Debug Script
echo =======================================
echo.

:: Check if Python environment exists
if not exist python-env (
  echo Python environment not found! Please run win-setup.bat first.
  pause
  exit /b 1
)

:: Activate the Python environment
call python-env\Scripts\activate.bat

:: Create a debug log file
echo Creating debug log file...
echo SHI Desktop App Debug Log > debug.log
echo ====================== >> debug.log
echo. >> debug.log
echo Date: %date% Time: %time% >> debug.log
echo. >> debug.log

:: Check Python version
echo Checking Python version...
python --version >> debug.log 2>&1
echo. >> debug.log

:: List installed packages
echo Checking installed packages...
python -m pip list >> debug.log 2>&1
echo. >> debug.log

:: Check for streamlit
echo Checking streamlit installation...
python -c "import streamlit; print(f'Streamlit version: {streamlit.__version__}')" >> debug.log 2>&1
echo. >> debug.log

:: Check for numpy
echo Checking numpy installation...
python -c "import numpy; print(f'NumPy version: {numpy.__version__}')" >> debug.log 2>&1
echo. >> debug.log

:: Check for PIL
echo Checking Pillow installation...
python -c "import PIL; print(f'Pillow version: {PIL.__version__}')" >> debug.log 2>&1
echo. >> debug.log

:: Try running streamlit directly
echo Testing streamlit directly...
python -m streamlit --version >> debug.log 2>&1
echo. >> debug.log

:: Test app paths
echo Checking app paths...
python -c "import os; print(f'Current directory: {os.getcwd()}'); print(f'App directory exists: {os.path.exists(\"../app\")}'); print(f'gui.py exists: {os.path.exists(\"../app/gui.py\")}')" >> debug.log 2>&1
echo. >> debug.log

:: Try to manually run the streamlit app
echo Running streamlit app directly (this will open a new window)...
start cmd /c "call python-env\Scripts\activate.bat && python -m streamlit run ..\app\gui.py --server.headless=true"

echo.
echo Debug information saved to debug.log
echo A streamlit window should open. If it doesn't, check debug.log for errors.
echo.
echo You can now try to run: npx electron .
echo.

pause