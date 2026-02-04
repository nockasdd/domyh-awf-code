---
name: refactor
trigger: ["/refactor", "clean", "improve"]
persona: developer
description: "🔧 Code refactoring: identify smells → plan changes → apply → verify tests pass"
---

# 🔧 /refactor — Refactor Pro v3.1

> Safe, Incremental Code Improvement
> 📚 30+ Languages • Code Smells • Patterns

---

## 🔄 REFACTORING FLOW

```
User: /refactor [target]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: IDENTIFY                       │
│ ▸ Detect code smells                    │
│ ▸ Analyze complexity                    │
│ ▸ Find duplications                     │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: TEST BASELINE                  │
│ ▸ Run existing tests                    │
│ ▸ Ensure all pass                       │
│ ⛔ STOP if tests fail                   │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: PLAN                           │
│ ▸ Define changes                        │
│ ▸ Assess risk                           │
│ ⛔ STOP → Confirm before apply          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: REFACTOR                       │
│ ▸ Apply changes incrementally           │
│ ▸ Commit small batches                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Run tests again                       │
│ ▸ Compare before/after                  │
│ ▸ Validate behavior unchanged           │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command             | Description             |
| ------------------- | ----------------------- |
| `/refactor [file]`  | Refactor specific file  |
| `/refactor [dir]`   | Refactor directory      |
| `/refactor extract` | Extract method/function |
| `/refactor rename`  | Rename symbols          |
| `/refactor dedupe`  | Remove duplication      |

---

## 🧪 CODE SMELLS CATALOG

```yaml
code_smells:
  # ═══════════════════════════════════════════════════════════════
  # BLOATERS (Size Issues)
  # ═══════════════════════════════════════════════════════════════

  long_method:
    detect: "> 30 lines"
    fix: Extract Method

  large_class:
    detect: "> 500 lines"
    fix: Extract Class, Single Responsibility

  long_parameter_list:
    detect: "> 4 parameters"
    fix: Introduce Parameter Object

  # ═══════════════════════════════════════════════════════════════
  # OBJECT-ORIENTATION ABUSERS
  # ═══════════════════════════════════════════════════════════════

  switch_statements:
    detect: "Large switch/case"
    fix: Replace with Polymorphism

  refused_bequest:
    detect: "Unused inherited methods"
    fix: Replace Inheritance with Delegation

  # ═══════════════════════════════════════════════════════════════
  # CHANGE PREVENTERS
  # ═══════════════════════════════════════════════════════════════

  divergent_change:
    detect: "Class changed for multiple reasons"
    fix: Extract Class per responsibility

  shotgun_surgery:
    detect: "One change requires many small changes"
    fix: Move Method, Move Field

  # ═══════════════════════════════════════════════════════════════
  # DISPENSABLES
  # ═══════════════════════════════════════════════════════════════

  duplicate_code:
    detect: "Copy-pasted code"
    fix: Extract Method/Class

  dead_code:
    detect: "Unreachable code"
    fix: Remove

  speculative_generality:
    detect: "Unused abstractions"
    fix: Collapse Hierarchy

  # ═══════════════════════════════════════════════════════════════
  # COUPLERS
  # ═══════════════════════════════════════════════════════════════

  feature_envy:
    detect: "Method uses another class's data more"
    fix: Move Method

  inappropriate_intimacy:
    detect: "Classes access each other's internals"
    fix: Extract Class, Hide Delegate
```

---

## 📋 REFACTORING PATTERNS

```yaml
patterns:
  extract_method:
    before: |
      function process() {
        // 50+ lines of mixed logic
      }
    after: |
      function process() {
        validateInput();
        transformData();
        saveResult();
      }

  early_return:
    before: |
      function foo(x) {
        if (x) {
          if (y) {
            if (z) {
              // deep nesting
            }
          }
        }
      }
    after: |
      function foo(x) {
        if (!x) return;
        if (!y) return;
        if (!z) return;
        // flat logic
      }

  replace_magic_numbers:
    before: |
      if (status === 1) { ... }
      if (timeout > 30000) { ... }
    after: |
      const STATUS_ACTIVE = 1;
      const TIMEOUT_MS = 30000;
      if (status === STATUS_ACTIVE) { ... }
      if (timeout > TIMEOUT_MS) { ... }
```

---

## 🔧 ANALYSIS TOOLS

```yaml
tools:
  go:
    complexity: "gocyclo"
    duplication: "dupl"
    lint: "golangci-lint"

  typescript:
    complexity: "eslint --rule complexity"
    duplication: "jscpd"
    lint: "eslint"

  python:
    complexity: "radon cc"
    duplication: "pylint --disable=all --enable=duplicate-code"
    lint: "ruff"

  java:
    complexity: "pmd"
    duplication: "simian"
    lint: "checkstyle"

  rust:
    lint: "clippy"
    complexity: "cargo-complexity"

  csharp:
    lint: "dotnet format"
    complexity: "NDepend"
```

---

## 📊 REFACTOR REPORT

```markdown
🔧 REFACTOR REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target: `src/services/user.ts`

## Smells Detected

| Smell          | Location   | Severity |
| -------------- | ---------- | -------- |
| Long Method    | L45-120    | High     |
| Duplicate Code | L200, L350 | Medium   |
| Magic Numbers  | L78, L92   | Low      |

## Changes Applied

| Change      | Before | After |
| ----------- | ------ | ----- |
| Complexity  | 25     | 8     |
| Lines       | 450    | 320   |
| Functions   | 5      | 12    |
| Duplication | 15%    | 2%    |

## Test Results

| Phase           | Status        |
| --------------- | ------------- |
| Before refactor | ✅ 45/45 pass |
| After refactor  | ✅ 45/45 pass |

## Commits

1. `refactor: extract validation logic`
2. `refactor: remove duplicate user lookup`
3. `refactor: replace magic numbers with constants`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🤖 AI SMELL DETECTION

```yaml
ai_smell_detection:
  description: "AI-assisted identification of code smells"

  tools:
    - "CodeAnt.ai (prioritized smells)"
    - "SonarQube (quality gates)"
    - "Cursor/Copilot (inline suggestions)"
    - "ESLint/RuboCop (static analysis)"

  workflow:
    1_analyze: "AI scans codebase for patterns"
    2_categorize: "Group by smell type"
    3_prioritize: "Rank by impact (high → low)"
    4_suggest: "AI proposes refactoring"
    5_validate: "Human reviews changes"

  commands:
    analyze_file: "/refactor analyze [file]"
    full_scan: "/refactor scan ."
```

---

## 🧪 CHARACTERIZATION TESTS

```yaml
characterization_tests:
  description: "Tests that document existing behavior"

  use_when:
    - "Legacy code without tests"
    - "Before major refactoring"
    - "Behavior is unclear"

  process:
    1_run: "Execute code with known inputs"
    2_capture: "Record actual outputs"
    3_assert: "Make output the expected value"
    4_repeat: "Cover edge cases"

  example: |
    // Generate test from current behavior
    it('legacy login - characterization', () => {
      const result = legacyLogin({ user: 'test' });
      // Captured from actual run
      expect(result).toEqual({
        token: expect.any(String),
        expires: 3600
      });
    });

  tools:
    - "Jest snapshot testing"
    - "Approval tests pattern"
    - "Golden master testing"
```

---

## 📝 INCREMENTAL COMMIT STRATEGY

```yaml
incremental_commits:
  rule: "One refactoring = One commit"

  pattern:
    - "refactor: extract validateUser()"
    - "refactor: rename userService → UserService"
    - "refactor: remove duplicate lookup"
    - "refactor: apply early return pattern"

  benefits:
    - "Easy to revert single change"
    - "Clear audit trail"
    - "Bisectable history"

  workflow: 1. "Make one refactoring"
    2. "Run tests"
    3. "If pass → commit"
    4. "Repeat"
```

---

## 📊 COMPLEXITY METRICS

```yaml
complexity_metrics:
  track_before_after:
    - cyclomatic_complexity
    - lines_of_code
    - duplication_percentage
    - function_count
    - nesting_depth

  command: "/refactor metrics [file]"

  output: |
    📊 COMPLEXITY ANALYSIS

    | Metric     | Before | After | Change |
    |------------|--------|-------|--------|
    | Complexity | 25     | 8     | ✅ -68% |
    | LOC        | 450    | 320   | ✅ -29% |
    | Duplication| 15%    | 2%    | ✅ -87% |
    | Functions  | 3      | 8     | ⬆️ +167%|
    | Max Depth  | 5      | 2     | ✅ -60% |

  thresholds:
    complexity: "< 10 per function"
    function_length: "< 50 lines"
    nesting: "< 3 levels"
```

---

## ⚠️ GOLDEN RULES

```yaml
rules:
  1_tests_first:
    rule: "All tests must pass BEFORE refactoring"
    if_no_tests: "Write characterization tests first"

  2_small_steps:
    rule: "Make one change at a time"
    commit_after: "Each successful refactoring step"

  3_no_behavior_change:
    rule: "External behavior must remain unchanged"
    verify: "Tests pass after each change"

  4_separate_concerns:
    rule: "Don't mix refactoring with bug fixes"
    reason: "Easier to revert if needed"

  5_ai_as_assistant:
    rule: "AI suggests, human decides"
    validate: "Review all AI suggestions"
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Focus on highest-impact smells first
  - Batch similar refactorings
  - Use standard patterns
  - AI pre-analysis before human review
```

---

_DOMYH Awesome Code v6.1.2 • Refactor Pro v3.1 • AI-Assisted Refactoring_
