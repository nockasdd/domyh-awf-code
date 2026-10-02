---
name: license-audit
description: "Defensive license validation audit — identify licensing weaknesses and provide hardening guidance."
detect: ["license", "activation", "entitlement", "license check", "serial key", "license validation", "hardening license"]
category: core
tier: 2
---

# License Robustness Audit

> Defensive audit of software licensing mechanisms. Identifies common weaknesses in license validation logic and provides hardening recommendations.

## Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `license-weakness-patterns.yaml` | Common license validation weaknesses | 15 |
| `license-hardening.yaml` | Hardening recommendations | 10 |

## Core Problem

License validation is often the weakest link in commercial software. Client-side checks, hardcoded keys, and predictable algorithms create vulnerabilities that undermine software protection.

## Quick Reference

| Weakness | Risk | Mitigation |
| -------- | ---- | ---------- |
| Hardcoded validation key | CRITICAL | Server-side HMAC validation |
| Client-only check | HIGH | Server round-trip verification |
| Predictable serial algorithm | HIGH | Cryptographic key derivation |
| No integrity check | HIGH | Code signing + runtime hash |
| Static expiry date | MEDIUM | Server-synced time validation |

## Anti-Patterns

| Pattern | Why Bad |
| ------- | ------- |
| Single validation point | One patch disables all protection |
| String comparison for keys | Easily found via static analysis |
| No obfuscation | Validation logic trivially readable |

## Checklist

- [ ] License validation uses server-side component
- [ ] Keys derived cryptographically (not hardcoded)
- [ ] Multiple distributed validation points
- [ ] Runtime integrity verification enabled
- [ ] Expiry synced with server time
