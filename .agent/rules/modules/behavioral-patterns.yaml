# Behavioral Patterns — Anti-Pattern Examples
# Concrete BAD/GOOD examples teach LLM to avoid common reasoning failures.
# Referenced by SACRED_RULES.xml SURGICAL_001.
---
name: behavioral-patterns
rule_id: "MOD-BEH-001"
description: "Anti-pattern examples for LLM reasoning. BAD shows what LLMs do wrong. GOOD shows correct approach."
category: "quality"

context:
  always_apply: true
  personas: ["*"]
  trigger: "Every code implementation, refactor, or fix"

# Group 1: Surgical Changes (most critical — 60%+ of regressions)
surgical_changes:

  - id: SC-001
    name: "Scope Creep in Bug Fix"
    severity: critical
    bad: |
      User: "Fix the bug where empty emails crash the validator"
      Agent: Fixes empty check + improves regex + adds username validation
      Violation: Fixed 1 bug + 2 unrelated changes
    good: |
      User: "Fix the bug where empty emails crash the validator"
      Agent: Adds empty check ONLY. Existing code unchanged.
    self_check: "Does every changed line trace directly to user's request?"

  - id: SC-002
    name: "Style Imposition"
    severity: medium
    bad: |
      User: "Add logging to upload function"
      Agent: Adds logging + changes quotes ('' → "") + adds type hints + adds docstring
    good: |
      Adds logging only. Preserves existing quote style, formatting, and conventions.
    self_check: "Did I preserve existing style EXACTLY?"

  - id: SC-003
    name: "Cleanup Overreach"
    severity: medium
    bad: |
      User: "Add new endpoint"
      Agent: Adds endpoint + deletes old endpoint that 'looks unused'
    good: |
      Adds new endpoint. Mentions old endpoint may be unused: "I noticed `old_fn` appears unused. Want me to remove it?"
    self_check: "Did I touch code outside the explicit scope?"

# Group 2: Think Before Coding
think_first:

  - id: TC-001
    name: "Silent Assumption"
    severity: high
    bad: |
      User: "Add export feature"
      Agent: Implements CSV export of all users to /tmp/users.csv
      Violation: Assumed scope (all), location (/tmp), format (CSV) without asking
    good: |
      Agent: "Before implementing — clarify: (1) scope: all or filtered? (2) format: CSV/JSON? (3) destination: download/email/API?"
    self_check: "Did I list assumptions before writing code?"

  - id: TC-002
    name: "Specification Drift"
    severity: high
    bad: |
      User: "Add a simple login"
      Agent: Implements OAuth2 + MFA + session management + password reset
    good: |
      Agent: "By 'simple login' I'll do email+password+session cookie. Expanding to OAuth/MFA adds ~500 LOC. Confirm scope?"
    self_check: "Does my implementation match user's stated scope?"

# Group 3: Simplicity First
simplicity:

  - id: SF-001
    name: "Premature Abstraction"
    severity: medium
    bad: |
      User: "Add discount calculation"
      Agent: Creates DiscountStrategy ABC + PercentageDiscount class + factory (30+ LOC)
    good: |
      def calculate_discount(amount, percent): return amount * (percent / 100)
    self_check: "Would a senior engineer say this is overcomplicated?"

  - id: SF-002
    name: "Speculative Features"
    severity: high
    bad: |
      User: "Save user preferences to db"
      Agent: Adds save + caching + validation + merge + notify (30+ LOC of unrequested features)
    good: |
      def save_preferences(db, user_id, prefs):
          db.execute("UPDATE users SET preferences=? WHERE id=?", (json.dumps(prefs), user_id))
    self_check: "Is this feature explicitly requested or speculative?"

# Group 4: Verify Before Claiming Done
verification:

  - id: VR-001
    name: "Unverified Completion"
    severity: high
    bad: |
      Agent: "Fixed the auth bug. The code should work now." (no test, no evidence)
    good: |
      Agent: "Fixed auth bug. Verified: test_login_valid passes, test_login_invalid returns 401, regression tests pass."
    self_check: "What command proves this works? Did I run it?"

  - id: VR-002
    name: "Fix Without Reproducing"
    severity: critical
    bad: |
      User: "Sorting breaks with duplicate scores"
      Agent: Changes sort logic without writing failing test first
    good: |
      1. Write test reproducing bug (fails 10/10 runs)
      2. Apply fix (stable sort by name as tiebreaker)
      3. Test passes consistently
    self_check: "Can I write a test that reproduces this BEFORE fixing?"

integration:
  tier: 2
  related_modules: ["edit-verification", "stop-conditions", "drift-prevention"]
  referenced_by: ["SACRED_RULES.xml SURGICAL_001"]
