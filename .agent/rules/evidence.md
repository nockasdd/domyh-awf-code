---
name: evidence
priority: 2
always_apply: true
---

# 📍 Evidence Rule

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)

## Description

All findings MUST include concrete evidence.

---

## Rules

### ✅ REQUIRED

Each finding must have:

1. **File path** — Full path to the file
2. **Line number** — Specific line number
3. **Code snippet** — 3-7 relevant lines of code

### 📋 Format

````
**File:** path/to/file.go:45
**Code:**
```go
// Lines 43-47
func handleLogin(w http.ResponseWriter, r *http.Request) {
    password := r.FormValue("password")  // ⚠️ Not hashed
    db.Query("SELECT * FROM users WHERE pass = '" + password + "'")
}
````

---

## Fallback (If no line number)

If exact line number cannot be obtained, use:

1. **Function/Class anchor** — Function or class name
2. **Code snippet** — 3-7 lines of code
3. **Search pattern** — Regex to find

### Fallback Example

```
**File:** path/to/file.go
**Function:** `handleLogin`
**Pattern:** `db.Query.*password`
**Code:**
[snippet]
```

---

## Confidence Levels

| Level         | Description     | When to use       |
| ------------- | --------------- | ----------------- |
| 🟢 **High**   | Exact file:line | Direct evidence   |
| 🟡 **Medium** | File + function | Indirect evidence |
| 🔴 **Low**    | Pattern only    | Inferred          |

---

## 🔍 Multi-Source Verification (v4.3)

### When Required

| Topic Type               | Min Sources | Cross-Check   |
| ------------------------ | ----------- | ------------- |
| Security vulnerabilities | 2+          | **Mandatory** |
| Production deployment    | 2+          | **Mandatory** |
| Breaking changes         | 2+          | Recommended   |
| General technical        | 1           | Optional      |

### Verification Scoring

```yaml
confidence_from_sources:
  HIGH:
    criteria: "2+ sources agree, includes official docs"
    action: "Proceed with high confidence"

  MEDIUM:
    criteria: "1 reliable source (Stack Overflow 20+ votes)"
    action: "Proceed with note about verification"

  LOW:
    criteria: "Single blog/forum post, no votes"
    action: "Warn user, suggest manual verification"
```

### Integration with Online Research

> See `online-research.md` for detailed caching and search rules

---

## Examples

### ❌ WRONG

```
There is a SQL Injection bug in the code.
```

### ✅ CORRECT

````
**Finding:** SQL Injection
**Severity:** P0 🔴
**File:** internal/handlers/auth.go:45
**Confidence:** 🟢 High

**Code:**
```go
// Line 45
db.Query("SELECT * FROM users WHERE pass = '" + password + "'")
````

**Recommendation:**

```go
db.Query("SELECT * FROM users WHERE pass = $1", password)
```

```

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Mọi finding PHẢI có bằng chứng cụ thể.

## Quy Tắc

### ✅ BẮT BUỘC

Mỗi finding phải có:

1. **File path** — Đường dẫn đầy đủ
2. **Line number** — Số dòng cụ thể
3. **Code snippet** — 3-7 dòng code liên quan

## Mức Độ Tin Cậy

| Mức | Mô tả | Khi nào dùng |
|-----|-------|--------------|
| 🟢 **Cao** | Có file:line chính xác | Bằng chứng trực tiếp |
| 🟡 **Trung bình** | Có file + function | Bằng chứng gián tiếp |
| 🔴 **Thấp** | Chỉ có pattern | Suy luận |

## Ví Dụ

### ❌ SAI

```

Có lỗi SQL Injection trong code.

```

### ✅ ĐÚNG

```

**Finding:** SQL Injection
**Mức độ:** P0 🔴
**File:** internal/handlers/auth.go:45
**Tin cậy:** 🟢 Cao

**Đề xuất:** Sử dụng parameterized queries

```

---

_DOMYH Agent v2.0.0 • NockDev_
```
