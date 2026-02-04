/**
 * HSA v6.0 — Async Tool Execution
 * Non-blocking tool execution for better performance
 * Prepares for Nov 2025 MCP spec changes
 */

import { logger, metrics, startTimer } from "./observability.js";
import type { HSAConfig } from "./config.js";

// ============================================================
// TYPES
// ============================================================

export interface AsyncJob {
  id: string;
  tool: string;
  args: Record<string, unknown>;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  result?: unknown;
  error?: string;
  createdAt: Date;
  startedAt?: Date;
  completedAt?: Date;
  progress?: number;
}

export interface JobOptions {
  timeout?: number;
  priority?: "low" | "normal" | "high";
  retries?: number;
  onProgress?: (progress: number) => void;
}

// ============================================================
// JOB QUEUE
// ============================================================

const log = logger.child({ component: "async-exec" });
const jobs = new Map<string, AsyncJob>();
const jobQueue: string[] = [];
let isProcessing = false;

const DEFAULT_TIMEOUT = 30000; // 30s
const MAX_CONCURRENT = 3;
let activeJobs = 0;

/**
 * Generate job ID
 */
function generateJobId(): string {
  return `job_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`;
}

/**
 * Submit async job
 */
export function submitJob(
  tool: string,
  args: Record<string, unknown>,
  executor: (args: Record<string, unknown>, config: HSAConfig) => Promise<unknown>,
  config: HSAConfig,
  options: JobOptions = {}
): AsyncJob {
  const jobId = generateJobId();
  
  const job: AsyncJob = {
    id: jobId,
    tool,
    args,
    status: "pending",
    createdAt: new Date(),
    progress: 0,
  };
  
  jobs.set(jobId, job);
  
  // Add to queue based on priority
  if (options.priority === "high") {
    jobQueue.unshift(jobId);
  } else {
    jobQueue.push(jobId);
  }
  
  log.debug({ jobId, tool }, "Job submitted");
  
  // Start processing if not already
  processQueue(executor, config, options);
  
  return job;
}

/**
 * Process job queue
 */
async function processQueue(
  executor: (args: Record<string, unknown>, config: HSAConfig) => Promise<unknown>,
  config: HSAConfig,
  options: JobOptions
): Promise<void> {
  if (isProcessing || activeJobs >= MAX_CONCURRENT) return;
  
  isProcessing = true;
  
  while (jobQueue.length > 0 && activeJobs < MAX_CONCURRENT) {
    const jobId = jobQueue.shift();
    if (!jobId) break;
    
    const job = jobs.get(jobId);
    if (!job || job.status !== "pending") continue;
    
    activeJobs++;
    executeJob(job, executor, config, options).finally(() => {
      activeJobs--;
      // Continue processing
      processQueue(executor, config, options);
    });
  }
  
  isProcessing = false;
}

/**
 * Execute single job
 */
async function executeJob(
  job: AsyncJob,
  executor: (args: Record<string, unknown>, config: HSAConfig) => Promise<unknown>,
  config: HSAConfig,
  options: JobOptions
): Promise<void> {
  const timer = startTimer();
  
  job.status = "running";
  job.startedAt = new Date();
  
  log.info({ jobId: job.id, tool: job.tool }, "Job started");
  
  const timeout = options.timeout || DEFAULT_TIMEOUT;
  let retries = options.retries || 0;
  
  while (retries >= 0) {
    try {
      const result = await Promise.race([
        executor(job.args, config),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error("Timeout")), timeout)
        ),
      ]);
      
      job.status = "completed";
      job.result = result;
      job.completedAt = new Date();
      job.progress = 100;
      
      const duration = timer.end();
      metrics.toolDuration.observe({ tool: job.tool }, duration);
      metrics.toolCalls.inc({ tool: job.tool, status: "success" });
      
      log.info({ jobId: job.id, duration: Math.round(duration * 1000) }, "Job completed");
      
      options.onProgress?.(100);
      return;
      
    } catch (error) {
      retries--;
      
      if (retries < 0) {
        job.status = "failed";
        job.error = error instanceof Error ? error.message : String(error);
        job.completedAt = new Date();
        
        metrics.toolCalls.inc({ tool: job.tool, status: "error" });
        log.error({ jobId: job.id, error: job.error }, "Job failed");
      } else {
        log.warn({ jobId: job.id, retriesLeft: retries }, "Retrying job");
        await new Promise((r) => setTimeout(r, 1000)); // Wait 1s before retry
      }
    }
  }
}

/**
 * Get job status
 */
export function getJob(jobId: string): AsyncJob | undefined {
  return jobs.get(jobId);
}

/**
 * Cancel job
 */
export function cancelJob(jobId: string): boolean {
  const job = jobs.get(jobId);
  
  if (!job) return false;
  
  if (job.status === "pending") {
    job.status = "cancelled";
    job.completedAt = new Date();
    
    const idx = jobQueue.indexOf(jobId);
    if (idx !== -1) {
      jobQueue.splice(idx, 1);
    }
    
    log.info({ jobId }, "Job cancelled");
    return true;
  }
  
  return false;
}

/**
 * List all jobs
 */
export function listJobs(status?: AsyncJob["status"]): AsyncJob[] {
  const allJobs = Array.from(jobs.values());
  
  if (status) {
    return allJobs.filter((j) => j.status === status);
  }
  
  return allJobs;
}

/**
 * Clean completed jobs older than max age
 */
export function cleanupJobs(maxAgeMs = 3600000): number {
  const cutoff = Date.now() - maxAgeMs;
  let removed = 0;
  
  for (const [id, job] of jobs) {
    if (
      (job.status === "completed" || job.status === "failed" || job.status === "cancelled") &&
      job.completedAt &&
      job.completedAt.getTime() < cutoff
    ) {
      jobs.delete(id);
      removed++;
    }
  }
  
  log.info({ removed }, "Job cleanup complete");
  return removed;
}

/**
 * Get queue stats
 */
export function getQueueStats(): object {
  const allJobs = Array.from(jobs.values());
  
  return {
    total: allJobs.length,
    pending: allJobs.filter((j) => j.status === "pending").length,
    running: allJobs.filter((j) => j.status === "running").length,
    completed: allJobs.filter((j) => j.status === "completed").length,
    failed: allJobs.filter((j) => j.status === "failed").length,
    queueLength: jobQueue.length,
    activeJobs,
    maxConcurrent: MAX_CONCURRENT,
  };
}

// Periodic cleanup
setInterval(() => {
  cleanupJobs();
}, 600000); // Every 10 minutes
