---
name: browser-agent
description: "Browser automation agent patterns. Use when implementing headless browser control or web scraping."
detect: []
category: tooling
tier: 1
---

# Browser Agent Verification Patterns (2026)

> AI IDE browser verification skill — forces comprehensive testing, not surface checks. Check `data/` for lookup tables.

## 📦 Data Files

| File                      | Content                            | Records |
| ------------------------- | ---------------------------------- | ------- |
| `verification-flow.yaml`  | 5-phase comprehensive testing flow | 5       |
| `subagent-patterns.yaml`  | browser_subagent task templates    | 5       |
| `element-discovery.yaml`  | Element categorization patterns    | 15      |
| `recording-patterns.yaml` | WebP recording best practices      | 6       |
| `reporting-patterns.yaml` | Evidence-based reporting templates | 4       |

## 🎯 Core Problem

```
❌ AI agent says: "Page loads correctly, layout looks good ✅"
   → MISSED: dropdown doesn't open, modal has no focus trap,
     button submits twice, hover tooltip obscured

✅ AI agent MUST: Test EVERY interactive element systematically
   → Dropdown opens? Select works? Keyboard nav? Escape closes?
   → Modal triggers? Focus trapped? Escape closes? Form submits?
   → Button performs action? Disabled works? Rage-click safe?
```

## 🔄 5-Phase Comprehensive Verification Flow

```
Phase 1: Page Load ────────────────── HTTP 200? Errors? Layout OK?
    ↓
Phase 2: Element Discovery ────────── browser_snapshot → list ALL elements
    ↓
Phase 3: Systematic Testing ───────── Test EACH element by type
    ↓
Phase 4: Accessibility & Edge Cases ─ Keyboard nav, console, network
    ↓
Phase 5: Evidence Report ──────────── Screenshots + pass/fail table
```

### Phase 1: Page Load Verification

| Step     | MCP Tool                   | Check           |
| -------- | -------------------------- | --------------- |
| Navigate | `browser_navigate`         | HTTP 200        |
| Wait     | `browser_wait_for`         | networkidle     |
| Errors   | `browser_console_messages` | No JS errors    |
| Layout   | `browser_take_screenshot`  | Visual baseline |

### Phase 2: Interactive Element Discovery

| Step       | MCP Tool           | Output                                        |
| ---------- | ------------------ | --------------------------------------------- |
| Snapshot   | `browser_snapshot` | Full accessibility tree                       |
| Parse      | —                  | List: buttons, links, inputs, selects, custom |
| Categorize | —                  | Group by type for Phase 3                     |

### Phase 3: Systematic Interaction Testing

| Element Type | Tests                                | MCP Tools                                                     |
| ------------ | ------------------------------------ | ------------------------------------------------------------- |
| Button       | Click → action, disabled, rage-click | `browser_click`, `browser_snapshot`                           |
| Dropdown     | Open, select, keyboard, close        | `browser_click`, `browser_select_option`, `browser_press_key` |
| Modal        | Trigger, focus trap, Escape, form    | `browser_click`, `browser_press_key`, `browser_fill_form`     |
| Hover        | Trigger, content, keyboard equiv     | `browser_hover`, `browser_press_key`                          |
| Form         | Fill, submit, validate, error        | `browser_fill_form`, `browser_click`, `browser_snapshot`      |

### Phase 4: Accessibility & Edge Cases

| Step          | MCP Tool                          | Check                  |
| ------------- | --------------------------------- | ---------------------- |
| Keyboard nav  | `browser_press_key(Tab)`          | All elements reachable |
| Focus visible | `browser_take_screenshot`         | Focus indicator shown  |
| Console       | `browser_console_messages(error)` | No errors              |
| Network       | `browser_network_requests`        | No 4xx/5xx             |
| Resize        | `browser_resize`                  | Responsive at 375px    |

### Phase 5: Evidence-Based Report

| Item       | Content                        |
| ---------- | ------------------------------ |
| Screenshot | Per-element evidence           |
| Pass/Fail  | Per-checkpoint table           |
| Issues     | Element + expected + actual    |
| Recording  | WebP video of interaction flow |

## 🤖 browser_subagent Task Template

```
Task: "Navigate to {URL}. Wait for page load.

1. Take a browser_snapshot and list ALL interactive elements
2. For EACH button: click it, verify the action, take screenshot
3. For EACH dropdown: open it, select an option, verify update
4. For EACH modal trigger: open modal, test Escape close, test focus trap
5. Check browser_console_messages for errors
6. Check browser_network_requests for failed requests

Return: List of all elements tested with pass/fail status."

RecordingName: "comprehensive_verification"
```

## 🔍 Decision Tree: Playwright MCP vs browser_subagent

```
Need browser interaction?
├─ Quick check (1-2 actions) → Use Playwright MCP tools directly
│   browser_navigate → browser_snapshot → browser_click
│
├─ Comprehensive verification → Use browser_subagent
│   Delegate entire 5-phase flow as one task
│
└─ Visual comparison → Use browser_subagent with screenshots
    Take screenshots before/after changes
```

## ⚠️ Anti-Patterns

| ❌ Don't                    | ✅ Do                                     |
| --------------------------- | ----------------------------------------- |
| "Page loads, looks good ✅" | Run 5-phase flow, test EVERY element      |
| Test only buttons           | Test buttons + dropdowns + modals + hover |
| Skip keyboard testing       | Test Tab/Enter/Escape on ALL elements     |
| Just take screenshot        | Take snapshot first (accessibility tree)  |
| Assume modal works          | Test focus trap, Escape close, overlay    |
| Test once                   | Test at mobile (375px) + desktop (1280px) |

## 📋 Quick Checklist

Before reporting "frontend works":

- [ ] Phase 1: Page loads without console errors?
- [ ] Phase 2: ALL interactive elements discovered?
- [ ] Phase 3: EACH element tested (click, select, type)?
- [ ] Phase 4: Keyboard navigation works?
- [ ] Phase 4: No 4xx/5xx network errors?
- [ ] Phase 5: Evidence (screenshots) collected?
- [ ] Responsive: Works at 375px mobile width?

## 🔌 HSA Integration

Data powered by HSA BM25 search engine:

| Domain    | Query Examples                         |
| --------- | -------------------------------------- |
| Flow      | "5-phase verification flow"            |
| Subagent  | "browser_subagent task template"       |
| Discovery | "element discovery accessibility tree" |
| Recording | "WebP recording naming convention"     |
| Reporting | "evidence-based report template"       |

**Data domains**: `verification-flow`, `subagent-patterns`, `element-discovery`, `recording-patterns`, `reporting-patterns`

---
