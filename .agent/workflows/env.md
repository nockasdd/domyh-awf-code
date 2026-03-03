---
description: "🔐 Environment management: configure variables, secrets, and multi-environment setup"
skills: { required: [security], contextual: [auto] }
success_criteria: "Environment secure, no exposed secrets, .env.example synced"
---

# 🔐 /env — Env Pro

> Secure Configuration Management
> 📚 Multi-environment • Secrets vault • Drift detection

---

## ENV FLOW

1. **SCAN** (Auto) — `hsa_session("environment config audit")`, detect stack via HSA (`hsa_detect`), find all .env\* files, check .gitignore rules, detect exposed secrets
2. **VALIDATE** — Validate format/types, detect missing/deprecated vars
3. **SYNC** — Sync .env.example template, drift detection between envs
4. **REPORT** — Security recommendations, next steps
5. **SYNC** — `hsa_check_changes` to update index after environment file changes

---

## COMMANDS

| Command                   | Description           | Risk      |
| ------------------------- | --------------------- | --------- |
| `/env`                    | Full audit & status   | 🟢 Safe   |
| `/env scan`               | Security scan only    | 🟢 Safe   |
| `/env add [KEY=val]`      | Add new variable      | 🟡 Medium |
| `/env sync`               | Sync .env.example     | 🟡 Medium |
| `/env rotate [KEY]`       | Rotate secret         | 🔴 High   |
| `/env validate`           | Type/format check     | 🟢 Safe   |
| `/env diff [env1] [env2]` | Compare environments  | 🟢 Safe   |
| `/env vault`              | Setup secrets manager | 🔴 High   |

---

## 📁 FILE STRUCTURE

### Standard Files

| File               | Purpose                            | Commit?      |
| ------------------ | ---------------------------------- | ------------ |
| `.env.example`     | Template with placeholders         | ✅ Yes       |
| `.env`             | Local development values           | ❌ No        |
| `.env.local`       | Local overrides (highest priority) | ❌ No        |
| `.env.development` | Development environment            | ❌ No        |
| `.env.staging`     | Staging server                     | ❌ No        |
| `.env.production`  | Production (use vault instead)     | ❌ No        |
| `.env.test`        | Test environment                   | ⚠️ Sometimes |

### Load Priority (By Framework)

| Framework | Priority Order                                                      |
| --------- | ------------------------------------------------------------------- |
| Next.js   | `.env.local` → `.env.{NODE_ENV}.local` → `.env.{NODE_ENV}` → `.env` |
| Vite      | `.env.{mode}.local` → `.env.{mode}` → `.env.local` → `.env`         |
| Nuxt      | `nuxt.config.ts` → `.env`                                           |
| Go        | `godotenv.Load()` + env struct parsing                              |
| Python    | `pydantic-settings` with env file precedence                        |

---

## 🔑 Validation Libraries

| Language       | Library                | Validation                         |
| -------------- | ---------------------- | ---------------------------------- |
| **Go**         | godotenv, caarlos0/env | Struct tags + Parse                |
| **Rust**       | dotenvy, config        | Serde + envy                       |
| **Python**     | python-dotenv          | pydantic-settings                  |
| **TypeScript** | dotenv                 | envalid, zod, t3-env               |
| **Java**       | Spring Profiles        | @Value, @ConfigurationProperties   |
| **C#**         | DotNetEnv              | Microsoft.Extensions.Configuration |
| **PHP**        | vlucas/phpdotenv       | Laravel config()                   |
| **Ruby**       | dotenv                 | figaro                             |

---

## 🔒 SECRETS MANAGEMENT

### Recommended Vaults

| Tool                   | Best For       | Key Feature     |
| ---------------------- | -------------- | --------------- |
| **HashiCorp Vault**    | Multi-cloud    | Dynamic secrets |
| **AWS SSM**            | AWS native     | Parameter Store |
| **GCP Secret Manager** | GCP native     | Auto-rotation   |
| **Azure Key Vault**    | Azure native   | HSM-backed      |
| **Doppler**            | Multi-platform | Auto-sync       |
| **1Password CLI**      | Teams          | Code references |

### Variable Categories

| Category     | Example                      | Security Level |
| ------------ | ---------------------------- | -------------- |
| App Config   | `PORT`, `LOG_LEVEL`          | 🟢 Low         |
| Service URLs | `DATABASE_URL`, `API_BASE`   | 🟡 Medium      |
| API Keys     | `STRIPE_KEY`, `GITHUB_TOKEN` | 🔴 High        |
| Credentials  | `DB_PASSWORD`, `JWT_SECRET`  | 🔴 Critical    |
---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...], auto_notify:true})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

