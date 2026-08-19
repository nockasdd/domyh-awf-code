# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp>=1.26.0,<2",
# ]
# ///
"""
HSA IDA MCP Bridge Server (runs OUTSIDE IDA Pro)
=================================================
This is the MCP stdio bridge that HSA Engine spawns as a subprocess.
It connects to the IDA plugin's HTTP server (hsa_ida_plugin.py) running
inside IDA Pro on port 28472.

Flow: HSA Engine → stdio → [this server] → HTTP → [IDA plugin inside IDA]
"""

import asyncio
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional
from mcp.server.fastmcp import FastMCP
from hsa_ida_compat import compat

mcp = FastMCP("ida-mcp-bridge")
IDA_HTTP_HOST = os.environ.get("HSA_IDA_HTTP_HOST", "127.0.0.1")
IDA_HTTP_PORT = int(os.environ.get("HSA_IDA_HTTP_PORT", "28472"))
IDA_HTTP_PORT_RANGE = int(os.environ.get("HSA_IDA_HTTP_PORT_RANGE", "32"))
IDA_HTTP_PROBE_TIMEOUT = max(0.05, int(os.environ.get("HSA_IDA_PROBE_TIMEOUT_MS", "350")) / 1000)
IDA_HTTP_SCAN_WORKERS = max(1, int(os.environ.get("HSA_IDA_SCAN_WORKERS", "32")))
IDA_AUTODISCOVER_ON_CALL = os.environ.get("HSA_IDA_AUTODISCOVER_ON_CALL", "1").lower() not in {"0", "false", "no"}


def _port_candidates(params: dict | None = None) -> List[int]:
    ports = []

    def _append_port(value: Any) -> None:
        try:
            if isinstance(value, str):
                token = value.strip()
                if not token:
                    return
                if '-' in token:
                    left, right = token.split('-', 1)
                    start = int(left)
                    end = int(right)
                    if start > end:
                        start, end = end, start
                    for port in range(start, end + 1):
                        if 0 < port < 65536:
                            ports.append(port)
                    return
                value = int(token)
            port = int(value)
            if 0 < port < 65536:
                ports.append(port)
        except Exception:
            return

    if params:
        raw_ports = params.get("scan_ports")
        if isinstance(raw_ports, list):
            for value in raw_ports:
                _append_port(value)
    if not ports:
        env_ports = os.environ.get("HSA_IDA_PORTS", "")
        if env_ports:
            for part in env_ports.split(","):
                _append_port(part)
    if not ports:
        ports = list(range(IDA_HTTP_PORT, IDA_HTTP_PORT + max(1, IDA_HTTP_PORT_RANGE)))
    return list(dict.fromkeys(ports))


def _normalize_path(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    text = value.strip().replace("/", os.sep)
    if not text:
        return ""
    try:
        return os.path.normcase(os.path.normpath(text))
    except Exception:
        return text.lower()


def _read_text(value: Any) -> str:
    return value.strip() if isinstance(value, str) and value.strip() else ""


def _read_int(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        try:
            parsed = int(text, 10)
            return parsed if parsed > 0 else None
        except Exception:
            return None
    return None


def _instance_matches(info: dict, params: dict | None = None) -> bool:
    if not params:
        return False

    requested_port = _read_int(params.get("port"))
    if requested_port is not None and _read_int(info.get("port")) != requested_port:
        return False

    requested_pid = _read_int(params.get("process_id"))
    if requested_pid is None:
        requested_pid = _read_int(params.get("pid"))
    if requested_pid is not None and _read_int(info.get("process_id")) != requested_pid:
        return False

    requested_instance_key = _read_text(params.get("instance_key"))
    if requested_instance_key:
        current_instance_key = _read_text(info.get("instance_key"))
        if current_instance_key and current_instance_key != requested_instance_key:
            return False

    requested_path = _read_text(params.get("binary_path"))
    if not requested_path:
        requested_path = _read_text(params.get("database_path"))
    if not requested_path:
        requested_path = _read_text(params.get("file"))
    if not requested_path:
        requested_path = _read_text(params.get("module_path"))
    if requested_path:
        candidate_paths = [
            _read_text(info.get("binary_path")),
            _read_text(info.get("database_path")),
            _read_text(info.get("file")),
            _read_text(info.get("module_path")),
        ]
        normalized_requested = _normalize_path(requested_path)
        if normalized_requested:
            candidate_matches = [_normalize_path(candidate) == normalized_requested for candidate in candidate_paths if candidate]
            if not any(candidate_matches):
                return False

    requested_name = _read_text(params.get("module_name"))
    if requested_name:
        candidate_name = _read_text(info.get("module_name"))
        if candidate_name and candidate_name.lower() != requested_name.lower():
            return False

    requested_imagebase = _read_text(params.get("imagebase"))
    if requested_imagebase:
        candidate_imagebase = _read_text(info.get("imagebase"))
        if candidate_imagebase and candidate_imagebase.lower() != requested_imagebase.lower():
            return False

    return bool(
        requested_port is not None
        or requested_pid is not None
        or requested_instance_key
        or requested_path
        or requested_name
        or requested_imagebase
    )


def _has_requested_identity(params: dict | None = None) -> bool:
    if not params:
        return False
    return any(
        _read_text(params.get(key))
        for key in ("instance_key", "binary_path", "database_path", "file", "module_path", "module_name", "imagebase")
    ) or _read_int(params.get("process_id")) is not None or _read_int(params.get("pid")) is not None


def _resolve_base_url(params: dict | None = None, command: str = "") -> tuple[str, dict | None]:
    if params:
        port = params.get("port")
        if isinstance(port, int) and port > 0:
            return f"http://{IDA_HTTP_HOST}:{port}", {"mode": "direct", "port": port}
        if isinstance(port, str) and port.isdigit():
            resolved_port = int(port)
            return f"http://{IDA_HTTP_HOST}:{resolved_port}", {"mode": "direct", "port": resolved_port}
        requested_identity = _has_requested_identity(params)
        if requested_identity:
            ports = _port_candidates(params)
            matches = [info for info in _probe_instances(ports) if _instance_matches(info, params)]
            if len(matches) == 1:
                selected_port = int(matches[0].get("port", 0) or 0)
                if selected_port > 0:
                    return f"http://{IDA_HTTP_HOST}:{selected_port}", {
                        "mode": "matched",
                        "port": selected_port,
                        "instance_key": matches[0].get("instance_key"),
                        "process_id": matches[0].get("process_id"),
                        "binary_path": matches[0].get("binary_path") or matches[0].get("file"),
                    }
            if len(matches) > 1:
                raise ValueError(f"Multiple IDA instances matched the requested identity: {[match.get('port') for match in matches]}")
            raise ValueError(
                "No IDA instance matched the requested identity. "
                f"Scanned ports: {ports}. Pass port, instance_key, process_id, or binary_path from ida_list_instances."
            )

    if IDA_AUTODISCOVER_ON_CALL and command != "list_instances":
        ports = _port_candidates(params)
        instances = _probe_instances(ports)
        if len(instances) == 1:
            selected_port = int(instances[0].get("port", 0) or 0)
            if selected_port > 0:
                return f"http://{IDA_HTTP_HOST}:{selected_port}", {
                    "mode": "single_live",
                    "port": selected_port,
                    "instance_key": instances[0].get("instance_key"),
                    "process_id": instances[0].get("process_id"),
                    "binary_path": instances[0].get("binary_path") or instances[0].get("file"),
                    "ports_scanned": ports,
                }
        if len(instances) > 1:
            raise ValueError(
                "Multiple live IDA instances are available. "
                f"Candidates: {[instance.get('port') for instance in instances]}. "
                "Pass port plus instance_key, process_id, or binary_path before calling IDA tools."
            )
    base = os.environ.get("HSA_IDA_HTTP_BASE")
    if base:
        return base.rstrip("/"), {"mode": "base", "base_url": base.rstrip("/")}
    return f"http://{IDA_HTTP_HOST}:{IDA_HTTP_PORT}", {"mode": "default", "port": IDA_HTTP_PORT}


def _request_json(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ida_request(command: str, params: dict) -> dict:
    """Send a command to the IDA plugin HTTP server."""
    if compat.is_headless:
        return {"error": "Headless mode — HTTP bridge not used."}
    try:
        base_url, route = _resolve_base_url(params, command)
        response = _request_json(base_url, {"command": command, "params": params})
        if route and isinstance(response, dict):
            data = response.get("data")
            if isinstance(data, dict):
                data["bridge_route"] = route
            else:
                response["bridge_route"] = route
        return response
    except urllib.error.URLError as e:
        return {"ok": False, "error": f"Cannot connect to IDA plugin: {e}. Is IDA running with hsa_ida_plugin.py loaded?"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(res: dict) -> str:
    """Format IDA response for agent consumption."""
    if not res.get("ok", False):
        error = res.get("error", "Unknown error")
        return json.dumps({"ok": False, "error": error, "raw": res}, indent=2, default=str)
    data = res.get("data", {})
    return json.dumps(data, indent=2, default=str)


def _routing_payload(
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {}
    if port:
        payload["port"] = port
    if instance_key:
        payload["instance_key"] = instance_key
    if process_id:
        payload["process_id"] = process_id
    if binary_path:
        payload["binary_path"] = binary_path
    if module_path:
        payload["module_path"] = module_path
    if module_name:
        payload["module_name"] = module_name
    if imagebase:
        payload["imagebase"] = imagebase
    if scan_ports:
        payload["scan_ports"] = scan_ports
    return payload


def _with_route(params: Dict[str, Any], **route: Any) -> Dict[str, Any]:
    merged = dict(params)
    merged.update(_routing_payload(**route))
    return merged


def _normalize_batch_command(name: Any) -> str:
    if not isinstance(name, str):
        return ""
    clean = name.strip()
    if clean.startswith("ida_"):
        clean = clean[4:]
    aliases = {
        "get_info": "get_info",
        "get_pseudocode": "decompile",
        "decompile": "decompile",
        "rename": "rename_symbol",
        "bulk_rename": "rename_many",
        "apply_types": "apply_types",
        "set_member_type": "set_struct_member_type",
        "rename_member": "rename_struct_member",
        "delete_member": "delete_struct_member",
    }
    return aliases.get(clean, clean)


def _is_mutating_batch_command(command: str) -> bool:
    return command in {
        "rename",
        "rename_symbol",
        "rename_function",
        "rename_global",
        "rename_many",
        "set_comment",
        "rename_local",
        "apply_type",
        "apply_types",
        "set_function_type",
        "import_c_declarations",
        "create_struct",
        "add_struct_member",
        "set_struct_member_type",
        "rename_struct_member",
        "delete_struct_member",
        "apply_plan",
    }


def _execute_batch_locally(requests: List[Dict[str, Any]], stop_on_error: bool, allow_mutations: bool, max_requests: int) -> dict:
    results = []
    failed = 0
    stopped = False

    for index, item in enumerate((requests or [])[:max_requests]):
        if not isinstance(item, dict):
            failed += 1
            results.append({"index": index, "ok": False, "error": "batch item must be an object"})
            if stop_on_error:
                stopped = True
                break
            continue

        command = _normalize_batch_command(item.get("command") or item.get("cmd") or item.get("tool"))
        request_id = item.get("id", index)
        if not command or command == "batch":
            failed += 1
            results.append({"index": index, "id": request_id, "ok": False, "error": "invalid batch command"})
            if stop_on_error:
                stopped = True
                break
            continue

        mutates = _is_mutating_batch_command(command)
        if mutates and not allow_mutations:
            failed += 1
            results.append({
                "index": index,
                "id": request_id,
                "command": command,
                "ok": False,
                "mutates": True,
                "error": "batch contains mutating commands; pass allow_mutations=true",
            })
            if stop_on_error:
                stopped = True
                break
            continue

        result = ida_request(command, item.get("params") or item.get("payload") or {})
        ok = bool(result.get("ok", False)) and "error" not in result
        if not ok:
            failed += 1
        results.append({
            "index": index,
            "id": request_id,
            "command": command,
            "ok": ok,
            "mutates": mutates,
            "result": result,
        })
        if not ok and stop_on_error:
            stopped = True
            break

    return {
        "ok": failed == 0,
        "data": {
            "mode": "sequential-fallback",
            "count": len(results),
            "failed": failed,
            "stopped": stopped,
            "results": results,
        },
    }


def _probe_instance(port: int) -> dict | None:
    import urllib.request
    import urllib.error
    url = f"http://{IDA_HTTP_HOST}:{port}"
    try:
        with urllib.request.urlopen(url, timeout=IDA_HTTP_PROBE_TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            data = json.loads(body)
            if isinstance(data, dict) and data.get("status") == "ok":
                data["port"] = port
                return data
    except Exception:
        return None
    return None


def _probe_instances(ports: List[int]) -> List[dict]:
    if not ports:
        return []
    results: dict[int, dict] = {}
    max_workers = min(len(ports), IDA_HTTP_SCAN_WORKERS)
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {executor.submit(_probe_instance, port): port for port in ports if port > 0}
        for future in as_completed(future_map):
            port = future_map[future]
            try:
                info = future.result()
            except Exception:
                info = None
            if info is not None:
                results[port] = info
    return [results[port] for port in ports if port in results]


# ── MCP Tools ──────────────────────────────────────────────────────

@mcp.tool()
def ida_get_info(
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Get basic info about the loaded IDA database (file, imagebase, functions count)."""
    return format_result(ida_request("get_info", _routing_payload(
        port, instance_key, process_id, binary_path, module_path, module_name, imagebase, scan_ports,
    )))


@mcp.tool()
def ida_list_instances(
    scan_ports: Optional[List[int]] = None,
    port: int = 0,
    process_id: int = 0,
    binary_path: str = "",
    instance_key: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
) -> str:
    """Enumerate reachable IDA bridge instances by HTTP port."""
    params = {
        "port": port,
        "process_id": process_id,
        "binary_path": binary_path,
        "instance_key": instance_key,
        "module_path": module_path,
        "module_name": module_name,
        "imagebase": imagebase,
        "scan_ports": scan_ports,
    }
    ports = scan_ports or _port_candidates(params)
    instances = _probe_instances(ports)
    matched_instances = [instance for instance in instances if _instance_matches(instance, params)]
    return json.dumps({
        "ok": True,
        "instances": instances,
        "matched_instances": matched_instances,
        "selected_port": matched_instances[0]["port"] if len(matched_instances) == 1 else None,
        "count": len(instances),
        "matched_count": len(matched_instances),
        "probe_timeout_ms": int(IDA_HTTP_PROBE_TIMEOUT * 1000),
        "scan_workers": min(len(ports), IDA_HTTP_SCAN_WORKERS) if ports else 0,
        "requested_identity": {
            "port": port if port > 0 else None,
            "process_id": process_id if process_id > 0 else None,
            "binary_path": binary_path or None,
            "instance_key": instance_key or None,
            "module_path": module_path or None,
            "module_name": module_name or None,
            "imagebase": imagebase or None,
        },
        "ports_scanned": ports,
    }, indent=2, default=str)


@mcp.tool()
def ida_list_functions(
    offset: int = 0,
    limit: int = 50,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """List functions in the database with pagination.
    
    Args:
        offset: Start index (default 0)
        limit: Max functions to return (default 50, max 200)
    """
    return format_result(ida_request("list_functions", _with_route(
        {"offset": offset, "limit": min(limit, 200)},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_decompile(
    address: Any,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Decompile a function at the given hex address using Hex-Rays.
    
    Args:
        address: Hex address like '0x401000' or '401000'
    """
    if compat.is_headless:
        # Headless mode uses idalib directly
        try:
            import ida_hexrays
            import ida_funcs as _ida_funcs
            ea = int(address, 16) if isinstance(address, str) else int(address)
            cfunc = ida_hexrays.decompile(ea)
            if cfunc:
                return str(cfunc)
            return f"❌ Decompilation failed at {address}"
        except Exception as e:
            return f"❌ Headless decompile error: {e}"
    
    return format_result(ida_request("decompile", _with_route(
        {"address": address},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_get_disasm(
    address: Any,
    count: int = 20,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Get disassembly lines starting from an address.
    
    Args:
        address: Hex address like '0x401000'
        count: Number of instructions to disassemble (default 20)
    """
    return format_result(ida_request("get_disasm", _with_route(
        {"address": address, "count": count},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_rename(
    address: Any,
    name: str,
    force: bool = False,
    scope: str = "auto",
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Rename a symbol/function at the given address.
    
    Args:
        address: Hex address of the symbol
        name: New name for the symbol
        force: If True, allow IDA to force a unique name when normal checks fail
        scope: auto, function, or address
    """
    return format_result(ida_request("rename_symbol", _with_route({
        "address": address,
        "name": name,
        "force": force,
        "scope": scope,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_rename_function(
    address: Any,
    name: str,
    force: bool = False,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Rename the function containing or starting at an address."""
    return format_result(ida_request("rename_function", _with_route({
        "address": address,
        "name": name,
        "force": force,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_rename_global(
    address: Any,
    name: str,
    force: bool = False,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Rename the exact global/address label instead of snapping to function start."""
    return format_result(ida_request("rename_global", _with_route({
        "address": address,
        "name": name,
        "force": force,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_rename_many(
    items: List[Dict[str, Any]],
    force: bool = False,
    stop_on_error: bool = False,
    max_items: int = 64,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Rename several functions/symbols in one request with per-item diagnostics."""
    return format_result(ida_request("rename_many", _with_route({
        "items": items,
        "force": force,
        "stop_on_error": stop_on_error,
        "max_items": min(max_items, 128),
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_set_comment(
    address: str,
    comment: str,
    func: bool = False,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Set a comment at an address.
    
    Args:
        address: Hex address
        comment: Comment text
        func: If True, set as function comment instead of inline
    """
    return format_result(ida_request("set_comment", _with_route(
        {"address": address, "comment": comment, "func": func},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_read_bytes(
    address: Any,
    size: int = 16,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Read raw bytes from the database.
    
    Args:
        address: Hex address to read from
        size: Number of bytes to read (default 16)
    """
    return format_result(ida_request("read_bytes", _with_route(
        {"address": address, "size": size},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_get_xrefs(
    address: Any,
    direction: str = "to",
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Get cross-references to or from an address.
    
    Args:
        address: Hex address
        direction: 'to' (who references this address) or 'from' (what this address references)
    """
    return format_result(ida_request("get_xrefs", _with_route(
        {"address": address, "direction": direction},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_get_strings(
    min_length: int = 4,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Get all strings found in the database.
    
    Args:
        min_length: Minimum string length (default 4)
    """
    return format_result(ida_request("get_strings", _with_route(
        {"min_length": min_length},
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_search_string(
    pattern: str,
    case_sensitive: bool = False,
    max_results: int = 100,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Search for strings matching a pattern (substring or regex) in the binary.
    Returns matching strings with their addresses and cross-references.

    Args:
        pattern: Search pattern (substring or regex like 'kernel32|ntdll')
        case_sensitive: Case-sensitive matching (default False)
        max_results: Maximum results to return (default 100, max 500)
    """
    return format_result(ida_request("search_string", _with_route({
        "pattern": pattern,
        "case_sensitive": case_sensitive,
        "max_results": max_results,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_search_bytes(
    hex_pattern: str,
    start: str = "",
    max_results: int = 50,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Search for a hex byte pattern in the binary. Supports ?? wildcards.

    Args:
        hex_pattern: Hex bytes separated by spaces, e.g. '48 8B ?? 10' or 'E8 ?? ?? ?? ??'
        start: Start address for search (hex, default: beginning of binary)
        max_results: Maximum results (default 50, max 200)
    """
    params = {"hex_pattern": hex_pattern, "max_results": max_results}
    if start:
        params["start"] = start
    return format_result(ida_request("search_bytes", _with_route(
        params,
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_get_segments(
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """List all segments in the binary (.text, .data, .rdata, etc.) with permissions."""
    return format_result(ida_request("get_segments", _routing_payload(
        port, instance_key, process_id, binary_path, module_path, module_name, imagebase, scan_ports,
    )))


@mcp.tool()
def ida_search_functions(
    pattern: str,
    max_results: int = 50,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Search functions by name pattern (substring or regex).
    Useful when you know a partial function name but not the address.

    Args:
        pattern: Function name pattern (e.g. 'main', 'crypt.*init', 'sub_4[0-9]+')
        max_results: Maximum results (default 50, max 200)
    """
    return format_result(ida_request("search_functions", _with_route({
        "pattern": pattern,
        "max_results": max_results,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_rename_local(
    function_address: Any,
    old_name: str,
    new_name: str,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Rename a Hex-Rays local variable inside a function.

    Args:
        function_address: Hex address inside or at the start of the function
        old_name: Existing local variable name
        new_name: Replacement local variable name
    """
    return format_result(ida_request("rename_local", _with_route({
        "function_address": function_address,
        "old_name": old_name,
        "new_name": new_name,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_apply_type(
    address: Any,
    c_decl: str,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Apply a C type declaration to an address.

    Args:
        address: Hex address to type
        c_decl: C declaration/type string accepted by IDA, e.g. 'int __cdecl sub_401000(int a)'
    """
    return format_result(ida_request("apply_type", _with_route({
        "address": address,
        "c_decl": c_decl,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_set_function_type(
    address: Any,
    prototype: str,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Set the full function prototype at an address.

    Args:
        address: Hex address inside or at the start of the function
        prototype: Function prototype accepted by IDA, e.g. 'int __fastcall main(int argc, char **argv)'
    """
    return format_result(ida_request("set_function_type", _with_route({
        "address": address,
        "prototype": prototype,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_apply_types(
    items: List[Dict[str, Any]],
    stop_on_error: bool = False,
    max_items: int = 64,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Apply several address types/prototypes in one request."""
    return format_result(ida_request("apply_types", _with_route({
        "items": items,
        "stop_on_error": stop_on_error,
        "max_items": min(max_items, 128),
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_import_c_declarations(
    declarations: str,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Import C declarations into IDA Local Types.

    Args:
        declarations: One or more C declarations, structs, typedefs, or class-like declarations
    """
    return format_result(ida_request("import_c_declarations", _with_route({
        "declarations": declarations,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_create_struct(
    name: str,
    members: Optional[List[Dict[str, Any]]] = None,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Create or update a struct/class-like type.

    Args:
        name: Struct name
        members: Optional member list. Each member may include name, offset, size, type_name, and comment.
    """
    return format_result(ida_request("create_struct", _with_route({
        "name": name,
        "members": members or [],
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_add_struct_member(
    struct_name: str,
    member_name: str,
    offset: int,
    size: int,
    type_name: str = "",
    comment: str = "",
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Add a member to an existing struct.

    Args:
        struct_name: Existing struct name
        member_name: New member name
        offset: Member offset in bytes
        size: Member size in bytes
        type_name: Optional C type name/declaration for the member
        comment: Optional repeatable member comment
    """
    return format_result(ida_request("add_struct_member", _with_route({
        "struct_name": struct_name,
        "member_name": member_name,
        "offset": offset,
        "size": size,
        "type_name": type_name,
        "comment": comment,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_set_struct_member_type(
    struct_name: str,
    type_name: str,
    member_name: str = "",
    offset: int = -1,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Set a struct member type by member name or offset."""
    payload: Dict[str, Any] = {
        "struct_name": struct_name,
        "type_name": type_name,
    }
    if member_name:
        payload["member_name"] = member_name
    if offset >= 0:
        payload["offset"] = offset
    return format_result(ida_request("set_struct_member_type", _with_route(
        payload,
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_rename_struct_member(
    struct_name: str,
    new_name: str,
    old_name: str = "",
    offset: int = -1,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Rename a struct member by member name or offset."""
    payload: Dict[str, Any] = {
        "struct_name": struct_name,
        "new_name": new_name,
    }
    if old_name:
        payload["old_name"] = old_name
    if offset >= 0:
        payload["offset"] = offset
    return format_result(ida_request("rename_struct_member", _with_route(
        payload,
        port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports,
    )))


@mcp.tool()
def ida_delete_struct_member(
    struct_name: str,
    offset: int,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Delete a struct member at an offset."""
    return format_result(ida_request("delete_struct_member", _with_route({
        "struct_name": struct_name,
        "offset": offset,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_apply_plan(
    declarations: str = "",
    structs: Optional[List[Dict[str, Any]]] = None,
    renames: Optional[List[Dict[str, Any]]] = None,
    local_renames: Optional[List[Dict[str, Any]]] = None,
    types: Optional[List[Dict[str, Any]]] = None,
    comments: Optional[List[Dict[str, Any]]] = None,
    force: bool = False,
    stop_on_error: bool = False,
    max_operations: int = 128,
    allow_mutations: bool = False,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Apply a bounded multi-edit IDA plan: declarations, structs, renames, local variables, types, and comments."""
    if not allow_mutations:
        return json.dumps({
            "ok": False,
            "error": "ida_apply_plan mutates the IDB; pass allow_mutations=true",
        }, indent=2)
    return format_result(ida_request("apply_plan", _with_route({
        "declarations": declarations,
        "structs": structs or [],
        "renames": renames or [],
        "local_renames": local_renames or [],
        "types": types or [],
        "comments": comments or [],
        "force": force,
        "stop_on_error": stop_on_error,
        "max_operations": min(max_operations, 256),
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_list_structs(
    pattern: str = "",
    max_results: int = 100,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """List IDA structs/local types by name filter.

    Args:
        pattern: Optional substring or regex filter
        max_results: Maximum rows to return
    """
    return format_result(ida_request("list_structs", _with_route({
        "pattern": pattern,
        "max_results": max_results,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_get_types(
    pattern: str = "",
    max_results: int = 100,
    port: int = 0,
    instance_key: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """List local type names known to IDA.

    Args:
        pattern: Optional substring or regex filter
        max_results: Maximum rows to return
    """
    return format_result(ida_request("get_types", _with_route({
        "pattern": pattern,
        "max_results": max_results,
    }, port=port, instance_key=instance_key, process_id=process_id, binary_path=binary_path,
        module_path=module_path, module_name=module_name, imagebase=imagebase, scan_ports=scan_ports)))


@mcp.tool()
def ida_batch(
    requests: List[Dict[str, Any]],
    stop_on_error: bool = True,
    allow_mutations: bool = False,
    max_requests: int = 32,
    port: int = 0,
    instance_key: str = "",
    session_id: str = "",
    process_id: int = 0,
    binary_path: str = "",
    module_path: str = "",
    module_name: str = "",
    imagebase: str = "",
    scan_ports: Optional[List[int]] = None,
) -> str:
    """Execute multiple bounded IDA commands in one MCP call.

    Args:
        requests: Batch items with command/tool and params/payload fields.
        stop_on_error: Stop after first failed item.
        allow_mutations: Required for rename/comment/type/struct writes.
        max_requests: Maximum batch items, capped at 32.
        port: Optional IDA HTTP plugin port discovered by ida_list_instances.
    """
    payload = {
        "requests": requests or [],
        "stop_on_error": stop_on_error,
        "allow_mutations": allow_mutations,
        "max_requests": min(max_requests, 32),
    }
    if port:
        payload["port"] = port
    if instance_key:
        payload["instance_key"] = instance_key
    if session_id:
        payload["session_id"] = session_id
    if process_id:
        payload["process_id"] = process_id
    if binary_path:
        payload["binary_path"] = binary_path
    if module_path:
        payload["module_path"] = module_path
    if module_name:
        payload["module_name"] = module_name
    if imagebase:
        payload["imagebase"] = imagebase
    if scan_ports:
        payload["scan_ports"] = scan_ports
    response = ida_request("batch", payload)
    if not response.get("ok", False):
        error_text = str(response.get("error", ""))
        if "Unknown command: batch" in error_text or "'batch'" in error_text:
            response = _execute_batch_locally(
                requests or [],
                stop_on_error,
                allow_mutations,
                min(max_requests, 32),
            )
    return format_result(response)


# ── Entry Point ────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HSA IDA MCP Bridge Server")
    parser.add_argument("--headless", type=str, help="Path to binary for idalib headless mode (IDA 9.x+ only)")
    args = parser.parse_args()

    if args.headless:
        if not compat.init_idalib_if_headless(args.headless):
            print("Failed to init idalib. Falling back to HTTP bridge mode.")
    
    mcp.run()
