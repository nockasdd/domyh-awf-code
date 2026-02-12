---
name: electron
detect:
  [
    "electron.vite.config.ts",
    "main.ts:electron",
    "preload.ts",
    "forge.config.ts",
  ]
version: "1.0.0"
category: desktop
tier: 1
---

# Electron Patterns — DOMYH Awesome Code

> **Version**: Electron 35-40 (2025-2026)
> **Chromium**: 134.0.6998+
> **Node.js**: 22.14.0
> **Philosophy**: Context isolation, secure IPC, minimal privileges, performant builds

---

## 🎯 When to Use This Skill

Use for: Cross-platform desktop apps, web tech on desktop.
**NOT for**: Mobile (→ react-native), CLI tools (→ nodejs), Lightweight apps (→ tauri).

---

## 📦 What's New (2025-2026)

| Version | Feature                            | Description                   |
| ------- | ---------------------------------- | ----------------------------- |
| **35**  | ServiceWorker Preload              | MV3 extension support         |
| **35**  | `contextBridge.executeInMainWorld` | Safe cross-world execution    |
| **35**  | `roundedCorners` (Windows)         | UI customization              |
| **36**  | ESM-first                          | Native ES modules default     |
| **37**  | Chrome Extensions API              | Better extension support      |
| **38**  | WebGPU stable                      | Hardware-accelerated graphics |
| **39**  | Utility Process V8                 | Worker process improvements   |
| **40**  | Fuse improvements                  | Compile-time security flags   |

---

## 🔨 Build Tools Comparison

| Tool                 | Purpose             | Best For                              |
| -------------------- | ------------------- | ------------------------------------- |
| **electron-vite**    | Dev + Build         | Fast HMR, Vite ecosystem              |
| **electron-forge**   | Scaffolding + Build | Official, templates, plugins          |
| **electron-builder** | Packaging + Publish | Distribution, installers, auto-update |

### Recommended Combo

```bash
# Development: electron-vite (fast HMR)
npm create @electron-vite/quick-start@latest my-app

# Packaging: electron-builder (mature, flexible)
npm install -D electron-builder

# Or full-featured: electron-forge
npm init electron-app@latest my-app -- --template=vite-typescript
```

### electron-vite Config

```typescript
// electron.vite.config.ts
import { defineConfig, externalizeDepsPlugin } from "electron-vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  main: {
    plugins: [externalizeDepsPlugin()],
    build: { rollupOptions: { external: ["better-sqlite3"] } },
  },
  preload: {
    plugins: [externalizeDepsPlugin()],
  },
  renderer: {
    plugins: [react()],
  },
});
```

### electron-builder Config

```json5
// electron-builder.json5
{
  appId: "com.yourcompany.app",
  productName: "MyApp",
  directories: { output: "dist" },
  files: ["out/**/*"],
  mac: {
    target: ["dmg", "zip"],
    notarize: { teamId: "YOUR_TEAM_ID" },
    hardenedRuntime: true,
  },
  win: {
    target: ["nsis"],
    signingHashAlgorithms: ["sha256"],
    sign: "./scripts/sign.js",
  },
  linux: {
    target: ["deb", "AppImage"],
  },
  publish: [
    {
      provider: "github",
      owner: "yourname",
      repo: "yourapp",
    },
  ],
}
```

---

## 🔒 Security Best Practices

### Context Isolation (Required)

```typescript
// main.ts
import { BrowserWindow, app } from "electron";
import path from "path";

const mainWindow = new BrowserWindow({
  width: 1200,
  height: 800,
  roundedCorners: true, // Windows 11
  webPreferences: {
    // ✅ Always enable
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true,
    preload: path.join(__dirname, "preload.js"),
    devTools: !app.isPackaged,
    // ✅ Only allow specific web features
    spellcheck: false,
    enableWebSQL: false,
  },
});
```

### Secure Preload Script

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from "electron";

// ✅ Type-safe API exposure
const electronAPI = {
  // File operations
  openFile: () => ipcRenderer.invoke("dialog:openFile"),
  saveFile: (data: string) => ipcRenderer.invoke("file:save", data),

  // Event listeners (properly cleanup-able)
  onUpdateProgress: (callback: (progress: number) => void) => {
    const handler = (_: unknown, progress: number) => callback(progress);
    ipcRenderer.on("update:progress", handler);
    return () => ipcRenderer.removeListener("update:progress", handler);
  },

  // ❌ Never expose raw ipcRenderer
} as const;

contextBridge.exposeInMainWorld("electronAPI", electronAPI);

// TypeScript types for renderer
export type ElectronAPI = typeof electronAPI;
```

### TypeScript Integration

```typescript
// preload.d.ts - Add to renderer's src/
import type { ElectronAPI } from "../preload/index";

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
export {};
```

---

## 📡 IPC Communication

### Main Process Handlers

```typescript
// main.ts
import { ipcMain, dialog, BrowserWindow } from "electron";
import { z } from "zod";

// ✅ Schema validation
const SaveFileSchema = z.object({
  path: z.string(),
  content: z.string(),
});

ipcMain.handle("dialog:openFile", async (event) => {
  const window = BrowserWindow.fromWebContents(event.sender);
  if (!window) return null;

  const result = await dialog.showOpenDialog(window, {
    properties: ["openFile"],
    filters: [{ name: "Text", extensions: ["txt", "md"] }],
  });

  if (result.canceled) return null;
  return result.filePaths[0];
});

ipcMain.handle("file:save", async (event, data: unknown) => {
  const parsed = SaveFileSchema.safeParse(data);
  if (!parsed.success) {
    throw new Error("Invalid data format");
  }
  // Save logic with validated data
  return true;
});
```

---

## 🧪 Testing Patterns

### Unit Testing with Vitest

```typescript
// src/main/__tests__/validators.test.ts
import { describe, it, expect } from "vitest";
import { validateFilePath, sanitizeInput } from "../validators";

describe("Input Validation", () => {
  it("rejects path traversal", () => {
    expect(validateFilePath("../etc/passwd")).toBe(false);
    expect(validateFilePath("..\\windows\\system32")).toBe(false);
  });

  it("accepts valid paths", () => {
    expect(validateFilePath("/home/user/documents/file.txt")).toBe(true);
  });

  it("sanitizes HTML input", () => {
    expect(sanitizeInput("<script>alert(1)</script>")).toBe("");
  });
});
```

### E2E Testing with Playwright

```typescript
// e2e/app.spec.ts
import { test, expect, _electron as electron } from "@playwright/test";

test("app launches and shows main window", async () => {
  const app = await electron.launch({ args: ["./dist/main.js"] });
  const window = await app.firstWindow();

  await expect(window).toHaveTitle(/MyApp/);

  // Test IPC communication
  const result = await window.evaluate(() => {
    return window.electronAPI.getVersion();
  });
  expect(result).toMatch(/\d+\.\d+\.\d+/);

  await app.close();
});

test("file dialog works", async () => {
  const app = await electron.launch({ args: ["./dist/main.js"] });
  const window = await app.firstWindow();

  await window.click('button[data-testid="open-file"]');
  // Dialog opens - mock or handle appropriately

  await app.close();
});
```

### Playwright Config

```typescript
// playwright.config.ts
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30000,
  use: {
    trace: "on-first-retry",
  },
  projects: [{ name: "electron" }],
});
```

---

## 🔄 Auto Updates

### electron-updater Setup

```typescript
// main.ts
import { autoUpdater } from "electron-updater";
import { app, dialog, BrowserWindow } from "electron";
import log from "electron-log";

// Configure logging
autoUpdater.logger = log;
autoUpdater.autoDownload = false;

export function initAutoUpdater(mainWindow: BrowserWindow) {
  // Check for updates on launch
  autoUpdater.checkForUpdatesAndNotify();

  autoUpdater.on("checking-for-update", () => {
    log.info("Checking for update...");
  });

  autoUpdater.on("update-available", (info) => {
    dialog
      .showMessageBox(mainWindow, {
        type: "info",
        title: "Update Available",
        message: `Version ${info.version} is available. Download now?`,
        buttons: ["Download", "Later"],
      })
      .then(({ response }) => {
        if (response === 0) autoUpdater.downloadUpdate();
      });
  });

  autoUpdater.on("download-progress", (progress) => {
    mainWindow.webContents.send("update:progress", progress.percent);
  });

  autoUpdater.on("update-downloaded", (info) => {
    dialog
      .showMessageBox(mainWindow, {
        type: "info",
        title: "Update Ready",
        message: `Version ${info.version} is ready. Restart to apply?`,
        buttons: ["Restart", "Later"],
      })
      .then(({ response }) => {
        if (response === 0) autoUpdater.quitAndInstall();
      });
  });

  autoUpdater.on("error", (err) => {
    log.error("Auto-update error:", err);
  });
}
```

### Code Signing (macOS)

```bash
# macOS notarization
npx electron-builder --mac --publish always

# Required environment variables
export APPLE_ID="your@email.com"
export APPLE_APP_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
export APPLE_TEAM_ID="XXXXXXXXXX"
```

---

## 💾 Data Persistence

### better-sqlite3 (Best for Desktop)

```typescript
// main/database.ts
import Database from "better-sqlite3";
import path from "path";
import { app } from "electron";

const dbPath = path.join(app.getPath("userData"), "app.db");
const db = new Database(dbPath);

// Enable WAL mode for better concurrent performance
db.pragma("journal_mode = WAL");

// Initialize schema
db.exec(`
  CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
  )
`);

// Type-safe operations
export const settings = {
  get: db.prepare("SELECT value FROM settings WHERE key = ?"),
  set: db.prepare("INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)"),
};
```

### electron-store (Simple Key-Value)

```typescript
// main/store.ts
import Store from "electron-store";

interface AppSettings {
  theme: "light" | "dark" | "system";
  windowBounds?: { width: number; height: number; x: number; y: number };
  recentFiles: string[];
}

const store = new Store<AppSettings>({
  defaults: {
    theme: "system",
    recentFiles: [],
  },
  encryptionKey: process.env.STORE_ENCRYPTION_KEY, // Optional
});

export function getSetting<K extends keyof AppSettings>(
  key: K,
): AppSettings[K] {
  return store.get(key);
}

export function setSetting<K extends keyof AppSettings>(
  key: K,
  value: AppSettings[K],
) {
  store.set(key, value);
}
```

### safeStorage (Sensitive Data)

```typescript
// main/secrets.ts
import { safeStorage } from "electron";
import fs from "fs";
import path from "path";
import { app } from "electron";

const secretsPath = path.join(app.getPath("userData"), "secrets.enc");

export function storeSecret(key: string, value: string) {
  if (!safeStorage.isEncryptionAvailable()) {
    throw new Error("Encryption not available");
  }

  const encrypted = safeStorage.encryptString(`${key}:${value}`);
  // Append to secrets file or use a database
  fs.appendFileSync(secretsPath, encrypted);
}

export function getSecret(key: string): string | null {
  // Implementation to retrieve and decrypt
  // ...
}
```

---

## 📟 Native Integrations

### System Tray

```typescript
// main/tray.ts
import { Tray, Menu, nativeImage, app, BrowserWindow } from "electron";
import path from "path";

let tray: Tray | null = null;

export function createTray(mainWindow: BrowserWindow) {
  const icon = nativeImage.createFromPath(
    path.join(__dirname, "assets/tray-icon.png"),
  );

  tray = new Tray(icon);
  tray.setToolTip("MyApp");

  const contextMenu = Menu.buildFromTemplate([
    { label: "Show", click: () => mainWindow.show() },
    { type: "separator" },
    { label: "Quit", click: () => app.quit() },
  ]);

  tray.setContextMenu(contextMenu);

  // Click to show window
  tray.on("click", () => {
    mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
  });
}
```

### Global Shortcuts

```typescript
// main/shortcuts.ts
import { globalShortcut, app, BrowserWindow } from "electron";

export function registerGlobalShortcuts(mainWindow: BrowserWindow) {
  // Register when app is ready
  app.whenReady().then(() => {
    globalShortcut.register("CommandOrControl+Shift+X", () => {
      if (mainWindow.isVisible()) {
        mainWindow.hide();
      } else {
        mainWindow.show();
        mainWindow.focus();
      }
    });
  });

  // Unregister on quit
  app.on("will-quit", () => {
    globalShortcut.unregisterAll();
  });
}
```

### Power Monitor

```typescript
// main/power.ts
import { powerMonitor } from "electron";

export function initPowerMonitor() {
  powerMonitor.on("suspend", () => {
    console.log("System suspended - saving state");
    // Save draft, pause sync, etc.
  });

  powerMonitor.on("resume", () => {
    console.log("System resumed - checking for updates");
    // Resume sync, check for updates
  });

  powerMonitor.on("on-battery", () => {
    console.log("On battery - reducing background tasks");
  });

  powerMonitor.on("on-ac", () => {
    console.log("On AC power - resuming normal operations");
  });
}
```

### Notifications

```typescript
// main/notifications.ts
import { Notification } from "electron";

export function showNotification(title: string, body: string) {
  if (!Notification.isSupported()) return;

  new Notification({
    title,
    body,
    icon: path.join(__dirname, "assets/icon.png"),
  }).show();
}

// With actions (macOS)
export function showActionNotification(title: string, body: string) {
  const notification = new Notification({
    title,
    body,
    actions: [
      { text: "View", type: "button" },
      { text: "Dismiss", type: "button" },
    ],
  });

  notification.on("action", (_, index) => {
    if (index === 0) {
      // Handle View action
    }
  });

  notification.show();
}
```

---

## 🔗 Deep Linking

```typescript
// main.ts
import { app, BrowserWindow } from "electron";

const PROTOCOL = "my-app";

// Register protocol
if (process.defaultApp) {
  app.setAsDefaultProtocolClient(PROTOCOL, process.execPath, [__dirname]);
} else {
  app.setAsDefaultProtocolClient(PROTOCOL);
}

// Single instance lock
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on("second-instance", (event, argv) => {
    // Windows/Linux: URL in argv
    const url = argv.find((arg) => arg.startsWith(`${PROTOCOL}://`));
    if (url) handleDeepLink(url);

    // Focus window
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });

  // macOS: URL via open-url event
  app.on("open-url", (event, url) => {
    event.preventDefault();
    handleDeepLink(url);
  });
}

function handleDeepLink(url: string) {
  const parsed = new URL(url);
  console.log("Deep link:", parsed.pathname, parsed.searchParams);
  // Route to appropriate view
}
```

---

## 💥 Crash Reporting

### Built-in crashReporter

```typescript
// main.ts
import { crashReporter } from "electron";

crashReporter.start({
  productName: "MyApp",
  submitURL: "https://your-crash-server.com/submit",
  uploadToServer: true,
  extra: {
    app_version: app.getVersion(),
    build_type: process.env.NODE_ENV,
  },
});
```

### Sentry Integration

```typescript
// main.ts
import * as Sentry from "@sentry/electron/main";

Sentry.init({
  dsn: "https://your-dsn@sentry.io/project",
  release: app.getVersion(),
});

// preload.ts
import * as Sentry from "@sentry/electron/renderer";

Sentry.init({
  dsn: "https://your-dsn@sentry.io/project",
});
```

---

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

## 📁 Project Structure

```
my-electron-app/
├── src/
│   ├── main/              # Main process
│   │   ├── index.ts       # Entry point
│   │   ├── ipc.ts         # IPC handlers
│   │   ├── tray.ts        # System tray
│   │   ├── shortcuts.ts   # Global shortcuts
│   │   ├── updates.ts     # Auto-updater
│   │   └── database.ts    # SQLite
│   ├── preload/           # Preload scripts
│   │   ├── index.ts       # Main preload
│   │   └── index.d.ts     # Type declarations
│   └── renderer/          # Renderer (React/Vue)
│       ├── App.tsx
│       └── main.tsx
├── e2e/                   # E2E tests
│   └── app.spec.ts
├── electron.vite.config.ts
├── electron-builder.json5
├── playwright.config.ts
└── package.json
```

---

## ✅ Best Practices Checklist

### Security

- [ ] Context isolation enabled
- [ ] Node integration disabled
- [ ] Sandbox enabled
- [ ] CSP configured
- [ ] Input validation in IPC handlers
- [ ] Code signing configured

### IPC

- [ ] Use invoke/handle pattern
- [ ] Limited API exposure
- [ ] Validate sender
- [ ] Type-safe preload API
- [ ] Cleanup event listeners

### Performance

- [ ] Async IPC only
- [ ] No remote module
- [ ] Lazy window loading
- [ ] Worker threads for heavy tasks

### Distribution

- [ ] Auto-update configured
- [ ] Crash reporting enabled
- [ ] Logging configured
- [ ] All platforms tested

---

## 🔌 HSA Integration

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain   | Query Examples                              |
| -------- | ------------------------------------------- |
| Security | "context isolation sandbox preload"         |
| IPC      | "invoke handle ipcMain ipcRenderer"         |
| Updates  | "auto update electron-updater signing"      |
| Storage  | "better-sqlite3 electron-store safeStorage" |
| Native   | "tray notification shortcut deep link"      |
| Testing  | "Playwright E2E Vitest unit test"           |

---

_DOMYH Awesome Code • Electron 35-40 • HSA v1.0.0 • 2026_
