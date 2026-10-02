---
name: windows-forensics
description: "Defensive threat hunting over Windows Event Logs — detects suspicious authentication, persistence, and execution."
detect: ["windows event log", "forensics", "event viewer", "ETW", "sysmon", "security log", "logon event", "hayabusa"]
category: core
tier: 2
---

# Windows Forensic Analysis

> Defensive threat hunting over Windows Event Logs. Sweeps high-signal security events and produces triaged findings reports.

## Data Files

| File | Content | Records |
| ---- | ------- | ------- |
| `windows-eventlog-patterns.yaml` | High-signal Event IDs and detection rules | 15 |
| `forensic-artifacts.yaml` | Forensic artifact locations and significance | 10 |

## Engines

| Engine | Needs | Best for |
| ------ | ----- | -------- |
| native | PowerShell only | Live triage of current machine |
| hayabusa | Hayabusa exe in PATH | Deep Sigma-rule timeline over .evtx |

## Key Event IDs

| Event ID | Log | Significance |
| -------- | --- | ------------ |
| 4624/4625 | Security | Successful/failed logon |
| 4720 | Security | Account created |
| 4697 | Security | Service installed |
| 7045 | System | New service |
| 1102 | Security | Audit log cleared |
| 4688 | Security | Process created |
| 4104 | PowerShell | Script block logging |
| Sysmon 1 | Sysmon | Process creation |
| Sysmon 3 | Sysmon | Network connection |
| Sysmon 11 | Sysmon | File creation |

## Checklist

- [ ] Run as Administrator for Security log access
- [ ] Check Sysmon installation status
- [ ] Review last 24-72h of events
- [ ] Correlate with network logs if available
- [ ] Export findings in structured format
