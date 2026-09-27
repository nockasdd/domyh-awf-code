# Session Governance v8.0.0
# Merged: session-governance + context-integrity
# Single source for session discipline, anchoring, and context coherence
---
name: session-governance
rule_id: "MOD-GOV-001"

description: "Session discipline: declare intent, track progress, anchor facts, check drift, preserve context across compaction."
category: "governance"

context:
  always_apply: true
  personas: ["*"]

rules:
  - id: GOV-001
    name: "Declare Before Code"
    severity: warning
    when: "Starting any significant task"
    action: |
      hsa_session({action:"intent", intent:"...", focus:"...", mode:"plan_driven|exploration|bugfix|refactor", goals:[...]})
      Creates session trajectory and enables drift detection.

  - id: GOV-002
    name: "Track Progress"
    severity: info
    when: "Completing milestone or starting sub-task"
    action: |
      hsa_session({action:"track", level:"trajectory|tactic|action", label:"...", status:"active|completed|blocked", parent_id:"..."})
      Hierarchy: 1 trajectory -> N tactics -> N actions.

  - id: GOV-003
    name: "Anchor Immutable Facts"
    severity: info
    when: "Discovering stack, conventions, or making architecture decisions"
    action: |
      hsa_session({action:"anchor", key:"...", value:"...", category:"stack|convention|decision|constraint|context"})
      Anchors survive context compaction. Save on: stack discovery, arch decisions, deployment constraints.

  - id: GOV-004
    name: "Drift Check"
    severity: warning
    when: "Before unplanned work or scope change"
    action: |
      hsa_session({action:"drift", focus:"current action", include_anchors:true})
      If drift: (1) evaluate necessity (2) update intent or refocus.

  - id: GOV-005
    name: "Context Gate Before Code"
    severity: warning
    when: "Before ANY code implementation"
    action: |
      5-step verifiable gate (each produces visible output):
        1. ANCHORS: hsa_session(include_anchors:true) — review prior decisions
        2. SEARCH: hsa_search(query) — find relevant files (>=1 required)
        3. DRY: hsa_search(function/component name) — check existing code
        4. SKILLS: hsa_search(action:'skills') — load patterns
        5. INTENT: verify intent declared — if not, declare now
      On gate fail: ask user for context before coding.

  - id: GOV-006
    name: "Pre-Stop Checklist"
    severity: warning
    when: "Before claiming done or ending session"
    action: |
      Verify (mode-aware):
        1. BUILD passes (code-change workflows only)
        2. TESTS pass (code-change workflows only)
        3. HIERARCHY updated (track status:completed)
        4. SESSION persisted: hsa_session({action:'persist', task_summary:'...', auto_notify:true})
        5. If HSA unavailable: update memory/session.md + CONTEXT_SNAPSHOT.md
      Skip 1-2 for: /think, /plan, /recap, /help, /suggest, /search, /onboard, /doc.

  - id: GOV-007
    name: "Session Handoff"
    severity: info
    when: "Ending session or resuming after compaction"
    action: |
      End format: [SESSION-END] Topic: {what}. Done: {list}. Pending: {list}. Files: {key}. Build: pass/fail.
      Resume: hsa_session(include_anchors:true) -> review bridge -> declare intent.

  - id: GOV-008
    name: "Memory vs Anchor Selection"
    severity: info
    when: "Choosing persistence mechanism"
    action: |
      hsa_session(anchor): session-scoped, survives compaction, lost on session end.
      hsa_memory(store): cross-session via SQLite, searchable by recall.
      hsa_session(fact): extracted facts with temporal validity.
      Rule: future sessions need it? -> memory/fact. Only this session? -> anchor.

integration:
  tier: 2
  related_modules: ["drift-prevention", "stop-conditions", "read-before-write"]
