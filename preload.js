// preload.js
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('electronAPI', {
    // Metodi specifici per controlli finestra (SICURI)
    minimizeWindow: () => ipcRenderer.invoke('minimize-window'),
    toggleFullscreen: () => ipcRenderer.invoke('toggle-fullscreen')
});
