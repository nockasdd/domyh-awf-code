/**
 * HSA v6.0 — Optimization Module
 * Unified interface for all optimization features
 */

import { semanticCache, requestCache } from "./cache.js";
import { getRelevantTools, getAllTools, estimateToolTokens } from "./tool-filter.js";
import { compressContext, smartCompress, estimateTokens } from "./compression.js";
import { kvCache, cached } from "./kv-cache.js";
import { submitJob, getJob, listJobs, getQueueStats } from "./async-exec.js";
import { logger, metrics } from "./observability.js";
import type { HSAConfig } from "./config.js";

// ============================================================
// TYPES
// ============================================================

export interface OptimizationConfig {
  enableSemanticCache: boolean;
  enableRequestCache: boolean;
  enableToolFiltering: boolean;
  enableCompression: boolean;
  enableKVCache: boolean;
  enableAsync: boolean;
  maxTokens: number;
}

export interface OptimizationStats {
  semantic: object;
  request: object;
  kv: object;
  filter: object;
  async: object;
  totalTokensSaved: number;
}

// ============================================================
// DEFAULT CONFIG
// ============================================================

const log = logger.child({ component: "optimization" });

const DEFAULT_CONFIG: OptimizationConfig = {
  enableSemanticCache: true,
  enableRequestCache: true,
  enableToolFiltering: true,
  enableCompression: true,
  enableKVCache: true,
  enableAsync: true,
  maxTokens: 8000,
};

let config: OptimizationConfig = { ...DEFAULT_CONFIG };

// ============================================================
// CONFIGURATION
// ============================================================

/**
 * Initialize optimization with config
 */
export function initOptimization(cfg: Partial<OptimizationConfig> = {}): void {
  config = { ...DEFAULT_CONFIG, ...cfg };
  
  log.info({
    semantic: config.enableSemanticCache,
    request: config.enableRequestCache,
    filter: config.enableToolFiltering,
    compression: config.enableCompression,
    kv: config.enableKVCache,
    async: config.enableAsync,
  }, "Optimization initialized");
}

// ============================================================
// UNIFIED CACHE INTERFACE
// ============================================================

/**
 * Try to get cached response (semantic or exact match)
 */
export function getCachedResponse(
  tool: string,
  args: Record<string, unknown>
): unknown | null {
  // Try request cache first (exact match)
  if (config.enableRequestCache) {
    const exact = requestCache.get(tool, args);
    if (exact) return exact;
  }
  
  // Try semantic cache (similar queries)
  if (config.enableSemanticCache) {
    const query = `${tool}:${JSON.stringify(args)}`;
    const similar = semanticCache.findSimilar(query);
    if (similar) return similar.response;
  }
  
  // Try KV cache if applicable
  if (config.enableKVCache) {
    const kv = kvCache.get(tool, JSON.stringify(args));
    if (kv) return kv;
  }
  
  return null;
}

/**
 * Store response in appropriate caches
 */
export function cacheResponse(
  tool: string,
  args: Record<string, unknown>,
  response: unknown,
  cacheTypes: ("request" | "semantic" | "kv")[] = ["request"]
): void {
  const query = `${tool}:${JSON.stringify(args)}`;
  
  if (cacheTypes.includes("request") && config.enableRequestCache) {
    requestCache.set(tool, args, response);
  }
  
  if (cacheTypes.includes("semantic") && config.enableSemanticCache) {
    semanticCache.store(query, response);
  }
  
  if (cacheTypes.includes("kv") && config.enableKVCache) {
    kvCache.set(tool, JSON.stringify(args), response);
  }
}

// ============================================================
// TOOL OPTIMIZATION
// ============================================================

/**
 * Get optimized tool list for context
 */
export function getOptimizedTools(context?: string): { tools: unknown[]; tokensSaved: number } {
  if (!config.enableToolFiltering || !context) {
    const all = getAllTools();
    return { tools: all, tokensSaved: 0 };
  }
  
  const result = getRelevantTools(context);
  const allTokens = estimateToolTokens(getAllTools());
  const filteredTokens = estimateToolTokens(result.tools);
  
  return {
    tools: result.tools,
    tokensSaved: allTokens - filteredTokens,
  };
}

// ============================================================
// CONTEXT OPTIMIZATION
// ============================================================

/**
 * Optimize context for token efficiency
 */
export function optimizeContext(
  content: string,
  maxTokens?: number
): { content: string; ratio: number; method: string } {
  if (!config.enableCompression) {
    return { content, ratio: 0, method: "none" };
  }
  
  const result = compressContext(content, {
    maxTokens: maxTokens || config.maxTokens,
  });
  
  metrics.compressionRatio.observe(result.ratio);
  
  return {
    content: result.compressed,
    ratio: result.ratio,
    method: result.method,
  };
}

/**
 * Optimize multiple files
 */
export function optimizeFiles(
  files: { path: string; content: string }[],
  maxTokens?: number
): { path: string; content: string; compressed: boolean }[] {
  if (!config.enableCompression) {
    return files.map((f) => ({ ...f, compressed: false }));
  }
  
  return smartCompress(files, maxTokens || config.maxTokens);
}

// ============================================================
// ASYNC EXECUTION
// ============================================================

export { submitJob, getJob, listJobs, getQueueStats };
export { cached };

// ============================================================
// STATS
// ============================================================

/**
 * Get comprehensive optimization stats
 */
export function getOptimizationStats(): OptimizationStats {
  return {
    semantic: semanticCache.getStats(),
    request: requestCache.getStats(),
    kv: kvCache.getStats(),
    filter: { enabled: config.enableToolFiltering },
    async: getQueueStats(),
    totalTokensSaved: 0, // Track over time
  };
}

/**
 * Clear all caches
 */
export function clearAllCaches(): void {
  semanticCache.clear();
  requestCache.clear();
  kvCache.clear();
  log.info("All caches cleared");
}

/**
 * Get config
 */
export function getConfig(): OptimizationConfig {
  return { ...config };
}
