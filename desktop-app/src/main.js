const { app, BrowserWindow, ipcMain, dialog, shell } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const fs = require('fs');
const findProcess = require('find-process');
const armHelper = require('./arm-helper');

let mainWindow;
let streamlitProcess;
let pythonPath;
let streamlitReady = false;
let appQuitting = false;

// Debug logging for ARM issues
console.log('Application starting...');
console.log('Process architecture:', process.arch);
console.log('Process platform:', process.platform);

// Get the app path
const appPath = app.isPackaged
  ? path.join(process.resourcesPath)
  : path.join(__dirname, '../../');

// Determine Python executable path
function getPythonPath() {
  if (app.isPackaged) {
    // Use bundled Python in production
    const pythonRelativePath = process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python';
    const defaultPythonPath = path.join(process.resourcesPath, 'python-env', pythonRelativePath);
    
    // Log the Python path to help diagnose ARM issues
    console.log('Default Python path:', defaultPythonPath);
    
    // Special handling for ARM architecture
    if (armHelper.isArmArchitecture()) {
      console.log('ARM64 architecture detected, checking Python availability...');
      
      if (armHelper.isPythonAvailable(defaultPythonPath)) {
        console.log('Bundled Python is available for ARM64, using it');
        return defaultPythonPath;
      } else {
        console.log('Bundled Python not available for ARM64, looking for system Python...');
        const armPythonPath = armHelper.getArmPythonPath(defaultPythonPath);
        console.log('Using Python for ARM64:', armPythonPath);
        return armPythonPath;
      }
    }
    
    // For non-ARM architectures, check if the Python executable exists
    if (fs.existsSync(defaultPythonPath)) {
      console.log('Python executable exists at path');
      return defaultPythonPath;
    } else {
      console.error('ERROR: Python executable does not exist at expected path');
      // Try to fall back to system Python as a last resort
      console.log('Falling back to system Python');
      return process.platform === 'win32' ? 'python' : 'python3';
    }
  } else {
    // Use system Python in development
    const devPython = process.platform === 'win32' ? 'python' : 'python3';
    console.log('Using development Python:', devPython);
    return devPython;
  }
}

// Create the main window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
    show: false,
    title: 'SHI - Images to PDF Converter',
    icon: path.join(__dirname, 'assets', process.platform === 'win32' ? 'icon.ico' : 'icon.png'),
  });

  // Show loading screen
  mainWindow.loadFile(path.join(__dirname, 'loading.html'));
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Start Streamlit server
  startStreamlit();

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// Start Streamlit
function startStreamlit() {
  try {
    // Get Python path
    pythonPath = getPythonPath();
    
    // Determine Streamlit script path
    const streamlitScriptPath = path.join(appPath, 'app', 'gui.py');
    
    // Verify files exist
    console.log('Checking if script path exists:', streamlitScriptPath);
    if (!fs.existsSync(streamlitScriptPath)) {
      console.error('ERROR: Streamlit script does not exist at path:', streamlitScriptPath);
      // Show error dialog to user
      if (mainWindow) {
        dialog.showErrorBox(
          'Missing Files',
          `Cannot find required files. The app may not have been installed correctly.
          
Missing file: gui.py
          
Please try reinstalling the application or contact support.`
        );
      }
      return;
    }
    
    // Create app directory if not exists
    const appDir = path.join(appPath, 'app');
    if (!fs.existsSync(appDir)) {
      console.log('Creating app directory:', appDir);
      fs.mkdirSync(appDir, { recursive: true });
    }
    
    console.log('Starting Streamlit with Python:', pythonPath);
    console.log('Streamlit script path:', streamlitScriptPath);
  
    // Initialize timeout to detect if Streamlit starts successfully
    let startupTimeout = setTimeout(() => {
      if (!streamlitReady && mainWindow) {
        console.error('Streamlit failed to start within timeout period');
        
        // Check if we're on ARM architecture
        if (armHelper.isArmArchitecture()) {
          console.log('ARM architecture detected, showing patience message instead of error');
          
          // Just show a patience message for ARM users, don't require installation
          if (mainWindow) {
            mainWindow.webContents.executeJavaScript(`
              document.body.innerHTML = '<div style="padding: 20px; font-family: sans-serif; background-color: #1e1e1e; color: #e1e1e1;">
                <h2 style="color: #4a9cf6;">Please be patient...</h2>
                <p>The application is still trying to start.</p>
                <p>Windows on ARM devices might take longer on first launch.</p>
                <div style="margin-top: 20px; background-color: #2d2d2d; padding: 10px; border-radius: 5px;">
                  <p style="margin: 0; font-style: italic;">This is normal and might take up to 2 minutes.</p>
                </div>
              </div>';
            `);
          }
          
          // Extend the timeout for ARM devices
          startupTimeout = setTimeout(() => {
            if (!streamlitReady && mainWindow) {
              console.error('Streamlit still failed to start after extended timeout');
              dialog.showErrorBox(
                'Application Error',
                `Unable to start the application. 

This device may not be compatible with SHI.
Please contact support for assistance.`
              );
            }
          }, 120000); // Additional 2 minute timeout
          
          return;
        }
        
        // For non-ARM devices, show a regular error
        dialog.showErrorBox(
          'Startup Error',
          `The application failed to start within the expected time.
          
This might be due to:
- Firewall or antivirus blocking the application
- Another application using the same port
- Temporary system resource constraints

Please try restarting your computer and running the application again.`
        );
      }
    }, 60000); // 60 second timeout (extended from original 30 seconds)
  
    // Find a free port
    findFreePort(8501, (port) => {
      try {
        // Special handling for ARM architecture
        let streamlitArgs = [
          '-m', 'streamlit', 'run', 
          streamlitScriptPath,
          '--server.port', port.toString(),
          '--server.headless', 'true',
          '--browser.serverAddress', 'localhost',
          '--server.enableCORS', 'false',
          '--browser.gatherUsageStats', 'false'
        ];
        
        // Add extra debugging for ARM
        if (armHelper.isArmArchitecture()) {
          console.log('Using ARM-specific launch settings');
          
          // Show installation message
          if (mainWindow) {
            mainWindow.webContents.executeJavaScript(`
              document.body.innerHTML = '<div style="padding: 20px; font-family: sans-serif; background-color: #1e1e1e; color: #e1e1e1;">
                <h2 style="color: #4a9cf6;">Installing required components...</h2>
                <p>Please wait while we install required components for Windows on ARM.</p>
                <p>This may take a few minutes.</p>
                <div style="margin-top: 20px; background-color: #2d2d2d; padding: 10px; border-radius: 5px;">
                  <p style="margin: 0; font-style: italic;">Note: Windows on ARM devices require special setup on first run.</p>
                  <p style="margin: 5px 0 0 0; font-style: italic;">After this setup completes, future launches will be much faster.</p>
                </div>
              </div>';
            `);
          }
          
          // Try to install all required packages
          try {
            // First check if streamlit is already available
            const testCmd = process.platform === 'win32' ? 
              `"${pythonPath}" -c "import streamlit; print('Streamlit found')"` :
              `${pythonPath} -c "import streamlit; print('Streamlit found')"`;
            
            try {
              console.log('Testing for streamlit module...');
              require('child_process').execSync(testCmd);
              console.log('Streamlit module found');
            } catch (e) {
              console.log('Streamlit module not found, installing all required packages...');
              
              // Install all required packages for ARM
              const installResult = armHelper.installArmRequirements(pythonPath);
              
              if (installResult) {
                console.log('ARM requirements installation successful');
              } else {
                console.warn('ARM requirements installation failed but attempting to continue');
                
                // Update loading screen with a notice but don't require user action
                if (mainWindow) {
                  mainWindow.webContents.executeJavaScript(`
                    document.body.innerHTML = '<div style="padding: 20px; font-family: sans-serif; background-color: #1e1e1e; color: #e1e1e1;">
                      <h2 style="color: #f7a046;">Starting application...</h2>
                      <p>SHI is preparing to start. This might take a bit longer on first run.</p>
                      <div style="margin-top: 20px; background-color: #2d2d2d; padding: 10px; border-radius: 5px;">
                        <p style="margin: 0; font-style: italic;">Note: Windows on ARM devices might experience slower performance.</p>
                      </div>
                    </div>';
                  `);
                }
                
                // Continue anyway - it's possible the bundled Python environment will work
              }
            }
          } catch (armSetupErr) {
            console.error('ARM setup error:', armSetupErr);
          }
        }
  
        // Launch Streamlit
        console.log('Spawning Streamlit process with args:', streamlitArgs);
        streamlitProcess = spawn(pythonPath, streamlitArgs, {
          cwd: path.join(appPath),
          env: {
            ...process.env,
            PYTHONUNBUFFERED: '1',
          }
        });
  
        // Handle Streamlit output
        streamlitProcess.stdout.on('data', (data) => {
          console.log('Streamlit:', data.toString());
          
          // Check if Streamlit is ready
          if (data.toString().includes('You can now view your Streamlit app') && !streamlitReady) {
            streamlitReady = true;
            
            // Clear the startup timeout since Streamlit started successfully
            if (startupTimeout) {
              clearTimeout(startupTimeout);
              startupTimeout = null;
            }
            
            // Load Streamlit in the window
            setTimeout(() => {
              if (mainWindow) {
                mainWindow.loadURL(`http://localhost:${port}`);
                
                // Open DevTools in development mode
                if (!app.isPackaged) {
                  mainWindow.webContents.openDevTools();
                }
              }
            }, 1000);
          }
        });
  
        streamlitProcess.stderr.on('data', (data) => {
          console.error('Streamlit Error:', data.toString());
        });
  
        streamlitProcess.on('close', (code) => {
          console.log(`Streamlit process exited with code ${code}`);
          
          // Clear the startup timeout if it still exists
          if (startupTimeout) {
            clearTimeout(startupTimeout);
            startupTimeout = null;
          }
          
          if (!appQuitting && mainWindow) {
            dialog.showErrorBox(
              'Streamlit Error',
              `The Streamlit process has unexpectedly terminated (code: ${code}). 
              
This might be due to:
- Missing Python dependencies
- Incompatible Python version
- Permission issues

Please restart the application or contact support if the issue persists.`
            );
          }
        });
      } catch (spawnError) {
        console.error('Error launching Streamlit process:', spawnError);
        if (mainWindow) {
          dialog.showErrorBox(
            'Launch Error',
            `Failed to launch the Streamlit process: ${spawnError.message}
            
Please check if Python is installed correctly on your system.`
          );
        }
      }
    });
  } catch (error) {
    console.error('Error in startStreamlit function:', error);
    if (mainWindow) {
      dialog.showErrorBox(
        'Application Error',
        `An error occurred while starting the application: ${error.message}`
      );
    }
  }
}

// Find a free port starting from the given port
function findFreePort(startPort, callback) {
  let port = startPort;
  
  const checkPort = () => {
    findProcess('port', port)
      .then(list => {
        if (list.length === 0) {
          callback(port);
        } else {
          port++;
          checkPort();
        }
      })
      .catch(err => {
        console.error('Error finding free port:', err);
        callback(startPort); // Fallback to the start port
      });
  };
  
  checkPort();
}

// Create window when Electron is ready
app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

// Quit the app when all windows are closed (except on macOS)
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Clean up Streamlit process before quitting
app.on('before-quit', () => {
  appQuitting = true;
  if (streamlitProcess) {
    // Kill Streamlit process and all child processes
    if (process.platform === 'win32') {
      spawn('taskkill', ['/pid', streamlitProcess.pid, '/f', '/t']);
    } else {
      process.kill(-streamlitProcess.pid);
    }
  }
});

// Handle Electron activation (macOS)
app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});