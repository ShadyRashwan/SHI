/**
 * Python Bundling Script for Windows ARM
 * 
 * This script creates a standalone Python distribution that can be bundled
 * with the SHI application for Windows on ARM devices.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Constants
const PYTHON_VERSION = '3.10.11';  // A version with ARM64 support
const PYTHON_DOWNLOAD_URL = `https://www.python.org/ftp/python/${PYTHON_VERSION}/python-${PYTHON_VERSION}-embed-aarch64.zip`;
const DOWNLOAD_DIR = path.join(__dirname, 'python-download');
const EMBEDDED_DIR = path.join(__dirname, 'python-embedded');

// Ensure directories exist
if (!fs.existsSync(DOWNLOAD_DIR)) {
    fs.mkdirSync(DOWNLOAD_DIR, { recursive: true });
}

if (!fs.existsSync(EMBEDDED_DIR)) {
    fs.mkdirSync(EMBEDDED_DIR, { recursive: true });
}

console.log(`Downloading Python ${PYTHON_VERSION} for ARM64...`);
try {
    // Download embedded Python for ARM64
    execSync(`curl -L "${PYTHON_DOWNLOAD_URL}" -o "${path.join(DOWNLOAD_DIR, 'python-embedded.zip')}"`, { stdio: 'inherit' });
    
    // Extract the ZIP file
    console.log('Extracting Python distribution...');
    execSync(`powershell -command "Expand-Archive -Path '${path.join(DOWNLOAD_DIR, 'python-embedded.zip')}' -DestinationPath '${EMBEDDED_DIR}' -Force"`, { stdio: 'inherit' });
    
    // Create pip and install base packages
    console.log('Setting up pip...');
    fs.writeFileSync(path.join(EMBEDDED_DIR, 'get-pip.py'), 'import sys; sys.path.insert(0, ""); import ensurepip; ensurepip._bootstrap(); import pip; pip.main(["install", "--no-cache-dir", "wheel", "setuptools"])');
    
    // Get full path for embedded Python
    const pythonExe = path.join(EMBEDDED_DIR, 'python.exe');
    
    // Run get-pip.py to install pip
    execSync(`"${pythonExe}" "${path.join(EMBEDDED_DIR, 'get-pip.py')}"`, { stdio: 'inherit' });
    
    // Install required packages
    console.log('Installing required packages...');
    execSync(`"${pythonExe}" -m pip install --no-cache-dir streamlit==1.32.0 numpy pillow reportlab tqdm`, { stdio: 'inherit' });
    
    console.log('Bundled Python setup completed successfully.');
    console.log(`Python distribution is ready at: ${EMBEDDED_DIR}`);
    
    // Update package.json to include the embedded Python
    const packageJsonPath = path.join(__dirname, 'package.json');
    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    
    // Add the embedded Python to extraResources
    const hasEmbeddedPython = packageJson.build.extraResources.some(resource => 
        resource.from === 'python-embedded' || resource.to === 'python-embedded'
    );
    
    if (!hasEmbeddedPython) {
        packageJson.build.extraResources.push({
            from: 'python-embedded',
            to: 'python-embedded'
        });
        
        fs.writeFileSync(packageJsonPath, JSON.stringify(packageJson, null, 2));
        console.log('Updated package.json to include bundled Python.');
    }
    
} catch (error) {
    console.error('Failed to set up bundled Python:', error);
    process.exit(1);
}