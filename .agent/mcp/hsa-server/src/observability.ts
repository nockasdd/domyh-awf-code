/**
 * HSA v5.0 — Observability Module
 * Structured logging + Metrics collection
 * 
 * Follows 2025-2026 MCP best practices for enterprise observability
 */

import pino from "pino";
import client from "prom-client";

// ============================================================
// STRUCTURED LOGGING (Pino)
// ============================================================

export const logger = pino({
  name: "hsa-mcp",
  level: process.env.LOG_LEVEL || "info",
  transport: process.env.NODE_ENV !== "production" 
    ? { target: "pino-pretty", options: { colorize: true } }
    : undefined,
  formatters: {
    level: (label) => ({ level: label }),
    bindings: (bindings) => ({
      pid: bindings.pid,
      hostname: bindings.hostname,
      service: "hsa-mcp",
      version: "5.0.0",
    }),
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

// Request context logging
export function createRequestLogger(requestId: string, tool: string) {
  return logger.child({ requestId, tool });
}

// ============================================================
// METRICS (Prometheus)
// ============================================================

// Initialize default metrics
client.collectDefaultMetrics({ prefix: "hsa_mcp_" });

// Custom metrics
export const metrics = {
  // Request counters
  toolCalls: new client.Counter({
    name: "hsa_mcp_tool_calls_total",
    help: "Total number of MCP tool calls",
    labelNames: ["tool", "status"],
  }),

  // Request duration histogram
  toolDuration: new client.Histogram({
    name: "hsa_mcp_tool_duration_seconds",
    help: "Duration of MCP tool calls in seconds",
    labelNames: ["tool"],
    buckets: [0.01, 0.05, 0.1, 0.5, 1, 2, 5, 10],
  }),

  // Python bridge metrics
  pythonCalls: new client.Counter({
    name: "hsa_mcp_python_calls_total",
    help: "Total number of Python bridge calls",
    labelNames: ["status"],
  }),

  pythonDuration: new client.Histogram({
    name: "hsa_mcp_python_duration_seconds",
    help: "Duration of Python execution in seconds",
    buckets: [0.1, 0.5, 1, 2, 5, 10, 30],
  }),

  // Active sessions gauge
  activeSessions: new client.Gauge({
    name: "hsa_mcp_active_sessions",
    help: "Number of active MCP sessions",
  }),

  // Cache metrics (v6.0 - multiple cache types)
  cacheHits: new client.Counter({
    name: "hsa_mcp_cache_hits_total",
    help: "Number of cache hits",
    labelNames: ["cache"],
  }),

  cacheMisses: new client.Counter({
    name: "hsa_mcp_cache_misses_total",
    help: "Number of cache misses",
    labelNames: ["cache"],
  }),

  // Token budget usage
  tokenUsage: new client.Gauge({
    name: "hsa_mcp_token_usage",
    help: "Current token budget usage",
    labelNames: ["category"],
  }),

  // Tool filtering (v6.0)
  toolsFiltered: new client.Counter({
    name: "hsa_mcp_tools_filtered_total",
    help: "Number of tools filtered from context",
    labelNames: ["count"],
  }),

  // Compression metrics (v6.0)
  compressionRatio: new client.Histogram({
    name: "hsa_mcp_compression_ratio",
    help: "Context compression ratio achieved",
    buckets: [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
  }),

  // Async jobs (v6.0)
  asyncJobs: new client.Gauge({
    name: "hsa_mcp_async_jobs",
    help: "Number of async jobs by status",
    labelNames: ["status"],
  }),
};

// Get metrics endpoint data
export async function getMetrics(): Promise<string> {
  return await client.register.metrics();
}

// Get metrics content type
export function getMetricsContentType(): string {
  return client.register.contentType;
}

// ============================================================
// TRACING HELPERS
// ============================================================

export interface TraceContext {
  requestId: string;
  traceId: string;
  spanId: string;
  parentSpanId?: string;
}

export function generateTraceContext(): TraceContext {
  const timestamp = Date.now().toString(36);
  const random = Math.random().toString(36).substring(2, 10);
  
  return {
    requestId: `req_${timestamp}${random}`,
    traceId: `trace_${timestamp}${random}`,
    spanId: `span_${Math.random().toString(36).substring(2, 10)}`,
  };
}

// ============================================================
// TIMING UTILITIES
// ============================================================

export function startTimer() {
  const start = process.hrtime.bigint();
  return {
    end: () => {
      const end = process.hrtime.bigint();
      return Number(end - start) / 1e9; // Convert to seconds
    },
  };
}

// ============================================================
// ERROR TRACKING
// ============================================================

export function logError(
  log: pino.Logger,
  error: unknown,
  context?: Record<string, unknown>
) {
  const errorInfo = error instanceof Error
    ? {
        name: error.name,
        message: error.message,
        stack: error.stack,
      }
    : { message: String(error) };

  log.error({ error: errorInfo, ...context }, "Error occurred");
}
