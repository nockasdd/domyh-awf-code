---
name: reverse-engineering
description: "Reverse engineering workflows for IDA, Ghidra, x64dbg, pattern scans, struct reconstruction, and protocol analysis. Use when inspecting binaries, scripts, or dumped game clients."
detect: ["*.idb", "*.i64", "*.gzf", "*.sig", "*.py", "*.dll", "*.exe"]
category: cross-cutting
tier: 1
---

# Reverse Engineering

> RE tools, IDA/Ghidra scripting, pattern scanning, struct reconstruction, protocol analysis

## 📦 Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `ida-patterns.yaml` | IDAPython scripts, FLIRT sigs, xref, auto-analysis | ~18 |
| `ghidra-patterns.yaml` | Ghidra Java/Python scripting, Pcode, data types | ~15 |
| `signature-generation.yaml` | AOB gen, wildcard strategy, version-safe patterns | ~12 |

## 🎯 Core Problem

```
❌ Without: Agent generates naive hex patterns, misses wildcards, wrong IDA API
✅ With: Agent uses proper IDAPython API, version-safe AOB, efficient xref analysis
```

## 📋 Quick Reference

| Topic | Pattern |
| ----- | ------- |
| IDA function xrefs | `idautils.CodeRefsTo(ea, 0)` |
| IDA rename | `idc.set_name(ea, name, SN_NOWARN)` |
| Ghidra decompile | `DecompInterface().decompileFunction(func, 60, monitor)` |
| AOB gen | Use `?` wildcards on relocation-dependent bytes |
| Version-safe sig | Wildcard call targets, keep opcode prefixes |
| Struct recon | ReClass.NET attach → browse → define → export header |
| VTable analysis | `object+0x00 → vptr → func[0]=dtor, func[N]=methods` |
| Protocol RE | Wireshark capture → find patterns → build parser |

## ⚠️ Anti-Patterns

| ❌ Don't | ✅ Do |
| -------- | ----- |
| Hardcode absolute addresses | Use pattern scan with wildcards |
| Full byte pattern (no wildcards) | Wildcard relocation/offset bytes |
| Parse all packets manually | Build dispatcher with opcode map |
| Assume class layout across versions | Use pattern scan to find offsets |

## 📋 Checklist

- [ ] Patterns use wildcards for version safety?
- [ ] IDA scripts use `idaapi`/`idautils` (not deprecated `idc`)?
- [ ] Ghidra scripts handle API version differences?
- [ ] Struct sizes verified against runtime memory?
- [ ] Signatures tested across game versions?

---
