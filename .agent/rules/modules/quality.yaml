# Quality Rule v7.1.0
---
name: quality
rule_id: "MOD-QUA-001"

description: "Code quality standards: SOLID, naming, structure, error handling, documentation, quality gates."
category: "quality"

context:
  always_apply: true
  personas: ["developer", "tester", "architect"]

# --- SOLID PRINCIPLES (ref: coding-rules/data/solid-principles.yaml) ---

solid:
  source: "skills/cross-cutting/coding-rules/data/solid-principles.yaml"
  enforcement:
    S_single_responsibility:
      - "Each file/module has one purpose"
      - "Functions do one thing — max 50 lines"
      - "Classes max 300 lines"
      - "Violation: God class with 10+ methods"
    O_open_closed:
      - "Extend via interfaces/traits, not modification"
      - "Violation: Switch statements on types"
    L_liskov_substitution:
      - "Subtypes honor base contracts"
      - "Violation: Square extends Rectangle problem"
    I_interface_segregation:
      - "Small, focused interfaces (not 20+ method APIs)"
      - "Violation: Fat interface with unused methods"
    D_dependency_inversion:
      - "High-level depends on abstractions, not concretions"
      - "Violation: Direct new() in high-level code"

# --- DESIGN PRINCIPLES ---

principles:
  DRY:
    - "No duplicated logic — extract shared code into utils/helpers"
    - "Search existing code before creating new (EXEC_004)"
  KISS:
    - "Simple over clever — prefer readability"
    - "Architecture complexity ≤ project needs"
  YAGNI:
    - "No premature features — build only what's needed now"
    - "Scope gate: P0-P6 phases define boundaries"
  twelve_factor:
    - "Config via environment variables (.env)"
    - "Explicit dependencies (lock files)"
    - "Backing services as attached resources"
    - "Dev/prod parity via Docker"

# --- CODE QUALITY STANDARDS ---

standards:
  naming:
    - "Use descriptive, intent-revealing names (avoid abbreviations)"
    - "Follow language conventions: camelCase (JS/TS), snake_case (Python/Go), PascalCase (C#)"
    - "Boolean variables start with is/has/should/can"
    - "Functions describe actions: getUserById, calculateTotal"

  structure:
    - "Single Responsibility: each function/class does one thing"
    - "Keep functions under 50 lines, classes under 300 lines"
    - "Max 3 levels of nesting — refactor deeper logic into helpers"
    - "Prefer early returns over deep if/else chains"
    - "Separation of concerns scales with task size (see proportional-response module):"
    - "  MICRO/SMALL (≤50 LOC): inline logic OK, no forced file separation"
    - "  MEDIUM (50-200 LOC): separate into logical files"
    - "  LARGE (200+ LOC): full service/controller/model pattern appropriate"

  error_handling:
    - "Handle errors explicitly — never silently swallow exceptions"
    - "Use typed errors when language supports it"
    - "Include context in error messages: what failed, why, what to do"
    - "Log errors with structured data (not just message strings)"

  documentation:
    - "Document WHY, not WHAT (code shows what, comments explain why)"
    - "Public APIs require JSDoc/GoDoc/docstring with params and return types"
    - "Update docs when changing behavior — stale docs are worse than no docs"

# --- ANTI-PATTERNS ---

anti_patterns:
  - "Magic numbers — use named constants"
  - "God classes/functions — break into focused units"
  - "Copy-paste code — extract shared logic"
  - "Commented-out code — delete it, git remembers"
  - "TODO without issue reference — add ticket number"
  - "Circular dependencies — use DI or events"
  - "Premature optimization — profile before optimizing"

# --- CODE REVIEW CRITERIA ---

review_criteria:
  - "Does it solve the stated problem?"
  - "Are edge cases handled?"
  - "Is error handling complete?"
  - "Are there security implications?"
  - "Is it testable?"
  - "Does it follow SOLID principles?"
  - "Is the architecture pattern respected?"

# --- QUALITY GATE (for /init and /code) ---

quality_gate:
  description: "Minimum quality checks before marking a phase complete"
  checks:
    - "Build succeeds with zero errors"
    - "Linter passes with zero warnings"
    - "No god classes (> 300 lines)"
    - "No functions > 50 lines"
    - "Test coverage ≥ 80% (unit), ≥ 60% (integration)"
    - "No circular dependencies"
    - "All public APIs documented"

integration:
  tier: 2
  related_modules: ["edit-verification", "yagni"]
  related_skills: ["coding-rules"]
