---
name: electron
version: "6.4.2"
category: desktop
---

﻿---
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

# Electron Patterns DOMYH Awesome Code

> **Version**: Electron 35-40 (2025-2026)
> **Chromium**: 134.0.6998+
> **Node.js**: 22.14.0
> **Philosophy**: Context isolation, secure IPC, minimal privileges, performant builds

---

## 📦 When to Use This Skill

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

## 📦 Build Tools Comparison

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

## 📚 Deep-Dive References

- **IPC Communication & Testing** — Inter-process communication, testing patterns
  → See [references/ipc-testing.md](references/ipc-testing.md)

- **Auto Updates & Data Persistence** — electron-updater, SQLite, keytar, electron-store
  → See [references/updates-persistence.md](references/updates-persistence.md)

- **Native Integrations & Deep Linking** — Tray, notifications, clipboard, protocol handlers
  → See [references/native-integrations.md](references/native-integrations.md)

- **Performance & Accessibility** — V8 optimization, memory, WCAG compliance
  → See [references/performance-accessibility.md](references/performance-accessibility.md)

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

## 📌 HSA Integration

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

_DOMYH Awesome Code Electron 35-40 HSA v1.0.0 2026_
