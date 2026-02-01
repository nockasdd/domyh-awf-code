# DOMYH Agent — Architectural Decisions Log

> Records key decisions made during development sessions.
> Auto-updated when agent makes architectural or significant technical choices.

---

## Decision Template

<!--
Each decision follows this format:

### [DATE] Decision Title
- **Context**: What situation led to this decision
- **Options Considered**: What alternatives were evaluated
- **Decision**: What was chosen
- **Rationale**: Why this choice was made
- **Consequences**: Expected outcomes or trade-offs
-->

---

## Decisions

<!-- Auto-appended below this line -->

### [Template] Example Decision

- **Context**: Need to choose database for user data
- **Options Considered**:
  1. PostgreSQL - full relational
  2. MongoDB - flexible schema
  3. SQLite - embedded, simple
- **Decision**: PostgreSQL
- **Rationale**: Strong consistency needed, complex queries expected
- **Consequences**: Requires more setup, but better long-term scalability

---

_This file is auto-managed by DOMYH Agent. Manual edits are preserved._
