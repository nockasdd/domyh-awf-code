---
library: game-patterns-ue
version: 1
latest: true
category: api-tool
official_docs: https://docs.unrealengine.com/
last_updated: 2026-03-28
---

<!-- BM25: game unreal engine UE5 python blueprint asset level automation remote control MCP bridge actor spawn property editor scripting -->

# game-patterns-ue

Unreal Engine 5 Python scripting patterns for agent-assisted game development. Covers 5 essential patterns: Blueprint Creation, Asset Import, Level Population, Build Configuration, and Editor Utility scripting. All patterns designed for use via MCP bridge `ue_execute_python`.

## Installation

### UE Requirements
```
Unreal Engine 5.x (recommended: 5.3+)
Required plugins:
  - Remote Control API (for REST/WS bridge)
  - Python Editor Script Plugin (for ue_execute_python)
```

### Plugin Setup
```
1. Edit > Plugins > search "Remote Control" > Enable
2. Edit > Plugins > search "Python" > Enable "Python Editor Script Plugin"
3. Restart Editor
4. Verify: Window > Developer Tools > Remote Control API
```

### Bridge Configuration
```
# Project Settings > Remote Control API
HTTP Port: 30010    (REST API)
WS Port: 30020      (WebSocket push)
Enable: true

# Python MCP Bridge
Python HTTP Port: 30011  (Native HTTP server for Python execution)
```

## Configuration

### ObjectPath Format
```
/Game/Maps/MyLevel.MyLevel:PersistentLevel.StaticMeshActor_0.StaticMeshComponent0
│     │         │        │                │                  │
│     │         │        │                │                  └─ Component
│     │         │        │                └─ Actor name
│     │         │        └─ Sub-object
│     │         └─ Asset name (duplicated)
│     └─ Content path
└─ Root
```

### Remote Control REST API
```
Base URL: http://127.0.0.1:30010/remote

GET  /remote/object/property         → Read property
PUT  /remote/object/property         → Write property
PUT  /remote/object/call             → Call function
PUT  /remote/batch                   → Multiple operations
GET  /remote/preset/{name}/describe  → Describe preset properties
```

### Project Structure
```
Content/
├── Blueprints/     → BP_Player, BP_Enemy, BP_Projectile
├── Maps/           → Level_Menu, Level_01, Level_02
├── Meshes/         → SM_Platform, SM_Obstacle
├── Materials/      → M_Base, MI_Red, MI_Blue
├── Textures/       → T_Player, T_Enemy
├── Audio/          → Music/, SFX/
├── Python/         → game_setup.py, level_builder.py
└── Data/           → DT_Enemies, DT_Items (DataTables)
```

## Core API

### Pattern 1: Blueprint Creation via Python (v5.0+)

Create new Blueprint assets programmatically.

```python
import unreal

def create_actor_blueprint(name, parent_class=None, output_path="/Game/Blueprints"):
    """Create a new Blueprint asset from Python."""
    if parent_class is None:
        parent_class = unreal.Actor

    factory = unreal.BlueprintFactory()
    factory.set_editor_property('ParentClass', parent_class)

    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp = asset_tools.create_asset(name, output_path, None, factory)

    if bp:
        unreal.EditorAssetLibrary.save_loaded_asset(bp)
        unreal.log(f"Created: {bp.get_path_name()}")
    return bp

# Usage
create_actor_blueprint("BP_Enemy", unreal.Character)
create_actor_blueprint("BP_Projectile", unreal.Actor)
create_actor_blueprint("BP_Pickup", unreal.Actor)
```

### Pattern 2: Batch Asset Import (v5.0+)

Import textures, meshes, and sounds from filesystem.

```python
import unreal
import os

def batch_import(source_dir, dest_path, replace=True):
    """Import all supported files from a directory."""
    SUPPORTED = {'.png', '.jpg', '.tga', '.fbx', '.obj', '.wav', '.mp3', '.ogg'}
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    tasks = []

    for f in os.listdir(source_dir):
        if os.path.splitext(f)[1].lower() in SUPPORTED:
            task = unreal.AssetImportTask()
            task.set_editor_property('filename', os.path.join(source_dir, f))
            task.set_editor_property('destination_path', dest_path)
            task.set_editor_property('automated', True)       # No dialog
            task.set_editor_property('replace_existing', replace)
            task.set_editor_property('save', True)
            tasks.append(task)

    if tasks:
        asset_tools.import_asset_tasks(tasks)
        unreal.log(f"Imported {len(tasks)} assets to {dest_path}")

    return len(tasks)

# Usage
batch_import("C:/Assets/Textures", "/Game/Art/Textures")
batch_import("C:/Assets/Meshes", "/Game/Meshes")
batch_import("C:/Assets/Audio", "/Game/Audio/SFX")
```

⚠️ Always set `automated=True`. Without it, UE shows import dialog for each file.

### Pattern 3: Level Population — Scatter Objects (v5.0+)

Programmatically place actors in the level for greybox prototyping.

```python
import unreal
import random

def populate_level(mesh_path, count, area=5000, height=0, random_rot=True):
    """Scatter static mesh actors across the level."""
    mesh = unreal.load_asset(mesh_path)
    if not mesh:
        unreal.log_error(f"Mesh not found: {mesh_path}")
        return []

    spawned = []
    for i in range(count):
        loc = unreal.Vector(
            random.uniform(-area, area),
            random.uniform(-area, area),
            height
        )
        rot = unreal.Rotator(0, random.uniform(0, 360) if random_rot else 0, 0)

        actor = unreal.EditorLevelLibrary.spawn_actor_from_class(
            unreal.StaticMeshActor, loc, rot
        )
        if actor:
            smc = actor.get_editor_property('static_mesh_component')
            smc.set_editor_property('static_mesh', mesh)
            actor.set_actor_label(f"{mesh.get_name()}_{i:03d}")
            spawned.append(actor)

    unreal.log(f"Spawned {len(spawned)}/{count}")
    return spawned

# Usage — scatter trees and rocks
populate_level("/Game/Meshes/SM_Tree", 50, area=3000)
populate_level("/Game/Meshes/SM_Rock", 30, area=4000)
```

⚠️ Use `EditorLevelLibrary.spawn_actor_from_class` for editor-mode spawning. Runtime-spawned actors are lost when exiting PIE.

### Pattern 4: Build & Package Configuration (v5.0+)

Automate build pipeline settings.

```python
import unreal
import subprocess

def configure_build(platform="Win64", config="Shipping"):
    """Configure project for packaging."""
    # Set packaging settings via Python
    settings = unreal.EditorProjectSettings()

    # Build via command line (alternative to Remote Control)
    # RunUAT.bat BuildCookRun -project=MyGame.uproject -platform=Win64
    # -clientconfig=Shipping -cook -build -stage -pak -archive

    unreal.log(f"Build configured for {platform}/{config}")

def get_project_stats():
    """Get current project statistics."""
    # Count assets
    registry = unreal.AssetRegistryHelpers.get_asset_registry()

    meshes = registry.get_assets_by_class(unreal.TopLevelAssetPath('/Script/Engine', 'StaticMesh'))
    textures = registry.get_assets_by_class(unreal.TopLevelAssetPath('/Script/Engine', 'Texture2D'))
    blueprints = registry.get_assets_by_class(unreal.TopLevelAssetPath('/Script/Engine', 'Blueprint'))

    unreal.log(f"Project stats: {len(meshes)} meshes, {len(textures)} textures, {len(blueprints)} blueprints")
```

### Pattern 5: Editor Utility Scripts (v5.0+)

Custom editor tools for asset management and level cleanup.

```python
import unreal
import re

def batch_rename(pattern, replacement, dry_run=True):
    """Rename selected assets matching pattern."""
    selected = unreal.EditorUtilityLibrary.get_selected_assets()
    renames = []

    for asset in selected:
        old = asset.get_name()
        new = re.sub(pattern, replacement, old)
        if old != new:
            renames.append((asset, old, new))

    if dry_run:
        for _, old, new in renames:
            unreal.log(f"  {old} → {new}")
        unreal.log(f"Dry run: {len(renames)} would be renamed")
    else:
        for asset, old, new in renames:
            path = asset.get_path_name()
            parent = "/".join(path.split("/")[:-1])
            unreal.EditorAssetLibrary.rename_asset(path, f"{parent}/{new}")
        unreal.log(f"Renamed {len(renames)} assets")

def cleanup_actors(label_pattern, dry_run=True):
    """Remove actors matching name pattern from level."""
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    matched = [a for a in actors if re.match(label_pattern, a.get_actor_label())]

    if dry_run:
        unreal.log(f"Would delete {len(matched)} actors")
    else:
        for a in matched:
            a.destroy_actor()
        unreal.log(f"Deleted {len(matched)} actors")

# Usage
batch_rename(r"^SM_(\w+)$", r"SM_Prop_\1", dry_run=True)
cleanup_actors(r"Tree_\d+", dry_run=False)
```

## Common Patterns

### Reading Actor Properties via REST

```json
// GET /remote/object/property
{
  "objectPath": "/Game/Maps/Level.Level:PersistentLevel.BP_Player_0",
  "propertyName": "RelativeLocation",
  "access": "READ_ACCESS"
}
```

### Modifying Actor Properties via REST

```json
// PUT /remote/object/property
{
  "objectPath": "/Game/Maps/Level.Level:PersistentLevel.BP_Player_0",
  "propertyName": "RelativeLocation",
  "propertyValue": { "X": 100.0, "Y": 200.0, "Z": 50.0 },
  "access": "WRITE_ACCESS"
}
```

### Batch Operations

```json
// PUT /remote/batch
{
  "Requests": [
    {
      "RequestId": 1,
      "URL": "/remote/object/property",
      "Body": { "objectPath": "...", "propertyName": "...", "access": "READ_ACCESS" }
    },
    {
      "RequestId": 2,
      "URL": "/remote/object/call",
      "Body": { "objectPath": "...", "functionName": "..." }
    }
  ]
}
```

⚠️ Batch responses are keyed by `RequestId`, NOT by array index. Always match by ID.

## Gotchas

⚠️ Remote Control 404 → Plugin "Remote Control API" not enabled. Edit > Plugins > search > Enable > Restart.

⚠️ PropertyName is **case-sensitive**. Use `/remote/preset/{name}/describe` to list exact names before setting.

⚠️ `ue_execute_python` has **NO SANDBOX**. Python runs with full editor permissions. Never: delete outside project, access network, modify Engine/ files.

⚠️ Runtime-spawned actors lost on PIE exit → Use `EditorLevelLibrary.spawn_actor_from_class` for persistent changes.

⚠️ `unreal.is_valid(obj)` check required before accessing any UObject. Accessing invalid object crashes editor.

⚠️ Assets not saved after Python modification → Call `unreal.EditorAssetLibrary.save_loaded_asset(asset)`.

⚠️ Python `import` fails for project modules → Add to sys.path: `sys.path.append(unreal.Paths.project_content_dir() + 'Python')`.

⚠️ Editor slows after many Python executions → Call `import gc; gc.collect()` periodically.

⚠️ Function not callable via Remote Control → Only `UFUNCTION(BlueprintCallable)` or `UFUNCTION(Exec)` are exposed.

⚠️ WebSocket events not arriving → Wrong port. REST = 30010, WebSocket = 30020. Register presets via WS only.

---
