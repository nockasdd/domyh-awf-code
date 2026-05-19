# Terminal Safety (merged: terminal-safety + terminal-antigravity)
---
name: terminal-safety
rule_id: "MOD-TRM-001"

description: "Safe terminal execution and Windows hang prevention."
category: safety

context:
  always_apply: true
  platforms: [windows]

principles:
  - Detect shell before generating commands (hsa_detect or manual check)
  - Use shell-specific chaining (bash: &&, cmd: &, ps5: ;, ps7: &&)
  - Confirm with user before destructive commands
  - Prefer non-interactive flags (--yes, -y)

windows_hang_prevention:
  core: "On Windows MINGW64/ConPTY: NEVER pipe, NEVER pager, NEVER interactive without flags."
  shell_detection: "hsa_detect(action:environment) FIRST. cmd=cmd /c, bash=native, ps=PS syntax."
  banned_pipes: ["| grep", "| tail", "| head", "| wc", "| sort", "| awk", "| sed", "| less", "| more"]
  banned_pagers: ["less", "more", "man", "git log/diff/show without --no-pager"]
  banned_interactive: ["npm init (add -y)", "npx create-* (add -y)", "python/node without -c/-e", "git add -p / rebase -i"]
  banned_infinite: ["tail -f", "watch", "docker logs -f", "npm run dev (background it)"]
  recovery: "No output >30s = terminate, retry with safe alternative"

dangerous_commands:
  require_confirmation: ["rm -rf", "DROP TABLE", "chmod 777", "curl|sh", "--force push"]
  always_blocked: ["fork bomb", "mkfs", "format drive"]

shell_syntax:
  chaining: { bash: "&&", cmd: "&", ps5: ";", ps7: "&&" }
  env_vars: { bash: "$VAR", cmd: "%VAR%", ps: "$env:VAR" }
