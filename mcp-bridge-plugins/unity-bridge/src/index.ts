import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "unity-mcp-bridge",
  version: "2.0.0",
});

const UNITY_HTTP_BASE = process.env.UNITY_HTTP_URL ?? "http://127.0.0.1:30030";

async function unityRequest(
  endpoint: string,
  body?: Record<string, unknown>,
): Promise<unknown> {
  const url = `${UNITY_HTTP_BASE}${endpoint}`;
  const res = await fetch(url, {
    method: body ? "POST" : "GET",
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
    signal: AbortSignal.timeout(30_000),
  });
  if (!res.ok) {
    throw new Error(`Unity API Error: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

function tool(
  name: string,
  description: string,
  schema: Record<string, any>,
  endpoint: string,
) {
  server.tool(name, description, schema, async (params) => {
    try {
      const data = await unityRequest(endpoint, Object.keys(params).length > 0 ? params : undefined);
      return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
    } catch (e: any) {
      return { isError: true, content: [{ type: "text" as const, text: e.message }] };
    }
  });
}

// ══════════════════════════════════════════════════════════
//  Phase 0 — READ Tools
// ══════════════════════════════════════════════════════════

tool("unity_get_hierarchy", "Get the current scene hierarchy from Unity Editor", {}, "/hierarchy");

tool("unity_get_properties", "Get properties of a specific GameObject", {
  objectPath: z.string().describe("Path to the GameObject (e.g. 'Canvas/Panel/Button')"),
}, "/properties");

tool("unity_get_scene_info", "Get info about the active scene", {}, "/scene-info");

// ══════════════════════════════════════════════════════════
//  Phase 1 — OBJECT MANIPULATION Tools
// ══════════════════════════════════════════════════════════

tool("unity_create_object", "Create a new GameObject in the Unity scene", {
  name: z.string().describe("Name of the new GameObject"),
  primitiveType: z.enum(["None", "Cube", "Sphere", "Capsule", "Cylinder", "Plane", "Quad"]).optional()
    .describe("Optional primitive mesh type. Omit for empty object."),
  position: z.object({ x: z.number(), y: z.number(), z: z.number() }).optional()
    .describe("Initial world position"),
  parent: z.string().optional().describe("Path to parent GameObject"),
}, "/create-object");

tool("unity_add_component", "Add a component to a GameObject", {
  objectPath: z.string().describe("Path to the GameObject"),
  componentType: z.string().describe("Component type name (e.g. 'Rigidbody', 'BoxCollider', 'AudioSource')"),
}, "/add-component");

tool("unity_set_transform", "Set position, rotation, and/or scale of a GameObject", {
  objectPath: z.string().describe("Path to the GameObject"),
  position: z.object({ x: z.number(), y: z.number(), z: z.number() }).optional(),
  rotation: z.object({ x: z.number(), y: z.number(), z: z.number() }).optional().describe("Euler angles"),
  scale: z.object({ x: z.number(), y: z.number(), z: z.number() }).optional(),
}, "/set-transform");

tool("unity_set_property", "Set a serialized property on a GameObject or Component", {
  objectPath: z.string().describe("Path to the GameObject"),
  componentType: z.string().optional().describe("Component type to target (e.g. 'Camera'). Omit for GameObject."),
  propertyName: z.string().describe("Serialized property name (e.g. 'm_IsActive', 'mass')"),
  propertyValue: z.string().describe("Value as string. Colors: 'r,g,b,a'"),
}, "/set-property");

tool("unity_delete_object", "Delete a GameObject from the scene (with Undo support)", {
  objectPath: z.string().describe("Path to the GameObject to delete"),
}, "/delete-object");

tool("unity_duplicate_object", "Duplicate a GameObject", {
  objectPath: z.string().describe("Path to the GameObject to duplicate"),
}, "/duplicate-object");

tool("unity_set_parent", "Set parent-child relationship between GameObjects", {
  childPath: z.string().describe("Path to the child GameObject"),
  parentPath: z.string().optional().describe("Path to the new parent (omit to unparent to root)"),
}, "/set-parent");

tool("unity_rename_object", "Rename a GameObject", {
  objectPath: z.string().describe("Current path to the GameObject"),
  newName: z.string().describe("New name"),
}, "/rename-object");

tool("unity_play_mode", "Control Unity Play Mode", {
  action: z.enum(["play", "stop", "pause", "toggle"]).optional()
    .describe("Action to perform. Default: toggle"),
}, "/play-mode");

tool("unity_save_scene", "Save all open scenes", {}, "/save-scene");

tool("unity_new_scene", "Create a new empty scene", {
  name: z.string().optional().describe("Scene name"),
}, "/new-scene");

// ══════════════════════════════════════════════════════════
//  Phase 2 — ASSET PIPELINE Tools
// ══════════════════════════════════════════════════════════

tool("unity_create_material", "Create a new Material asset", {
  name: z.string().describe("Material name"),
  shaderName: z.string().optional().describe("Shader name (e.g. 'Standard', 'Universal Render Pipeline/Lit'). Default: auto-detect."),
  color: z.object({ r: z.number(), g: z.number(), b: z.number(), a: z.number().optional() }).optional()
    .describe("Base color RGBA (0-1 range)"),
  savePath: z.string().optional().describe("Save directory (default: Assets/Materials)"),
}, "/create-material");

tool("unity_create_prefab", "Save a GameObject as a Prefab asset", {
  objectPath: z.string().describe("Path to the scene GameObject"),
  savePath: z.string().optional().describe("Prefab save path (e.g. 'Assets/Prefabs/Player.prefab')"),
}, "/create-prefab");

tool("unity_instantiate_prefab", "Instantiate a Prefab into the scene", {
  prefabPath: z.string().describe("Asset path to the prefab (e.g. 'Assets/Prefabs/Player.prefab')"),
  name: z.string().optional().describe("Override instance name"),
  position: z.object({ x: z.number(), y: z.number(), z: z.number() }).optional(),
}, "/instantiate-prefab");

tool("unity_import_asset", "Import an external file into the Unity project", {
  sourcePath: z.string().describe("Absolute path to the source file"),
  destPath: z.string().describe("Unity project relative path (e.g. 'Assets/Textures/sky.png')"),
}, "/import-asset");

// unity_create_script — uses base64 for reliable code delivery
server.tool("unity_create_script",
  "Create a new C# script in the Unity project. Content is auto-encoded to base64 for reliable delivery.",
  {
    name: z.string().describe("Script/class name (no .cs extension)"),
    content: z.string().optional().describe("Full C# source code. Omit for default MonoBehaviour template."),
    savePath: z.string().optional().describe("Save directory (default: Assets/Scripts)"),
  },
  async (params) => {
    try {
      const body: Record<string, unknown> = { name: params.name };
      if (params.savePath) body.savePath = params.savePath;
      // Auto-encode content to base64 — avoids all JSON escaping issues
      if (params.content) {
        body.contentBase64 = Buffer.from(params.content, "utf-8").toString("base64");
      }
      const data = await unityRequest("/create-script", body);
      return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
    } catch (e: any) {
      return { isError: true, content: [{ type: "text" as const, text: e.message }] };
    }
  },
);

// ══════════════════════════════════════════════════════════
//  Phase 3 — AUTOMATION Tools (Play, Logs, Debug Loop)
// ══════════════════════════════════════════════════════════

tool("unity_get_logs", "Read Unity Editor Console logs. Returns log entries with type (error/warning/log), message, and stacktrace. Essential for auto-debug loop.", {
  limit: z.number().optional().describe("Max number of logs to return (default: 50, newest first)"),
  errorOnly: z.string().optional().describe("Set to 'true' to only return errors"),
  clear: z.string().optional().describe("Set to 'true' to clear the console after reading"),
}, "/get-logs");

// ── Existing ──────────────────────────────────────────────

tool("unity_execute_menu", "Execute a Unity Editor menu item", {
  menuPath: z.string().describe("Menu path like 'File/Save' or 'Assets/Refresh'"),
}, "/execute-menu");

tool("unity_recompile", "Trigger script recompilation", {}, "/recompile");

// ── Entry ─────────────────────────────────────────────────

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
main().catch(console.error);
