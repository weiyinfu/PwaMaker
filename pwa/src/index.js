const {app, BrowserWindow, shell} = require('electron');
const path = require('path');
const config = require("./config.json");
const createWindow = () => {
    // Create the browser window.
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 800,
        fullscreen: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
        },
        frame: true,
    });

    mainWindow.loadURL(config.index)
    // mainWindow.loadURL("https://bytedance.feishu.cn/drive/home/");

    // Open the DevTools.
    // mainWindow.webContents.openDevTools();
    // mainWindow.webContents.on('new-window', function(e, url) {
    //     e.preventDefault();
    //     shell.openExternal(url);
    // });
    mainWindow.webContents.setWindowOpenHandler(({url}) => {
        // config.fileProtocol is my custom file protocol
        // if (url.startsWith(config.fileProtocol)) {
        //     return {action: 'allow'};
        // }
        // open url in a browser and prevent default
        shell.openExternal(url);
        return {action: 'deny'};
    });
};

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
    // if (process.platform !== 'darwin') {
    //     app.quit();
    // }
    app.quit();
});
app.on("before-quit", () => {
})
app.on('activate', () => {
    // On OS X it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});
