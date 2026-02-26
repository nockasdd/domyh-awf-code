---
name: browser-agent-advanced
---

# Browser Agent Advanced Patterns

> Reference only — loaded when explicitly needed via ADVANCED.md tier.

## Multi-Page Verification Workflow

```
Complete Application Verification:

Page Discovery:
  1. Navigate to root URL
  2. browser_snapshot → find all links (role=link)
  3. Map unique internal routes
  4. Create page queue

Per-Page Loop:
  For each page in queue:
    1. browser_navigate(page.url)
    2. Run 5-phase verification flow
    3. Collect results
    4. Move to next page

Cross-Page Tests:
  1. Navigation consistency (same nav on all pages)
  2. Footer consistency
  3. Auth state persistence
  4. Back/forward navigation
```

### Implementation

```typescript
// Multi-page verification orchestration
async function verifyApplication(rootUrl: string) {
  const pages = await discoverPages(rootUrl);
  const results: PageResult[] = [];

  for (const page of pages) {
    // Phase 1: Load
    await browser_navigate({ url: page.url });
    await browser_wait_for({ time: 2 });

    // Phase 2: Discover
    const snapshot = await browser_snapshot();
    const elements = parseElements(snapshot);

    // Phase 3: Test each element
    for (const element of elements) {
      const result = await testElement(element);
      results.push(result);
    }

    // Phase 4: Edge cases
    await checkConsoleErrors();
    await checkNetworkErrors();
    await testResponsive();
  }

  // Phase 5: Report
  return generateReport(results);
}
```

## Complex Interaction Chains

### Chain: Button → Modal → Form → Success

```
Step 1: Click "Add User" button
  └─ browser_click(ref="add-user-btn")
  └─ browser_snapshot() → verify dialog visible

Step 2: Fill modal form
  └─ browser_fill_form([
       { ref: "name", type: "textbox", value: "John Doe" },
       { ref: "email", type: "textbox", value: "john@test.com" },
       { ref: "role", type: "combobox", value: "Admin" }
     ])

Step 3: Submit form
  └─ browser_click(ref="submit-btn")
  └─ browser_wait_for({ text: "Success" })

Step 4: Verify success
  └─ browser_snapshot() → modal closed
  └─ browser_snapshot() → new user in list
  └─ browser_take_screenshot() → visual evidence
```

### Chain: Search → Filter → Sort → Paginate

```
Step 1: Type search query
  └─ browser_type(ref="search", text="admin")
  └─ browser_wait_for({ text: "results" })

Step 2: Apply filter
  └─ browser_click(ref="role-filter")
  └─ browser_select_option(ref="role-filter", values=["admin"])

Step 3: Sort by column
  └─ browser_click(ref="name-header")
  └─ browser_snapshot() → verify sort indicator

Step 4: Navigate pages
  └─ browser_click(ref="next-page")
  └─ browser_snapshot() → page 2 content
```

## Error Recovery Patterns

### Pattern: Element Not Found Recovery

```
Attempt: browser_click(ref="submit-btn")
Error: Element not found

Recovery:
  1. browser_snapshot() — re-read page state
  2. Search for similar element:
     - Look for role=button with name containing "submit"
     - Look for button with aria-label
  3. If found with different ref → retry with new ref
  4. If not found → report as issue with screenshot evidence
```

### Pattern: State Transition Failure

```
Attempt: Click "Save" → expect "Saved" message
Error: Message not appearing

Recovery:
  1. Check browser_console_messages(level="error")
     → If JS error → report with error details
  2. Check browser_network_requests
     → If API 500 → report as backend issue
  3. browser_wait_for({ time: 5 })
     → Retry with longer timeout
  4. If still failing → screenshot + report
```

### Pattern: Modal Won't Close

```
Attempt: browser_press_key("Escape") → modal still visible
Recovery:
  1. Look for close button: browser_snapshot → find X button
  2. browser_click(ref="close-btn")
  3. If still open → try overlay click
  4. If still open → report as critical bug
```

## Performance Profiling via Browser Agent

```
Performance Checks:
  1. Page load time
     └─ browser_evaluate(() => performance.timing.loadEventEnd - performance.timing.navigationStart)

  2. Largest Contentful Paint
     └─ browser_evaluate(() => {
          const entries = performance.getEntriesByType('largest-contentful-paint');
          return entries[entries.length - 1]?.startTime;
        })

  3. DOM element count
     └─ browser_evaluate(() => document.querySelectorAll('*').length)

  4. Memory usage
     └─ browser_evaluate(() => performance.memory?.usedJSHeapSize)
```

## Multi-Agent Coordination

### Orchestrator Delegates to Browser Agent

```
Orchestrator receives: "Build the login page and verify it works"

Step 1: Developer persona — writes login page code
Step 2: Orchestrator delegates to Browser Agent:
  browser_subagent(
    TaskName: "Verify Login Page",
    Task: "Navigate to http://localhost:3000/login.
           1. Verify page loads (no errors)
           2. Test email input (type, clear, validation)
           3. Test password input (type, mask verification)
           4. Test 'Sign in' button (click, disabled when empty)
           5. Test form submission (valid + invalid credentials)
           6. Test 'Forgot password' link navigation
           Return: pass/fail table for all 6 tests",
    RecordingName: "login_verification"
  )
Step 3: Orchestrator reviews results
Step 4: If failures → Developer fixes → re-delegate to Browser Agent
```

## Advanced Subagent Task: Responsive Matrix

```
Task for browser_subagent:
"Navigate to {URL}. Test at these viewport sizes:

1. Desktop (1280x720):
   - Take screenshot
   - Verify navigation is horizontal
   - Verify sidebar visible

2. Tablet (768x1024):
   - browser_resize(768, 1024)
   - Take screenshot
   - Verify navigation is horizontal
   - Verify sidebar collapsed or hidden

3. Mobile (375x812):
   - browser_resize(375, 812)
   - Take screenshot
   - Verify hamburger menu appears
   - Click hamburger → verify menu opens
   - Verify content single-column

Return: 3 screenshots + pass/fail for each breakpoint"
```

## Checklist

- [ ] Multi-page discovery implemented?
- [ ] Complex interaction chains tested?
- [ ] Error recovery handled?
- [ ] Performance metrics collected?
- [ ] Responsive matrix verified?
- [ ] Multi-agent coordination documented?

---
