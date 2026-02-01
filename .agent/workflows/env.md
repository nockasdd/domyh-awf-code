---
name: env
trigger: ["/env", "environment", "config", "secrets"]
persona: devops
description: "🔐 Environment management: configure variables, secrets, and multi-environment setup"
---

# 🔐 /env — Environment & Secrets Pro v3.0

> Secure Configuration Management
> 📚 30+ Languages • Secrets Vault • Multi-Environment

---

## 🔄 ENVIRONMENT FLOW

```
User: /env [command]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: AUDIT (Auto)                  │
│ ▸ Scan for env files                    │
│ ▸ Detect secrets exposure               │
│ ▸ Check gitignore coverage              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: VALIDATE                       │
│ ▸ Check required vars present           │
│ ▸ Validate format/types                 │
│ ▸ Detect missing/deprecated vars        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: SYNC                           │
│ ▸ Sync .env.example template            │
│ ▸ Compare across environments           │
│ ▸ Flag drift between envs               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: PROTECT                        │
│ ▸ Encrypt sensitive values              │
│ ▸ Rotate secrets if needed              │
│ ▸ Update vault/cloud secrets            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: REPORT                         │
│ ▸ Show status summary                   │
│ ▸ Security recommendations              │
│ ▸ Next steps                            │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command         | Description               | Risk      |
| --------------- | ------------------------- | --------- |
| `/env`          | Full audit & status       | 🟢 Safe   |
| `/env init`     | Create .env from template | 🟢 Safe   |
| `/env sync`     | Sync .env.example         | 🟢 Safe   |
| `/env validate` | Validate all vars         | 🟢 Safe   |
| `/env encrypt`  | Encrypt secrets           | 🟡 Medium |
| `/env rotate`   | Rotate secrets            | 🟠 High   |
| `/env diff`     | Compare environments      | 🟢 Safe   |
| `/env --check`  | CI/CD validation          | 🟢 Safe   |

---

## 📋 PHASE 1: AUDIT

### Environment Audit Report:

```
🔐 ENVIRONMENT AUDIT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Files Found:
├── .env (local) ✅ gitignored
├── .env.example (template) ✅ committed
├── .env.development ✅ gitignored
├── .env.production ⚠️ NOT gitignored!
└── .env.local ✅ gitignored

Security Scan:
├── Exposed secrets: ⚠️ 2 found
│   ├── API_KEY in .env.production (line 5)
│   └── DB_PASSWORD in .env.production (line 12)
├── Hardcoded in code: ✅ None detected
└── Git history: ⚠️ 1 secret in commit abc123

Variables:
├── Total: 25 variables
├── Required: 18 (✅ all present)
├── Optional: 7
└── Deprecated: 1 (OLD_API_URL)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Action Required:
1. 🔴 Add .env.production to .gitignore
2. 🔴 Rotate exposed secrets
3. 🟡 Remove deprecated OLD_API_URL
```

---

## 📁 FILE STRUCTURE

### Standard Files:

```yaml
env_files:
  # ═══════════════════════════════════════════════════════════════
  # TEMPLATE (committed)
  # ═══════════════════════════════════════════════════════════════

  .env.example:
    purpose: "Template with placeholder values"
    commit: true
    contents: |
      # Database
      DATABASE_URL=postgresql://user:password@localhost:5432/db

      # API Keys (get from dashboard)
      API_KEY=your_api_key_here

      # App Config
      NODE_ENV=development
      PORT=3000

  # ═══════════════════════════════════════════════════════════════
  # LOCAL DEVELOPMENT (gitignored)
  # ═══════════════════════════════════════════════════════════════

  .env:
    purpose: "Local development values"
    commit: false

  .env.local:
    purpose: "Local overrides (highest priority)"
    commit: false

  .env.development:
    purpose: "Development environment"
    commit: false

  .env.development.local:
    purpose: "Local dev overrides"
    commit: false

  # ═══════════════════════════════════════════════════════════════
  # OTHER ENVIRONMENTS (gitignored or encrypted)
  # ═══════════════════════════════════════════════════════════════

  .env.staging:
    purpose: "Staging server"
    commit: false

  .env.production:
    purpose: "Production (use vault instead)"
    commit: false
    recommend: "Use secrets manager"

  .env.test:
    purpose: "Test environment"
    commit: sometimes # If no secrets
```

### Load Priority (Framework-specific):

```yaml
priority:
  nextjs:
    order: [".env.local", ".env.{NODE_ENV}.local", ".env.{NODE_ENV}", ".env"]

  vite:
    order: [".env.{mode}.local", ".env.{mode}", ".env.local", ".env"]

  create_react_app:
    order: [".env.{NODE_ENV}.local", ".env.local", ".env.{NODE_ENV}", ".env"]

  rails:
    order: ["config/credentials.yml.enc", ".env.{RAILS_ENV}", ".env"]

  spring_boot:
    order: ["application-{profile}.yml", "application.yml"]
```

---

## 🌐 VALIDATION TOOLS (30+ Languages)

### Backend / Systems

```yaml
go:
  library: "github.com/joho/godotenv"
  validation: "github.com/caarlos0/env"
  command: |
    go get github.com/joho/godotenv
    go get github.com/caarlos0/env/v10
  example: |
    type Config struct {
        Port     int    `env:"PORT" envDefault:"3000"`
        APIKey   string `env:"API_KEY,required"`
        Debug    bool   `env:"DEBUG" envDefault:"false"`
    }

    func LoadConfig() (*Config, error) {
        godotenv.Load()
        cfg := &Config{}
        return cfg, env.Parse(cfg)
    }

rust:
  library: "dotenvy, config"
  validation: "envy"
  command: "cargo add dotenvy config envy"
  example: |
    use serde::Deserialize;

    #[derive(Deserialize)]
    struct Config {
        port: u16,
        api_key: String,
        #[serde(default)]
        debug: bool,
    }

    fn load_config() -> Result<Config, envy::Error> {
        dotenvy::dotenv().ok();
        envy::from_env()
    }

java:
  library: "io.github.cdimascio:dotenv-java"
  validation: "Spring @Value, @ConfigurationProperties"
  command: "implementation 'io.github.cdimascio:dotenv-java:3.0.0'"
  example: |
    @Configuration
    @ConfigurationProperties(prefix = "app")
    @Validated
    public class AppConfig {
        @NotNull
        private String apiKey;
        
        @Min(1024) @Max(65535)
        private int port = 3000;
    }

kotlin:
  library: "io.github.cdimascio:dotenv-kotlin"
  validation: "Spring, Konf"
  command: 'implementation("io.github.cdimascio:dotenv-kotlin:6.4.1")'
  example: |
    val dotenv = dotenv()
    val apiKey = dotenv["API_KEY"] ?: throw Exception("API_KEY required")
    val port = dotenv["PORT"]?.toIntOrNull() ?: 3000

csharp:
  library: "DotNetEnv"
  validation: "Microsoft.Extensions.Configuration"
  command: "dotnet add package DotNetEnv"
  example: |
    DotNetEnv.Env.Load();
    var apiKey = Environment.GetEnvironmentVariable("API_KEY")
        ?? throw new Exception("API_KEY is required");

python:
  library: "python-dotenv"
  validation: "pydantic-settings"
  command: "pip install python-dotenv pydantic-settings"
  example: |
    from pydantic_settings import BaseSettings

    class Settings(BaseSettings):
        api_key: str
        port: int = 3000
        debug: bool = False
        
        class Config:
            env_file = ".env"

    settings = Settings()

ruby:
  library: "dotenv"
  validation: "dry-schema, config gem"
  command: "gem install dotenv"
  example: |
    require 'dotenv/load'

    API_KEY = ENV.fetch('API_KEY') { raise 'API_KEY required' }
    PORT = ENV.fetch('PORT', 3000).to_i

php:
  library: "vlucas/phpdotenv"
  validation: "symfony/validator"
  command: "composer require vlucas/phpdotenv"
  example: |
    $dotenv = Dotenv\Dotenv::createImmutable(__DIR__);
    $dotenv->load();
    $dotenv->required(['API_KEY', 'DATABASE_URL']);
    $dotenv->required('PORT')->isInteger();

# ═══════════════════════════════════════════════════════════════
# JAVASCRIPT / TYPESCRIPT
# ═══════════════════════════════════════════════════════════════

nodejs:
  library: "dotenv"
  validation: "envalid, zod, joi"
  command: "npm install dotenv envalid"
  example: |
    import { cleanEnv, str, port, bool } from 'envalid';

    const env = cleanEnv(process.env, {
      API_KEY: str(),
      PORT: port({ default: 3000 }),
      DEBUG: bool({ default: false }),
    });

typescript:
  library: "dotenv"
  validation: "zod, envalid, t3-env"
  command: "npm install dotenv zod @t3-oss/env-core"
  example: |
    import { createEnv } from "@t3-oss/env-core";
    import { z } from "zod";

    export const env = createEnv({
      server: {
        API_KEY: z.string().min(1),
        PORT: z.string().transform(Number).default("3000"),
      },
      runtimeEnv: process.env,
    });

nextjs:
  library: "Built-in + @t3-oss/env-nextjs"
  validation: "zod"
  command: "npm install @t3-oss/env-nextjs zod"
  example: |
    // env.mjs
    import { createEnv } from "@t3-oss/env-nextjs";
    import { z } from "zod";

    export const env = createEnv({
      server: {
        DATABASE_URL: z.string().url(),
        API_KEY: z.string().min(1),
      },
      client: {
        NEXT_PUBLIC_APP_URL: z.string().url(),
      },
      runtimeEnv: {
        DATABASE_URL: process.env.DATABASE_URL,
        API_KEY: process.env.API_KEY,
        NEXT_PUBLIC_APP_URL: process.env.NEXT_PUBLIC_APP_URL,
      },
    });

# ═══════════════════════════════════════════════════════════════
# MOBILE
# ═══════════════════════════════════════════════════════════════

swift:
  library: "Built-in ProcessInfo"
  validation: "Custom"
  command: "// Use xcconfig files"
  example: |
    enum Config {
        static let apiKey = ProcessInfo.processInfo
            .environment["API_KEY"] ?? ""
    }

dart:
  library: "flutter_dotenv, envied"
  validation: "envied"
  command: "flutter pub add flutter_dotenv envied"
  example: |
    import 'package:envied/envied.dart';

    @Envied(path: '.env')
    abstract class Env {
      @EnviedField(varName: 'API_KEY')
      static const String apiKey = _Env.apiKey;
    }

# ═══════════════════════════════════════════════════════════════
# INFRASTRUCTURE
# ═══════════════════════════════════════════════════════════════

docker:
  method: "--env-file, docker-compose"
  validation: "Container healthcheck"
  example: |
    # docker-compose.yml
    services:
      app:
        env_file:
          - .env
          - .env.${ENVIRONMENT:-development}
        environment:
          - NODE_ENV=${NODE_ENV:-production}

kubernetes:
  method: "ConfigMaps, Secrets"
  validation: "kubectl describe"
  example: |
    apiVersion: v1
    kind: Secret
    metadata:
      name: app-secrets
    type: Opaque
    stringData:
      API_KEY: ${API_KEY}
      DB_PASSWORD: ${DB_PASSWORD}

terraform:
  method: "terraform.tfvars, TF_VAR_*"
  validation: "variable validation blocks"
  example: |
    variable "api_key" {
      type        = string
      sensitive   = true
      
      validation {
        condition     = length(var.api_key) > 10
        error_message = "API key must be at least 10 characters"
      }
    }
```

---

## 🔐 SECRETS MANAGEMENT

### Secrets Platforms:

```yaml
# ═══════════════════════════════════════════════════════════════
# CLOUD NATIVE
# ═══════════════════════════════════════════════════════════════

aws_secrets_manager:
  best_for: "AWS infrastructure"
  features: ["Rotation", "IAM", "Audit"]
  cli: "aws secretsmanager get-secret-value --secret-id my-secret"
  sdk:
    node: "await secretsClient.getSecretValue({ SecretId: 'my-secret' })"
    python: "client.get_secret_value(SecretId='my-secret')"
    go: 'svc.GetSecretValue(&secretsmanager.GetSecretValueInput{SecretId: aws.String("my-secret")})'

aws_ssm_parameter:
  best_for: "Simple key-value, cost-effective"
  cli: "aws ssm get-parameter --name /app/api-key --with-decryption"

gcp_secret_manager:
  best_for: "Google Cloud"
  cli: "gcloud secrets versions access latest --secret=my-secret"

azure_key_vault:
  best_for: "Azure infrastructure"
  cli: "az keyvault secret show --vault-name myvault --name my-secret"

# ═══════════════════════════════════════════════════════════════
# PLATFORM AGNOSTIC
# ═══════════════════════════════════════════════════════════════

hashicorp_vault:
  best_for: "Enterprise, multi-cloud"
  features: ["Dynamic secrets", "Encryption", "PKI"]
  cli: "vault kv get secret/my-app"
  dynamic: |
    # Generate short-lived DB credentials
    vault read database/creds/my-role

doppler:
  best_for: "SaaS, team collaboration"
  features: ["Sync", "Versioning", "Audit"]
  cli: "doppler run -- npm start"
  inject: "doppler secrets download --no-file --format env"

infisical:
  best_for: "Open source, self-hosted"
  features: ["E2E encryption", "Versioning"]
  cli: "infisical run -- npm start"

1password:
  best_for: "Teams already using 1Password"
  cli: "op run -- npm start"
  inject: "op inject -i .env.tpl -o .env"

# ═══════════════════════════════════════════════════════════════
# CI/CD INTEGRATION
# ═══════════════════════════════════════════════════════════════

github_actions:
  store: "Repository secrets, Environment secrets"
  usage: "${{ secrets.API_KEY }}"

gitlab_ci:
  store: "CI/CD Variables"
  usage: "$API_KEY"

vercel:
  store: "Environment Variables"
  cli: "vercel env pull"
```

---

## 📋 PHASE 2: VALIDATE

### Validation Output:

```
✅ ENVIRONMENT VALIDATION

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Required Variables:
├── DATABASE_URL: ✅ Valid (postgresql://...)
├── API_KEY: ✅ Present (sk-***abc)
├── JWT_SECRET: ✅ Present (32+ chars)
├── REDIS_URL: ✅ Valid (redis://...)
└── NODE_ENV: ✅ Valid (production)

Format Validation:
├── PORT: ✅ Number (3000)
├── DEBUG: ✅ Boolean (false)
├── TIMEOUT_MS: ✅ Number (5000)
└── ALLOWED_ORIGINS: ✅ Array (["..."])

Warnings:
├── ⚠️ JWT_SECRET: Consider rotation (90+ days old)
└── ⚠️ API_KEY: Using legacy format

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 📋 PHASE 3: SYNC

### Environment Drift Detection:

```
🔄 ENVIRONMENT SYNC

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Comparing: .env.example ↔ .env

Missing in .env (need to add):
├── REDIS_URL (required)
└── CACHE_TTL (optional)

Extra in .env (not in template):
├── OLD_API_KEY (deprecated?)
└── TEMP_DEBUG (remove?)

Sync Command:
  Add missing: copy from .env.example
  Remove extra: review and delete

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Cross-Environment Drift:
├── development ↔ staging: 2 differences
└── staging ↔ production: 0 differences ✅
```

---

## 📋 PHASE 4: PROTECT

### Encryption & Rotation:

```yaml
encryption:
  # SOPS (Mozilla)
  sops:
    install: "brew install sops"
    encrypt: "sops -e .env > .env.enc"
    decrypt: "sops -d .env.enc > .env"

  # Age
  age:
    install: "brew install age"
    encrypt: "age -r $PUBLIC_KEY .env > .env.age"

  # git-crypt
  git_crypt:
    install: "brew install git-crypt"
    command: "git-crypt init && git-crypt add-gpg-user"

rotation:
  schedule:
    api_keys: "90 days"
    db_passwords: "30 days"
    jwt_secrets: "90 days"
    encryption_keys: "yearly"

  tools:
    aws: "aws secretsmanager rotate-secret"
    vault: "vault write -f auth/token/renew"
    manual: "Generate new → Update vault → Deploy → Invalidate old"
```

---

## 📋 PHASE 5: REPORT

### Final Summary:

```
🔐 ENVIRONMENT REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ⚠️ Needs Attention

Security Score: 7/10
├── ✅ .gitignore configured
├── ✅ No secrets in code
├── ⚠️ Secrets in git history
├── ✅ Validation in place
└── ⚠️ Rotation overdue

Environment Parity:
├── dev ↔ staging: ⚠️ 2 diffs
└── staging ↔ prod: ✅ Matched

Secrets Health:
├── Last rotation: 45 days ago
├── Next rotation: 45 days
└── Vault status: Connected

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Fix: Add .env.production to .gitignore
2️⃣ Rotate: API_KEY (exposed in history)
3️⃣ Sync: Add REDIS_URL to .env
4️⃣ Cleanup: Remove OLD_API_KEY

Enter number:
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  # Quick checks first
  - Audit gitignore before full scan
  - Validate required vars only
  - Skip optional if all required present

  # Batch operations
  - Group similar issues
  - One-command fixes where possible
  - Template-based .env generation
```

---

## 📜 RULES APPLIED

| Phase    | Rules                              |
| -------- | ---------------------------------- |
| Audit    | `safety`, `prompt-injection-guard` |
| Validate | `stop-conditions`                  |
| Sync     | `edit-verification`                |
| Protect  | `safety` (never log secrets)       |
| Report   | `evidence`                         |

---

## 🔐 SECRETS VAULT INTEGRATION (v3.1)

```yaml
secrets_vault:
  description: "Secure secrets management with auto-rotation"

  providers:
    local:
      - "1Password CLI (op)"
      - "Doppler"
      - "direnv"
    cloud:
      - "AWS Secrets Manager"
      - "HashiCorp Vault"
      - "Azure Key Vault"
      - "GCP Secret Manager"
    ci_cd:
      - "GitHub Secrets"
      - "GitLab CI Variables"
      - "Vercel Environment"

  rotation:
    auto_rotate: true
    frequency: "90 days default"
    notification: "7 days before expiry"
    grace_period: "24 hours overlap"

  zero_trust:
    principles:
      - "Never store secrets in code"
      - "Encrypt at rest and transit"
      - "Audit access logs"
      - "Least privilege access"

  commands:
    sync: "/env vault sync"
    rotate: "/env vault rotate [key]"
    audit: "/env vault audit"
```

---

## 🔄 MULTI-ENVIRONMENT SYNC (v3.1)

```yaml
multi_env_sync:
  description: "Consistent configuration across environments"

  environments:
    local: ".env.local"
    development: ".env.development"
    staging: ".env.staging"
    production: ".env.production"

  sync_strategies:
    template:
      source: ".env.example"
      action: "Copy and fill"

    vault:
      source: "Secrets vault"
      action: "Pull and decrypt"

    diff:
      description: "Compare environments"
      command: "/env diff [env1] [env2]"

  drift_detection:
    enabled: true
    alerts:
      - "Missing required variables"
      - "Type mismatches"
      - "Deprecated variables"

  validation:
    required_vars: ["DATABASE_URL", "API_KEY"]
    type_check: true
    format_check: true

  commands:
    sync: "/env sync [from] [to]"
    diff: "/env diff [env1] [env2]"
    validate: "/env validate [env]"
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command                   | Description            |
| ------------------------- | ---------------------- |
| `/env`                    | Audit all environments |
| `/env vault sync`         | Sync from vault        |
| `/env vault rotate [key]` | Rotate secret          |
| `/env diff [env1] [env2]` | Compare environments   |
| `/env sync [from] [to]`   | Sync between envs      |
| `/env validate [env]`     | Validate configuration |
| `/env generate`           | Generate .env.example  |

---

_DOMYH Agent v4.3 • Env Pro v3.1 • Vault + Multi-Env Sync_
