---
name: security
detect: ["always"]
priority: 0
version: "4.3"
---

# Security Patterns (2025)

## 📦 Security Tools

| Tool           | Use Case            |
| -------------- | ------------------- |
| **Snyk**       | Dependency scanning |
| **Trivy**      | Container scanning  |
| **OWASP ZAP**  | DAST                |
| **SonarQube**  | SAST                |
| **Dependabot** | Auto updates        |

## OWASP Top 10 (2025)

- [ ] **A01 Broken Access Control** — Auth on every endpoint
- [ ] **A02 Cryptographic Failures** — TLS, proper encryption
- [ ] **A03 Injection** — Parameterized queries, input validation
- [ ] **A04 Insecure Design** — Threat modeling
- [ ] **A05 Security Misconfiguration** — Secure defaults
- [ ] **A06 Vulnerable Components** — Dependency scanning
- [ ] **A07 Auth Failures** — MFA, session management
- [ ] **A08 Integrity Failures** — Signed updates, CI/CD security
- [ ] **A09 Logging Failures** — Security events logged
- [ ] **A10 SSRF** — URL validation

## Common Fixes

| Vulnerability   | Fix                      |
| --------------- | ------------------------ |
| SQL Injection   | Parameterized queries    |
| XSS             | Output encoding, CSP     |
| CSRF            | Tokens, SameSite cookies |
| Secrets in code | Environment variables    |
| Weak passwords  | Bcrypt, argon2           |
| IDOR            | Authorization checks     |

## Security Headers

```typescript
// ✅ Security headers middleware
const securityHeaders = {
  "Content-Security-Policy": "default-src 'self'",
  "X-Frame-Options": "DENY",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
};
```

## Auth Patterns

```typescript
// ✅ JWT verification
import { jwtVerify } from "jose";

async function verifyToken(token: string) {
  const { payload } = await jwtVerify(
    token,
    new TextEncoder().encode(process.env.JWT_SECRET),
  );
  return payload;
}

// ✅ Password hashing
import bcrypt from "bcrypt";

const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.compare(password, hash);
```

## Input Validation

```typescript
// ✅ Zod validation
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z.string().min(1).max(100),
});

// Validate
const result = UserSchema.safeParse(input);
if (!result.success) {
  throw new ValidationError(result.error);
}
```

## Code Review Focus

```
- [ ] No hardcoded secrets?
- [ ] Input validated?
- [ ] Output encoded?
- [ ] Auth on endpoints?
- [ ] Errors don't leak info?
- [ ] Rate limiting?
```

---

_DOMYH Awesome Code v4.3_
