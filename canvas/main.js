const { app, BrowserWindow } = require('electron');
const path = require('path');

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    titleBarStyle: 'hiddenInset',
    vibrancy: 'under-window', // macOS glass effect
    visualEffectState: 'active',
    backgroundColor: '#00000000', // Transparent bg for vibrancy
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false, // For prototype speed, allowing direct require in HTML if needed (optional)
    },
  });

  mainWindow.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
