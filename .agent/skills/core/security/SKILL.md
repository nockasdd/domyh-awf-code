---
name: security
detect: ["always"]
priority: 0
version: "6.1.2"
---

# Security Patterns (2026)

> Core skill with data-driven patterns. Check `data/` for comprehensive lookup tables.

## 📦 Data Files

| File                | Content                                                   | Records |
| ------------------- | --------------------------------------------------------- | ------- |
| `owasp-top10.csv`   | OWASP Top 10:2025 (NEW: A03 Supply Chain)                 | 10      |
| `cwe-top25.csv`     | CWE Top 25:2024 (XSS now #1, full 25 entries)             | 25      |
| `auth-patterns.csv` | AuthN/AuthZ patterns với secure examples và anti-patterns | 15      |

## 📦 Security Tools

| Tool           | Use Case            |
| -------------- | ------------------- |
| **Snyk**       | Dependency scanning |
| **Trivy**      | Container scanning  |
| **OWASP ZAP**  | DAST                |
| **SonarQube**  | SAST                |
| **Dependabot** | Auto updates        |

## OWASP Top 10 Quick Reference

See `data/owasp-top10.csv` for detection patterns and code examples.

| ID  | Vulnerability             | Severity | Key Fix                     |
| --- | ------------------------- | -------- | --------------------------- |
| A01 | Broken Access Control     | CRITICAL | RBAC/ABAC on every endpoint |
| A02 | Cryptographic Failures    | CRITICAL | bcrypt/argon2, TLS 1.3      |
| A03 | Injection                 | CRITICAL | Parameterized queries       |
| A04 | Insecure Design           | HIGH     | Threat modeling             |
| A05 | Security Misconfiguration | HIGH     | Hardened defaults           |
| A06 | Vulnerable Components     | HIGH     | Dependency scanning         |
| A07 | Auth Failures             | CRITICAL | MFA, session rotation       |
| A08 | Integrity Failures        | HIGH     | Signed releases, SRI        |
| A09 | Logging Failures          | MEDIUM   | Security event logging      |
| A10 | SSRF                      | HIGH     | URL allowlisting            |

## CWE Top 25 Quick Reference

See `data/cwe-top25.csv` for language-specific examples.

| CWE     | Name                | Languages | Key Fix                |
| ------- | ------------------- | --------- | ---------------------- |
| CWE-787 | Out-of-bounds Write | C, C++    | strncpy, bounds check  |
| CWE-79  | XSS                 | JS, TS    | DOMPurify, CSP         |
| CWE-89  | SQL Injection       | All       | Prepared statements    |
| CWE-416 | Use After Free      | C, C++    | Smart pointers         |
| CWE-78  | Command Injection   | All       | Avoid shell, safe APIs |
| CWE-22  | Path Traversal      | All       | path.basename, jail    |

## Security Headers

```typescript
// ✅ Security headers middleware
const securityHeaders = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self'",
  "X-Frame-Options": "DENY",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
};
```

## Auth Patterns

See `data/auth-patterns.csv` for comprehensive list.

```typescript
// ✅ JWT verification (jose library)
import { jwtVerify } from "jose";

async function verifyToken(token: string) {
  const { payload } = await jwtVerify(
    token,
    new TextEncoder().encode(process.env.JWT_SECRET),
  );
  return payload;
}

// ✅ Password hashing (bcrypt)
import bcrypt from "bcrypt";
const hash = await bcrypt.hash(password, 12);
const valid = await bcrypt.compare(password, hash);

// ✅ Rate limiting
import rateLimit from "express-rate-limit";
const limiter = rateLimit({ windowMs: 15 * 60 * 1000, max: 5 });
app.use("/login", limiter);
```

## Session Security

```typescript
// ✅ Secure cookie settings
Set-Cookie: sessionId=xxx; HttpOnly; Secure; SameSite=Strict; Path=/

// ✅ Session regeneration after login
req.session.regenerate(() => {
  req.session.userId = user.id;
  next();
});
```

## Input Validation

```typescript
// ✅ Zod validation
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8).max(100),
  name: z
    .string()
    .min(1)
    .max(100)
    .regex(/^[a-zA-Z\s]+$/),
});

const result = UserSchema.safeParse(input);
if (!result.success) throw new ValidationError(result.error);
```

## SQL Injection Prevention

```typescript
// ❌ BAD: String concatenation
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ GOOD: Parameterized query
db.query("SELECT * FROM users WHERE id = $1", [userId]);

// ✅ GOOD: ORM with safe methods
await User.findOne({ where: { id: userId } });
```

## Code Review Checklist

```
Security Review Checklist:
□ No hardcoded secrets/API keys?
□ All inputs validated (type, length, format)?
□ Outputs properly encoded/escaped?
□ Authorization checked on every endpoint?
□ Errors don't leak sensitive information?
□ Rate limiting on auth endpoints?
□ CSRF protection for state-changing operations?
□ Dependencies up to date (npm audit)?
```

## Quick Fixes Table

| Vulnerability   | Detection Pattern                      | Fix                    |
| --------------- | -------------------------------------- | ---------------------- |
| SQL Injection   | `query + `, string concat              | Parameterized queries  |
| XSS             | `innerHTML`, `dangerouslySetInnerHTML` | textContent, DOMPurify |
| CSRF            | Form without token                     | CSRF middleware        |
| Secrets in code | API_KEY=, password=                    | Environment variables  |
| Weak passwords  | MD5, SHA1 hash                         | bcrypt(12), argon2id   |
| IDOR            | No authz check                         | Permission middleware  |
| Path Traversal  | `../` in path                          | path.basename()        |

---

_DOMYH Awesome Code v6.1.2 • Security Skill (Data-Driven)_
