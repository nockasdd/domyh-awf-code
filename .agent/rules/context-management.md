---
name: context-management
priority: 1
always_apply: true
category: optimization
---

# 🧠 Context & Token Management Rules

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📚 **Based on**: AI Agent Error Research 2024-2025

## Description

Rules to prevent context overflow and optimize token usage.

---

## ⚠️ CRITICAL THRESHOLDS

### Context Window Limits

| Threshold   | Tokens  | Action                   |
| ----------- | ------- | ------------------------ |
| 🟢 Normal   | < 15k   | Continue normally        |
| 🟡 Warning  | 15k-20k | Start cleanup            |
| 🟠 High     | 20k-25k | Force cleanup            |
| 🔴 Critical | > 25k   | Models become distracted |

**Research Note:** "Above 25k tokens, most models start to become distracted and fail to follow system prompts" - Aider FAQ

---

## 📉 CONTEXT CLEANUP TRIGGERS

### Automatic Cleanup When

1. **Workflow Switch**
   - Clear previous workflow context
   - Keep only relevant state

2. **Successful Build**
   - Remove build logs
   - Keep only errors if any

3. **Debug Complete**
   - Remove stack traces
   - Keep solution summary

4. **Large File Process**
   - Remove full file contents after processing
   - Keep relevant snippets only

---

## 🧹 CLEANUP COMMANDS

### For Agent Users

```
/tokens  - Check current token usage
/drop    - Remove file from context
/clear   - Clear conversation history
```

### When To Use

| Situation         | Command                           |
| ----------------- | --------------------------------- |
| Context > 20k     | `/clear` + re-add essential files |
| Too many files    | `/drop` irrelevant files          |
| Long conversation | `/clear` + summarize              |

---

## 📋 TOKEN BUDGET ALLOCATION

### Recommended Distribution

```yaml
token_budget:
  system_prompt: 1,500 # Core instructions
  skills_t1: 1,800 # Always loaded
  skills_t2: 1,500 # Per active skill
  conversation: 8,000 # Chat history
  files: 10,000 # Code context
  output: 2,000 # Response generation
  # Total: ~25,000 max
```

---

## 🔄 AUTO-SUMMARIZATION

### When Conversation Gets Long

Every 10 interactions:

```
📊 CONTEXT SUMMARY

Completed:
- ✅ Fixed login bug
- ✅ Updated user model

Current Focus:
- Adding password validation

Files Active:
- auth.service.ts (450 tokens)
- user.model.ts (180 tokens)

Token Usage: 12,500 / 25,000 (50%)
```

---

## 🗂️ FILE MANAGEMENT

### Add Only What's Needed

```yaml
do:
  - Add files that need editing
  - Add files for reference (briefly)
  - Use snippets instead of full files

dont:
  - Add entire codebase
  - Keep files after done editing
  - Add binary files
```

### Large File Warning

```
⚠️ LARGE FILE DETECTED

File: src/components/Dashboard.tsx
Lines: 1,200+
Tokens: ~4,500

Recommendation:
1️⃣ Add specific section only
2️⃣ Use /drop after editing
3️⃣ Summarize instead of full view
```

---

## 📊 TOKEN MONITORING

### Status Display Format

```
💾 TOKEN STATUS

Current: 18,500 / 25,000 (74%)
Skills: 3,200 (security, react)
Files: 8,100 (5 files)
History: 7,200 (23 messages)

⚠️ Approaching limit - consider /clear
```

---

## 🚫 ANTI-HALLUCINATION RULES

### Context Quality > Context Quantity

1. **Verify Before Adding**
   - Does file exist?
   - Is content current?
   - Is it relevant?

2. **Remove Stale Data**
   - Old file versions
   - Outdated API docs
   - Previous session context

3. **Fact-Check Outputs**
   - Verify generated paths exist
   - Check API calls are valid
   - Confirm syntax is correct

---

## 📋 CHECKLIST

Before proceeding:

- [ ] Context under 20k tokens?
- [ ] Only relevant files loaded?
- [ ] Old conversation summarized?
- [ ] Stale data removed?

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Rules để ngăn chặn context overflow và tối ưu token usage.

## ⚠️ NGƯỠNG QUAN TRỌNG

| Ngưỡng         | Tokens  | Hành động              |
| -------------- | ------- | ---------------------- |
| 🟢 Bình thường | < 15k   | Tiếp tục               |
| 🟡 Cảnh báo    | 15k-20k | Bắt đầu cleanup        |
| 🔴 Nguy hiểm   | > 25k   | Models bị "distracted" |

## 🧹 LỆNH DỌN DẸP

```
/tokens  - Kiểm tra token usage
/drop    - Xóa file khỏi context
/clear   - Xóa lịch sử hội thoại
```

## 📋 PHÂN BỔ TOKEN

```yaml
token_budget:
  system_prompt: 1,500 # Core
  skills: 3,300 # Active skills
  conversation: 8,000 # Lịch sử chat
  files: 10,000 # Code context
  # Tổng: ~25,000 max
```

## 🔄 TỰ ĐỘNG TÓM TẮT

Mỗi 10 tương tác:

```
📊 TÓM TẮT CONTEXT

Đã hoàn thành:
- ✅ Sửa bug login
- ✅ Update user model

Đang làm:
- Thêm password validation

Token: 12,500 / 25,000 (50%)
```

## 📋 CHECKLIST

- [ ] Context dưới 20k tokens?
- [ ] Chỉ load files liên quan?
- [ ] Đã tóm tắt conversation cũ?
- [ ] Đã xóa data cũ?

---

_DOMYH Awesome Code v4.3 • Optimized for context efficiency_
