# Response Precision Rule v7.2.0
# Enforce concise, structured agent responses
# Source: Deep Think Analysis — Q1 (agent verbose output)
---
name: response-precision
rule_id: "MOD-RSP-001"

description: "Enforce concise, structured agent responses with clear output tiers."
category: "quality"

context:
  always_apply: true
  personas: ["*"]

rules:
  - id: RSP-001
    name: "Output Length Tiers"
    severity: warning
    description: |
      Auto-detect appropriate output tier based on task type:
        quick_answer (≤500 tok): simple question, yes/no, fix confirm, status check
        standard (≤1500 tok): single-file implementation, explanation, fix
        detailed (≤3000 tok): multi-file change with diffs, audit finding with evidence
        comprehensive (≤5000 tok): architecture review, full audit, complex analysis
      Default to standard. Tier detection is heuristic — agent judgment applies.
      When exceeding tier: move details to artifact file, keep response concise.

  - id: RSP-002
    name: "Answer-First Structure"
    severity: warning
    description: |
      Structure EVERY response using Answer-First pattern:
        1. DIRECT ACTION/ANSWER — what was done or the answer (1-3 sentences max)
        2. EVIDENCE — code snippet, file:line reference, or command output
        3. CONTEXT — only if user likely needs follow-up info

      Anti-patterns (DO NOT):
        ❌ Preamble: "Let me explain the background first..."
        ❌ Echo: Repeating user's question back before answering
        ❌ Narration: "I'm going to do X" — just DO X, then report result
        ❌ Over-explanation: Explaining obvious code changes line-by-line

  - id: RSP-003
    name: "Artifact Offload"
    severity: info
    description: |
      When response content exceeds standard tier:
        - Move detailed analysis, large code blocks, or comprehensive lists to artifact
        - Keep inline response as executive summary (≤500 tok)
        - Reference artifact: "Chi tiết trong [artifact.md](path)"
      This applies especially to: audit reports, architecture reviews,
      multi-file diffs, and research summaries.

integration:
  tier: 2
  related_modules: ["yagni", "performance-optimization"]
