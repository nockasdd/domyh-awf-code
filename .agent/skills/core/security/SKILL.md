---
name: security
detect: ["always"]
priority: 0
version: "6.2.2"
---

# Security Patterns (Enhanced 2026)

> Comprehensive security skill with 290+ patterns across 14 data files. Covers OWASP Top 10, API Security, Mobile, Cloud, AI/ML, and Supply Chain.

## 📦 Data Files Overview

### Core Security

| File                 | Content                               | Records |
| -------------------- | ------------------------------------- | ------- |
| `owasp-top10.yaml`   | OWASP Top 10:2025 (NEW: Supply Chain) | 10      |
| `cwe-top25.yaml`     | CWE Top 25:2024 (XSS now #1)          | 25      |
| `auth-patterns.yaml` | AuthN/AuthZ patterns                  | 15      |

### Domain-Specific Security

| File                       | Content                               | Records |
| -------------------------- | ------------------------------------- | ------- |
| `network-security.yaml`    | TLS, DNS, GraphQL, gRPC, WebSocket    | 25      |
| `api-security.yaml`        | OWASP API Top 10:2023, JWT, OAuth     | 20      |
| `mobile-security.yaml`     | OWASP Mobile Top 10:2024, iOS/Android | 35      |
| `cloud-security.yaml`      | AWS/Azure/GCP, K8s, IaC               | 25      |
| `supply-chain.yaml`        | SLSA, SBOM, Dependency security       | 20      |
| `ai-ml-security.yaml`      | LLM, Prompt Injection, Adversarial    | 20      |
| `reverse-engineering.yaml` | Frida, Xposed, Play Integrity         | 30      |

### Language-Specific

| File                                       | Content              | Records |
| ------------------------------------------ | -------------------- | ------- |
| `language-specific/go-security.yaml`       | Go-specific patterns | 20      |
| `language-specific/csharp-security.yaml`   | C#/.NET patterns     | 20      |
| `language-specific/php-security.yaml`      | PHP patterns         | 20      |
| `language-specific/solidity-security.yaml` | Smart contracts      | 20      |

**Total: 290+ patterns across 14 files**

---

## �️ Security Tools

| Tool           | Use Case            |
| -------------- | ------------------- |
| **Snyk**       | Dependency scanning |
| **Trivy**      | Container scanning  |
| **OWASP ZAP**  | DAST                |
| **SonarQube**  | SAST                |
| **Semgrep**    | Custom rules        |
| **Dependabot** | Auto updates        |

---

## OWASP Top 10:2025 Quick Reference

| ID  | Vulnerability             | Severity | Key Fix                     |
| --- | ------------------------- | -------- | --------------------------- |
| A01 | Broken Access Control     | CRITICAL | RBAC/ABAC on every endpoint |
| A02 | Cryptographic Failures    | CRITICAL | bcrypt/argon2, TLS 1.3      |
| A03 | Injection                 | CRITICAL | Parameterized queries       |
| A04 | Insecure Design           | HIGH     | Threat modeling             |
| A05 | Security Misconfiguration | HIGH     | Hardened defaults           |
| A06 | Vulnerable Components     | HIGH     | SBOM, Dependency scanning   |
| A07 | Auth Failures             | CRITICAL | MFA, session rotation       |
| A08 | Integrity Failures        | HIGH     | SLSA, Signed releases       |
| A09 | Logging Failures          | MEDIUM   | Security event logging      |
| A10 | SSRF                      | HIGH     | URL allowlisting            |

---

## 🔥 NEW: AI/ML Security

> See `data/ai-ml-security.yaml` for 20 AI/ML threat patterns.

| ID      | Vulnerability      | Severity | Fix                            |
| ------- | ------------------ | -------- | ------------------------------ |
| AIML-01 | Prompt Injection   | CRITICAL | Input sanitization, guardrails |
| AIML-02 | Indirect Injection | CRITICAL | Content scanning               |
| AIML-03 | Jailbreaking       | HIGH     | Content policy checks          |
| AIML-04 | Training Poisoning | CRITICAL | Data validation, provenance    |
| AIML-09 | LLM Data Leakage   | CRITICAL | PII filtering, redaction       |
| AIML-10 | Insecure AI Output | HIGH     | Validation, sandboxing         |

```python
# ✅ LLM Security Example
def secure_llm_call(user_input: str) -> str:
    # 1. Sanitize input
    cleaned = sanitize_prompt(user_input)

    # 2. Detect prompt injection
    if detect_injection(cleaned):
        raise SecurityError("Potential injection detected")

    # 3. Call with guardrails
    response = llm.complete(
        messages=[
            {"role": "system", "content": STRICT_SYSTEM_PROMPT},
            {"role": "user", "content": cleaned}
        ],
        max_tokens=1000
    )

    # 4. Filter output
    return pii_filter(response)
```

---

## 📱 Mobile Security (OWASP 2024)

> See `data/mobile-security.yaml` for 35 mobile patterns.

| ID  | Vulnerability                    | Platform | Fix                        |
| --- | -------------------------------- | -------- | -------------------------- |
| M1  | Improper Credential Usage        | Both     | Keychain/Keystore          |
| M2  | Inadequate Supply Chain Security | Both     | Verify SDK, SBOM           |
| M3  | Insecure Auth/AuthZ              | Both     | Biometric + server verify  |
| M6  | Inadequate Privacy Controls      | Both     | Consent, data minimization |
| M7  | Insufficient Binary Protection   | Both     | Obfuscation, anti-tamper   |

```kotlin
// ✅ Play Integrity API (replaced SafetyNet 2024)
val integrityRequest = IntegrityManager.createRequest(nonce)
integrityManager.requestIntegrityToken(integrityRequest)
    .addOnSuccessListener { response ->
        // Verify token on server
        verifyTokenOnServer(response.token())
    }
```

---

## ☁️ Cloud Security

> See `data/cloud-security.yaml` for 25 cloud patterns.

```hcl
# ✅ Terraform: S3 Bucket Security
resource "aws_s3_bucket" "secure" {
  bucket = "my-secure-bucket"
}

resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.secure.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# ✅ Force IMDSv2 (prevent SSRF)
resource "aws_instance" "secure" {
  metadata_options {
    http_tokens = "required"
    http_put_response_hop_limit = 1
  }
}
```

---

## 🔗 Supply Chain Security

> See `data/supply-chain.yaml` for 20 patterns.

| SLSA Level | Description   | Requirements      |
| ---------- | ------------- | ----------------- |
| 1          | Documentation | Build exists      |
| 2          | Control       | Signed provenance |
| 3          | Integrity     | Hardened builds   |
| 4          | Trust         | Two-party review  |

```bash
# ✅ Generate SBOM (EU CRA 2024 mandatory)
npx @cyclonedx/cyclonedx-npm --output sbom.json

# ✅ Sign with Sigstore
cosign sign-blob sbom.json --bundle sbom.bundle

# ✅ npm publish with provenance
npm publish --provenance
```

---

## 🔐 Auth Patterns Quick Reference

```typescript
// ✅ JWT verification (jose)
import { jwtVerify } from "jose";

async function verifyToken(token: string) {
  const { payload } = await jwtVerify(
    token,
    new TextEncoder().encode(process.env.JWT_SECRET),
    { algorithms: ["HS256"] }, // Explicit algorithm
  );
  return payload;
}

// ✅ Password hashing (argon2)
import argon2 from "argon2";
const hash = await argon2.hash(password);
const valid = await argon2.verify(hash, password);
```

---

## ✅ Code Review Checklist

```
Security Review Checklist:
□ No hardcoded secrets/API keys?
□ All inputs validated (type, length, format)?
□ Outputs properly encoded/escaped?
□ Authorization checked on every endpoint?
□ Errors don't leak sensitive information?
□ Rate limiting on auth endpoints?
□ CSRF protection for state-changing ops?
□ Dependencies up to date (npm audit)?
□ SBOM generated for release?
□ LLM inputs/outputs sanitized?
```

---

_DOMYH Awesome Code • Security Skill Enhanced • 290+ Patterns_
