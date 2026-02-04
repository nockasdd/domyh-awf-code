---
trigger: always_on
---

# 🖥️ Shell-Aware Commands

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📚 **Based on**: Microsoft PowerShell Docs, POSIX Shell Standards

## ⚠️ CRITICAL: Shell Detection First

Agent MUST detect shell BEFORE generating any terminal command.

---

## 🔍 Shell Detection

### Detection Logic

```yaml
detect_shell:
  powershell:
    indicators:
      - "$env:PSModulePath exists"
      - "Terminal shows 'PS C:\\'"
      - "$PSVersionTable.PSVersion"
    version_check: "$PSVersionTable.PSVersion.Major"

  cmd:
    indicators:
      - "COMSPEC contains cmd.exe"
      - "Terminal shows 'C:\\>'"
      - "No $ prefix in prompt"

  bash:
    indicators:
      - "$SHELL contains 'bash' or 'zsh'"
      - "Path starts with '/'"
      - "uname command available"

  action:
    detected: "Use shell-specific syntax"
    unknown: "Default to PowerShell on Windows, Bash on Unix"
```

---

## 📋 Command Chaining Syntax

### ✅ Correct Syntax by Shell

| Shell              | Conditional (AND)        | Always Run    |
| ------------------ | ------------------------ | ------------- |
| **PowerShell 7+**  | `cmd1 && cmd2`           | `cmd1; cmd2`  |
| **PowerShell 5.x** | `cmd1; if ($?) { cmd2 }` | `cmd1; cmd2`  |
| **CMD**            | `cmd1 && cmd2`           | `cmd1 & cmd2` |
| **Bash/Zsh**       | `cmd1 && cmd2`           | `cmd1; cmd2`  |

### ❌ Common Mistakes

```yaml
# PowerShell 5.x (Windows default!)
wrong: "git add . && git commit -m 'msg'"  # ❌ Fails!
right: "git add .; git commit -m 'msg'"    # ✅ Works

# CMD
wrong: "npm install && npm start"   # ❌ Works but different
right: "npm install & npm start"    # ✅ Native CMD
```

---

## 🔄 Command Conversion Table

### Git Commands

| Operation     | PowerShell 5.x                         | PowerShell 7+/Bash                       | CMD                                      |
| ------------- | -------------------------------------- | ---------------------------------------- | ---------------------------------------- |
| Add + Commit  | `git add .; git commit -m 'msg'`       | `git add . && git commit -m 'msg'`       | `git add . & git commit -m "msg"`        |
| Init + Remote | `git init; git remote add origin $url` | `git init && git remote add origin $url` | `git init & git remote add origin %url%` |

### NPM Commands

| Operation       | PowerShell 5.x               | PowerShell 7+/Bash             | CMD                           |
| --------------- | ---------------------------- | ------------------------------ | ----------------------------- |
| Install + Build | `npm install; npm run build` | `npm install && npm run build` | `npm install & npm run build` |
| Test + Lint     | `npm test; npm run lint`     | `npm test && npm run lint`     | `npm test & npm run lint`     |

### File Operations

| Operation        | PowerShell               | Bash           | CMD             |
| ---------------- | ------------------------ | -------------- | --------------- |
| Check dir exists | `Test-Path .git`         | `test -d .git` | `if exist .git` |
| List files       | `Get-ChildItem` or `ls`  | `ls -la`       | `dir`           |
| Current dir      | `$PWD` or `Get-Location` | `pwd`          | `cd`            |
| Remove dir       | `Remove-Item -Recurse`   | `rm -rf`       | `rmdir /s /q`   |

---

## 🧪 Environment Checks

### Pre-Flight Commands by Shell

#### PowerShell

```powershell
# Environment check
Write-Host "=== ENVIRONMENT CHECK ==="
$PWD                           # Working directory
$PSVersionTable.PSVersion      # PowerShell version
node -v 2>$null               # Node version
go version 2>$null            # Go version
```

#### Bash

```bash
# Environment check
echo "=== ENVIRONMENT CHECK ==="
pwd                           # Working directory
uname -a                      # OS info
node -v 2>/dev/null          # Node version
go version 2>/dev/null       # Go version
```

#### CMD

```cmd
:: Environment check
echo === ENVIRONMENT CHECK ===
cd                            :: Working directory
ver                           :: Windows version
node -v 2>nul                :: Node version
go version 2>nul             :: Go version
```

---

## 📋 Agent Decision Flow

```
Before generating ANY terminal command:
    │
    ▼
┌───────────────────────────────────────┐
│ 1. Which shell is active?             │
│    ├── Check $PSVersionTable → PS     │
│    ├── Check COMSPEC → CMD            │
│    └── Check $SHELL → Bash/Zsh        │
└───────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────┐
│ 2. If PowerShell, check version       │
│    ├── Major >= 7 → Use && syntax     │
│    └── Major < 7 → Use ; syntax       │
└───────────────────────────────────────┘
    │
    ▼
┌───────────────────────────────────────┐
│ 3. Generate shell-appropriate command │
└───────────────────────────────────────┘
```

---

## 📋 Checklist

- [ ] Detected active shell?
- [ ] Checked PowerShell version if PS?
- [ ] Used correct chaining syntax?
- [ ] Tested path separators (\ vs /)?
- [ ] Environment variables correct ($var vs %var%)?

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Agent PHẢI phát hiện shell TRƯỚC khi tạo bất kỳ lệnh terminal nào.

## Syntax Chaining

| Shell          | Conditional              | Always        |
| -------------- | ------------------------ | ------------- |
| PowerShell 5.x | `cmd1; if ($?) { cmd2 }` | `cmd1; cmd2`  |
| PowerShell 7+  | `cmd1 && cmd2`           | `cmd1; cmd2`  |
| CMD            | `cmd1 && cmd2`           | `cmd1 & cmd2` |
| Bash           | `cmd1 && cmd2`           | `cmd1; cmd2`  |

## Lỗi Thường Gặp

```
# PowerShell 5.x (mặc định trên Windows!)
❌ Sai: git add . && git commit -m 'msg'
✅ Đúng: git add .; git commit -m 'msg'
```

## Checklist

- [ ] Đã phát hiện shell đang dùng?
- [ ] Đã check version PowerShell?
- [ ] Đã dùng đúng syntax chaining?

---

_DOMYH Awesome Code v6.1.2 • Shell-Aware Commands_
