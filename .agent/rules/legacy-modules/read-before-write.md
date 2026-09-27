# Read-Before-Write Rule v7.2.0
# Enforce reading existing code before writing new code
# Source: Deep Think Analysis — Q8 (agent guessing instead of reading)
---
name: read-before-write
rule_id: "MOD-RBW-001"

description: "Enforce reading existing code before writing. Complements CTX-005."
category: "quality"

context:
  always_apply: true
  personas: ["developer", "debugger", "devops", "tester"]

rules:
  - id: RBW-001
    name: "Read Before Modify"
    severity: warning
    when: "Before modifying an existing file"
    action: |
      1. Read the FULL function/class being modified (not just the line)
      2. Read callers (hsa_trace_flow upstream if available)
      3. Read tests for the function (hsa_search '{function} test')
      4. ONLY THEN make changes
      Rationale: 60%+ of regressions come from not understanding call sites.

  - id: RBW-002
    name: "Search Before Create"
    severity: warning
    when: "Before creating a new file or function"
    action: |
      1. Search for similar files: hsa_search('{purpose}')
      2. If similar found → extend existing, don't create new
      3. If truly new → verify no module-name collision
      This enforces DRY (EXEC_004) with concrete steps.

  - id: RBW-003
    name: "Search Before Depend"
    severity: warning
    when: "Before adding a new dependency"
    action: |
      1. Search existing utils: hsa_search('{functionality needed}')
      2. If found → use existing code
      3. If not found → search skills for recommended libraries
      4. Check npm/pypi for package health (downloads, maintenance)
      5. ONLY THEN propose new dependency to user

integration:
  tier: 2
  related_modules: ["edit-verification", "quality", "yagni", "context-integrity"]
