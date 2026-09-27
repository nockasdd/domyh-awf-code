# Naming Discipline Rule v1.0.0
# Enforce concise, consistent naming across files, functions, and comments
---
name: naming-discipline
rule_id: "MOD-NAM-001"

description: "Enforce short, meaningful names. No numeric prefixes, no phase/version markers, no redundant context."
category: "quality"

context:
  always_apply: true
  personas: ["developer", "architect"]

rules:
  - id: NAM-001
    name: "Short File Names"
    severity: warning
    description: |
      File names MUST be under 25 characters (excluding extension).
      Use kebab-case. No version or phase suffixes.
      Bad: user-authentication-service-v2.ts, phase3-migration-handler.ts
      Good: auth-svc.ts, migrate.ts, user-repo.ts

  - id: NAM-002
    name: "No Numeric Prefixes"
    severity: warning
    description: |
      Do not use numeric prefixes for ordering files.
      Import/load order is handled by bundlers and module systems.
      Bad: t01_guide.ts, 01-setup.md, step1-plan.md
      Good: guide.ts, setup.md, plan.md

  - id: NAM-003
    name: "Function Names Max 30 Chars"
    severity: info
    description: |
      Functions: verb + noun, max 30 characters.
      Bad: handleUserAuthenticationAndSessionCreation()
      Good: createAuthSession()
      Bad: processIncomingWebSocketMessageFromClient()
      Good: handleWsMessage()

  - id: NAM-004
    name: "No Redundant Context"
    severity: info
    description: |
      Class/module name already provides context. Do not repeat it.
      Bad: UserService.getUserById(), authMiddleware.authenticateUser()
      Good: UserService.getById(), authMiddleware.verify()
      Bad: DatabaseConnection.connectToDatabase()
      Good: DatabaseConnection.connect()

  - id: NAM-005
    name: "No Phase/Version in Identifiers"
    severity: warning
    description: |
      Never include phase, version, or temporal markers in code identifiers.
      These belong in git history, changelogs, or package.json.
      Bad: migrateV2(), handlePhase3Logic(), newAuthFlow()
      Good: migrate(), handleAuth(), createSession()
      Bad: UserModelV3, OldPaymentService, LegacyRouter
      Good: UserModel, PaymentService, Router (delete old, don't rename)

  - id: NAM-006
    name: "Abbreviation Allowlist"
    severity: info
    description: |
      Common abbreviations are acceptable when unambiguous:
      svc (service), repo (repository), cfg/conf (config), ctx (context),
      req/res (request/response), msg (message), btn (button), nav (navigation),
      auth (authentication), db (database), ws (websocket), fn (function),
      util (utility), err (error), cb (callback), opts (options)

integration:
  tier: 2
  related_modules: ["quality", "proportional-response", "token-efficiency"]
