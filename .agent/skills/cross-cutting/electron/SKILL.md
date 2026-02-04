---
name: electron
detect: ["electron.vite.config.ts", "main.ts:electron", "preload.ts"]
version: "6.1.2"
category: desktop
tier: 1
---

# Electron Patterns — DOMYH Awesome Code v6.1.2

> **Version**: Electron 33+ (2025-2026)
> **Philosophy**: Context isolation, secure IPC, minimal privileges

---

## 🎯 When to Use This Skill

Use for: Cross-platform desktop apps, web tech on desktop.
**NOT for**: Mobile (→ react-native), CLI tools (→ nodejs).

---

## 📦 Recommended Stack (2025-2026)

### Core

| Tool                 | Use Case             |
| -------------------- | -------------------- |
| **Electron 33+**     | Desktop framework 🏆 |
| **electron-vite**    | Build tool           |
| **electron-builder** | Packaging            |

### UI Frameworks

| Library    | Use Case       |
| ---------- | -------------- |
| **React**  | Component UI   |
| **Vue**    | Progressive UI |
| **Svelte** | Compiled UI    |

### IDE Support

| IDE          | Features             |
| ------------ | -------------------- |
| **VS Code**  | Built on Electron 🏆 |
| **WebStorm** | Full support         |

---

## 🔒 Security Best Practices

### Context Isolation (Required)

```typescript
// main.ts
import { BrowserWindow } from "electron";

const mainWindow = new BrowserWindow({
  webPreferences: {
    // ✅ Always enable
    contextIsolation: true,
    nodeIntegration: false,
    sandbox: true,

    // ✅ Preload script path
    preload: path.join(__dirname, "preload.js"),

    // ✅ Disable devtools in production
    devTools: !app.isPackaged,
  },
});
```

### Secure Preload Script

```typescript
// preload.ts
import { contextBridge, ipcRenderer } from "electron";

// ✅ Expose limited API via contextBridge
contextBridge.exposeInMainWorld("electronAPI", {
  // ✅ Only expose what renderer needs
  openFile: () => ipcRenderer.invoke("dialog:openFile"),
  saveFile: (data: string) => ipcRenderer.invoke("file:save", data),

  // ✅ Receive events from main
  onUpdateProgress: (callback: (progress: number) => void) => {
    ipcRenderer.on("update:progress", (_, progress) => callback(progress));
  },

  // ✅ Never expose raw IPC
  // ❌ send: ipcRenderer.send  // DANGEROUS
});
```

### Renderer Type Definitions

```typescript
// preload.d.ts
export interface ElectronAPI {
  openFile: () => Promise<string | null>;
  saveFile: (data: string) => Promise<boolean>;
  onUpdateProgress: (callback: (progress: number) => void) => void;
}

declare global {
  interface Window {
    electronAPI: ElectronAPI;
  }
}
```

---

## 📡 IPC Communication

### Main Process Handlers

```typescript
// main.ts
import { ipcMain, dialog, BrowserWindow } from "electron";

// ✅ Use invoke/handle for request-response
ipcMain.handle("dialog:openFile", async (event) => {
  // ✅ Validate sender
  const window = BrowserWindow.fromWebContents(event.sender);
  if (!window) return null;

  const result = await dialog.showOpenDialog(window, {
    properties: ["openFile"],
    filters: [{ name: "Text", extensions: ["txt", "md"] }],
  });

  if (result.canceled) return null;
  return result.filePaths[0];
});

ipcMain.handle("file:save", async (event, data: string) => {
  // ✅ Validate and sanitize input
  if (typeof data !== "string") {
    throw new Error("Invalid data");
  }

  // Save logic here
  return true;
});
```

### Renderer Usage

```typescript
// renderer.ts (React example)
function FileManager() {
  const [content, setContent] = useState('');

  async function handleOpen() {
    // ✅ Use exposed API
    const filePath = await window.electronAPI.openFile();
    if (filePath) {
      // Handle file
    }
  }

  async function handleSave() {
    await window.electronAPI.saveFile(content);
  }

  return (
    <div>
      <button onClick={handleOpen}>Open</button>
      <button onClick={handleSave}>Save</button>
    </div>
  );
}
```

---

## 🔧 App Structure

```
my-electron-app/
├── src/
│   ├── main/           # Main process
│   │   ├── index.ts
│   │   └── ipc.ts
│   ├── preload/        # Preload scripts
│   │   ├── index.ts
│   │   └── index.d.ts
│   └── renderer/       # Renderer (React/Vue)
│       ├── App.tsx
│       └── main.tsx
├── electron.vite.config.ts
└── package.json
```

### electron-vite Config

```typescript
// electron.vite.config.ts
import { defineConfig, externalizeDepsPlugin } from "electron-vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  main: {
    plugins: [externalizeDepsPlugin()],
  },
  preload: {
    plugins: [externalizeDepsPlugin()],
  },
  renderer: {
    plugins: [react()],
  },
});
```

---

## 🛡️ CSP Configuration

```typescript
// main.ts
mainWindow.webContents.session.webRequest.onHeadersReceived(
  (details, callback) => {
    callback({
      responseHeaders: {
        ...details.responseHeaders,
        "Content-Security-Policy": [
          "default-src 'self'",
          "script-src 'self'",
          "style-src 'self' 'unsafe-inline'",
          "img-src 'self' data: https:",
          "connect-src 'self' https://api.yourapp.com",
        ].join("; "),
      },
    });
  },
);
```

---

## ✅ Best Practices Checklist

### Security

- [ ] Context isolation enabled
- [ ] Node integration disabled
- [ ] Sandbox enabled
- [ ] CSP configured
- [ ] Input validation in IPC

### IPC

- [ ] Use invoke/handle pattern
- [ ] Limited API exposure
- [ ] Validate sender
- [ ] Type-safe preload API

### Performance

- [ ] Async IPC only
- [ ] No remote module
- [ ] Lazy window loading
- [ ] Regular dependency audits

---

_DOMYH Awesome Code v6.1.2 • Electron 33+_
