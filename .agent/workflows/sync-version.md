---
name: sync-version
trigger: ["/sync-version", "sync version", "update version"]
persona: devops
description: "🔄 Sync version across all files from VERSION.yaml SSoT"
---

# 🔄 /sync-version — Version Synchronization

> **Purpose**: Đồng bộ version từ `VERSION.yaml` tới TẤT CẢ files trong hệ thống
> **SSoT**: `.agent/core/VERSION.yaml`

---

## USAGE

```bash
/sync-version              # Full sync all files
/sync-version check        # Check for mismatches only (dry-run)
/sync-version workflows    # Sync workflow headers/footers only
/sync-version skills       # Sync skill headers/footers only
/sync-version core         # Sync core config files only
```

---

## HOW IT WORKS

### Step 1: Read VERSION.yaml SSoT

```yaml
# .agent/core/VERSION.yaml
system:
  version: "v5.5.0"
  version_short: "v5.5"

components:
  plan_pro: "3.2"
  code_pro: "3.2"
  debug_pro: "3.3"
  # ...etc
```

### Step 2: Generate Replacement Patterns

| Target          | Pattern                                          | Replacement                                                               |
| --------------- | ------------------------------------------------ | ------------------------------------------------------------------------- |
| Workflow Header | `# {emoji} /{cmd} — {Name} Pro v{old}`           | `# {emoji} /{cmd} — {Name} Pro v{component_version}`                      |
| Workflow Footer | `_DOMYH Awesome Code v{old} • {Name} Pro v{old}` | `_DOMYH Awesome Code v{system_version} • {Name} Pro v{component_version}` |
| Skill Header    | `# {Skill} — DOMYH Awesome Code v{old}`          | `# {Skill} — DOMYH Awesome Code v{system_version}`                        |
| Skill Footer    | `_DOMYH Awesome Code v{old} • {Tech}_`           | `_DOMYH Awesome Code v{system_version} • {Tech}_`                         |

### Step 3: Execute PowerShell Batch Update

```powershell
# Windows/PowerShell
$files = Get-ChildItem -Path ".agent" -Recurse -Include "*.md"
foreach ($file in $files) {
    (Get-Content $file.FullName -Raw) `
        -replace 'DOMYH Awesome Code v\d+\.\d+', 'DOMYH Awesome Code v5.5' `
        -replace '(Plan|Code|Debug|Test|Audit) Pro v\d+\.\d+', '$1 Pro v{version}' |
        Set-Content $file.FullName -NoNewline
}
```

---

## VERSION MAPPING

### Workflows → Component Versions

| Workflow | Component Key              | Current Version |
| -------- | -------------------------- | --------------- |
| `/plan`  | `plan_pro`                 | 3.2             |
| `/code`  | `code_pro`                 | 3.2             |
| `/debug` | `debug_pro`                | 3.3             |
| `/test`  | `test_pro`                 | 3.2             |
| `/ap`    | `audit_pro`                | 5.1             |
| Others   | `default_workflow_version` | 3.1             |

### Skills → Default Version

All skills use `system.version_short` (v5.5) in headers/footers.

---

## SYNC RULES

### Rule 1: Headers Use Component Version

```markdown
# Before

# 🔬 /ap — DOMYH Audit Pro v5.0

# After

# 🔬 /ap — Audit Pro v5.1
```

### Rule 2: Footers Use System + Component Version

```markdown
# Before

_DOMYH Awesome Code v4.3 • Audit Pro v5.0 • Multi-Expert Consensus_

# After

_DOMYH Awesome Code v5.5 • Audit Pro v5.1 • Multi-Expert Consensus_
```

### Rule 3: Skills Use System Version Only

```markdown
# Before

# React — DOMYH Awesome Code v4.3

# After

# React — DOMYH Awesome Code v5.5

# Footer unchanged (tech-specific)

_DOMYH Awesome Code v5.5 • React 19_
```

---

## QUICK SYNC COMMANDS

### Windows PowerShell

```powershell
# Sync SYSTEM version (v5.5) - ALWAYS DO THIS FIRST
Get-ChildItem -Path ".agent" -Recurse -Include "*.md","*.yaml" | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace 'DOMYH Awesome Code v\d+\.\d+', 'DOMYH Awesome Code v5.5' |
    Set-Content $_.FullName -NoNewline
}

# Then sync specific component versions:
# Audit Pro v5.1
Get-ChildItem -Path ".agent\workflows\ap.md" | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace 'Audit Pro v\d+\.\d+', 'Audit Pro v5.1' |
    Set-Content $_.FullName -NoNewline
}
```

### Linux/macOS (sed)

```bash
# Sync SYSTEM version
find .agent -name "*.md" -exec sed -i 's/DOMYH Awesome Code v[0-9]*\.[0-9]*/DOMYH Awesome Code v5.5/g' {} +

# Sync Audit Pro
sed -i 's/Audit Pro v[0-9]*\.[0-9]*/Audit Pro v5.1/g' .agent/workflows/ap.md
```

---

## DETECTION ALGORITHM

When agent reads a workflow file, it SHOULD:

1. **Extract command name** from filename (e.g., `ap.md` → `ap`)
2. **Map to component key** (e.g., `ap` → `audit_pro`)
3. **Lookup version** from VERSION.yaml
4. **Use that version** for all operations in that workflow

---

## AUTOMATED SYNC

Khi update version, chạy các lệnh sau theo thứ tự:

```powershell
# 1. Update VERSION.yaml manually (SSoT)
# 2. Run system-wide sync
Get-ChildItem -Path ".agent" -Recurse -Include "*.md","*.yaml" | ForEach-Object {
    (Get-Content $_.FullName -Raw) -replace 'DOMYH Awesome Code v[0-9]+\.[0-9]+', 'DOMYH Awesome Code v5.5' |
    Set-Content $_.FullName -NoNewline
}

# 3. Verify
$count = (Get-ChildItem -Path ".agent" -Recurse -Include "*.md","*.yaml" |
    Select-String "DOMYH Awesome Code v5.5" | Measure-Object).Count
Write-Host "Updated $count references to v5.5"
```

---

_DOMYH Awesome Code v5.5 • Version Sync • SSoT Architecture_
