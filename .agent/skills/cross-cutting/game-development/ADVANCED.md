# Game Development — Advanced Patterns

> Deep-dive content for game-development skill.  
> Load on demand when agent needs full script templates or advanced techniques.

---

## Full Unity C# Script Templates

### 1. Event System — Complete Implementation

```csharp
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Events;

// === GameEvent.cs ===
[CreateAssetMenu(menuName = "Events/GameEvent")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> _listeners = new();

    public void Raise()
    {
        for (int i = _listeners.Count - 1; i >= 0; i--)
            _listeners[i].OnEventRaised();
    }

    public void Register(GameEventListener listener) => _listeners.Add(listener);
    public void Unregister(GameEventListener listener) => _listeners.Remove(listener);
}

// === GameEventListener.cs ===
public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent _event;
    [SerializeField] private UnityEvent _response;

    private void OnEnable() => _event.Register(this);
    private void OnDisable() => _event.Unregister(this);
    public void OnEventRaised() => _response?.Invoke();
}

// Usage: Create GameEvent asset → Attach GameEventListener to objects → Wire response
// GameManager calls myEvent.Raise() → all listeners respond
```

### 2. Object Pool — Generic Reusable Pool

```csharp
using System.Collections.Generic;
using UnityEngine;

// === ObjectPool.cs ===
public class ObjectPool<T> where T : MonoBehaviour
{
    private readonly Queue<T> _pool = new();
    private readonly T _prefab;
    private readonly Transform _parent;
    private readonly int _maxSize;

    public int ActiveCount { get; private set; }
    public int PooledCount => _pool.Count;

    public ObjectPool(T prefab, int initialSize, Transform parent = null, int maxSize = 200)
    {
        _prefab = prefab;
        _parent = parent;
        _maxSize = maxSize;
        for (int i = 0; i < initialSize; i++)
            _pool.Enqueue(CreateNew());
    }

    public T Get()
    {
        T obj;
        if (_pool.Count > 0)
        {
            obj = _pool.Dequeue();
        }
        else if (ActiveCount < _maxSize)
        {
            obj = CreateNew();
        }
        else
        {
            Debug.LogWarning($"Pool max size {_maxSize} reached for {_prefab.name}");
            return null;
        }

        obj.gameObject.SetActive(true);
        ActiveCount++;
        return obj;
    }

    public void Return(T obj)
    {
        obj.gameObject.SetActive(false);
        _pool.Enqueue(obj);
        ActiveCount--;
    }

    private T CreateNew()
    {
        var obj = Object.Instantiate(_prefab, _parent);
        obj.gameObject.SetActive(false);
        return obj;
    }
}
```

### 3. Player Movement — New Input System + CharacterController

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

// === PlayerController.cs ===
[RequireComponent(typeof(CharacterController))]
public class PlayerController : MonoBehaviour
{
    [Header("Movement")]
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float sprintMultiplier = 1.5f;

    [Header("Jump")]
    [SerializeField] private float jumpForce = 7f;
    [SerializeField] private float gravity = -20f;
    [SerializeField] private float coyoteTime = 0.15f;

    [Header("Ground Check")]
    [SerializeField] private Transform groundCheck;
    [SerializeField] private float groundRadius = 0.2f;
    [SerializeField] private LayerMask groundMask;

    private CharacterController _cc;
    private Vector2 _moveInput;
    private float _verticalVelocity;
    private float _coyoteTimer;
    private bool _isGrounded;
    private bool _isSprinting;

    private void Awake() => _cc = GetComponent<CharacterController>();

    private void Update()
    {
        // Ground check
        _isGrounded = Physics.CheckSphere(groundCheck.position, groundRadius, groundMask);
        if (_isGrounded && _verticalVelocity < 0)
        {
            _verticalVelocity = -2f;
            _coyoteTimer = coyoteTime;
        }
        else
        {
            _coyoteTimer -= Time.deltaTime;
        }

        // Horizontal movement
        float speed = _isSprinting ? moveSpeed * sprintMultiplier : moveSpeed;
        Vector3 move = transform.right * _moveInput.x + transform.forward * _moveInput.y;
        _cc.Move(move * speed * Time.deltaTime);

        // Gravity
        _verticalVelocity += gravity * Time.deltaTime;
        _cc.Move(Vector3.up * _verticalVelocity * Time.deltaTime);
    }

    // Input System callbacks
    public void OnMove(InputAction.CallbackContext ctx) => _moveInput = ctx.ReadValue<Vector2>();
    public void OnJump(InputAction.CallbackContext ctx)
    {
        if (ctx.started && _coyoteTimer > 0)
        {
            _verticalVelocity = jumpForce;
            _coyoteTimer = 0;
        }
    }
    public void OnSprint(InputAction.CallbackContext ctx) => _isSprinting = ctx.ReadValueAsButton();
}
```

### 4. Camera Controller — Smooth Follow with Look-Ahead

```csharp
using UnityEngine;

// === CameraFollow.cs ===
public class CameraFollow : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private Vector3 offset = new(0, 8, -10);
    [SerializeField] private float smoothSpeed = 5f;
    [SerializeField] private float lookAheadFactor = 3f;
    [SerializeField] private float lookAheadSmooth = 0.5f;

    private Vector3 _lookAheadPos;
    private Vector3 _currentLookAhead;
    private float _lastTargetX;

    private void LateUpdate()
    {
        if (target == null) return;

        float xDelta = target.position.x - _lastTargetX;
        _lookAheadPos = Vector3.right * (lookAheadFactor * Mathf.Sign(xDelta));
        _currentLookAhead = Vector3.SmoothDamp(_currentLookAhead, _lookAheadPos, ref _currentLookAhead, lookAheadSmooth);

        Vector3 desiredPos = target.position + offset + _currentLookAhead;
        transform.position = Vector3.Lerp(transform.position, desiredPos, smoothSpeed * Time.deltaTime);
        transform.LookAt(target.position + Vector3.up * 2);

        _lastTargetX = target.position.x;
    }
}
```

### 5. UI Manager — Full HUD Implementation

```csharp
using UnityEngine;
using TMPro;
using UnityEngine.UI;

// === UIManager.cs ===
public class UIManager : MonoBehaviour
{
    public static UIManager Instance { get; private set; }

    [Header("HUD")]
    [SerializeField] private TextMeshProUGUI scoreText;
    [SerializeField] private TextMeshProUGUI timerText;
    [SerializeField] private Slider healthSlider;

    [Header("Panels")]
    [SerializeField] private GameObject mainMenuPanel;
    [SerializeField] private GameObject gameOverPanel;
    [SerializeField] private GameObject pausePanel;

    [Header("Game Over")]
    [SerializeField] private TextMeshProUGUI finalScoreText;
    [SerializeField] private TextMeshProUGUI highScoreText;

    private void Awake()
    {
        Instance = this;
        HideAllPanels();
        mainMenuPanel.SetActive(true);
    }

    public void UpdateScore(int score) => scoreText.text = $"Score: {score}";
    public void UpdateTimer(float seconds)
    {
        int min = Mathf.FloorToInt(seconds / 60);
        int sec = Mathf.FloorToInt(seconds % 60);
        timerText.text = $"{min:00}:{sec:00}";
    }
    public void UpdateHealth(float current, float max) => healthSlider.value = current / max;

    public void ShowGameOver(int finalScore, int highScore)
    {
        HideAllPanels();
        gameOverPanel.SetActive(true);
        finalScoreText.text = $"Score: {finalScore}";
        highScoreText.text = $"Best: {highScore}";
    }

    public void TogglePause(bool paused)
    {
        pausePanel.SetActive(paused);
    }

    private void HideAllPanels()
    {
        mainMenuPanel.SetActive(false);
        gameOverPanel.SetActive(false);
        pausePanel.SetActive(false);
    }
}
```

### 6. Score Manager — With Persistence

```csharp
using UnityEngine;

// === ScoreManager.cs ===
public class ScoreManager : MonoBehaviour
{
    public static ScoreManager Instance { get; private set; }

    public int CurrentScore { get; private set; }
    public int HighScore { get; private set; }

    public event System.Action<int> OnScoreChanged;

    private const string HIGH_SCORE_KEY = "HighScore";

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
        HighScore = PlayerPrefs.GetInt(HIGH_SCORE_KEY, 0);
    }

    public void AddScore(int amount)
    {
        CurrentScore += amount;
        OnScoreChanged?.Invoke(CurrentScore);
        UIManager.Instance?.UpdateScore(CurrentScore);
    }

    public void ResetScore()
    {
        if (CurrentScore > HighScore)
        {
            HighScore = CurrentScore;
            PlayerPrefs.SetInt(HIGH_SCORE_KEY, HighScore);
            PlayerPrefs.Save();
        }
        CurrentScore = 0;
        OnScoreChanged?.Invoke(CurrentScore);
    }
}
```

### 7. Audio Manager — Full Implementation

```csharp
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

// === AudioManager.cs ===
public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }

    [Header("Sources")]
    [SerializeField] private AudioSource musicSource;
    [SerializeField] private AudioSource sfxPrefab;

    [Header("Settings")]
    [SerializeField] private int sfxPoolSize = 15;
    [SerializeField] private float musicFadeDuration = 1f;

    private Queue<AudioSource> _sfxPool = new();
    private Coroutine _fadeCoroutine;

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);

        for (int i = 0; i < sfxPoolSize; i++)
        {
            var src = Instantiate(sfxPrefab, transform);
            src.gameObject.SetActive(false);
            _sfxPool.Enqueue(src);
        }
    }

    public void PlaySFX(AudioClip clip, float volume = 1f, float pitch = 1f)
    {
        if (clip == null) return;
        var src = GetPooledSource();
        src.clip = clip;
        src.volume = volume;
        src.pitch = pitch;
        src.Play();
        StartCoroutine(ReturnToPool(src, clip.length / pitch));
    }

    public void PlayMusic(AudioClip clip, bool fade = true)
    {
        if (_fadeCoroutine != null) StopCoroutine(_fadeCoroutine);
        if (fade)
            _fadeCoroutine = StartCoroutine(FadeMusic(clip));
        else
        {
            musicSource.clip = clip;
            musicSource.Play();
        }
    }

    private IEnumerator FadeMusic(AudioClip newClip)
    {
        float startVol = musicSource.volume;
        for (float t = 0; t < musicFadeDuration; t += Time.unscaledDeltaTime)
        {
            musicSource.volume = Mathf.Lerp(startVol, 0, t / musicFadeDuration);
            yield return null;
        }
        musicSource.clip = newClip;
        musicSource.Play();
        for (float t = 0; t < musicFadeDuration; t += Time.unscaledDeltaTime)
        {
            musicSource.volume = Mathf.Lerp(0, startVol, t / musicFadeDuration);
            yield return null;
        }
    }

    private AudioSource GetPooledSource()
    {
        if (_sfxPool.Count > 0)
        {
            var src = _sfxPool.Dequeue();
            src.gameObject.SetActive(true);
            return src;
        }
        return Instantiate(sfxPrefab, transform);
    }

    private IEnumerator ReturnToPool(AudioSource src, float delay)
    {
        yield return new WaitForSeconds(delay + 0.1f);
        src.gameObject.SetActive(false);
        _sfxPool.Enqueue(src);
    }
}
```

---

## Full UE Python Script Templates

### 1. Blueprint Factory — Create Actor Blueprint

```python
import unreal

def create_actor_blueprint(name: str, parent_class=None, output_path="/Game/Blueprints"):
    """Create a new Blueprint asset programmatically."""
    if parent_class is None:
        parent_class = unreal.Actor

    factory = unreal.BlueprintFactory()
    factory.set_editor_property('ParentClass', parent_class)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp = asset_tools.create_asset(name, output_path, None, factory)

    if bp:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
        unreal.log(f"✅ Created Blueprint: {bp.get_path_name()}")
    else:
        unreal.log_error(f"❌ Failed to create Blueprint: {name}")

    return bp

# Usage
create_actor_blueprint("BP_EnemyBase", unreal.Character)
```

### 2. Batch Asset Import — Textures + Meshes

```python
import unreal
import os

def batch_import_assets(source_dir: str, dest_path: str, replace=True):
    """Import all supported files from a directory."""
    supported = {'.png', '.jpg', '.tga', '.fbx', '.obj', '.wav', '.mp3'}
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []

    for f in os.listdir(source_dir):
        ext = os.path.splitext(f)[1].lower()
        if ext in supported:
            task = unreal.AssetImportTask()
            task.set_editor_property('filename', os.path.join(source_dir, f))
            task.set_editor_property('destination_path', dest_path)
            task.set_editor_property('automated', True)
            task.set_editor_property('replace_existing', replace)
            task.set_editor_property('save', True)
            tasks.append(task)

    if tasks:
        asset_tools.import_asset_tasks(tasks)
        unreal.log(f"✅ Imported {len(tasks)} assets to {dest_path}")
    else:
        unreal.log_warning(f"⚠️ No supported files found in {source_dir}")

    return len(tasks)

# Usage
batch_import_assets("C:/GameAssets/Textures", "/Game/Art/Textures")
```

### 3. Level Builder — Scatter Objects

```python
import unreal
import random

def populate_level(mesh_path: str, count: int, area: float = 5000,
                   height_offset: float = 0, random_rotation: bool = True):
    """Scatter static mesh actors across the level."""
    mesh = unreal.load_asset(mesh_path)
    if not mesh:
        unreal.log_error(f"❌ Mesh not found: {mesh_path}")
        return

    spawned = []
    for i in range(count):
        loc = unreal.Vector(
            random.uniform(-area, area),
            random.uniform(-area, area),
            height_offset
        )
        rot = unreal.Rotator(0, random.uniform(0, 360) if random_rotation else 0, 0)

        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, loc, rot
        )
        if actor:
            smc = actor.get_editor_property('static_mesh_component')
            smc.set_editor_property('static_mesh', mesh)
            actor.set_actor_label(f"{mesh.get_name()}_{i:03d}")
            spawned.append(actor)

    unreal.log(f"✅ Spawned {len(spawned)}/{count} actors")
    return spawned

# Usage
populate_level("/Game/Meshes/SM_Tree", 50, area=3000)
```

### 4. Material Creator — Dynamic Material Setup

```python
import unreal

def create_material_instance(parent_material_path: str, name: str,
                              output_path: str, params: dict = None):
    """Create a Material Instance from parent material."""
    parent = unreal.load_asset(parent_material_path)
    if not parent:
        unreal.log_error(f"❌ Parent material not found: {parent_material_path}")
        return None

    factory = unreal.MaterialInstanceConstantFactoryNew()
    factory.set_editor_property('InitialParent', parent)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mi = asset_tools.create_asset(name, output_path, None, factory)

    if mi and params:
        for key, value in params.items():
            if isinstance(value, unreal.LinearColor):
                mi.set_editor_property_by_name(key, value)

    if mi:
        unreal.EditorAssetLibrary.save_loaded_asset(mi)
        unreal.log(f"✅ Created Material Instance: {mi.get_path_name()}")

    return mi
```

### 5. Level Cleanup — Remove Actors by Pattern

```python
import unreal
import re

def cleanup_actors(pattern: str, dry_run: bool = True):
    """Remove actors matching name pattern from current level."""
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    matched = []

    for actor in actors:
        label = actor.get_actor_label()
        if re.match(pattern, label):
            matched.append(actor)

    if dry_run:
        unreal.log(f"🔍 Dry run: would delete {len(matched)} actors:")
        for a in matched[:10]:
            unreal.log(f"  - {a.get_actor_label()}")
        if len(matched) > 10:
            unreal.log(f"  ... and {len(matched) - 10} more")
    else:
        for actor in matched:
            actor.destroy_actor()
        unreal.log(f"✅ Deleted {len(matched)} actors matching '{pattern}'")

    return matched

# Usage
cleanup_actors(r"Tree_\d+", dry_run=True)  # Preview
cleanup_actors(r"Tree_\d+", dry_run=False)  # Execute
```

---

## Advanced Debug Techniques

### Visual Verification Protocol

```
1. CAPTURE   → Request screenshot via bridge endpoint (future)
2. ANALYZE   → Send to multimodal LLM for analysis
3. COMPARE   → Check against GDD expected layout:
               - Player position correct?
               - UI elements visible?
               - Background rendering?
               - No visual glitches?
4. REPORT    → List discrepancies with fix suggestions
5. FIX       → Apply corrections via bridge
```

### Performance Profiling via Bridge

```
Check FPS:
  Unity  → Time.deltaTime monitoring via script
  UE     → stat fps console command

Check Memory:
  Unity  → Profiler.GetTotalAllocatedMemoryLong()
  UE     → stat memory console command

Common Performance Fixes:
  - Enable Object Pooling for frequent spawns
  - Reduce draw calls with sprite atlasing
  - Use LOD (Level of Detail) for 3D meshes
  - Optimize physics with simplified colliders
```

### Multiplayer Basics (Brief)

```
Networking options:
  Unity  → Netcode for GameObjects (NGO) or Photon Fusion
  UE     → Built-in Replication system

Key concepts:
  - Server Authority: Server validates all game state
  - Client Prediction: Input → predict → reconcile
  - State Sync: Replicate variables with [SyncVar] / UPROPERTY(Replicated)

⚠️ Agent support for multiplayer is LIMITED:
  - Can generate boilerplate code
  - CANNOT debug networking issues reliably
  - Recommend: user handles networking architecture
```

---
