# Unity Editor MCP Bridge

HSA MCP Bridge Server for Unity Editor 2022+. This bridge enables DOMYH Agent to introspect scenes, read component properties, manipulate GameObjects, import assets, and trigger script recompilations—all completely automatically.

## 🌉 Architecture

```mermaid
flowchart LR
    A[HSA Engine\n(DOMYH Agent)] <-->|stdio| B(Bridge Server\nunity-bridge/src/index.ts)
    B <-->|HTTP port 30030| C[HsaUnityServer.cs\nInside Unity]
    C <-->|UnityEditor API| D[(Scene / Assets)]
```

## 📦 Prerequisites

1. **Unity Editor 2022.3 LTS** or newer.
2. **Node.js 18+**
3. **pnpm** (preferred) or `npm`.

## 🚀 Setup & Installation

### 1. Install Unity Editor C# Script

The bridge requires a C# script running inside Unity Editor to expose an HTTP endpoint (port 30030).

1. Open your Unity Project.
2. If you don't have an `Assets/Editor` folder, create one.
3. Copy `mcp-bridge-plugins/unity-bridge/Editor/HsaUnityServer.cs` into `Assets/Editor/HsaUnityServer.cs` in your Unity project.
4. Unity will recompile. Once done, the server will start automatically listening on `http://localhost:30030`. You will see `[HSA] Server started on port 30030` in the Unity Console.

*(Note: The `[InitializeOnLoad]` attribute handles starting the server automatically whenever you open your Unity project.)*

### 2. Build the TypeScript Bridge

In the `mcp-bridge-plugins/unity-bridge` directory, install dependencies and build the TypeScript server:

```bash
pnpm install
pnpm build
```

This compiles `src/index.ts` to `dist/index.js` which the HSA Engine invokes.

## 💻 Usage via HSA

Open Unity Editor, then prompt the DOMYH Agent to generate scenes or UI.

**Example MCP Tool Calls used by the Agent:**

```javascript
// Reading current hierarchy structure
hsa_bridge({target: "unity", action: "unity_get_hierarchy"})

// Creating a primitives or objects
hsa_bridge({target: "unity", action: "unity_create_object", payload: {name: "Ground", primitiveType: "Plane"}})

importing an asset
hsa_bridge({target: "unity", action: "unity_import_asset", payload: {sourcePath: "C:/images/texture.png", destPath: "Assets/tex.png"}})

// Editing properties
hsa_bridge({target: "unity", action: "unity_set_transform", payload: {objectPath: "Ground", position: {x: 0, y: -2, z: 0}}})
```

## 🛠️ Available Tools

| Tool | Phase | Description |
|------|-------|-------------|
| `unity_get_hierarchy` | Read | Get the active scene hierarchy tree. |
| `unity_get_properties` | Read | Get properties of a specific GameObject. |
| `unity_get_scene_info` | Read | Get info about the active scene. |
| `unity_create_object` | Modify | Create a new primitive or empty GameObject. |
| `unity_add_component` | Modify | Add a component (e.g. Rigidbody, BoxCollider). |
| `unity_set_transform` | Modify | Set position, rotation (Euler), and scale. |
| `unity_set_property` | Modify | Set a serialized property string representation. |
| `unity_delete_object` | Modify | Delete an object from the scene (Undo supported). |
| `unity_duplicate_object` | Modify | Clone an existing object. |
| `unity_set_parent` | Modify | Parent objects under one another. |
| `unity_save_scene` | Action | Save all open scenes. |
| `unity_play_mode` | Action | Enter/Exit Play Mode inside the editor. |
| `unity_create_material` | Pipeline | Create PBR materials with defined colors/shaders. |
| `unity_create_prefab` | Pipeline | Save an object configuration into a Prefab asset. |
| `unity_instantiate_prefab` | Pipeline | Spawn instances of an existing Prefab asset. |
| `unity_create_script` | Pipeline | Create base64-encoded C# source files inside Unity. |
| `unity_get_logs` | Debug | Fetch the current Editor Console logs and stack traces. |
