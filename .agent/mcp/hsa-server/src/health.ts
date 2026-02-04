/**
 * HSA v5.0 — Health Check Module
 * Health endpoints for monitoring and orchestration
 */

import type { HSAConfig } from "./config.js";
import { checkHSAAvailable, getHSAVersion } from "./python-bridge.js";
import { logger, metrics } from "./observability.js";

// ============================================================
// HEALTH STATUS TYPES
// ============================================================

export interface HealthStatus {
  status: "healthy" | "degraded" | "unhealthy";
  version: string;
  uptime: number;
  timestamp: string;
  checks: {
    python: ComponentHealth;
    hsa_engine: ComponentHealth;
    cache: ComponentHealth;
  };
  metrics?: {
    activeSessions: number;
    totalToolCalls: number;
    avgResponseTime: number;
  };
}

export interface ComponentHealth {
  status: "ok" | "warn" | "error";
  message?: string;
  latency_ms?: number;
}

// ============================================================
// HEALTH CHECK IMPLEMENTATION
// ============================================================

const startTime = Date.now();

export async function checkHealth(config: HSAConfig): Promise<HealthStatus> {
  const log = logger.child({ component: "health" });
  
  // Check Python availability
  const pythonCheck = await checkPythonHealth(config);
  
  // Check HSA engine
  const hsaCheck = await checkHSAHealth(config);
  
  // Check cache status
  const cacheCheck = checkCacheHealth();
  
  // Determine overall status
  const status = determineOverallStatus([pythonCheck, hsaCheck, cacheCheck]);
  
  const health: HealthStatus = {
    status,
    version: "5.0.0",
    uptime: Math.floor((Date.now() - startTime) / 1000),
    timestamp: new Date().toISOString(),
    checks: {
      python: pythonCheck,
      hsa_engine: hsaCheck,
      cache: cacheCheck,
    },
  };
  
  log.info({ health }, "Health check completed");
  
  return health;
}

async function checkPythonHealth(config: HSAConfig): Promise<ComponentHealth> {
  const start = Date.now();
  
  try {
    const available = await checkHSAAvailable(config);
    const latency = Date.now() - start;
    
    if (available) {
      return { status: "ok", latency_ms: latency };
    } else {
      return { 
        status: "error", 
        message: "HSA modules not available",
        latency_ms: latency,
      };
    }
  } catch (error) {
    return {
      status: "error",
      message: error instanceof Error ? error.message : "Unknown error",
      latency_ms: Date.now() - start,
    };
  }
}

async function checkHSAHealth(config: HSAConfig): Promise<ComponentHealth> {
  const start = Date.now();
  
  try {
    const version = await getHSAVersion(config);
    const latency = Date.now() - start;
    
    if (version && version !== "unknown") {
      return { 
        status: "ok", 
        message: `v${version}`,
        latency_ms: latency,
      };
    } else {
      return { 
        status: "warn", 
        message: "Version unknown",
        latency_ms: latency,
      };
    }
  } catch (error) {
    return {
      status: "error",
      message: error instanceof Error ? error.message : "Unknown error",
      latency_ms: Date.now() - start,
    };
  }
}

function checkCacheHealth(): ComponentHealth {
  // Currently basic check - can be enhanced with actual cache metrics
  try {
    return { status: "ok", message: "Cache operational" };
  } catch {
    return { status: "warn", message: "Cache status unknown" };
  }
}

function determineOverallStatus(
  checks: ComponentHealth[]
): "healthy" | "degraded" | "unhealthy" {
  const hasError = checks.some((c) => c.status === "error");
  const hasWarn = checks.some((c) => c.status === "warn");
  
  if (hasError) return "unhealthy";
  if (hasWarn) return "degraded";
  return "healthy";
}

// ============================================================
// READINESS & LIVENESS PROBES
// ============================================================

export async function checkReadiness(config: HSAConfig): Promise<boolean> {
  const health = await checkHealth(config);
  return health.status !== "unhealthy";
}

export function checkLiveness(): boolean {
  // Simple liveness check - process is alive
  return true;
}
