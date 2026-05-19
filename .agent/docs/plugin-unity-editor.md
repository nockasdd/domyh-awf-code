---
library: plugin-unity-editor
version: 1
latest: true
category: mcp-plugin
target_app: Unity Editor 2021.3+ / 6.x
transport: WebSocket ws://127.0.0.1:15557
plugin_type: C# Editor Script [InitializeOnLoad] (Assets/Editor/)
last_updated: 2026-03-27
---

# plugin-unity-editor — HSA MCP Bridge for Unity Editor

> Full Unity Editor plugin reference: threading model, [InitializeOnLoad] WebSocket server, all Editor API classes, AssetDatabase, BuildPipeline, CompilationPipeline, Reflection-based property dispatch, and complete MCP command table.

---

## 1. Architecture & Threading Model

Unity Editor API is **main-thread only**. The WebSocket server runs on a background thread and must
dispatch all Editor API calls back to the main thread. Three dispatch strategies are available:

```
LLM Agent
  │  MCP tool call
  ▼
MCP Bridge (TypeScript) ──ws://127.0.0.1:15557──► C# WebSocket Server
                                                    │  (background Thread / HttpListener)
                                                    │
                         ┌──────────────────────────┤
                         │  Strategy A (one-shot):  │
                         │  EditorApplication.delayCall += () => { ... }
                         │                          │
                         │  Strategy B (queue):     │
                         │  HsaDispatcher.Enqueue(action)
                         │  → MonoBehaviour.Update() dequeues
                         │                          │
                         │  Strategy C (polling):   │
                         │  EditorApplication.update += OnUpdate
                         └──────────────────────────┘
                                                    ▼
                                               Unity Main Thread
                                                    │  Editor API: SceneManager, AssetDatabase, ...
                                                    ▼
                                               Return result via TaskCompletionSource
```

### 1.1. Main Thread Dispatch Patterns

```csharp
// ─── Pattern A: one-shot delayCall (simple, no return value) ──────
EditorApplication.delayCall += () => {
    SceneView.RepaintAll();
};

// ─── Pattern B: async result via TaskCompletionSource ─────────────
// Safe for returning data from any background thread
static Task<T> RunOnMainThread<T>(Func<T> fn) {
    var tcs = new TaskCompletionSource<T>();
    EditorApplication.delayCall += () => {
        try   { tcs.SetResult(fn()); }
        catch (Exception e) { tcs.SetException(e); }
    };
    return tcs.Task;
}
// Usage from WebSocket handler:
var hierarchy = await RunOnMainThread(() => GetHierarchy());

// ─── Pattern C: persistent action queue (high-frequency dispatch) ─
[ExecuteInEditMode]
public class HsaDispatcher : MonoBehaviour {
    static readonly Queue<Action> _q = new();
    public static void Enqueue(Action a) { lock (_q) _q.Enqueue(a); }
    void Update() {
        lock (_q) {
            while (_q.Count > 0) _q.Dequeue()?.Invoke();
        }
    }
}
```

---

## 2. [InitializeOnLoad] WebSocket Server

```csharp
// File: Assets/Editor/HsaBridgeServer.cs
// Unity auto-loads this class when Editor starts (no manual setup needed)

using UnityEditor;
using UnityEditor.Compilation;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using System;
using System.Collections.Generic;
using System.IO;
using System.Net;
using System.Net.WebSockets;
using System.Reflection;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

[InitializeOnLoad]
public static class HsaBridgeServer {
    const string HOST    = "http://127.0.0.1:15557/";
    static HttpListener  _listener = new HttpListener();
    static bool          _running  = false;

    static HsaBridgeServer() {
        if (_running) return;
        _running = true;
        _listener.Prefixes.Add(HOST);
        new Thread(ListenLoop) { IsBackground = true, Name = "HsaBridge" }.Start();
        Debug.Log($"[HSA Unity Bridge] WebSocket server starting on {HOST}");
    }

    static async void ListenLoop() {
        try {
            _listener.Start();
            while (true) {
                var ctx = await _listener.GetContextAsync();
                if (ctx.Request.IsWebSocketRequest) {
                    var wsCtx = await ctx.AcceptWebSocketAsync(null);
                    _ = HandleConnection(wsCtx.WebSocket);
                } else {
                    ctx.Response.StatusCode = 400;
                    ctx.Response.Close();
                }
            }
        } catch (Exception e) {
            Debug.LogError($"[HSA] Listen error: {e.Message}");
        }
    }

    static async Task HandleConnection(WebSocket ws) {
        var buffer = new byte[131072]; // 128 KB
        while (ws.State == WebSocketState.Open) {
            try {
                var result = await ws.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                if (result.MessageType == WebSocketMessageType.Close) break;
                var raw    = Encoding.UTF8.GetString(buffer, 0, result.Count);
                var msg    = JObject.Parse(raw);
                var cmd    = msg["cmd"]?.ToString();
                var params_ = (JObject)(msg["params"] ?? new JObject());
                string reply = await DispatchAsync(cmd, params_);
                var rb = Encoding.UTF8.GetBytes(reply);
                await ws.SendAsync(new ArraySegment<byte>(rb),
                    WebSocketMessageType.Text, true, CancellationToken.None);
            } catch (Exception e) {
                var err = JsonConvert.SerializeObject(new { ok = false, error = e.Message });
                await ws.SendAsync(Encoding.UTF8.GetBytes(err).AsSegment(),
                    WebSocketMessageType.Text, true, CancellationToken.None);
            }
        }
    }

    static Task<string> DispatchAsync(string cmd, JObject p) {
        return RunOnMainThread(() => {
            object result = cmd switch {
                "get_hierarchy"       => GetHierarchy(),
                "get_object"          => GetObjectInfo(p["path"]?.ToString()),
                "set_property"        => SetProperty(
                                           p["path"]?.ToString(),
                                           p["component"]?.ToString(),
                                           p["field"]?.ToString(),
                                           p["value"]),
                "create_object"       => CreateObject(p["type"]?.ToString(), p["name"]?.ToString()),
                "destroy_object"      => DestroyObject(p["path"]?.ToString()),
                "get_assets"          => GetAssets(p["filter"]?.ToString() ?? "", p["folder"]?.ToString()),
                "load_scene"          => LoadScene(p["scenePath"]?.ToString()),
                "save_scene"          => SaveScene(),
                "build_player"        => BuildPlayer(p),
                "compile_scripts"     => CompileScripts(),
                "run_static_method"   => RunStaticMethod(p["class"]?.ToString(), p["method"]?.ToString(), p["args"]),
                "exec_menu"           => ExecMenuItem(p["path"]?.ToString()),
                "repaint"             => (object)RepaintAll(),
                "get_editor_info"     => GetEditorInfo(),
                _                     => $"Unknown cmd: {cmd}"
            };
            return JsonConvert.SerializeObject(new { ok = true, result });
        });
    }

    static Task<T> RunOnMainThread<T>(Func<T> fn) {
        var tcs = new TaskCompletionSource<T>();
        EditorApplication.delayCall += () => {
            try   { tcs.SetResult(fn()); }
            catch (Exception e) { tcs.SetException(e); }
        };
        return tcs.Task;
    }
}
```

---

## 3. Unity Editor API Reference (Full)

### 3.1. SceneManager / Hierarchy

```csharp
// Get active scene info
var scene = SceneManager.GetActiveScene();
string name = scene.name;
string path = scene.path;
bool   isDirty = scene.isDirty;

// Get all root GameObjects
var roots = scene.GetRootGameObjects();

// Find GameObject by name/path
var go = GameObject.Find("Player/Arm/Hand");   // path-style
var go2 = GameObject.FindWithTag("Enemy");

// Get all GameObjects in scene (including children)
var all = Resources.FindObjectsOfTypeAll<GameObject>();

// Scene traversal helper
static object GetHierarchy() {
    var scene = SceneManager.GetActiveScene();
    var roots = scene.GetRootGameObjects();
    return SerializeHierarchy(roots);
}

static object SerializeHierarchy(GameObject[] objects, int depth = 0) {
    var list = new List<object>();
    foreach (var go in objects) {
        var children = new GameObject[go.transform.childCount];
        for (int i = 0; i < go.transform.childCount; i++)
            children[i] = go.transform.GetChild(i).gameObject;
        list.Add(new {
            name       = go.name,
            active     = go.activeSelf,
            tag        = go.tag,
            layer      = LayerMask.LayerToName(go.layer),
            position   = new { x=go.transform.position.x, y=go.transform.position.y, z=go.transform.position.z },
            components = Array.ConvertAll(go.GetComponents<Component>(), c => c?.GetType().Name),
            children   = depth < 5 ? SerializeHierarchy(children, depth+1) : null
        });
    }
    return list;
}
```

### 3.2. EditorApplication — Lifecycle & Menu

```csharp
// delayCall: run once on next editor frame (main thread)
EditorApplication.delayCall += () => { Debug.Log("next frame"); };

// update: run every editor frame (like Update() for non-MonoBehaviour)
EditorApplication.update += OnEveryFrame;

// Execute Editor menu items
EditorApplication.ExecuteMenuItem("File/Save Project");
EditorApplication.ExecuteMenuItem("Edit/Play");             // Start play mode
EditorApplication.ExecuteMenuItem("Window/Analysis/Profiler");

// Open a scene
EditorApplication.OpenScene("Assets/Scenes/Level01.unity");

// isPlayingOrWillChangePlaymode, isPlaying, isPaused
bool playing = EditorApplication.isPlaying;
EditorApplication.isPlaying = true;   // Enter play mode

// Quit editor (headless CI)
EditorApplication.Exit(0);
```

### 3.3. AssetDatabase — Asset Management

```csharp
// Search assets
// Filter syntax: "name:Query t:TypeName l:Label"
string[] guids = AssetDatabase.FindAssets("t:Texture2D", new[] {"Assets/Art"});
foreach (var guid in guids) {
    string assetPath = AssetDatabase.GUIDToAssetPath(guid);
    var tex = AssetDatabase.LoadAssetAtPath<Texture2D>(assetPath);
}

// Search examples:
// "t:Scene"         — all scenes
// "t:Prefab"        — all prefabs
// "t:Material co"   — materials with "co" in name
// "l:MyLabel"       — assets with label "MyLabel"

static object GetAssets(string filter, string folder) {
    var folders = string.IsNullOrEmpty(folder) ? null : new[] { folder };
    var guids   = AssetDatabase.FindAssets(filter ?? "", folders);
    return Array.ConvertAll(guids, g => new {
        guid = g,
        path = AssetDatabase.GUIDToAssetPath(g)
    });
}

// Load and save assets
var prefab = AssetDatabase.LoadAssetAtPath<GameObject>("Assets/Prefabs/Enemy.prefab");
AssetDatabase.CreateAsset(someScriptableObject, "Assets/Data/Config.asset");
AssetDatabase.SaveAssets();
AssetDatabase.Refresh();    // Reimport all modified assets

// Delete asset
AssetDatabase.DeleteAsset("Assets/Old/Unused.mat");

// Move / rename
AssetDatabase.MoveAsset("Assets/Old/File.cs", "Assets/New/File.cs");
```

### 3.4. Reflection-Based Property Dispatch

```csharp
// Set any field/property on any component by name — no hardcoding needed
static object SetProperty(string goPath, string compType, string fieldName, JToken value) {
    var go = GameObject.Find(goPath);
    if (go == null) return new { ok=false, error="GameObject not found" };

    var comp = go.GetComponent(compType);
    if (comp == null) return new { ok=false, error=$"Component {compType} not found" };

    var type = comp.GetType();

    // Try field first
    var fi = type.GetField(fieldName,
        BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
    if (fi != null) {
        fi.SetValue(comp, value.ToObject(fi.FieldType));
        EditorUtility.SetDirty(go);
        SceneView.RepaintAll();
        return new { ok=true, field=fieldName, type="field" };
    }

    // Try property
    var pi = type.GetProperty(fieldName,
        BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
    if (pi != null && pi.CanWrite) {
        pi.SetValue(comp, value.ToObject(pi.PropertyType));
        EditorUtility.SetDirty(go);
        SceneView.RepaintAll();
        return new { ok=true, field=fieldName, type="property" };
    }

    return new { ok=false, error=$"Field/Property '{fieldName}' not found on {compType}" };
}

// Get all fields + values of a component
static object GetObjectInfo(string path) {
    var go = GameObject.Find(path);
    if (go == null) return null;
    var result = new Dictionary<string, object>();
    result["name"]     = go.name;
    result["active"]   = go.activeSelf;
    result["position"] = new {x=go.transform.position.x, y=go.transform.position.y, z=go.transform.position.z};
    var comps = new List<object>();
    foreach (var comp in go.GetComponents<Component>()) {
        if (comp == null) continue;
        var fields = new Dictionary<string, string>();
        foreach (var fi in comp.GetType().GetFields(BindingFlags.Public | BindingFlags.Instance))
            try { fields[fi.Name] = fi.GetValue(comp)?.ToString(); } catch {}
        comps.Add(new { type = comp.GetType().Name, fields });
    }
    result["components"] = comps;
    return result;
}
```

### 3.5. BuildPipeline — Headless Build

```csharp
// Trigger a player build from agent command
static object BuildPlayer(JObject p) {
    var scenes   = p["scenes"]?.ToObject<string[]>()
                   ?? new[] { SceneManager.GetActiveScene().path };
    var output   = p["output"]?.ToString() ?? "Build/Player";
    var target   = Enum.Parse<BuildTarget>(p["target"]?.ToString() ?? "StandaloneWindows64");
    var options  = BuildOptions.None;

    var buildOptions = new BuildPlayerOptions {
        scenes           = scenes,
        locationPathName = output,
        target           = target,
        options          = options,
    };
    var report = BuildPipeline.BuildPlayer(buildOptions);
    return new {
        summary = report.summary.result.ToString(),
        errors  = report.steps.Length,
        output  = output
    };
}
```

### 3.6. CompilationPipeline — Script Compilation Events

```csharp
// Trigger a recompile (useful after agent modifies .cs files)
static object CompileScripts() {
    CompilationPipeline.RequestScriptCompilation(RequestScriptCompilationOptions.None);
    return new { ok = true, status = "compilation requested" };
}

// Listen for compilation finish (register in [InitializeOnLoad] static ctor)
static HsaBridgeServer() {
    CompilationPipeline.compilationFinished += OnCompilationFinished;
    // ... start server ...
}

static void OnCompilationFinished(object context) {
    // context: CompilationFinishedEventArgs or null
    Debug.Log("[HSA] Compilation finished");
    // Push event to connected WebSocket clients
}
```

### 3.7. Roslyn — Runtime C# Execution (Optional)

```csharp
// Requires: Microsoft.CodeAnalysis.CSharp.Scripting NuGet
using Microsoft.CodeAnalysis.CSharp.Scripting;
using Microsoft.CodeAnalysis.Scripting;

static async Task<object> RunCSharpCode(string code) {
    var options = ScriptOptions.Default
        .AddReferences(typeof(UnityEngine.GameObject).Assembly)
        .AddReferences(typeof(UnityEditor.EditorApplication).Assembly)
        .AddImports("UnityEngine", "UnityEditor");
    var result = await CSharpScript.EvaluateAsync<object>(code, options);
    return result;
}
// Example: agent sends "UnityEngine.Camera.main.transform.position.ToString()"
```

### 3.8. SceneView & EditorUtility

```csharp
// Repaint editor views
SceneView.RepaintAll();
InspectorWindow.RepaintAllInspectors();   // optional, requires reflection

// Mark object dirty (so Unity knows to save it)
EditorUtility.SetDirty(gameObject);

// Progress bar (useful for long operations)
EditorUtility.DisplayProgressBar("Building", "Compiling shaders...", 0.5f);
EditorUtility.ClearProgressBar();

// Display dialog
bool ok = EditorUtility.DisplayDialog("HSA", "Apply changes?", "Yes", "Cancel");

// Save all dirty assets
AssetDatabase.SaveAssets();
```

---

## 4. Full Command Table (MCP Dispatch)

| cmd | Required params | Returns | Unity API |
|:----|:----------------|:--------|:----------|
| `get_editor_info` | — | `{unityVersion, platform, isPlaying, sceneName}` | `Application.unityVersion`, `EditorApplication.isPlaying` |
| `get_hierarchy` | — | tree of GameObjects | `SceneManager.GetActiveScene().GetRootGameObjects()` |
| `get_object` | `path` | `{name,active,position,components}` | `GameObject.Find`, `GetComponents` |
| `set_property` | `path,component,field,value` | `{ok}` | Reflection `SetValue` |
| `create_object` | `type,name` | `{ok}` | `new GameObject(name)` / `Instantiate` |
| `destroy_object` | `path` | `{ok}` | `Object.DestroyImmediate(go)` |
| `get_assets` | `filter?,folder?` | `[{guid,path}]` | `AssetDatabase.FindAssets` |
| `load_scene` | `scenePath` | `{ok}` | `EditorApplication.OpenScene` |
| `save_scene` | — | `{ok}` | `EditorSceneManager.SaveOpenScenes` |
| `build_player` | `scenes?,output?,target?` | `{summary,output}` | `BuildPipeline.BuildPlayer` |
| `compile_scripts` | — | `{ok}` | `CompilationPipeline.RequestScriptCompilation` |
| `run_static_method` | `class,method,args?` | `{result}` | `Type.GetMethod().Invoke(null,args)` |
| `exec_menu` | `path` | `{ok}` | `EditorApplication.ExecuteMenuItem` |
| `repaint` | — | `{ok}` | `SceneView.RepaintAll` |

---

## 5. Install

```
1. Copy HsaBridgeServer.cs to Assets/Editor/ in your Unity project
2. Install Newtonsoft.Json:
   - Via Package Manager: com.unity.nuget.newtonsoft-json
   - Or: Window → Package Manager → + → Add by name → com.unity.nuget.newtonsoft-json
3. Open Unity Editor — plugin loads automatically (no menu action needed)
4. Check Console for: [HSA Unity Bridge] WebSocket server starting on http://127.0.0.1:15557/
```

```typescript
// Test from TypeScript
import WebSocket from 'ws';
const ws = new WebSocket('ws://127.0.0.1:15557');
ws.on('open', () => {
  ws.send(JSON.stringify({ cmd: 'get_editor_info', params: {} }));
});
ws.on('message', (data) => console.log(JSON.parse(data.toString())));
```

<!-- BM25: library=plugin-unity-editor target=Unity Editor C# InitializeOnLoad WebSocket MCP bridge EditorApplication -->
