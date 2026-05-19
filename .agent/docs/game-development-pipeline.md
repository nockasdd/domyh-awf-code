---
library: game-development-pipeline
version: 1
latest: true
category: other
official_docs: https://docs.unity3d.com/Manual/
last_updated: 2026-03-28
---

<!-- BM25: game development pipeline GDD prototype vertical slice alpha beta gold master milestones text-to-game automation agent gamedev -->

# game-development-pipeline

Game development pipeline for agent-assisted game creation. Covers the full lifecycle from concept to gold master, with GDD schema, automation coverage maps, and milestone definitions.

## Installation

### Prerequisites
- Unity 2022.3+ LTS or Unreal Engine 5.x
- HSA MCP Bridge plugin installed and running
  - Unity: WebSocket server on ws://127.0.0.1:15557
  - UE: Remote Control API on http://127.0.0.1:30010
- DOMYH AWF with `game-development` skill loaded

### Quick Start
```bash
# 1. Open Unity/UE Editor with bridge plugin
# 2. Verify bridge: hsa_bridge({target:'unity', action:'get_hierarchy'})
# 3. Start game workflow: /game "Create a flappy bird clone"
```

## Configuration

### GDD Schema (Game Design Document)
```json
{
  "meta": {
    "title": "string",
    "genre": "endless-runner|platformer|top-down-shooter|puzzle|rpg|tower-defense|card-game",
    "engine": "unity|unreal",
    "target_platform": "pc|mobile|web|console",
    "art_style": "2d-pixel|2d-vector|3d-low-poly|3d-realistic"
  },
  "core_loop": {
    "action": "What the player does",
    "challenge": "What makes it hard",
    "reward": "What player gains",
    "fail_condition": "How player loses"
  },
  "systems": {
    "physics": { "gravity": -9.81, "jump_force": 7.0 },
    "spawner": { "type": "infinite|level-based|wave-based" },
    "scoring": { "type": "incremental|collectible|kill-count" }
  },
  "scripts_needed": [
    { "name": "ScriptName", "desc": "What it does" }
  ],
  "assets_needed": {
    "sprites": ["asset_name"],
    "audio": ["sfx_name"]
  }
}
```

### Engine Configuration

#### Unity Project Setup
```
1. Create Unity 2022.3+ project with URP template
2. Install packages:
   - com.unity.inputsystem (New Input System)
   - com.unity.textmeshpro (UI text)
   - com.unity.cinemachine (camera, optional)
3. Project Settings > Player > Active Input Handling = "Input System Package (New)"
4. Create folders: Assets/Scripts/, Assets/Prefabs/, Assets/Scenes/
```

#### UE Project Setup
```
1. Create UE 5.x project (Blank or Third Person)
2. Enable plugins:
   - Remote Control API (Edit > Plugins)
   - Python Editor Script Plugin
3. Project Settings > Remote Control API > Enable = true
4. Create folders: Content/Blueprints/, Content/Python/
```

## Core API

### 6-Phase Game Development Pipeline

#### Phase 1: Concept (Agent Coverage: 90%)

The concept phase translates user intent into a structured Game Design Document.

```
User Prompt → Intent Parsing → Genre Template Selection → GDD Generation
```

Key actions:
- Parse natural language for game type, mechanics, art style
- Match to closest genre template (7 available)
- Generate GDD.json with complete systems specification
- Present to user for review and approval

Agent can fully automate: ideation, core loop design, technical feasibility check, GDD generation.

#### Phase 2: Pre-Production (Agent Coverage: 70%)

Create a greybox prototype with placeholder art and basic mechanics.

```
GDD → Engine Detection → Project Scaffold → Greybox Level → Core Mechanics Code
```

Key actions:
- Detect engine (Unity/UE) from project files
- Create scene hierarchy (managers, player, camera, UI canvas)
- Generate core scripts from patterns (Movement, GameManager, ScoreManager)
- Set up input system and camera follow

Limitation: User must have engine editor open with bridge running.

#### Phase 3: Production (Agent Coverage: 50%)

Build full game content with art assets, audio, and game systems.

```
Core Mechanics → Art Integration → UI Implementation → Game Systems → Level Population
```

Key actions:
- Import art assets via bridge
- Create UI Canvas with HUD (score, health, timer)
- Implement game-specific systems (spawner, scoring, difficulty curve)
- Populate levels with objects

Limitation: 3D art, animation, and high-quality audio need human artists.

#### Phase 4: QA & Polish (Agent Coverage: 60%)

Systematic debugging and visual verification.

```
Compile Check → Log Parse → Error Match → Auto-Fix → Visual Verify → Performance Check
```

Key actions:
- Compile scripts and parse errors
- Match against gotchas database (40 known issues)
- Apply auto-fixes for common errors
- Run debug loop (max 5 iterations per session)

Limitation: Complex logic bugs and visual bugs need human review.

#### Phase 5: Launch (Agent Coverage: 40%)

Build and package game for distribution.

```
Final Compile → Build Configuration → Export Binary → Platform Checks
```

Key actions:
- Trigger build: `unity_build_player` or UE packaging
- Verify build output
- Generate build report

Limitation: Platform certification requires manual steps.

#### Phase 6: Post-Launch (Agent Coverage: 50%)

Patches, updates, and new content.

```
Bug Report → Debug Loop → Fix → Patch Build → Content Update
```

Uses same pipeline as Phase 3-4 for iterative updates.

## Common Patterns

### Automation Coverage Matrix

| Phase | Agent % | Key Capability | Primary Limitation |
|:------|:--------|:--------------|:-------------------|
| Concept | 90% | GDD generation from prompt | Only needs user description |
| Pre-Production | 70% | Script generation + scene setup | Engine must be open |
| Production | 50% | Code + UI + systems | Art/audio needs artist |
| QA & Polish | 60% | Debug loop + auto-fix | Visual bugs need screenshot |
| Launch | 40% | Build automation | Platform cert is manual |
| Post-Launch | 50% | Patch pipeline | Bug complexity varies |

### Milestone Definitions

| Milestone | Criteria | Deliverable |
|:----------|:---------|:-----------|
| **Prototype** | Core mechanic playable with cubes | Greybox + 1 script |
| **Vertical Slice** | One complete level with art | Polished sample |
| **Alpha** | Feature complete, all systems working | Full game, placeholder art OK |
| **Beta** | Content complete, in QA | All levels + art + audio |
| **Gold Master** | Ship-ready, all bugs fixed | Final build |

### Genre Complexity Guide

| Genre | Scripts | Dev Time (Agent-assisted) | Recommended First Game? |
|:------|:--------|:------------------------|:----------------------|
| Endless Runner | 4 | 1-2 days | ✅ Best starter |
| Puzzle | 5 | 2-3 days | ✅ Good starter |
| Platformer | 6 | 3-5 days | ✅ Classic choice |
| Top-Down Shooter | 7 | 4-7 days | ⚠️ Medium complexity |
| Tower Defense | 7 | 5-8 days | ⚠️ Medium complexity |
| Card Game | 8 | 1-2 weeks | ❌ Complex |
| RPG | 10 | 2-4 weeks | ❌ Very complex |

## Gotchas

### Phase-Specific Risks

⚠️ **Phase 1 (Concept)**:
- GDD too ambitious — always scope down for first iteration
- Genre mismatch — verify user really wants detected genre

⚠️ **Phase 2 (Pre-Production)**:
- Engine not open — bridge fails silently
- Wrong input system — legacy Input.GetAxis causes issues later

⚠️ **Phase 3 (Production)**:
- Asset import fails — check file formats (PNG/JPG for Unity, FBX/OBJ for 3D)
- Script references broken after rename — use [SerializeField] consistently

⚠️ **Phase 4 (QA)**:
- NullReferenceException from race condition — objects loaded async
- Physics jitter — move Rigidbody code to FixedUpdate()
- UI overflow on different screen sizes — always set Canvas Scaler

⚠️ **Phase 5 (Launch)**:
- Missing scenes in Build Settings — add ALL scenes
- WebGL + System.IO = crash — use PlayerPrefs for web builds

### Bridge-Specific Gotchas

Unity:
- `rb.velocity` deprecated in Unity 6+ → use `rb.linearVelocity`
- `FindObjectOfType` per frame kills performance → cache in Awake()
- New Input System requires PlayerInput component AND Input Actions asset

UE:
- Remote Control 404 → plugin not enabled, restart editor
- PropertyName is CASE SENSITIVE → use describe endpoint first
- `ue_execute_python` has NO SANDBOX → never access files outside project

---
