/**
 * End-to-end: the built bridge over stdio, talking to the real add-on.
 *
 * The unit tests prove the add-on's logic and the envelope's math separately.
 * Neither proves the two are wired to the same protocol, which is the failure
 * a manifest rename or a field rename produces and nothing else catches.
 *
 * Run: node test/e2e.mjs
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

import { McpClient, call, counter, freePort, init, parse } from './harness.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const BRIDGE_DIR = join(HERE, '..');
const PYTHON = process.env.HSA_TEST_PYTHON || 'python';

async function main() {
  const t = counter();
  const check = t.check;
  const port = await freePort();
  const token = 'e2e-token-abc123';

  const blender = spawn(PYTHON, [join(HERE, 'fake_blender.py'), String(port), token, '120'], {
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const ready = await new Promise((resolve, reject) => {
    let buf = '';
    const timer = setTimeout(() => reject(new Error('fake blender did not start')), 15000);
    blender.stdout.on('data', (c) => {
      buf += c.toString();
      if (buf.includes('FAKE_BLENDER_READY')) {
        clearTimeout(timer);
        resolve(true);
      }
    });
    blender.stderr.on('data', (c) => process.stderr.write(`[blender] ${c}`));
  }).catch((e) => { throw e; });
  if (!ready) throw new Error('fake blender did not start');

  const bridge = spawn(process.execPath, ['--no-warnings', join(BRIDGE_DIR, 'dist', 'index.js')], {
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, HSA_BLENDER_PORT: String(port), HSA_BLENDER_TOKEN: token, HSA_DASHBOARD: 'false' },
  });
  const client = new McpClient(bridge);

  try {
    await init(client);
    console.log('tools');

    const listed = await client.request('tools/list', {});
    const names = listed.tools.map((t) => t.name).sort();
    check('all seven tools are exposed', names.length === 7, names);
    check('read tools are marked read-only', listed.tools.filter((t) => t.annotations.readOnlyHint).length === 6, names);
    const exec = listed.tools.find((t) => t.name === 'blender_execute_python');
    check('the escape hatch is the only mutating tool', exec && exec.annotations.readOnlyHint === false);

    console.log('health + scene');
    const health = parse(await call(client, 'blender_health'));
    check('health reports the protocol', health.data?.protocol === 1, health);
    check('health envelope is not truncated', health.meta?.truncated === false);

    const scene = parse(await call(client, 'blender_get_scene_info'));
    check('scene info names the version', scene.data?.blender === '4.2.1', scene.data?.blender);
    check('scene info returns 50 by default', scene.data?.objects_in_page?.length === 50, scene.data?.objects_in_page?.length);
    check('nothing was cut, the page was simply bounded', scene.meta?.truncated === false, scene.meta);
    check('total_items is the real scene size, not the page', scene.meta?.total_items === 120, scene.meta?.total_items);
    check('returned_items is what actually came back', scene.meta?.returned_items === 50, scene.meta?.returned_items);
    check('next_offset points past this page', scene.meta?.next_offset === 50, scene.meta?.next_offset);

    const tail = parse(await call(client, 'blender_get_scene_info', { offset: 100, limit: 50 }));
    check('the last page has no next_offset', tail.meta?.next_offset === null, tail.meta);
    check('the last page is not marked truncated', tail.meta?.truncated === false, tail.meta);
    check('the last page is short', tail.meta?.returned_items === 20, tail.meta?.returned_items);

    console.log('budget');
    const big = parse(await call(client, 'blender_execute_python', {
      code: "print('y' * 60000)\n_result = 'done'",
    }));
    check('stdout over the cap is cut', big.data?.stdout_truncated === true, big.data);
    check('the cut is reported, not hidden', big.data?.stdout_bytes_dropped > 0, big.data);
    check('the returned stdout respects the cap', big.data?.stdout_bytes <= 8000, big.data?.stdout_bytes);
    check('the script still completed', big.data?.result === 'done', big.data?.result);

    console.log('scene diff');
    const first = parse(await call(client, 'blender_scene_diff'));
    check('the first diff says it has no baseline', first.data?.first_call === true, first.data);
    const second = parse(await call(client, 'blender_scene_diff'));
    check('an unchanged scene diffs to nothing', second.data?.changes?.length === 0, second.data);
    check('the unchanged count covers the scene', second.data?.unchanged_count === 120, second.data?.unchanged_count);

    console.log('errors');
    const missing = parse(await call(client, 'blender_describe_object', { name: 'nope' }));
    check('a missing object is an error, not empty success', missing.status === 'error', missing);
    check('the error names the object', String(missing.meta?.note).includes('nope'), missing.meta);

    // A dead add-on must not read as a live scene report. The version, scene
    // and frame are cached at startup, so a Blender that closed since then used
    // to leave get_scene_info answering "unknown" and an object list from
    // nothing — a scene report for a scene that no longer exists.
    console.log('a closed blender');
    blender.kill();
    await new Promise((r) => setTimeout(r, 500));
    const afterDeath = parse(await call(client, 'blender_get_scene_info'));
    check('a closed blender is an error, not a scene report', afterDeath.status === 'error', afterDeath);
    check('the error says the add-on is gone', /add-on|connect|listening|ECONNREFUSED/i.test(String(afterDeath.meta?.note)), afterDeath.meta);

    const unknown = await call(client, 'blender_not_a_tool');
    check('an unknown tool returns an error envelope', parse(unknown).status === 'error');
  } finally {
    bridge.stdin.end();
    bridge.kill();
    blender.kill();
  }

  console.log(`\n${t.summary()}`);
  // exitCode rather than process.exit(): the latter cuts the process off while
  // stdout is still draining, so the summary can be lost and the run reported
  // as passing or failing at random depending on how the output was piped.
  process.exitCode = t.failed === 0 ? 0 : 1;
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
