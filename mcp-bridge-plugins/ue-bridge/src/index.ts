import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { UnrealRestClient } from "./ue-rest-api.js";
import { auditPath, logAttempt, logResult } from "./audit.js";
import * as fs from "fs";
import * as path from "path";
import { fileURLToPath } from "url";

const server = new McpServer({
  name: "ue-mcp-bridge",
  version: "2.0.0",
});

const restClient = new UnrealRestClient();

// ── Python Executor State ─────────────────────────────────
let _pythonExecutorReady = false;
const EXECUTOR_OBJECT_PATH = "/Script/PythonScriptPlugin.Default__HsaPythonExecutor";

// The executor runs inside the editor process, so HSA_BRIDGE_TOKEN on this
// server is not visible to it — the token has to be written to disk beside the
// project, in Saved/, which Unreal keeps out of version control. See
// init_unreal.py:_load_bridge_config.
const EXEC_HOST = process.env.HSA_UE_BRIDGE_HOST || "127.0.0.1";
const EXEC_PORT = Number(process.env.HSA_UE_BRIDGE_PORT || 30011);
const BRIDGE_TOKEN = process.env.HSA_BRIDGE_TOKEN || "";
const EXEC_URL = `http://${EXEC_HOST}:${EXEC_PORT}`;

function writeBridgeConfig(projectDir: string): string {
  const configDir = path.join(projectDir, "Saved", "HSA");
  fs.mkdirSync(configDir, { recursive: true });
  const configFile = path.join(configDir, "bridge_config.json");
  fs.writeFileSync(
    configFile,
    JSON.stringify({
      host: EXEC_HOST,
      port: EXEC_PORT,
      token: BRIDGE_TOKEN,
    }, null, 2),
    "utf-8",
  );
  // chmod after the write, not as a mode option: the mode is masked by the
  // process umask, and on Windows it is not applied at all, so the bearer token
  // would land world-readable.
  fs.chmodSync(configFile, 0o600);
  return configFile;
}

function wrapTool(
  name: string,
  description: string,
  schema: Record<string, any>,
  handler: (params: any) => Promise<any>,
) {
  server.tool(name, description, schema as any, async (params: any) => {
    try {
      const data = await handler(params);
      return { content: [{ type: "text" as const, text: JSON.stringify(data, null, 2) }] };
    } catch (e: any) {
      return { isError: true, content: [{ type: "text" as const, text: e.message }] };
    }
  });
}

// ══════════════════════════════════════════════════════════
//  READ Tools
// ══════════════════════════════════════════════════════════

wrapTool("ue_get_info",
  "Get Unreal Engine Remote Control API info and available endpoints",
  {},
  () => restClient.getInfo(),
);

wrapTool("ue_describe_object",
  "Get metadata, properties and functions of a UObject in Unreal Engine",
  {
    objectPath: z.string().describe("UE object path (e.g. '/Game/Maps/Main.Main:PersistentLevel.MyActor')"),
  },
  ({ objectPath }) => restClient.describeObject(objectPath),
);

wrapTool("ue_search_assets",
  "Search for assets in the Unreal Engine Asset Registry",
  {
    query: z.string().describe("Search query"),
    filterClass: z.string().optional().describe("Filter by class (e.g. 'StaticMesh', 'Material', 'Blueprint')"),
  },
  ({ query, filterClass }) => restClient.searchAssets(query, filterClass),
);

wrapTool("ue_get_property",
  "Read a property value from a UObject",
  {
    objectPath: z.string().describe("UE object path"),
    propertyName: z.string().describe("Property name to read"),
  },
  ({ objectPath, propertyName }) => restClient.getProperty(objectPath, propertyName),
);

wrapTool("ue_set_property",
  "Set a property on a UObject in Unreal Engine",
  {
    objectPath: z.string().describe("UE object path"),
    propertyName: z.string().describe("Property name to set"),
    propertyValue: z.union([z.number(), z.boolean(), z.string(), z.record(z.any())])
      .describe("New value"),
  },
  ({ objectPath, propertyName, propertyValue }) =>
    restClient.setProperty(objectPath, propertyName, propertyValue),
);

// ══════════════════════════════════════════════════════════
//  FUNCTION CALL Tools (Phase 1)
// ══════════════════════════════════════════════════════════

wrapTool("ue_call_function",
  "Call any Blueprint-callable UFunction on a UObject. This is the most powerful tool — can spawn actors, modify levels, etc.",
  {
    objectPath: z.string().describe("Path to the UObject to call the function on"),
    functionName: z.string().describe("Name of the function to call"),
    parameters: z.record(z.any()).optional().describe("Function parameters as key-value pairs"),
  },
  ({ objectPath, functionName, parameters }) =>
    restClient.callFunction(objectPath, functionName, parameters ?? {}),
);

wrapTool("ue_spawn_actor",
  "Spawn an actor of a given class at a location in the current level. Uses EditorActorSubsystem (UE 4.24+).",
  {
    className: z.string().describe("Actor class path (e.g. '/Script/Engine.PointLight', '/Script/Engine.StaticMeshActor', '/Game/BP/MyActor.MyActor_C')"),
    location: z.object({
      X: z.number().optional().default(0),
      Y: z.number().optional().default(0),
      Z: z.number().optional().default(0),
    }).optional().describe("World location (default: 0,0,0)"),
    rotation: z.object({
      Pitch: z.number().optional().default(0),
      Yaw: z.number().optional().default(0),
      Roll: z.number().optional().default(0),
    }).optional().describe("World rotation (default: 0,0,0)"),
  },
  async ({ className, location, rotation }) => {
    // Verified correct path for EditorActorSubsystem (UE 4.24+/5.x)
    const SUBSYSTEM = "/Script/UnrealEd.Default__EditorActorSubsystem";
    return restClient.callFunction(SUBSYSTEM, "SpawnActorFromClass", {
      ActorClass: className,
      Location: location ?? { X: 0, Y: 0, Z: 0 },
      Rotation: rotation ?? { Pitch: 0, Yaw: 0, Roll: 0 },
    });
  },
);

wrapTool("ue_set_actor_transform",
  "Set the transform (location, rotation, scale) of an actor",
  {
    objectPath: z.string().describe("Actor object path"),
    location: z.object({ X: z.number(), Y: z.number(), Z: z.number() }).optional(),
    rotation: z.object({ Pitch: z.number(), Yaw: z.number(), Roll: z.number() }).optional(),
    scale: z.object({ X: z.number(), Y: z.number(), Z: z.number() }).optional(),
  },
  async ({ objectPath, location, rotation, scale }) => {
    const results: any[] = [];
    if (location) {
      results.push(await restClient.setProperty(objectPath, "RelativeLocation", location));
    }
    if (rotation) {
      results.push(await restClient.setProperty(objectPath, "RelativeRotation", rotation));
    }
    if (scale) {
      results.push(await restClient.setProperty(objectPath, "RelativeScale3D", scale));
    }
    return { ok: true, updated: results.length, results };
  },
);

wrapTool("ue_delete_actor",
  "Delete an actor from the level",
  {
    objectPath: z.string().describe("Actor object path to delete"),
  },
  async ({ objectPath }) => {
    const SUBSYSTEM = "/Script/UnrealEd.Default__EditorActorSubsystem";
    return restClient.callFunction(SUBSYSTEM, "DestroyActor", {
      ActorToDestroy: objectPath,
    });
  },
);

wrapTool("ue_list_actors",
  "List all actors in the current level",
  {
    classFilter: z.string().optional().describe("Filter by actor class name"),
  },
  async ({ classFilter }) => {
    const SUBSYSTEM = "/Script/UnrealEd.Default__EditorActorSubsystem";
    const result = await restClient.callFunction(SUBSYSTEM, "GetAllLevelActors", {});
    if (classFilter && result?.ReturnValue) {
      result.ReturnValue = result.ReturnValue.filter((a: string) =>
        a.toLowerCase().includes(classFilter.toLowerCase())
      );
    }
    return result;
  },
);

wrapTool("ue_batch",
  "Execute multiple UFunction calls in a single batch request",
  {
    requests: z.array(z.object({
      objectPath: z.string(),
      functionName: z.string(),
      params: z.record(z.any()).optional(),
    })).describe("List of function calls to batch"),
  },
  ({ requests }) => restClient.batch(requests),
);

// ══════════════════════════════════════════════════════════
//  Phase 2 — PYTHON EXECUTION (Zero-Click Auto-Setup)
// ══════════════════════════════════════════════════════════

/**
 * Whether the user has agreed to let code run in the editor.
 *
 * Deliberately not a tool. Every tool on this server is reachable by the model,
 * so a `ue_execute_python_consent` tool would be consent the model grants
 * itself, and the call would be indistinguishable from the execution it
 * authorises. An environment variable is the only channel here the model
 * cannot write to.
 */
const EXEC_CONSENT = process.env.HSA_UE_EXEC_CONSENT || "";
const CONSENT_GRANTED = ["1", "true", "yes", "on"].includes(EXEC_CONSENT.toLowerCase());
const CONSENT_REFUSED =
  "HSA_UE_EXEC_CONSENT is not set on the ue-bridge, so ue_execute_python is refused. " +
  "This is the one control between a generated code string and arbitrary Python running " +
  "in the editor as you. Set HSA_UE_EXEC_CONSENT=1 in the MCP server environment and " +
  "restart it to allow execution. Every call is appended to " + auditPath() + " either way.";

/**
 * Ensure the Native Python Server is deployed and running.
 * Uses KismetSystemLibrary to find the project and auto-creates init_unreal.py.
 */
async function ensurePythonExecutor(): Promise<{ ready: boolean; message: string }> {
  // Step 1: Liveness. /health is unauthenticated and does not execute, so a
  // probe no longer occupies a Game Thread slot or shows up in the exec log.
  try {
    const res = await fetch(`${EXEC_URL}/health`, {
      signal: AbortSignal.timeout(2000),
    });
    if (res.ok) {
      const health = await res.json();
      if (health.auth_required && !BRIDGE_TOKEN) {
        return {
          ready: false,
          message: "UE Python server is running with auth enabled, but HSA_BRIDGE_TOKEN is unset on this bridge. Set the same token in both places and restart the editor.",
        };
      }
      _pythonExecutorReady = true;
      return { ready: true, message: `Native Python Server is running on port ${EXEC_PORT}.` };
    }
  } catch {
    // Not listening — fall through to deploy
  }

  // Step 2: Server not running → deploy init_unreal.py into UE project
  try {
    // Get the UE project directory via Remote Control API
    const projResult = await restClient.callFunction(
      "/Script/Engine.Default__KismetSystemLibrary",
      "GetProjectDirectory",
      {}
    );
    const projectDir = projResult?.ReturnValue;
    if (!projectDir) {
      return { ready: false, message: "Could not determine UE project directory. Is Remote Control running?" };
    }

    if (!BRIDGE_TOKEN) {
      return {
        ready: false,
        message: "HSA_BRIDGE_TOKEN is not set. The executor refuses to start without it, because anything local could otherwise run arbitrary Python in the editor.",
      };
    }

    // Create Content/Python directory
    const pythonDir = path.join(projectDir, "Content", "Python");
    if (!fs.existsSync(pythonDir)) {
      fs.mkdirSync(pythonDir, { recursive: true });
    }

    // Copy init_unreal.py from our resources
    const targetFile = path.join(pythonDir, "init_unreal.py");
    const __filename = fileURLToPath(import.meta.url);
    const __dirname = path.dirname(__filename);
    let sourceFile = path.resolve(__dirname, "..", "resources", "init_unreal.py");
    if (!fs.existsSync(sourceFile)) {
      sourceFile = path.resolve(__dirname, "..", "..", "resources", "init_unreal.py");
    }

    if (!fs.existsSync(sourceFile)) {
      return { ready: false, message: `Executor stub not found at ${sourceFile}. Package may be incomplete.` };
    }

    fs.copyFileSync(sourceFile, targetFile);
    const configFile = writeBridgeConfig(projectDir);

    return {
      ready: false,
      message: `File deployed to ${targetFile} (config: ${configFile}), but could not auto-execute. Please enable "Python Editor Script Plugin" in UE Editor and restart. The script will auto-load on next startup.`,
    };
  } catch (e: any) {
    return { ready: false, message: `Auto-setup failed: ${e.message}` };
  }
}

wrapTool("ue_execute_python",
  "Execute Python code inside Unreal Engine Editor. Auto-deploys the executor stub on first call (zero-click setup). The Python code has full access to the 'unreal' module.",
  {
    code: z.string().describe("Python source code to execute. Has access to 'unreal' module. Example: unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight, unreal.Vector(0,0,300))"),
  },
  async ({ code }) => {
    if (!CONSENT_GRANTED) {
      logAttempt(code, "refused", CONSENT_REFUSED);
      return { ok: false, error: CONSENT_REFUSED };
    }

    // Ensure executor is deployed
    const setup = await ensurePythonExecutor();
    if (!setup.ready) {
      logAttempt(code, "refused", setup.message);
      return { ok: false, error: setup.message, hint: "Enable 'Python Editor Script Plugin' in UE, RESTART editor, then retry." };
    }

    // Encode code to base64
    const codeBase64 = Buffer.from(code, "utf-8").toString("base64");

    try {
      const response = await fetch(`${EXEC_URL}/execute`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${BRIDGE_TOKEN}`,
        },
        body: JSON.stringify({ code_base64: codeBase64 }),
        signal: AbortSignal.timeout(60000)
      });

      const responseData = await response.json();
      if (response.status === 401) {
        logAttempt(code, "refused", "token rejected by the editor");
        return {
          ok: false,
          error: "UE Python server rejected the token. HSA_BRIDGE_TOKEN must be identical on the bridge and in the UE project (Saved/HSA/bridge_config.json).",
        };
      }
      // Logged here rather than in the editor: the editor's record cannot be
      // trusted to cover a task that timed out, because the thread that would
      // write it is the one that is stuck.
      logResult(code, responseData);
      return responseData;
    } catch (e: any) {
      logAttempt(code, "err", e.message);
      return { ok: false, error: `Failed to connect to UE Python Server: ${e.message}` };
    }
  },
);

wrapTool("ue_python_status",
  "Check if the Python executor is deployed and active in UE Editor",
  {},
  async () => {
    return ensurePythonExecutor();
  },
);

// ── Entry ─────────────────────────────────────────────────

// On stderr, not stdout: stdout is the MCP transport, and a stray line there
// corrupts the protocol stream.
if (!CONSENT_GRANTED) {
  console.error(
    `[ue-bridge] ue_execute_python is refused: HSA_UE_EXEC_CONSENT is unset. ` +
    `Set it to 1 to allow. Attempts are still logged to ${auditPath()}.`,
  );
}

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
main().catch(console.error);

