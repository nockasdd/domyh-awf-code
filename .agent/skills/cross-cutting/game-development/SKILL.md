---
name: game-development
description: "Game development pipeline from concept to gold master. Unity C#/URP and Unreal Engine Python/Blueprint. Use when creating, debugging, or modifying games via MCP bridge. Text-to-game automation."
detect: ["*.unity", "*.uproject", "*.umap", "ProjectSettings/*.asset", "Config/DefaultEngine.ini"]
category: cross-cutting
tier: 1
---

# Game Development Pipeline — DOMYH Awesome Code

> **Engines**: Unity 2022+ (C#/URP) · Unreal Engine 5.x (Python/Blueprint)
> **Philosophy**: Agent-assisted game creation via MCP bridge — from prompt to playable

---

## 🌳 Decision Tree

```
Task → What game development action?
  ├─ Engine Detection
  │   ├─ *.unity / *.cs / ProjectSettings/ → Unity
  │   ├─ *.uproject / *.umap / Config/    → Unreal Engine
  │   └─ No project files                 → Ask user, default Unity
  │
  ├─ Phase Detection
  │   ├─ "create game / tạo game / new game"  → Phase 1: Concept + GDD
  │   ├─ "prototype / greybox / scaffold"     → Phase 2: Pre-production
  │   ├─ "add feature / implement / code"     → Phase 3: Production
  │   ├─ "fix bug / debug / error"            → Phase 4: QA
  │   ├─ "build / export / package"           → Phase 5: Launch
  │   └─ "update / patch / DLC"               → Phase 6: Post-launch
  │
  ├─ Genre Detection (for new games)
  │   ├─ "flappy / endless / runner"   → Endless Runner template
  │   ├─ "platform / jump / mario"     → Platformer template
  │   ├─ "shoot / gun / arena"         → Shooter template
  │   ├─ "puzzle / match / logic"      → Puzzle template
  │   ├─ "rpg / quest / inventory"     → RPG template
  │   ├─ "tower / defense / wave"      → Tower Defense template
  │   └─ "card / deck / battle"        → Card Game template
  │
  └─ Action Type
      ├─ Create → GDD → Scaffold → Build → Debug → Verify
      ├─ Modify → Load project → Identify target → Apply → Verify
      └─ Debug  → Read logs → Identify error → Fix → Compile → Verify
```

---

## 🎯 When to Use This Skill

- User wants to **create a game** from scratch (text-to-game)
- User wants to **modify an existing game** (add features, change mechanics)
- User wants to **debug a game** (fix bugs, optimize performance)
- User mentions "game", "Unity game", "UE game", "tạo game", "gamedev"
- Project contains `.unity`, `.uproject`, `.cs` game scripts

**NOT for**: Web apps (→ react/nextjs), mobile apps (→ flutter/react-native), 3D art creation (needs artist)

**Prerequisites**: Unity Editor or UE Editor must be OPEN with HSA MCP bridge running.

---

## 📋 6-Phase Pipeline Overview

| Phase | Name | Duration | Agent Coverage | Key Deliverable |
|:------|:-----|:---------|:-------------|:---------------|
| 1 | **Concept** | 1-4 weeks | 90% | GDD.json |
| 2 | **Pre-Production** | 1-6 months | 70% | Greybox Prototype |
| 3 | **Production** | 3-24 months | 50% | Content-Complete (Alpha) |
| 4 | **QA & Polish** | 1-6 months | 60% | Bug-free (Beta) |
| 5 | **Launch** | 1-4 weeks | 40% | Gold Master Build |
| 6 | **Post-Launch** | Ongoing | 50% | Patches & DLC |

### Phase 1: Concept (Agent = 90%)

```
User prompt → Parse intent → Select genre template → Generate GDD.json
```

```json
{
  "meta": {
    "title": "Game Title",
    "genre": "platformer",
    "engine": "unity",
    "target_platform": "pc"
  },
  "core_loop": {
    "action": "jump between platforms",
    "challenge": "avoid obstacles, reach goal",
    "reward": "coins, score, checkpoint",
    "fail_condition": "fall off screen or hit hazard"
  },
  "systems": {
    "physics": { "gravity": -9.81, "jump_force": 7.0 },
    "spawner": { "type": "level-based", "difficulty_curve": "linear" },
    "scoring": { "type": "incremental", "display": "UI_text" }
  },
  "scripts_needed": ["PlayerController", "GameManager", "ScoreManager", "LevelLoader"],
  "assets_needed": {
    "sprites": ["player", "platform", "coin", "hazard", "background"],
    "audio": ["jump_sfx", "coin_sfx", "death_sfx", "bg_music"]
  }
}
```

### Phase 2-4: Build → Debug Loop

```
1. SCAFFOLD  → Create GameObjects/Actors from GDD
2. CODE      → Generate scripts from patterns.yaml
3. COMPILE   → unity_compile_scripts / ue build
4. LOG CHECK → Parse compilation errors + runtime logs
5. FIX       → Auto-fix common errors (see gotchas.yaml)
6. VERIFY    → Visual check (screenshot if available)
7. REPEAT    → Max 5 iterations (rule GCS_006)
```

---

## 🔧 Core Bridge Actions (Quick Reference)

### Unity (via WebSocket ws://127.0.0.1:15557)

| Action | Command | Use Case |
|:-------|:--------|:---------|
| Get scene tree | `get_hierarchy` | Understand current scene |
| Get object info | `get_object(path)` | Read component values |
| Set property | `set_property(path, comp, field, value)` | Modify any field |
| Create object | `create_object(type, name)` | Add new GameObjects |
| Destroy object | `destroy_object(path)` | Remove GameObjects |
| Search assets | `get_assets(filter, folder)` | Find prefabs/materials |
| Load scene | `load_scene(scenePath)` | Switch scenes |
| Save scene | `save_scene()` | Persist changes |
| Compile | `compile_scripts()` | Trigger recompilation |
| Build | `build_player(scenes, output, target)` | Export final build |

### Unreal Engine (via REST http://127.0.0.1:30010)

| Action | Endpoint | Use Case |
|:-------|:---------|:---------|
| Read property | `GET /remote/object/property` | Read UObject values |
| Write property | `PUT /remote/object/property` | Modify UObject values |
| Call function | `PUT /remote/object/call` | Execute UFUNCTION |
| Batch ops | `PUT /remote/batch` | Multiple ops at once |
| Execute Python | `ue_execute_python(script)` | Run Python in editor |

> 📚 Full API details: `hsa_search(action:'docs', doc_libraries:['plugin-unity-editor'])` or `['plugin-unreal-engine']`

---

## 📝 Essential Patterns (Compact)

### Pattern 1: Event System (Unity C#)

```csharp
// ScriptableObject-based — decoupled communication
[CreateAssetMenu(menuName = "Events/GameEvent")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> _listeners = new();

    public void Raise() {
        for (int i = _listeners.Count - 1; i >= 0; i--)
            _listeners[i].OnEventRaised();
    }

    public void Register(GameEventListener listener) => _listeners.Add(listener);
    public void Unregister(GameEventListener listener) => _listeners.Remove(listener);
}

public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent _event;
    [SerializeField] private UnityEvent _response;

    private void OnEnable() => _event.Register(this);
    private void OnDisable() => _event.Unregister(this);
    public void OnEventRaised() => _response?.Invoke();
}
```

### Pattern 2: Object Pooling (Unity C#)

```csharp
public class ObjectPool<T> where T : MonoBehaviour
{
    private readonly Queue<T> _pool = new();
    private readonly T _prefab;
    private readonly Transform _parent;

    public ObjectPool(T prefab, int initialSize, Transform parent = null)
    {
        _prefab = prefab;
        _parent = parent;
        for (int i = 0; i < initialSize; i++)
            _pool.Enqueue(CreateNew());
    }

    public T Get()
    {
        var obj = _pool.Count > 0 ? _pool.Dequeue() : CreateNew();
        obj.gameObject.SetActive(true);
        return obj;
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
    }

    private T CreateNew()
    {
        var obj = Object.Instantiate(_prefab, _parent);
        obj.gameObject.SetActive(false);
        return obj;
    }
}
```

### Pattern 3: State Machine (Unity C#)

```csharp
public enum GameState { Menu, Playing, Paused, GameOver }

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }

    private GameState _currentState;
    public GameState CurrentState => _currentState;

    public event System.Action<GameState> OnStateChanged;

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void ChangeState(GameState newState)
    {
        if (_currentState == newState) return;
        _currentState = newState;
        OnStateChanged?.Invoke(newState);

        switch (newState)
        {
            case GameState.Menu:    Time.timeScale = 1f; break;
            case GameState.Playing: Time.timeScale = 1f; break;
            case GameState.Paused:  Time.timeScale = 0f; break;
            case GameState.GameOver: Time.timeScale = 0f; break;
        }
    }
}
```

> 🔍 Full templates (7 Unity + 5 UE patterns): See [ADVANCED.md](./ADVANCED.md)

---

## 🐛 Debug Loop Protocol

```
┌───────────────────────────────────────────┐
│        GAME DEBUG LOOP (Max 5 iter)       │
│                                           │
│  1. COMPILE → unity_compile_scripts()     │
│       ↓                                   │
│  2. CHECK LOGS → Parse errors/warnings    │
│       ↓                                   │
│  3. IDENTIFY → Match against gotchas.yaml │
│       ↓                                   │
│  4. FIX → Apply auto-fix or generate fix  │
│       ↓                                   │
│  5. VERIFY → Re-compile + runtime check   │
│       ↓                                   │
│  ✅ Pass → Continue    ❌ Fail → Loop     │
│  ⚠️ 5 failures → Escalate to user        │
└───────────────────────────────────────────┘
```

### Common Error Categories

| Category | Example | Auto-Fix? |
|:---------|:--------|:----------|
| Compile error | Missing `;`, wrong type | ✅ Yes |
| Missing reference | NullReferenceException | ✅ Usually |
| Missing component | `GetComponent<T>()` returns null | ✅ Add component |
| Scene structure | Object at wrong position | ✅ Via bridge |
| Logic error | Wrong calculation, bad timing | ⚠️ Partial |
| Visual bug | Wrong sprite, misaligned UI | ⚠️ Needs screenshot |
| Performance | Low FPS, GC spikes | ⚠️ Profiling needed |

> 📚 Full debug protocol: See [references/debug-loop.md](./references/debug-loop.md)

---

## ⚠️ Critical Gotchas (Top 10)

| # | Engine | Problem | Fix |
|:--|:-------|:--------|:----|
| 1 | Unity | `rb.velocity` deprecated in Unity 6+ | Use `rb.linearVelocity` |
| 2 | Unity | `FindObjectOfType` every frame = slow | Cache reference in `Awake()` |
| 3 | Unity | `Input.GetButtonDown` is legacy | Use New Input System `ReadValue<T>()` |
| 4 | Unity | BIRP rendering = outdated | Default to URP (Universal Render Pipeline) |
| 5 | Unity | No `DontDestroyOnLoad` = objects destroyed | Add to persistent managers |
| 6 | UE | Remote Control 404 | Plugin "Remote Control API" not enabled |
| 7 | UE | PropertyName case-sensitive | Exact match required — use describe endpoint |
| 8 | UE | `ue_execute_python` no sandbox | NEVER access files outside project |
| 9 | Both | Too many spawned objects | Max 100/session (rule GCS_002) |
| 10 | Both | No scene save before edit | Always `save_scene` first (rule GCS_003) |

> 📚 Full gotchas list (40 entries): See [data/gotchas.yaml](./data/gotchas.yaml)

---

## ✅ Game Development Checklist

### Before Starting
- [ ] Engine editor is OPEN and running
- [ ] MCP bridge responding (health check)
- [ ] Scene saved before modifications

### During Development
- [ ] GDD.json generated and validated
- [ ] Scripts follow patterns from data/patterns.yaml
- [ ] New Input System used (not legacy)
- [ ] URP configured (not BIRP)
- [ ] Object pooling for high-frequency spawns
- [ ] Event system for decoupled communication

### Before Shipping
- [ ] All compile errors resolved
- [ ] Debug loop passed (0 runtime errors)
- [ ] Visual verification completed
- [ ] Performance acceptable (target FPS met)
- [ ] Build exported successfully

---
