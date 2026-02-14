## 📦 Native Integrations

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
