---
name: quality
priority: 3
always_apply: true
version: "4.5"
data_file: "data/quality-standards.json"
---

# 📊 Quality Standards Rule v4.5

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📦 **Data**: See `data/quality-standards.json` for full tables

## Description

Agent applies international quality standards.

---

## Quick Reference

### 📏 ISO 25010 (8 Characteristics)

Functional Suitability | Performance | Compatibility | Usability | Reliability | Security | Maintainability | Portability

### 🔐 CWE Top 10 (2024)

| Priority | CWE     | Name           |
| -------- | ------- | -------------- |
| 1        | CWE-79  | XSS            |
| 2        | CWE-89  | SQL Injection  |
| 3        | CWE-352 | CSRF           |
| 4        | CWE-22  | Path Traversal |
| 5        | CWE-287 | Improper Auth  |

### 🌐 OWASP Top 5 (2021)

A01 Broken Access Control | A02 Crypto Failures | A03 Injection | A04 Insecure Design | A05 Misconfiguration

### 📊 Severity Levels

| P0 🔴 | P1 🟠  | P2 🟡  | P3 🟢   |
| ----- | ------ | ------ | ------- |
| 24h   | 3 days | 1 week | 2 weeks |

---

## ✅ Checklist

- [ ] CWE Top 25 vulnerabilities?
- [ ] OWASP Top 10 violations?
- [ ] ISO 25010 criteria met?
- [ ] Test coverage present?

---

# Tiếng Việt

> 🇻🇳 Xem `data/quality-standards.json` cho bảng đầy đủ

## Mức Độ Nghiêm Trọng

| P0 🔴 Nghiêm trọng | P1 🟠 Cao | P2 🟡 Trung bình | P3 🟢 Thấp |
| ------------------ | --------- | ---------------- | ---------- |
| 24h                | 3 ngày    | 1 tuần           | 2 tuần     |

---

_DOMYH Awesome Code v4.3 • Quality Standards (Externalized)_
