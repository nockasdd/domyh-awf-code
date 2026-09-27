# Output Hygiene Rule v1.0.0
# Clean, consistent output: no emoji in code, no version markers, standard comment format
---
name: output-hygiene
rule_id: "MOD-HYG-001"

description: "Enforce clean output: no emoji in code, no phase/version markers, consistent comment format."
category: "quality"

context:
  always_apply: true
  personas: ["developer", "debugger", "devops", "tester"]

rules:
  - id: HYG-001
    name: "No Emoji in Code Output"
    severity: warning
    description: |
      Generated code, comments, and variable names MUST NOT contain emoji.
      Emoji cost 3-4 bytes each and provide zero semantic value to LLM parsing.
      Bad: // Fix the auth bug
      Good: // Fix: OAuth token refresh race condition
      Exception: User-facing UI strings only when user explicitly requests emoji.

  - id: HYG-002
    name: "No Version or Phase Markers in Code"
    severity: warning
    description: |
      Code comments and identifiers must not reference versions, phases, or temporal context.
      This information belongs in git history, CHANGELOG, or package.json.
      Banned patterns in code:
        - "Phase [0-9]"
        - "v[0-9]+\.[0-9]+"
        - "Step [0-9]+/[0-9]+"
        - "Added in", "Since version", "New in"
        - "TODO(v2)", "FIXME(phase3)"
      Allowed locations: CHANGELOG.md, package.json version field, git tags, PR descriptions.

  - id: HYG-003
    name: "Comment Format Standard"
    severity: info
    description: |
      Comments follow a single format: one line, WHY not WHAT.
      Format: // [context]: [non-obvious reason]
      Good examples:
        // OAuth2 spec 4.1: token refresh needs 5s buffer for clock skew
        // Workaround: Chrome 120 drops WebSocket on tab sleep
        // Constraint: DB connection pool max 10 per AWS RDS tier
      Bad examples:
        // Loop through users and check permissions (describes WHAT)
        // Added 2024-03-15 by @dev for Phase 2 (temporal, who-did-it)
        // TODO: fix this later (vague, no context)
        // This function handles authentication (redundant with fn name)

  - id: HYG-004
    name: "No Multi-line Comment Blocks"
    severity: info
    description: |
      Prefer single-line comments. Multi-line JSDoc/docstrings only for public API signatures.
      Bad:
        /**
         * This function processes the user authentication
         * by validating the JWT token against the secret
         * and checking if the user has the required role.
         */
      Good:
        // Validate JWT + check role permission
      Exception: Public library APIs need param/return docs for consumers.

  - id: HYG-005
    name: "No Trailing Summaries"
    severity: info
    description: |
      Do not add summary comments at end of functions or files.
      Bad: // End of authentication module
      Bad: // --- Done processing users ---
      Good: (nothing - the closing brace is sufficient)

  - id: HYG-006
    name: "Consistent Log Messages"
    severity: info
    description: |
      Log messages follow: [level] action:subject detail
      Good: logger.info("created:session", { userId, ttl })
      Good: logger.error("failed:token-refresh", { reason, retryIn })
      Bad: logger.info("Session was successfully created for the user!")
      Bad: logger.error("Something went wrong!!!")
      Rules: no emoji, no exclamation marks, structured data over prose.

integration:
  tier: 2
  related_modules: ["naming-discipline", "token-efficiency", "quality", "response-precision"]
