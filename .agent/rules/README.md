# 📜 DOMYH Agent Rules System

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📚 **Version**: v4.4 - Architecture-Aware Implementation (AI Best Practices 2025)
>
> _Powered by [NockDev](https://github.com/nockasdd)_

## Overview

Universal rules that prevent common AI agent failures and optimize performance.

## Rules (21 files)

### 🔴 Priority 0 - Security Critical

| File                        | Description                                        |
| --------------------------- | -------------------------------------------------- |
| `prompt-injection-guard.md` | Prevent CVE-2025-53773 attacks, secrets protection |

### 🟠 Priority 1 - Core Safety

| File                    | Description                                  |
| ----------------------- | -------------------------------------------- |
| `context-management.md` | Token optimization, prevent context overflow |
| `safety.md`             | Dangerous action prevention                  |
| `language.md`           | Language output configuration                |
| `project-detection.md`  | **NEW** 5-phase scan, build system detection |

### 🟡 Priority 2 - Execution

| File                                   | Description                                      |
| -------------------------------------- | ------------------------------------------------ |
| `terminal-safety.md`                   | Command timeout, anti-loop, environment checks   |
| `edit-verification.md`                 | Verify edits, prevent code deletion              |
| `stop-conditions.md`                   | When agent must stop and ask                     |
| `evidence.md`                          | Evidence requirements for findings               |
| `pre-check-validation.md`              | 4-step flow before adding code                   |
| `yagni-enforcement.md`                 | Block unnecessary features                       |
| `incremental-changes.md`               | Small batches, test after each step              |
| `code-deduplication.md`                | Prevent duplicate utils/helpers                  |
| `logic-duplication-check.md`           | Verify logic before reporting missing            |
| `git-prerequisite-check.md`            | Git status check before operations               |
| `git-detection.md`                     | Detect git repository and branch                 |
| `architecture-aware-implementation.md` | **NEW** 5-phase validation before creating files |
| `online-research.md`                   | Decision matrix for web search                   |

### 🟢 Priority 3 - Quality

| File            | Description                         |
| --------------- | ----------------------------------- |
| `quality.md`    | ISO 25010, CWE Top 25, OWASP Top 10 |
| `vietnamese.md` | Vietnamese language support         |

## Priority Levels

| Level | Icon | Description       | When Applied   |
| ----- | ---- | ----------------- | -------------- |
| P0    | 🔴   | Security Critical | Always first   |
| P1    | 🟠   | Core Safety       | Every action   |
| P2    | 🟡   | Execution         | Commands/edits |
| P3    | 🟢   | Quality           | Analysis/audit |

## New in v4.2

Based on research of **62+ documented AI agent failures**:

### Terminal Safety (Prevents 12 failure types)

- Command timeout (60s default)
- Anti-loop detection (2 retries max)
- Environment verification
- Shell integration conflict detection

### Context Management (Prevents 8 failure types)

- Token warning at 15k
- Critical threshold at 20k
- Auto-summarize every 10 interactions
- Cleanup on workflow switch

### Edit Verification (Prevents 14 failure types)

- Mandatory diff evidence
- Syntax check after edits
- Scope limit enforcement
- Code deletion detection

### Prompt Injection Guard (CVE-2025-53773)

- Block external commands
- Sanitize user content
- Mask secrets in output
- Block "YOLO mode" activation

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Tổng Quan

Các quy tắc để ngăn chặn lỗi AI agent và tối ưu hiệu suất.

## Các Quy Tắc (11 files)

### 🔴 Priority 0 - Bảo mật Critical

| File                        | Mô tả                               |
| --------------------------- | ----------------------------------- |
| `prompt-injection-guard.md` | Ngăn CVE-2025-53773, bảo vệ secrets |

### 🟠 Priority 1 - An toàn Core

| File                    | Mô tả                               |
| ----------------------- | ----------------------------------- |
| `context-management.md` | Tối ưu token, ngăn context overflow |
| `safety.md`             | Ngăn hành động nguy hiểm            |
| `language.md`           | Cấu hình ngôn ngữ                   |

### 🟡 Priority 2 - Thực thi

| File                   | Mô tả                                    |
| ---------------------- | ---------------------------------------- |
| `terminal-safety.md`   | Timeout, chống loop, kiểm tra môi trường |
| `edit-verification.md` | Verify edits, ngăn xóa code              |
| `stop-conditions.md`   | Khi nào agent phải dừng                  |
| `evidence.md`          | Yêu cầu bằng chứng                       |

### Mới trong v4.2

Dựa trên nghiên cứu **62+ lỗi AI agent**:

- **Terminal Safety**: Timeout 60s, anti-loop 2 retries
- **Context Management**: Warning 15k, critical 20k tokens
- **Edit Verification**: Diff evidence bắt buộc
- **Prompt Injection Guard**: CVE-2025-53773 protection

---

_DOMYH Agent v4.2 • NockDev_
