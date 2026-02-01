# DOMYH Agent Permissions v4.3

> Access control tiers based on 2025 AI safety best practices

## Permission Tiers

| Tier | Level       | Tools                       | Requires  |
| ---- | ----------- | --------------------------- | --------- |
| T1   | Read        | view_file, search, list_dir | None      |
| T2   | Write       | write_file, edit_file       | Auto      |
| T3   | Execute     | run_command                 | Safe flag |
| T4   | Destructive | delete, drop, deploy        | CONFIRM   |

---

## T1: Read-Only (Safe)

```yaml
allowed:
  - view_file
  - view_file_outline
  - grep_search
  - find_by_name
  - list_dir
  - read_url_content
```

No confirmation needed.

---

## T2: Safe Writes (Auto-approve)

```yaml
allowed:
  - write_to_file (new files)
  - replace_file_content
  - multi_replace_file_content
requires: File in project scope
```

---

## T3: Command Execution (SafeToAutoRun check)

```yaml
allowed:
  - run_command (SafeToAutoRun=true)
  - send_command_input
forbidden:
  - rm -rf
  - format
  - shutdown
  - DROP TABLE
  - DELETE FROM (no WHERE)
```

---

## T4: Destructive (MUST CONFIRM)

```yaml
requires_confirmation:
  - Any production environment
  - File deletion
  - Database drops
  - Schema migrations
  - Deploy commands
format: "⚠️ CONFIRM: [action] — [impact]"
```

---

## Path Restrictions

```yaml
allowed_paths:
  - "{project_root}/**"
  - "{temp}/**"
  - "{artifacts}/**"
forbidden_paths:
  - "C:/Windows/**"
  - "/etc/**"
  - "~/.ssh/**"
  - "**/node_modules/**"
```

---

## Rate Limits

| Action      | Limit | Window |
| ----------- | ----- | ------ |
| file_writes | 50    | 1min   |
| commands    | 20    | 1min   |
| api_calls   | 100   | 1min   |

---

_DOMYH Agent v4.3 — Permission Framework_
