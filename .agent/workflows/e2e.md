---
description: "🌐 E2E test generation: detect framework, write critical path tests, run and verify"
skills: { required: [testing, tdd-workflow], contextual: [auto] }
success_criteria: "E2E tests generated and passing for critical user flows"
---

# 🌐 /e2e — End-to-End Test Generation

> Generate and run E2E tests for critical user flows
> 📚 Playwright • Cypress • Selenium • Multi-browser

---

${RULES_E2E}
## E2E FLOW

1. **DETECT** — `hsa_session("generate E2E tests")`, detect stack via HSA (`hsa_detect`), verify environment (`hsa_detect`), identify frontend framework, existing E2E setup, test runner. Show: `[Step 1/6] Detecting E2E framework...`
2. **MAP** — Identify critical user flows from routes/pages. Show: `[Step 2/6] Mapping 8 critical user flows...`
3. **GENERATE** — Write E2E tests for critical paths. Show: `[Step 3/6] Generating tests for Login → Dashboard → Checkout`
4. **RUN** — Execute E2E tests, capture screenshots on failure. Show: `[Step 4/6] Running 12 E2E tests...`
5. **REPORT** — Show results with pass/fail, timing, screenshots. Show: `[Step 5/6] ✅ 11/12 passed (1 flaky)`
6. **SYNC** — `hsa_check_changes` to update index after test file creation

---

## COMMANDS

| Command       | Description                           |
| ------------- | ------------------------------------- |
| `/e2e`        | Generate E2E tests for critical flows |
| `/e2e [page]` | Generate E2E tests for specific page  |
| `/e2e run`    | Run existing E2E tests                |
| `/e2e smoke`  | Generate smoke tests only             |
| `/e2e visual` | Visual regression tests               |

---

## FRAMEWORK DETECTION

| Framework      | Config File            | Runner                |
| -------------- | ---------------------- | --------------------- |
| **Playwright** | `playwright.config.ts` | `npx playwright test` |
| **Cypress**    | `cypress.config.ts`    | `npx cypress run`     |
| **Selenium**   | `wdio.conf.ts`         | `npx wdio run`        |

If no E2E framework found:

1. Recommend Playwright (modern, fast, multi-browser)
2. Offer to scaffold: `npm init playwright@latest`

---

## CRITICAL FLOW IDENTIFICATION

Automatically identify critical flows from:

- **Routes/pages**: Login, dashboard, checkout, settings
- **Forms**: Registration, payment, contact
- **CRUD**: Create, read, update, delete operations
- **Auth**: Login, logout, password reset, 2FA

Priority:

1. 🔴 **Revenue flows**: Checkout, payment, subscription
2. 🟠 **User onboarding**: Registration, login, first-use
3. 🟡 **Core features**: Primary user actions
4. 🟢 **Settings/profile**: Account management

---

## TEST STRUCTURE

```typescript
// Playwright E2E test template
import { test, expect } from "@playwright/test";

test.describe("User Login Flow", () => {
  test("should login with valid credentials", async ({ page }) => {
    // Arrange
    await page.goto("/login");

    // Act
    await page.fill('[data-testid="email"]', "user@example.com");
    await page.fill('[data-testid="password"]', "password123");
    await page.click('[data-testid="login-button"]');

    // Assert
    await expect(page).toHaveURL("/dashboard");
    await expect(page.locator('[data-testid="welcome"]')).toBeVisible();
  });

  test("should show error for invalid credentials", async ({ page }) => {
    await page.goto("/login");
    await page.fill('[data-testid="email"]', "wrong@example.com");
    await page.fill('[data-testid="password"]', "wrong");
    await page.click('[data-testid="login-button"]');
    await expect(page.locator('[data-testid="error"]')).toContainText(
      "Invalid",
    );
  });
});
```

---

## BEST PRACTICES

| Rule                            | Why                            |
| ------------------------------- | ------------------------------ |
| Use `data-testid` selectors     | Stable, decoupled from styling |
| One assertion per critical path | Clear failure identification   |
| Set up test data via API        | Faster than UI setup           |
| Clean up after tests            | Avoid inter-test dependencies  |
| Run in CI with retries          | Handle flakiness               |
| Screenshot on failure           | Visual debugging               |

---

## 🔄 CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE step** — see `delegation-intelligence` skill for scoring.

For E2E test generation, delegate to specialized model via cascade:
```
hsa_delegate({action:'cascade', cascade_text:'[detailed prompt]', task_type:'test'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
→ repeat cascade_read (3-5s intervals, max 10 polls)
```
**Auto-cascade** (weighted score ≥6.5): Multi-page flow (checkout, onboarding), >10 E2E tests
**Suggest cascade** (weighted score 4.0-6.5): Comprehensive E2E suite, cross-browser testing

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

