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
version: "4.3"
---

# Testing Patterns (2025)

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

_DOMYH Agent v4.2_
