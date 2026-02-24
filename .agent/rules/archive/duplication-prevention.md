---
name: duplication-prevention
priority: 2
always_apply: true
category: quality
version: "4.5"
---

# 🔄 Duplication Prevention v6.4.5

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📝 **Note**: Consolidates `code-deduplication.md` + `logic-duplication-check.md`

## Enforcement Level: WARN

## Description

Two complementary rules:

1. **Code Dedup** — Before adding new functions, search existing code
2. **Logic Check** — Before reporting "missing", verify logic exists elsewhere

---

## 🔍 Before Adding New Functions

### Step 1: Search Existing Code

```yaml
search_patterns:
  1. grep_search: function name, keywords
  2. find_by_name: "utils", "helpers", "shared", "lib"
  3. view_file_outline: existing utility files
```

### Step 2: Check Standard Locations

| Language   | Check Directories                              |
| ---------- | ---------------------------------------------- |
| TypeScript | `src/lib/`, `src/utils/`, `lib/`               |
| Go         | `pkg/`, `internal/utils/`, `internal/helpers/` |
| Python     | `src/utils/`, `utils/`, `common/`              |
| Java       | `src/main/java/**/utils/`, `**/common/`        |
| C#         | `Common/`, `Utilities/`, `Helpers/`            |

### Step 3: Decision Matrix

| Found       | Action                             |
| ----------- | ---------------------------------- |
| Exact match | ✅ Use existing, don't create new  |
| Similar     | ⚠️ Consider extending existing     |
| None        | ✅ Create new in appropriate utils |

---

## 🔍 Before Reporting "Missing"

### Check for Refactored Logic

```yaml
fallback_checks: 1. Check _deprecated/ folder for migration notes
  2. Check manifest.yaml for updated references
  3. Check related directories (rules/ vs core/)
  4. Search for similar functionality elsewhere
```

### Example

```
❌ Wrong: "RULES.md is MISSING in core/"
Reality: RULES.md was split into 15 files in rules/

✅ Correct: Check rules/README.md → find evidence.md, safety.md
Report: "RULES.md was refactored into rules/"
```

---

## 📋 Enforcement

### On Function Creation:

```
⚠️ Similar function found: formatDate
📍 Location: src/utils/format.ts:42
💡 Consider using existing: formatDate()
```

### On Missing Report:

```
🔍 Checking fallbacks...
├── _deprecated/: Not found
├── manifest.yaml: Found → rules_dir updated
└── Result: Refactored to rules/
```

---

## 📋 Checklist

### Before Adding Utils:

- [ ] Searched existing codebase?
- [ ] Checked utils/lib/helpers directories?
- [ ] Confirmed no similar function exists?

### Before Reporting Missing:

- [ ] Checked \_deprecated/ folder?
- [ ] Checked manifest for new paths?
- [ ] Searched related directories?

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Ngăn chặn code trùng lặp và báo cáo sai về file thiếu.

## Trước Khi Thêm Function

1. Tìm kiếm code tương tự
2. Kiểm tra thư mục utils/shared
3. Chỉ tạo mới nếu thực sự không có

## Trước Khi Báo "Thiếu"

1. Kiểm tra \_deprecated/
2. Kiểm tra manifest.yaml
3. Tìm trong các thư mục liên quan

---

_DOMYH Awesome Code • Consolidated Duplication Prevention_
