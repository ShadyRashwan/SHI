/**
 * ARM Helper Module for SHI Desktop App
 * 
 * This module provides ARM-specific workarounds and utilities
 * for the SHI desktop application.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { app } = require('electron');

/**
 * Checks if running on ARM architecture
 */
function isArmArchitecture() {
  return process.arch === 'arm64';
}

/**
 * Checks if Python is available on the system
 * @param {string} pythonPath - Path to check
 * @returns {boolean} - Whether Python is available
 */
function isPythonAvailable(pythonPath) {
  try {
    if (fs.existsSync(pythonPath)) {
      return true;
    }
    
    // Try to run system Python
    try {
      execSync('python --version', { stdio: 'ignore' });
      return true;
    } catch (e) {
      // Python not available in PATH
      return false;
    }
  } catch (error) {
    console.error('Error checking Python availability:', error);
    return false;
  }
}

/**
 * Find Python in common system locations
 * @returns {string|null} - Path to Python if found, null otherwise
 */
function findSystemPython() {
  // First check for bundled Python distribution
  if (app.isPackaged) {
    const bundledPythonPath = path.join(process.resourcesPath, 'python-embedded', 'python.exe');
    console.log('Checking for bundled Python at:', bundledPythonPath);
    if (fs.existsSync(bundledPythonPath)) {
      console.log('Found bundled Python distribution!');
      return bundledPythonPath;
    }
  }
  
  // Standard system locations
  const commonLocations = [
    'C:\\Program Files\\Python310\\python.exe',
    'C:\\Program Files\\Python311\\python.exe',
    'C:\\Program Files\\Python312\\python.exe',
    'C:\\Program Files\\Python39\\python.exe',
    'C:\\Python310\\python.exe',
    'C:\\Python311\\python.exe',
    'C:\\Python312\\python.exe',
    'C:\\Python39\\python.exe'
  ];
  
  for (const location of commonLocations) {
    if (fs.existsSync(location)) {
      return location;
    }
  }
  
  return null;
}

/**
 * Get Python path for ARM architecture
 * @param {string} defaultPath - Default Python path
 * @returns {string} - Best Python path for ARM
 */
function getArmPythonPath(defaultPath) {
  // Check if default path exists
  if (fs.existsSync(defaultPath)) {
    return defaultPath;
  }
  
  // Try to find system Python
  const systemPython = findSystemPython();
  if (systemPython) {
    return systemPython;
  }
  
  // Fall back to plain 'python' command and hope it's in PATH
  return 'python';
}

/**
 * Install required packages for ARM Windows
 * @param {string} pythonPath - Path to Python executable
 * @returns {boolean} - Whether installation was successful
 */
function installArmRequirements(pythonPath) {
  try {
    console.log('Installing required packages for ARM Windows...');
    
    // Get path to desktop-requirements.txt
    const appPath = app.isPackaged
      ? path.join(process.resourcesPath)
      : path.join(__dirname, '../..');
      
    const requirementsPath = path.join(appPath, 'desktop-requirements.txt');
    
    if (fs.existsSync(requirementsPath)) {
      console.log('Found desktop-requirements.txt at:', requirementsPath);
    } else {
      console.error('Could not find desktop-requirements.txt at:', requirementsPath);
      
      // Create minimal requirements file if it doesn't exist
      const minimalRequirements = 
`# Core dependencies for SHI ARM app
streamlit==1.32.0
numpy>=1.24.0
Pillow>=10.0.0
reportlab>=4.0.0
tqdm>=4.0.0
altair>=4.0.0
packaging>=23.0
click>=8.0.0
protobuf>=4.0.0
`;
      
      const tempRequirementsPath = path.join(
        app.isPackaged 
          ? path.join(process.resourcesPath)
          : __dirname, 
        'arm-requirements.txt'
      );
      
      fs.writeFileSync(tempRequirementsPath, minimalRequirements);
      console.log('Created minimal requirements file at:', tempRequirementsPath);
      
      // Install from minimal requirements
      console.log('Installing from minimal requirements file...');
      execSync(`"${pythonPath}" -m pip install --prefer-binary -r "${tempRequirementsPath}"`, { 
        stdio: 'inherit' 
      });
      return true;
    }
    
    // Install directly from requirements file with prefer-binary
    console.log('Installing from desktop-requirements.txt...');
    execSync(`"${pythonPath}" -m pip install --prefer-binary -r "${requirementsPath}"`, { 
      stdio: 'inherit' 
    });
    
    // Make sure streamlit is installed
    console.log('Ensuring streamlit is installed...');
    execSync(`"${pythonPath}" -m pip install --prefer-binary streamlit==1.32.0`, { 
      stdio: 'inherit' 
    });
    
    console.log('Package installation completed successfully');
    return true;
  } catch (error) {
    console.error('Failed to install ARM requirements:', error);
    return false;
  }
}

module.exports = {
  isArmArchitecture,
  isPythonAvailable,
  findSystemPython,
  getArmPythonPath,
  installArmRequirements
};