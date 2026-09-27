# Token Efficiency Rule v1.0.0
# Minimize token waste in generated content, skill loading, and rule injection
---
name: token-efficiency
rule_id: "MOD-TOK-001"

description: "Reduce token waste via conditional loading, content limits, and elimination of decorative elements."
category: "performance"

context:
  always_apply: true
  personas: ["*"]

rules:
  - id: TOK-001
    name: "No Decorative Elements in Generated Content"
    severity: warning
    description: |
      Box-drawing characters and decorative separators waste tokens with zero semantic value.
      Banned in code output and internal documents:
        chars: ["===", "---" (as separator), "***", "~~~", "|||"]
        unicode: box-drawing block (U+2500-U+257F)
      Allowed only in: user-facing reports explicitly requested (audit, status dashboard).

  - id: TOK-002
    name: "Workflow Files Max 80 Effective Lines"
    severity: info
    description: |
      Workflow .md files should contain max 80 lines of effective content
      (excluding blank lines and markdown headers).
      Beyond 80 lines, LLM attention degrades due to middle-of-context effect.
      Split overflow into: data/*.yaml for patterns, ADVANCED.md for deep detail.

  - id: TOK-003
    name: "Skill Progressive Loading"
    severity: warning
    description: |
      Skills MUST support 3-tier progressive disclosure:
        Tier 0: META only (frontmatter: name, detect, category) — 30 tokens
        Tier 1: SKILL.md core (max 60 lines) — 150 tokens
        Tier 2: data/*.yaml patterns — 300 tokens (load on-demand)
        Tier 3: ADVANCED.md — 500 tokens (only for complex tasks)
      Default load: Tier 1. Escalate only when task complexity requires it.

  - id: TOK-004
    name: "Conditional Rule Loading"
    severity: warning
    description: |
      Not all rules apply to all contexts. Load conditionally:
        always_load:
          - quality, yagni, stop-conditions, behavioral-patterns
          - session-governance, drift-prevention, response-precision
          - naming-discipline, output-hygiene, token-efficiency
        platform_specific (load only on matching OS):
          - terminal-antigravity (Windows only)
          - terminal-safety (Windows-heavy content)
        language_specific (load only when stack matches):
          - cpp-single-binary-build (C++ projects)
          - game-dev-security (game projects)
          - game-creation-safety (Unity/UE projects)
        workflow_specific (load only when workflow active):
          - git-workflow (git operations)
          - online-research (external search needed)
          - memory-checkpoints (multi-step tasks)

  - id: TOK-005
    name: "Deduplicate Shared Rules"
    severity: info
    description: |
      When multiple workflows share identical rules, extract to a shared reference:
        Bad: Repeating "Run tests after every change" in /code, /fix, /refactor, /tdd
        Good: Reference "See edit-verification module" with one-line reminder
      Saves ~50-150 tokens per workflow that would otherwise repeat content.

  - id: TOK-006
    name: "Compact MCP Tool Results"
    severity: info
    description: |
      MCP tool results should be structured JSON, not prose.
      Prefer: { files: ["a.ts", "b.ts"], count: 2, status: "ok" }
      Avoid: "I found 2 files: a.ts and b.ts. The operation completed successfully."
      Structured data is 40-60% more token-efficient than equivalent prose.

  - id: TOK-007
    name: "Early Termination"
    severity: info
    description: |
      Stop searching/loading after finding the answer.
      Bad: Load 5 skills when first skill already has the pattern needed.
      Bad: Read 10 files when the bug is found in file 2.
      Good: Return immediately when sufficient context is gathered.
      Metric: If search returns confidence > 0.8, stop expanding.

integration:
  tier: 2
  related_modules: ["performance-optimization", "response-precision", "proportional-response"]
