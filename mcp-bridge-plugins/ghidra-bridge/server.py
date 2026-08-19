# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp>=1.26.0,<2",
# ]
# ///
"""
HSA Ghidra MCP Bridge Server (runs OUTSIDE Ghidra)
===================================================
This stdio bridge talks to the Ghidra HTTP plugin loaded inside Ghidra.
It keeps instance discovery bounded so the agent can pin the right program
before calling rename/type/struct tools.
"""

import json
import os
import urllib.error
import urllib.request
from typing import List, Optional

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ghidra-mcp-bridge")
GHIDRA_HTTP_HOST = os.environ.get("HSA_GHIDRA_HTTP_HOST", "127.0.0.1")
GHIDRA_HTTP_PORT = int(os.environ.get("HSA_GHIDRA_HTTP_PORT", "28572"))
GHIDRA_HTTP_PORT_RANGE = int(os.environ.get("HSA_GHIDRA_HTTP_PORT_RANGE", "32"))


def _port_candidates(scan_ports: Optional[List[int]] = None) -> List[int]:
    if scan_ports:
        ports = []
        for value in scan_ports:
            try:
                port = int(value)
                if 0 < port < 65536:
                    ports.append(port)
            except Exception:
                continue
        if ports:
            return list(dict.fromkeys(ports))

    env_ports = os.environ.get("HSA_GHIDRA_PORTS", "")
    if env_ports:
        ports = []
        for part in env_ports.split(","):
            part = part.strip()
            if not part:
                continue
            try:
                port = int(part)
                if 0 < port < 65536:
                    ports.append(port)
            except Exception:
                continue
        if ports:
            return list(dict.fromkeys(ports))

    return list(range(GHIDRA_HTTP_PORT, GHIDRA_HTTP_PORT + max(1, GHIDRA_HTTP_PORT_RANGE)))


def _resolve_base_url(params: dict | None = None) -> str:
    if params:
        port = params.get("port")
        if isinstance(port, int) and port > 0:
            return "http://%s:%s" % (GHIDRA_HTTP_HOST, port)
        if isinstance(port, str) and port.isdigit():
            return "http://%s:%s" % (GHIDRA_HTTP_HOST, int(port))
    base = os.environ.get("HSA_GHIDRA_HTTP_BASE")
    if base:
        return base.rstrip("/")
    return "http://%s:%s" % (GHIDRA_HTTP_HOST, GHIDRA_HTTP_PORT)


def _request_json(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))


def ghidra_request(command: str, params: dict) -> dict:
    try:
        return _request_json(_resolve_base_url(params), {"command": command, "params": params})
    except urllib.error.URLError as e:
        return {"ok": False, "error": "Cannot connect to Ghidra plugin: %s" % e}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def format_result(res: dict) -> str:
    if not res.get("ok", False):
        return "❌ Ghidra Error: %s" % res.get("error", "Unknown error")
    return json.dumps(res.get("data", {}), indent=2, default=str)


def _probe_instance(port: int) -> dict | None:
    try:
        with urllib.request.urlopen("http://%s:%s" % (GHIDRA_HTTP_HOST, port), timeout=2) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if isinstance(data, dict) and data.get("status") == "ok":
                data["port"] = port
                return data
    except Exception:
        return None
    return None


@mcp.tool()
def ghidra_list_instances(scan_ports: Optional[List[int]] = None) -> str:
    ports = _port_candidates(scan_ports)
    instances = []
    for port in ports:
        info = _probe_instance(port)
        if info is not None:
            instances.append(info)
    return json.dumps({
        "ok": True,
        "instances": instances,
        "count": len(instances),
        "ports_scanned": ports,
    }, indent=2, default=str)


@mcp.tool()
def ghidra_get_info() -> str:
    return format_result(ghidra_request("get_info", {}))


@mcp.tool()
def ghidra_list_functions(offset: int = 0, limit: int = 50) -> str:
    return format_result(ghidra_request("list_functions", {"offset": offset, "limit": min(limit, 200)}))


@mcp.tool()
def ghidra_search_functions(pattern: str, max_results: int = 50) -> str:
    return format_result(ghidra_request("search_functions", {"pattern": pattern, "max_results": min(max_results, 200)}))


@mcp.tool()
def ghidra_decompile(address: str) -> str:
    return format_result(ghidra_request("decompile", {"address": address}))


@mcp.tool()
def ghidra_get_disasm(address: str, count: int = 20) -> str:
    return format_result(ghidra_request("get_disasm", {"address": address, "count": count}))


@mcp.tool()
def ghidra_get_xrefs(address: str, direction: str = "to") -> str:
    return format_result(ghidra_request("get_xrefs", {"address": address, "direction": direction}))


@mcp.tool()
def ghidra_get_symbols(pattern: str = "", max_results: int = 100) -> str:
    return format_result(ghidra_request("get_symbols", {"pattern": pattern, "max_results": min(max_results, 500)}))


@mcp.tool()
def ghidra_get_data_types(pattern: str = "", max_results: int = 100) -> str:
    return format_result(ghidra_request("get_data_types", {"pattern": pattern, "max_results": min(max_results, 500)}))


@mcp.tool()
def ghidra_rename_symbol(address: str, name: str, source_type: str = "user") -> str:
    return format_result(ghidra_request("rename_symbol", {"address": address, "name": name, "source_type": source_type}))


@mcp.tool()
def ghidra_set_function_signature(address: str, signature: str) -> str:
    return format_result(ghidra_request("set_function_signature", {"address": address, "signature": signature}))


@mcp.tool()
def ghidra_create_struct(name: str, members: Optional[List[dict]] = None) -> str:
    return format_result(ghidra_request("create_struct", {"name": name, "members": members or []}))


@mcp.tool()
def ghidra_apply_data_type(address: str, type_name: str, length: int = 0) -> str:
    return format_result(ghidra_request("apply_data_type", {"address": address, "type_name": type_name, "length": length}))


@mcp.tool()
def ghidra_create_class_layout(name: str, fields: Optional[List[dict]] = None, vtable: Optional[str] = None) -> str:
    return format_result(ghidra_request("create_class_layout", {"name": name, "fields": fields or [], "vtable": vtable}))


if __name__ == "__main__":
    mcp.run()
