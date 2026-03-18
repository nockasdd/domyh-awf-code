---
name: playwright
description: "Playwright E2E testing patterns. Use when writing browser automation or end-to-end tests."
detect: ["playwright.config.*", "*.e2e.*", "tests/e2e/**"]
category: cross-cutting
tier: 1
---

# Playwright Browser Automation (2026)

> Comprehensive browser testing skill with 58-checkpoint interaction checklist. Check `data/` for lookup tables.

## 📦 Data Files

| File                         | Content                                 | Records |
| ---------------------------- | --------------------------------------- | ------- |
| `mcp-tools.yaml`             | 19 Playwright MCP tool definitions      | 19      |
| `interaction-checklist.yaml` | 58 mandatory UI interaction checkpoints | 58      |
| `locator-patterns.yaml`      | Priority-ordered locator strategies     | 5       |
| `config-templates.yaml`      | CI/local/mobile/visual configs          | 4       |
| `ai-agents.yaml`             | Planner/Generator/Healer patterns       | 3       |
| `open-source-tools.yaml`     | Browser automation ecosystem            | 8       |

## 🎯 Core Problem & Solution

```
❌ Agent chỉ kiểm tra: page load, layout, text visible
✅ Agent PHẢI kiểm tra: dropdown, modal, button, hover, form, keyboard nav
```

**Solution**: 58-checkpoint interaction checklist — buộc test TỪNG interactive element.

## 🛠️ MCP Tools Quick Reference

### Navigation (5 tools)

| Tool                    | Purpose           |
| ----------------------- | ----------------- |
| `browser_navigate`      | Mở URL            |
| `browser_navigate_back` | Quay lại          |
| `browser_close`         | Đóng browser      |
| `browser_resize`        | Thay đổi viewport |
| `browser_tabs`          | Quản lý tabs      |

### Interaction (9 tools) — **CRITICAL cho comprehensive testing**

| Tool                    | Use Case                            |
| ----------------------- | ----------------------------------- |
| `browser_click`         | Button, link, tab, accordion        |
| `browser_type`          | Form input, search                  |
| `browser_press_key`     | Escape đóng modal, Enter submit     |
| `browser_hover`         | Tooltip, dropdown menu, hover state |
| `browser_select_option` | Native `<select>` dropdown          |
| `browser_drag`          | Drag-and-drop, reorder              |
| `browser_file_upload`   | File input                          |
| `browser_handle_dialog` | Alert/confirm/prompt                |
| `browser_fill_form`     | Nhiều fields cùng lúc               |

### Observation (5 tools)

| Tool                       | Use Case                          |
| -------------------------- | --------------------------------- |
| `browser_snapshot`         | **CORE: LLM hiểu page structure** |
| `browser_take_screenshot`  | Visual verification               |
| `browser_evaluate`         | Run JS, check DOM/CSS             |
| `browser_console_messages` | Error detection                   |
| `browser_network_requests` | API verification                  |

## 🎯 Locator Priority

```
1. getByRole('button', { name: 'Submit' })  ← BEST (semantic)
2. getByLabel('Email')                       ← Form fields
3. getByTestId('submit-btn')                 ← Explicit markers
4. getByText('Sign in')                      ← Visible content
5. locator('.btn-primary')                   ← LAST RESORT
```

## 📋 58-Checkpoint Summary

### Dropdown (18 checks)

- **Functional**: open list, select updates value, default value, dependent, multi-select, search
- **Keyboard**: Tab focus, Enter/Space open, arrows navigate, typing jumps, Escape close
- **Visual**: no truncation, scroll, no layout shift
- **Validation**: required error, invalid input blocked, clear message

### Modal (16 checks)

- **Trigger**: button triggers, centered overlay, background blocked, content visible
- **Close**: X button, overlay click, Escape key, focus returns
- **Keyboard**: Tab trap inside, Shift+Tab backward, no focus escape, screen reader
- **Form**: submit works, validation, success/error states

### Button (14 checks)

- **Functional**: click performs action, state changes, rage-click safe, disabled, navigation, toggle
- **Visual**: consistent design, hitbox accurate, text meaningful, responsive
- **Accessibility**: Tab order, Enter activates, focus visible, screen reader name

### Hover (10 checks)

- **Trigger**: hover triggers state, content persists, keyboard equivalent
- **Content**: readable, no layout shift, no obstruction
- **Dismiss**: Escape dismisses, no interference
- **Technical**: CSS states correct, JS handlers work

## 🤖 AI Test Agents

| Agent         | Role                             | I/O                        |
| ------------- | -------------------------------- | -------------------------- |
| **Planner**   | Explore app → generate test plan | App URL → Markdown plan    |
| **Generator** | Plan → executable tests          | Markdown → Playwright code |
| **Healer**    | Detect UI changes → repair tests | Failed test → Fixed code   |

## 🔍 Decision Tree

```
Need to interact with page?
├─ Understand page structure → browser_snapshot (accessibility tree)
├─ Visual verification → browser_take_screenshot
├─ Click/type/select → browser_click / browser_type / browser_select_option
├─ Open modal → browser_click trigger → browser_snapshot modal content
├─ Close modal → browser_press_key "Escape"
├─ Test dropdown → browser_click → browser_select_option → browser_snapshot
└─ Check errors → browser_console_messages + browser_network_requests
```

## ⚠️ Common Pitfalls

| ❌ Don't                             | ✅ Do                                       |
| ------------------------------------ | ------------------------------------------- |
| Use screenshot for LLM understanding | Use `browser_snapshot` (accessibility tree) |
| Test only page load                  | Test ALL interactive elements               |
| Use CSS selectors                    | Use `getByRole()` / `getByLabel()`          |
| Skip keyboard testing                | Test Tab, Enter, Escape                     |
| Ignore console errors                | Always check `browser_console_messages`     |
| Single browser                       | Cross-browser: Chromium + Firefox + WebKit  |

## Playwright Config (Quick Start)

```typescript
import { defineConfig, devices } from "@playwright/test";
export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  reporter: "html",
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
    { name: "firefox", use: { ...devices["Desktop Firefox"] } },
    { name: "mobile", use: { ...devices["iPhone 14"] } },
  ],
});
```

## Page Object Model

```typescript
import { Page, Locator, expect } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly email: Locator;
  readonly password: Locator;
  readonly submit: Locator;
  readonly errorMsg: Locator;

  constructor(page: Page) {
    this.page = page;
    this.email = page.getByLabel("Email");
    this.password = page.getByLabel("Password");
    this.submit = page.getByRole("button", { name: "Sign in" });
    this.errorMsg = page.getByRole("alert");
  }

  async login(email: string, password: string) {
    await this.email.fill(email);
    await this.password.fill(password);
    await this.submit.click();
  }

  async expectError(message: string) {
    await expect(this.errorMsg).toContainText(message);
  }
}
```

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain    | Query Examples                        |
| --------- | ------------------------------------- |
| MCP Tools | "browser_click browser_snapshot"      |
| Checklist | "dropdown testing modal verification" |
| Locators  | "getByRole getByLabel priority"       |
| Config    | "CI pipeline mobile testing"          |
| AI Agents | "planner generator healer"            |
| Tools     | "stagehand browser-use midscene"      |

**Data domains**: `mcp-tools`, `interaction-checklist`, `locator-patterns`, `config-templates`, `ai-agents`, `open-source-tools`

---
