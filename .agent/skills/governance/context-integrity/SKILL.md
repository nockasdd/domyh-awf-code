---
name: "context-integrity"
description: "Detects and repairs context drift. Monitors hierarchy staleness, chain breaks, and context decay. Recovery playbooks for 4 common scenarios."
triggers:
  - "When drift score is low (hsa_check_drift warns)"
  - "After context compaction or session gap"
  - "When hierarchy feels wrong"
  - "When resuming work after hours/days"
  - "Every 5+ turns without hierarchy update"
---

# Context Integrity

**Core principle:** Detect loss. Repair state. Never work on stale context.

## Detect — Know When Context Is Broken

### Automatic Detection (via HSA)

```
hsa_check_drift(current_action: "What I'm about to do")
```

Output contains:
- **Drift analysis** — does current action match declared intent?
- **Progress report** — hierarchy completion status
- **Saved anchors** — compaction-proof decisions

### Context Staleness Index

| Turns Since Last Update | Staleness | Action |
|------------------------|-----------|--------|
| 0-3 turns | 🟢 Fresh | Continue working |
| 4-7 turns | 🟡 Aging | Consider drift check |
| 8-12 turns | 🟠 Stale | Run drift check NOW |
| 13+ turns | 🔴 Critical | STOP. Check drift + update hierarchy |

### When to Check (Mandatory)

| Situation | Action | Priority |
|-----------|--------|----------|
| 5+ turns without updating hierarchy | `hsa_check_drift` | 🟠 High |
| Resuming after a gap (hours/days) | `hsa_check_drift(include_anchors: true)` | 🔴 Critical |
| "What was I doing?" moment | `hsa_check_drift` + read anchors | 🔴 Critical |
| After subagent delegation | `hsa_check_drift` to verify alignment | 🟡 Medium |
| Before concluding any task | `hsa_check_drift` | 🟡 Medium |
| Topic or scope changed | `hsa_check_drift` + possibly re-declare | 🟠 High |

## Repair — Fix Broken Context

### Recovery Playbook: 4 Scenarios

#### Scenario 1: After Drift Warning

```
# 1. Check current alignment
hsa_check_drift(current_action: "Checking alignment after drift warning")

# 2. Read the drift report — understand what drifted

# 3. Re-align hierarchy
hsa_track_progress(
  level: "action",
  label: "Re-aligned: {what I'm actually doing now}"
)

# 4. If scope changed significantly → re-declare
hsa_declare_intent(
  focus: "Updated scope: {new focus}",
  mode: "plan_driven",
  goals: ["Updated goal 1", "Updated goal 2"]
)
```

#### Scenario 2: After Context Compaction

Signs: earlier conversation details seem fuzzy, code references lost.

```
# 1. Retrieve saved state
hsa_check_drift(
  current_action: "Recovering from context compaction",
  include_anchors: true
)

# 2. Read ALL anchors — especially:
#    - [SESSION] anchors → what was done
#    - [DECISION] anchors → what was decided
#    - [CONVENTION] anchors → what patterns to follow
#    - [CONSTRAINT] anchors → what limits exist

# 3. Re-read key files mentioned in anchors
# Use hsa_get_context to retrieve relevant code

# 4. Declare fresh intent
hsa_declare_intent(
  focus: "Continuing after compaction: {summary from anchors}",
  mode: "plan_driven",
  goals: ["Remaining goals from anchors"]
)

# 5. Save recovery note
hsa_save_anchor(
  content: "[RECOVERY] Recovered from compaction. Prior state restored from anchors.",
  category: "context"
)
```

#### Scenario 3: After Session Gap (Hours/Days)

```
# 1. Full anchor retrieval
hsa_check_drift(
  current_action: "Resuming after gap",
  include_anchors: true
)

# 2. Re-read key files (they may have changed externally)
hsa_check_changes()  # Re-index for any file changes

# 3. Verify prior work still valid
# Run build/test to check nothing broke

# 4. Declare intent for new session
hsa_declare_intent(
  focus: "Resuming: {focus from anchors}",
  mode: "plan_driven"
)
```

#### Scenario 4: After Topic Switch / Subagent Confusion

When you realize you've been working on the wrong thing:

```
# 1. Check where drift started
hsa_check_drift(current_action: "Checking: am I on the right track?")

# 2. If off-track: save current work state
hsa_save_anchor(
  content: "[DRIFT] Was working on {wrong thing}. Correct focus: {right thing}.",
  category: "context"
)

# 3. Re-declare with correct focus
hsa_declare_intent(
  focus: "Corrected: {right focus}",
  mode: "plan_driven"
)

# 4. Re-align hierarchy
hsa_track_progress(
  level: "action",
  label: "Topic correction: returning to {right thing}"
)
```

## Survive — Long-Haul Patterns

### The Anchor Pattern (Compaction-Proof)

Before any significant decision:
```
hsa_save_anchor(
  content: "[DECISION] Chose X over Y because: {reasons}. Trade-off: {what}",
  category: "decision"
)
```

### The Checkpoint Pattern (Drift-Proof)

Every 3-5 meaningful actions:
```
hsa_track_progress(
  level: "action",
  label: "Done: A, B, C. Next: D."
)
```

### The Bridge Pattern (Cross-Session)

At session boundaries:
```
hsa_save_anchor(
  content: "[SESSION] Topic: {X}. Done: {list}. Pending: {list}. Files: {key files}",
  category: "context"
)
```

### Chain-of-Thought Validation

Before continuing complex work, verify your logic chain:

1. **What is the current goal?** (Check intent)
2. **What have I done so far?** (Check hierarchy)
3. **What am I about to do?** (Check it aligns)
4. **What prior decisions affect this?** (Check anchors)

If any answer is unclear → run `hsa_check_drift` before proceeding.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I remember what I was doing" | After compaction you're guessing. Check drift. |
| "The context is fine" | If you haven't checked in 5+ turns, it's not fine. |
| "I'll recover context later" | Later = after more drift. Recover NOW. |
| "I know the codebase well enough" | Re-read files after gaps. Code changes externally. |
| "The hierarchy is up to date" | If you haven't updated in 5+ turns, it's stale. |
