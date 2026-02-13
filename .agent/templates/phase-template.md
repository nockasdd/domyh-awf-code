# 📋 Phase Template — DOMYH v6.2.4

> **Mục đích**: Template chuẩn cho phase files khi sử dụng `/plan full`
> **Tạo bởi**: Agent tự động tạo theo complexity detection

---

## 📊 Phase: {PHASE_NUMBER} — {PHASE_NAME}

**Status**: ⚪ Chưa bắt đầu | 🟡 Đang làm | ✅ Hoàn thành
**Estimated**: {X} tasks, ~{Y} giờ

---

## 🎯 Mục Tiêu

{Mô tả ngắn gọn mục tiêu của phase này}

---

## 📝 Tasks

- [ ] **Task 1**: {Mô tả task}
  - Files: `path/to/file.ts`
  - Est: {XS|S|M|L}

- [ ] **Task 2**: {Mô tả task}
  - Files: `path/to/file.ts`
  - Est: {XS|S|M|L}

- [ ] **Task 3**: {Mô tả task}
  - Files: `path/to/file.ts`
  - Est: {XS|S|M|L}

---

## 🔗 Dependencies

```yaml
depends_on:
  - phase-01 # Nếu có

blocks:
  - phase-03 # Phases phụ thuộc vào phase này
```

---

## ✅ Definition of Done

- [ ] Tất cả tasks hoàn thành
- [ ] Tests passed (nếu có)
- [ ] Code reviewed (nếu yêu cầu)
- [ ] Documentation updated

---

## 📊 Progress

```
████░░░░░░ 40% (2/5 tasks)
```

---

## 📝 Notes

{Ghi chú, decisions, issues gặp phải trong quá trình thực hiện}

---

_Phase Template • DOMYH Awesome Code v6.1_
