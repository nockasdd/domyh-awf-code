/**
 * The handshake across a shared config file.
 *
 * fake_blender.py starts the add-on with no env, which is the state a real
 * Blender sits in when the IDE launched it before the bridge existed. The only
 * thing that can make the two sides agree then is the file the bridge
 * publishes, so this proves that path end to end rather than assuming it.
 *
 * Run: node test/handover.mjs
 */

import { spawn } from 'child_process';
import { existsSync, mkdtempSync, readFileSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';
import { dirname } from 'path';
import { fileURLToPath } from 'url';

const HERE = dirname(fileURLToPath(import.meta.url));
const BRIDGE_DIR = join(HERE, '..');
const PYTHON = process.env.HSA_TEST_PYTHON || 'python';

let passed = 0;
let failed = 0;
function check(name, condition, detail) {
  if (condition) {
    passed += 1;
    console.log(`  ok   ${name}`);
  } else {
    failed += 1;
    console.log(`  FAIL ${name}${detail !== undefined ? ` — ${JSON.stringify(detail)}` : ''}`);
  }
}

function waitFor(pattern, stream, ms, label) {
  return new Promise((resolve, reject) => {
    let buf = '';
    const timer = setTimeout(() => reject(new Error(`${label} did not start`)), ms);
    stream.on('data', (c) => {
      buf += c.toString();
      if (buf.includes(pattern)) {
        clearTimeout(timer);
        resolve(buf);
      }
    });
  });
}

async function main() {
  const home = mkdtempSync(join(tmpdir(), 'bb-handover-'));
  const configPath = join(home, '.nockdev', 'blender-bridge.json');
  const env = { ...process.env, HSA_NOCKDEV_HOME: home, HSA_DASHBOARD: 'false' };
  delete env.HSA_BLENDER_TOKEN;
  delete env.HSA_BLENDER_PORT;

  // The add-on, with no token of its own — it has to find one.
  const blender = spawn(PYTHON, [join(HERE, 'fake_blender.py'), '0', '', '5'], {
    stdio: ['ignore', 'pipe', 'pipe'],
    env,
  });
  const stdout = [];
  blender.stdout.on('data', (c) => stdout.push(c.toString()));
  blender.stderr.on('data', (c) => process.stderr.write(`[blender] ${c}`));
  await waitFor('FAKE_BLENDER_READY', blender.stdout, 15000, 'fake blender');
  check('the add-on starts with no token', true);

  // The bridge, told nothing except where the config lives.
  const bridge = spawn(process.execPath, ['--no-warnings', join(BRIDGE_DIR, 'dist', 'index.js')], {
    stdio: ['ignore', 'pipe', 'pipe'],
    env,
  });
  const stderr = [];
  bridge.stderr.on('data', (c) => stderr.push(c.toString()));
  bridge.stdout.resume();

  // Past the bridge's own 6s retry budget plus the add-on's 2s poll, so the
  // result is the settled one rather than a snapshot of a handshake still
  // running.
  await new Promise((r) => setTimeout(r, 12000));

  check('the bridge published a config file', existsSync(configPath), configPath);
  const published = existsSync(configPath) ? JSON.parse(readFileSync(configPath, 'utf8')) : {};
  check('the published port is a real port', published.port > 0, published.port);
  check('the published token is a real token', typeof published.token === 'string' && published.token.length >= 16, published.token?.length);

  const log = stderr.join('');
  const addOnLog = stdout.join('');
  // The add-on read the file only if it autostarted on the published port.
  const started = /listening on 127\.0\.0\.1:(\d+)/.exec(addOnLog) ?? null;
  check('the add-on listened on the published port', started?.[1] === String(published.port), {
    published: published.port, addOn: started?.[1] ?? null,
  });

  // Matching for the success line rather than the absence of a failure: an
  // empty log satisfies "no error mentioned", which passes even when the bridge
  // died before it said anything.
  check('the bridge completed the handshake', log.includes(' on "') && log.includes('Blender '), log.slice(0, 400));
  check('the add-on authenticated it', !log.includes('unauthorized'), log.slice(0, 400));

  bridge.kill();
  blender.kill();
  console.log(`\n${passed} passed, ${failed} failed`);
  process.exitCode = failed === 0 ? 0 : 1;
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
