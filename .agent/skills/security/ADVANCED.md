# Security — Advanced Patterns

# DOMYH Agent v4.2 — Tier 3 Reference

# Load only when explicitly referenced

## Table of Contents

- [Input Validation](#input-validation)
- [Authentication Patterns](#authentication-patterns)
- [Authorization Patterns](#authorization-patterns)
- [Cryptography](#cryptography)

---

## Input Validation

### Schema Validation (Zod)

```typescript
import { z } from "zod";

const UserSchema = z.object({
  email: z.string().email(),
  password: z
    .string()
    .min(8, "Minimum 8 characters")
    .regex(/[A-Z]/, "Need uppercase")
    .regex(/[0-9]/, "Need number")
    .regex(/[^a-zA-Z0-9]/, "Need special char"),
  age: z.number().int().min(13).max(120),
});

// Validate and get typed result
const result = UserSchema.safeParse(input);
if (!result.success) {
  return { errors: result.error.format() };
}
const validUser = result.data; // Type-safe
```

### SQL Injection Prevention

```typescript
// ❌ VULNERABLE
const query = `SELECT * FROM users WHERE id = '${userId}'`;

// ✅ SAFE: Parameterized query
const query = `SELECT * FROM users WHERE id = $1`;
await db.query(query, [userId]);

// ✅ SAFE: ORM query builder
const user = await prisma.user.findUnique({
  where: { id: userId },
});
```

### XSS Prevention

```typescript
// ❌ VULNERABLE
element.innerHTML = userInput;

// ✅ SAFE: Text content
element.textContent = userInput;

// ✅ SAFE: DOMPurify for HTML
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// ✅ SAFE: React auto-escapes
<div>{userInput}</div>
```

---

## Authentication Patterns

### JWT with Refresh Tokens

```typescript
interface TokenPair {
  accessToken: string; // Short-lived (15 min)
  refreshToken: string; // Long-lived (7 days)
}

async function generateTokens(userId: string): Promise<TokenPair> {
  const accessToken = jwt.sign(
    { sub: userId, type: "access" },
    process.env.JWT_SECRET!,
    { expiresIn: "15m" },
  );

  const refreshToken = jwt.sign(
    { sub: userId, type: "refresh" },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: "7d" },
  );

  // Store refresh token hash in DB
  await db.refreshToken.create({
    data: { userId, tokenHash: hash(refreshToken) },
  });

  return { accessToken, refreshToken };
}

async function refreshAccessToken(refreshToken: string) {
  const payload = jwt.verify(refreshToken, process.env.JWT_REFRESH_SECRET!);

  // Validate token exists in DB
  const stored = await db.refreshToken.findFirst({
    where: { tokenHash: hash(refreshToken) },
  });

  if (!stored) throw new Error("Token revoked");

  return generateTokens(payload.sub);
}
```

### Cookie Security

```typescript
// Secure cookie settings
res.cookie("session", token, {
  httpOnly: true, // No JS access
  secure: true, // HTTPS only
  sameSite: "strict", // CSRF protection
  maxAge: 3600000, // 1 hour
  path: "/",
  domain: ".example.com",
});
```

---

## Authorization Patterns

### RBAC Implementation

```typescript
type Role = "admin" | "editor" | "viewer";
type Permission = "read" | "write" | "delete" | "admin";

const rolePermissions: Record<Role, Permission[]> = {
  admin: ["read", "write", "delete", "admin"],
  editor: ["read", "write"],
  viewer: ["read"],
};

function hasPermission(userRole: Role, required: Permission): boolean {
  return rolePermissions[userRole].includes(required);
}

// Middleware
function requirePermission(permission: Permission) {
  return (req: Request, res: Response, next: NextFunction) => {
    if (!hasPermission(req.user.role, permission)) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}
```

### ABAC (Attribute-Based)

```typescript
interface Policy {
  resource: string;
  action: string;
  condition: (user: User, resource: Resource) => boolean;
}

const policies: Policy[] = [
  {
    resource: "document",
    action: "edit",
    condition: (user, doc) => doc.ownerId === user.id || user.role === "admin",
  },
  {
    resource: "document",
    action: "delete",
    condition: (user, doc) => doc.ownerId === user.id && !doc.isPublished,
  },
];

function can(user: User, action: string, resource: Resource): boolean {
  return policies.some(
    (p) =>
      p.resource === resource.type &&
      p.action === action &&
      p.condition(user, resource),
  );
}
```

---

## Cryptography

### Password Hashing (Argon2)

```typescript
import argon2 from "argon2";

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3, // 3 iterations
    parallelism: 4, // 4 threads
  });
}

async function verifyPassword(
  hash: string,
  password: string,
): Promise<boolean> {
  return argon2.verify(hash, password);
}
```

### Encryption at Rest

```typescript
import { createCipheriv, createDecipheriv, randomBytes } from "crypto";

const ALGORITHM = "aes-256-gcm";

function encrypt(
  text: string,
  key: Buffer,
): { encrypted: string; iv: string; tag: string } {
  const iv = randomBytes(16);
  const cipher = createCipheriv(ALGORITHM, key, iv);

  let encrypted = cipher.update(text, "utf8", "hex");
  encrypted += cipher.final("hex");

  return {
    encrypted,
    iv: iv.toString("hex"),
    tag: cipher.getAuthTag().toString("hex"),
  };
}

function decrypt(
  data: { encrypted: string; iv: string; tag: string },
  key: Buffer,
): string {
  const decipher = createDecipheriv(
    ALGORITHM,
    key,
    Buffer.from(data.iv, "hex"),
  );
  decipher.setAuthTag(Buffer.from(data.tag, "hex"));

  let decrypted = decipher.update(data.encrypted, "hex", "utf8");
  decrypted += decipher.final("utf8");

  return decrypted;
}
```

---

_DOMYH Agent v4.2 — Tier 3 Reference_
