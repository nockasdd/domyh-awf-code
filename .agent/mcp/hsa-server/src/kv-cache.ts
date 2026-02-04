/**
 * HSA v6.0 — KV Cache
 * Precomputed key-value storage for attention optimization
 */

import { logger, metrics } from "./observability.js";

// ============================================================
// TYPES
// ============================================================

interface KVEntry {
  key: string;
  value: unknown;
  embedding?: number[];
  metadata: {
    createdAt: Date;
    accessCount: number;
    lastAccess: Date;
    size: number;
  };
}

interface KVCacheConfig {
  maxSize: number;
  maxMemory: number; // bytes
  ttlMs: number;
  precomputeOnStart: boolean;
}

// ============================================================
// KV CACHE IMPLEMENTATION
// ============================================================

const log = logger.child({ component: "kv-cache" });

const DEFAULT_CONFIG: KVCacheConfig = {
  maxSize: 5000,
  maxMemory: 100 * 1024 * 1024, // 100MB
  ttlMs: 7200000, // 2 hours
  precomputeOnStart: true,
};

class KVCache {
  private cache: Map<string, KVEntry> = new Map();
  private config: KVCacheConfig;
  private currentMemory = 0;
  
  constructor(config: Partial<KVCacheConfig> = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
  }
  
  /**
   * Estimate memory size of value
   */
  private estimateSize(value: unknown): number {
    const json = JSON.stringify(value);
    return json.length * 2; // UTF-16 chars
  }
  
  /**
   * Generate cache key with namespace
   */
  private makeKey(namespace: string, key: string): string {
    return `${namespace}:${key}`;
  }
  
  /**
   * Get value from cache
   */
  get<T>(namespace: string, key: string): T | null {
    const fullKey = this.makeKey(namespace, key);
    const entry = this.cache.get(fullKey);
    
    if (!entry) {
      metrics.cacheMisses.inc({ cache: "kv" });
      return null;
    }
    
    // Check TTL
    const age = Date.now() - entry.metadata.createdAt.getTime();
    if (age > this.config.ttlMs) {
      this.delete(namespace, key);
      metrics.cacheMisses.inc({ cache: "kv" });
      return null;
    }
    
    // Update access stats
    entry.metadata.accessCount++;
    entry.metadata.lastAccess = new Date();
    
    metrics.cacheHits.inc({ cache: "kv" });
    return entry.value as T;
  }
  
  /**
   * Set value in cache
   */
  set(namespace: string, key: string, value: unknown, embedding?: number[]): boolean {
    const size = this.estimateSize(value);
    
    // Check memory limit
    if (this.currentMemory + size > this.config.maxMemory) {
      this.evictByMemory(size);
    }
    
    // Check size limit
    if (this.cache.size >= this.config.maxSize) {
      this.evictLRU();
    }
    
    const fullKey = this.makeKey(namespace, key);
    
    // Remove old entry if exists
    if (this.cache.has(fullKey)) {
      const old = this.cache.get(fullKey)!;
      this.currentMemory -= old.metadata.size;
    }
    
    this.cache.set(fullKey, {
      key: fullKey,
      value,
      embedding,
      metadata: {
        createdAt: new Date(),
        accessCount: 1,
        lastAccess: new Date(),
        size,
      },
    });
    
    this.currentMemory += size;
    
    log.debug({ namespace, key, size }, "KV cached");
    return true;
  }
  
  /**
   * Delete entry
   */
  delete(namespace: string, key: string): boolean {
    const fullKey = this.makeKey(namespace, key);
    const entry = this.cache.get(fullKey);
    
    if (entry) {
      this.currentMemory -= entry.metadata.size;
      this.cache.delete(fullKey);
      return true;
    }
    
    return false;
  }
  
  /**
   * Check if key exists
   */
  has(namespace: string, key: string): boolean {
    return this.cache.has(this.makeKey(namespace, key));
  }
  
  /**
   * Get all keys in namespace
   */
  keys(namespace: string): string[] {
    const prefix = `${namespace}:`;
    return Array.from(this.cache.keys())
      .filter((k) => k.startsWith(prefix))
      .map((k) => k.slice(prefix.length));
  }
  
  /**
   * Clear namespace
   */
  clearNamespace(namespace: string): number {
    const prefix = `${namespace}:`;
    let count = 0;
    
    for (const [key, entry] of this.cache) {
      if (key.startsWith(prefix)) {
        this.currentMemory -= entry.metadata.size;
        this.cache.delete(key);
        count++;
      }
    }
    
    log.info({ namespace, count }, "Namespace cleared");
    return count;
  }
  
  /**
   * Evict LRU entry
   */
  private evictLRU(): void {
    let oldestKey: string | null = null;
    let oldestTime = Infinity;
    
    for (const [key, entry] of this.cache) {
      const score = entry.metadata.lastAccess.getTime() - entry.metadata.accessCount * 1000;
      if (score < oldestTime) {
        oldestTime = score;
        oldestKey = key;
      }
    }
    
    if (oldestKey) {
      const entry = this.cache.get(oldestKey)!;
      this.currentMemory -= entry.metadata.size;
      this.cache.delete(oldestKey);
      log.debug({ key: oldestKey }, "Evicted LRU");
    }
  }
  
  /**
   * Evict until memory available
   */
  private evictByMemory(needed: number): void {
    const entries = Array.from(this.cache.entries())
      .sort((a, b) => {
        const scoreA = a[1].metadata.lastAccess.getTime() - a[1].metadata.accessCount * 1000;
        const scoreB = b[1].metadata.lastAccess.getTime() - b[1].metadata.accessCount * 1000;
        return scoreA - scoreB;
      });
    
    let freed = 0;
    for (const [key, entry] of entries) {
      if (freed >= needed) break;
      
      this.currentMemory -= entry.metadata.size;
      freed += entry.metadata.size;
      this.cache.delete(key);
    }
    
    log.debug({ freed }, "Memory eviction complete");
  }
  
  /**
   * Precompute common values
   */
  async precompute(entries: { namespace: string; key: string; compute: () => Promise<unknown> }[]): Promise<number> {
    let computed = 0;
    
    for (const entry of entries) {
      if (!this.has(entry.namespace, entry.key)) {
        const value = await entry.compute();
        this.set(entry.namespace, entry.key, value);
        computed++;
      }
    }
    
    log.info({ computed, total: entries.length }, "Precomputation complete");
    return computed;
  }
  
  /**
   * Get cache stats
   */
  getStats(): object {
    return {
      entries: this.cache.size,
      maxSize: this.config.maxSize,
      memory: this.currentMemory,
      maxMemory: this.config.maxMemory,
      memoryUsage: ((this.currentMemory / this.config.maxMemory) * 100).toFixed(1) + "%",
      ttlMs: this.config.ttlMs,
    };
  }
  
  /**
   * Clear all entries
   */
  clear(): void {
    this.cache.clear();
    this.currentMemory = 0;
    log.info("Cache cleared");
  }
}

// ============================================================
// EXPORTS
// ============================================================

export const kvCache = new KVCache();

/**
 * Helper: Cache function result
 */
export async function cached<T>(
  namespace: string,
  key: string,
  compute: () => Promise<T>,
  ttl?: number
): Promise<T> {
  const existing = kvCache.get<T>(namespace, key);
  if (existing !== null) {
    return existing;
  }
  
  const value = await compute();
  kvCache.set(namespace, key, value);
  return value;
}
