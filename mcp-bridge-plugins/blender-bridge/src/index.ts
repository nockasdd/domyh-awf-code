#!/usr/bin/env node
/**
 * HSA Blender Bridge — MCP server over stdio.
 *
 * The only process in the chain that lives outside Blender. It owns the socket,
 * the tool schemas, and the byte budget; the add-on owns the scene.
 *
 * Tool descriptions carry the byte budget on purpose. A caller that does not
 * know a scene read can cost 24kB will ask for a full list and only find out
 * from the response, which is one turn too late.
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';

import { BlenderClient, BlenderError, publishConfig, resolveConfig, DEFAULT_TIMEOUT_MS } from './client.js';
import { BlenderTools, EXEC_OUTPUT_CAP } from './tools.js';
import { DEFAULT_BYTE_BUDGET, DEFAULT_PAGE_LIMIT, errorEnvelope } from './envelope.js';

const VERSION = '1.0.0';
const NAME = 'blender-hsa-bridge';
// Two poll cycles of the add-on's autostart timer, plus a margin.
const HANDSHAKE_RETRY_MS = 6_000;

const PAGE_SCHEMA = {
  offset: {
    type: 'number',
    description: `Zero-based index of the first item to return. Use meta.next_offset from the previous call to continue.`,
    default: 0,
  },
  limit: {
    type: 'number',
    description: `Maximum items to return (capped at 500). The byte budget can cut this lower.`,
    default: DEFAULT_PAGE_LIMIT,
  },
} as const;

interface ToolSpec {
  name: string;
  description: string;
  inputSchema: Record<string, unknown>;
  mutates?: boolean;
  run: (args: Record<string, unknown>) => Promise<unknown>;
}

function buildTools(tools: BlenderTools): ToolSpec[] {
  return [
    {
      name: 'blender_health',
      description: `Check the add-on is listening and report its protocol version and stdout cap. Costs nothing and runs no code.`,
      inputSchema: { type: 'object', properties: {} },
      run: () => tools.health(),
    },
    {
      name: 'blender_get_scene_info',
      description: `Blender version, active scene, current frame, and one page of object summaries (name, type, parent, transform, dimensions, modifier and material counts). Paged; check meta.truncated and meta.next_offset before treating it as the whole scene. Response is bounded to about ${DEFAULT_BYTE_BUDGET} bytes.`,
      inputSchema: { type: 'object', properties: { ...PAGE_SCHEMA } },
      run: (a) => tools.getSceneInfo(a.offset as number, a.limit as number),
    },
    {
      name: 'blender_list_objects',
      description: `List object summaries, optionally filtered by Blender type (MESH, CAMERA, LIGHT, EMPTY, CURVE). Paged the same way as blender_get_scene_info.`,
      inputSchema: {
        type: 'object',
        properties: {
          ...PAGE_SCHEMA,
          type: { type: 'string', description: 'Blender object type to filter by.' },
        },
      },
      run: (a) => tools.listObjects(a.offset as number, a.limit as number, a.type as string | undefined),
    },
    {
      name: 'blender_describe_object',
      description: `Full detail for one object: transform, modifiers, materials, mesh counts, children, and custom properties. Fails loudly if the object does not exist.`,
      inputSchema: {
        type: 'object',
        properties: { name: { type: 'string', description: 'Exact object name.' } },
        required: ['name'],
      },
      run: (a) => tools.describeObject(a.name as string),
    },
    {
      name: 'blender_get_selection',
      description: `Currently selected objects, the active object, and the interaction mode.`,
      inputSchema: { type: 'object', properties: {} },
      run: () => tools.getSelection(),
    },
    {
      name: 'blender_scene_diff',
      description: `What changed since the previous call in this bridge process: objects added, modified (transform, modifiers or materials), or removed. Costs what changed rather than the size of the scene, so it stays cheap on large files. The first call reports first_call: true and establishes the baseline.`,
      inputSchema: { type: 'object', properties: { ...PAGE_SCHEMA } },
      run: (a) => tools.sceneDiff(a.offset as number, a.limit as number),
    },
    {
      name: 'blender_execute_python',
      description: `Run arbitrary Python inside Blender with bpy in scope. Assign to _result to return a value. stdout is capped at the source and reported with stdout_truncated and stdout_bytes_dropped. Prefer the named tools for reads: they are cheaper and their output is structured.`,
      inputSchema: {
        type: 'object',
        properties: {
          code: { type: 'string', description: 'Python source to run.' },
          stdout_cap_bytes: { type: 'number', description: 'Lower the stdout cap for this call.', default: EXEC_OUTPUT_CAP },
        },
        required: ['code'],
      },
      mutates: true,
      run: (a) => tools.executePython(a.code as string, (a.stdout_cap_bytes as number) ?? EXEC_OUTPUT_CAP),
    },
  ];
}

function content(value: unknown) {
  return { content: [{ type: 'text' as const, text: JSON.stringify(value, null, 2) }] };
}

async function main(): Promise<void> {
  const config = resolveConfig();
  const path = publishConfig(config);
  process.stderr.write(`[blender-bridge] config published to ${path} (port ${config.port})\n`);

  const client = new BlenderClient(config, DEFAULT_TIMEOUT_MS);
  const tools = new BlenderTools(client);
  const specs = buildTools(tools);

  // Retry rather than probe once. A Blender that was already open learns the
  // port and token from the file this process just published, and its own poll
  // runs on a 2s interval — so a single attempt reports "no add-on" for a
  // Blender that is answering a moment later. The bounded wait is what makes
  // the line below a statement about the connection rather than about timing.
  const deadline = Date.now() + HANDSHAKE_RETRY_MS;
  let lastError: unknown = null;
  for (;;) {
    try {
      await tools.primeContext();
      process.stderr.write(`[blender-bridge] Blender ${tools.blenderVersion()} on "${tools.sceneName()}"\n`);
      lastError = null;
      break;
    } catch (err) {
      lastError = err;
      if (Date.now() >= deadline) break;
      await new Promise((r) => setTimeout(r, 500));
    }
  }

  if (lastError) {
    process.stderr.write(
      `[blender-bridge] no add-on on 127.0.0.1:${config.port}: ${(lastError as Error).message}\n` +
        '[blender-bridge] install src/addon/hsa_blender_addon.py, or set HSA_BLENDER_TOKEN to the add-on\'s token\n',
    );
  }

  const server = new Server(
    { name: NAME, version: VERSION },
    { capabilities: { tools: {} } },
  );

  server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: specs.map((s) => ({
      name: s.name,
      description: s.description,
      inputSchema: s.inputSchema,
      annotations: { title: s.name, readOnlyHint: !s.mutates, destructiveHint: Boolean(s.mutates) },
    })),
  }));

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const spec = specs.find((s) => s.name === request.params.name);
    if (!spec) {
      return content(errorEnvelope(`unknown tool ${request.params.name}`));
    }
    try {
      return content(await spec.run((request.params.arguments ?? {}) as Record<string, unknown>));
    } catch (err) {
      if (err instanceof BlenderError) {
        return content(errorEnvelope(err.message));
      }
      return content(errorEnvelope(`unexpected: ${(err as Error)?.message ?? String(err)}`));
    }
  });

  await server.connect(new StdioServerTransport());
  process.stderr.write('[blender-bridge] ready on stdio\n');
}

main().catch((err) => {
  process.stderr.write(`[blender-bridge] fatal: ${(err as Error).stack ?? String(err)}\n`);
  process.exit(1);
});
