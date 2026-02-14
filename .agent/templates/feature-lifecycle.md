# Feature Lifecycle Template — DOMYH v6.2.7

> **Mục đích**: Template chuẩn cho feature docs khi sử dụng `/feature`
> **Tạo bởi**: Agent tự động tạo theo feature workflow

---

## 🏗️ Feature: {{FEATURE_NAME}}

**Status**: ⬜ Requirements | 🟡 Design | 🔵 Planning | 🟢 Implementation | ✅ Ship
**Created**: {{DATE}}
**Slug**: `{{FEATURE_SLUG}}`

---

## 📊 Phase Progress

| Phase             | Status | Gate          | Document            |
| ----------------- | ------ | ------------- | ------------------- |
| 1. Requirements   | ⬜     | G1 (Approval) | `requirements.md`   |
| 2. Design         | ⬜     | —             | `design.md`         |
| 3. Planning       | ⬜     | G2 (Approval) | `planning.md`       |
| 4. Implementation | ⬜     | —             | `implementation.md` |
| 5. Testing        | ⬜     | G3 (ACs pass) | `testing.md`        |

---

## 📋 Traceability

| AC     | Task(s) | File(s)     | Test(s) | Status |
| ------ | ------- | ----------- | ------- | ------ |
| AC-001 | T-001   | `file:line` | TC-001  | ⬜     |

---

## 📝 Summary

{Tóm tắt feature khi hoàn thành}

---

## 📊 Metrics

```yaml
total_effort: "Xh estimated / Yh actual"
files_changed: N
tests_added: N
coverage: "X%"
```

---

_Feature Lifecycle • DOMYH Awesome Code v6.2.7_
