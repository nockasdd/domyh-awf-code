---
library: plugin-unreal-engine
version: 1
latest: true
category: mcp-plugin
target_app: Unreal Engine 4.26 / 5.x (Editor)
transport: REST http://127.0.0.1:30010 + WebSocket ws://127.0.0.1:30020
plugin_type: Built-in (Remote Control API plugin — no custom C++ needed)
last_updated: 2026-03-27
---

# plugin-unreal-engine — HSA MCP Bridge for Unreal Engine

> Full Unreal Engine Remote Control API reference: HTTP endpoints, WebSocket message types, Preset system, batch calls, TypeScript MCP bridge implementation, and logic flow.

---

## 1. Setup — Enable Remote Control

Unreal has a **built-in** Remote Control system. No custom plugin compilation needed.

```ini
# DefaultEngine.ini (project or Engine config)
[/Script/RemoteControl.RemoteControlSettings]
RemoteControlHttpServerPort=30010
RemoteControlWebSocketServerPort=30020
bRemoteControlAllowForceQuitting=True
```

Or via Editor: **Edit → Plugins → search "Remote Control API"** → Enable both:
- **Remote Control API** — HTTP + WebSocket server
- **Remote Control UI** — Editor panel for creating presets

```bash
# Verify server is running after launching UE Editor:
curl http://127.0.0.1:30010/remote/info
```

---

## 2. Architecture

```
LLM Agent
  │  MCP tool call
  ▼
MCP Bridge (TypeScript)
  │
  ├─ REST: POST http://127.0.0.1:30010/remote/...
  │
  └─ WebSocket: ws://127.0.0.1:30020
       │  {"MessageName":"http","RequestId":N,"Parameters":{"Url":"/remote/...","Verb":"PUT","Body":{...}}}
       │
       ▼
  Unreal Editor (Main Thread — Remote Control handles threading internally)
       │  Read/Write property on UObject
       │  Call UFUNCTION on UObject
       │  Manage Remote Control Presets
       ▼
  Return JSON response
```

**Key difference:** REST calls block until completion. WebSocket calls are async but support push events (preset.changed) that REST cannot do.

---

## 3. HTTP Endpoints (Full)

### 3.1. Remote Info

```http
GET /remote/info
```
Returns all available HTTP routes + descriptions.

```json
{
  "HttpRoutes": [
    {"Path": "/remote/info",              "Verb": "Get",    "Description": "..."},
    {"Path": "/remote/object/property",   "Verb": "Get",    "Description": "..."},
    {"Path": "/remote/object/property",   "Verb": "Put",    "Description": "..."},
    {"Path": "/remote/object/call",       "Verb": "Put",    "Description": "..."},
    {"Path": "/remote/batch",             "Verb": "Put",    "Description": "..."},
    {"Path": "/remote/preset/{name}/describe",  "Verb": "Get", "Description": "..."},
    {"Path": "/remote/preset/{name}/property",  "Verb": "Put", "Description": "..."}
  ]
}
```

### 3.2. Read Object Property

```http
GET /remote/object/property
Content-Type: application/json

{
  "ObjectPath": "/Game/Maps/Level01.Level01:PersistentLevel.BP_Player_C_0",
  "PropertyName": "Health",
  "access": "READ_ACCESS"
}
```

Response:
```json
{
  "Health": 85.0
}
```

### 3.3. Write Object Property

```http
PUT /remote/object/property
Content-Type: application/json

{
  "ObjectPath": "/Game/Maps/Level01.Level01:PersistentLevel.BP_Player_C_0",
  "PropertyName": "Health",
  "PropertyValue": { "Health": 100.0 },
  "access": "WRITE_ACCESS"
}
```

### 3.4. Call Function on Object

```http
PUT /remote/object/call
Content-Type: application/json

{
  "ObjectPath": "/Script/Engine.Default__KismetSystemLibrary",
  "FunctionName": "PrintString",
  "Parameters": {
    "InString": "Hello from HSA MCP!",
    "bPrintToScreen": true,
    "bPrintToLog": true,
    "TextColor": {"R":0,"G":255,"B":0,"A":255},
    "Duration": 5.0
  },
  "GenerateTransaction": false
}
```

### 3.5. Batch Call (Multiple Operations in One Request)

```http
PUT /remote/batch
Content-Type: application/json

{
  "Requests": [
    {
      "RequestId": "req_1",
      "URL": "/remote/object/property",
      "Verb": "GET",
      "Body": {
        "ObjectPath": "/Game/Level01.Level01:PersistentLevel.BP_Player_C_0",
        "PropertyName": "Health",
        "access": "READ_ACCESS"
      }
    },
    {
      "RequestId": "req_2",
      "URL": "/remote/object/property",
      "Verb": "PUT",
      "Body": {
        "ObjectPath": "/Game/Level01.Level01:PersistentLevel.BP_Enemy_C_0",
        "PropertyName": "bIsAlive",
        "PropertyValue": {"bIsAlive": false},
        "access": "WRITE_ACCESS"
      }
    }
  ]
}
```

Response: array of results keyed by RequestId.

### 3.6. Spawn Actor via KismetMath

```http
PUT /remote/object/call
Content-Type: application/json

{
  "ObjectPath": "/Script/Engine.Default__GameplayStatics",
  "FunctionName": "BeginSpawningActorFromClass",
  "Parameters": {
    "ActorClass": "/Game/Blueprints/BP_Enemy.BP_Enemy_C",
    "SpawnTransform": {
      "Translation": {"X": 0.0, "Y": 200.0, "Z": 100.0},
      "Rotation":    {"Pitch": 0.0, "Yaw": 90.0, "Roll": 0.0},
      "Scale3D":     {"X": 1.0, "Y": 1.0, "Z": 1.0}
    }
  }
}
```

---

## 4. WebSocket Messages (Full)

Port: **30020**

### 4.1. HTTP Proxy via WebSocket (Primary Pattern)

Wrap any HTTP endpoint call as a WebSocket message for async handling.

```json
{
  "MessageName": "http",
  "RequestId": 42,
  "Parameters": {
    "Url": "/remote/object/property",
    "Verb": "PUT",
    "Body": {
      "ObjectPath": "/Game/Level.Level:PersistentLevel.SunLight_0",
      "PropertyName": "Intensity",
      "PropertyValue": { "Intensity": 5.0 },
      "access": "WRITE_ACCESS"
    }
  }
}
```

Response:
```json
{
  "RequestId": 42,
  "ResponseCode": 200,
  "ResponseBody": {}
}
```

### 4.2. Preset Registration (Push Events)

```json
// Client → Server: subscribe to preset changes
{
  "MessageName": "preset.register",
  "Parameters": {
    "PresetName": "MyLevelPreset",
    "IgnoreRemoteChanges": false
  }
}
```

After registration, Server → Client pushes on any property change:
```json
{
  "Type": "PresetFieldsChanged",
  "PresetName": "MyLevelPreset",
  "ChangedFields": [
    {
      "PropertyLabel": "SunIntensity",
      "ObjectPath": "/...",
      "PropertyName": "Intensity",
      "PropertyValue": { "Intensity": 7.5 }
    }
  ]
}
```

```json
// Unsubscribe
{
  "MessageName": "preset.unregister",
  "Parameters": { "PresetName": "MyLevelPreset" }
}
```

### 4.3. Preset Field List

```json
// GET preset describe via WebSocket
{
  "MessageName": "http",
  "RequestId": 1,
  "Parameters": {
    "Url": "/remote/preset/MyLevelPreset/describe",
    "Verb": "GET",
    "Body": {}
  }
}
```

Response: list of exposed fields with name, objectPath, propertyName, type.

---

## 5. ObjectPath Format

```
/Game/Maps/LevelName.LevelName:PersistentLevel.ActorLabel_InstanceId
                                                 └─ Actor class C-suffix + index
/Script/Engine.Default__ClassName              ← CDO (Class Default Object) for static funcs
/Game/Blueprints/BP_Name.BP_Name_C            ← Blueprint class reference
```

Common static function targets:

| ObjectPath | Functions available |
|:-----------|:--------------------|
| `/Script/Engine.Default__KismetSystemLibrary` | `PrintString`, `QuitGame`, `SetTimer` |
| `/Script/Engine.Default__GameplayStatics` | `BeginSpawningActorFromClass`, `GetAllActorsOfClass` |
| `/Script/Engine.Default__KismetMathLibrary` | Math utilities |
| `/Script/Engine.Default__KismetStringLibrary` | String utilities |

---

## 6. TypeScript MCP Bridge — Full Implementation

```typescript
// unreal-bridge.ts
import WebSocket from 'ws';
import fetch from 'node-fetch';

const HTTP_BASE = 'http://127.0.0.1:30010';
const WS_URL    = 'ws://127.0.0.1:30020';

export class UnrealBridge {
  private ws!: WebSocket;
  private pending = new Map<number, (d: any) => void>();
  private reqId   = 0;

  // ── Connect ────────────────────────────────────────────────────
  connect(): Promise<void> {
    return new Promise((res, rej) => {
      this.ws = new WebSocket(WS_URL);
      this.ws.on('open', () => {
        console.log('[Unreal Bridge] WebSocket connected');
        res();
      });
      this.ws.on('error', rej);
      this.ws.on('message', (raw) => {
        try {
          const msg = JSON.parse(raw.toString());
          // Handle push events (preset.changed)
          if (msg.Type === 'PresetFieldsChanged') {
            this.onPresetChanged?.(msg);
            return;
          }
          const cb = this.pending.get(msg.RequestId);
          if (cb) { cb(msg); this.pending.delete(msg.RequestId); }
        } catch { /* ignore malformed */ }
      });
    });
  }

  onPresetChanged?: (event: any) => void;

  // ── HTTP proxy via WebSocket ───────────────────────────────────
  private wsCall(url: string, verb: string, body: object): Promise<any> {
    return new Promise((res) => {
      const id = ++this.reqId;
      this.pending.set(id, res);
      this.ws.send(JSON.stringify({
        MessageName: 'http',
        RequestId:   id,
        Parameters:  { Url: url, Verb: verb, Body: body }
      }));
    });
  }

  // ── REST fallback (for non-WebSocket scenarios) ────────────────
  private async httpCall(method: string, path: string, body?: object): Promise<any> {
    const resp = await fetch(`${HTTP_BASE}${path}`, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    });
    return resp.json();
  }

  // ── High-level API ─────────────────────────────────────────────

  /** Read a property from a UObject */
  getProperty(objectPath: string, propertyName: string): Promise<any> {
    return this.wsCall('/remote/object/property', 'GET', {
      ObjectPath: objectPath,
      PropertyName: propertyName,
      access: 'READ_ACCESS'
    });
  }

  /** Write a property on a UObject */
  setProperty(objectPath: string, propertyName: string, value: any): Promise<any> {
    return this.wsCall('/remote/object/property', 'PUT', {
      ObjectPath: objectPath,
      PropertyName: propertyName,
      PropertyValue: { [propertyName]: value },
      access: 'WRITE_ACCESS'
    });
  }

  /** Call a UFUNCTION on a UObject */
  callFunction(objectPath: string, functionName: string, parameters: object = {}): Promise<any> {
    return this.wsCall('/remote/object/call', 'PUT', {
      ObjectPath: objectPath,
      FunctionName: functionName,
      Parameters: parameters,
      GenerateTransaction: false
    });
  }

  /** Spawn an actor at position */
  spawnActor(classPath: string, x: number, y: number, z: number, yaw = 0): Promise<any> {
    return this.callFunction(
      '/Script/Engine.Default__GameplayStatics',
      'BeginSpawningActorFromClass',
      {
        ActorClass: classPath,
        SpawnTransform: {
          Translation: { X: x, Y: y, Z: z },
          Rotation:    { Pitch: 0, Yaw: yaw, Roll: 0 },
          Scale3D:     { X: 1, Y: 1, Z: 1 }
        }
      }
    );
  }

  /** Batch multiple calls in one request */
  async batchCall(calls: Array<{url: string; verb: string; body: object}>): Promise<any> {
    const requests = calls.map((c, i) => ({
      RequestId: `batch_${i}`,
      URL: c.url,
      Verb: c.verb.toUpperCase(),
      Body: c.body
    }));
    return this.httpCall('PUT', '/remote/batch', { Requests: requests });
  }

  /** Subscribe to a Remote Control Preset for push events */
  registerPreset(presetName: string): void {
    this.ws.send(JSON.stringify({
      MessageName: 'preset.register',
      Parameters:  { PresetName: presetName, IgnoreRemoteChanges: false }
    }));
  }

  /** Unsubscribe from preset events */
  unregisterPreset(presetName: string): void {
    this.ws.send(JSON.stringify({
      MessageName: 'preset.unregister',
      Parameters:  { PresetName: presetName }
    }));
  }

  /** Print a string on screen (quick debug) */
  printString(text: string, duration = 5.0, r=0, g=255, b=0): Promise<any> {
    return this.callFunction(
      '/Script/Engine.Default__KismetSystemLibrary',
      'PrintString',
      {
        InString: text,
        bPrintToScreen: true,
        bPrintToLog: true,
        TextColor: { R: r, G: g, B: b, A: 255 },
        Duration: duration
      }
    );
  }

  disconnect(): void { this.ws?.close(); }
}

// ── MCP Server Tool Registration ───────────────────────────────────

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({ name: 'unreal-hsa-bridge', version: '1.0.0' });
const bridge = new UnrealBridge();

server.registerTool('ue_get_property', {
  description: 'Read a property from a Unreal Engine UObject',
  inputSchema: {
    objectPath:   z.string().describe('Full UObject path'),
    propertyName: z.string().describe('Property name to read'),
  }
}, async ({ objectPath, propertyName }) => {
  const r = await bridge.getProperty(objectPath, propertyName);
  return { content: [{ type: 'text', text: JSON.stringify(r) }] };
});

server.registerTool('ue_set_property', {
  description: 'Write a property on a Unreal Engine UObject',
  inputSchema: {
    objectPath:   z.string(),
    propertyName: z.string(),
    value:        z.any().describe('New property value'),
  }
}, async ({ objectPath, propertyName, value }) => {
  const r = await bridge.setProperty(objectPath, propertyName, value);
  return { content: [{ type: 'text', text: JSON.stringify(r) }] };
});

server.registerTool('ue_call_function', {
  description: 'Call a UFUNCTION on a Unreal Engine object',
  inputSchema: {
    objectPath:   z.string(),
    functionName: z.string(),
    parameters:   z.record(z.any()).optional().default({}),
  }
}, async ({ objectPath, functionName, parameters }) => {
  const r = await bridge.callFunction(objectPath, functionName, parameters);
  return { content: [{ type: 'text', text: JSON.stringify(r) }] };
});

server.registerTool('ue_spawn_actor', {
  description: 'Spawn an actor in the current Unreal level',
  inputSchema: {
    classPath: z.string().describe('Blueprint class path e.g. /Game/BP/BP_Enemy.BP_Enemy_C'),
    x: z.number(), y: z.number(), z: z.number(),
    yaw: z.number().optional().default(0),
  }
}, async (params) => {
  const r = await bridge.spawnActor(params.classPath, params.x, params.y, params.z, params.yaw);
  return { content: [{ type: 'text', text: JSON.stringify(r) }] };
});

async function main() {
  await bridge.connect();
  const transport = new StdioServerTransport();
  await server.connect(transport);
}
main();
```

---

## 7. Logic Flow: End-to-End Example

```
Agent: "Set sun intensity to 8 in the current level"

1. agent calls ue_set_property({
     objectPath: "/Game/Maps/Main.Main:PersistentLevel.DirectionalLight_0",
     propertyName: "Intensity",
     value: 8.0
   })

2. MCP Bridge → ws.send({
     MessageName:"http", RequestId:1,
     Parameters:{Url:"/remote/object/property", Verb:"PUT",
       Body:{ObjectPath:"...", PropertyName:"Intensity",
             PropertyValue:{"Intensity":8.0}, access:"WRITE_ACCESS"}}
   })

3. Unreal Remote Control handles on main thread → sets Intensity=8.0
   → returns {"ResponseCode":200,"ResponseBody":{}}

4. MCP Bridge → Tool result: "ok"
5. Agent confirms: "Sun intensity set to 8."
```

---

## 8. Gotchas & Best Practices

| Issue | Cause | Fix |
|:------|:------|:----|
| 404 on `/remote/object/property` | Remote Control plugin not enabled | Enable "Remote Control API" in Plugins |
| Property not found | Wrong PropertyName (case-sensitive) | Use `/remote/preset/{name}/describe` to list |
| Function call fails | UFUNCTION not marked `BlueprintCallable` | Must have `UFUNCTION(BlueprintCallable)` |
| WS push events not arriving | Used REST instead of WS | Register preset only via WS (port 30020) |
| Batch result order | `RequestId` in response may differ | Key results by `RequestId`, not array index |
| Actor path unknown | Need to enumerate scene | Use `GetAllActorsOfClass` call to list |

<!-- BM25: library=plugin-unreal-engine target=Unreal Engine Remote Control API WebSocket preset MCP bridge -->
