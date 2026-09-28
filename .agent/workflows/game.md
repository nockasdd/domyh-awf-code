---
description: Tạo, sửa, debug game tự động qua Unity/UE MCP bridge
---

# 🎮 /game — Game Development Pipeline

> Text-to-Game automation via MCP bridge
> 📋 GDD Generation • Scaffolding • Build • Debug • Visual Verify

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | MUST check bridge health BEFORE any operation (GCS_001) | Safety |
| R2 | Max 100 spawned objects per session (GCS_002) | Safety |
| R3 | MUST save scene before destructive operations (GCS_003) | Safety |
| R4 | Default: New Input System + URP for Unity (GCS_004/005) | Convention |
| R5 | Max 5 debug loop iterations (GCS_006) | Safety |

> Rules source: `.agent/rules/modules/game-editor-safety.yaml`

---

## STEP 0: PREFLIGHT — pick a branch, do not assume

Run this **first**, every time. A hard failure here is cheaper than a wrong assumption.

```
1. hsa_detect(action:"stack")                     → engine + project type
2. Glob: *.unity | *.uproject | project.godot | ProjectSettings/ProjectVersion.txt
3. hsa_bridge({target:'unity|ue', action:'status'})   (GCS_001)
```

| Detected | Editor reachable | Route |
|:---------|:-----------------|:------|
| Unity project | yes | **A — Adopting existing project** |
| Unity project | no | **B — User must open Editor** |
| Unreal project | yes | **A** |
| Unreal project | no | **B** |
| Godot project | n/a | **A** (file-based; use `godot --headless`) |
| Nothing | — | **C — No project yet** |

**A — Adopt.** Read `data/gdd-schema.md`, then MODIFY path.
**B — Blocked.** Stop. Tell the user exactly:
> "Found a `<engine>` project at `<path>`, but the Editor is not running.
> Open it and load the HSA bridge plugin, then re-run. Bridge listens on
> `<port>` — I need it to read and write the scene."

Do not scaffold a project by hand. Unity and Unreal projects are editor-generated
and partly binary; a hand-written one is broken in ways that only surface later.

**C — No project.** The user must create it first — Unity Hub or Epic launcher.
Then re-run `/game`. Route creative ideation (no project, no engine named) to
`/game-start`, not here.

> There is no WebSocket transport. Unity is stdio MCP → HTTP 30030;
> UE is stdio MCP → HTTP 30010 (Remote Control) + 30011 (Python executor).

---

## GAME FLOW (5 Steps, after preflight)

1. **STEP 1: UNDERSTAND INTENT**
   - Parse request → action type: **CREATE** | **MODIFY** | **DEBUG**
   - For CREATE: identify genre → load from `data/genres.yaml`

2. **STEP 2: GENERATE GDD** (CREATE only)
   - Parse prompt for: genre, mechanics, art style, platform
   - Generate `GDD.json` from genre template + user requirements
   - Present GDD to user for approval
   - ⛔ STOP and wait for approval before proceeding

3. **STEP 3: SCAFFOLD**
   - CREATE: create scene objects + manager scripts from GDD
   - MODIFY: load existing project structure via bridge
   - DEBUG: read current logs and scene state
   - Use patterns from `data/patterns.yaml` for script generation

4. **STEP 4: BUILD & DEBUG LOOP**
   ```
   compile_scripts() → check_logs() → fix_errors() → verify()
   Repeat max 5 times (GCS_006)
   Match errors against data/gotchas.yaml for auto-fixes
   ```

5. **STEP 5: VERIFY & PERSIST**
   - **Visual verification is not optional.** Launch play mode, capture the
     viewport, look at it. A passing compile proves the code loaded; it does
     not prove the game is playable. See `references/run-and-observe.md`.
   - Summary: files created/modified, errors fixed, remaining issues
   - `hsa_session({action:'persist', task_summary:'Game: [action] [game_name]'})`

---

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/game [description]` | Create new game from text description |
| `/game modify [what]` | Modify existing game project |
| `/game debug` | Debug game errors |
| `/game genres` | List available genre templates |
| `/game gdd [description]` | Generate GDD only (no build) |

---

## GENRE TEMPLATES (7)

| Genre | Difficulty | Scripts | Example |
|:------|:-----------|:--------|:--------|
| Endless Runner | S (4 scripts) | Controller, Spawner, Score, GameManager | Flappy Bird |
| Platformer | M (6 scripts) | Controller, Enemy, Level, Coins, Health, GM | Mario |
| Top-Down Shooter | M (7 scripts) | Controller, Weapon, Bullets, Enemy, Waves, Health, GM | Hotline Miami |
| Puzzle | S (5 scripts) | Grid, Tile, Score, Level, UI | Match-3 |
| RPG | L (10 scripts) | Controller, Combat, Stats, Inventory, Quest, NPC, Save... | Final Fantasy |
| Tower Defense | M (7 scripts) | Tower, Enemy, Waves, Economy, Grid, Projectile, GM | Bloons TD |
| Card Game | L (8 scripts) | Card, Deck, Combat, Mana, AI, Collection, UI, GM | Slay the Spire |

---

## BRIDGE REFERENCE

### Unity Quick Actions

```
get_hierarchy()          → Scene tree
create_object(type,name) → Spawn primitive
set_property(path,comp,field,val) → Modify any property
compile_scripts()        → Trigger recompilation
save_scene()            → Persist changes
get_logs(count)         → Read console
```

### UE Quick Actions

```
ue_execute_python(script) → Run Python in editor
ue_get_property(path,prop) → Read UObject value
ue_set_property(path,prop,val) → Modify UObject value
ue_search_assets(class,filter) → Find assets
```

> 📚 Full reference: `.agent/skills/cross-cutting/game-development/references/bridge-actions.md`
> 📚 Full patterns: `hsa_search(action:'docs', doc_libraries:['game-patterns-unity'])`

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_001):

1. **VERIFY** — Game compiles without errors? Visual check passed?
2. **PERSIST** (if HSA available):
   - `hsa_session({action:'persist', task_summary:'/game [action] [game_name]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable):
   - Append task summary to `memory/session.md`
