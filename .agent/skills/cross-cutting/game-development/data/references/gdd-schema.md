# GDD Schema Reference — Game Design Document

> Machine-readable Game Design Document format for text-to-game automation.

---

## JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Game Design Document (GDD)",
  "type": "object",
  "required": ["meta", "core_loop", "systems", "scripts_needed"],
  "properties": {
    "meta": {
      "type": "object",
      "required": ["title", "genre", "engine"],
      "properties": {
        "title": { "type": "string", "description": "Game title" },
        "genre": {
          "type": "string",
          "enum": ["endless-runner", "platformer", "top-down-shooter", "puzzle", "rpg", "tower-defense", "card-game"]
        },
        "engine": { "type": "string", "enum": ["unity", "unreal"] },
        "target_platform": { "type": "string", "enum": ["pc", "mobile", "web", "console"] },
        "art_style": { "type": "string", "enum": ["2d-pixel", "2d-vector", "2d-hand-drawn", "3d-low-poly", "3d-realistic"] },
        "estimated_dev_time": { "type": "string" }
      }
    },
    "core_loop": {
      "type": "object",
      "required": ["action", "challenge", "reward", "fail_condition"],
      "properties": {
        "action": { "type": "string", "description": "What the player does" },
        "challenge": { "type": "string", "description": "What makes it hard" },
        "reward": { "type": "string", "description": "What the player gains" },
        "fail_condition": { "type": "string", "description": "How the player loses" }
      }
    },
    "systems": {
      "type": "object",
      "properties": {
        "physics": { "type": "object" },
        "spawner": { "type": "object" },
        "scoring": { "type": "object" },
        "health": { "type": "object" },
        "economy": { "type": "object" },
        "difficulty": { "type": "object" }
      }
    },
    "scripts_needed": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": { "type": "string" },
          "desc": { "type": "string" }
        }
      }
    },
    "assets_needed": {
      "type": "object",
      "properties": {
        "sprites": { "type": "array", "items": { "type": "string" } },
        "audio": { "type": "array", "items": { "type": "string" } },
        "models": { "type": "array", "items": { "type": "string" } },
        "tilemaps": { "type": "array", "items": { "type": "string" } }
      }
    },
    "milestones": {
      "type": "array",
      "items": { "type": "string", "enum": ["prototype", "vertical_slice", "alpha", "beta", "gold"] }
    }
  }
}
```

---

## Example 1: Flappy Bird Clone

```json
{
  "meta": {
    "title": "Floppy Wings",
    "genre": "endless-runner",
    "engine": "unity",
    "target_platform": "mobile",
    "art_style": "2d-pixel",
    "estimated_dev_time": "1-2 days"
  },
  "core_loop": {
    "action": "Tap to flap wings upward",
    "challenge": "Navigate through gaps between pipes",
    "reward": "Score +1 per pipe passed",
    "fail_condition": "Hit pipe or ground"
  },
  "systems": {
    "physics": { "gravity": -9.81, "flap_force": 5.0, "rotation_speed": 150 },
    "spawner": { "type": "infinite", "spawn_rate": 1.8, "gap_size": 3.0, "speed": 2.5 },
    "scoring": { "type": "incremental", "display": "UI_text" },
    "difficulty": { "type": "time-based", "speed_increment": 0.05, "ramp_every_seconds": 30 }
  },
  "scripts_needed": [
    { "name": "BirdController", "desc": "Tap to flap, gravity fall, rotation based on velocity" },
    { "name": "PipeSpawner", "desc": "Infinite pipe generation with random Y offset" },
    { "name": "ScoreZone", "desc": "Trigger between pipes that increments score" },
    { "name": "GameManager", "desc": "Menu, Playing, GameOver states" }
  ],
  "assets_needed": {
    "sprites": ["bird_flap1", "bird_flap2", "pipe_top", "pipe_bottom", "background_sky", "ground"],
    "audio": ["flap_sfx", "score_sfx", "hit_sfx", "bg_music"]
  },
  "milestones": ["prototype", "alpha", "gold"]
}
```

---

## Example 2: 2D Platformer

```json
{
  "meta": {
    "title": "Crystal Dash",
    "genre": "platformer",
    "engine": "unity",
    "target_platform": "pc",
    "art_style": "2d-pixel",
    "estimated_dev_time": "1-2 weeks"
  },
  "core_loop": {
    "action": "Run and jump through levels, collect crystals",
    "challenge": "Moving platforms, enemies, spikes, precision jumps",
    "reward": "Crystals (currency), checkpoints, level completion stars",
    "fail_condition": "Fall into pit or lose all 3 hearts"
  },
  "systems": {
    "physics": { "gravity": -20, "jump_force": 12, "move_speed": 8, "coyote_time": 0.15 },
    "health": { "type": "hearts", "max": 3, "invincibility_time": 1.5 },
    "scoring": { "type": "collectible", "crystal_value": 10 },
    "spawner": { "type": "level-based", "enemy_types": ["walker", "flyer"] },
    "difficulty": { "type": "level-progression", "levels": 10 }
  },
  "scripts_needed": [
    { "name": "PlayerController2D", "desc": "Movement, jump (coyote time), wall slide" },
    { "name": "EnemyAI", "desc": "Patrol + chase behavior with raycasting" },
    { "name": "LevelManager", "desc": "Level loading, checkpoints, door transitions" },
    { "name": "CrystalCollector", "desc": "Collectible trigger with VFX" },
    { "name": "HealthSystem", "desc": "Hearts display, damage, death, respawn" },
    { "name": "GameManager", "desc": "Score persistence, level unlock, save/load" }
  ],
  "assets_needed": {
    "sprites": ["player_idle", "player_run", "player_jump", "walker_enemy", "flyer_enemy", "crystal", "heart", "spike"],
    "audio": ["jump_sfx", "crystal_sfx", "hurt_sfx", "enemy_death_sfx", "level_complete_sfx", "bg_music"],
    "tilemaps": ["ground_tiles", "platform_tiles", "decoration_tiles"]
  },
  "milestones": ["prototype", "vertical_slice", "alpha", "beta", "gold"]
}
```

---
