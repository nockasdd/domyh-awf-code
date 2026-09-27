# Blender Bridge

MCP bridge for Blender. Reads the scene through structured tools with a byte
budget, and keeps `execute_python` as the escape hatch rather than the main
path.

## Why it is built this way

The cost of a Blender bridge is not the socket, it is the tokens. Two decisions
follow from that:

- **A cut response says it was cut.** Every read returns
  `{status, data, meta: {truncated, total_items, returned_items, next_offset, bytes_returned}}`.
  A listing that was bounded but not cut has `truncated: false` and a
  `next_offset` — a cut listing has `truncated: true`. Both are recoverable;
  a silently sliced string is not.
- **stdout is capped at the source.** The cap lives in the add-on's writer,
  where the string is produced, and the reply carries `stdout_truncated` and
  `stdout_bytes_dropped`. Capping after the fact would still have paid for the
  whole string.

## Install

1. Install the add-on: Blender > Edit > Preferences > Add-ons > Install, pick
   `src/addon/hsa_blender_addon.py`.
2. Build this bridge: `npm install && npm run build`.

That is the whole setup. The bridge writes its port and token to
`~/.nockdev/blender-bridge.json` on startup, and the add-on polls for that file
every 2s until it appears — so it does not matter whether Blender or the bridge
starts first, and neither one needs a token typed in by hand. Set
`HSA_BLENDER_TOKEN` (and optionally `HSA_BLENDER_PORT`, default 28782) before
launching Blender to skip the file entirely.

## Tools

| Tool | Cost |
| --- | --- |
| `blender_health` | Proves the link without running anything |
| `blender_get_scene_info` | Version, scene, frame, one page of objects |
| `blender_list_objects` | Object summaries, optionally filtered by type |
| `blender_describe_object` | One object in full: modifiers, materials, mesh counts |
| `blender_get_selection` | Selection, active object, mode |
| `blender_scene_diff` | What changed since the last call, not the whole scene |
| `blender_execute_python` | Anything else (mutating) |

`blender_scene_diff` is the one that scales: it costs what changed rather than
the size of the scene, so checking a 4000-object file stays affordable. The
first call reports `first_call: true` and establishes the baseline.

## Paging

Read tools take `offset` and `limit`. Follow `meta.next_offset` until it is
`null`. `meta.total_items` is the real scene size, not the size of the page.

## Tests

```
python test_bridge_logic.py    # add-on logic against a stubbed bpy
node test/envelope.test.mjs    # the byte budget and paging arithmetic on its own
node test/e2e.mjs              # built bridge over stdio against the real add-on
node test/handover.mjs         # bridge starting after Blender, agreeing via the config file
```

`test/fake_blender.py` runs the shipping add-on under a thread that calls
`_drain` the way `bpy.app.timers` would. Blender is not installed in CI, so
the tests cover what decides what the caller sees — the stdout cap, the
framing, the auth gate, the queue deadline, the envelope — without needing it.

## Threading

`bpy` is not thread-safe. Socket threads only enqueue; `bpy.app.timers` drains
on the main thread and is the only place the scene is touched. The timer is
registered `persistent=True` and re-registered on `load_post`, so a Save does
not make the bridge go deaf.
