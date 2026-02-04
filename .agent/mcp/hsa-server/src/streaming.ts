/**
 * HSA v5.0 — Streaming Resources
 * Real-time data feeds with backpressure handling
 * Follows 2026 MCP streaming patterns
 */

import { EventEmitter } from "events";
import { logger } from "./observability.js";
import type { HSAConfig } from "./config.js";

// ============================================================
// TYPES
// ============================================================

export interface StreamConfig {
  id: string;
  type: "file-changes" | "context-updates" | "metrics" | "logs";
  interval?: number; // ms
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

export interface StreamSubscription {
  id: string;
  streamId: string;
  callback: (event: StreamEvent) => void;
  createdAt: Date;
}

// ============================================================
// STREAM MANAGER
// ============================================================

const log = logger.child({ component: "streaming" });

class StreamManager extends EventEmitter {
  private streams = new Map<string, StreamInstance>();
  private subscriptions = new Map<string, StreamSubscription[]>();
  
  constructor() {
    super();
    this.setMaxListeners(100); // Allow many subscribers
  }
  
  createStream(config: StreamConfig): StreamInstance {
    if (this.streams.has(config.id)) {
      throw new Error(`Stream ${config.id} already exists`);
    }
    
    const stream = new StreamInstance(config, this);
    this.streams.set(config.id, stream);
    
    log.info({ streamId: config.id, type: config.type }, "Stream created");
    return stream;
  }
  
  getStream(id: string): StreamInstance | undefined {
    return this.streams.get(id);
  }
  
  subscribe(streamId: string, callback: (event: StreamEvent) => void): string {
    const stream = this.streams.get(streamId);
    if (!stream) {
      throw new Error(`Stream ${streamId} not found`);
    }
    
    const subscription: StreamSubscription = {
      id: `sub_${Date.now().toString(36)}`,
      streamId,
      callback,
      createdAt: new Date(),
    };
    
    const subs = this.subscriptions.get(streamId) || [];
    subs.push(subscription);
    this.subscriptions.set(streamId, subs);
    
    log.info({ subscriptionId: subscription.id, streamId }, "Subscription created");
    return subscription.id;
  }
  
  unsubscribe(subscriptionId: string): boolean {
    for (const [streamId, subs] of this.subscriptions) {
      const idx = subs.findIndex((s) => s.id === subscriptionId);
      if (idx !== -1) {
        subs.splice(idx, 1);
        log.info({ subscriptionId, streamId }, "Subscription removed");
        return true;
      }
    }
    return false;
  }
  
  publish(streamId: string, event: StreamEvent): void {
    const subs = this.subscriptions.get(streamId) || [];
    for (const sub of subs) {
      try {
        sub.callback(event);
      } catch (error) {
        log.error({ subscriptionId: sub.id, error }, "Subscription callback failed");
      }
    }
  }
  
  destroyStream(id: string): void {
    const stream = this.streams.get(id);
    if (stream) {
      stream.stop();
      this.streams.delete(id);
      this.subscriptions.delete(id);
      log.info({ streamId: id }, "Stream destroyed");
    }
  }
  
  listStreams(): StreamConfig[] {
    return Array.from(this.streams.values()).map((s) => s.config);
  }
}

// ============================================================
// STREAM INSTANCE
// ============================================================

class StreamInstance {
  public readonly config: StreamConfig;
  private manager: StreamManager;
  private buffer: StreamEvent[] = [];
  private sequence = 0;
  private intervalId?: NodeJS.Timeout;
  private paused = false;
  
  constructor(config: StreamConfig, manager: StreamManager) {
    this.config = config;
    this.manager = manager;
  }
  
  start(): void {
    if (this.config.interval) {
      this.intervalId = setInterval(() => {
        this.flush();
      }, this.config.interval);
    }
    log.info({ streamId: this.config.id }, "Stream started");
  }
  
  stop(): void {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    log.info({ streamId: this.config.id }, "Stream stopped");
  }
  
  push(data: unknown): boolean {
    const maxBuffer = this.config.maxBufferSize || 1000;
    const threshold = this.config.backpressureThreshold || 0.8;
    
    // Check backpressure
    if (this.buffer.length >= maxBuffer * threshold) {
      if (!this.paused) {
        this.paused = true;
        this.manager.emit("backpressure", { streamId: this.config.id, paused: true });
        log.warn({ streamId: this.config.id }, "Stream backpressure activated");
      }
    }
    
    if (this.buffer.length >= maxBuffer) {
      // Drop oldest events
      this.buffer.shift();
    }
    
    const event: StreamEvent = {
      id: `evt_${Date.now().toString(36)}`,
      type: this.config.type,
      timestamp: new Date(),
      data,
      sequence: this.sequence++,
    };
    
    this.buffer.push(event);
    
    // Immediate publish if no interval
    if (!this.config.interval) {
      this.flush();
    }
    
    return true;
  }
  
  flush(): void {
    while (this.buffer.length > 0) {
      const event = this.buffer.shift()!;
      this.manager.publish(this.config.id, event);
    }
    
    // Release backpressure
    if (this.paused) {
      this.paused = false;
      this.manager.emit("backpressure", { streamId: this.config.id, paused: false });
      log.info({ streamId: this.config.id }, "Stream backpressure released");
    }
  }
  
  getBufferSize(): number {
    return this.buffer.length;
  }
  
  isPaused(): boolean {
    return this.paused;
  }
}

// ============================================================
// GLOBAL INSTANCE
// ============================================================

export const streamManager = new StreamManager();

// ============================================================
// BUILT-IN STREAMS
// ============================================================

export function initializeBuiltInStreams(config: HSAConfig): void {
  // File changes stream
  const fileChangesStream = streamManager.createStream({
    id: "file-changes",
    type: "file-changes",
    interval: 1000,
    maxBufferSize: 500,
  });
  fileChangesStream.start();
  
  // Metrics stream
  const metricsStream = streamManager.createStream({
    id: "metrics",
    type: "metrics",
    interval: 5000,
    maxBufferSize: 100,
  });
  metricsStream.start();
  
  log.info("Built-in streams initialized");
}

// ============================================================
// SSE HELPER
// ============================================================

export function createSSEHandler(streamId: string) {
  return (req: any, res: any) => {
    res.setHeader("Content-Type", "text/event-stream");
    res.setHeader("Cache-Control", "no-cache");
    res.setHeader("Connection", "keep-alive");
    
    const subscriptionId = streamManager.subscribe(streamId, (event) => {
      res.write(`id: ${event.id}\n`);
      res.write(`event: ${event.type}\n`);
      res.write(`data: ${JSON.stringify(event.data)}\n\n`);
    });
    
    req.on("close", () => {
      streamManager.unsubscribe(subscriptionId);
    });
  };
}

// ============================================================
// MCP TOOL INTEGRATION
// ============================================================

export async function handleStreamingRequest(
  action: string,
  args: Record<string, unknown>,
  config: HSAConfig
): Promise<unknown> {
  switch (action) {
    case "create_stream":
      const stream = streamManager.createStream(args.config as StreamConfig);
      stream.start();
      return { streamId: stream.config.id };
      
    case "subscribe":
      // Note: HTTP subscriptions handled via SSE endpoint
      return { message: "Use SSE endpoint /stream/:id for subscriptions" };
      
    case "push":
      const targetStream = streamManager.getStream(args.streamId as string);
      if (!targetStream) throw new Error("Stream not found");
      return { success: targetStream.push(args.data) };
      
    case "list_streams":
      return streamManager.listStreams();
      
    case "destroy_stream":
      streamManager.destroyStream(args.streamId as string);
      return { success: true };
      
    default:
      throw new Error(`Unknown streaming action: ${action}`);
  }
}
