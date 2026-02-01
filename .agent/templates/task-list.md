---
name: task-list
description_en: "Standard format for task lists and progress tracking."
description_vi: "Format chuẩn cho danh sách tasks và theo dõi tiến độ."
type: format
used_by: ["/plan", "/code", "/debug"]
---

> 🌍 **Language**: English (default) | Tiếng Việt available

# 📋 Template: Task List

## Description / Mô Tả

Standard format for task lists.

_Format chuẩn cho danh sách tasks._

---

## 📄 Task List Template

```markdown
# 📋 Task List — [Feature/Bug Name]

> **Created:** [Date]
> **Status:** [In Progress | Blocked | Done]
> **Assignee:** Agent + User

---

## 📊 Progress

| Status         | Count |
| -------------- | ----- |
| ⬜ Todo        | [X]   |
| 🔄 In Progress | [X]   |
| ✅ Done        | [X]   |
| ⏸️ Blocked     | [X]   |

---

## 📝 Tasks

### Phase 1: [Phase Name]

- [ ] **Task 1** — [Mô tả]
  - File: `path/to/file`
  - Effort: [S/M/L]
- [ ] **Task 2** — [Mô tả]
  - File: `path/to/file`
  - Effort: [S/M/L]
  - Depends on: Task 1

### Phase 2: [Phase Name]

- [ ] **Task 3** — [Mô tả]
- [ ] **Task 4** — [Mô tả]

---

## ⏸️ Blocked

| Task     | Blocked By | Action Needed |
| -------- | ---------- | ------------- |
| [Task X] | [Reason]   | [Action]      |

---

## ✅ Completed

- [x] **Task 0** — [Mô tả] ✅ [Date]

---

## 📝 Notes

[Ghi chú thêm nếu có]
```

---

## 📊 Task Status Icons

| Icon | Status      | Mô tả        |
| ---- | ----------- | ------------ |
| ⬜   | Todo        | Chưa bắt đầu |
| 🔄   | In Progress | Đang làm     |
| ✅   | Done        | Hoàn thành   |
| ⏸️   | Blocked     | Bị chặn      |
| ❌   | Cancelled   | Hủy bỏ       |

---

## 📏 Effort Sizing

| Size | Time     | Mô tả        |
| ---- | -------- | ------------ |
| S    | < 30m    | Thay đổi nhỏ |
| M    | 30m - 2h | Thay đổi vừa |
| L    | > 2h     | Thay đổi lớn |

---

## 📋 Ví Dụ

```markdown
# 📋 Task List — Add User Authentication

> **Created:** 2026-01-31
> **Status:** In Progress

---

## 📝 Tasks

### Phase 1: Setup

- [x] **Install dependencies** — Add bcrypt, jwt
  - File: `package.json`
  - Effort: S
- [x] **Create auth middleware**
  - File: `src/middleware/auth.ts`
  - Effort: M

### Phase 2: Implementation

- [ ] **Create login endpoint**
  - File: `src/routes/auth.ts`
  - Effort: M
  - Depends on: auth middleware
- [ ] **Create register endpoint**
  - File: `src/routes/auth.ts`
  - Effort: M

### Phase 3: Testing

- [ ] **Write unit tests**
  - Effort: L
```

---

_DOMYH Agent v4.2_
