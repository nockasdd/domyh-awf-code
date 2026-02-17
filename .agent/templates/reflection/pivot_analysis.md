# 🔄 Pivot Analysis Template

> Perspective shift when agent is stuck (Progressive Escalation)

---

## Purpose

When a fix attempt fails 2+ times, use this template to analyze why the current approach isn't working and systematically shift to a different strategy. This template guides through the escalation levels defined in `rules/modules/progressive-escalation.yaml`.

---

## Step 1: Stuck Assessment

### Failed Attempts Log

```yaml
attempts:
  - id: 1
    approach: "[What was tried]"
    file_line: "[file:line]"
    result: "[What happened]"
    why_failed: "[Root cause of failure]"
  - id: 2
    approach: "[What was tried]"
    file_line: "[file:line]"
    result: "[What happened]"
    why_failed: "[Root cause of failure]"
```

### Stuck Signal Check

- [ ] **S1 Repeat Fix**: Am I editing the same location the same way?
- [ ] **S2 Oscillation**: Am I adding then removing the same code?
- [ ] **S3 Same Error**: Is the error message unchanged after fixes?
- [ ] **S4 Scope Creep**: Am I touching more files without progress?
- [ ] **S5 Circular**: Am I returning to a previously failed approach?

### Bias Check

- [ ] **Confirmation Bias**: Am I only looking for evidence supporting my theory?
  - → List 3 pieces of evidence AGAINST current hypothesis
- [ ] **Anchoring**: Is my first hypothesis still my main one?
  - → Generate 2 NEW alternative hypotheses
- [ ] **Tunnel Vision**: Have I checked beyond code?
  - → Checklist: code ✓ config ✓ env ✓ deps ✓ data ✓ logs ✓

---

## Step 2: Level Selection

Based on assessment, select the appropriate level:

| If... | Then → |
|-------|--------|
| First stuck detection | Level 2: REFLECT |
| REFLECT didn't reveal new insight | Level 3: REFRAME |
| Perspective shift didn't help | Level 4: WIDEN |
| Wide search found nothing | Level 5: DECOMPOSE |
| Isolation tests inconclusive | Level 6: ESCALATE |

---

## Step 3: Execute Selected Strategy

### Level 2: REFLECT

```
1. List ALL attempts in table format
2. Find PATTERN in failures (same location? different errors? cascading?)
3. Run bias checkpoint
4. Generate corrected hypothesis
```

### Level 3: REFRAME

Choose 1-2 strategies:

| Strategy | When to use |
|----------|-------------|
| **INVERT** | When stuck on one hypothesis → flip all assumptions |
| **RUBBER DUCK** | When logic is unclear → explain step-by-step |
| **DEVIL'S ADVOCATE** | When fix seems right but doesn't work → challenge it |
| **FRESH EYES** | When too deep → forget everything, read code fresh |

### Level 4: WIDEN

Choose 1-2 strategies:

| Strategy | When to use |
|----------|-------------|
| **UPSTREAM/DOWNSTREAM** | When bug might come from callers/callees |
| **DIFF FORENSICS** | When bug appeared recently → git history |
| **ENVIRONMENTAL AUDIT** | When code looks correct → check runtime env |
| **CONTRACT VERIFICATION** | When integration points might be mismatched |

### Level 5: DECOMPOSE

| Strategy | When to use |
|----------|-------------|
| **MINIMAL REPRODUCTION** | Isolate function in test file, add complexity gradually |
| **BINARY SEARCH** | Narrow down the exact line via midpoint logging |
| **COMPONENT ISOLATION** | Disable components one by one to find the culprit |

---

## Step 4: Episodic Memory Entry

After resolution (or escalation), record the lesson:

```yaml
episodic_entry:
  id: "EP-[timestamp]"
  bug_signature: "[error hash]"
  failed_approaches:
    - approach: "[what didn't work]"
      reason: "[why]"
  successful_approach: "[what worked]"
  lesson: "[one-line takeaway for future]"
  level_reached: "[1-6]"
```

Save to `.domyh/debug/episodic_memory.yaml`

---

## Quick Reference

```
Level 1 RETRY    → Fix directly (2 attempts)
Level 2 REFLECT  → Ask "WHY is this failing?"
Level 3 REFRAME  → Ask "Am I looking at this WRONG?"
Level 4 WIDEN    → Ask "Is the bug SOMEWHERE ELSE?"
Level 5 DECOMPOSE → Ask "WHICH PART exactly is broken?"
Level 6 ESCALATE → Report everything to user
```

---

_DOMYH Awesome Code • Pivot Analysis Template • Progressive Escalation_
