# SHI Desktop App Build Guide

This guide explains how to build and package the SHI desktop application for various platforms, with special attention to Windows compatibility.

## Setting Up the Development Environment

Before building, you need to set up the development environment:

```bash
# Clone the repository
git clone <repository-url>
cd SHI

# Navigate to the desktop-app directory
cd desktop-app
```

## Windows Build Guide

### Prerequisites for Windows

- **Node.js**: Version 14+ and npm ([Download](https://nodejs.org/))
- **Python**: Any version (3.9+ recommended, but 3.13+ will work too)
- **Windows**: Windows 10/11

### Simplified Windows Setup (Recommended)

Use this approach for any Python version, including 3.13+:

1. **Run the Windows setup script**:
   ```
   # Double-click win-setup.bat in the desktop-app folder
   # OR run it from command prompt:
   win-setup.bat
   ```

   This script:
   - Creates a Python virtual environment
   - Installs compatible pre-built wheels from desktop-requirements.txt
   - Automatically modifies package.json to avoid installation issues
   - Works with any Python version including 3.13+

2. **Install Node.js dependencies**:
   ```
   npm install
   ```
   (The script disables the problematic postinstall hook automatically)

3. **Build the Windows installer**:
   ```
   npx electron-builder --win
   ```

The installable .exe will be in the `dist` folder.

### Step-by-Step Manual Process

If you prefer to understand each step, here's the manual process:

1. **Create and activate a Python virtual environment**:
   ```
   python -m venv python-env
   python-env\Scripts\activate.bat
   ```

2. **Install dependencies from the desktop-requirements.txt file**:
   ```
   pip install -r desktop-requirements.txt
   ```

3. **Make a backup of package.json and disable the postinstall script**:
   ```
   copy package.json package.json.bak
   ```
   Then edit package.json to rename "postinstall" to "_postinstall"

4. **Install Node.js dependencies**:
   ```
   npm install
   ```

5. **Build the Windows installer**:
   ```
   npx electron-builder --win
   ```

## Building for macOS

### Prerequisites for macOS

- Node.js 14+ and npm
- Python 3.9+
- macOS 10.15+ (Catalina or later)
- Xcode or Xcode Command Line Tools

### macOS Setup

```bash
# Install dependencies and set up Python env
npm install

# Build for macOS
npm run build:mac
```

For code signing:

```bash
# Set your developer identity
export CSC_IDENTITY_AUTO_DISCOVERY=true
# or
export CSC_NAME="Your Developer Name"

# Then build
npm run build:mac
```

## Building for Linux

### Prerequisites for Linux

- Node.js 14+ and npm
- Python 3.9+
- Required system libraries

```bash
# Debian/Ubuntu
sudo apt update
sudo apt install -y libgconf-2-4 libgtk-3-0 libnotify4 libnss3 libxss1 libxtst6 xdg-utils libatspi2.0-0 libuuid1

# Fedora
sudo dnf install -y libXScrnSaver GConf2 libnotify libXtst nss at-spi2-core libuuid
```

### Linux Setup

```bash
# Install dependencies and set up Python env
npm install

# Build for Linux
npm run build:linux
```

## Troubleshooting Windows Builds

### Common Windows Issues

1. **Python version compatibility**:
   - **Problem**: "Cannot import 'mesonpy'" or "Failed to build wheel for numpy"
   - **Solution**: Use the `win-setup.bat` script which installs pre-built wheels

2. **Missing C++ compiler**:
   - **Problem**: "Microsoft Visual C++ 14.0 or greater is required"
   - **Solutions**:
     - Use `win-setup.bat` (preferred)
     - Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

3. **PowerShell execution policy**:
   - **Problem**: "Running scripts is disabled on this system"
   - **Solution**: Run PowerShell as Administrator and execute:
     ```
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

4. **Running the correct commands**:
   - Always use `npx electron-builder --win` if `npm run build:win` fails

5. **Python package installation errors**:
   - Use the `win-setup.bat` script which installs compatible versions 
   - Avoid Python 3.13+ for maximum compatibility

### Detailed Troubleshooting

For detailed troubleshooting, check:
- npm logs: `%USERPROFILE%\AppData\Local\npm-cache\_logs\`
- Build logs: `desktop-app\dist\builder-debug.yml`
- Python install logs: Run `win-setup.bat` and check the output

## Customizing the Build

You can customize the build by editing `package.json`:

- Change app name and description in the top section
- Modify the build configuration in the `"build"` section
- Update the app icon by replacing the files in `src/assets/`

## Creating a Release

When creating a release:

1. Update the version number in `package.json`
2. Build for all target platforms (recommended: build on each target OS)
3. Test the built applications on each platform
4. Create a release archive with the built applications
5. Update the changelog