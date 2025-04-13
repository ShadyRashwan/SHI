#!/usr/bin/env node

/**
 * SHI Desktop App Setup Script
 * 
 * This script sets up the development environment for the SHI Desktop app.
 * It creates a Python virtual environment and installs the required packages.
 */

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Constants
const PYTHON_ENV_DIR = path.join(__dirname, 'python-env');
const REQUIREMENTS_FILE = path.join(__dirname, 'desktop-requirements.txt');
const STREAMLIT_PACKAGE = 'streamlit==1.32.0'; // Fixed version for stability

// Core dependencies required for SHI
const CORE_DEPENDENCIES = [
  'wheel',
  'setuptools',
  'numpy',
  'pillow',
  'reportlab',
  'tqdm'
];

// Determine platform-specific commands
const isWindows = os.platform() === 'win32';
const pythonCommand = isWindows ? 'python' : 'python3';
const pipCommand = 'pip';

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  red: '\x1b[31m'
};

// Helper function to log with colors
function log(message, color = colors.reset) {
  console.log(`${color}${message}${colors.reset}`);
}

// Check if Python is installed
function checkPython() {
  try {
    const version = execSync(`${pythonCommand} --version`).toString().trim();
    log(`Found ${version}`, colors.green);
    return true;
  } catch (error) {
    log('Python not found. Please install Python 3.9 or higher.', colors.red);
    return false;
  }
}

// Create Python virtual environment
function createVirtualEnv() {
  log('Creating Python virtual environment...', colors.blue);

  if (fs.existsSync(PYTHON_ENV_DIR)) {
    log('Virtual environment already exists.', colors.yellow);
    return true;
  }

  try {
    execSync(`${pythonCommand} -m venv ${PYTHON_ENV_DIR}`);
    log('Virtual environment created successfully.', colors.green);
    return true;
  } catch (error) {
    log(`Failed to create virtual environment: ${error.message}`, colors.red);
    return false;
  }
}

// Install Python packages
function installPackages() {
  log('Installing Python packages...', colors.blue);

  // Determine the pip path based on the platform
  const pipPath = isWindows
    ? path.join(PYTHON_ENV_DIR, 'Scripts', 'pip')
    : path.join(PYTHON_ENV_DIR, 'bin', 'pip');

  try {
    // Upgrade pip first
    execSync(`${pipPath} install --upgrade pip`);
    log('Upgraded pip.', colors.green);

    // Install wheel and setuptools first (needed for binary packages)
    log('Installing wheel and setuptools...', colors.blue);
    execSync(`${pipPath} install --upgrade wheel setuptools`);
    log('Wheel and setuptools installed successfully.', colors.green);

    // Install core dependencies first using binary packages
    log('Installing core dependencies...', colors.blue);
    
    // Windows needs special handling to avoid compilation issues
    if (isWindows) {
      // Install packages separately using binary packages whenever possible
      for (const pkg of CORE_DEPENDENCIES) {
        log(`Installing ${pkg} (binary if available)...`, colors.blue);
        try {
          // Try binary-only first
          execSync(`${pipPath} install --only-binary=:all: ${pkg}`, { stdio: 'pipe' });
        } catch (e) {
          // Fall back to allowing source builds
          log(`Binary package not available for ${pkg}, trying with source...`, colors.yellow);
          execSync(`${pipPath} install ${pkg}`, { stdio: 'pipe' });
        }
      }
    } else {
      // On non-Windows platforms, we can install all at once
      execSync(`${pipPath} install ${CORE_DEPENDENCIES.join(' ')}`);
    }
    
    log('Core dependencies installed successfully.', colors.green);

    // Install remaining requirements with no-build-isolation to avoid C compiler issues
    log('Installing remaining requirements from requirements.txt...', colors.blue);
    execSync(`${pipPath} install --no-build-isolation -r ${REQUIREMENTS_FILE}`, { 
      stdio: 'inherit',  // Show output directly for better debugging
      env: {
        ...process.env,
        PIP_NO_BUILD_ISOLATION: '1'
      }
    });
    log('Requirements installed successfully.', colors.green);

    // Install Streamlit
    log(`Installing ${STREAMLIT_PACKAGE}...`, colors.blue);
    execSync(`${pipPath} install ${STREAMLIT_PACKAGE}`);
    log('Streamlit installed successfully.', colors.green);
    
    // Install pillow_heif explicitly for HEIC support
    log('Installing pillow_heif for HEIC support...', colors.blue);
    
    try {
      // Try binary-only first for pillow_heif
      execSync(`${pipPath} install --only-binary=:all: pillow_heif`, { stdio: 'pipe' });
    } catch (e) {
      // Fallback - skip on Windows if not available as binary
      if (isWindows) {
        log('Binary package not available for pillow_heif and may require C compiler.', colors.yellow);
        log('HEIC support may be limited. App will still work for other image formats.', colors.yellow);
      } else {
        execSync(`${pipPath} install pillow_heif`);
        log('pillow_heif installed successfully.', colors.green);
      }
    }

    return true;
  } catch (error) {
    log(`Failed to install packages: ${error.message}`, colors.red);
    
    if (isWindows) {
      log('', colors.reset);
      log('Windows build issue detected. You might need Visual C++ Build Tools.', colors.yellow);
      log('Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/', colors.yellow);
      log('When installing, select "Desktop development with C++" workload.', colors.yellow);
      log('', colors.reset);
      log('Alternatively, you can try building on another Windows system and', colors.yellow);
      log('copying the completed installer to share with others.', colors.yellow);
    }
    
    return false;
  }
}

// Main function
async function main() {
  log('Setting up the SHI Desktop development environment...', colors.blue);

  // Check Python
  if (!checkPython()) {
    process.exit(1);
  }

  // Create virtual environment
  if (!createVirtualEnv()) {
    process.exit(1);
  }

  // Install packages
  if (!installPackages()) {
    process.exit(1);
  }

  log('\nSetup completed successfully! 🎉', colors.green);
  log('\nTo run the application in development mode:', colors.blue);
  log('  npm start', colors.yellow);
  log('\nTo build the application for distribution:', colors.blue);
  log('  npm run build', colors.yellow);
  
  if (isWindows) {
    log('\nOn Windows:', colors.blue);
    log('  npx electron-builder --win', colors.yellow);
  }
}

// Run the main function
main().catch(error => {
  log(`Error: ${error.message}`, colors.red);
  process.exit(1);
});