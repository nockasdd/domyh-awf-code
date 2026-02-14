## 📦 Auto Updates

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
