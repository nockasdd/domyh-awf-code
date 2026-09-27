/**
 * Schema-based tools.
 *
 * The alternative is `execute_blender_code` for everything, which is why most
 * Blender MCP setups are expensive: the model writes a script, the script
 * prints a repr, and the model reads a repr. Each of those steps loses
 * structure and adds prose. Naming the shape instead makes the common reads
 * cheap and leaves `exec` for the genuinely open-ended case.
 *
 * Pagination is decided inside the generated script rather than after the fact.
 * The socket would otherwise carry the whole scene first and cut it second,
 * which bounds the response but not the cost of producing it.
 */

import { BlenderClient, BlenderError } from './client.js';
import {
  Budget,
  DEFAULT_PAGE_LIMIT,
  Envelope,
  MAX_PAGE_LIMIT,
  byteLength,
  clipText,
  errorEnvelope,
  measure,
  page,
  withPage,
} from './envelope.js';

export const EXEC_OUTPUT_CAP = 8_000;

export interface ObjectSummary {
  name: string;
  type: string;
  parent: string | null;
  location: number[];
  dimensions: number[];
  modifiers: number;
  materials: string[];
  hidden: boolean;
}

function pyList(values: number[]): string {
  return `[${values.map((v) => Number(v.toFixed(6))).join(', ')}]`;
}

function pyStr(value: string): string {
  return `'${value.replace(/\\/g, '\\\\').replace(/'/g, "\\'")}'`;
}

/**
 * The fields a diff is computed over.
 *
 * Name and type identify; the rest is what a modelling step actually changes.
 * A diff over names alone would report "nothing changed" for a moved object,
 * which is the case that matters most here.
 */
const FINGERPRINT_KEYS = ['type', 'location', 'dimensions', 'scale', 'rotation', 'modifiers', 'materials'] as const;

function fingerprint(o: ObjectSummary): string {
  return JSON.stringify(FINGERPRINT_KEYS.map((k) => (o as unknown as Record<string, unknown>)[k]));
}

/**
 * Where the next page starts, or null when this one reached the end.
 *
 * The real total, not the page length: reporting a next_offset when the page
 * happened to be the last one makes a caller loop for a page that never comes.
 */
function nextOffset(offset: number, returned: number, total: number): number | null {
  const end = offset + returned;
  return end < total ? end : null;
}

export function keyOf(o: ObjectSummary): string {
  return `${o.type}:${o.name}`;
}

export class SceneSnapshot {
  private baseline: Map<string, string> | null = null;
  private baselineScene: string | null = null;

  get hasBaseline(): boolean {
    return this.baseline !== null;
  }

  get capturedAt(): string | null {
    return this.baselineScene;
  }

  /**
   * Compare against the previous call, then become the new baseline.
   *
   * First call has nothing to compare against and says so rather than
   * reporting an empty diff, which would read as "nothing changed".
   */
  diff(objects: ObjectSummary[]): {
    first_call: boolean;
    added: ObjectSummary[];
    removed: ObjectSummary[];
    changed: ObjectSummary[];
    unchanged_count: number;
    total_items: number;
  } {
    const next = new Map(objects.map((o) => [keyOf(o), fingerprint(o)]));

    if (this.baseline === null) {
      this.baseline = next;
      this.baselineScene = new Date().toISOString();
      return { first_call: true, added: [], removed: [], changed: [], unchanged_count: 0, total_items: next.size };
    }

    const added: ObjectSummary[] = [];
    const changed: ObjectSummary[] = [];
    let unchanged = 0;

    for (const o of objects) {
      const before = this.baseline.get(keyOf(o));
      if (before === undefined) added.push(o);
      else if (before !== fingerprint(o)) changed.push(o);
      else unchanged += 1;
    }

    const removedKeys = [...this.baseline.keys()].filter((k) => !next.has(k));
    const removed = removedKeys
      .map((k) => {
        const [type, ...rest] = k.split(':');
        return { name: rest.join(':'), type } as ObjectSummary;
      })
      .filter((o) => this.baseline!.has(keyOf(o)));

    this.baseline = next;
    this.baselineScene = new Date().toISOString();

    return { first_call: false, added, removed, changed, unchanged_count: unchanged, total_items: next.size };
  }

  reset(): void {
    this.baseline = null;
    this.baselineScene = null;
  }
}

export class BlenderTools {
  private readonly client: BlenderClient;
  readonly snapshot = new SceneSnapshot();

  constructor(client: BlenderClient) {
    this.client = client;
  }

  /**
   * Run a generated script and reject a failed one.
   *
   * `{ok: false}` inside a successful call is the shape that turns a failed
   * script into a silent wrong answer, so it is raised at the only place every
   * tool passes through.
   */
  private async run(code: string, cap = EXEC_OUTPUT_CAP): Promise<{ result: unknown; stdout: string; stdout_truncated: boolean; stdout_bytes_dropped: number; elapsed_ms?: number }> {
    const reply = await this.client.exec(code, cap);
    if (!reply.ok) {
      throw new BlenderError(reply.error ?? 'script failed', reply.stdout?.trim() || reply.traceback);
    }
    return {
      result: reply.result,
      stdout: reply.stdout,
      stdout_truncated: reply.stdout_truncated,
      stdout_bytes_dropped: reply.stdout_bytes_dropped,
      elapsed_ms: reply.elapsed_ms,
    };
  }

  private objectScript(where: string, offset: number, limit: number): string {
    // Substituted, not string-concatenated at the top: exec() requires the
    // import at column 0, and an indented one is a SyntaxError the caller
    // would see as a Blender problem.
    return [
      'import bpy',
      where,
      '_rows = [',
      '    {',
      '        "name": o.name,',
      '        "type": o.type,',
      '        "parent": o.parent.name if o.parent else None,',
      '        "location": [round(v, 6) for v in o.location],',
      '        "dimensions": [round(v, 6) for v in o.dimensions],',
      '        "scale": [round(v, 6) for v in o.scale],',
      '        "rotation": [round(v, 6) for v in o.rotation_euler],',
      '        "modifiers": len(o.modifiers),',
      '        "materials": [m.name if m else None for m in getattr(o.data, "materials", [])],',
      '        "hidden": o.hide_viewport,',
      '    }',
      '    for o in _src',
      ']',
      `_result = {"objects": _rows[${offset}:${offset + limit}], "total_items": len(_rows)}`,
    ].join('\n');
  }

  async health(): Promise<Envelope<Record<string, unknown>>> {
    const health = await this.client.health();
    return withPage({ ...health }, 1, 1, null, measure(health));
  }

  async getSceneInfo(offset = 0, limit = DEFAULT_PAGE_LIMIT): Promise<Envelope<Record<string, unknown>>> {
    const all = await this.run(this.objectScript('_src = list(bpy.data.objects)', offset, Math.min(limit, MAX_PAGE_LIMIT)));
    const rows = (all.result as { objects: ObjectSummary[]; total_items: number }).objects;
    const total = (all.result as { total_items: number }).total_items;

    // The object list above already proves an add-on is answering, so an empty
    // context here means this Blender arrived after the startup handshake gave
    // up — not that there is nothing to report. Filling it on the read is what
    // keeps the version and the scene from staying "unknown" beside a real
    // object list, and costs one extra call only on the first read of a session.
    if (this.version === null) {
      await this.primeContext();
    }

    const info = {
      blender: this.blenderVersion(),
      scene: this.sceneName(),
      frame_current: this.frameCurrent(),
      objects_in_page: rows,
    };

    return withPage(info, total, rows.length, nextOffset(offset, rows.length, total), measure(info));
  }

  async listObjects(offset = 0, limit = DEFAULT_PAGE_LIMIT, type?: string): Promise<Envelope<{ objects: ObjectSummary[] }>> {
    const where = type
      ? `_src = [o for o in bpy.data.objects if o.type == ${pyStr(type)}]`
      : '_src = list(bpy.data.objects)';
    const all = await this.run(this.objectScript(where, offset, limit));
    const rows = (all.result as { objects: ObjectSummary[]; total_items: number }).objects;
    const total = (all.result as { total_items: number }).total_items;

    const budget: Budget = { bytes: byteLength(JSON.stringify(rows)), truncated: false, bytes_returned: byteLength(JSON.stringify(rows)) };
    return withPage({ objects: rows }, total, rows.length, nextOffset(offset, rows.length, total), budget);
  }

  async describeObject(name: string): Promise<Envelope<Record<string, unknown>>> {
    const out = await this.run([
      'import bpy',
      `_obj = bpy.data.objects.get(${pyStr(name)})`,
      'if _obj is None:',
      `    _result = {"error": "no object named " + ${pyStr(name)}}`,
      'else:',
      '    _data = getattr(_obj, "data", None)',
      '    _result = {',
      '        "name": _obj.name,',
      '        "type": _obj.type,',
      '        "parent": _obj.parent.name if _obj.parent else None,',
      '        "location": [round(v, 6) for v in _obj.location],',
      '        "rotation_euler": [round(v, 6) for v in _obj.rotation_euler],',
      '        "scale": [round(v, 6) for v in _obj.scale],',
      '        "dimensions": [round(v, 6) for v in _obj.dimensions],',
      '        "hidden": _obj.hide_viewport,',
      '        "modifiers": [{"name": m.name, "type": m.type} for m in _obj.modifiers],',
      '        "materials": [m.name if m else None for m in getattr(_data, "materials", [])],',
      '        "custom_properties": {k: str(_obj[k])[:200] for k in _obj.keys() if not k.startswith("_RNA")},',
      '        "mesh": None if _data is None or not hasattr(_data, "vertices") else {',
      '            "vertices": len(_data.vertices),',
      '            "edges": len(_data.edges),',
      '            "polygons": len(_data.polygons),',
      '        },',
      '        "children": [c.name for c in _obj.children],',
      '    }',
    ].join('\n'));
    const data = out.result as Record<string, unknown>;
    if (data && typeof data === 'object' && 'error' in data) {
      throw new BlenderError(String(data.error));
    }
    return { status: 'ok', data, meta: { truncated: false, bytes_returned: byteLength(JSON.stringify(data)) } };
  }

  async getSelection(): Promise<Envelope<{ selected: string[]; active: string | null; mode: string }>> {
    const out = await this.run([
      'import bpy',
      '_view = bpy.context.view_layer',
      '_active = _view.objects.active',
      '_result = {',
      '    "selected": [o.name for o in _view.objects if o.select_get()],',
      '    "active": _active.name if _active else None,',
      '    "mode": bpy.context.mode,',
      '}',
    ].join('\n'));
    const data = out.result as { selected: string[]; active: string | null; mode: string };
    return withPage(data, data.selected.length, data.selected.length, null, measure(data));
  }

  /**
   * What changed since the last call.
   *
   * Costs O(changed) to read instead of O(scene), which is the difference
   * between checking a 4000-object file and being unable to check one.
   */
  async sceneDiff(offset = 0, limit = DEFAULT_PAGE_LIMIT): Promise<Envelope<Record<string, unknown>>> {
    const listed = await this.listObjects(0, MAX_PAGE_LIMIT);
    const all = (listed.data as { objects: ObjectSummary[] }).objects;
    const diff = this.snapshot.diff(all);

    const changes = [
      ...diff.added.map((o) => ({ change: 'added', object: o })),
      ...diff.changed.map((o) => ({ change: 'modified', object: o })),
      ...diff.removed.map((o) => ({ change: 'removed', object: o })),
    ];

    const p = page(changes, offset, limit);
    const data = {
      first_call: diff.first_call,
      baseline: this.snapshot.capturedAt,
      changes: p.items,
      unchanged_count: diff.unchanged_count,
      note: diff.first_call
        ? 'no previous snapshot in this bridge process; this call established the baseline'
        : undefined,
    };
    return withPage(data, changes.length, p.items.length, p.nextOffset, {
      bytes: byteLength(JSON.stringify(data)),
      truncated: p.truncated,
      bytes_returned: byteLength(JSON.stringify(data)),
    });
  }

  /**
   * The escape hatch.
   *
   * Marked as mutating in the manifest so the caller has to say it means it,
   * and the stdout is capped at the source with what was dropped reported.
   */
  async executePython(code: string, stdoutCapBytes = EXEC_OUTPUT_CAP): Promise<Envelope<Record<string, unknown>>> {
    if (!code || !code.trim()) {
      throw new BlenderError('code is required');
    }
    const out = await this.run(code, stdoutCapBytes);
    const clipped = clipText(out.stdout, stdoutCapBytes);
    const data = {
      result: out.result ?? null,
      stdout: clipped.text,
      stdout_truncated: out.stdout_truncated,
      stdout_bytes: clipped.bytes_returned,
      stdout_bytes_dropped: out.stdout_bytes_dropped,
      elapsed_ms: out.elapsed_ms,
    };
    return withPage(data, 1, 1, null, measure(data));
  }

  // Filled in by the health probe so a scene report carries the version that
  // produced it; a diff taken across a Blender restart is not a valid diff.
  private version: string | null = null;
  private scene: string | null = null;
  private frame: number | null = null;

  blenderVersion(): string { return this.version ?? 'unknown'; }
  sceneName(): string { return this.scene ?? 'unknown'; }
  private frameCurrent(): number { return this.frame ?? 0; }

  async primeContext(): Promise<void> {
    const out = await this.run([
      'import bpy',
      '_result = {',
      '    "blender": bpy.app.version_string,',
      '    "scene": bpy.context.scene.name,',
      '    "frame": bpy.context.scene.frame_current,',
      '}',
    ].join('\n'));
    const data = out.result as { blender: string; scene: string; frame: number };
    this.version = data.blender;
    this.scene = data.scene;
    this.frame = data.frame;
  }
}

export { errorEnvelope };
