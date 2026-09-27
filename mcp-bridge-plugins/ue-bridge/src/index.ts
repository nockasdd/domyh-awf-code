import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { UnrealRestClient } from "./ue-rest-api.js";
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
 * Ensure the Native Python Server is deployed and running on port 30011.
 * Uses KismetSystemLibrary to find the project and auto-creates init_unreal.py.
 */
async function ensurePythonExecutor(): Promise<{ ready: boolean; message: string }> {
  // Step 1: Check if Native HTTP Server is already running on port 30011
  // Use a generous timeout — UE Game Thread may be busy
  try {
    const res = await fetch("http://127.0.0.1:30011/execute", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code_base64: Buffer.from('print("pong")').toString("base64") }),
      signal: AbortSignal.timeout(5000),
    });
    if (res.ok) {
      _pythonExecutorReady = true;
      return { ready: true, message: "Native Python Server is running on port 30011." };
    }
  } catch {
    // Not listening or timeout — fall through to deploy
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

    return {
      ready: false,
      message: `File deployed to ${targetFile}, but could not auto-execute. Please enable "Python Editor Script Plugin" in UE Editor and restart. The script will auto-load on next startup.`,
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
    // Ensure executor is deployed
    const setup = await ensurePythonExecutor();
    if (!setup.ready) {
      return { ok: false, error: setup.message, hint: "Enable 'Python Editor Script Plugin' in UE, RESTART editor, then retry." };
    }

    // Encode code to base64
    const codeBase64 = Buffer.from(code, "utf-8").toString("base64");

    try {
      const response = await fetch("http://127.0.0.1:30011/execute", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code_base64: codeBase64 }),
        signal: AbortSignal.timeout(60000)
      });
      
      const responseData = await response.json();
      return responseData;
    } catch (e: any) {
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

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
main().catch(console.error);

