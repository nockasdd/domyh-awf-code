# Core Archive

> Legacy operational specifications (v5.x → v6.x migration)

> [!WARNING]
> These are **DESIGN SPECIFICATIONS**, not runtime configs.
> They are used by HSA for semantic matching only.
> The actual runtime behaviors are defined in `AGENT_BEHAVIOR.md`.

These YAML files contain **legacy reference specs** for components that have been superseded by runtime implementations in the HSA Engine (v1.0+) and the LLM-as-Runtime architecture.

## Purpose

- **Historical reference** — Document design decisions from earlier architecture
- **Migration guide** — Help understand pre-v6 behavior patterns
- **Not actively loaded** — These files are NOT parsed by the runtime engine

## Contents (24 files)

| File | Original Purpose |
|---|---|
| ROUTER.yaml | Pre-HSA routing logic |
| SCORING_FORMULA.yaml | Pre-HSA skill scoring |
| MEMORY_ENGINE.yaml | Legacy memory management |
| CONTEXT_*.yaml | Pre-HSA context loading/optimization |
| SKILLS_FLOW.yaml | Legacy skill activation flow |
| STATE_MACHINE.yaml | Pre-LLM state management |
| *_ENGINE.yaml | Various engine specifications |

## Active Cross-References

Some active configs reference these files for documentation context (README, MEMORY_PATHS).
These references are for **developer documentation only** and do not affect runtime behavior.

---

_DOMYH Awesome Code • Archive Documentation • v6.3.1_
