---
description: "🧹 Code cleanup: remove dead code, organize imports, remove unused dependencies"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "Dead code removed, imports organized, build passes"
---

# 🧹 /clean — Code Cleanup Pro

> Intelligent code hygiene with safety gates
> 📚 Auto-detect stack • Preview before changes • Safe rollback

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | Preview ALL changes before deletion — never delete without showing | Safety |
| R2 | ⛔ STOP after PREVIEW — wait for user confirmation | Safety |
| R3 | Run build + tests after every change batch | Quality |
| R4 | Protected patterns: deprecated comments, TODO markers, test files, configs, migrations | Safety |
| R5 | Offer backup (`git stash`) before destructive operations | Safety |

---

## CLEANUP FLOW (6 Phases)

1. **DETECT** — `hsa_session`, `hsa_detect`, load cleanup tools from `data/clean-tools.yaml`. Show: `[1/6] Detected: {stack}, tools: {list}`
2. **SCAN** — Run analysis tools per detected stack. Collect dead code, unused deps, unorganized imports. Show: `[2/6] Found: {n} dead exports, {m} unused deps`
3. **PREVIEW** — Present concise table of proposed removals.
   → ⛔ **STOP: "Select: [y] Apply all, [1,2,6] Selective, [--backup] Backup first, [n] Cancel"**
4. **EXECUTE** — Create backup (if requested), remove dead code, remove unused deps, organize imports, format code.
   > Stack-specific commands loaded from `data/clean-tools.yaml`
5. **VERIFY** — Run build → tests → lint. Show summary of freed resources.
   > If any fail → offer rollback (`git stash pop`)
6. **SYNC** — `hsa_check_changes` to update index. Show next steps.

---

## COMMANDS

| Command | Action | Risk |
|:--------|:-------|:-----|
| `/clean` | Full analysis (preview only) | 🟢 Safe |
| `/clean dead` | Remove dead code | 🟡 Medium |
| `/clean imports` | Organize imports | 🟢 Safe |
| `/clean deps` | Remove unused dependencies | 🟡 Medium |
| `/clean cache` | Clear build/test cache | 🟢 Safe |
| `/clean all` | Apply all fixes | 🟠 High |
| `/clean --dry` | Preview without changes | 🟢 Safe |
| `/clean memory` | Preview agent memory files | 🟢 Safe |
| `/clean memory reset` | Reset memory (keep audit) | 🟠 High |
| `/clean memory --hard` | Delete all memory | 🔴 Danger |

---

## DEAD CODE DETECTION

> Tools + detection patterns loaded from `data/clean-tools.yaml` per stack.

| Detection Type | Description |
|:---------------|:------------|
| Unused exports | Exported but never imported |
| Unused functions | Defined but never called |
| Unused variables | Declared but never used |
| Unused imports | Imported but never referenced |
| Unreachable code | After return/throw/break |

**Safe mode:** Preview → backup → incremental → build-verify after each removal.

---

## DEPENDENCY PRUNING

| Analysis | Description | Tools (auto-detected) |
|:---------|:------------|:----------------------|
| Unused | Not imported anywhere | depcheck, knip, go mod tidy |
| Duplicate | Multiple versions | npm/yarn dedupe |
| Vulnerable | Security issues | npm audit, snyk, govulncheck |
| Bloat | Large unused transitive | bundle-analyzer |

**Actions:** Remove unused → deduplicate → upgrade vulnerable → replace deprecated.
**Validation:** Build after → Test after → Size comparison.

---

## MEMORY CLEANUP

> Only runs when explicitly requested with `memory` keyword.

| Command | Action | Scope |
|:--------|:-------|:------|
| `/clean memory` | Preview file sizes | Read-only |
| `/clean memory reset` | Reset session + state (keep audit) | Session |
| `/clean memory audit` | Reset audit logs only | Audit |
| `/clean memory --hard` | Delete everything ⚠️ | All |

**Safety:** Require confirmation → show preview first → backup before delete.

> Reset templates loaded from `data/memory-reset-templates.yaml`.

---

## REFERENCE DATA (Lazy-Load)

| Need | Data File | Content |
|:-----|:----------|:--------|
| Stack tools | `data/clean-tools.yaml` | Per-language: markers, dead_code, imports, deps, format, lint |
| Reset templates | `data/memory-reset-templates.yaml` | Session/state/audit reset YAML templates |

---

## CASCADE EVALUATION (Recommended — MCP)

⚠️ **Evaluate before EXECUTE** — see `delegation-intelligence` skill for scoring.

```
hsa_delegate({action:'cascade', cascade_text:'[prompt]', task_type:'code'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
```
**Auto-cascade** (≥6.5): Multi-language project cleanup, monorepo-wide dead code scan
**Suggest cascade** (4.0-6.5): Large dependency tree analysis, complex import reorganization

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`
