# Memory Checkpoints Rule v7.2.0
# Enforce periodic memory persistence on meaningful events
# Source: Deep Think Analysis — Q7 (agent forgetting context)
---
name: memory-checkpoints
rule_id: "MOD-MEM-001"

description: "Enforce periodic memory persistence on meaningful events to prevent context loss."
category: "governance"

context:
  always_apply: true
  personas: ["*"]

rules:
  - id: MEM-001
    name: "Checkpoint on Workflow Step"
    severity: info
    when: "After completing a workflow step (DETECT/PLAN/EXECUTE/VERIFY/SYNC)"
    action: |
      hsa_session({
        action: 'persist',
        task_summary: '[workflow]:[step] completed: [1-line result]'
      })
      Keeps session recoverable if context compacts or crashes.

  - id: MEM-002
    name: "Anchor on Key Changes"
    severity: info
    when: "After modifying >3 files or making significant code changes"
    action: |
      hsa_session({
        action: 'anchor',
        content: '[CHANGE] Files: {list}. What: {summary}',
        category: 'context'
      })

  - id: MEM-003
    name: "Anchor on Decision"
    severity: info
    when: "After choosing approach A over B, selecting library, or defining API"
    action: |
      hsa_session({
        action: 'anchor',
        content: '[DECISION] {choice}. Reason: {rationale}',
        category: 'decision'
      })

integration:
  tier: 3
  related_modules: ["session-governance", "context-integrity"]
