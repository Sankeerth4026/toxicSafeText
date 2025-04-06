import pkg from "electron";
const { app, BrowserWindow, globalShortcut, screen } = pkg;

import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let mainWindow;
let ignoreMouseEvents = true;

function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().bounds;

    mainWindow = new BrowserWindow({
        width,
        height,
        x: 0,
        y: 0,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        skipTaskbar: true,
        hasShadow: false,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    mainWindow.setIgnoreMouseEvents(ignoreMouseEvents);
    mainWindow.loadURL("http://localhost:3000");

    // ✅ DEV: Uncomment for debug visuals
    // mainWindow.webContents.openDevTools();
    // mainWindow.setOpacity(0.9); // Optional: make it slightly visible for testing

    mainWindow.setMenuBarVisibility(false);

    globalShortcut.register("Alt+Shift+T", () => {
        ignoreMouseEvents = !ignoreMouseEvents;
        mainWindow.setIgnoreMouseEvents(ignoreMouseEvents);
        mainWindow.webContents.send("toggle-interaction", ignoreMouseEvents);
    });

    globalShortcut.register("Alt+Shift+Q", () => {
        app.quit();
    });

    console.log("[✓] Electron overlay window launched");
}

app.whenReady().then(() => {
    createWindow();
    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});

app.on("will-quit", () => {
    globalShortcut.unregisterAll();
});
