---
name: frida
description: "Dynamic instrumentation with Frida — function hooking, runtime analysis, security testing."
detect: ["frida", "frida hook", "dynamic instrumentation", "frida script", "frida attach", "function trace"]
category: tooling
tier: 1
---

# Frida Dynamic Instrumentation

> Runtime analysis and function hooking using Frida for security testing and debugging.

## Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `frida-templates.yaml` | Hook script templates | 10 |
| `hook-patterns.yaml` | Common hook patterns | 12 |

## Modes

| Mode | Usage | When |
| ---- | ----- | ---- |
| Attach | `frida -p PID` | Running process |
| Spawn | `frida -f app` | Launch and hook |
| USB | `frida -U` | Mobile device |

## Checklist

- [ ] Target process identified
- [ ] Frida server running on target (if mobile)
- [ ] Hook script prepared
- [ ] Output logging configured
- [ ] Results documented
