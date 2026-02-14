## 📦 IPC Communication

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
