---
library: game-patterns-unity
version: 1
latest: true
category: api-tool
official_docs: https://docs.unity3d.com/ScriptReference/
last_updated: 2026-03-28
---

<!-- BM25: game unity C# script pattern event pooling state machine input system URP gameobject component monobehaviour new input system camera movement UI audio -->

# game-patterns-unity

Unity C# game development patterns for agent-assisted game creation. Covers 7 essential patterns: Event System, Object Pooling, State Machine, Player Movement (New Input System), Camera Controller, UI Manager, and Audio Manager.

## Installation

### Unity Requirements
```
Unity 2022.3+ LTS (recommended: 2023.2+)
Required packages:
  - com.unity.inputsystem >= 1.7.0
  - com.unity.textmeshpro >= 3.0.0
Optional packages:
  - com.unity.cinemachine >= 2.9.0
  - com.unity.2d.sprite >= 1.0.0 (for 2D games)
```

### Project Setup
```
1. Window > Package Manager > Install "Input System"
2. When prompted: "Enable New Input System backend?" → YES
3. Verify: Project Settings > Player > Active Input Handling = "Input System Package (New)"
4. Create Input Actions asset: Assets > Create > Input Actions
```

## Configuration

### URP Setup (Default for new games)
```
1. New project → Select "Universal 2D" or "Universal 3D" template
2. If converting existing: Window > Rendering > Render Pipeline Converter
3. All materials must use URP shaders (Lit, Unlit, Sprite-Unlit-Default)
```

### Recommended Project Structure
```
Assets/
├── Scripts/
│   ├── Core/          → GameManager, ScoreManager, AudioManager
│   ├── Player/        → PlayerController, HealthSystem
│   ├── Enemies/       → EnemyAI, EnemySpawner
│   ├── UI/            → UIManager, MenuController
│   └── Utils/         → ObjectPool, EventSystem
├── Prefabs/           → Player, Enemy, Projectile, UI panels
├── Scenes/            → Menu, Level1, Level2, GameOver
├── ScriptableObjects/ → GameEvents, ItemData, EnemyData
├── Art/               → Sprites, Animations, Materials
├── Audio/             → Music/, SFX/
└── Input/             → PlayerControls.inputactions
```

## Core API

### Pattern 1: ScriptableObject Event System (v2022+)

Decoupled inter-system communication. Zero tight coupling between systems.

```csharp
// GameEvent.cs — Create as asset: Assets > Create > Events > GameEvent
[CreateAssetMenu(menuName = "Events/GameEvent")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> _listeners = new();

    public void Raise()
    {
        // Iterate backwards to safely handle listener removal during raise
        for (int i = _listeners.Count - 1; i >= 0; i--)
            _listeners[i].OnEventRaised();
    }

    public void Register(GameEventListener listener) => _listeners.Add(listener);
    public void Unregister(GameEventListener listener) => _listeners.Remove(listener);
}

// GameEventListener.cs — Attach to any GameObject
public class GameEventListener : MonoBehaviour
{
    [SerializeField] private GameEvent _event;
    [SerializeField] private UnityEvent _response;

    private void OnEnable() => _event.Register(this);
    private void OnDisable() => _event.Unregister(this);
    public void OnEventRaised() => _response?.Invoke();
}
```

Usage flow: Create GameEvent asset → Attach GameEventListener to receiver → Wire UnityEvent response → Sender calls `.Raise()`.

### Pattern 2: Generic Object Pool (v2022+)

Eliminates GC spikes from Instantiate/Destroy. Critical for bullets, particles, enemies.

```csharp
public class ObjectPool<T> where T : MonoBehaviour
{
    private readonly Queue<T> _pool = new();
    private readonly T _prefab;
    private readonly Transform _parent;
    private readonly int _maxSize;
    public int ActiveCount { get; private set; }

    public ObjectPool(T prefab, int initialSize, Transform parent = null, int maxSize = 200)
    {
        _prefab = prefab; _parent = parent; _maxSize = maxSize;
        for (int i = 0; i < initialSize; i++) _pool.Enqueue(CreateNew());
    }

    public T Get()
    {
        T obj = _pool.Count > 0 ? _pool.Dequeue() : (ActiveCount < _maxSize ? CreateNew() : null);
        if (obj == null) { Debug.LogWarning($"Pool max reached: {_maxSize}"); return null; }
        obj.gameObject.SetActive(true); ActiveCount++;
        return obj;
    }

    public void Return(T obj) { obj.gameObject.SetActive(false); _pool.Enqueue(obj); ActiveCount--; }
    private T CreateNew() { var o = Object.Instantiate(_prefab, _parent); o.gameObject.SetActive(false); return o; }
}
```

### Pattern 3: Enum-Based State Machine (v2022+)

Game flow control with state transitions and event broadcasting.

```csharp
public enum GameState { Menu, Playing, Paused, GameOver }

public class GameManager : MonoBehaviour
{
    public static GameManager Instance { get; private set; }
    public GameState CurrentState { get; private set; }
    public event System.Action<GameState> OnStateChanged;

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }

    public void ChangeState(GameState newState)
    {
        if (CurrentState == newState) return;
        CurrentState = newState;
        OnStateChanged?.Invoke(newState);
        Time.timeScale = newState is GameState.Paused or GameState.GameOver ? 0f : 1f;
    }
}
```

### Pattern 4: Player Movement — New Input System (v2022+)

Modern input handling with CharacterController. Includes coyote time and sprint.

```csharp
using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(CharacterController))]
public class PlayerController : MonoBehaviour
{
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 7f;
    [SerializeField] private float gravity = -20f;
    [SerializeField] private float coyoteTime = 0.15f;

    private CharacterController _cc;
    private Vector2 _moveInput;
    private float _verticalVelocity;
    private float _coyoteTimer;

    private void Awake() => _cc = GetComponent<CharacterController>();

    private void Update()
    {
        bool grounded = _cc.isGrounded;
        if (grounded && _verticalVelocity < 0) { _verticalVelocity = -2f; _coyoteTimer = coyoteTime; }
        else _coyoteTimer -= Time.deltaTime;

        Vector3 move = transform.right * _moveInput.x + transform.forward * _moveInput.y;
        _cc.Move(move * moveSpeed * Time.deltaTime);

        _verticalVelocity += gravity * Time.deltaTime;
        _cc.Move(Vector3.up * _verticalVelocity * Time.deltaTime);
    }

    // New Input System callbacks
    public void OnMove(InputAction.CallbackContext ctx) => _moveInput = ctx.ReadValue<Vector2>();
    public void OnJump(InputAction.CallbackContext ctx)
    {
        if (ctx.started && _coyoteTimer > 0) { _verticalVelocity = jumpForce; _coyoteTimer = 0; }
    }
}
```

⚠️ **Do NOT use** `Input.GetAxis()` or `Input.GetButtonDown()` — these are legacy Input Manager APIs. Always use `InputAction.CallbackContext` with the New Input System.

### Pattern 5: Camera Follow Controller (v2022+)

Smooth camera follow with look-ahead for side-scrollers and third-person.

```csharp
public class CameraFollow : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private Vector3 offset = new(0, 5, -10);
    [SerializeField] private float smoothSpeed = 5f;

    private void LateUpdate()
    {
        if (target == null) return;
        var desired = target.position + offset;
        transform.position = Vector3.Lerp(transform.position, desired, smoothSpeed * Time.deltaTime);
        transform.LookAt(target);
    }
}
```

### Pattern 6: UI Manager (v2022+)

Canvas-based HUD management with panels and score display.

```csharp
using TMPro;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    public static UIManager Instance { get; private set; }
    [SerializeField] private TextMeshProUGUI scoreText;
    [SerializeField] private GameObject gameOverPanel;
    [SerializeField] private GameObject pausePanel;

    private void Awake() { Instance = this; gameOverPanel.SetActive(false); pausePanel.SetActive(false); }
    public void UpdateScore(int score) => scoreText.text = $"Score: {score}";
    public void ShowGameOver() => gameOverPanel.SetActive(true);
    public void TogglePause(bool p) => pausePanel.SetActive(p);
}
```

⚠️ Canvas must have `CanvasScaler` set to "Scale With Screen Size" with reference resolution 1920×1080.

### Pattern 7: Audio Manager — Pool-based (v2022+)

SFX pooling + music fade transitions.

```csharp
public class AudioManager : MonoBehaviour
{
    public static AudioManager Instance { get; private set; }
    [SerializeField] private AudioSource musicSource;
    [SerializeField] private AudioSource sfxPrefab;
    private Queue<AudioSource> _sfxPool = new();

    private void Awake()
    {
        if (Instance != null) { Destroy(gameObject); return; }
        Instance = this; DontDestroyOnLoad(gameObject);
        for (int i = 0; i < 10; i++) { var s = Instantiate(sfxPrefab, transform); s.gameObject.SetActive(false); _sfxPool.Enqueue(s); }
    }

    public void PlaySFX(AudioClip clip, float vol = 1f)
    {
        var src = _sfxPool.Count > 0 ? _sfxPool.Dequeue() : Instantiate(sfxPrefab, transform);
        src.gameObject.SetActive(true); src.clip = clip; src.volume = vol; src.Play();
        StartCoroutine(ReturnAfter(src, clip.length));
    }

    public void PlayMusic(AudioClip clip) { musicSource.clip = clip; musicSource.loop = true; musicSource.Play(); }

    private System.Collections.IEnumerator ReturnAfter(AudioSource s, float t)
    { yield return new WaitForSeconds(t + 0.1f); s.gameObject.SetActive(false); _sfxPool.Enqueue(s); }
}
```

## Common Patterns

### Scene Management Flow
```csharp
using UnityEngine.SceneManagement;
// Load: SceneManager.LoadScene("Level1");
// Async: SceneManager.LoadSceneAsync("Level1");
// Additive: SceneManager.LoadScene("UI", LoadSceneMode.Additive);
```

### ScriptableObject Data Pattern
```csharp
[CreateAssetMenu(menuName = "Data/EnemyData")]
public class EnemyData : ScriptableObject
{
    public string enemyName;
    public float health = 100f;
    public float speed = 3f;
    public float damage = 10f;
    public Sprite sprite;
}
```

### Singleton with Initialization
```csharp
// Standard singleton pattern for managers
public class T : MonoBehaviour where T is derived
{
    // Awake: null check → assign → DontDestroyOnLoad
    // Always check: if (Instance != null) { Destroy(gameObject); return; }
}
```

## Gotchas

⚠️ `rb.velocity` → Use `rb.linearVelocity` in Unity 6+. The API was renamed for clarity between linear and angular velocity.

⚠️ `FindObjectOfType<T>()` every frame → Cache in `Awake()`. This searches the entire scene hierarchy and is O(n) per call.

⚠️ `Input.GetButtonDown("Jump")` → Legacy. Use New Input System `InputAction.CallbackContext.ReadValue<T>()` with PlayerInput component.

⚠️ BIRP (Built-in Render Pipeline) → Deprecated for new projects. Use URP. BIRP materials won't render correctly in URP without conversion.

⚠️ Physics in `Update()` → Move to `FixedUpdate()`. Physics simulation runs at fixed timestep; Update runs at frame rate causing jitter.

⚠️ No `DontDestroyOnLoad` on managers → Objects destroyed on scene change. Add to all Singleton managers.

⚠️ String concatenation in `Update()` → GC allocations every frame. Use `StringBuilder` or update text only on value change.

⚠️ Canvas without Scaler → UI won't scale on different screens. Set Canvas Scaler to "Scale With Screen Size".

⚠️ Multiple Singleton instances → No duplicate check in `Awake()`. Always: `if (Instance != null) { Destroy(gameObject); return; }`

⚠️ Coroutines stop on `OnDisable` → MonoBehaviour stops all coroutines when disabled. Use a persistent runner or DOTween.

---
