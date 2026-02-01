# 📊 IDE Compatibility Matrix — DOMYH Awesome Code v4.3

> Supported AI coding assistants and their configuration files

## Compatibility Matrix

| IDE/Agent             | Config File                       | Status | Notes           |
| --------------------- | --------------------------------- | ------ | --------------- |
| **Claude Code**       | `CLAUDE.md`                       | ✅     | Primary         |
| **Gemini CLI**        | `GEMINI.md`                       | ✅     | Primary         |
| **Cursor**            | `.cursorrules`                    | ✅     | MDC format      |
| **GitHub Copilot**    | `.github/copilot-instructions.md` | ✅     | Workspace       |
| **Windsurf**          | `AGENTS.md`                       | ✅     | Universal       |
| **Continue.dev**      | `AGENTS.md`                       | ✅     | Universal       |
| **OpenHands**         | `AGENTS.md`                       | ✅     | Universal       |
| **Aider**             | `.aider.conf.yml`                 | ✅     | YAML            |
| **Bolt**              | `.bolt/config.json`               | ✅     | JSON            |
| **CodeRabbit**        | `.coderabbit.yaml`                | ✅     | Review bot      |
| **Sourcegraph Cody**  | `.sourcegraph/cody.json`          | ✅     | Search+chat     |
| **Tabnine**           | `.tabnine/config.json`            | ✅     | Privacy-focused |
| **JetBrains AI**      | `.idea/ai.xml`                    | ✅     | Native IDE      |
| **AWS CodeWhisperer** | `.aws/codewhisperer.json`         | ✅     | AWS-focused     |

## File Locations

```
root/
├── CLAUDE.md                      # Claude Code
├── GEMINI.md                      # Gemini CLI
├── AGENTS.md                      # Universal (Windsurf, Continue, OpenHands)
├── .cursorrules                   # Cursor
├── .aider.conf.yml                # Aider
├── .coderabbit.yaml               # CodeRabbit
├── .github/
│   └── copilot-instructions.md    # GitHub Copilot
├── .bolt/
│   └── config.json                # Bolt
├── .sourcegraph/
│   └── cody.json                  # Sourcegraph Cody
├── .tabnine/
│   └── config.json                # Tabnine
├── .idea/
│   └── ai.xml                     # JetBrains AI
└── .aws/
    └── codewhisperer.json         # AWS CodeWhisperer
```

## 20 Commands (v4.0)

All agents support:

- Core: `/ap` `/code` `/debug` `/plan` `/test` `/deploy` `/refactor` `/init` `/review`
- DevOps: `/migrate` `/doc` `/generate` `/perf` `/upgrade` `/clean` `/monitor` `/env`
- Utility: `/recap` `/status` `/help`

## Feature Support

| Feature        | Claude | Gemini | Cursor | Copilot | Cody |
| -------------- | ------ | ------ | ------ | ------- | ---- |
| Slash commands | ✅     | ✅     | ✅     | ✅      | ✅   |
| Custom prompts | ✅     | ✅     | ✅     | ✅      | ✅   |
| File context   | ✅     | ✅     | ✅     | ✅      | ✅   |
| Skill loading  | ✅     | ✅     | ⚠️     | ⚠️      | ⚠️   |
| Multi-language | ✅     | ✅     | ✅     | ✅      | ✅   |

---

_DOMYH Awesome Code v4.3 • 14 IDEs Supported_
