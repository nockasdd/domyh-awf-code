---
name: testing
detect:
  [
    "*.test.*",
    "*.spec.*",
    "jest.config.*",
    "vitest.config.*",
    "playwright.config.*",
  ]
version: "6.3.1"
---

# Testing Patterns (2026)

> Comprehensive testing skill with data-driven references. Check `data/` for lookup tables.

## 📦 Data Files

| File              | Content                                         | Records |
| ----------------- | ----------------------------------------------- | ------- |
| `frameworks.yaml` | Testing frameworks across 12 languages          | 20      |
| `patterns.yaml`   | Testing patterns, best practices, anti-patterns | 15      |

## 📦 Testing Frameworks

### Unit/Integration

| Framework   | Language      |
| ----------- | ------------- |
| **Vitest**  | TypeScript 🏆 |
| **Jest**    | JavaScript    |
| **Pytest**  | Python        |
| **Go test** | Go            |

### E2E

| Framework      | Use Case           |
| -------------- | ------------------ |
| **Playwright** | Cross-browser 🏆   |
| **Cypress**    | Developer friendly |

### API

- **Supertest**: Node.js API testing
- **Httpx**: Python async

## Test Structure (AAA)

```typescript
describe("UserService", () => {
  it("should create a user", async () => {
    // Arrange
    const input = { email: "test@test.com", name: "Test" };

    // Act
    const user = await service.createUser(input);

    // Assert
    expect(user.email).toBe(input.email);
    expect(user.name).toBe(input.name);
  });
});
```

## Vitest (2025 Standard)

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "node",
    coverage: {
      provider: "v8",
      reporter: ["text", "html"],
      thresholds: { lines: 80 },
    },
  },
});

// Test file
import { describe, it, expect, vi } from "vitest";

describe("UserService", () => {
  it("should fetch user", async () => {
    const mockRepo = {
      findById: vi.fn().mockResolvedValue({ id: 1, name: "Test" }),
    };

    const service = new UserService(mockRepo);
    const user = await service.getUser(1);

    expect(user.name).toBe("Test");
    expect(mockRepo.findById).toHaveBeenCalledWith(1);
  });
});
```

## Playwright E2E

```typescript
import { test, expect } from "@playwright/test";

test("should login successfully", async ({ page }) => {
  await page.goto("/login");
  await page.fill('[name="email"]', "test@test.com");
  await page.fill('[name="password"]', "password123");
  await page.click('button[type="submit"]');

  await expect(page).toHaveURL("/dashboard");
  await expect(page.locator("h1")).toContainText("Welcome");
});
```

## Test Types

| Type        | Coverage       | Speed  |
| ----------- | -------------- | ------ |
| Unit        | 80%+           | Fast   |
| Integration | 60%+           | Medium |
| E2E         | Critical paths | Slow   |

## Mocking

```typescript
// ✅ Vitest mocking
import { vi } from "vitest";

const mockFetch = vi.fn().mockResolvedValue({
  ok: true,
  json: () => Promise.resolve({ data: [] }),
});
vi.stubGlobal("fetch", mockFetch);

// ✅ Module mock
vi.mock("./api", () => ({
  fetchUsers: vi.fn().mockResolvedValue([]),
}));
```

## Checklist

- [ ] Units test pure logic?
- [ ] Integration tests APIs?
- [ ] E2E tests critical flows?
- [ ] Mocks isolated?
- [ ] Coverage >80%?

---

## 🌐 Browser Testing (Playwright Advanced)

> **Source**: Anthropic Webapp Testing
> **Purpose**: Test local web applications with reconnaissance-then-action pattern

### Decision Tree

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         └─ Write Playwright script using selectors
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Use helper script + write Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

### Reconnaissance Pattern

```typescript
import { test, expect } from "@playwright/test";

test("dynamic content test", async ({ page }) => {
  // Always wait for networkidle on dynamic apps
  await page.goto("http://localhost:3000");
  await page.waitForLoadState("networkidle"); // CRITICAL

  // Option 1: Screenshot for visual inspection
  await page.screenshot({ path: "/tmp/inspect.png", fullPage: true });

  // Option 2: Inspect rendered DOM
  const content = await page.content();
  const buttons = await page.locator("button").all();

  // Then execute actions with discovered selectors
  await page.click('button:has-text("Submit")');
});
```

### Common Pitfalls

| ❌ Don't                             | ✅ Do                                   |
| ------------------------------------ | --------------------------------------- |
| Inspect DOM before waiting           | Wait for `networkidle` first            |
| Use static selectors on dynamic apps | Discover selectors from rendered state  |
| Skip screenshot debugging            | Use screenshots for visual confirmation |

### Multi-Server Testing

```typescript
// Testing with backend + frontend
test.describe("Full stack test", () => {
  test.beforeAll(async () => {
    // Servers managed externally or via fixtures
  });

  test("API integration", async ({ page }) => {
    await page.goto("http://localhost:5173");
    await page.waitForLoadState("networkidle");

    // Verify frontend connects to backend
    await expect(page.locator('[data-testid="user-list"]')).not.toBeEmpty();
  });
});
```

### Best Practices

- Use `sync_playwright()` for synchronous scripts
- Always close the browser when done
- Use descriptive selectors: `text=`, `role=`, CSS selectors, or IDs
- Add appropriate waits: `page.wait_for_selector()` or timeouts
- Launch chromium in headless mode: `headless=True`

---

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain    | Query Examples                     |
| --------- | ---------------------------------- |
| Framework | "vitest typescript mocking"        |
| E2E       | "playwright cross-browser testing" |
| Pattern   | "AAA arrange act assert"           |
| Coverage  | "v8 coverage threshold"            |

**Data domains**: `frameworks`, `patterns`, `pyramid`, `mocking`, `coverage`

---

_DOMYH Awesome Code — Testing Patterns (Data-Driven + HSA)_
