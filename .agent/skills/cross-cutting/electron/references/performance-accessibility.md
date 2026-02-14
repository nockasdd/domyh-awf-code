## ⚡ Performance Optimization

### Lazy Window Loading

```typescript
// main/windows.ts
let settingsWindow: BrowserWindow | null = null;

export function getSettingsWindow(): BrowserWindow {
  if (!settingsWindow || settingsWindow.isDestroyed()) {
    settingsWindow = new BrowserWindow({
      show: false,
      webPreferences: { preload: settingsPreload },
    });
    settingsWindow.loadFile("settings.html");
  }
  return settingsWindow;
}

// Show when ready
ipcMain.handle("open-settings", () => {
  const win = getSettingsWindow();
  win.once("ready-to-show", () => win.show());
});
```

### Worker Threads for Heavy Tasks

```typescript
// main/workers/heavy-task.ts
import { Worker, isMainThread, parentPort } from "worker_threads";

if (!isMainThread && parentPort) {
  parentPort.on("message", (data) => {
    const result = processHeavyTask(data);
    parentPort!.postMessage(result);
  });
}

// main.ts
const worker = new Worker("./workers/heavy-task.js");
worker.postMessage(largeDataset);
worker.on("message", (result) => {
  mainWindow.webContents.send("task:complete", result);
});
```

---

## ♿ Accessibility

```typescript
// main.ts
import { app } from "electron";

// Check if accessibility is enabled
if (app.accessibilitySupportEnabled) {
  console.log("Accessibility support enabled");
}

// Enable programmatically if needed
app.setAccessibilitySupportEnabled(true);

// Inform renderer about accessibility state
ipcMain.handle("get-accessibility-state", () => {
  return app.accessibilitySupportEnabled;
});
```

### Renderer Best Practices

```typescript
// Use semantic HTML and ARIA
<button
  aria-label="Open file"
  aria-keyshortcuts="Ctrl+O"
  onClick={handleOpen}
>
  Open
</button>

// Focus management
useEffect(() => {
  if (isModalOpen) {
    modalRef.current?.focus();
  }
}, [isModalOpen]);
```

---

## 📦 Project Structure

```
my-electron-app/
 src/
   main/              # Main process
   index.ts       # Entry point
   ipc.ts         # IPC handlers
   tray.ts        # System tray
   shortcuts.ts   # Global shortcuts
   updates.ts     # Auto-updater
   database.ts    # SQLite
   preload/           # Preload scripts
   index.ts       # Main preload
   index.d.ts     # Type declarations
   renderer/          # Renderer (React/Vue)
   App.tsx
   main.tsx
   e2e/                   # E2E tests
   app.spec.ts
   electron.vite.config.ts
   electron-builder.json5
 playwright.config.ts
 package.json
```

---
