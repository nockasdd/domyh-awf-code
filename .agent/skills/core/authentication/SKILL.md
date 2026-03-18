---
name: authentication
description: "Authentication and authorization patterns. Use when implementing OAuth, JWT, MFA, session management, or access control."
detect: ["login*", "oauth*", "passport*", "jwt*", "auth*"]
category: core
tier: 1
---

# Authentication Skill v1.0

> **370+ Patterns** | **12 Languages** | **OAuth 2.1 + Passkeys**

---

## Quick Stats

| Metric     | Value |
| ---------- | ----- |
| Patterns   | 370+  |
| Languages  | 12    |
| Categories | 8     |

---

## Core Concepts

### Authentication Factors

| Factor     | Description        | Examples            |
| ---------- | ------------------ | ------------------- |
| Knowledge  | Something you know | Password, PIN       |
| Possession | Something you have | Phone, hardware key |
| Inherence  | Something you are  | Fingerprint, face   |

### Modern Auth Landscape (2025-2026)

| Method          | Security | UX   | Adoption   |
| --------------- | -------- | ---- | ---------- |
| Passkeys        | Highest  | Best | Growing    |
| OAuth 2.1       | High     | Good | Standard   |
| JWT + Refresh   | Medium   | Good | Common     |
| Session cookies | Medium   | Fair | Legacy     |
| Basic Auth      | Low      | Poor | Deprecated |

---

## Language Coverage

| Language   | Libraries                           | Patterns |
| ---------- | ----------------------------------- | -------- |
| Go         | golang-jwt, x/oauth2, goth          | 25       |
| Python     | FastAPI OAuth2, Flask-Login, Django | 25       |
| TypeScript | Auth.js, Passport.js, jose          | 25       |
| Rust       | jsonwebtoken, axum-jwt-auth         | 25       |
| Java       | Spring Security, Keycloak           | 25       |
| C#         | ASP.NET Identity, MSAL              | 25       |
| Swift      | AuthenticationServices, Keychain    | 15       |
| Kotlin     | Firebase Auth, BiometricPrompt      | 15       |

---

## Core Patterns

### JWT Best Practices

```yaml
jwt_security:
  access_token:
    expiry: "15-30 minutes"
    storage: "Memory or HttpOnly cookie"
    algorithm: "RS256 preferred"
  refresh_token:
    expiry: "7-30 days"
    storage: "HttpOnly cookie"
    rotation: "On each use"
  claims:
    required: [iss, sub, exp, iat, aud]
    avoid: "Sensitive data (PII)"
```

### OAuth 2.1 Flows

```yaml
oauth_flows:
  authorization_code:
    use_for: "Web apps, SPAs with backend"
    pkce: "Required"
  client_credentials:
    use_for: "Service-to-service"
  device_code:
    use_for: "CLI, smart TV"
```

### Passkeys/WebAuthn

```yaml
passkeys:
  registration:
    - "Generate challenge"
    - "Create credential (biometric)"
    - "Store public key"
  authentication:
    - "Generate challenge"
    - "Sign with private key"
    - "Verify signature"
  benefits:
    - "Phishing resistant"
    - "No passwords to steal"
    - "Biometric convenience"
```

---

## HSA Integration

### Available Queries

Data powered by HSA BM25 search engine. Query YAML data via skill search:

| Domain   | Query Examples                      |
| -------- | ----------------------------------- |
| JWT      | "jwt refresh token rotation RS256"  |
| OAuth    | "OAuth 2.1 authorization code PKCE" |
| Passkeys | "WebAuthn passkey biometric"        |
| Session  | "session cookie HttpOnly"           |
| MFA      | "multi-factor TOTP authenticator"   |
| Password | "bcrypt argon2 hashing"             |
| Language | "go jwt golang authentication"      |

---

## Data Files (15 YAMLs)

| Category  | File                       | Patterns |
| --------- | -------------------------- | -------- |
| Core      | `core-patterns.yaml`       | 30       |
| Core      | `jwt-patterns.yaml`        | 30       |
| Core      | `oauth-patterns.yaml`      | 30       |
| Core      | `passkeys-webauthn.yaml`   | 25       |
| Core      | `session-patterns.yaml`    | 25       |
| Core      | `mfa-patterns.yaml`        | 20       |
| Core      | `password-patterns.yaml`   | 20       |
| Languages | `language-go.yaml`         | 25       |
| Languages | `language-python.yaml`     | 25       |
| Languages | `language-typescript.yaml` | 25       |
| Languages | `language-rust.yaml`       | 25       |
| Languages | `language-java.yaml`       | 25       |
| Languages | `language-csharp.yaml`     | 25       |
| Languages | `language-mobile.yaml`     | 25       |
| Anti      | `anti-patterns.yaml`       | 15       |
| **Total** | -                          | **~370** |

---

## Anti-Patterns

| Anti-Pattern                | Risk            | Fix                    |
| --------------------------- | --------------- | ---------------------- |
| Storing JWT in localStorage | XSS theft       | HttpOnly cookie        |
| Long-lived access tokens    | Token theft     | Short expiry + refresh |
| Hardcoded secrets           | Credential leak | Environment variables  |
| No token rotation           | Session hijack  | Rotate refresh tokens  |
| MD5/SHA1 password hash      | Rainbow tables  | bcrypt/argon2          |

---
