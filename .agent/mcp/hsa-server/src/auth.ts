/**
 * HSA v5.0 — OAuth 2.1 Authentication
 * Token validation and scope-based authorization
 * Follows 2025-2026 MCP security best practices
 */

import * as jose from "jose";
import { logger } from "./observability.js";

// ============================================================
// TYPES
// ============================================================

export interface AuthContext {
  valid: boolean;
  userId?: string;
  scopes?: string[];
  expiresAt?: Date;
  error?: string;
}

export interface TokenPayload {
  sub: string;        // Subject (user ID)
  scope?: string;     // Space-separated scopes
  exp?: number;       // Expiration
  iat?: number;       // Issued at
  iss?: string;       // Issuer
  aud?: string | string[]; // Audience
}

// ============================================================
// CONFIGURATION
// ============================================================

const AUTH_CONFIG = {
  // JWT verification options
  issuer: process.env.AUTH_ISSUER || "domyh-hsa",
  audience: process.env.AUTH_AUDIENCE || "hsa-mcp",
  
  // JWKS endpoint for key rotation
  jwksUrl: process.env.AUTH_JWKS_URL,
  
  // Fallback secret for development (use JWKS in production!)
  secret: process.env.AUTH_SECRET || "development-secret-change-in-production",
  
  // API key fallback
  apiKeyHeader: "X-API-Key",
  apiKeys: new Set((process.env.API_KEYS || "").split(",").filter(Boolean)),
};

// ============================================================
// TOKEN VALIDATION
// ============================================================

const log = logger.child({ component: "auth" });

export async function validateToken(authHeader: string): Promise<AuthContext> {
  // Check for Bearer token
  if (authHeader.startsWith("Bearer ")) {
    return await validateJWT(authHeader.substring(7));
  }
  
  // Check for API key
  if (authHeader.startsWith("ApiKey ")) {
    return validateApiKey(authHeader.substring(7));
  }
  
  return { valid: false, error: "Invalid authorization format" };
}

async function validateJWT(token: string): Promise<AuthContext> {
  try {
    // Try JWKS first if configured
    if (AUTH_CONFIG.jwksUrl) {
      return await validateWithJWKS(token);
    }
    
    // Fallback to symmetric secret
    const secret = new TextEncoder().encode(AUTH_CONFIG.secret);
    const { payload } = await jose.jwtVerify(token, secret, {
      issuer: AUTH_CONFIG.issuer,
      audience: AUTH_CONFIG.audience,
    });
    
    return extractAuthContext(payload as unknown as TokenPayload);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Token validation failed";
    log.warn({ error: message }, "JWT validation failed");
    return { valid: false, error: message };
  }
}

async function validateWithJWKS(token: string): Promise<AuthContext> {
  const jwks = jose.createRemoteJWKSet(new URL(AUTH_CONFIG.jwksUrl!));
  
  const { payload } = await jose.jwtVerify(token, jwks, {
    issuer: AUTH_CONFIG.issuer,
    audience: AUTH_CONFIG.audience,
  });
  
  return extractAuthContext(payload as unknown as TokenPayload);
}

function extractAuthContext(payload: TokenPayload): AuthContext {
  return {
    valid: true,
    userId: payload.sub,
    scopes: payload.scope?.split(" ") || [],
    expiresAt: payload.exp ? new Date(payload.exp * 1000) : undefined,
  };
}

function validateApiKey(apiKey: string): AuthContext {
  if (AUTH_CONFIG.apiKeys.has(apiKey)) {
    return {
      valid: true,
      userId: "api-key-user",
      scopes: ["read", "write"], // API keys get full access
    };
  }
  
  log.warn("Invalid API key attempted");
  return { valid: false, error: "Invalid API key" };
}

// ============================================================
// SCOPE CHECKING
// ============================================================

export function hasScope(context: AuthContext, requiredScope: string): boolean {
  if (!context.valid || !context.scopes) return false;
  return context.scopes.includes(requiredScope) || context.scopes.includes("*");
}

export function hasAnyScope(context: AuthContext, requiredScopes: string[]): boolean {
  return requiredScopes.some((scope) => hasScope(context, scope));
}

export function hasAllScopes(context: AuthContext, requiredScopes: string[]): boolean {
  return requiredScopes.every((scope) => hasScope(context, scope));
}

// ============================================================
// TOOL-SPECIFIC SCOPES
// ============================================================

export const TOOL_SCOPES: Record<string, string[]> = {
  hsa_get_context: ["read", "context"],
  hsa_detect_stack: ["read", "stack"],
  hsa_check_changes: ["read", "changes"],
  hsa_prefetch: ["read", "prefetch"],
  hsa_status: ["read", "status"],
  hsa_health: ["read", "health"],
};

export function canAccessTool(context: AuthContext, toolName: string): boolean {
  // If no auth required (public mode)
  if (!context.valid && !process.env.AUTH_REQUIRED) {
    return true;
  }
  
  const requiredScopes = TOOL_SCOPES[toolName] || ["read"];
  return hasAnyScope(context, requiredScopes);
}

// ============================================================
// TOKEN GENERATION (for development/testing)
// ============================================================

export async function generateToken(
  userId: string,
  scopes: string[] = ["read"],
  expiresIn: string = "1h"
): Promise<string> {
  const secret = new TextEncoder().encode(AUTH_CONFIG.secret);
  
  const token = await new jose.SignJWT({ scope: scopes.join(" ") })
    .setProtectedHeader({ alg: "HS256" })
    .setSubject(userId)
    .setIssuer(AUTH_CONFIG.issuer)
    .setAudience(AUTH_CONFIG.audience)
    .setIssuedAt()
    .setExpirationTime(expiresIn)
    .sign(secret);
  
  return token;
}
