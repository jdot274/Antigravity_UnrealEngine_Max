const { app, BrowserWindow, screen } = require('electron');
const path = require('path');

function createWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  const mainWindow = new BrowserWindow({
    width: Math.min(1400, width - 100),
    height: Math.min(900, height - 100),
    frame: false,
    transparent: true,
    titleBarStyle: 'hidden',
    vibrancy: 'under-window', // macOS glass effect
    visualEffectState: 'active',
    backgroundColor: '#00000000', // Transparent bg for vibrancy
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  mainWindow.center();
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
