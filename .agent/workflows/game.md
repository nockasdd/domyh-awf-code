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

---

## GAME FLOW (6 Steps)

1. **STEP 0: PREREQUISITES**
   - `hsa_search(action:"skills", query:"game development")` → Load skill
   - `hsa_detect(action:"stack")` → Detect Unity/UE project
   - Verify engine editor is OPEN
   - `hsa_bridge({target:'unity|ue', action:'health_check'})` → Confirm bridge

2. **STEP 1: UNDERSTAND INTENT**
   - Parse user request → Determine action type:
     - **CREATE**: New game from description
     - **MODIFY**: Change existing game
     - **DEBUG**: Fix bugs in game
   - For CREATE: Identify genre → Load from `data/genres.yaml`

3. **STEP 2: GENERATE GDD** (CREATE only)
   - Parse user prompt for: genre, mechanics, art style, platform
   - Generate `GDD.json` from genre template + user requirements
   - Present GDD to user for approval
   - ⛔ STOP and wait for GDD approval before proceeding

4. **STEP 3: SCAFFOLD**
   - CREATE: Create scene objects + manager scripts from GDD
   - MODIFY: Load existing project structure via bridge
   - DEBUG: Read current logs and scene state
   - Use patterns from `data/patterns.yaml` for script generation

5. **STEP 4: BUILD & DEBUG LOOP**
   ```
   compile_scripts() → check_logs() → fix_errors() → verify()
   Repeat max 5 times (rule GCS_006)
   Match errors against data/gotchas.yaml for auto-fixes
   ```

6. **STEP 5: VERIFY & PERSIST**
   - Visual verification (screenshot if available)
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

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Game compiles without errors? Visual check passed?
2. **PERSIST** (if HSA available):
   - `hsa_session({action:'persist', task_summary:'/game [action] [game_name]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable):
   - Append task summary to `memory/session.md`
