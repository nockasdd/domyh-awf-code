---
name: review
trigger: ["/review", "pr", "code review"]
persona: developer
description: "👀 Code review for PRs: logic, quality, security, and tests verification"
---

# 👀 /review — Code Review Pro v3.0

> Comprehensive Code Review
> 📚 5 Categories • Actionable Feedback • Best Practices

---

## 🔄 REVIEW FLOW

```
User: /review [target]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: GET CHANGES                    │
│ ▸ Identify PR/commit/files              │
│ ▸ Load diff                             │
│ ▸ Context analysis                      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: REVIEW                         │
│ ▸ Logic & Correctness                   │
│ ▸ Code Quality                          │
│ ▸ Security                              │
│ ▸ Performance                           │
│ ▸ Tests                                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: FEEDBACK                       │
│ ▸ Categorize findings                   │
│ ▸ Provide suggestions                   │
│ ▸ Prioritize issues                     │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: DECISION                       │
│ ▸ Approve / Comment / Request Changes   │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command            | Description             |
| ------------------ | ----------------------- |
| `/review`          | Review current changes  |
| `/review [file]`   | Review specific file    |
| `/review pr #123`  | Review GitHub PR        |
| `/review security` | Security-focused review |
| `/review quick`    | Quick sanity check      |

---

## ✅ REVIEW CHECKLIST

### 1️⃣ Logic & Correctness

```yaml
logic:
  - Does the code do what it's supposed to?
  - Are edge cases handled?
  - Is the business logic accurate?
  - Are there off-by-one errors?
  - Is error handling complete?
  - Are race conditions handled?
```

### 2️⃣ Code Quality

```yaml
quality:
  - Is the code readable?
  - Are names meaningful and consistent?
  - Is there code duplication?
  - Is complexity manageable?
  - Does it follow project conventions?
  - Are comments helpful (not redundant)?
```

### 3️⃣ Security

```yaml
security:
  - Is user input validated?
  - Are there injection vulnerabilities?
  - Are secrets hardcoded?
  - Is authentication/authorization correct?
  - Is sensitive data exposed in logs?
  - Are dependencies secure?
```

### 4️⃣ Performance

```yaml
performance:
  - Are there N+1 queries?
  - Is there unnecessary computation?
  - Are large datasets handled efficiently?
  - Is caching considered?
  - Are there memory leaks?
```

### 5️⃣ Tests

```yaml
tests:
  - Are tests included for new code?
  - Do tests cover edge cases?
  - Are tests meaningful (not just for coverage)?
  - Do all tests pass?
  - Is mocking appropriate?
```

---

## 💬 FEEDBACK FORMAT

### Comment Types

```yaml
types:
  blocker:
    emoji: "🔴"
    description: "Must fix before merge"

  issue:
    emoji: "🟠"
    description: "Should fix, but can discuss"

  suggestion:
    emoji: "💡"
    description: "Nice to have improvement"

  nitpick:
    emoji: "🔵"
    description: "Style preference, optional"

  question:
    emoji: "❓"
    description: "Need clarification"

  praise:
    emoji: "👏"
    description: "Good job, highlight"
```

### Comment Template

````markdown
📍 `file.ts:42`

🟠 **Issue:** Potential null pointer exception

The `user` object might be null if the query returns no results.

**Suggestion:**

```typescript
// Before
const name = user.name;

// After
const name = user?.name ?? "Unknown";
```
````

**Impact:** Runtime crash if user not found

````

---

## 📊 REVIEW REPORT

```markdown
👀 CODE REVIEW REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PR: #123 - Add user authentication
Author: @developer
Files: 12 changed (+450/-120)

## Summary

| Category | Status | Issues |
|----------|--------|--------|
| Logic | ⚠️ | 2 |
| Quality | ✅ | 0 |
| Security | 🔴 | 1 |
| Performance | ✅ | 0 |
| Tests | ⚠️ | 1 |

## Findings

### 🔴 Blockers (1)

1. **[Security]** `auth/login.ts:45`
   - Hardcoded JWT secret in code
   - Must move to environment variable

### 🟠 Issues (2)

1. **[Logic]** `user/service.ts:78`
   - Missing null check on user lookup

2. **[Logic]** `user/controller.ts:32`
   - Error message exposes internal details

### 💡 Suggestions (1)

1. **[Tests]** `auth/login.test.ts`
   - Missing test for invalid token scenario

### 👏 Praise

- Clean separation of concerns
- Good use of TypeScript types
- Comprehensive input validation

## Decision

❌ **Request Changes**

Please address the security blocker before merge.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
````

---

## 🔧 DECISION MATRIX

| Status                 | When to Use                     |
| ---------------------- | ------------------------------- |
| ✅ **Approve**         | All checks pass, no blockers    |
| 💬 **Comment**         | Minor suggestions, non-blocking |
| ❌ **Request Changes** | Blockers that must be fixed     |

---

## 🤖 AI-ASSISTED REVIEW

```yaml
ai_review:
  role: "AI as first-pass reviewer"
  human_oversight: required

  ai_focus:
    - Style consistency
    - Basic logic errors
    - Security patterns (OWASP)
    - Performance issues
    - Missing test coverage

  human_focus:
    - Business logic validation
    - Architectural decisions
    - Context-specific tradeoffs
    - Final approval

  workflow:
    1_ai_scan: "AI identifies potential issues"
    2_prioritize: "Rank by severity (blocker > issue > nit)"
    3_human_review: "Developer validates suggestions"
    4_feedback: "Accept/reject improves AI"
```

---

## 📊 PR COMPLEXITY SCORING

```yaml
complexity_score:
  formula: |
    files_changed * 0.2 +
    lines_added * 0.01 +
    lines_removed * 0.01 +
    cyclomatic_increase * 0.3

  levels:
    simple: "< 10 → Quick review (15 min)"
    medium: "10-30 → Standard review (30 min)"
    complex: "> 30 → Deep review needed (1h+)"

  recommendations:
    simple: "Single reviewer sufficient"
    medium: "Primary + secondary reviewer"
    complex: "Split PR if possible, architecture review"
```

---

## 🔗 GITHUB CLI INTEGRATION

```yaml
github_cli:
  view:
    pr_list: "gh pr list"
    pr_view: "gh pr view #123"
    pr_diff: "gh pr diff #123"
    pr_checks: "gh pr checks #123"

  checkout:
    local: "gh pr checkout #123"

  review:
    approve: "gh pr review --approve"
    comment: "gh pr review --comment -b 'LGTM'"
    request_changes: "gh pr review --request-changes -b 'Please fix...'"

  comment:
    inline: "gh pr comment --body 'comment'"
    file_line: "Use web UI for inline comments"
```

---

## 📋 BEST PRACTICES

```yaml
reviewer:
  - Review < 400 lines at a time
  - Take breaks after 60 minutes
  - Focus on logic, not style (use linters)
  - Be constructive, not critical
  - Ask questions when unclear
  - Praise good code
  - Use conventional comment prefixes

author:
  - Keep PRs small and focused
  - Write clear PR descriptions
  - Self-review before requesting
  - Respond to all comments
  - Don't take feedback personally
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Focus on critical files first
  - Use checklist approach
  - Group similar issues
  - AI pre-filter before human review
```

---

_DOMYH Agent v4.3 • Review Pro v3.1 • AI-Assisted Reviews_
