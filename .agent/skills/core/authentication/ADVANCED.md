# Authentication — Advanced Patterns

## Table of Contents

- [OAuth 2.0 & OIDC](#oauth-20--oidc)
- [JWT Best Practices](#jwt-best-practices)
- [Session Management](#session-management)
- [Passkeys & WebAuthn](#passkeys--webauthn)
- [MFA Implementation](#mfa-implementation)

---

## OAuth 2.0 & OIDC

### Authorization Code + PKCE Flow

```typescript
// 1. Generate PKCE challenge
function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url')
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url')
  return { verifier, challenge }
}

// 2. Authorization request
const authUrl = new URL('https://auth.example.com/authorize')
authUrl.searchParams.set('response_type', 'code')
authUrl.searchParams.set('client_id', CLIENT_ID)
authUrl.searchParams.set('redirect_uri', REDIRECT_URI)
authUrl.searchParams.set('scope', 'openid profile email')
authUrl.searchParams.set('code_challenge', pkce.challenge)
authUrl.searchParams.set('code_challenge_method', 'S256')
authUrl.searchParams.set('state', crypto.randomBytes(16).toString('hex'))

// 3. Token exchange
async function exchangeCode(code: string, verifier: string) {
  const response = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: REDIRECT_URI,
      client_id: CLIENT_ID,
      code_verifier: verifier,
    }),
  })
  return response.json() // { access_token, refresh_token, id_token }
}
```

---

## JWT Best Practices

```yaml
token_design:
  access_token:
    algorithm: "RS256 or ES256 (asymmetric ✅), never HS256 for distributed"
    expiry: "15 minutes max"
    claims:
      required: [sub, iat, exp, iss, aud]
      optional: [roles, permissions, jti]
    storage: "Memory only (never localStorage)"
    size: "< 1KB"

  refresh_token:
    type: "Opaque (not JWT)"
    expiry: "7-30 days"
    storage: "HttpOnly + Secure + SameSite=Strict cookie"
    rotation: "Issue new refresh token on each use"
    revocation: "Server-side token family tracking"

  id_token:
    standard: "OIDC"
    usage: "Authentication only (never for API auth)"
    validation: "Verify signature + iss + aud + exp + nonce"

security_rules:
  - "NEVER store tokens in localStorage (XSS vulnerable)"
  - "ALWAYS validate JWT signature server-side"
  - "Use token rotation for refresh tokens"
  - "Implement token family revocation (detect reuse)"
  - "Set nbf (not before) for time-sensitive tokens"
  - "Include jti (JWT ID) for revocation lists"
```

---

## Session Management

### Secure Session Pattern

```typescript
// Server-side session with Redis
import { createSession, validateSession } from './auth'

const sessionConfig = {
  store: new RedisStore({ client: redis, prefix: 'sess:' }),
  cookie: {
    httpOnly: true,
    secure: true,
    sameSite: 'strict' as const,
    maxAge: 24 * 60 * 60 * 1000, // 24h
    domain: '.example.com',
    path: '/',
  },
  rolling: true, // Extend on activity
  regenerate: true, // New ID on privilege change
}

// Session fixation prevention
async function onLogin(req: Request, user: User) {
  // Regenerate session ID after auth
  await req.session.regenerate()
  req.session.userId = user.id
  req.session.role = user.role
  req.session.loginAt = Date.now()
}

// Concurrent session limit
async function checkConcurrentSessions(userId: string, max = 3) {
  const sessions = await redis.keys(`sess:user:${userId}:*`)
  if (sessions.length >= max) {
    // Revoke oldest session
    await redis.del(sessions[0])
  }
}
```

---

## Passkeys & WebAuthn

```typescript
// Registration
const credential = await navigator.credentials.create({
  publicKey: {
    challenge: serverChallenge,
    rp: { name: 'My App', id: 'example.com' },
    user: {
      id: userId,
      name: 'user@example.com',
      displayName: 'User',
    },
    pubKeyCredParams: [
      { alg: -7, type: 'public-key' },   // ES256
      { alg: -257, type: 'public-key' },  // RS256
    ],
    authenticatorSelection: {
      authenticatorAttachment: 'platform',  // Device biometric
      residentKey: 'required',
      userVerification: 'required',
    },
  },
})
// Send credential to server for storage
```

---

## MFA Implementation

```yaml
mfa_methods:
  totp:
    library: "otpauth (JS) / pyotp (Python)"
    algorithm: "SHA-1 (RFC 6238)"
    digits: 6
    period: 30
    backup_codes: 10  # One-time use

  webauthn:
    type: "Phishing-resistant ✅"
    standard: "FIDO2"
    factor: "Something you have + are"

  sms:
    status: "⚠️ Deprecated (SIM swap attacks)"
    fallback_only: true

flow:
  1: "User enters password"
  2: "Server verifies → requires MFA"
  3: "User provides TOTP/WebAuthn"
  4: "Server verifies → issues session"
  5: "Remember device (optional, 30 days)"
```

---
