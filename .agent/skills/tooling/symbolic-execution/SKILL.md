---
name: symbolic-execution
description: "Symbolic execution and constraint solving with angr, Z3, Unicorn for automated analysis."
detect: ["angr", "Z3", "symbolic execution", "constraint solver", "Unicorn", "Qiling", "concolic", "SMT solver"]
category: tooling
tier: 1
---

# Symbolic Execution Tools

> Automated binary analysis using symbolic execution engines and constraint solvers.

## Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `angr-patterns.yaml` | angr analysis patterns | 8 |
| `z3-patterns.yaml` | Z3 constraint patterns | 8 |
| `unicorn-patterns.yaml` | Unicorn emulation patterns | 6 |

## Tool Selection

| Tool | Strength | Use Case |
| ---- | -------- | -------- |
| angr | Full binary analysis | CFG, path exploration, automated solve |
| Z3 | Constraint solving | SMT formulas, proof generation |
| Unicorn | CPU emulation | Shellcode analysis, instruction trace |
| Qiling | OS emulation | Syscall emulation, sandbox analysis |

## Checklist

- [ ] Binary loaded and analyzed
- [ ] Entry point and target identified
- [ ] Constraints formulated
- [ ] Solution verified against target
- [ ] Results documented
