# Git Workflow Rule
---
name: git-workflow
rule_id: "MOD-GIT-001"

description: "Git operations: commit conventions, branching, and safety checks."
category: "workflow"

context:
  always_apply: false
  personas: ["developer", "devops"]
  trigger: "When performing git operations"

# --- COMMIT CONVENTIONS ---

commits:
  format: "type(scope): description"
  types: ["feat", "fix", "refactor", "docs", "test", "chore", "perf", "ci"]
  rules:
    - "Atomic commits — one logical change per commit"
    - "Description in imperative mood: 'Add feature' not 'Added feature'"
    - "Max 72 chars for first line"
    - "Reference issue/ticket in body when applicable"
    - "Incremental commits — DO NOT batch >5 file changes into one commit. Each logical change (1 bug fix, 1 feature) = 1 commit. Refactor separate from feature work."

# --- BRANCHING ---

branching:
  convention: "type/description (e.g., feat/user-auth, fix/login-redirect)"
  protected: ["main", "master", "production", "staging"]
  rule: "Request approval before force-pushing to protected branches"

# --- SAFETY CHECKS ---

safety:
  before_commit:
    - "Review staged changes with git diff --staged"
    - "Ensure no secrets/credentials in diff"
    - "Run lint/build/tests if available"
  before_push:
    - "Pull/rebase to resolve conflicts locally"
    - "Verify correct remote and branch"
  before_merge:
    - "Ensure CI passes"
    - "Squash fixup commits if applicable"

# --- DANGEROUS OPERATIONS ---

dangerous:
  require_confirmation:
    - "git push --force (history rewrite)"
    - "git reset --hard (discard changes)"
    - "git clean -fd (delete untracked files)"
    - "Merging into protected branches"

integration:
  tier: 2
  related_modules: ["terminal-safety"]
