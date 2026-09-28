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
| `HSA_BRIDGE_TOKEN` | *(unset)* | Bearer token the bridge presents to `init_unreal.py`. **Required** — the executor refuses to start without it, and refuses every call that does not present it. Must be identical on the bridge and in the UE project's `Saved/HSA/bridge_config.json`. The HSA server generates and persists one automatically; set it by hand only to override. |
| `HSA_UE_EXEC_CONSENT` | *(unset)* | Must be `1`/`true`/`yes`/`on` for `ue_execute_python` to run anything. Read from `~/.nockdev/hsa/.env`. See below. |
| `HSA_UE_AUDIT_LOG` | `~/.domyh/audit/ue-exec.jsonl` | Path of the exec audit trail. |
| `HSA_UE_EXEC_TIMEOUT_S` | `30` | How long a call waits on the Game Thread before the call is abandoned. |
| `HSA_UE_SAFE_MODE` | off | See below. |

#### Safe mode (opt-in, and not a sandbox)

With `HSA_UE_SAFE_MODE=1` a block is parsed with `ast` and every name it
touches is checked before `exec`:

- no `import` / `from ... import`
- no `open`, `eval`, `exec`, `compile`, `getattr`, `__import__`, `globals`
- no dunder attributes — `__class__`, `__globals__`, `f_globals`, `gi_frame`
  and the rest, which is the usual route from an object back to the import
  machinery without ever naming it
- no `class`, `global`, `nonlocal`, or `with`
- only `unreal.*` and a short list of value builtins; variables the block
  assigns are allowed, so ordinary editor scripting runs unchanged

A refusal happens **before** `exec`, so the Game Thread is never occupied and
the caller gets an answer immediately rather than after a timeout.

**It is a guard against accidents, not a sandbox.** Obfuscation defeats it, and
`exec_globals` still carries full `__builtins__` when it passes. It is off by
default for that reason. Treat the token as the boundary and safe mode as
"catch the obvious"; do not read a green result as "this was safe".

#### Why `HSA_UE_EXEC_CONSENT` is an env var and not a tool

`ue_execute_python` runs generated Python inside the editor as the user, with
no sandbox. The token only proves the caller is this bridge — it does not
record *what* the bridge was asked to run.

A consent tool would be consent the model grants itself: every tool on this
server is reachable by the model, so `ue_execute_python_consent` could be
called in the same turn as the execution it authorises, and the two calls are
indistinguishable in the transcript. An environment variable is the only
channel here the model cannot write to.

Put it in `~/.nockdev/hsa/.env` — one line, once:

```
HSA_UE_EXEC_CONSENT=1
```

That file is read for this key only. A project's own `.hsa/.env` is deliberately
not: it travels with a clone, and a repository that can switch on unsandboxed
Python execution in your editor by being opened defeats the point of a switch.
An explicit export still wins, if you want a bridge to run without consent.

`HSA_BRIDGE_TOKEN` needs no setup at all. The HSA server generates one the
first time it spawns a bridge, stores it at `~/.nockdev/hsa/bridge-token` with
mode 0600, and passes it in the environment from then on.

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
| `ue_execute_python` | Code Execution | Execute arbitrary Python scripts inside UE5. It has full context access to the `unreal` Python module namespace. Requires `HSA_UE_EXEC_CONSENT`. |

## 🔒 Executing code in the editor

`ue_execute_python` is the one tool with real blast radius: it runs generated
Python inside the editor, as the user, with `__builtins__` intact. Three
controls sit in front of it, and they are independent:

| Control | Where | What it stops |
|---------|-------|---------------|
| `HSA_BRIDGE_TOKEN` | both sides | Any local process, since only a caller holding the token reaches `/execute` |
| `HSA_UE_EXEC_CONSENT` | bridge | Accidental use, until the user opts in |
| `HSA_UE_SAFE_MODE` | editor | The obvious dangerous calls, if the user wants the extra layer |
| `MAX_CODE_BYTES` | editor | Oversized payloads (1 MiB default) |
| `HSA_UE_EXEC_TIMEOUT_S` | editor | A caller waiting forever on a Game Thread that will not come back |

A wedged Game Thread is not recoverable in-process — no thread can preempt a
thread that is stuck in an editor tick, and the platform offers no interrupt on
Windows. The timeout therefore abandons the *wait*, and the call after it stays
queued behind the stuck one. The error text says this rather than reporting a
timeout that reads like the work was cancelled.
