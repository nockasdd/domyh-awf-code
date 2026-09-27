# Proportional Response Rule v7.3.0
# Match code output size to task complexity
# Source: Deep Research (36+ sources), Martin Fowler "Rule of Three"
---
name: proportional-response
rule_id: "MOD-PRP-001"

description: "Match implementation size to task complexity. Prevent over-engineering."
category: "quality"

context:
  always_apply: true
  personas: ["developer", "debugger", "devops"]

rules:
  - id: PRP-001
    name: "Task Size Classification"
    severity: warning
    description: |
      Before writing code, classify task size:
        MICRO (≤10 LOC): utility helper, validation, format function
          → Add function to EXISTING file. DO NOT create new file.
        SMALL (10-50 LOC): API handler, transformer, single component
          → Add to existing module OR one new file max. No abstractions.
        MEDIUM (50-200 LOC): Feature with tests, multi-concern logic
          → 1-3 new files OK. Basic separation appropriate.
        LARGE (200+ LOC): New module, subsystem, architecture
          → Full planning, multiple files, clear boundaries.

  - id: PRP-002
    name: "Function-First Default"
    severity: warning
    description: |
      Default = add FUNCTION to existing file.
      Create new file ONLY when:
        1. No existing file has related functionality
        2. Existing file would exceed 300 lines
        3. New functionality has independent lifecycle
      Ask: "Can this be a function in an existing file?" YES → do that.

  - id: PRP-003
    name: "Abstraction Gate"
    severity: warning
    description: |
      DO NOT create for MICRO/SMALL tasks:
        ❌ service/ + controller/ + model/ for a single endpoint
        ❌ Abstract base class for one concrete implementation
        ❌ Factory/Strategy/Observer pattern for single use case
        ❌ Interface file for one implementation
      Rule of Three: abstract ONLY when pattern used 3+ times.

  - id: PRP-004
    name: "Change Summary Requirement"
    severity: warning
    description: |
      After EVERY non-trivial code modification, provide a brief summary:
        WHAT was changed (file:function)
        WHY it was changed (root cause, not just "fix bug")
        IMPACT on callers/tests
      This reduces Comprehension Debt — the gap between code volume and human understanding.

integration:
  tier: 2
  related_modules: ["yagni", "quality", "response-precision"]
