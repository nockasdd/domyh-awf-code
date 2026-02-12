---
description: "⚡ Quick-fix pipeline: capture error → identify → fix → verify (max 60s)"
skills: { required: [], contextual: [auto] }
---

# ⚡ /fix — Fix Pro

> Fast, Targeted Error Resolution
> 📚 Single-Pass Fix • Auto-Retry • Max 60s

---

## FIX FLOW

1. **DETECT** (5s) — Parse error, detect stack via HSA (`hsa_detect_stack`), load context (`hsa_get_context`), locate file + line, read surrounding code, classify fix category
2. **EXECUTE** (30s) — Apply targeted fix, minimal changes only, preserve existing behavior
3. **VERIFY** (15s) — Build/syntax check, run affected tests → If FAIL: retry (max 2) → If still FAIL: escalate to `/debug`
4. **SYNC** — `hsa_check_changes` to update index after edits

---

## COMMANDS

| Command        | Description             | Speed     |
| -------------- | ----------------------- | --------- |
| `/fix [error]` | Fix specific error      | ⚡ Fast   |
| `/fix last`    | Fix last terminal error | ⚡ Fast   |
| `/fix build`   | Fix build errors        | ⚡ Fast   |
| `/fix lint`    | Fix all lint errors     | ⚡ Fast   |
| `/fix types`   | Fix type errors         | ⚡ Fast   |
| `/fix imports` | Fix import errors       | ⚡ Fast   |
| `/fix tests`   | Fix failing tests       | 🔧 Medium |

---

## ⚡ vs 🐛 Khi nào dùng /fix vs /debug?

| Use `/fix` when                               | Use `/debug` when                        |
| --------------------------------------------- | ---------------------------------------- |
| Error message rõ ràng (compile, type, import) | Lỗi logic phức tạp, không rõ nguyên nhân |
| Biết file nào lỗi                             | Runtime error intermittent               |
| Fix đơn giản (< 10 lines)                     | Need root cause analysis                 |
| Cần fix nhanh để unblock                      | Multiple files involved                  |
| —                                             | `/fix` đã thử 2 lần vẫn fail             |

---

## 🔧 FIX CATEGORIES

| Category    | Detect Pattern                          | Approach                       | Confidence |
| ----------- | --------------------------------------- | ------------------------------ | ---------- |
| Syntax      | SyntaxError, unexpected token           | Auto-fix syntax                | 95%        |
| Types       | TypeError, type mismatch, TS errors     | Add/update types               | 90%        |
| Imports     | ModuleNotFoundError, Cannot find module | Fix paths, add missing         | 95%        |
| Null safety | Cannot read property of null/undefined  | Null checks, optional chaining | 85%        |
| Build       | Build failed, compilation error         | Fix config, missing deps       | 80%        |
| Lint        | ESLint, golangci-lint, ruff             | Auto-fix or recommended        | 90%        |
| Dependency  | Version mismatch, peer dependency       | Update/install correct         | 85%        |

---

## 🎨 UI FIX CATEGORY (→ FLOW.md §18.6)\r\n\r\n| Category | Detect Pattern | Additional Steps |\r\n|-----------|---------------------------------------------|---------------------------------------|\r\n| CSS/Style | overflow, z-index, opacity, display, visible | Load design tokens, check dark mode |\r\n| Layout | flex/grid, position, float, alignment | Verify responsive (mobile + desktop) |\r\n| Color | color, background, gradient, contrast | Verify WCAG contrast ≥ 4.5:1 |\r\n| Font | font-size, line-height, font-family | Check typography scale compliance |\r\n| Animation | transition, transform, keyframes | Check prefers-reduced-motion |\r\n| Dark Mode | dark: prefix, color-scheme, theme toggle | Test both modes after fix |\r\n\r\nWhen UI fix detected → auto-load `domyh-design` skill, apply §18.6 additional verify.\r\n\r\n---\r\n\r\n## 🔄 ESCALATION

After 2 retries fail:

- 1️⃣ Gọi `/debug` để phân tích sâu
- 2️⃣ Thử cách khác
- 3️⃣ Bỏ qua, làm tiếp

---

## ⛔ SAFETY

- Max changed files: 3
- Max changed lines: 30
- Require confirmation if: > 3 files, > 30 lines, modifies test/config files
