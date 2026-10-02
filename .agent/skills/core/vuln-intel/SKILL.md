---
name: vuln-intel
description: "CVE lookup, vulnerability triage, and threat intelligence from NVD, CISA KEV, EPSS, Exploit-DB."
detect: ["CVE", "vulnerability lookup", "CISA KEV", "EPSS", "NVD", "exploit-db", "threat intelligence"]
category: core
tier: 2
---

# Vulnerability Intelligence

> Multi-source CVE lookup and vulnerability triage. Aggregates data from NVD, CISA KEV, EPSS scoring, Exploit-DB, and Shodan.

## Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `cve-triage-matrix.yaml` | Priority triage decision matrix | 10 |
| `threat-intel-sources.yaml` | Intelligence source catalog | 8 |
| `exploitdb-search.yaml` | Exploit-DB search methodology | 10 |

## Quick Reference

| Source | Data | Use Case |
| ------ | ---- | -------- |
| NVD | CVSS scores, CWE mapping | Base severity assessment |
| CISA KEV | Known exploited vulns | Mandatory patch prioritization |
| EPSS | Exploitation probability | Risk-based prioritization |
| Exploit-DB | Public exploits/PoCs | Exploitability verification |
| Shodan | Exposed services | Attack surface correlation |

## Triage Workflow

1. Identify CVE from scan/advisory
2. Check CISA KEV for mandatory patches
3. Retrieve EPSS score for exploitation probability
4. Cross-reference Exploit-DB for public PoCs
5. Assess impact with CVSS environmental score
6. Prioritize: KEV > EPSS > 0.5 > CVSS Critical > CVSS High

## Anti-Patterns

| Pattern | Why Bad |
| ------- | ------- |
| CVSS-only prioritization | Ignores real-world exploitation likelihood |
| Ignoring KEV | Known exploited = must patch immediately |
| No EPSS correlation | Missing probability-based risk ranking |
