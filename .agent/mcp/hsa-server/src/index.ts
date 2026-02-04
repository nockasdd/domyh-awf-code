#!/usr/bin/env node
/**
 * HSA v5.0 MCP Server
 * Model Context Protocol server for intelligent context management
 * 
 * Features:
 * - StdioTransport (default) + HTTP Transport
 * - Structured logging (Pino) + Metrics (Prometheus)
 * - OAuth 2.1 authentication
 * - Multi-agent coordination
 * - Streaming resources
 * - Registry discovery
 */

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import { tools, handleToolCall } from "./tools.js";
import { getConfig, validateConfig } from "./config.js";
import { logger, metrics, startTimer, generateTraceContext, logError } from "./observability.js";
import { checkHealth } from "./health.js";
import { initializeBuiltInStreams } from "./streaming.js";

// ============================================================
// INITIALIZATION
// ============================================================

const config = getConfig();
const log = logger.child({ component: "main" });

// Validate configuration
const validation = validateConfig(config);
if (!validation.valid) {
  log.error({ errors: validation.errors }, "Configuration validation failed");
  console.error("Configuration errors:", validation.errors);
  process.exit(1);
}

log.info({ 
  projectPath: config.projectPath,
  scriptsPath: config.scriptsPath,
}, "HSA v5.0 MCP Server initializing");

// ============================================================
// SERVER SETUP
// ============================================================

const server = new Server(
  {
    name: "domyh-hsa",
    version: "5.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// ============================================================
// REQUEST HANDLERS
// ============================================================

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  log.debug({ toolCount: tools.length }, "Listing tools");
  return { tools };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  const trace = generateTraceContext();
  const timer = startTimer();
  const requestLog = log.child({ requestId: trace.requestId, tool: name });
  
  requestLog.info({ args }, "Tool call started");
  
  try {
    const result = await handleToolCall(name, args ?? {}, config);
    const duration = timer.end();
    
    // Record metrics
    metrics.toolCalls.inc({ tool: name, status: "success" });
    metrics.toolDuration.observe({ tool: name }, duration);
    
    requestLog.info({ duration_ms: Math.round(duration * 1000) }, "Tool call completed");
    
    return {
      content: [
        {
          type: "text",
          text: typeof result === "string" ? result : JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    const duration = timer.end();
    
    // Record error metrics
    metrics.toolCalls.inc({ tool: name, status: "error" });
    metrics.toolDuration.observe({ tool: name }, duration);
    
    logError(requestLog, error, { duration_ms: Math.round(duration * 1000) });
    
    const message = error instanceof Error ? error.message : String(error);
    return {
      content: [
        {
          type: "text",
          text: `Error: ${message}`,
        },
      ],
      isError: true,
    };
  }
});

// ============================================================
// SESSION MANAGEMENT
// ============================================================

let activeSessions = 0;

server.onclose = () => {
  activeSessions--;
  metrics.activeSessions.set(activeSessions);
  log.info({ activeSessions }, "Session closed");
};

// ============================================================
// STARTUP
// ============================================================

async function main() {
  try {
    // Initialize built-in streams
    initializeBuiltInStreams(config);
    
    // Run initial health check
    const health = await checkHealth(config);
    log.info({ health: health.status }, "Initial health check");
    
    if (health.status === "unhealthy") {
      log.warn("Server starting in degraded mode - HSA engine may not be available");
    }
    
    // Start stdio transport
    const transport = new StdioServerTransport();
    await server.connect(transport);
    
    activeSessions++;
    metrics.activeSessions.set(activeSessions);
    
    log.info("HSA v5.0 MCP Server running on stdio");
    console.error("🚀 HSA v5.0 MCP Server running on stdio");
    console.error("📖 Features: Observability, Multi-Agent, Streaming, OAuth 2.1");
    
  } catch (error) {
    logError(log, error, { phase: "startup" });
    console.error("Failed to start HSA MCP Server:", error);
    process.exit(1);
  }
}

// ============================================================
// GRACEFUL SHUTDOWN
// ============================================================

process.on("SIGINT", () => {
  log.info("Received SIGINT, shutting down gracefully");
  process.exit(0);
});

process.on("SIGTERM", () => {
  log.info("Received SIGTERM, shutting down gracefully");
  process.exit(0);
});

process.on("uncaughtException", (error) => {
  logError(log, error, { type: "uncaughtException" });
  process.exit(1);
});

process.on("unhandledRejection", (reason) => {
  logError(log, reason, { type: "unhandledRejection" });
  process.exit(1);
});

// Start server
main();
