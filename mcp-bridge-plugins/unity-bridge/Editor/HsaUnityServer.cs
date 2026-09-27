using UnityEngine;
using UnityEditor;
using UnityEditor.SceneManagement;
using System;
using System.IO;
using System.Net;
using System.Text;
using System.Reflection;
using System.Threading;
using System.Threading.Tasks;
using System.Collections.Generic;
using System.Collections.Concurrent;

/// <summary>
/// HSA MCP Bridge — Unity Editor Plugin v2.0.0
/// Full automation: create objects, add components, import assets, play mode, etc.
///
/// Compatibility: Unity 2019.4 LTS through Unity 6 (6000.x), C# 7.3+
/// Install: Copy to YourProject/Assets/Editor/HsaUnityServer.cs
/// </summary>
[InitializeOnLoad]
public class HsaUnityServer
{
    private const int PORT = 30030;
    private const string PREFIX = "http://127.0.0.1:30030/";
    private const string VERSION = "2.0.0";

    private static HttpListener _listener;
    private static CancellationTokenSource _cts;
    private static volatile bool _isRunning;
    private static readonly object _lock = new object();
    private static readonly ConcurrentQueue<Action> _queue = new ConcurrentQueue<Action>();

    // ── Bootstrap ─────────────────────────────────────────────

    static HsaUnityServer()
    {
        EditorApplication.update -= OnUpdate;
        EditorApplication.update += OnUpdate;
#if UNITY_2018_1_OR_NEWER
        EditorApplication.quitting -= OnQuitting;
        EditorApplication.quitting += OnQuitting;
#endif
        StartServer();
    }

    private static void StartServer()
    {
        lock (_lock)
        {
            if (_isRunning) return;
            try
            {
                CleanupListener();
                _cts = new CancellationTokenSource();
                _listener = new HttpListener();
                _listener.Prefixes.Add(PREFIX);
                _listener.Start();
                _isRunning = true;
                Task.Run(() => ListenLoop(_cts.Token));
                Debug.Log("[HSA Bridge] Unity Editor HTTP API v" + VERSION + " started on " + PREFIX);
            }
            catch (Exception ex)
            {
                Debug.LogError("[HSA Bridge] Failed to start: " + ex.Message);
                _isRunning = false;
            }
        }
    }

    private static void StopServer()
    {
        lock (_lock)
        {
            _isRunning = false;
            if (_cts != null) { try { _cts.Cancel(); } catch { } _cts = null; }
            CleanupListener();
        }
    }

    private static void CleanupListener()
    {
        if (_listener != null)
        {
            try { _listener.Stop(); } catch { }
            try { _listener.Close(); } catch { }
            _listener = null;
        }
    }

    [UnityEditor.Callbacks.DidReloadScripts]
    private static void OnScriptsReloaded() { StopServer(); StartServer(); }
    private static void OnQuitting() { StopServer(); }

    private static void OnUpdate()
    {
        Action action;
        while (_queue.TryDequeue(out action))
        {
            try { action(); }
            catch (Exception ex) { Debug.LogError("[HSA Bridge] Queue error: " + ex); }
        }
    }

    // ── HTTP Listener ─────────────────────────────────────────

    private static async Task ListenLoop(CancellationToken ct)
    {
        while (!ct.IsCancellationRequested && _isRunning)
        {
            try
            {
                HttpListenerContext ctx = await _listener.GetContextAsync().ConfigureAwait(false);
                Task.Run(() => HandleRequest(ctx));
            }
            catch (ObjectDisposedException) { break; }
            catch (HttpListenerException) { break; }
            catch (Exception e)
            {
                if (!ct.IsCancellationRequested)
                    Debug.LogError("[HSA Bridge] Listen error: " + e.Message);
            }
        }
    }

    private static void HandleRequest(HttpListenerContext ctx)
    {
        HttpListenerRequest req = ctx.Request;
        HttpListenerResponse res = ctx.Response;

        try
        {
            string path = req.Url.AbsolutePath.TrimEnd('/');
            string body = string.Empty;
            if (req.HttpMethod == "POST" && req.HasEntityBody)
            {
                using (StreamReader reader = new StreamReader(req.InputStream, req.ContentEncoding))
                { body = reader.ReadToEnd(); }
            }

            // ── Route ─────────────────────────────────────────
            if (string.IsNullOrEmpty(path) || path == "/")
                RespondOk(res, InfoJson());
            // Phase 0 — READ endpoints
            else if (path == "/hierarchy")
                RunOnMain(res, () => BuildHierarchy());
            else if (path == "/properties")
                RunOnMain(res, () => BuildProperties(body));
            else if (path == "/scene-info")
                RunOnMain(res, () => BuildSceneInfo());
            // Phase 1 — OBJECT MANIPULATION
            else if (path == "/create-object")
                RunOnMain(res, () => DoCreateObject(body));
            else if (path == "/add-component")
                RunOnMain(res, () => DoAddComponent(body));
            else if (path == "/set-transform")
                RunOnMain(res, () => DoSetTransform(body));
            else if (path == "/set-property")
                RunOnMain(res, () => DoSetProperty(body));
            else if (path == "/delete-object")
                RunOnMain(res, () => DoDeleteObject(body));
            else if (path == "/duplicate-object")
                RunOnMain(res, () => DoDuplicateObject(body));
            else if (path == "/set-parent")
                RunOnMain(res, () => DoSetParent(body));
            else if (path == "/rename-object")
                RunOnMain(res, () => DoRenameObject(body));
            else if (path == "/play-mode")
                RunOnMain(res, () => DoPlayMode(body));
            else if (path == "/get-logs")
                RunOnMain(res, () => DoGetLogs(body));
            else if (path == "/save-scene")
                RunOnMain(res, () => DoSaveScene());
            else if (path == "/new-scene")
                RunOnMain(res, () => DoNewScene(body));
            // Phase 2 — ASSET PIPELINE
            else if (path == "/create-material")
                RunOnMain(res, () => DoCreateMaterial(body));
            else if (path == "/create-prefab")
                RunOnMain(res, () => DoCreatePrefab(body));
            else if (path == "/instantiate-prefab")
                RunOnMain(res, () => DoInstantiatePrefab(body));
            else if (path == "/import-asset")
                RunOnMain(res, () => DoImportAsset(body));
            else if (path == "/create-script")
                RunOnMain(res, () => DoCreateScript(body));
            // Existing
            else if (path == "/execute-menu")
                RunOnMain(res, () => DoExecuteMenu(body));
            else if (path == "/recompile")
                RunOnMain(res, () => DoRecompile());
            else
                RespondOk(res, ErrJson("Unknown endpoint: " + path), 404);
        }
        catch (Exception ex)
        {
            try { RespondOk(res, ErrJson(ex.Message), 500); } catch { }
        }
    }

    // ══════════════════════════════════════════════════════════
    //  Phase 0 — READ
    // ══════════════════════════════════════════════════════════

    private static string InfoJson()
    {
        StringBuilder sb = new StringBuilder(512);
        sb.Append("{\"status\":\"ok\",\"plugin\":\"HSA Unity Bridge\",\"version\":\"")
          .Append(VERSION).Append("\",\"unity\":\"").Append(Esc(Application.unityVersion)).Append("\",")
          .Append("\"endpoints\":[");
        string[] eps = new string[] {
            "/","/hierarchy","/properties","/scene-info",
            "/create-object","/add-component","/set-transform","/set-property",
            "/delete-object","/duplicate-object","/set-parent","/rename-object",
            "/play-mode","/get-logs","/save-scene","/new-scene",
            "/create-material","/create-prefab","/instantiate-prefab",
            "/import-asset","/create-script",
            "/execute-menu","/recompile"
        };
        for (int i = 0; i < eps.Length; i++)
        {
            if (i > 0) sb.Append(",");
            sb.Append("\"").Append(eps[i]).Append("\"");
        }
        sb.Append("]}");
        return sb.ToString();
    }

    private static string BuildHierarchy()
    {
        GameObject[] gos;
#if UNITY_2023_1_OR_NEWER
        gos = GameObject.FindObjectsByType<GameObject>(FindObjectsSortMode.None);
#else
        gos = GameObject.FindObjectsOfType<GameObject>();
#endif
        StringBuilder sb = new StringBuilder(4096);
        sb.Append("{\"hierarchy\":[");
        for (int i = 0; i < gos.Length; i++)
        {
            GameObject go = gos[i];
            if (i > 0) sb.Append(",");
            sb.Append("{");
            KV(sb, "name", go.name, true); KV(sb, "path", GetPath(go));
            KB(sb, "active", go.activeInHierarchy);
            KV(sb, "tag", go.tag); KV(sb, "layer", LayerMask.LayerToName(go.layer));
            Component[] comps = go.GetComponents<Component>();
            sb.Append(",\"components\":[");
            for (int j = 0; j < comps.Length; j++)
            {
                if (j > 0) sb.Append(",");
                sb.Append("\"").Append(comps[j] != null ? Esc(comps[j].GetType().Name) : "null").Append("\"");
            }
            sb.Append("]}");
        }
        sb.Append("],\"count\":").Append(gos.Length).Append("}");
        return sb.ToString();
    }

    private static string BuildProperties(string body)
    {
        string path = JVal(body, "objectPath");
        if (string.IsNullOrEmpty(path)) return ErrJson("Missing objectPath");
        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);
        Transform t = go.transform;
        StringBuilder sb = new StringBuilder(512);
        sb.Append("{");
        KV(sb, "name", go.name, true); KB(sb, "active", go.activeInHierarchy);
        KV(sb, "tag", go.tag); KV(sb, "layer", LayerMask.LayerToName(go.layer));
        sb.Append(",\"position\":"); Vec3(sb, t.position);
        sb.Append(",\"rotation\":"); Vec3(sb, t.eulerAngles);
        sb.Append(",\"scale\":"); Vec3(sb, t.localScale);
        sb.Append(",\"childCount\":").Append(t.childCount);
        Component[] comps = go.GetComponents<Component>();
        sb.Append(",\"components\":[");
        bool first = true;
        for (int i = 0; i < comps.Length; i++)
        {
            if (comps[i] == null) continue;
            if (!first) sb.Append(","); first = false;
            Behaviour beh = comps[i] as Behaviour;
            bool en = beh != null ? beh.enabled : true;
            sb.Append("{\"type\":\"").Append(Esc(comps[i].GetType().Name))
              .Append("\",\"enabled\":").Append(en ? "true" : "false").Append("}");
        }
        sb.Append("]}");
        return sb.ToString();
    }

    private static string BuildSceneInfo()
    {
        var scene = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
        StringBuilder sb = new StringBuilder(256);
        sb.Append("{"); KV(sb, "name", scene.name, true); KV(sb, "path", scene.path);
        KB(sb, "isDirty", scene.isDirty); KB(sb, "isLoaded", scene.isLoaded);
        sb.Append(",\"rootCount\":").Append(scene.rootCount);
        sb.Append(",\"buildIndex\":").Append(scene.buildIndex).Append("}");
        return sb.ToString();
    }

    // ══════════════════════════════════════════════════════════
    //  Phase 1 — OBJECT MANIPULATION
    // ══════════════════════════════════════════════════════════

    private static string DoCreateObject(string body)
    {
        string name = JVal(body, "name");
        if (string.IsNullOrEmpty(name)) name = "NewObject";
        string prim = JVal(body, "primitiveType");

        GameObject go;
        if (!string.IsNullOrEmpty(prim) && prim != "None")
        {
            PrimitiveType pt;
            try { pt = (PrimitiveType)Enum.Parse(typeof(PrimitiveType), prim, true); }
            catch { return ErrJson("Invalid primitiveType: " + prim + ". Use: Cube,Sphere,Capsule,Cylinder,Plane,Quad"); }
            go = GameObject.CreatePrimitive(pt);
            go.name = name;
        }
        else
        {
            go = new GameObject(name);
        }

        Undo.RegisterCreatedObjectUndo(go, "HSA Create " + name);

        // Optional position
        float px = JNum(body, "px", 0); float py = JNum(body, "py", 0); float pz = JNum(body, "pz", 0);
        string posJson = JObj(body, "position");
        if (posJson != null)
        {
            px = JNum(posJson, "x", 0); py = JNum(posJson, "y", 0); pz = JNum(posJson, "z", 0);
        }
        go.transform.position = new Vector3(px, py, pz);

        // Optional parent
        string parentPath = JVal(body, "parent");
        if (!string.IsNullOrEmpty(parentPath))
        {
            GameObject parentGo = GameObject.Find(parentPath);
            if (parentGo != null) go.transform.SetParent(parentGo.transform, true);
        }

        EditorUtility.SetDirty(go);
        return OkJson("created", go);
    }

    private static string DoAddComponent(string body)
    {
        string path = JVal(body, "objectPath");
        string typeName = JVal(body, "componentType");
        if (string.IsNullOrEmpty(path)) return ErrJson("Missing objectPath");
        if (string.IsNullOrEmpty(typeName)) return ErrJson("Missing componentType");

        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);

        Type compType = ResolveType(typeName);
        if (compType == null) return ErrJson("Unknown component type: " + typeName);

        Undo.RecordObject(go, "HSA AddComponent " + typeName);
        Component comp = go.AddComponent(compType);
        if (comp == null) return ErrJson("Failed to add " + typeName);

        EditorUtility.SetDirty(go);
        StringBuilder sb = new StringBuilder("{");
        KV(sb, "ok", "true", true); KV(sb, "object", go.name);
        KV(sb, "added", comp.GetType().Name); sb.Append("}");
        return sb.ToString();
    }

    private static string DoSetTransform(string body)
    {
        string path = JVal(body, "objectPath");
        if (string.IsNullOrEmpty(path)) return ErrJson("Missing objectPath");
        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);

        Undo.RecordObject(go.transform, "HSA SetTransform");

        string posJson = JObj(body, "position");
        if (posJson != null)
            go.transform.position = new Vector3(JNum(posJson, "x", go.transform.position.x),
                JNum(posJson, "y", go.transform.position.y), JNum(posJson, "z", go.transform.position.z));

        string rotJson = JObj(body, "rotation");
        if (rotJson != null)
            go.transform.eulerAngles = new Vector3(JNum(rotJson, "x", go.transform.eulerAngles.x),
                JNum(rotJson, "y", go.transform.eulerAngles.y), JNum(rotJson, "z", go.transform.eulerAngles.z));

        string scaleJson = JObj(body, "scale");
        if (scaleJson != null)
            go.transform.localScale = new Vector3(JNum(scaleJson, "x", go.transform.localScale.x),
                JNum(scaleJson, "y", go.transform.localScale.y), JNum(scaleJson, "z", go.transform.localScale.z));

        EditorUtility.SetDirty(go);
        return OkJson("transformed", go);
    }

    private static string DoSetProperty(string body)
    {
        string path = JVal(body, "objectPath");
        string compType = JVal(body, "componentType");
        string propName = JVal(body, "propertyName");
        string propVal = JVal(body, "propertyValue");
        if (string.IsNullOrEmpty(path) || string.IsNullOrEmpty(propName))
            return ErrJson("Missing objectPath or propertyName");

        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);

        // If componentType specified, find that component; otherwise use GameObject
        UnityEngine.Object target = go;
        if (!string.IsNullOrEmpty(compType))
        {
            Type ct = ResolveType(compType);
            if (ct != null)
            {
                Component comp = go.GetComponent(ct);
                if (comp != null) target = comp;
                else return ErrJson("Component not found: " + compType);
            }
        }

        // Use SerializedObject for proper undo/dirty
        SerializedObject so = new SerializedObject(target);
        SerializedProperty sp = so.FindProperty(propName);
        if (sp == null) return ErrJson("Property not found: " + propName);

        Undo.RecordObject(target, "HSA SetProperty " + propName);
        switch (sp.propertyType)
        {
            case SerializedPropertyType.Integer: sp.intValue = int.Parse(propVal); break;
            case SerializedPropertyType.Float: sp.floatValue = float.Parse(propVal); break;
            case SerializedPropertyType.Boolean: sp.boolValue = propVal == "true" || propVal == "1"; break;
            case SerializedPropertyType.String: sp.stringValue = propVal; break;
            case SerializedPropertyType.Color:
                string[] c = propVal.Split(',');
                if (c.Length >= 3) sp.colorValue = new Color(float.Parse(c[0]), float.Parse(c[1]), float.Parse(c[2]), c.Length >= 4 ? float.Parse(c[3]) : 1f);
                break;
            default: return ErrJson("Unsupported property type: " + sp.propertyType);
        }
        so.ApplyModifiedProperties();
        return "{\"ok\":true,\"property\":\"" + Esc(propName) + "\",\"value\":\"" + Esc(propVal) + "\"}";
    }

    private static string DoDeleteObject(string body)
    {
        string path = JVal(body, "objectPath");
        if (string.IsNullOrEmpty(path)) return ErrJson("Missing objectPath");
        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);
        string n = go.name;
        Undo.DestroyObjectImmediate(go);
        return "{\"ok\":true,\"deleted\":\"" + Esc(n) + "\"}";
    }

    private static string DoDuplicateObject(string body)
    {
        string path = JVal(body, "objectPath");
        if (string.IsNullOrEmpty(path)) return ErrJson("Missing objectPath");
        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);
        GameObject clone = UnityEngine.Object.Instantiate(go, go.transform.parent);
        clone.name = go.name + "_Copy";
        Undo.RegisterCreatedObjectUndo(clone, "HSA Duplicate " + go.name);
        return OkJson("duplicated", clone);
    }

    private static string DoSetParent(string body)
    {
        string childPath = JVal(body, "childPath");
        string parentPath = JVal(body, "parentPath");
        if (string.IsNullOrEmpty(childPath)) return ErrJson("Missing childPath");

        GameObject child = GameObject.Find(childPath);
        if (child == null) return ErrJson("Child not found: " + childPath);

        Undo.SetTransformParent(child.transform,
            string.IsNullOrEmpty(parentPath) ? null : GameObject.Find(parentPath)?.transform,
            "HSA SetParent");

        return "{\"ok\":true,\"child\":\"" + Esc(child.name) + "\",\"parent\":\"" + Esc(parentPath ?? "root") + "\"}";
    }

    private static string DoRenameObject(string body)
    {
        string path = JVal(body, "objectPath");
        string newName = JVal(body, "newName");
        if (string.IsNullOrEmpty(path) || string.IsNullOrEmpty(newName)) return ErrJson("Missing objectPath or newName");
        GameObject go = GameObject.Find(path);
        if (go == null) return ErrJson("Not found: " + path);
        Undo.RecordObject(go, "HSA Rename");
        string old = go.name;
        go.name = newName;
        EditorUtility.SetDirty(go);
        return "{\"ok\":true,\"oldName\":\"" + Esc(old) + "\",\"newName\":\"" + Esc(newName) + "\"}";
    }

    private static string DoPlayMode(string body)
    {
        string action = JVal(body, "action");
        if (string.IsNullOrEmpty(action)) action = "toggle";

        if (action == "play") EditorApplication.isPlaying = true;
        else if (action == "stop") EditorApplication.isPlaying = false;
        else if (action == "pause") EditorApplication.isPaused = !EditorApplication.isPaused;
        else EditorApplication.isPlaying = !EditorApplication.isPlaying;

        return "{\"ok\":true,\"isPlaying\":" + (EditorApplication.isPlaying ? "true" : "false")
             + ",\"isPaused\":" + (EditorApplication.isPaused ? "true" : "false") + "}";
    }

    /// <summary>
    /// Read Unity Editor Console logs via Reflection on UnityEditorInternal.LogEntries.
    /// Works across Unity 2019.4 - 6000.x. Returns log entries with message, type, and stacktrace.
    /// </summary>
    private static string DoGetLogs(string body)
    {
        int limit = (int)JNum(body, "limit", 50);
        bool errorOnly = JVal(body, "errorOnly") == "true";
        bool clear = JVal(body, "clear") == "true";

        try
        {
            // Resolve internal LogEntries class via Reflection
            Type logEntriesType = null;
            Type logEntryType = null;
            foreach (Assembly asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                if (logEntriesType == null)
                    logEntriesType = asm.GetType("UnityEditor.LogEntries") ?? asm.GetType("UnityEditorInternal.LogEntries");
                if (logEntryType == null)
                    logEntryType = asm.GetType("UnityEditor.LogEntry") ?? asm.GetType("UnityEditorInternal.LogEntry");
                    
                if (logEntriesType != null && logEntryType != null) break;
            }
            if (logEntriesType == null)
                return ErrJson("LogEntries type not found — Unity version may not support this API. Types Checked: UnityEditor.LogEntries / UnityEditorInternal.LogEntries");

            // Get methods
            MethodInfo startMethod = logEntriesType.GetMethod("StartGettingEntries", BindingFlags.Static | BindingFlags.Public);
            MethodInfo endMethod = logEntriesType.GetMethod("EndGettingEntries", BindingFlags.Static | BindingFlags.Public);
            MethodInfo countMethod = logEntriesType.GetMethod("GetCount", BindingFlags.Static | BindingFlags.Public);
            MethodInfo clearMethod = logEntriesType.GetMethod("Clear", BindingFlags.Static | BindingFlags.Public);

            // Try GetEntryInternal (Unity 2019+) or GetEntryAtIndex
            MethodInfo getEntryMethod = logEntriesType.GetMethod("GetEntryInternal", BindingFlags.Static | BindingFlags.Public);
            if (getEntryMethod == null)
                getEntryMethod = logEntriesType.GetMethod("GetEntryAtIndex", BindingFlags.Static | BindingFlags.Public);

            if (countMethod == null || getEntryMethod == null)
                return ErrJson("Required LogEntries methods not found");

            int total = (int)countMethod.Invoke(null, null);
            if (startMethod != null) startMethod.Invoke(null, null);

            try
            {
                StringBuilder sb = new StringBuilder(4096);
                sb.Append("{\"total\":").Append(total).Append(",\"logs\":[");

                // Read from newest to oldest (end of list = newest)
                int start = Math.Max(0, total - limit);
                int written = 0;

                for (int i = total - 1; i >= start; i--)
                {
                    // Create LogEntry instance
                    object entry = Activator.CreateInstance(logEntryType);
                    bool ok = (bool)getEntryMethod.Invoke(null, new object[] { i, entry });
                    if (!ok) continue;

                    // Read fields: message (string), mode (int)
                    FieldInfo msgField = logEntryType.GetField("message", BindingFlags.Instance | BindingFlags.Public);
                    FieldInfo modeField = logEntryType.GetField("mode", BindingFlags.Instance | BindingFlags.Public);

                    string message = msgField != null ? (string)msgField.GetValue(entry) : "";
                    int mode = modeField != null ? (int)modeField.GetValue(entry) : 0;

                    // Classify log type from mode bitmask
                    // Bits: 1=Error, 2=Assert, 4=Log, 8=Fatal, 16=DontPreprocess,
                    //       32=LogLevelLog, 64=ScriptingError, 128=ScriptingWarning, etc.
                    string logType = "log";
                    if ((mode & (1 | 2 | 8 | 64)) != 0) logType = "error";
                    else if ((mode & (128 | 256)) != 0) logType = "warning";

                    if (errorOnly && logType != "error") continue;

                    // Split message into first line (message) and rest (stacktrace)
                    string mainMsg = message;
                    string stacktrace = "";
                    int nlIdx = message.IndexOf('\n');
                    if (nlIdx >= 0)
                    {
                        mainMsg = message.Substring(0, nlIdx);
                        stacktrace = message.Substring(nlIdx + 1);
                    }

                    if (written > 0) sb.Append(",");
                    sb.Append("{\"type\":\"").Append(logType)
                      .Append("\",\"message\":\"").Append(Esc(mainMsg))
                      .Append("\",\"stacktrace\":\"").Append(Esc(stacktrace))
                      .Append("\"}");
                    written++;
                }

                sb.Append("],\"returned\":").Append(written).Append("}");

                // Clear logs after reading if requested
                if (clear && clearMethod != null)
                    clearMethod.Invoke(null, null);

                return sb.ToString();
            }
            finally
            {
                if (endMethod != null) endMethod.Invoke(null, null);
            }
        }
        catch (Exception ex)
        {
            return ErrJson("GetLogs failed: " + ex.Message);
        }
    }

    private static string DoSaveScene()
    {
        bool ok = EditorSceneManager.SaveOpenScenes();
        return "{\"ok\":" + (ok ? "true" : "false") + ",\"message\":\"Scene saved\"}";
    }

    private static string DoNewScene(string body)
    {
        string name = JVal(body, "name");
#if UNITY_2019_1_OR_NEWER
        var scene = EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects, NewSceneMode.Single);
#else
        EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects);
        var scene = UnityEngine.SceneManagement.SceneManager.GetActiveScene();
#endif
        return "{\"ok\":true,\"scene\":\"" + Esc(scene.name) + "\"}";
    }

    // ══════════════════════════════════════════════════════════
    //  Phase 2 — ASSET PIPELINE
    // ══════════════════════════════════════════════════════════

    private static string DoCreateMaterial(string body)
    {
        string mName = JVal(body, "name");
        if (string.IsNullOrEmpty(mName)) mName = "NewMaterial";
        string shaderName = JVal(body, "shaderName");
        if (string.IsNullOrEmpty(shaderName)) shaderName = "Standard";

        Shader shader = Shader.Find(shaderName);
        if (shader == null)
        {
            // Try common URP/HDRP shaders
            shader = Shader.Find("Universal Render Pipeline/Lit");
            if (shader == null) shader = Shader.Find("HDRP/Lit");
            if (shader == null) shader = Shader.Find("Standard");
            if (shader == null) return ErrJson("Shader not found: " + shaderName);
        }

        Material mat = new Material(shader);
        mat.name = mName;

        // Optional color
        string colorJson = JObj(body, "color");
        if (colorJson != null)
        {
            mat.color = new Color(
                JNum(colorJson, "r", 1f), JNum(colorJson, "g", 1f),
                JNum(colorJson, "b", 1f), JNum(colorJson, "a", 1f));
        }

        string savePath = JVal(body, "savePath");
        if (string.IsNullOrEmpty(savePath)) savePath = "Assets/Materials";
        if (!Directory.Exists(savePath)) Directory.CreateDirectory(savePath);

        string fullPath = savePath + "/" + mName + ".mat";
        AssetDatabase.CreateAsset(mat, fullPath);
        AssetDatabase.SaveAssets();

        return "{\"ok\":true,\"path\":\"" + Esc(fullPath) + "\",\"shader\":\"" + Esc(shader.name) + "\"}";
    }

    private static string DoCreatePrefab(string body)
    {
        string objPath = JVal(body, "objectPath");
        string savePath = JVal(body, "savePath");
        if (string.IsNullOrEmpty(objPath)) return ErrJson("Missing objectPath");
        if (string.IsNullOrEmpty(savePath)) savePath = "Assets/Prefabs/" + objPath + ".prefab";

        GameObject go = GameObject.Find(objPath);
        if (go == null) return ErrJson("Not found: " + objPath);

        string dir = Path.GetDirectoryName(savePath);
        if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir)) Directory.CreateDirectory(dir);

#if UNITY_2018_3_OR_NEWER
        bool success;
        PrefabUtility.SaveAsPrefabAsset(go, savePath, out success);
        if (!success) return ErrJson("Failed to create prefab");
#else
        PrefabUtility.CreatePrefab(savePath, go);
#endif
        return "{\"ok\":true,\"prefabPath\":\"" + Esc(savePath) + "\"}";
    }

    private static string DoInstantiatePrefab(string body)
    {
        string prefabPath = JVal(body, "prefabPath");
        if (string.IsNullOrEmpty(prefabPath)) return ErrJson("Missing prefabPath");

        GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
        if (prefab == null) return ErrJson("Prefab not found: " + prefabPath);

        GameObject instance = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
        if (instance == null) return ErrJson("Failed to instantiate prefab");

        Undo.RegisterCreatedObjectUndo(instance, "HSA InstantiatePrefab");

        string posJson = JObj(body, "position");
        if (posJson != null)
            instance.transform.position = new Vector3(JNum(posJson, "x", 0), JNum(posJson, "y", 0), JNum(posJson, "z", 0));

        string newName = JVal(body, "name");
        if (!string.IsNullOrEmpty(newName)) instance.name = newName;

        EditorUtility.SetDirty(instance);
        return OkJson("instantiated", instance);
    }

    private static string DoImportAsset(string body)
    {
        string sourcePath = JVal(body, "sourcePath");
        string destPath = JVal(body, "destPath");
        if (string.IsNullOrEmpty(sourcePath) || string.IsNullOrEmpty(destPath))
            return ErrJson("Missing sourcePath or destPath");

        string dir = Path.GetDirectoryName(destPath);
        if (!string.IsNullOrEmpty(dir) && !Directory.Exists(dir)) Directory.CreateDirectory(dir);

        try { File.Copy(sourcePath, destPath, true); }
        catch (Exception ex) { return ErrJson("Copy failed: " + ex.Message); }

        AssetDatabase.ImportAsset(destPath, ImportAssetOptions.ForceUpdate);
        AssetDatabase.Refresh();

        return "{\"ok\":true,\"imported\":\"" + Esc(destPath) + "\"}";
    }

    private static string DoCreateScript(string body)
    {
        string scriptName = JVal(body, "name");
        string savePath = JVal(body, "savePath");
        if (string.IsNullOrEmpty(scriptName)) return ErrJson("Missing name");

        if (string.IsNullOrEmpty(savePath)) savePath = "Assets/Scripts";
        if (!Directory.Exists(savePath)) Directory.CreateDirectory(savePath);

        string fullPath = savePath + "/" + scriptName + ".cs";

        // Priority: contentBase64 > content > default template
        // Base64 is preferred for complex code — avoids all JSON escaping issues
        string contentBase64 = JVal(body, "contentBase64");
        string content;
        if (!string.IsNullOrEmpty(contentBase64))
        {
            try { content = Encoding.UTF8.GetString(Convert.FromBase64String(contentBase64)); }
            catch (Exception ex) { return ErrJson("Invalid base64: " + ex.Message); }
        }
        else
        {
            content = JVal(body, "content");
            if (string.IsNullOrEmpty(content))
            {
                content = "using UnityEngine;\n\npublic class " + scriptName + " : MonoBehaviour\n{\n    void Start()\n    {\n        \n    }\n\n    void Update()\n    {\n        \n    }\n}\n";
            }
        }

        File.WriteAllText(fullPath, content, Encoding.UTF8);
        AssetDatabase.ImportAsset(fullPath);
        AssetDatabase.Refresh();

        return "{\"ok\":true,\"scriptPath\":\"" + Esc(fullPath) + "\"}";
    }

    // ── Existing endpoints ────────────────────────────────────

    private static string DoExecuteMenu(string body)
    {
        string menuPath = JVal(body, "menuPath");
        if (string.IsNullOrEmpty(menuPath)) return ErrJson("Missing menuPath");
        bool ok = EditorApplication.ExecuteMenuItem(menuPath);
        return "{\"ok\":" + (ok ? "true" : "false") + ",\"menuPath\":\"" + Esc(menuPath) + "\"}";
    }

    private static string DoRecompile()
    {
#if UNITY_2019_3_OR_NEWER
        UnityEditor.Compilation.CompilationPipeline.RequestScriptCompilation();
        return "{\"ok\":true,\"message\":\"Recompilation requested\"}";
#else
        AssetDatabase.Refresh();
        return "{\"ok\":true,\"message\":\"AssetDatabase.Refresh triggered\"}";
#endif
    }

    // ══════════════════════════════════════════════════════════
    //  HELPERS
    // ══════════════════════════════════════════════════════════

    private static void RunOnMain(HttpListenerResponse res, Func<string> work)
    {
        TaskCompletionSource<string> tcs = new TaskCompletionSource<string>();
        _queue.Enqueue(() => {
            try { tcs.TrySetResult(work()); }
            catch (Exception ex) { tcs.TrySetException(ex); }
        });
        Task.Run(async () => {
            try { RespondOk(res, await tcs.Task.ConfigureAwait(false)); }
            catch (Exception ex) { RespondOk(res, ErrJson(ex.Message), 500); }
        });
    }

    private static void RespondOk(HttpListenerResponse res, string json, int status = 200)
    {
        try
        {
            byte[] buf = Encoding.UTF8.GetBytes(json);
            res.StatusCode = status; res.ContentType = "application/json"; res.ContentLength64 = buf.Length;
            res.OutputStream.Write(buf, 0, buf.Length); res.OutputStream.Close();
        }
        catch { }
    }

    // ── Type Resolution ───────────────────────────────────────

    private static Type ResolveType(string name)
    {
        // Try direct
        Type t = Type.GetType(name);
        if (t != null) return t;

        // Try UnityEngine namespace
        t = Type.GetType("UnityEngine." + name + ", UnityEngine");
        if (t != null) return t;

        // Scan loaded assemblies
        foreach (Assembly asm in AppDomain.CurrentDomain.GetAssemblies())
        {
            t = asm.GetType(name);
            if (t != null) return t;
            t = asm.GetType("UnityEngine." + name);
            if (t != null) return t;
            t = asm.GetType("UnityEngine.UI." + name);
            if (t != null) return t;
        }
        return null;
    }

    // ── JSON helpers (no deps, C# 7.3 compat) ────────────────

    private static string OkJson(string action, GameObject go)
    {
        Transform t = go.transform;
        StringBuilder sb = new StringBuilder("{");
        KV(sb, "ok", "true", true); KV(sb, "action", action); KV(sb, "name", go.name);
        KV(sb, "path", GetPath(go));
        sb.Append(",\"position\":"); Vec3(sb, t.position);
        sb.Append(",\"instanceId\":").Append(go.GetInstanceID());
        sb.Append("}");
        return sb.ToString();
    }

    private static string ErrJson(string msg) { return "{\"error\":\"" + Esc(msg) + "\"}"; }

    private static void KV(StringBuilder sb, string k, string v, bool first = false)
    { if (!first) sb.Append(","); sb.Append("\"").Append(k).Append("\":\"").Append(Esc(v)).Append("\""); }

    private static void KB(StringBuilder sb, string k, bool v, bool first = false)
    { if (!first) sb.Append(","); sb.Append("\"").Append(k).Append("\":").Append(v ? "true" : "false"); }

    private static void Vec3(StringBuilder sb, Vector3 v)
    { sb.Append("{\"x\":").Append(v.x).Append(",\"y\":").Append(v.y).Append(",\"z\":").Append(v.z).Append("}"); }

    private static string GetPath(GameObject go)
    {
        string p = go.name;
        Transform parent = go.transform.parent;
        while (parent != null) { p = parent.name + "/" + p; parent = parent.parent; }
        return p;
    }

    /// <summary>Extract string value from JSON.</summary>
    private static string JVal(string json, string key)
    {
        if (string.IsNullOrEmpty(json)) return null;
        string search = "\"" + key + "\"";
        int idx = json.IndexOf(search);
        if (idx < 0) return null;
        int colon = json.IndexOf(':', idx + search.Length);
        if (colon < 0) return null;
        // Skip whitespace
        int i = colon + 1;
        while (i < json.Length && (json[i] == ' ' || json[i] == '\t' || json[i] == '\n' || json[i] == '\r')) i++;
        if (i >= json.Length) return null;
        if (json[i] == '"')
        {
            int sq = i;
            // Find closing quote, skipping escaped quotes
            int eq = sq + 1;
            while (eq < json.Length)
            {
                if (json[eq] == '\\') { eq += 2; continue; }
                if (json[eq] == '"') break;
                eq++;
            }
            if (eq >= json.Length) return null;
            return JUnescape(json.Substring(sq + 1, eq - sq - 1));
        }
        // Number or bool or null
        int end = i;
        while (end < json.Length && json[end] != ',' && json[end] != '}' && json[end] != ']') end++;
        return json.Substring(i, end - i).Trim();
    }

    /// <summary>Extract nested JSON object as raw string.</summary>
    private static string JObj(string json, string key)
    {
        if (string.IsNullOrEmpty(json)) return null;
        string search = "\"" + key + "\"";
        int idx = json.IndexOf(search);
        if (idx < 0) return null;
        int colon = json.IndexOf(':', idx + search.Length);
        if (colon < 0) return null;
        int brace = json.IndexOf('{', colon);
        if (brace < 0) return null;
        int depth = 1; int pos = brace + 1;
        while (pos < json.Length && depth > 0)
        {
            if (json[pos] == '{') depth++;
            else if (json[pos] == '}') depth--;
            pos++;
        }
        return json.Substring(brace, pos - brace);
    }

    /// <summary>Extract float from JSON.</summary>
    private static float JNum(string json, string key, float def)
    {
        string v = JVal(json, key);
        if (v == null) return def;
        float result;
        if (float.TryParse(v, System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out result))
            return result;
        return def;
    }

    private static string Esc(string s)
    {
        if (s == null) return "";
        return s.Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\n", "\\n").Replace("\r", "\\r");
    }

    /// <summary>Unescape JSON string sequences: \n \t \r \\ \"</summary>
    private static string JUnescape(string s)
    {
        if (s == null || s.IndexOf('\\') < 0) return s;
        StringBuilder sb = new StringBuilder(s.Length);
        for (int i = 0; i < s.Length; i++)
        {
            if (s[i] == '\\' && i + 1 < s.Length)
            {
                char next = s[i + 1];
                if (next == 'n') { sb.Append('\n'); i++; }
                else if (next == 't') { sb.Append('\t'); i++; }
                else if (next == 'r') { sb.Append('\r'); i++; }
                else if (next == '\\') { sb.Append('\\'); i++; }
                else if (next == '"') { sb.Append('"'); i++; }
                else if (next == '/') { sb.Append('/'); i++; }
                else sb.Append(s[i]);
            }
            else sb.Append(s[i]);
        }
        return sb.ToString();
    }
}
