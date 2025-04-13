# SHI Desktop Application

This is an Electron-based desktop application wrapper for the SHI (Images to PDF Converter) tool, designed to make distribution to non-technical users easy and intuitive.

## Features

- Cross-platform desktop application (Windows, macOS, Linux)
- Embedded Python environment with all dependencies
- Native file system access for image processing
- No need for Docker or command-line knowledge
- Simple installer for non-technical users

## Building and Distributing to Non-Technical Users

### Important: Build on the Target Platform

For the most reliable results, **build the application on the same platform you intend to distribute it for**:
- Build Windows installers on a Windows machine
- Build macOS installers on a Mac
- Build Linux packages on a Linux machine

Cross-platform building (like building Windows installers from Mac) is technically possible but often leads to subtle issues with native dependencies or filesystem permissions.

### Building for Windows (Recommended for most users)

1. **Set up a Windows development environment**:
   - Install [Node.js](https://nodejs.org/) (v14 or later)
   - Install [Python](https://www.python.org/downloads/) (3.9 or later)
   - Install [Git](https://git-scm.com/download/win)

2. **Clone and prepare the project**:
   ```
   git clone <repository-url>
   cd SHI\desktop-app
   npm install
   ```

3. **Build the Windows installer**:
   ```
   npm run build:win
   ```

4. **Distribute to users**:
   - The installer will be created in `dist\SHI-Images-to-PDF-Setup-1.0.0.exe`
   - Share this .exe file with your friends via email, cloud storage, or USB drive
   - They simply double-click to install (no technical knowledge required)
   - The app appears in their Start menu like any other Windows program

### Building for macOS

1. **On a Mac**:
   ```
   git clone <repository-url>
   cd SHI/desktop-app
   npm install
   npm run build:mac
   ```

2. **Distribute to users**:
   - The DMG installer will be in `dist/SHI-Images-to-PDF-1.0.0.dmg`
   - Share this file with Mac users
   - They open the DMG and drag the app to their Applications folder

### Building for Linux

1. **On a Linux machine**:
   ```
   git clone <repository-url>
   cd SHI/desktop-app
   npm install
   npm run build:linux
   ```

2. **Distribute to users**:
   - The AppImage will be in `dist/SHI-Images-to-PDF-1.0.0.AppImage`
   - Share this file with Linux users
   - They make it executable and run it directly

## For Non-Technical Users

When distributing to non-technical friends, simply provide them with:

1. The appropriate installer for their operating system
2. Basic instructions:
   - **Windows**: Double-click the .exe file to install, then find "SHI" in the Start menu
   - **Mac**: Open the .dmg file, drag the app to Applications, then open from Applications
   - **Linux**: Right-click the .AppImage, make it executable, then double-click to run

They don't need to:
- Install Python
- Use the command line
- Understand Docker 
- Deal with dependencies

## Development Setup

### Prerequisites

- Node.js (v14 or later)
- npm (v6 or later)
- Python 3.9+ (for development)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd SHI
   ```

2. Install Node.js dependencies:
   ```bash
   cd desktop-app
   npm install
   ```

3. Create a Python virtual environment (only required for development):
   ```bash
   # From the desktop-app directory
   cd ..
   python -m venv desktop-app/python-env
   ```

4. Activate the virtual environment and install Python dependencies:
   ```bash
   # Windows
   desktop-app\python-env\Scripts\activate
   
   # macOS/Linux
   source desktop-app/python-env/bin/activate
   
   pip install -r requirements.txt
   pip install streamlit
   ```

### Running in Development Mode

```bash
# From the desktop-app directory
npm start
```

This will launch the Electron app in development mode with the Streamlit server.

## Application Structure

- `src/main.js`: Main Electron process
- `src/loading.html`: Loading screen HTML
- `src/assets/`: Application icons and assets
- `../app/`: SHI Python application code (your original code)
- `python-env/`: Python virtual environment (bundled in the final app)

## How It Works

1. The Electron app launches and displays a loading screen
2. It starts a Python subprocess running the Streamlit server with your original app
3. Once the Streamlit server is ready, the app loads the Streamlit UI in the Electron window
4. When the app is closed, it properly shuts down the Streamlit server

## Customization

- To change the app icon, replace the files in `src/assets/`
- To modify the loading screen, edit `src/loading.html`
- To customize the window size, edit the `width` and `height` values in `src/main.js`

## Troubleshooting

- **Error: Python Not Found**: Make sure the Python path is correctly set in `getPythonPath()` function
- **Error: Streamlit Not Starting**: Check if the Streamlit package is installed in the Python environment
- **Error: App Not Building**: Make sure you have all required build dependencies for Electron Builder
- **Error: Command Not Found**: Try using `npx electron-builder` instead of `npm run build`