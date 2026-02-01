---
name: language
priority: 1
always_apply: true
version: "4.5"
---

# 🌐 Language Rule v4.5

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📝 **Note**: This rule consolidates `language.md` + `vietnamese.md`

## Description

Agent output language is configurable. Supports English and Vietnamese.

---

## Configuration

Set language in `.agent/config.yaml`:

```yaml
i18n:
  default: "vi" # or "en"
  force: true # Force this language (from vietnamese.md)
```

---

## Language Modes

| Mode           | Behavior                         |
| -------------- | -------------------------------- |
| `en` (default) | All responses in English         |
| `vi`           | All responses in Vietnamese      |
| `force: true`  | Override user language detection |

---

## Output Rules

### ✅ REQUIRED

1. **Responses** — Reply in configured language
2. **Comments** — Code comments in configured language
3. **Reports** — Reports in configured language
4. **Error messages** — Explain errors in configured language
5. **Suggestions** — Suggestions in configured language

### ⚠️ EXCEPTIONS (Both Languages)

Keep in English regardless of mode:

- Variable names, function names, class names
- Code keywords (`if`, `for`, `function`, etc.)
- Library/framework names
- Error codes (e.g., `CWE-79`, `HTTP 500`)
- Technical terms without common translation

---

## Thuật Ngữ Kỹ Thuật / Technical Terms

| English        | Tiếng Việt   |
| -------------- | ------------ |
| Vulnerability  | Lỗ hổng      |
| Authentication | Xác thực     |
| Authorization  | Phân quyền   |
| Injection      | Chèn mã độc  |
| Memory leak    | Rò rỉ bộ nhớ |
| Performance    | Hiệu năng    |
| Refactor       | Tái cấu trúc |
| Deploy         | Triển khai   |
| Debug          | Gỡ lỗi       |
| Build          | Biên dịch    |

---

## Example

### ❌ WRONG (Mixed)

```
Found lỗ hổng SQL injection trong dòng 45.
```

### ✅ CORRECT (English mode)

```
Found SQL injection vulnerability at line 45.
Recommendation: Use parameterized queries.
```

### ✅ CORRECT (Vietnamese mode)

```
Phát hiện lỗ hổng SQL Injection tại dòng 45.
Đề xuất: Sử dụng parameterized queries.
```

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt (Mặc định cho dự án này)

## Mô Tả

Tất cả output của agent PHẢI bằng **Tiếng Việt** khi `force: true`.

## Quy Tắc

### ✅ BẮT BUỘC

1. **Responses** — Trả lời bằng tiếng Việt
2. **Comments** — Comment code bằng tiếng Việt
3. **Reports** — Báo cáo bằng tiếng Việt
4. **Error messages** — Giải thích lỗi bằng tiếng Việt
5. **Suggestions** — Đề xuất bằng tiếng Việt

### ⚠️ NGOẠI LỆ

Giữ nguyên tiếng Anh cho:

- Tên biến, function, class
- Code keywords
- Technical terms không có từ Việt phổ biến
- Library/framework names
- Error codes

---

_DOMYH Awesome Code v4.3 • Consolidated Language Rule_
