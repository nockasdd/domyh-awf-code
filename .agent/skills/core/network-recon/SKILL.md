---
name: network-recon
description: "Network reconnaissance — Nmap scanning, host discovery, service detection, attack surface mapping."
detect: ["nmap", "port scan", "network scan", "service detection", "host discovery", "network reconnaissance"]
category: core
tier: 2
---

# Network Reconnaissance

> Network scanning and attack surface mapping for defensive security assessments.

## Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `nmap-profiles.yaml` | Scan configuration profiles | 10 |
| `service-fingerprints.yaml` | Service identification patterns | 15 |

## Scan Profiles

| Profile | Speed | Coverage | Use Case |
| ------- | ----- | -------- | -------- |
| Quick | Fast | Top 100 ports | Initial discovery |
| Standard | Medium | Top 1000 ports | Regular assessment |
| Full | Slow | All 65535 ports | Comprehensive audit |
| Stealth | Slow | Top 1000 | IDS evasion testing |
| Service | Medium | Open ports only | Version detection |
| UDP | Slow | Top 100 UDP | DNS, SNMP, NTP discovery |

## Checklist

- [ ] Authorization obtained for target scope
- [ ] Host discovery completed
- [ ] TCP port scan completed
- [ ] Service version detection run
- [ ] NSE vulnerability scripts executed
- [ ] Findings documented with severity
