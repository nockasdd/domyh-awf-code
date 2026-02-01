---
name: edit-verification
priority: 2
always_apply: true
category: verification
---

# ✅ Edit Verification Rules

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📚 **Based on**: AI Agent Error Research 2024-2025

## Description

Mandatory verification after code edits to prevent silent failures.

---

## 🔴 CRITICAL: CODE DELETION BUG

### The Problem

```
⚠️ DOCUMENTED BUG (CVE Research 2025)

Agent may delete 100+ lines when merging new code.
Affects: GitHub Copilot Agent, Visual Studio
Cause: File merge mechanism bug
```

### Prevention

After EVERY file edit:

```bash
git diff HEAD -- <file>  # Always verify changes
```

---

## ✅ VERIFICATION GATES

### Gate 1: Edit Confirmation

After any edit, display:

```
📝 EDIT APPLIED

File: src/auth/login.service.ts
Lines Changed: +15, -3
Status: ✅ Applied

Changes:
- Added password validation
- Updated error messages
- Fixed null check

Verify: git diff HEAD -- src/auth/login.service.ts
```

### Gate 2: Syntax Check

```bash
# JavaScript/TypeScript
npx tsc --noEmit

# Go
go build ./...

# Python
python -m py_compile file.py

# Rust
cargo check
```

### Gate 3: Test Run (if applicable)

```bash
# Run related tests
npm test -- --testPathPattern="auth"
go test ./internal/auth/...
```

---

## 🔄 DIFF VERIFICATION

### Required Evidence Format

```diff
File: src/auth/login.service.ts
Lines: 45-52

- async login(email: string, password: string) {
-   return this.authService.login(email, password);
+ async login(email: string, password: string) {
+   if (!password || password.length < 8) {
+     throw new ValidationError('Password too short');
+   }
+   return this.authService.login(email, password);
  }
```

---

## 🚫 SCOPE LIMIT

### Only Edit What's Requested

```yaml
scope_rules:
  - DO edit files mentioned in request
  - DO edit directly related files (imports, types)
  - DONT refactor unrelated code
  - DONT auto-format entire file
  - DONT change coding style
```

### Scope Violation Warning

```
⚠️ SCOPE EXPANSION DETECTED

Request: Fix login validation
I also want to:
- Refactor error handling
- Update 3 related files

This expands the scope. Continue? (y/n):
```

---

## 📋 PATCH STRATEGY

### Small Changes Rule

```yaml
patch_rules:
  - Apply small hunks, not entire files
  - Commit frequently
  - Pull/rebase before patching
  - If patch fails, regenerate don't force
```

### When Patch Fails

```
❌ PATCH FAILED

File has changed since context was loaded.
Conflict in: auth.service.ts (line 45-50)

Options:
1️⃣ Pull latest and regenerate patch
2️⃣ Show manual merge steps
3️⃣ Abort and review changes

Enter number:
```

---

## 🔒 PROTECTED PATTERNS

### Never Auto-Edit

```yaml
protected_files:
  - .env*           # Environment secrets
  - *.key, *.pem    # Certificates
  - id_rsa*         # SSH keys
  - credentials.*   # Auth files
  - secrets.*       # Secrets files
```

### Protected Sections

```javascript
// @protected - do not modify
const API_KEY = process.env.API_KEY;
// @end-protected
```

---

## 📊 EDIT METRICS

### Track Per Session

```yaml
metrics:
  edits_attempted: 15
  edits_successful: 14
  edits_failed: 1
  lines_changed: +245, -89
  files_modified: 8
  scope_violations: 0
```

---

## 📋 VERIFICATION CHECKLIST

After every edit:

- [ ] Displayed diff evidence?
- [ ] Lines added/removed correct?
- [ ] Syntax check passed?
- [ ] No unintended deletions?
- [ ] Within requested scope?
- [ ] Tests still pass?

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Verification bắt buộc sau mỗi code edit để ngăn chặn silent failures.

## 🔴 QUAN TRỌNG: LỖI XÓA CODE

```
⚠️ LỖI ĐÃ ĐƯỢC GHI NHẬN

Agent có thể xóa 100+ dòng khi merge code mới.
Ảnh hưởng: GitHub Copilot Agent, Visual Studio
```

### Phòng Ngừa

Sau MỖI file edit:

```bash
git diff HEAD -- <file>  # Luôn verify changes
```

## ✅ CÁC GATE VERIFICATION

### Gate 1: Xác nhận Edit

```
📝 EDIT ĐÃ ÁP DỤNG

File: src/auth/login.service.ts
Lines: +15, -3
Status: ✅ Applied

Verify: git diff HEAD -- src/auth/login.service.ts
```

### Gate 2: Syntax Check

```bash
npx tsc --noEmit    # TypeScript
go build ./...      # Go
```

### Gate 3: Chạy Tests

```bash
npm test -- --testPathPattern="auth"
```

## 🚫 GIỚI HẠN SCOPE

```yaml
scope_rules:
  - ĐƯỢC sửa files trong request
  - KHÔNG refactor code không liên quan
  - KHÔNG auto-format toàn file
```

## 📋 CHECKLIST VERIFICATION

- [ ] Đã hiển thị diff evidence?
- [ ] Lines added/removed đúng?
- [ ] Syntax check passed?
- [ ] Không xóa code ngoài ý muốn?
- [ ] Trong scope requested?

---

_DOMYH Agent v4.2 • Verified: 62 documented edit failures_
