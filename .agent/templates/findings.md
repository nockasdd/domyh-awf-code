---
name: findings
description_en: "Standard format for individual audit findings."
description_vi: "Format chuẩn cho từng finding được phát hiện."
type: format
used_by: ["all"]
---

> 🌍 **Language**: English (default) | Tiếng Việt available

# 📋 Template: Finding Format

## Description / Mô Tả

Standard format for each detected finding.

_Format chuẩn cho mỗi finding được phát hiện._

---

## 📄 Single Finding Template

````markdown
### [Severity Icon] [Finding Title]

**File:** `path/to/file.ext:line`
**Type:** [Security | Quality | Performance | DevOps]
**Severity:** [P0 🔴 | P1 🟠 | P2 🟡 | P3 🟢]
**CWE/OWASP:** [CWE-XX hoặc OWASP-XX nếu có]
**Confidence:** [🟢 High | 🟡 Medium | 🔴 Low]

**Vấn đề:**
[Mô tả ngắn gọn vấn đề, 1-2 câu]

**Code hiện tại:**

```[language]
// Line [X-Y]
[Code snippet - 3-7 lines]
```
````

**Đề xuất:**

```[language]
[Fixed code]
```

**Giải thích:**
[Tại sao đây là vấn đề, impact, best practice]

**References:**

- [Link to docs/CWE/OWASP nếu có]

````

---

## 📊 Severity Icons

| Level | Icon | Label | SLA |
|-------|------|-------|-----|
| P0 | 🔴 | Critical | 24h |
| P1 | 🟠 | High | 3 days |
| P2 | 🟡 | Medium | 1 week |
| P3 | 🟢 | Low | 2 weeks |

---

## 📝 Finding Types

| Type | Icon | Mô tả |
|------|------|-------|
| Security | 🔐 | Lỗ hổng bảo mật |
| Quality | ✨ | Vấn đề chất lượng |
| Performance | ⚡ | Vấn đề hiệu năng |
| DevOps | 🔧 | Vấn đề infrastructure |
| Bug | 🐛 | Logic error |
| Style | 🎨 | Code style |

---

## 📋 Ví Dụ

### 🔴 SQL Injection trong Login Handler

**File:** `internal/handlers/auth.go:45`
**Type:** Security 🔐
**Severity:** P0 🔴
**CWE:** CWE-89
**Confidence:** 🟢 High

**Vấn đề:**
Query SQL được xây dựng bằng string concatenation, cho phép attacker inject SQL.

**Code hiện tại:**
```go
// Line 45
query := "SELECT * FROM users WHERE email = '" + email + "'"
db.Query(query)
````

**Đề xuất:**

```go
query := "SELECT * FROM users WHERE email = $1"
db.Query(query, email)
```

**Giải thích:**
String concatenation cho phép attacker nhập `' OR '1'='1` để bypass auth.
Parameterized queries ngăn chặn hoàn toàn SQL injection.

**References:**

- https://cwe.mitre.org/data/definitions/89.html
- https://owasp.org/www-community/attacks/SQL_Injection

---

_DOMYH Awesome Code v4.3_
