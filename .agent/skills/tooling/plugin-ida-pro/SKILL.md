---
name: plugin-ida-pro
description: "Use when a task involves analyzing or mutating EXE/DLL/binary targets in IDA Pro, or when the agent needs a bounded multi-call flow for IDA bridge work."
category: tooling
tier: 1
---

# IDA Pro Binary Workflow

## When To Use

- Any task mentioning `exe`, `dll`, `binary`, `dump`, `packer`, `anti-tamper`, `decompile`, `xrefs`, `strings`, `struct`, `class`, or `rename`.
- Any task that needs several IDA facts in one pass.
- Any task that mutates names, comments, types, or structs in the same binary.

## Workflow

1. Discover live targets first: `hsa_bridge(action='discover', target='ida')`; pass `scan_ports` if the default port window may be too small.
2. Pin identity before mutation with `port` and, when relevant, `instance_key`, `process_id`, `binary_path`, `module_name`, or `module_path`.
3. Inspect the current surface with `hsa_bridge(action='tools', target='ida')`.
4. Prefer `ida_batch` for mixed read/write bundles and `ida_apply_plan` for coordinated IDB edits.
5. For writes, pass `allow_mutations=true` and keep the batch/plan bounded.
6. If bulk tools are unavailable, fall back to bounded single `ida_*` calls.

## Good Batch Shapes

- Read bundle: `ida_get_info`, `ida_list_functions`, `ida_get_segments`, `ida_get_strings`, `ida_get_xrefs`, `ida_decompile`
- Rename bundle: `ida_search_functions`, `ida_decompile`, `ida_rename_function`, `ida_rename_global`, `ida_rename_many`, `ida_set_comment`
- Type bundle: `ida_import_c_declarations`, `ida_apply_type`, `ida_apply_types`, `ida_set_function_type`
- Struct bundle: `ida_get_types`, `ida_create_struct`, `ida_add_struct_member`, `ida_set_struct_member_type`, `ida_rename_struct_member`
- Plan bundle: `ida_apply_plan` with `declarations`, `structs`, `renames`, `local_renames`, `types`, `comments`, `allow_mutations=true`

## Mutation Rules

- Treat `ok:false` as not completed even when the MCP call itself succeeds.
- Read `retry_hint`, `conflict_address`, and per-item `results` before retrying a rename.
- For function names, prefer `ida_rename_function`; for exact labels/data names, use `ida_rename_global`.
- For multiple IDA windows, read `instances`, `matched_instances`, `selected_port`, and `bridge_route`; never mutate until the `instance_key`, `process_id`, `binary_path`, or `imagebase` matches the requested target.
- Prefer `port + instance_key`; if `port` is unknown, pass `process_id` or exact `binary_path` so the bridge can resolve the correct live IDA instead of falling back to the first port.
- Port scans are bounded and parallel; if a custom range is large, keep it explicit and read `probe_timeout_ms` and `scan_workers` from `ida_list_instances`.
- A single unpinned read may auto-route only when exactly one live IDA instance is found. If several instances are live, the bridge must reject the call until the agent pins the intended instance.
- For EXE/DLL relationship work, discover/list each open IDA instance, then pin by `port` plus `binary_path` or module identity.

## Guardrails

- Never assume the first live IDA window is correct.
- Never mutate without a pinned target and explicit `allow_mutations=true`.
- Keep batches bounded. Default to 32 requests or fewer.
- Use `plugin-ida-pro.md` for exact bridge contracts and current runtime notes.
