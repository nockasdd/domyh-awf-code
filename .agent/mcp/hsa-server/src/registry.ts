/**
 * HSA v5.0 — MCP Registry Integration
 * Server metadata and capability discovery
 * Follows .well-known/mcp specification
 */

import { tools } from "./tools.js";

// ============================================================
// TYPES
// ============================================================

export interface ServerMetadata {
  name: string;
  version: string;
  description: string;
  homepage?: string;
  repository?: string;
  author?: string;
  license?: string;
  capabilities: ServerCapabilities;
  tools: ToolMetadata[];
  transports: TransportInfo[];
  authentication?: AuthenticationInfo;
  rateLimit?: RateLimitInfo;
}

export interface ServerCapabilities {
  tools: boolean;
  resources: boolean;
  prompts: boolean;
  sampling: boolean;
  streaming: boolean;
  multiAgent: boolean;
}

export interface ToolMetadata {
  name: string;
  description: string;
  inputSchema: object;
  scopes?: string[];
}

export interface TransportInfo {
  type: "stdio" | "http" | "websocket";
  url?: string;
  version: string;
}

export interface AuthenticationInfo {
  type: "none" | "oauth2" | "api-key" | "bearer";
  oauth2?: {
    authorizationUrl?: string;
    tokenUrl?: string;
    scopes?: Record<string, string>;
  };
}

export interface RateLimitInfo {
  requestsPerMinute: number;
  requestsPerHour: number;
  burstLimit: number;
}

// ============================================================
// SERVER METADATA
// ============================================================

export function getServerMetadata(): ServerMetadata {
  return {
    name: "domyh-hsa",
    version: "5.0.0",
    description: "HSA v5.0 MCP Server - Intelligent context management for AI coding agents",
    homepage: "https://github.com/NockDev/domyh-awesome-code",
    repository: "https://github.com/NockDev/domyh-awesome-code",
    author: "NockDev",
    license: "MIT",
    
    capabilities: {
      tools: true,
      resources: false, // Future: file resources
      prompts: false,   // Future: prompt templates
      sampling: false,
      streaming: true,  // SSE streaming support
      multiAgent: true, // Multi-agent coordination
    },
    
    tools: tools.map((tool) => ({
      name: tool.name,
      description: tool.description || "",
      inputSchema: tool.inputSchema,
      scopes: getToolScopes(tool.name),
    })),
    
    transports: [
      {
        type: "stdio",
        version: "2.0",
      },
      {
        type: "http",
        url: process.env.HTTP_BASE_URL || "http://localhost:3000",
        version: "2.0",
      },
    ],
    
    authentication: {
      type: process.env.AUTH_REQUIRED ? "oauth2" : "none",
      oauth2: process.env.AUTH_REQUIRED ? {
        tokenUrl: process.env.AUTH_TOKEN_URL,
        scopes: {
          read: "Read access to context and status",
          write: "Write access for prefetching",
          admin: "Administrative access",
        },
      } : undefined,
    },
    
    rateLimit: {
      requestsPerMinute: 60,
      requestsPerHour: 1000,
      burstLimit: 10,
    },
  };
}

function getToolScopes(toolName: string): string[] {
  const scopeMap: Record<string, string[]> = {
    hsa_get_context: ["read", "context"],
    hsa_detect_stack: ["read", "stack"],
    hsa_check_changes: ["read", "changes"],
    hsa_prefetch: ["write", "prefetch"],
    hsa_status: ["read", "status"],
    hsa_health: ["read", "health"],
  };
  return scopeMap[toolName] || ["read"];
}

// ============================================================
// CAPABILITY QUERIES
// ============================================================

export function supportsCapability(capability: keyof ServerCapabilities): boolean {
  return getServerMetadata().capabilities[capability];
}

export function getToolByName(name: string): ToolMetadata | undefined {
  return getServerMetadata().tools.find((t) => t.name === name);
}

export function listToolNames(): string[] {
  return getServerMetadata().tools.map((t) => t.name);
}

// ============================================================
// DISCOVERY HELPERS
// ============================================================

export function getOpenAPISpec(): object {
  const metadata = getServerMetadata();
  
  return {
    openapi: "3.1.0",
    info: {
      title: metadata.name,
      version: metadata.version,
      description: metadata.description,
    },
    servers: metadata.transports
      .filter((t) => t.type === "http")
      .map((t) => ({ url: t.url })),
    paths: Object.fromEntries(
      metadata.tools.map((tool) => [
        `/tools/${tool.name}`,
        {
          post: {
            summary: tool.description,
            requestBody: {
              content: {
                "application/json": {
                  schema: tool.inputSchema,
                },
              },
            },
            responses: {
              "200": { description: "Tool executed successfully" },
              "401": { description: "Unauthorized" },
              "500": { description: "Tool execution error" },
            },
          },
        },
      ])
    ),
  };
}
