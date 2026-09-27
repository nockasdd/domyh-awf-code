# Progressive Escalation Rule
# Perspective Pivot Engine — Detect stuck agents, auto-pivot strategy
---
name: progressive-escalation
rule_id: "MOD-ESC-001"

description: |
  When an agent fails to fix a bug after repeated attempts,
  detect stuck state and escalate through 7 levels of debugging strategies.
  Based on: Reflexion, Tree-of-Thought, DoVer, Devil's Advocate.

category: "workflow"

context:
  always_apply: false
  personas: ["Developer", "Debugger"]
  workflows: ["/debug", "/fix"]

# ═══ STUCK DETECTION ═══

stuck_detection:
  signals:
    S1_repeat_fix:  { detection: "Diff similarity > 70% between fixes", weight: 0.9 }
    S2_oscillation: { detection: "Revert pattern A→B→A within 3 edits", weight: 1.0 }
    S3_same_error:  { detection: "Error similarity > 85% after 2+ attempts", weight: 0.8 }
    S4_scope_creep: { detection: "More files changed but error unchanged", weight: 0.7 }
    S5_circular:    { detection: "Current strategy matches prior failure", weight: 0.85 }

  bias_detectors:
    B1_confirmation: { detection: "Searching only 1 file", counter: "Force ≥3 files, list counter-evidence" }
    B2_anchoring:    { detection: "Same hypothesis after 2+ fails", counter: "Force ≥3 hypotheses ranked" }
    B3_tunnel_vision: { detection: "Only code modified, no config check", counter: "code ✓ config ✓ env ✓ deps ✓ data ✓ logs ✓" }

  thresholds:
    level_2_reflect: 0.6
    level_3_reframe: 0.75
    level_3_5_delegate: 0.80
    level_4_widen: 0.85
    level_5_decompose: 0.90
    level_6_escalate: 0.95

# ═══ 7 ESCALATION LEVELS ═══

levels:
  level_1_retry:
    name: "RETRY"
    max_attempts: 2
    trigger: "Initial fix attempt"
    action: "Apply targeted fix, verify, retry if fail"

  level_2_reflect:
    name: "REFLECT"
    trigger: "After 2 failed retries OR stuck_score ≥ 0.6"
    prompt_file: "templates/reflection/escalation-L2.md"

  level_3_reframe:
    name: "REFRAME"
    trigger: "Level 2 failed OR stuck_score ≥ 0.75"
    prompt_file: "templates/reflection/escalation-L3.md"

  level_3_5_delegate:
    name: "DELEGATE"
    trigger: "Level 3 failed OR stuck_score ≥ 0.80"
    condition: "Only when the platform provides a subagent tool"
    action: |
      Hand the debug context to a fresh subagent so the stuck model is not the
      one that has to solve it:
      1. Package context: error output, every approach already rejected (L1-L3), relevant files
      2. Dispatch via the platform's native subagent tool with that context as the prompt
      3. If the subagent returns an actionable fix → apply and verify
      4. If it returns nothing actionable → continue to Level 4 (WIDEN)
    rationale: "A fresh context breaks the anchoring that produced the stuck state"

  level_4_widen:
    name: "WIDEN"
    trigger: "Level 3.5 failed OR stuck_score ≥ 0.85"
    prompt_file: "templates/reflection/escalation-L4.md"

  level_5_decompose:
    name: "DECOMPOSE"
    trigger: "Level 4 failed OR stuck_score ≥ 0.90"
    prompt_file: "templates/reflection/escalation-L5.md"

  level_6_escalate:
    name: "ESCALATE"
    trigger: "Level 5 failed OR stuck_score ≥ 0.95"
    prompt_file: "templates/reflection/escalation-L6.md"

# ═══ FAILURE MEMORY ═══

episodic_memory:
  storage: ".domyh/debug/episodic_memory.yaml"
  lookup: "Before EACH fix: hash error → search memory → exclude failed approaches."

integration:
  tier: 2
  related_modules: ["stop-conditions", "complexity-scoring"]
  workflows: ["/debug", "/fix"]
