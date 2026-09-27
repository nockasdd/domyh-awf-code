# Unreal Engine MCP Bridge

HSA MCP Bridge Server for Unreal Engine 5.x. This bridge harnesses UE's **Remote Control API** combined with a zero-click setup native **Python Executor** to deeply instrument the Editor, spawn actors, batch edit blueprints, and call UFunctions directly from the agent.

## 🌉 Architecture

```mermaid
flowchart LR
    A[HSA Engine\n(DOMYH Agent)] <-->|stdio| B(Bridge Server\nue-bridge/src/index.ts)
    B <-->|HTTP port 30010| C[Remote Control API\nInside UE5]
    B <-->|HTTP port 30011| P[init_unreal.py\nInside UE5]
    C <-->|Kismet/C++ API| D[(Unreal Engine Classes)]
```

## 📦 Prerequisites

1. **Unreal Engine 5.0** or newer.
2. **Node.js 18+** with `pnpm` (or `npm`).

## 🚀 Setup & Installation

### 1. Enable UE5 Plugins

Open your Unreal Engine project, navigate to **Edit ➝ Plugins** and enable:
- **Remote Control API** (Provides the HTTP/REST interface on port 30010).
- **Python Editor Script Plugin** (Allows execution of Python inside the Editor).

After enabling both, click **Restart Now**.

### 2. Build the TypeScript Bridge

In the `mcp-bridge-plugins/ue-bridge` directory, install dependencies and build the TypeScript server:

```bash
pnpm install
pnpm build
```

This compiles `src/index.ts` to `dist/index.js` which the HSA Engine invokes.

### 3. "Zero-Click" Auto-Setup for Python

The TypeScript bridge features an **auto-setup mechanism**. When the DOMYH Agent tries to execute Python code (`ue_execute_python`), the Bridge server will:
1. Contact UE5 via Remote Control to locate your project's path.
2. Automatically create the directory `Content/Python` in your project if it doesn't exist.
3. Copy `init_unreal.py` (the Python HTTP API endpoint) into that folder.

> **Note:** On the very first execution, the agent will inform you to restart the UE project so `init_unreal.py` auto-loads on startup. It will then listen on port `30011`.

### 4. Environment Variables

| Variable | Default | Meaning |
|----------|---------|---------|
| `HSA_BRIDGE_TOKEN` | *(unset)* | Bearer token the bridge presents to `init_unreal.py`. **Required** — the executor refuses to start without it, and refuses every call that does not present it. Must be identical on the bridge and in the UE project's `Saved/HSA/bridge_config.json`. |
| `HSA_UE_EXEC_CONSENT` | *(unset)* | Must be `1`/`true`/`yes`/`on` for `ue_execute_python` to run anything. See below. |
| `HSA_UE_AUDIT_LOG` | `~/.domyh/audit/ue-exec.jsonl` | Path of the exec audit trail. |
| `HSA_UE_EXEC_TIMEOUT_S` | `30` | How long a call waits on the Game Thread before the call is abandoned. |

#### Why `HSA_UE_EXEC_CONSENT` is an env var and not a tool

`ue_execute_python` runs generated Python inside the editor as the user, with
no sandbox. The token only proves the caller is this bridge — it does not
record *what* the bridge was asked to run.

A consent tool would be consent the model grants itself: every tool on this
server is reachable by the model, so `ue_execute_python_consent` could be
called in the same turn as the execution it authorises, and the two calls are
indistinguishable in the transcript. An environment variable is the only
channel here the model cannot write to.

Set it in the MCP server config, not in a tool call:

```json
{
  "mcpServers": {
    "ue-bridge": {
      "command": "node",
      "args": [".../ue-bridge/dist/index.js"],
      "env": { "HSA_UE_EXEC_CONSENT": "1", "HSA_BRIDGE_TOKEN": "..." }
    }
  }
}
```

#### Audit trail

Every `ue_execute_python` call is appended to the JSONL log whether it was
allowed or refused:

```json
{"ts":"2026-09-27T05:51:55.879Z","code_len":61,"sha256":"7dc73f8…","outcome":"refused","error_head":"HSA_UE_EXEC_CONSENT is not set…"}
```

The code is hashed, not stored — the log answers "is this the same snippet I
ran before?" without keeping a copy of every script a session has run. Refusals
are logged too, because a refused call is exactly the one worth noticing.

## 💻 Usage via HSA

With the UE project running, use the DOMYH Agent to spawn assets and write logic. 

**Example MCP Tool Calls used by the Agent:**

```javascript
// Reading current properties of a light
hsa_bridge({target: "ue", action: "ue_get_property", payload: {objectPath: "/Game/Maps/Main.Main:PersistentLevel.DirectionalLight", propertyName: "Intensity"}})

// Spawning a Native Class
hsa_bridge({target: "ue", action: "ue_spawn_actor", payload: {className: "/Script/Engine.PointLight", location: {X: 0, Y: 0, Z: 500}}})

// Executing raw Python through the editor
hsa_bridge({target: "ue", action: "ue_execute_python", payload: {code: "unreal.log('Hello from HSA!')"}})
```

##  🛠️ Available Tools

| Tool | Type | Description |
|------|------|-------------|
| `ue_get_info` | Read | Print remote API state and active endpoints. |
| `ue_describe_object` | Read | Reflect the properties, metadata, and available UFunctions on a specific ObjectPath. |
| `ue_search_assets` | Read | Query the project's Asset Registry across all package paths. |
| `ue_get_property` | Read | Retrieve a specific property value. |
| `ue_set_property` | Modify | Update a specific UProperty. |
| `ue_call_function` | Logic | Extremely powerful: invoke *any* Blueprint-callable `UFunction` (SpawnActorFromClass, GetProjectDirectory, etc). |
| `ue_spawn_actor` | Logic | Convenience wrapper around `EditorActorSubsystem.SpawnActorFromClass` with initial Transforms. |
| `ue_set_actor_transform` | Modify | Change Actor Position/Rotation/Scale simultaneously in Editor. |
| `ue_list_actors` | Read | Uses the EditorActorSubsystem to list everything spawned in the current editing level. |
| `ue_batch` | Logic | Execute an array of `ue_call_function` RPCs in a single HTTP payload for performance. |
| `ue_execute_python` | Code Execution | Execute arbitrary Python scripts inside UE5. It has full context access to the `unreal` Python module namespace. |
