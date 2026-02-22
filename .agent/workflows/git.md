---
description: "🔀 Git operations: commit, branch, stash, log, diff, merge, rebase"
skills: { required: [], contextual: [auto] }
success_criteria: "git operation completed, repo state verified, index synced"
---

# 🔀 /git — Git Pro

> Intelligent Git Operations Hub
> 📚 Conventional Commits • Branch Strategy • Safe Merge

---

## GIT FLOW

1. **PARSE** — `hsa_declare_intent("git: {operation}")`, identify git command intent, detect stack via HSA (`hsa_detect_stack`), check current repo state, detect branch strategy
2. **DETECT** — Current branch & status, uncommitted changes, remote sync state
3. **EXECUTE** — Run git operations, handle conflicts → ⛔ STOP on destructive actions
4. **SYNC** — `hsa_check_changes` after commit/merge/rebase/checkout to update index
5. **VERIFY** — Confirm state after operation, show summary

---

## COMMANDS

| Command                | Description                            | Risk      |
| ---------------------- | -------------------------------------- | --------- |
| `/git commit`          | Smart commit with conventional message | 🟢 Safe   |
| `/git commit --auto`   | Auto-generate commit message from diff | 🟢 Safe   |
| `/git branch [name]`   | Create branch with naming convention   | 🟢 Safe   |
| `/git stash`           | Stash current changes                  | 🟢 Safe   |
| `/git stash pop`       | Pop last stash                         | 🟡 Medium |
| `/git log`             | Pretty log (last 10)                   | 🟢 Safe   |
| `/git diff`            | Show diff summary                      | 🟢 Safe   |
| `/git merge [branch]`  | Merge with conflict resolution         | 🟡 Medium |
| `/git rebase [branch]` | Interactive rebase                     | 🟠 High   |
| `/git undo`            | Undo last commit (soft)                | 🟡 Medium |
| `/git undo --hard`     | Hard reset (destructive)               | 🔴 Danger |
| `/git status`          | Full repo status                       | 🟢 Safe   |
| `/git sync`            | Pull + push with rebase                | 🟡 Medium |

---

## 📝 CONVENTIONAL COMMITS

| Type       | Description                  |
| ---------- | ---------------------------- |
| `feat`     | New feature                  |
| `fix`      | Bug fix                      |
| `docs`     | Documentation                |
| `style`    | Formatting (no logic change) |
| `refactor` | Code restructuring           |
| `perf`     | Performance improvement      |
| `test`     | Adding/updating tests        |
| `build`    | Build system changes         |
| `ci`       | CI/CD changes                |
| `chore`    | Maintenance tasks            |
| `revert`   | Revert previous commit       |

Format: `{type}({scope}): {description}`

Breaking changes: append `!` after type/scope — `feat!: remove legacy API` or `feat(api)!: change response format`

> `BREAKING CHANGE:` footer also accepted for detailed explanation.

Examples: `feat(auth): add JWT refresh token` • `fix(api): handle null response` • `feat!: drop Node 16 support`

### Auto-Generate Commit Message

1. `git diff --staged` → analyze changes
2. Classify change type (feat/fix/refactor/...)
3. Extract scope from file paths
4. Generate concise description
5. Present for user confirmation → ⛔ Commit with this message? (y/edit/n)

---

## 🌿 BRANCH NAMING

| Type    | Convention                      | Example                        |
| ------- | ------------------------------- | ------------------------------ |
| feature | `feature/{ticket}-{short-desc}` | `feature/AUTH-123-jwt-refresh` |
| bugfix  | `fix/{ticket}-{short-desc}`     | `fix/API-456-null-response`    |
| hotfix  | `hotfix/{ticket}-{short-desc}`  | `hotfix/PROD-789-memory-leak`  |
| release | `release/{version}`             | `release/v2.1.0`               |
| docs    | `docs/{topic}`                  | `docs/api-reference`           |

---

## ⚠️ SAFETY RULES

**Destructive commands** (⛔ require explicit user confirmation):

- `git reset --hard`, `git push --force`, `git clean -fd`, `git branch -D`

**Pre-checks**:

- Check for uncommitted changes before branch switch
- Verify remote exists before push
- Confirm target branch before merge/rebase

**Conflict resolution**: Show conflicting files → Offer: manual | theirs | ours → Run tests after resolution
---

## REFLECTION CHECKPOINT

> Before saving session, verify: operation completed cleanly? No uncommitted changes? Remote in sync? Conflicts resolved?

---

## SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`
