/**
 * The bridge test harness.
 *
 * Every bridge suite drives the same thing — a stdio MCP server speaking
 * JSON-RPC to a child process — so the client lives here rather than being
 * copied per suite. Two copies can drift on framing, and then two suites
 * disagree about whether the bridge is broken.
 */

import { createServer } from 'net';

export function freePort() {
  return new Promise((resolve, reject) => {
    const srv = createServer();
    srv.listen(0, '127.0.0.1', () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
    srv.on('error', reject);
  });
}

export class McpClient {
  constructor(child) {
    this.child = child;
    this.buffer = '';
    this.nextId = 1;
    this.pending = new Map();
    child.stdout.on('data', (chunk) => this.onData(chunk));
    child.stderr.on('data', (chunk) => process.stderr.write(`[bridge] ${chunk}`));
  }

  onData(chunk) {
    this.buffer += chunk.toString('utf8');
    for (;;) {
      const nl = this.buffer.indexOf('\n');
      if (nl === -1) return;
      const line = this.buffer.slice(0, nl).trim();
      this.buffer = this.buffer.slice(nl + 1);
      if (!line) continue;
      const msg = JSON.parse(line);
      const entry = this.pending.get(msg.id);
      if (entry) {
        this.pending.delete(msg.id);
        entry(msg);
      }
    }
  }

  request(method, params) {
    const id = this.nextId++;
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`${method} timed out`));
      }, 20000);
      this.pending.set(id, (msg) => {
        clearTimeout(timer);
        if (msg.error) reject(new Error(JSON.stringify(msg.error)));
        else resolve(msg.result);
      });
      this.child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id, method, params })}\n`);
    });
  }

  notify(method, params) {
    this.child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', method, params })}\n`);
  }
}

export function init(client) {
  client.notify('notifications/initialized');
  return client.request('initialize', {
    protocolVersion: '2024-11-05',
    capabilities: {},
    clientInfo: { name: 'hsa-bridge-test', version: '1.0.0' },
  });
}

export function call(client, name, args = {}) {
  return client.request('tools/call', { name, arguments: args });
}

export function parse(result) {
  return JSON.parse(result.content[0].text);
}

export function counter() {
  let passed = 0;
  let failed = 0;
  return {
    check(name, condition, detail) {
      if (condition) {
        passed += 1;
        console.log(`  ok   ${name}`);
      } else {
        failed += 1;
        console.log(`  FAIL ${name}${detail ? ` — ${JSON.stringify(detail)}` : ''}`);
      }
    },
    summary: () => `${passed} passed, ${failed} failed`,
    get failed() {
      return failed;
    },
  };
}
