# Orchestration Log Template v7.1.0

> Template for execution log output during /orchestrate workflow
> Created per orchestration session at: memory/orchestration/logs/

---

## Summary

| Metric         | Value                        |
| -------------- | ---------------------------- |
| **ID**         | `{orch_id}`                  |
| **Trigger**    | manual / auto (score: {N})   |
| **Status**     | completed / failed / partial |
| **Duration**   | {elapsed}                    |
| **Tasks**      | {completed}/{total}          |
| **Token Usage**| {used}/{budget}              |
| **Checkpoints**| {count}                      |

---

## Task Execution

| #  | Task         | Persona    | Workflow | Status | Duration | Tokens | Attempts |
| -- | ------------ | ---------- | -------- | ------ | -------- | ------ | -------- |
| T1 | {task_name}  | {persona}  | {cmd}    | ✅/❌  | {time}   | {n}    | {n}      |
| T2 | {task_name}  | {persona}  | {cmd}    | ✅/❌  | {time}   | {n}    | {n}      |

---

## DAG Visualization

```
{mermaid or ASCII DAG here}
```

---

## Decisions Made

1. `{timestamp}` — **{persona}**: {decision}
2. `{timestamp}` — **{persona}**: {decision}

---

## Files Changed

| File                | Changed By | Action        |
| ------------------- | ---------- | ------------- |
| `{path/to/file}`    | T{id}      | created/modified |

---

## Event Timeline

| Timestamp    | Task | Event     | Detail                    |
| ------------ | ---- | --------- | ------------------------- |
| `{ISO}`      | T1   | started   | Assigned to {persona}     |
| `{ISO}`      | T1   | completed | {summary}                 |
| `{ISO}`      | —    | checkpoint| cp-t1-{timestamp}         |

---

## Blockers (if any)

| Blocker         | Raised By | Status   | Resolution              |
| --------------- | --------- | -------- | ----------------------- |
| {description}   | {persona} | resolved | {how it was resolved}   |

---

## Recommendations

- Next suggested workflow: `{command}`
- Remaining work: {description}

---
