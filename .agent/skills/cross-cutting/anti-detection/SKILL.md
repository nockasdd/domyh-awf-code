---
name: anti-detection
description: "Anti-detection and stealth patterns for code obfuscation, anti-debugging, false-positive reduction, and evasion review. Use when hardening runtime behavior or reviewing suspicious detection surfaces."
detect: ["*.cpp", "*.h", "*.hpp", "*.cxx", "*.cs", "*.py"]
category: cross-cutting
tier: 1
---

# Anti-Detection & Stealth

> Code obfuscation, anti-debugging, stealth, false positive avoidance, anti-cheat evasion

## 📦 Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `obfuscation-patterns.yaml` | String encrypt, control flow, polymorphic code | ~20 |
| `anti-debug-patterns.yaml` | NtQuery, timing, TLS callbacks, hardware breakpoints | ~20 |
| `stealth-evasion.yaml` | Header erasure, module unlink, handle cloak, HWID spoof | ~20 |

## 🎯 Core Problem

```
❌ Without: Bot detected in minutes — obvious patterns, no obfuscation
✅ With: Proper stealth, human-like behavior, anti-cheat evasion
```

## 📋 Quick Reference

| Topic | Pattern |
| ----- | ------- |
| String encrypt | Compile-time XOR with `constexpr` |
| Anti-debug basic | `IsDebuggerPresent()` + NtQuery |
| Anti-debug timing | RDTSC delta check |
| PE header erase | `VirtualProtect → memset(base, 0, 0x1000)` |
| Module unlink | Remove from PEB InLoadOrderModuleList |
| Handle cloaking | NtSetInformationObject OBJ_PROTECT_CLOSE |
| HWID spoof | IoControlCode intercept for disk serial |
| Direct syscall | Manual `syscall` instruction (SSN table) |
| Integrity check bypass | EPT split page or VEH redirect |

## ⚠️ Anti-Patterns

| ❌ Don't | ✅ Do |
| -------- | ----- |
| Plaintext strings in binary | Compile-time encrypted strings |
| Single anti-debug check | Layered checks (NtQuery + timing + TLS) |
| Fixed timing patterns | Randomized delays with `normal_distribution` |
| Use `CreateRemoteThread` only | Manual mapping + header erasure |
| Ignore behavioral analysis | Normalize API call patterns |
| Hardcoded HWID values | Spoof at driver level |

## 📋 Checklist

- [ ] All sensitive strings encrypted at compile-time?
- [ ] Anti-debug checks layered (3+ methods)?
- [ ] PE headers erased after DLL load?
- [ ] Module unlinked from PEB?
- [ ] Input timing randomized?
- [ ] API call patterns look normal?
- [ ] No known detection signatures in code?
- [ ] HWID spoof if needed?

---
