---
name: terminal-safety
priority: 2
always_apply: true
category: execution
version: "4.5"
related: [shell-commands]
---

# 🖥️ Terminal Safety & Execution Rules

> 🌍 **Language / Ngôn ngữ**: English (default) | [Tiếng Việt](#tiếng-việt)
> 📚 **Based on**: AI Agent Error Research 2024-2025
> 📝 **Note**: Incorporates `safety.md` protected files and procedures

## Description

Rules to prevent terminal execution errors based on documented agent failures.

---

## 🛑 PRE-FLIGHT CHECKS

### Before ANY Terminal Command

> ⚠️ **See `shell-commands.md` for shell-specific syntax**

#### PowerShell (Windows)

```powershell
# Environment check
Write-Host "=== ENVIRONMENT CHECK ==="
$PWD                           # Working directory
$PSVersionTable.PSVersion      # PowerShell version (5.x vs 7+)
node -v 2>$null               # Node version
go version 2>$null            # Go version
```

#### Bash/Zsh (Linux/macOS)

```bash
# Environment check
echo "=== ENVIRONMENT CHECK ==="
pwd                           # Working directory
uname -a                      # OS info
node -v 2>/dev/null          # Node version
go version 2>/dev/null       # Go version
```

**Why?** WSL/Remote/Shell mismatch causes 15% of terminal failures.

---

## ⏱️ COMMAND TIMEOUT RULES

### T-01: Hang Prevention

| Condition                   | Action                  |
| --------------------------- | ----------------------- |
| Command > 60s no output     | ⏸️ Cancel + inform user |
| Command > 180s total        | 🛑 Force stop           |
| Interactive prompt detected | ⚠️ Warn and wait        |

### T-02: Output Verification

After every command:

```
✅ Exit code: 0 = success
❌ Exit code: non-zero = investigate
⚠️ No output = possible shell issue
```

---

## 🔒 DANGEROUS COMMANDS - REQUIRE CONFIRMATION

```yaml
always_confirm:
  - rm -rf
  - rm -r
  - drop table
  - truncate
  - format
  - git reset --hard
  - git push --force
  - docker system prune
  - npm publish
  - go install (global)
```

### Confirmation Format

```
⚠️ DANGEROUS COMMAND DETECTED

Command: rm -rf node_modules/
Impact: Delete 1,500+ files
Reversible: ❌ No

Proceed? (y/n):
```

---

## 🔄 COMMAND HISTORY TRACKING

### Anti-Loop Rule

If same command fails 2+ times:

```
🔁 LOOP DETECTED

Command `npm install` failed 2 times.
Errors: EACCES, ENOENT

Options:
1️⃣ Try with elevated permissions
2️⃣ Clear cache and retry
3️⃣ Manual intervention

Enter number:
```

---

## 🌐 REMOTE/WSL AWARENESS

### Detection Pattern

```
if (path.contains('/mnt/') || env.WSL_DISTRO_NAME) {
  → WSL environment detected
}
if (env.SSH_CONNECTION || env.REMOTE_CONTAINERS) {
  → Remote environment detected
}
```

### When Detected

```
📡 REMOTE ENVIRONMENT

Type: WSL Ubuntu
Windows Path: /mnt/c/Users/...
Linux Path: ~/project/...

⚠️ Ensure commands match environment
```

---

## 🛡️ SHELL INTEGRATION ISSUES

### Known Conflicts (Cursor 2.0+)

- Starship prompt
- Oh My Posh
- ble.sh
- OSC 633/133 sequences

### Workaround

If terminal output not visible:

```
1. Settings > Agents > Inline Editing & Terminal
2. Enable "Legacy Terminal Tool"
3. Kill all terminals (Ctrl+Shift+P)
4. Restart IDE
```

---

## 🔒 PROTECTED FILES

Always ask before modifying (from `safety.md`):

```yaml
protected_patterns:
  - ".env*" # Environment files
  - "*.config.*" # Config files
  - "docker-compose*.yml" # Docker configs
  - "Makefile" # Build scripts
  - "*.sql" # Database files
  - "package.json" # NPM dependencies
  - "go.mod" # Go dependencies
  - "requirements.txt" # Python dependencies
  - ".git*" # Git files
```

### Safe Procedure for Protected Files

1. **Notify** — Explain what will be done
2. **Reason** — Why it's needed
3. **Impact** — Consequences if done
4. **Wait** — Wait for user confirmation

---

## 📋 CHECKLIST

Before running commands:

- [ ] Verified current directory?
- [ ] Checked OS/environment?
- [ ] Command is safe?
- [ ] Not repeating failed command?
- [ ] Timeout configured?

---

# Tiếng Việt

> 🇻🇳 Phiên bản Tiếng Việt

## Mô Tả

Rules để ngăn chặn lỗi terminal dựa trên nghiên cứu về failures của AI agents.

## 🛑 KIỂM TRA TRƯỚC KHI CHẠY

### Trước MỌI Lệnh Terminal

```bash
# Luôn verify environment trước
pwd                    # Thư mục hiện tại
uname -a 2>/dev/null   # Thông tin OS
node -v 2>/dev/null    # Version Node (nếu JS)
go version 2>/dev/null # Version Go (nếu Go)
```

## ⏱️ QUY TẮC TIMEOUT

| Điều kiện                    | Hành động          |
| ---------------------------- | ------------------ |
| Lệnh > 60s không output      | ⏸️ Hủy + thông báo |
| Lệnh > 180s tổng             | 🛑 Force stop      |
| Phát hiện interactive prompt | ⚠️ Cảnh báo và chờ |

## 🔒 LỆNH NGUY HIỂM - CẦN XÁC NHẬN

- `rm -rf` - Xóa đệ quy
- `drop table` - Xóa bảng database
- `git reset --hard` - Reset git
- `npm publish` - Publish package

## 🔄 THEO DÕI LỊCH SỬ LỆNH

Nếu cùng 1 lệnh fail 2+ lần:

```
🔁 PHÁT HIỆN LẶP

Lệnh `npm install` fail 2 lần.

Options:
1️⃣ Thử với quyền admin
2️⃣ Clear cache và retry
3️⃣ Can thiệp thủ công
```

## 📋 CHECKLIST

- [ ] Đã verify directory hiện tại?
- [ ] Đã check OS/environment?
- [ ] Lệnh có an toàn?
- [ ] Không lặp lại lệnh đã fail?

---

_DOMYH Agent v4.5 • Based on 62 documented agent errors_
