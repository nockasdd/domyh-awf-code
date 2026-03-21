# Stop Conditions Rule v7.3.0
# v7.3: Added error chain breaker
---
name: stop-conditions
rule_id: "MOD-STP-001"

description: "When to pause and consult the user before proceeding."
category: "safety"

context:
  always_apply: true

# --- STOP CONDITIONS ---

conditions:
  critical:
    - trigger: "About to delete files, drop tables, or remove data"
      action: "STOP — confirm destructive action with impact description"
    - trigger: "About to modify auth, permissions, or security config"
      action: "STOP — confirm security change with impact analysis"
    - trigger: "Any action targeting production environment"
      action: "STOP — confirm production action, note it affects live users"

  high:
    - trigger: "3+ consecutive errors in same execution flow"
      action: |
        STOP — Error chain detected.
        1. Summarize all errors and what was tried for each
        2. DO NOT attempt another fix without fundamentally different approach
        3. If stuck: activate progressive-escalation or ask user
    - trigger: "Task requires changes outside original scope"
      action: "STOP — describe scope expansion and ask to proceed"
    - trigger: "Request has multiple valid interpretations"
      action: "STOP — list interpretations and ask which one"
    - trigger: "Cannot proceed without information not available"
      action: "STOP — describe what information is needed"
    - trigger: "Change affects > 200 lines or > 5 files"
      action: "STOP — present change plan with per-file justification before proceeding"
    - trigger: "Creating new function/class when existing one could be extended"
      action: "STOP — search existing codebase for similar patterns first (hsa_trace_flow or view callers)"

  medium:
    - trigger: "Need to add new external dependency"
      action: "Confirm package name, version, and purpose before adding"
    - trigger: "Proposed solution differs from project patterns"
      action: "Note deviation and reason, optionally confirm"
    - trigger: "Existing tests fail after changes"
      action: "After 2 retries → activate progressive-escalation module (REFLECT → REFRAME → WIDEN → DECOMPOSE → ESCALATE)"

# --- OVERRIDE PROTOCOL ---

override:
  critical: "Cannot be overridden"
  high: "Requires explicit user confirmation"
  medium: "Can be overridden by user preference or explicit request"

integration:
  tier: 1
  related_modules: ["progressive-escalation", "drift-prevention"]
