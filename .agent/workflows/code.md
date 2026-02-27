---
description: "💻 Write production-ready code, fix/improve existing projects, with proper error handling, types, and documentation"
skills: { required: [coding-rules], contextual: [auto, domyh-design, tailwind] }
success_criteria: "Feature implemented, build passes, tests written"
---

# 💻 /code — Code Pro

> Intelligent code generation & project improvement with language-specific patterns
> 📚 30+ Languages • Auto Test Loop • Fix/Improve Mode • Self-Review

---

## CODE FLOW

1. **DETECT** (Auto) — Parse intent (feature/bugfix/refactor), detect stack via HSA (`hsa_detect_stack`), load language skill via HSA (`hsa_get_context`, `hsa_search_skills`)
   - **UI INTENT CHECK**: Classify intent:
     T1 (Create new UI, no existing ref) → Load `domyh-design` skill → `hsa_design_analyze({scope: "full"})` → design tokens + accessibility guidelines
     T2 (Modify existing UI) → `hsa_design_analyze({scope: "full"})` → analyze existing components + design tokens → apply via `domyh-design` patterns
     T3 (Design-only, no code) → Route to `/visualize`
     Auto-load: `domyh-design` + `tailwind` skills
     Auto-run: `hsa_design_analyze` → design system search → inject design tokens + platform guidelines
2. **PLAN** — Break down into steps, identify dependencies → `hsa_prefetch` planned files → ⛔ STOP if major change (>50 lines). Show step count: `Plan: 4 steps, ~85 lines`
   **VARIATION CHECK** (if T1 or T2): Read `products.yaml` `style_alternatives` + `color_palette_variants`. Pick specific hex palette matching mood. NEVER default to generic blue.
   **UI PREVIEW** (if T1 or T2 detected):
   - Generate `{project}/.preview/{component}.html` — standalone HTML+CSS with design tokens as `:root` vars
   - Include: responsive breakpoints, dark mode toggle, focus-visible, hover/active states
   - Open via `browser_subagent` → take screenshot → show to user
   - → ⛔ **STOP: "Preview ready. Approve to implement in {framework}?"**
   - If user iterates → update preview HTML only (fast, no build)
3. **EXECUTE** — Write code following skill patterns, error handling + types, add tests (auto test loop). Show progress: `[Step 2/4] Creating auth middleware...`
4. **VERIFY** — Run tests → Fix → Repeat (max 3), lint check. Agent re-reads ALL generated code:
   - [ ] Matches original intent?
   - [ ] Edge cases handled?
   - [ ] No hardcoded values or magic numbers?
   - [ ] Error messages helpful and descriptive?
   - [ ] Names follow language conventions?
   - [ ] No security anti-patterns (hardcoded secrets, raw SQL)?
   - → If issues found: fix silently before output
   - **UI QUALITY GATE** (if UI intent detected):
     Apply Visual QA Pipeline (score /100):
     L1. Accessibility (30pts): WCAG 2.2 AA, contrast ≥ 4.5:1, keyboard nav, focus visible
     L2. Visual Consistency (25pts): design tokens (no magic values), spacing rhythm, typography scale
     L3. Responsiveness (20pts): 375px / 768px / 1024px / 1440px breakpoints pass
     L4. Interaction Quality (15pts): hover/focus/active states, loading/error states
     L5. Performance (10pts): CLS < 0.1, images optimized, CSS < 50KB
     L6. **Design Health** (bonus): `hsa_design_health()` → show Grade (A-F) + top issues + score /100
     Apply Nielsen Heuristic Check (§18.2 A10): 10 items, score ≥8/10
     Result: ≥90/100 → SHIP ✅ | 70-89 → FIX MINOR ⚠️ | <70 → REDESIGN ❌
     - [ ] Design tokens used (no magic color/spacing values)
     - [ ] Responsive: tested 375px, 768px, 1024px, 1440px
     - [ ] Dark mode: no pure black/white, CSS variables, prefers-color-scheme
     - [ ] SVG icons only (no emoji as icons)
     - [ ] Focus states visible, transitions 150-300ms
5. **SYNC** — `hsa_check_changes` to update index, `hsa_feedback` on key files used, output summary of changes, confidence score (1-10), next steps. Persist key decisions to `.agent/memory/state.json`

---

## SUB-COMMANDS

| Command                        | Description             | Mode     |
| ------------------------------ | ----------------------- | -------- |
| `/code [task]`                 | Generate code for task  | Create   |
| `/code fix [issue]`            | Fix existing issue      | Fix      |
| `/code improve [area]`         | Improve existing code   | Refactor |
| `/code add [feature]`          | Add feature to existing | Update   |
| `/code test [feature]`         | Generate tests only     | Test     |
| `/code secure [feature]`       | Generate secure code    | Create   |
| `/code quality analyze [path]` | Static analysis         | Analyze  |

---

## FIX/IMPROVE MODE

1. **DETECT** stack (auto) → 2. **ANALYZE** issue (scan files) → 3. **PLAN** fix (scope, confirm) → 4. **EXECUTE** fix → 5. **VERIFY** (tests, lint) → 6. **SELF-REVIEW** → 7. **SUMMARY**

### Priority Matrix

| Priority | Description                  | SLA          | Action               |
| -------- | ---------------------------- | ------------ | -------------------- |
| **P0**   | Critical security/breaking   | Immediate    | Must fix now         |
| **P1**   | Affects core functionality   | Same session | Fix before next task |
| **P2**   | Code quality/maintainability | This sprint  | Schedule fix         |
| **P3**   | Nice to have improvements    | Backlog      | Track                |

---

## LANGUAGE PATTERNS (Quick Reference)

> Full patterns loaded via language skills (HSA). Each skill has: patterns, style, error handling, structure, tests.

| Language   | Patterns               | Style           | Error Handling           | Tests           |
| ---------- | ---------------------- | --------------- | ------------------------ | --------------- |
| Go         | Interfaces, Channels   | gofmt           | error wrapping           | go test         |
| Python     | Type hints, Decorators | black, ruff     | try-except               | pytest          |
| TypeScript | Strict types, Generics | prettier+eslint | try-catch + custom Error | jest, vitest    |
| Rust       | Ownership, Traits      | rustfmt         | Result<T,E>              | cargo test      |
| Java       | Spring DI, Streams     | google-java     | try-catch                | JUnit 5         |
| C#         | .NET Core, LINQ        | dotnet format   | try-catch, nullable      | xUnit           |
| PHP        | Laravel patterns       | PHP-CS-Fixer    | try-catch                | PHPUnit         |
| Ruby       | Rails conventions      | rubocop         | begin-rescue             | RSpec           |
| Swift      | Protocols, Actors      | swift-format    | do-try-catch             | XCTest          |
| Kotlin     | Coroutines, DSL        | ktlint          | runCatching              | kotest          |
| C++        | RAII, Smart ptrs       | clang-format    | exceptions               | GoogleTest      |
| React      | Hooks, Context         | prettier        | ErrorBoundary            | RTL             |
| Next.js    | App Router, RSC        | prettier        | error.tsx                | Jest+Playwright |
| Vue        | Composition API        | eslint-vue      | onErrorCaptured          | Vitest          |
| Angular    | Signals, RxJS          | Angular Guide   | ErrorHandler             | Jasmine         |

> Mobile: React Native, Flutter, Swift(iOS), Kotlin(Android)
> Functional: Elixir, Haskell, Scala, OCaml
> Data/ML: Python+NumPy, R, Julia

---

## CODE QUALITY CONTRACT

```yaml
every_change:
  - Error handling at every boundary
  - Input validation on public APIs
  - Types/interfaces defined
  - Named exports preferred
  - Constants over magic numbers

test_loop:
  max_iterations: 3
  strategy: "Write test → Run → Fix → Repeat"
  coverage_target: "> 70% (new code)"

self_review:
  enabled: true
  trigger: "after_verify, before_output"
  checklist: 7 # items checked above
```

---

## SECURITY-FIRST

| Category | Default Behavior                         |
| -------- | ---------------------------------------- |
| Input    | Validate all user input, sanitize        |
| Output   | Context-aware encoding, XSS prevention   |
| Errors   | Non-revealing errors, structured logging |
| Secrets  | Environment variables, no hardcoded      |
| Queries  | Parameterized only (no raw SQL)          |
| Auth     | RBAC checks, secure sessions             |

---

## AI QUALITY GATES

| Layer | Name            | What                                       |
| ----- | --------------- | ------------------------------------------ |
| 1     | AI Auto-Fix     | Linting, formatting, naming, comments      |
| 2     | Static Analysis | Snyk, SonarQube, ESLint; cyclomatic < 10   |
| 3     | Self-Review     | Agent self-critique before delivery        |
| 4     | Human Review    | Complex logic, security, infra, >100 lines |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** — Update session memory:
   - Append task summary to `memory/session.md` (per SESSION_005 format)
   - If key decision made → append to `memory/decisions.md`
3. **SNAPSHOT** — If this is the last task in session:
   - Update `memory/CONTEXT_SNAPSHOT.md` (Recent Changes, Status, Decisions)
4. **ANCHOR** (if HSA available):
   - `hsa_track_progress(level: "action", label: "[workflow] completed", status: "completed")`
   - `hsa_save_anchor(content: "[SESSION] Done: [summary]. Files: [list].", category: "context")`

