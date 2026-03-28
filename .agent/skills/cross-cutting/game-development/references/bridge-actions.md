# Bridge Actions Quick Reference — Game Development

> All MCP bridge tool actions for Unity and Unreal Engine.
> Use via: `hsa_bridge({target:'unity|ue', action:'...', payload:{...}})`

---

## Unity Bridge Actions (14 commands)

Target: `unity` | Protocol: WebSocket `ws://127.0.0.1:15557` or HTTP `http://127.0.0.1:30030`

| Action | Payload | Response | Use Case |
|:-------|:--------|:---------|:---------|
| `get_hierarchy` | `{}` | Scene tree with all GameObjects | Understand scene structure |
| `get_object` | `{ path: "/Player" }` | Object details + components | Read component values |
| `set_property` | `{ path: "/Player", component: "Transform", field: "position", value: [0,1,0] }` | Success/fail | Modify any property |
| `create_object` | `{ type: "Empty/Cube/Sphere/Capsule/Plane/Cylinder", name: "MyObj" }` | Created object path | Add new GameObjects |
| `create_object` | `{ type: "Empty", name: "MyObj", parent: "/Canvas" }` | Created UI object | Add UI elements |
| `destroy_object` | `{ path: "/OldObj" }` | Success/fail | Remove GameObjects |
| `get_assets` | `{ filter: "t:Prefab", folder: "Assets/Prefabs" }` | Asset list with paths | Find project assets |
| `load_scene` | `{ scenePath: "Assets/Scenes/Level1.unity" }` | Success/fail | Switch active scene |
| `save_scene` | `{}` | Success/fail | Persist scene changes |
| `compile_scripts` | `{}` | Compilation result | Trigger C# recompilation |
| `get_logs` | `{ count: 50 }` | Recent console logs | Read errors/warnings |
| `build_player` | `{ scenes: [...], outputPath: "...", target: "StandaloneWindows64" }` | Build result | Export game build |
| `execute_menu` | `{ menuPath: "Edit/Project Settings..." }` | Success/fail | Trigger menu actions |
| `get_components` | `{ path: "/Player" }` | List of attached components | Inspect object setup |

### Unity Example Flow: Create Flappy Bird

```javascript
// 1. Understand scene
hsa_bridge({target:'unity', action:'get_hierarchy'})

// 2. Create player
hsa_bridge({target:'unity', action:'create_object', payload:{type:'Sphere', name:'Bird'}})
hsa_bridge({target:'unity', action:'set_property', payload:{
  path:'/Bird', component:'Transform', field:'position', value:[0, 3, 0]
}})

// 3. Create pipe spawner
hsa_bridge({target:'unity', action:'create_object', payload:{type:'Empty', name:'PipeSpawner'}})
hsa_bridge({target:'unity', action:'set_property', payload:{
  path:'/PipeSpawner', component:'Transform', field:'position', value:[10, 0, 0]
}})

// 4. Save and compile
hsa_bridge({target:'unity', action:'save_scene'})
hsa_bridge({target:'unity', action:'compile_scripts'})

// 5. Check for errors
hsa_bridge({target:'unity', action:'get_logs', payload:{count: 20}})
```

---

## Unreal Engine Bridge Actions (6 commands)

Target: `ue` | Protocol: REST `http://127.0.0.1:30010` + Python `http://127.0.0.1:30011`

| Action | Payload | Response | Use Case |
|:-------|:--------|:---------|:---------|
| `ue_get_property` | `{ objectPath: "/Game/...", propertyName: "RelativeLocation" }` | Property value | Read UObject values |
| `ue_set_property` | `{ objectPath: "/Game/...", propertyName: "...", propertyValue: {...} }` | Success/fail | Modify UObject values |
| `ue_call_function` | `{ objectPath: "/Game/...", functionName: "...", parameters: {...} }` | Function result | Execute UFUNCTION |
| `ue_batch` | `{ requests: [{...}, {...}] }` | Batch results | Multiple ops at once |
| `ue_execute_python` | `{ script: "import unreal\n..." }` | Script output | Run Python in editor |
| `ue_search_assets` | `{ classPath: "/Script/Engine.StaticMesh", filter: "SM_" }` | Asset list | Find project assets |

### UE ObjectPath Format

```
/Game/Maps/MyLevel.MyLevel:PersistentLevel.StaticMeshActor_0.StaticMeshComponent0
│     │         │        │                │                  │
│     │         │        │                │                  └─ Component name
│     │         │        │                └─ Actor name
│     │         │        └─ Sub-object level
│     │         └─ Asset name (duplicated)
│     └─ Content folder path
└─ Root
```

### UE Example Flow: Populate Level

```javascript
// 1. Execute Python to scatter objects
hsa_bridge({target:'ue', action:'ue_execute_python', payload:{
  script: `
import unreal
import random
mesh = unreal.load_asset('/Game/Meshes/SM_Rock')
for i in range(20):
    loc = unreal.Vector(random.uniform(-3000,3000), random.uniform(-3000,3000), 0)
    actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
        unreal.StaticMeshActor, loc, unreal.Rotator(0, random.uniform(0,360), 0)
    )
    actor.get_editor_property('static_mesh_component').set_editor_property('static_mesh', mesh)
    actor.set_actor_label(f'Rock_{i:03d}')
unreal.log(f'Spawned 20 rocks')
`
}})

// 2. Search for spawned assets
hsa_bridge({target:'ue', action:'ue_search_assets', payload:{
  classPath: '/Script/Engine.StaticMeshActor',
  filter: 'Rock_'
}})
```

---

## Connection Troubleshooting

| Problem | Engine | Solution |
|:--------|:-------|:---------|
| Connection refused | Unity | Unity Editor not running or MCP bridge plugin not installed |
| Connection refused | UE | UE Editor not running or Remote Control API plugin not enabled |
| 404 Not Found | UE | Wrong ObjectPath or function not UFUNCTION(BlueprintCallable) |
| Timeout | Both | Editor busy (compiling, importing). Wait and retry |
| Wrong port | Unity | Check WebSocket port in plugin settings (default: 15557) |
| Wrong port | UE | Check Remote Control API settings (default: 30010) |

---
