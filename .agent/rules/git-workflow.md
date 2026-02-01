---
name: git-workflow
priority: 3
always_apply: true
category: execution
version: "4.5"
related: [shell-commands]
---

# 📦 Git Workflow Rules v4.5

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📝 **Note**: Consolidates `git-detection.md` + `git-prerequisite-check.md`
> ⚠️ **Shell Awareness**: Commands use `;` for PS5.x. See `shell-commands.md`

## Description

Rules for git operations: detection, prerequisite checks, and deployment readiness.

---

## 🔍 Git Detection

### Before Suggesting Git Commands

| Condition       | Action                                     |
| --------------- | ------------------------------------------ |
| `.git/` exists  | Include git commands (commit, push, diff)  |
| `.git/` missing | Skip git suggestions, offer initialization |

### Detection Commands

```yaml
# Shell-specific detection
git_check:
  powershell: "Test-Path .git -PathType Container"
  bash: "test -d .git"
  on_success: include_git_suggestions
  on_failure: skip_git_suggestions
```

---

## ⚙️ Pre-Deploy Checks

### Before Suggesting `/deploy`

```yaml
preconditions:
  1_git_init:
    check: ".git/ directory exists"
    fail_action: "Suggest git init first"

  2_remote:
    check: "git remote -v has origin"
    fail_action: "Suggest: git remote add origin <url>"

  3_uncommitted:
    check: "git status --porcelain is empty"
    fail_action: "Suggest: git add .; git commit -m 'message'"
```

### Decision Flow

```
Before suggesting /deploy:
    │
    ├── No .git/? → "Initialize git: git init"
    │
    ├── No remote? → "Add remote: git remote add origin <url>"
    │
    ├── Uncommitted? → "Commit: git add .; git commit -m 'msg'"
    │
    └── All good → Proceed with /deploy
```

---

## 📋 Output Examples

### Project WITH Git

```
Next Steps:
├── ✅ Review changes: git diff
├── ✅ Commit: git commit -am "chore: cleanup"
└── ✅ Push: git push
```

### Project WITHOUT Git

```
Next Steps:
├── ✅ Changes saved successfully
└── 💡 Consider: git init; git add .; git commit -m 'Initial'
```

### Pre-Deploy (No Git)

```
📋 NEXT STEPS:
1️⃣ Initialize git: git init
2️⃣ Add remote: git remote add origin <your-repo-url>
3️⃣ First commit: git add .; git commit -m 'Initial commit'
4️⃣ Push: git push -u origin main

Would you like me to help set this up?
```

---

## 📋 Checklist

- [ ] Check `.git/` directory exists
- [ ] Check `git remote -v` has origin
- [ ] Check `git status` for uncommitted changes
- [ ] Only suggest `/deploy` if all conditions pass
- [ ] Provide helpful git setup instructions if missing

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Quy tắc cho các thao tác git: phát hiện, kiểm tra điều kiện tiên quyết, và sẵn sàng deploy.

## Trước Khi Đề Xuất Deploy

1. Kiểm tra `.git/` tồn tại?
2. Kiểm tra remote origin?
3. Kiểm tra uncommitted changes?

## Ví Dụ

```
📋 CÁC BƯỚC TIẾP THEO:
1️⃣ Khởi tạo git: git init
2️⃣ Thêm remote: git remote add origin <url>
3️⃣ Commit đầu tiên: git add .; git commit -m 'Initial'
4️⃣ Push: git push -u origin main
```

---

_DOMYH Agent v4.5 • Consolidated Git Workflow • Shell-Aware_
