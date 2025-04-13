@echo off
echo SHI Desktop App - Windows Setup Script
echo =====================================
echo.

:: Check for Python
python --version 2>NUL
if %ERRORLEVEL% NEQ 0 (
  echo Python not found! Please install Python before continuing.
  echo Download from: https://www.python.org/downloads/
  echo Make sure to check "Add Python to PATH" during installation.
  pause
  exit /b 1
)

:: Create virtual environment
echo Creating Python virtual environment...
if exist python-env (
  echo Virtual environment already exists.
) else (
  python -m venv python-env
  if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
  )
  echo Virtual environment created successfully.
)

:: Activate virtual environment and install packages
echo Activating virtual environment and installing packages...
call python-env\Scripts\activate.bat

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

:: Install wheel and setuptools
echo Installing wheel and setuptools...
python -m pip install --upgrade wheel setuptools

:: Install packages from desktop-requirements.txt, preferring binary wheels
echo Installing packages (preferring pre-built wheels)...
python -m pip install --prefer-binary -r desktop-requirements.txt
if %ERRORLEVEL% NEQ 0 (
  echo.
  echo Warning: Some packages couldn't be installed. Retrying with pip's default behavior...
  echo.
  
  :: Try a simpler approach with core packages first
  echo Installing core dependencies one by one...
  python -m pip install numpy --upgrade
  python -m pip install Pillow --upgrade
  python -m pip install reportlab --upgrade
  python -m pip install tqdm --upgrade
  python -m pip install streamlit --upgrade
  
  :: Then try remaining packages
  python -m pip install -r desktop-requirements.txt
)

echo.
echo Python environment setup completed!
echo.
echo To complete setup, run these commands:
echo   npm install --no-scripts
echo.
echo To build the Windows installer:
echo   npx electron-builder --win
echo.

:: Create a package.json backup if not exists
if not exist package.json.bak (
  echo Creating backup of package.json...
  copy package.json package.json.bak
)

:: Modify package.json to remove postinstall script
echo Modifying package.json to remove postinstall script...
powershell -Command "(Get-Content package.json) -replace '\"postinstall\": \"node install.js\"', '\"_postinstall\": \"node install.js\"' | Set-Content package.json"

echo.
echo Ready to proceed with:
echo   npm install
echo.
echo Then build with:
echo   npx electron-builder --win
echo.

pause