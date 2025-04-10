@echo off
echo =========================
echo Launching the application
echo =========================

:: Try to launch the app
start "" streamlit run app/gui.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Could not launch Streamlit.
    echo Make sure Python is installed and the dependencies are set up.
    pause
)
