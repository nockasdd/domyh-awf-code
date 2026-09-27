/**
 * A Blender that comes up after the bridge gave up waiting.
 *
 * The bridge reads the version, the scene and the frame once, at startup. The
 * add-on reads the config file the bridge publishes, so either side can be
 * second: an IDE harness that launches the bridge first has the bridge waiting
 * for a port that is not bound yet, and the wait is bounded. Once that bound
 * expires, a cached context that was never filled is a scene report that calls
 * a live Blender "unknown" — the objects come back real and the header does
 * not, which reads as data rather than as a missed handshake.
 *
 * Run: node test/late_addon.mjs
 */

import { spawn } from 'child_process';
import { existsSync, mkdtempSync, readFileSync } from 'fs';
import { tmpdir } from 'os';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

import { McpClient, call, counter, freePort, init, parse } from './harness.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const BRIDGE_DIR = join(HERE, '..');
const PYTHON = process.env.HSA_TEST_PYTHON || 'python';

/** Null once `ms` runs out, rather than a rejection the caller must catch. */
function waitForLog(pattern, chunks, ms) {
  return new Promise((resolve) => {
    const seen = () => chunks.join('');
    if (pattern.test(seen())) {
      resolve(true);
      return;
    }
    const timer = setTimeout(() => resolve(null), ms);
    const poll = setInterval(() => {
      if (pattern.test(seen())) {
        clearTimeout(timer);
        clearInterval(poll);
        resolve(true);
      }
    }, 100);
  });
}

async function main() {
  const t = counter();
  const home = mkdtempSync(join(tmpdir(), 'bb-late-'));
  const configPath = join(home, '.nockdev', 'blender-bridge.json');
  const env = { ...process.env, HSA_NOCKDEV_HOME: home, HSA_DASHBOARD: 'false' };
  delete env.HSA_BLENDER_TOKEN;
  // Pinned rather than left to default: the default port is where a real
  // Blender is listening, and a test that lands there gets "unauthorized" from
  // it instead of an answer from its own stand-in.
  env.HSA_BLENDER_PORT = String(await freePort());

  // The bridge goes first, knowing nothing about any Blender. This is the
  // order an IDE harness produces when it starts the MCP server before the
  // user opens Blender.
  const bridge = spawn(process.execPath, ['--no-warnings', join(BRIDGE_DIR, 'dist', 'index.js')], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env,
  });
  const client = new McpClient(bridge);
  const stderr = [];
  bridge.stderr.on('data', (c) => {
    stderr.push(c.toString());
    process.stderr.write(`[bridge] ${c}`);
  });

  let blender = null;
  try {
    await init(client);
    t.check('the bridge serves before any Blender exists', true);

    const published = existsSync(configPath) ? JSON.parse(readFileSync(configPath, 'utf8')) : {};
    t.check('it published a port for the add-on to read', published.port > 0, published);

    const before = parse(await call(client, 'blender_get_scene_info'));
    t.check('no add-on is an error, not a scene report', before.status === 'error', before);
    t.check('the error points at the port', /127\.0\.0\.1|listening/i.test(String(before.meta?.note)), before.meta);

    // Blender now opens, and picks the port and token off disk the way a real
    // one does — which is the whole reason the bridge publishes them.
    console.log('a blender that arrives late');
    blender = spawn(PYTHON, [join(HERE, 'fake_blender.py'), String(published.port), published.token, '5'], {
      stdio: ['ignore', 'pipe', 'pipe'],
      env,
    });
    const ready = await new Promise((resolve, reject) => {
      let buf = '';
      const timer = setTimeout(() => reject(new Error('fake blender did not start')), 15000);
      blender.stdout.on('data', (c) => {
        buf += c.toString();
        if (buf.includes('FAKE_BLENDER_READY')) {
          clearTimeout(timer);
          resolve(buf);
        }
      });
      blender.stderr.on('data', (c) => process.stderr.write(`[blender] ${c}`));
    });
    t.check('the add-on came up on the published port', /FAKE_BLENDER_READY/.test(ready), ready.slice(0, 200));

    const after = parse(await call(client, 'blender_get_scene_info'));
    t.check('the live Blender is reachable', after.status === 'ok', after);
    t.check('the scene names the version, not "unknown"', after.data?.blender === '4.2.1', after.data?.blender);
    t.check('the scene is named, not "unknown"', after.data?.scene === 'TestScene', after.data?.scene);
    t.check('the frame is real, not 0', after.data?.frame_current === 1, after.data?.frame_current);
    t.check('the objects are the real scene', after.data?.objects_in_page?.length === 5, after.data?.objects_in_page?.length);

    // The poll is what fills the cache without a call, so its own log line is
    // the only thing that proves it is running at all — the read above primes
    // on demand and would pass either way.
    const pickedUp = await waitForLog(/Blender 4\.2\.1/, stderr, 10000);
    t.check('the bridge says it picked the Blender up', pickedUp !== null, stderr.join('').slice(-400));
  } finally {
    bridge.stdin.end();
    bridge.kill();
    if (blender) blender.kill();
  }

  console.log(`\n${t.summary()}`);
  process.exitCode = t.failed === 0 ? 0 : 1;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
