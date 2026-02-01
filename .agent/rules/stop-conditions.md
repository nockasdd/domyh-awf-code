---
name: stop-conditions
priority: 2
always_apply: true
---

# ⛔ Stop Conditions Rule

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)

## Description

Agent MUST STOP and wait for user in the following situations.

---

## 🛑 STOP IMMEDIATELY WHEN

### 1. Scope Confirmation Required

```
🎯 SCOPE CONTRACT - CONFIRMATION REQUIRED

| # | Scope | Estimate | Description |
|---|-------|----------|-------------|
| 1 | Full Audit | 2h | Everything |
| 2 | Backend Only | 1h | Backend only |
...

📝 Enter number (1-5):
```

### 2. Unclear Instructions

When user says:

- "Fix this" (fix what?)
- "Make it better" (better how?)
- "There's a problem" (what problem?)

**Action:** Ask for clarification.

### 3. Multiple Valid Approaches

When there are 2+ valid options:

- Pattern A vs Pattern B
- Library X vs Library Y
- Approach 1 vs Approach 2

**Action:** Present options and ask user.

### 4. Potential Data Loss

- File deletion
- Config overwrite
- Database changes
- Git operations (reset, force push)

**Action:** See Safety Rule.

### 5. Scope Expansion

When initial task is X but needs Y to complete:

```
⚠️ **Scope Expansion**

Initial task: Fix login bug
Additional needed: Refactor auth module

Continue with expanded scope? (y/n):
```

---

## 📋 STOP FORMAT

```
⏸️ **Confirmation Required**

[Describe situation]

Options:
1️⃣ [Option 1]
2️⃣ [Option 2]
3️⃣ [Option 3]

Enter number or describe:
```

---

## ✅ CONTINUE WHEN

- User has confirmed
- Instructions are clear
- Only 1 valid approach
- Action is safe and reversible
- Within agreed scope

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Agent PHẢI DỪNG và chờ user trong các tình huống sau.

## 🛑 DỪNG NGAY KHI

### 1. Cần Xác Nhận Scope

```
🎯 SCOPE CONTRACT - CẦN XÁC NHẬN

| # | Scope | Ước lượng | Mô tả |
|---|-------|-----------|-------|
| 1 | Full Audit | 2h | Toàn bộ |
| 2 | Backend Only | 1h | Chỉ backend |

📝 Gõ số (1-5):
```

### 2. Instruction Không Rõ Ràng

Khi user nói:

- "Sửa cái này" (cái nào?)
- "Làm tốt hơn" (tốt hơn như thế nào?)
- "Có vấn đề" (vấn đề gì?)

**Hành động:** Hỏi làm rõ.

### 3. Nhiều Cách Tiếp Cận

Khi có 2+ cách hợp lệ:

- Pattern A vs Pattern B
- Library X vs Library Y

**Hành động:** Trình bày options và hỏi user.

### 4. Action Có Thể Gây Mất Dữ Liệu

- Xóa file
- Overwrite config
- Database changes
- Git operations (reset, force push)

**Hành động:** Xem Safety Rule.

### 5. Vượt Quá Phạm Vi

```
⚠️ **Mở rộng scope**

Task ban đầu: Sửa bug login
Cần thêm: Refactor auth module

Tiếp tục với scope mở rộng? (y/n):
```

## ✅ TIẾP TỤC KHI

- User đã xác nhận
- Instruction rõ ràng
- Chỉ có 1 cách tiếp cận hợp lệ
- Action an toàn và có thể đảo ngược
- Trong phạm vi scope đã thống nhất

---

_DOMYH Agent v2.0.0 • NockDev_
