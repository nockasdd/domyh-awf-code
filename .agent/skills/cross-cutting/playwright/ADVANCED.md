---
name: playwright-advanced
version: "1.0.0"
---

# Playwright Advanced Patterns

> Reference only — loaded when explicitly needed via ADVANCED.md tier.

## Full 58-Checkpoint Workflow

### Phase 1: Page Load Verification

```typescript
test("page load verification", async ({ page }) => {
  const response = await page.goto("http://localhost:3000");
  expect(response?.status()).toBe(200);
  await page.waitForLoadState("networkidle");

  // Check for console errors
  const errors: string[] = [];
  page.on("console", (msg) => {
    if (msg.type() === "error") errors.push(msg.text());
  });

  // Verify no JS errors
  expect(errors).toHaveLength(0);
});
```

### Phase 2: Interactive Element Discovery

```typescript
// Using MCP: browser_snapshot → returns accessibility tree
// Parse tree to find ALL interactive elements:
// - Buttons (role=button)
// - Links (role=link)
// - Inputs (role=textbox, role=combobox)
// - Selects (role=listbox)
// - Checkboxes (role=checkbox)
// - Dialogs (role=dialog)

test("discover all interactive elements", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  const buttons = await page.getByRole("button").all();
  const links = await page.getByRole("link").all();
  const inputs = await page.getByRole("textbox").all();
  const selects = await page.getByRole("combobox").all();

  console.log(
    `Found: ${buttons.length} buttons, ${links.length} links, ${inputs.length} inputs, ${selects.length} selects`,
  );

  // Each should be tested according to checklist
});
```

### Phase 3: Systematic Interaction Testing

#### Dropdown Complete Test

```typescript
test("dropdown comprehensive test", async ({ page }) => {
  await page.goto("/form");

  const dropdown = page.getByRole("combobox", { name: "Country" });

  // DD-F01: Click opens list
  await dropdown.click();
  await expect(page.getByRole("listbox")).toBeVisible();

  // DD-F02: All options present
  const options = await page.getByRole("option").all();
  expect(options.length).toBeGreaterThan(0);

  // DD-F03: Select updates value
  await page.getByRole("option", { name: "Vietnam" }).click();
  await expect(dropdown).toHaveValue("vietnam");

  // DD-K01: Tab focuses
  await page.keyboard.press("Tab");
  await page.keyboard.press("Shift+Tab"); // Back to dropdown
  await expect(dropdown).toBeFocused();

  // DD-K02: Enter opens
  await page.keyboard.press("Enter");
  await expect(page.getByRole("listbox")).toBeVisible();

  // DD-K03: Arrow navigation
  await page.keyboard.press("ArrowDown");
  await page.keyboard.press("ArrowDown");

  // DD-K05: Escape closes
  await page.keyboard.press("Escape");
  await expect(page.getByRole("listbox")).not.toBeVisible();
});
```

#### Modal Complete Test

```typescript
test("modal comprehensive test", async ({ page }) => {
  await page.goto("/");

  // MD-TD01: Trigger opens modal
  await page.getByRole("button", { name: "Open Settings" }).click();
  const modal = page.getByRole("dialog");
  await expect(modal).toBeVisible();

  // MD-TD03: Background blocked
  // Attempting click outside should not close (or close, depending on design)
  const modalContent = await modal.textContent();
  expect(modalContent).toBeTruthy();

  // MD-KA01: Tab trap inside modal
  const firstFocusable = modal.getByRole("button").first();
  await firstFocusable.focus();

  // Tab through all elements — should stay in modal
  for (let i = 0; i < 20; i++) {
    await page.keyboard.press("Tab");
    const focused = await page.evaluate(() => {
      const el = document.activeElement;
      const dialog = document.querySelector("[role=dialog]");
      return dialog?.contains(el);
    });
    expect(focused).toBeTruthy();
  }

  // MD-CB03: Escape closes
  await page.keyboard.press("Escape");
  await expect(modal).not.toBeVisible();

  // MD-CB04: Focus returns to trigger
  const trigger = page.getByRole("button", { name: "Open Settings" });
  await expect(trigger).toBeFocused();
});
```

#### Button Rage-Click Test

```typescript
test("button rage-click safety", async ({ page }) => {
  await page.goto("/checkout");

  let apiCalls = 0;
  await page.route("**/api/submit", (route) => {
    apiCalls++;
    route.fulfill({ status: 200, body: JSON.stringify({ ok: true }) });
  });

  const submitBtn = page.getByRole("button", { name: "Place Order" });

  // BT-F03: Rapid clicks
  await submitBtn.click();
  await submitBtn.click();
  await submitBtn.click();

  await page.waitForTimeout(500);
  expect(apiCalls).toBe(1); // Only 1 API call despite 3 clicks
});
```

## Visual Regression Testing

```typescript
test("visual regression", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");

  // Full page comparison
  await expect(page).toHaveScreenshot("homepage.png", {
    maxDiffPixelRatio: 0.01,
    animations: "disabled",
  });

  // Element-specific comparison
  const header = page.getByRole("banner");
  await expect(header).toHaveScreenshot("header.png");

  // After interaction
  await page.getByRole("button", { name: "Toggle dark mode" }).click();
  await expect(page).toHaveScreenshot("homepage-dark.png");
});
```

## Network Interception

```typescript
test("API error handling", async ({ page }) => {
  // Mock API failure
  await page.route("**/api/users", (route) => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: "Server error" }),
    });
  });

  await page.goto("/users");

  // Verify error UI
  await expect(page.getByRole("alert")).toContainText("Failed to load");
  await expect(page.getByRole("button", { name: "Retry" })).toBeVisible();
});
```

## Authentication State Management

```typescript
// fixtures.ts — Shared auth state
import { test as base } from "@playwright/test";

export const test = base.extend({
  authenticatedPage: async ({ browser }, use) => {
    const context = await browser.newContext({
      storageState: "auth-state.json", // Pre-saved auth cookies
    });
    const page = await context.newPage();
    await use(page);
    await context.close();
  },
});

// Save auth state (run once)
// npx playwright test --project=setup
test("save auth state", async ({ page }) => {
  await page.goto("/login");
  await page.getByLabel("Email").fill("admin@test.com");
  await page.getByLabel("Password").fill("password");
  await page.getByRole("button", { name: "Sign in" }).click();
  await page.waitForURL("/dashboard");
  await page.context().storageState({ path: "auth-state.json" });
});
```

## Cross-Browser Matrix Testing

```typescript
// playwright.config.ts — Full matrix
export default defineConfig({
  projects: [
    // Desktop
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "webkit", use: { ...devices["Desktop Safari"] } },
    { name: "edge", use: { ...devices["Desktop Edge"] } },

    // Mobile
    { name: "iphone", use: { ...devices["iPhone 14"] } },
    { name: "android", use: { ...devices["Pixel 7"] } },

    // Tablet
    { name: "ipad", use: { ...devices["iPad (gen 7)"] } },
  ],
});
```

## Trace Viewer Debugging

```typescript
// Capture trace for debugging
test("debug with trace", async ({ page, context }) => {
  await context.tracing.start({ screenshots: true, snapshots: true });

  await page.goto("/");
  // ... test steps ...

  // Save trace on failure
  await context.tracing.stop({ path: "trace.zip" });
  // View: npx playwright show-trace trace.zip
});
```

## Checklist

- [ ] 58 checkpoints applied to all interactive elements?
- [ ] Accessibility locators used (getByRole preferred)?
- [ ] Cross-browser tested (Chromium + Firefox + WebKit)?
- [ ] Mobile responsive verified?
- [ ] Console errors checked?
- [ ] Network requests verified?
- [ ] Visual regression baselines set?
- [ ] Authentication state managed?

---

_DOMYH Awesome Code — Playwright Advanced Patterns (Reference Only)_
