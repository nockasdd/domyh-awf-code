/**
 * HSA v6.0 — Core Types
 * Shared type definitions across all modules
 */

// ============================================================
// CONFIGURATION TYPES
// ============================================================

export interface HSAConfig {
  projectPath: string;
  scriptsPath: string;
  pythonPath: string;
  cacheDir: string;
}

export interface ServerConfig {
  name: string;
  version: string;
  port: number;
  host: string;
  logLevel: string;
}

// ============================================================
// TOOL TYPES
// ============================================================

export interface ToolResult {
  success: boolean;
  data?: unknown;
  error?: string;
  duration?: number;
}

export interface ToolMetrics {
  calls: number;
  errors: number;
  avgDuration: number;
  lastCall: Date | null;
}

// ============================================================
// HEALTH TYPES
// ============================================================

export type HealthStatus = "healthy" | "degraded" | "unhealthy";

export interface ComponentHealth {
  name: string;
  status: HealthStatus;
  message?: string;
  latency?: number;
}

export interface HealthReport {
  status: HealthStatus;
  uptime: number;
  version: string;
  components: ComponentHealth[];
  timestamp: Date;
}

// ============================================================
// CACHE TYPES
// ============================================================

export interface CacheStats {
  hits: number;
  misses: number;
  size: number;
  hitRate: number;
}

export interface CacheEntry<T = unknown> {
  key: string;
  value: T;
  createdAt: Date;
  expiresAt: Date;
  accessCount: number;
}

// ============================================================
// AUTH TYPES
// ============================================================

export interface AuthContext {
  valid: boolean;
  userId?: string;
  scopes?: string[];
  expiresAt?: Date;
  method?: "jwt" | "apikey" | "none";
  error?: string;
}

export interface AuthConfig {
  required: boolean;
  issuer?: string;
  audience?: string;
  jwksUrl?: string;
  secret?: string;
  apiKeys?: string[];
}

// ============================================================
// MULTI-AGENT TYPES
// ============================================================

export type AgentType = "primary" | "specialist" | "reviewer" | "coordinator";
export type AgentStatus = "idle" | "working" | "waiting" | "completed";
export type TaskType = "analysis" | "coding" | "testing" | "review" | "research";
export type TaskStatus = "pending" | "assigned" | "in-progress" | "completed" | "failed";

export interface Agent {
  id: string;
  name: string;
  type: AgentType;
  capabilities: string[];
  status: AgentStatus;
  currentTask?: string;
}

export interface Task {
  id: string;
  description: string;
  type: TaskType;
  status: TaskStatus;
  assignedTo?: string;
  result?: unknown;
  dependencies?: string[];
  createdAt: Date;
  completedAt?: Date;
}

export interface Squad {
  id: string;
  name: string;
  agents: Agent[];
  tasks: Task[];
  coordinator: string;
  status: "forming" | "active" | "completing" | "disbanded";
  createdAt: Date;
}

// ============================================================
// STREAMING TYPES
// ============================================================

export type StreamType = "file-changes" | "context-updates" | "metrics" | "logs";

export interface StreamConfig {
  id: string;
  type: StreamType;
  interval?: number;
  maxBufferSize?: number;
  backpressureThreshold?: number;
}

export interface StreamEvent {
  id: string;
  type: string;
  timestamp: Date;
  data: unknown;
  sequence: number;
}

// ============================================================
// OBSERVABILITY TYPES
// ============================================================

export interface TraceContext {
  requestId: string;
  traceId: string;
  spanId: string;
  parentSpanId?: string;
}

export interface LogContext {
  component: string;
  requestId?: string;
  tool?: string;
  duration?: number;
  error?: Error;
}

// ============================================================
// REGISTRY TYPES
// ============================================================

export interface ServerMetadata {
  name: string;
  version: string;
  description: string;
  capabilities: {
    tools: boolean;
    streaming: boolean;
    multiAgent: boolean;
  };
  tools: ToolInfo[];
  transports: TransportInfo[];
  authentication?: AuthInfo;
}

export interface ToolInfo {
  name: string;
  description: string;
  scopes: string[];
}

export interface TransportInfo {
  type: "stdio" | "http" | "websocket";
  config?: Record<string, unknown>;
}

export interface AuthInfo {
  methods: ("jwt" | "apikey" | "oauth2")[];
  tokenUrl?: string;
  scopes?: Record<string, string>;
}

// ============================================================
// UTILITY TYPES
// ============================================================

export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};

export type AsyncFunction<T = unknown> = (...args: unknown[]) => Promise<T>;

export interface Result<T, E = Error> {
  success: boolean;
  data?: T;
  error?: E;
}
