/**
 * Socket client for the Blender add-on.
 *
 * Length-framed, token-authenticated, and deadline-bounded. The deadline is a
 * whole-operation budget rather than a per-read timeout: a socket read timeout
 * is meaningless here because the add-on does all its work in one burst, so a
 * stalled read and a slow render look identical and both would otherwise hang
 * until the harness gives up.
 */

import { connect, Socket } from 'net';
import { homedir } from 'os';
import { join, dirname } from 'path';
import { randomBytes } from 'crypto';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';

export const DEFAULT_PORT = 28782;
export const DEFAULT_TIMEOUT_MS = 60_000;
const MAX_FRAME_BYTES = 32 * 1024 * 1024;
const HEADER_BYTES = 4;

export class BlenderError extends Error {
  readonly detail?: string;
  constructor(message: string, detail?: string) {
    super(message);
    this.name = 'BlenderError';
    this.detail = detail;
  }
}

export interface ExecResult {
  ok: boolean;
  error?: string;
  result?: unknown;
  stdout: string;
  stdout_bytes: number;
  stdout_truncated: boolean;
  stdout_bytes_dropped: number;
  elapsed_ms?: number;
  traceback?: string;
}

export interface HealthResult {
  ok: boolean;
  protocol: number;
  stdout_cap_bytes: number;
  elapsed_ms?: number;
}

/**
 * Where the add-on looks for its port and token.
 *
 * The add-on runs inside Blender, which the user launched, so it cannot
 * inherit the bridge process's environment. A file is the only channel that
 * works in both directions, and mirrors what unity-bridge does with
 * HsaBridgeConfig.json.
 */
export function configPath(): string {
  // HSA_NOCKDEV_HOME is what the add-on reads too, so pointing both at a
  // scratch directory keeps a test run from republishing over the config a real
  // Blender is already using.
  return join(process.env.HSA_NOCKDEV_HOME || homedir(), '.nockdev', 'blender-bridge.json');
}

export interface BridgeConfig {
  port: number;
  token: string;
}

export function resolveConfig(): BridgeConfig {
  const envPort = process.env.HSA_BLENDER_PORT;
  const envToken = process.env.HSA_BLENDER_TOKEN;
  if (envToken) {
    return { port: envPort ? Number(envPort) : DEFAULT_PORT, token: envToken };
  }

  const path = configPath();
  if (existsSync(path)) {
    try {
      const parsed = JSON.parse(readFileSync(path, 'utf8')) as Partial<BridgeConfig>;
      if (parsed.port && parsed.token) {
        return { port: parsed.port, token: parsed.token };
      }
    } catch {
      // A corrupt file is reported by the caller as "no add-on found" rather
      // than crashing the bridge at import time.
    }
  }

  return { port: envPort ? Number(envPort) : DEFAULT_PORT, token: randomBytes(24).toString('base64url') };
}

/**
 * Publish the port and token where the add-on will read them.
 *
 * Written before the first request so an add-on that is already running can
 * pick the values up on its next register() without a Blender restart.
 */
export function publishConfig(config: BridgeConfig): string {
  const path = configPath();
  // Derived from the path rather than rebuilt from homedir(): the two disagree
  // whenever HSA_NOCKDEV_HOME is set, and a mkdir for the wrong directory
  // leaves the write failing with a bare ENOENT on a path that was never
  // created.
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(config, null, 2), 'utf8');
  return path;
}

/**
 * Read one frame, accumulating across chunks.
 *
 * A single 'data' event routinely carries the 4-byte header and the body
 * together, so a reader that takes exactly `count` bytes and unhooks drops
 * whatever arrived after them. One accumulator for the whole frame is the fix;
 * the alternative is a per-read remainder buffer, which is the same idea with
 * more places to get it wrong.
 */
function readFrame(sock: Socket, deadline: number): Promise<Buffer> {
  return new Promise((resolve, reject) => {
    let buffer: Buffer = Buffer.alloc(0);

    const cleanup = () => {
      clearTimeout(timer);
      sock.off('data', onData);
      sock.off('error', onError);
      sock.off('close', onClose);
    };

    const timer = setTimeout(() => {
      cleanup();
      reject(new BlenderError(`no complete frame within the deadline (${buffer.length} bytes so far)`, 'deadline'));
    }, Math.max(0, deadline - Date.now()));

    const onData = (chunk: Buffer) => {
      buffer = buffer.length === 0 ? chunk : Buffer.concat([buffer, chunk]);
      if (buffer.length < HEADER_BYTES) return;
      const length = buffer.readUInt32BE(0);
      if (length > MAX_FRAME_BYTES) {
        cleanup();
        reject(new BlenderError(`add-on declared a ${length}-byte frame, over the ${MAX_FRAME_BYTES} limit`));
        return;
      }
      if (buffer.length < HEADER_BYTES + length) return;
      const body = buffer.subarray(HEADER_BYTES, HEADER_BYTES + length);
      cleanup();
      resolve(body);
    };
    const onError = (err: Error) => {
      cleanup();
      reject(err);
    };
    const onClose = () => {
      cleanup();
      reject(new BlenderError(`connection closed with ${buffer.length} bytes of a frame outstanding`));
    };

    sock.on('data', onData);
    sock.on('error', onError);
    sock.on('close', onClose);
  });
}

export class BlenderClient {
  private readonly config: BridgeConfig;
  private readonly timeoutMs: number;

  constructor(config: BridgeConfig, timeoutMs: number = DEFAULT_TIMEOUT_MS) {
    this.config = config;
    this.timeoutMs = timeoutMs;
  }

  get port(): number {
    return this.config.port;
  }

  /**
   * One request, one framed reply.
   *
   * A refused connection is reported with the install steps rather than as a
   * bare ECONNREFUSED, because "connection refused" is the single most common
   * first failure and its cause is almost never the socket.
   */
  async request(command: string, params: Record<string, unknown> = {}): Promise<Record<string, unknown>> {
    const payload = Buffer.from(
      JSON.stringify({ token: this.config.token, command, params }),
      'utf8',
    );
    const header = Buffer.alloc(HEADER_BYTES);
    header.writeUInt32BE(payload.length, 0);

    return new Promise((resolve, reject) => {
      const deadline = Date.now() + this.timeoutMs;
      const sock = connect({ host: '127.0.0.1', port: this.config.port });
      let settled = false;

      const finish = (err: Error | null, value?: Record<string, unknown>) => {
        if (settled) return;
        settled = true;
        clearTimeout(connectTimer);
        sock.destroy();
        if (err) reject(err);
        else resolve(value ?? {});
      };

      const connectTimer = setTimeout(() => {
        finish(new BlenderError(`no reply from Blender on port ${this.config.port} within ${this.timeoutMs}ms`, 'deadline'));
      }, this.timeoutMs);

      sock.once('error', (err: NodeJS.ErrnoException) => {
        if (err.code === 'ECONNREFUSED') {
          finish(new BlenderError(
            `nothing is listening on 127.0.0.1:${this.config.port}`,
            'install the HSA Blender Bridge add-on and set HSA_BLENDER_TOKEN to the same value this bridge uses',
          ));
          return;
        }
        finish(new BlenderError(err.message, err.code));
      });

      sock.once('connect', async () => {
        try {
          sock.write(Buffer.concat([header, payload]));
          const body = await readFrame(sock, deadline);
          finish(null, JSON.parse(body.toString('utf8')) as Record<string, unknown>);
        } catch (err) {
          finish(err as Error);
        }
      });
    });
  }

  /**
   * Run Python and fail loudly.
   *
   * A reply of `{ok: false}` nested inside a successful call is the exact shape
   * that turns a failed script into a silent wrong answer, so it is raised here
   * rather than handed back to the caller to be inspected.
   */
  async exec(code: string, stdoutCapBytes?: number): Promise<ExecResult> {
    const params: Record<string, unknown> = { code };
    if (stdoutCapBytes !== undefined) params.stdout_cap_bytes = stdoutCapBytes;

    const reply = await this.request('execute_code', params);
    return reply as unknown as ExecResult;
  }

  async health(): Promise<HealthResult> {
    const reply = await this.request('health');
    return reply as unknown as HealthResult;
  }
}
