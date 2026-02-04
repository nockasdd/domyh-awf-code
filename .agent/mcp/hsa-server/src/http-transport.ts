/**
 * HSA v5.0 — HTTP Transport
 * Streamable HTTP transport for multi-client support
 * Follows MCP 2025-06-18 specification
 */

import express, { Request, Response, NextFunction } from "express";
import cors from "cors";
import helmet from "helmet";
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { tools, handleToolCall } from "./tools.js";
import { getConfig, type HSAConfig } from "./config.js";
import { logger, metrics, startTimer, generateTraceContext } from "./observability.js";
import { checkHealth, checkLiveness, checkReadiness } from "./health.js";
import { validateToken, type AuthContext } from "./auth.js";
import { getServerMetadata } from "./registry.js";
import { getMetrics, getMetricsContentType } from "./observability.js";

// ============================================================
// EXPRESS APP SETUP
// ============================================================

export function createHttpServer(config: HSAConfig) {
  const app = express();
  const log = logger.child({ component: "http" });

  // Security middleware
  app.use(helmet({
    contentSecurityPolicy: false, // Allow JSON responses
  }));
  
  // CORS configuration
  app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(",") || "*",
    methods: ["GET", "POST", "OPTIONS"],
    allowedHeaders: ["Content-Type", "Authorization", "X-Request-ID"],
  }));

  // Body parser
  app.use(express.json({ limit: "10mb" }));

  // Request logging middleware
  app.use((req: Request, res: Response, next: NextFunction) => {
    const trace = generateTraceContext();
    req.headers["x-request-id"] = trace.requestId;
    
    const timer = startTimer();
    
    res.on("finish", () => {
      const duration = timer.end();
      log.info({
        method: req.method,
        path: req.path,
        status: res.statusCode,
        duration_ms: Math.round(duration * 1000),
        requestId: trace.requestId,
      }, "HTTP request completed");
    });
    
    next();
  });

  // ============================================================
  // HEALTH ENDPOINTS
  // ============================================================

  app.get("/health", async (_req: Request, res: Response) => {
    const health = await checkHealth(config);
    const statusCode = health.status === "healthy" ? 200 
      : health.status === "degraded" ? 200 : 503;
    res.status(statusCode).json(health);
  });

  app.get("/ready", async (_req: Request, res: Response) => {
    const ready = await checkReadiness(config);
    res.status(ready ? 200 : 503).json({ ready });
  });

  app.get("/live", (_req: Request, res: Response) => {
    res.json({ alive: checkLiveness() });
  });

  // ============================================================
  // METRICS ENDPOINT
  // ============================================================

  app.get("/metrics", async (_req: Request, res: Response) => {
    try {
      const metricsData = await getMetrics();
      res.set("Content-Type", getMetricsContentType());
      res.send(metricsData);
    } catch (error) {
      res.status(500).send("Error collecting metrics");
    }
  });

  // ============================================================
  // REGISTRY ENDPOINT (.well-known)
  // ============================================================

  app.get("/.well-known/mcp", (_req: Request, res: Response) => {
    res.json(getServerMetadata());
  });

  // ============================================================
  // MCP TOOL ENDPOINTS
  // ============================================================

  // List available tools
  app.get("/tools", (_req: Request, res: Response) => {
    res.json({ tools });
  });

  // Execute tool (with optional auth)
  app.post("/tools/:name", async (req: Request, res: Response) => {
    const { name } = req.params;
    const args = req.body || {};
    const timer = startTimer();
    
    try {
      // Optional auth check
      let authContext: AuthContext | null = null;
      const authHeader = req.headers.authorization;
      
      if (authHeader) {
        authContext = await validateToken(authHeader);
        if (!authContext.valid) {
          metrics.toolCalls.inc({ tool: name, status: "unauthorized" });
          res.status(401).json({ error: "Invalid token", code: "UNAUTHORIZED" });
          return;
        }
      }

      // Execute tool
      const result = await handleToolCall(name, args, config);
      const duration = timer.end();
      
      metrics.toolCalls.inc({ tool: name, status: "success" });
      metrics.toolDuration.observe({ tool: name }, duration);

      res.json({
        success: true,
        result,
        meta: {
          tool: name,
          duration_ms: Math.round(duration * 1000),
          requestId: req.headers["x-request-id"],
        },
      });
    } catch (error) {
      const duration = timer.end();
      metrics.toolCalls.inc({ tool: name, status: "error" });
      metrics.toolDuration.observe({ tool: name }, duration);

      const message = error instanceof Error ? error.message : String(error);
      log.error({ tool: name, error: message }, "Tool execution failed");
      
      res.status(500).json({
        success: false,
        error: message,
        code: "TOOL_ERROR",
      });
    }
  });

  // ============================================================
  // STREAMING ENDPOINT (SSE)
  // ============================================================

  app.get("/stream/:name", async (req: Request, res: Response) => {
    const { name } = req.params;
    
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    
    // Send initial connection event
    res.write(`event: connected\ndata: ${JSON.stringify({ tool: name })}\n\n`);
    
    // Execute tool and stream results
    try {
      const result = await handleToolCall(name, req.query as Record<string, unknown>, config);
      res.write(`event: result\ndata: ${JSON.stringify(result)}\n\n`);
      res.write(`event: done\ndata: {}\n\n`);
    } catch (error) {
      const message = error instanceof Error ? error.message : String(error);
      res.write(`event: error\ndata: ${JSON.stringify({ error: message })}\n\n`);
    }
    
    res.end();
  });

  // ============================================================
  // ERROR HANDLER
  // ============================================================

  app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
    log.error({ error: err.message, stack: err.stack }, "Unhandled error");
    res.status(500).json({
      error: "Internal server error",
      code: "INTERNAL_ERROR",
    });
  });

  return app;
}

// ============================================================
// START HTTP SERVER
// ============================================================

export function startHttpServer(port: number = 3000) {
  const config = getConfig();
  const app = createHttpServer(config);
  const log = logger.child({ component: "http" });
  
  app.listen(port, () => {
    log.info({ port }, "HSA v5.0 MCP HTTP Server running");
    console.log(`🚀 HSA v5.0 MCP Server listening on http://localhost:${port}`);
    console.log(`📋 Endpoints:`);
    console.log(`   GET  /health       - Health check`);
    console.log(`   GET  /metrics      - Prometheus metrics`);
    console.log(`   GET  /.well-known/mcp - Server metadata`);
    console.log(`   GET  /tools        - List tools`);
    console.log(`   POST /tools/:name  - Execute tool`);
  });
  
  return app;
}

// Start if run directly
if (process.argv[1]?.includes("http-transport")) {
  startHttpServer(parseInt(process.env.PORT || "3000"));
}
