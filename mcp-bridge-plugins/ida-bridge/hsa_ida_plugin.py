"""
HSA MCP Bridge Plugin for IDA Pro 8.x / 9.x
=============================================
Install: Copy this single file to %IDADIR%/plugins/hsa_ida_plugin.py

This plugin runs INSIDE IDA Pro as a proper idaapi.plugin_t.
It opens an HTTP server on port 28472 (localhost only) that accepts
JSON commands from the external MCP bridge (server.py).

Architecture:
  Agent -> HSA Engine -> server.py (MCP stdio) -> HTTP -> [THIS PLUGIN inside IDA]

IDA 8.3 compatible: Uses only APIs available in IDA 8.x.
No external pip dependencies (uses only stdlib + IDAPython).
"""

import idaapi
import ida_kernwin
import ida_funcs
import ida_name
import ida_bytes
import ida_nalt
import ida_lines
import ida_ida
import ida_typeinf
try:
    import ida_struct
except ImportError:
    ida_struct = None
import idautils
import idc

import os
import json
import socket
import threading
import traceback

# Use http.server from stdlib (no pip install needed in IDA's Python)
from http.server import HTTPServer, BaseHTTPRequestHandler

PLUGIN_NAME    = "HSA MCP Bridge"
PLUGIN_VERSION = "1.0.0"
PLUGIN_HOTKEY  = "Ctrl-Shift-H"
HTTP_HOST      = "127.0.0.1"
HTTP_PORT      = int(os.environ.get("HSA_IDA_HTTP_PORT", "28472"))
HTTP_PORT_RANGE = int(os.environ.get("HSA_IDA_HTTP_PORT_RANGE", "32"))
ACTIVE_HTTP_PORT = HTTP_PORT

# ── Thread-safe IDA execution ──────────────────────────────────────
# ALL IDA API calls MUST run on the main thread via execute_sync.

def sync_exec(fn, write=False):
    """Execute a function on IDA's main thread and return the result."""
    box = {}
    def wrapper():
        try:
            box["v"] = fn()
        except Exception as e:
            box["err"] = str(e)
            box["tb"] = traceback.format_exc()
    flags = ida_kernwin.MFF_WRITE if write else ida_kernwin.MFF_READ
    ida_kernwin.execute_sync(wrapper, flags)
    if "err" in box:
        raise RuntimeError(box["err"])
    return box.get("v")


def _parse_tinfo(c_decl):
    """Parse a C declaration into a tinfo_t, with small version fallbacks."""
    tif = ida_typeinf.tinfo_t()

    if hasattr(ida_typeinf, "parse_decl"):
        try:
            ok = ida_typeinf.parse_decl(tif, None, c_decl, 0)
            if ok:
                return tif
        except TypeError:
            pass

    if hasattr(ida_typeinf, "idc_parse_decl"):
        try:
            parsed = ida_typeinf.idc_parse_decl(tif, None, c_decl, 0)
            if parsed:
                return tif
        except Exception:
            pass

    return None


def _set_type_at(ea, c_decl):
    tif = _parse_tinfo(c_decl)
    if tif is None:
        return {"ok": False, "error": "Failed to parse type declaration"}

    if hasattr(idc, "set_type"):
        ok = idc.set_type(ea, c_decl)
    elif hasattr(idc, "SetType"):
        ok = idc.SetType(ea, c_decl)
    else:
        ok = ida_typeinf.apply_tinfo(ea, tif, ida_typeinf.TINFO_DEFINITE)

    return {"ok": bool(ok), "address": hex(ea), "type": c_decl}


def _set_member_tinfo(st, member, c_decl):
    tif = _parse_tinfo(c_decl)
    if tif is None:
        return False
    if hasattr(ida_struct, "set_member_tinfo"):
        return bool(ida_struct.set_member_tinfo(st, member, 0, tif, 0))
    return False


def _member_flag(size):
    if size <= 1:
        return getattr(ida_bytes, "FF_BYTE", 0)
    if size == 2:
        return getattr(ida_bytes, "FF_WORD", 0)
    if size == 4:
        return getattr(ida_bytes, "FF_DWORD", 0)
    if size == 8:
        return getattr(ida_bytes, "FF_QWORD", 0)
    return getattr(ida_bytes, "FF_BYTE", 0)


def _parse_address(value):
    if value is None or value == "":
        raise ValueError("missing address")
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("missing address")
        return int(text, 16) if text.lower().startswith("0x") else int(text, 16)
    return int(value)


def _safe_name(name):
    if not isinstance(name, str):
        return ""
    clean = name.strip()
    if not clean:
        return ""
    if hasattr(ida_name, "validate_name"):
        try:
            validated = ida_name.validate_name(clean, ida_name.VNT_IDENT)
            if isinstance(validated, str) and validated:
                return validated
            if validated is True:
                return clean
        except Exception:
            pass
    return clean


def _name_flags(force=False, check=True):
    flags = getattr(ida_name, "SN_NOWARN", 0)
    if force:
        flags |= getattr(ida_name, "SN_FORCE", 0)
    if check:
        flags |= getattr(ida_name, "SN_CHECK", 0)
    else:
        flags |= getattr(ida_name, "SN_NOCHECK", 0)
    return flags


def _rename_at(ea, name, scope="auto", force=False, function_start=True):
    clean_name = _safe_name(name)
    if not clean_name:
        return {"ok": False, "error": "Invalid or empty name", "address": hex(ea), "name": name}

    target_ea = ea
    func = ida_funcs.get_func(ea)
    if scope in ("function", "func") or (scope == "auto" and function_start and func is not None):
        target_ea = func.start_ea if func is not None else ea

    current_name = ida_name.get_name(target_ea) or ""
    attempts = []
    for mode, flags in (
        ("check", _name_flags(force=False, check=True)),
        ("nocheck", _name_flags(force=False, check=False)),
        ("force", _name_flags(force=True, check=False)),
    ):
        if mode == "force" and not force:
            continue
        ok = bool(ida_name.set_name(target_ea, clean_name, flags))
        attempts.append({"mode": mode, "ok": ok})
        if ok:
            new_name = ida_name.get_name(target_ea) or clean_name
            return {
                "ok": True,
                "address": hex(ea),
                "target_address": hex(target_ea),
                "scope": scope,
                "old_name": current_name,
                "name": new_name,
                "requested_name": name,
                "attempts": attempts,
            }

    existing_ea = ida_name.get_name_ea(idaapi.BADADDR, clean_name)
    error = "set_name failed"
    if existing_ea != idaapi.BADADDR and existing_ea != target_ea:
        error = "name already exists at another address"
    if target_ea == idaapi.BADADDR:
        error = "bad target address"
    return {
        "ok": False,
        "error": error,
        "address": hex(ea),
        "target_address": hex(target_ea),
        "scope": scope,
        "old_name": current_name,
        "name": clean_name,
        "conflict_address": hex(existing_ea) if existing_ea != idaapi.BADADDR else None,
        "attempts": attempts,
        "retry_hint": "Pass force=true for a unique forced name, or choose another name if conflict_address is set.",
    }


def _get_struct_api():
    return ida_struct if ida_struct is not None else idaapi


def _get_struct_by_name(name):
    api = _get_struct_api()
    sid = api.get_struc_id(name) if hasattr(api, "get_struc_id") else idaapi.get_struc_id(name)
    if sid == idaapi.BADADDR or sid == 0xFFFFFFFF:
        return None, sid, api
    st = api.get_struc(sid) if hasattr(api, "get_struc") else idaapi.get_struc(sid)
    return st, sid, api


def _member_by_offset(api, st, offset):
    if hasattr(api, "get_member"):
        return api.get_member(st, int(offset))
    if hasattr(idaapi, "get_member"):
        return idaapi.get_member(st, int(offset))
    return None


def _member_by_name(api, st, name):
    if hasattr(api, "get_member_by_name"):
        return api.get_member_by_name(st, name)
    if hasattr(idaapi, "get_member_by_name"):
        return idaapi.get_member_by_name(st, name)
    return None


def _set_struct_member_type(st, member_obj, c_decl):
    ok = _set_member_tinfo(st, member_obj, c_decl)
    return {"ok": bool(ok), "type_name": c_decl}


# ── Command Handlers ───────────────────────────────────────────────
# Each handler returns a dict that will be JSON-serialized back.

def cmd_get_info(_params):
    """Get basic info about the loaded database."""
    def _inner():
        input_file = ida_nalt.get_input_file_path()
        module_name = os.path.basename(input_file) if input_file else ""
        return {
            "plugin": PLUGIN_NAME,
            "version": PLUGIN_VERSION,
            "file": input_file,
            "database_path": input_file,
            "binary_path": input_file,
            "module_path": input_file,
            "module_name": module_name,
            "processor": ida_ida.inf_get_procname() if hasattr(ida_ida, 'inf_get_procname') else idc.get_inf_attr(idc.INF_PROCNAME),
            "imagebase": hex(idaapi.get_imagebase()),
            "min_ea": hex(idc.get_inf_attr(idc.INF_MIN_EA)),
            "max_ea": hex(idc.get_inf_attr(idc.INF_MAX_EA)),
            "num_functions": ida_funcs.get_func_qty(),
            "http_port": ACTIVE_HTTP_PORT,
            "process_id": os.getpid(),
            "instance_key": f"ida|{ACTIVE_HTTP_PORT}|{input_file}",
        }
    return sync_exec(_inner)


def cmd_list_instances(params):
    """Report the current IDA instance so the external bridge can enumerate ports."""
    return cmd_get_info(params)


def cmd_list_functions(params):
    """List functions with offset/limit pagination."""
    offset = int(params.get("offset", 0))
    limit = int(params.get("limit", 50))

    def _inner():
        result = []
        for i, ea in enumerate(idautils.Functions()):
            if i < offset:
                continue
            if len(result) >= limit:
                break
            func = ida_funcs.get_func(ea)
            name = ida_name.get_name(ea) or f"sub_{ea:X}"
            result.append({
                "ea": hex(ea),
                "name": name,
                "size": func.size() if func else 0,
            })
        return {"functions": result, "total": ida_funcs.get_func_qty()}
    return sync_exec(_inner)


def cmd_decompile(params):
    """Decompile a function at the given address."""
    addr = params.get("address") or params.get("ea")
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        try:
            import ida_hexrays
        except ImportError:
            return {"error": "Hex-Rays decompiler not available"}

        func = ida_funcs.get_func(ea)
        if not func:
            return {"error": f"No function at {hex(ea)}"}

        try:
            cfunc = ida_hexrays.decompile(func.start_ea)
            if not cfunc:
                return {"error": f"Decompilation failed at {hex(ea)}"}

            lines = []
            sv = cfunc.get_pseudocode()
            for i in range(sv.size()):
                raw_line = sv[i].line
                try:
                    line = ida_lines.tag_remove(raw_line)
                except:
                    line = idaapi.tag_remove(raw_line)
                lines.append(line)

            return {
                "address": hex(func.start_ea),
                "name": ida_name.get_name(func.start_ea) or f"sub_{func.start_ea:X}",
                "pseudocode": "\n".join(lines),
                "lines": len(lines),
            }
        except Exception as e:
            return {"error": f"Decompile error: {str(e)}"}

    return sync_exec(_inner)


def cmd_get_disasm(params):
    """Get disassembly lines around an address."""
    addr = params.get("address") or params.get("ea")
    count = int(params.get("count", 20))
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        lines = []
        current = ea
        for _ in range(count):
            disasm = idc.generate_disasm_line(current, 0)
            if disasm is None:
                break
            lines.append({
                "ea": hex(current),
                "disasm": disasm,
                "bytes": ida_bytes.get_bytes(current, idc.get_item_size(current)).hex() if ida_bytes.get_bytes(current, idc.get_item_size(current)) else "",
            })
            current = idc.next_head(current)
            if current == idaapi.BADADDR:
                break
        return {"lines": lines}
    return sync_exec(_inner)


def cmd_rename_symbol(params):
    """Rename a symbol at address."""
    addr = params.get("address") or params.get("ea")
    name = params.get("name")
    if not addr or not name:
        return {"error": "Missing 'address' and/or 'name' parameter"}

    ea = _parse_address(addr)
    scope = params.get("scope") or params.get("kind") or "auto"
    force = bool(params.get("force", False))
    function_start = bool(params.get("function_start", True))

    def _inner():
        return _rename_at(ea, name, scope=scope, force=force, function_start=function_start)
    return sync_exec(_inner, write=True)


def cmd_rename_many(params):
    """Rename several symbols/functions with per-item diagnostics."""
    items = params.get("items") or params.get("renames") or []
    if not isinstance(items, list):
        return {"ok": False, "error": "'items' must be a list"}

    max_items = min(int(params.get("max_items", 64)), 128)
    stop_on_error = bool(params.get("stop_on_error", False))
    default_force = bool(params.get("force", False))
    results = []
    failed = 0

    def _inner():
        nonlocal failed
        for index, item in enumerate(items[:max_items]):
            if not isinstance(item, dict):
                failed += 1
                results.append({"index": index, "ok": False, "error": "rename item must be an object"})
                if stop_on_error:
                    break
                continue
            try:
                ea = _parse_address(item.get("address") or item.get("ea"))
                result = _rename_at(
                    ea,
                    item.get("name"),
                    scope=item.get("scope") or item.get("kind") or "auto",
                    force=bool(item.get("force", default_force)),
                    function_start=bool(item.get("function_start", True)),
                )
            except Exception as e:
                result = {"ok": False, "error": str(e)}
            if not result.get("ok", False):
                failed += 1
            results.append({"index": index, **result})
            if not result.get("ok", False) and stop_on_error:
                break
        return {
            "ok": failed == 0,
            "count": len(results),
            "failed": failed,
            "truncated": len(items) > max_items,
            "results": results,
        }

    return sync_exec(_inner, write=True)


def cmd_set_comment(params):
    """Set a comment at address."""
    addr = params.get("address") or params.get("ea")
    comment = params.get("comment", "")
    is_func = params.get("func", False)
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        if is_func:
            func = ida_funcs.get_func(ea)
            if func:
                idc.set_func_cmt(func.start_ea, comment, 1)
                return {"ok": True, "type": "function"}
        idc.set_cmt(ea, comment, 0)
        return {"ok": True, "type": "inline"}
    return sync_exec(_inner, write=True)


def cmd_read_bytes(params):
    """Read raw bytes from address."""
    addr = params.get("address") or params.get("ea")
    size = int(params.get("size", 16))
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        data = ida_bytes.get_bytes(ea, size)
        if data is None:
            return {"error": f"Cannot read {size} bytes at {hex(ea)}"}
        return {"hex": data.hex(), "address": hex(ea), "size": size}
    return sync_exec(_inner)


def cmd_get_xrefs(params):
    """Get cross-references to/from an address."""
    addr = params.get("address") or params.get("ea")
    direction = params.get("direction", "to")  # "to" or "from"
    if not addr:
        return {"error": "Missing 'address' parameter"}

    ea = int(addr, 16) if isinstance(addr, str) else int(addr)

    def _inner():
        refs = []
        if direction == "to":
            for xref in idautils.XrefsTo(ea):
                refs.append({
                    "from": hex(xref.frm),
                    "to": hex(xref.to),
                    "type": xref.type,
                })
        else:
            for xref in idautils.XrefsFrom(ea):
                refs.append({
                    "from": hex(xref.frm),
                    "to": hex(xref.to),
                    "type": xref.type,
                })
        return {"xrefs": refs, "count": len(refs), "direction": direction}
    return sync_exec(_inner)


def cmd_get_strings(params):
    """Get all strings in the database."""
    min_len = int(params.get("min_length", 4))

    def _inner():
        strings = []
        sc = idautils.Strings()
        for s in sc:
            if s.length >= min_len:
                strings.append({
                    "ea": hex(s.ea),
                    "value": str(s),
                    "length": s.length,
                })
                if len(strings) >= 500:  # Cap at 500
                    break
        return {"strings": strings, "count": len(strings)}
    return sync_exec(_inner)


def cmd_search_string(params):
    """Search for a string pattern in the binary's string table."""
    pattern = params.get("pattern", "")
    case_sensitive = params.get("case_sensitive", False)
    max_results = min(int(params.get("max_results", 100)), 500)
    if not pattern:
        return {"error": "Missing 'pattern' parameter"}

    def _inner():
        import re
        results = []
        sc = idautils.Strings()
        flags = 0 if case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error:
            # Fallback to plain substring match
            regex = None

        for s in sc:
            s_val = str(s)
            matched = False
            if regex:
                matched = bool(regex.search(s_val))
            else:
                if case_sensitive:
                    matched = pattern in s_val
                else:
                    matched = pattern.lower() in s_val.lower()

            if matched:
                # Find xrefs to this string for context
                xrefs = [hex(x.frm) for x in idautils.XrefsTo(s.ea)]
                results.append({
                    "ea": hex(s.ea),
                    "value": s_val,
                    "length": s.length,
                    "xrefs": xrefs[:10],
                })
                if len(results) >= max_results:
                    break
        return {"results": results, "count": len(results), "pattern": pattern}
    return sync_exec(_inner)


def cmd_search_bytes(params):
    """Search for a hex byte pattern in the binary (supports ?? wildcards).
    Example: '48 8B ?? 10' or 'E8 ?? ?? ?? ??'
    """
    hex_pattern = params.get("hex_pattern", "").strip()
    start_addr = params.get("start", None)
    max_results = min(int(params.get("max_results", 50)), 200)
    if not hex_pattern:
        return {"error": "Missing 'hex_pattern' parameter"}

    def _inner():
        # Convert hex pattern to IDA binary search format
        # IDA uses  "48 8B ? 10" with single ? for wildcard
        search_str = hex_pattern.replace("??", "?").strip()

        min_ea = idc.get_inf_attr(idc.INF_MIN_EA)
        max_ea = idc.get_inf_attr(idc.INF_MAX_EA)
        ea = int(start_addr, 16) if start_addr else min_ea

        results = []
        while ea < max_ea and len(results) < max_results:
            ea = ida_bytes.bin_search(
                ea, max_ea,
                bytes.fromhex(hex_pattern.replace("??", "00").replace(" ", "")),
                None,  # mask (None = no wildcards via this param)
                ida_bytes.BIN_SEARCH_FORWARD,
                0  # flags
            )
            if ea == idaapi.BADADDR:
                break

            # Get context: function name if in a function
            func = ida_funcs.get_func(ea)
            func_name = ida_name.get_name(func.start_ea) if func else None
            disasm = idc.generate_disasm_line(ea, 0)

            results.append({
                "ea": hex(ea),
                "function": func_name,
                "disasm": disasm,
            })
            ea += 1

        return {"results": results, "count": len(results), "pattern": hex_pattern}
    return sync_exec(_inner)


def cmd_get_segments(params):
    """List all segments in the binary."""
    def _inner():
        segments = []
        for seg_ea in idautils.Segments():
            seg = idaapi.getseg(seg_ea)
            if seg:
                # Get permissions safely across IDA versions
                perm_str = "---"
                try:
                    p = seg.perm
                    perm_str = "%s%s%s" % (
                        "R" if p & 4 else "-",  # SFL_READ = 4
                        "W" if p & 2 else "-",  # SFL_WRITE = 2
                        "X" if p & 1 else "-",  # SFL_EXEC = 1
                    )
                except Exception:
                    pass

                seg_class = ""
                try:
                    seg_class = idaapi.get_segm_class(seg) or ""
                except Exception:
                    pass

                segments.append({
                    "name": idaapi.get_segm_name(seg) or "unknown",
                    "start": hex(seg.start_ea),
                    "end": hex(seg.end_ea),
                    "size": hex(seg.size()),
                    "perm": perm_str,
                    "class": seg_class,
                })
        return {"segments": segments, "count": len(segments)}
    return sync_exec(_inner)


def cmd_search_functions(params):
    """Search functions by name pattern (substring or regex)."""
    pattern = params.get("pattern", "")
    max_results = min(int(params.get("max_results", 50)), 200)
    if not pattern:
        return {"error": "Missing 'pattern' parameter"}

    def _inner():
        import re
        results = []
        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error:
            regex = None

        for ea in idautils.Functions():
            name = ida_name.get_name(ea) or f"sub_{ea:X}"
            matched = False
            if regex:
                matched = bool(regex.search(name))
            else:
                matched = pattern.lower() in name.lower()

            if matched:
                func = ida_funcs.get_func(ea)
                results.append({
                    "ea": hex(ea),
                    "name": name,
                    "size": func.size() if func else 0,
                })
                if len(results) >= max_results:
                    break
        return {"results": results, "count": len(results), "pattern": pattern}
    return sync_exec(_inner)


def cmd_rename_local(params):
    """Rename a local variable in Hex-Rays decompiler output."""
    function_address = params.get("function_address") or params.get("address")
    old_name = params.get("old_name")
    new_name = params.get("new_name")
    if not function_address or not old_name or not new_name:
        return {"error": "Missing 'function_address', 'old_name', or 'new_name' parameter"}

    ea = _parse_address(function_address)

    def _inner():
        try:
            import ida_hexrays
        except ImportError:
            return {"error": "Hex-Rays decompiler not available"}

        if hasattr(ida_hexrays, "rename_lvar"):
            ok = ida_hexrays.rename_lvar(ea, old_name, new_name)
            return {"ok": bool(ok), "function_address": hex(ea), "old_name": old_name, "new_name": new_name}

        return {"error": "rename_lvar API not available in this IDA build"}

    return sync_exec(_inner, write=True)


def cmd_apply_type(params):
    """Apply a type declaration to an address."""
    addr = params.get("address") or params.get("ea")
    c_decl = params.get("c_decl") or params.get("prototype") or params.get("decl")
    if not addr or not c_decl:
        return {"error": "Missing 'address' and/or type declaration parameter"}

    ea = _parse_address(addr)
    return sync_exec(lambda: _set_type_at(ea, c_decl), write=True)


def cmd_set_function_type(params):
    """Set the prototype of a function."""
    addr = params.get("address") or params.get("ea")
    prototype = params.get("prototype") or params.get("decl")
    if not addr or not prototype:
        return {"error": "Missing 'address' and/or 'prototype' parameter"}

    ea = _parse_address(addr)
    return sync_exec(lambda: _set_type_at(ea, prototype), write=True)


def cmd_apply_types(params):
    """Apply several address types/prototypes in one request."""
    items = params.get("items") or params.get("types") or []
    if not isinstance(items, list):
        return {"ok": False, "error": "'items' must be a list"}

    max_items = min(int(params.get("max_items", 64)), 128)
    stop_on_error = bool(params.get("stop_on_error", False))
    results = []
    failed = 0

    def _inner():
        nonlocal failed
        for index, item in enumerate(items[:max_items]):
            if not isinstance(item, dict):
                result = {"ok": False, "error": "type item must be an object"}
            else:
                try:
                    ea = _parse_address(item.get("address") or item.get("ea"))
                    c_decl = item.get("c_decl") or item.get("prototype") or item.get("decl") or item.get("type")
                    if not c_decl:
                        result = {"ok": False, "error": "missing type declaration"}
                    else:
                        result = _set_type_at(ea, c_decl)
                except Exception as e:
                    result = {"ok": False, "error": str(e)}
            if not result.get("ok", False):
                failed += 1
            results.append({"index": index, **result})
            if not result.get("ok", False) and stop_on_error:
                break
        return {
            "ok": failed == 0,
            "count": len(results),
            "failed": failed,
            "truncated": len(items) > max_items,
            "results": results,
        }

    return sync_exec(_inner, write=True)


def cmd_import_c_declarations(params):
    """Import one or more C declarations into Local Types."""
    declarations = params.get("declarations")
    if not declarations:
        return {"error": "Missing 'declarations' parameter"}

    def _inner():
        if hasattr(ida_typeinf, "parse_decls"):
            til = ida_typeinf.get_idati()
            try:
                ok = ida_typeinf.parse_decls(til, declarations, None, 0)
                return {"ok": bool(ok), "count": len(declarations.splitlines()), "mode": "parse_decls"}
            except Exception as e:
                return {"ok": False, "error": str(e)}

        return {"ok": False, "error": "parse_decls API not available in this IDA build"}

    return sync_exec(_inner, write=True)


def cmd_create_struct(params):
    """Create or update a struct type."""
    name = params.get("name")
    members = params.get("members") or []
    if not name:
        return {"error": "Missing 'name' parameter"}

    def _inner():
        api = _get_struct_api()
        sid = api.get_struc_id(name) if hasattr(api, "get_struc_id") else idaapi.get_struc_id(name)
        if sid == idaapi.BADADDR or sid == 0xFFFFFFFF:
            sid = api.add_struc(idaapi.BADADDR, name, False)
        st = api.get_struc(sid) if hasattr(api, "get_struc") else idaapi.get_struc(sid)
        if not st:
          return {"ok": False, "error": f"Could not create or load struct {name}"}

        applied = []
        for member in members:
            if not isinstance(member, dict):
                continue
            member_name = member.get("name")
            offset = int(member.get("offset", 0))
            size = int(member.get("size", 1))
            type_name = member.get("type_name") or member.get("type") or ""
            comment = member.get("comment") or ""
            if not member_name:
                continue
            flags = _member_flag(size)
            if hasattr(api, "add_struc_member"):
                rc = api.add_struc_member(st, member_name, offset, flags, None, size)
            else:
                rc = idaapi.add_struc_member(st, member_name, offset, flags, None, size)
            member_obj = _member_by_name(api, st, member_name) or _member_by_offset(api, st, offset)
            if type_name and member_obj is not None:
                type_ok = _set_member_tinfo(st, member_obj, type_name)
            else:
                type_ok = None
            if comment and member_obj is not None and hasattr(idc, "set_member_cmt"):
                try:
                    idc.set_member_cmt(st.id if hasattr(st, "id") else sid, offset, comment, 0)
                except Exception:
                    pass
            applied.append({
                "name": member_name,
                "offset": offset,
                "size": size,
                "type_name": type_name,
                "result": rc,
                "type_ok": type_ok,
            })

        return {
            "ok": True,
            "name": name,
            "struct_id": sid,
            "members": applied,
        }

    return sync_exec(_inner, write=True)


def cmd_add_struct_member(params):
    """Add a single member to an existing struct."""
    struct_name = params.get("struct_name")
    member_name = params.get("member_name")
    offset = params.get("offset")
    size = int(params.get("size", 1))
    type_name = params.get("type_name") or ""
    comment = params.get("comment") or ""
    if not struct_name or not member_name or offset is None:
        return {"error": "Missing 'struct_name', 'member_name', or 'offset' parameter"}

    def _inner():
        st, sid, api = _get_struct_by_name(struct_name)
        if not st:
            return {"ok": False, "error": f"Struct not found: {struct_name}"}

        flags = _member_flag(size)
        rc = api.add_struc_member(st, member_name, int(offset), flags, None, size)
        member_obj = _member_by_name(api, st, member_name) or _member_by_offset(api, st, int(offset))
        if type_name and member_obj is not None:
            type_ok = _set_member_tinfo(st, member_obj, type_name)
        else:
            type_ok = None
        if comment and member_obj is not None and hasattr(idc, "set_member_cmt"):
            try:
                idc.set_member_cmt(st.id if hasattr(st, "id") else sid, int(offset), comment, 0)
            except Exception:
                pass

        return {
            "ok": bool(rc == 0 or rc is True),
            "struct_name": struct_name,
            "member_name": member_name,
            "offset": int(offset),
            "size": size,
            "type_name": type_name,
            "type_ok": type_ok,
        }

    return sync_exec(_inner, write=True)


def cmd_set_struct_member_type(params):
    """Set a struct member type by struct/member name or offset."""
    struct_name = params.get("struct_name")
    type_name = params.get("type_name") or params.get("c_decl") or params.get("type")
    member_name = params.get("member_name")
    offset = params.get("offset")
    if not struct_name or not type_name or (member_name is None and offset is None):
        return {"error": "Missing 'struct_name', member selector, or type declaration"}

    def _inner():
        st, _sid, api = _get_struct_by_name(struct_name)
        if not st:
            return {"ok": False, "error": f"Struct not found: {struct_name}"}
        member_obj = _member_by_name(api, st, member_name) if member_name is not None else _member_by_offset(api, st, int(offset))
        if member_obj is None:
            return {"ok": False, "error": "Struct member not found", "struct_name": struct_name, "member_name": member_name, "offset": offset}
        result = _set_struct_member_type(st, member_obj, type_name)
        result.update({"struct_name": struct_name, "member_name": member_name, "offset": offset})
        return result

    return sync_exec(_inner, write=True)


def cmd_rename_struct_member(params):
    """Rename a struct member by name or offset."""
    struct_name = params.get("struct_name")
    old_name = params.get("old_name") or params.get("member_name")
    new_name = params.get("new_name") or params.get("name")
    offset = params.get("offset")
    if not struct_name or not new_name or (old_name is None and offset is None):
        return {"error": "Missing 'struct_name', member selector, or new name"}

    def _inner():
        st, sid, api = _get_struct_by_name(struct_name)
        if not st:
            return {"ok": False, "error": f"Struct not found: {struct_name}"}
        member_obj = _member_by_name(api, st, old_name) if old_name is not None else _member_by_offset(api, st, int(offset))
        if member_obj is None:
            return {"ok": False, "error": "Struct member not found", "struct_name": struct_name, "old_name": old_name, "offset": offset}
        member_offset = getattr(member_obj, "soff", None)
        if member_offset is None:
            member_offset = int(offset) if offset is not None else 0
        if hasattr(api, "set_member_name"):
            ok = api.set_member_name(st, member_offset, new_name)
        elif hasattr(idc, "set_member_name"):
            ok = idc.set_member_name(sid, member_offset, new_name)
        else:
            return {"ok": False, "error": "set_member_name API not available"}
        return {
            "ok": bool(ok),
            "struct_name": struct_name,
            "old_name": old_name,
            "new_name": new_name,
            "offset": int(member_offset),
        }

    return sync_exec(_inner, write=True)


def cmd_delete_struct_member(params):
    """Delete a struct member by offset."""
    struct_name = params.get("struct_name")
    offset = params.get("offset")
    if not struct_name or offset is None:
        return {"error": "Missing 'struct_name' or 'offset' parameter"}

    def _inner():
        st, _sid, api = _get_struct_by_name(struct_name)
        if not st:
            return {"ok": False, "error": f"Struct not found: {struct_name}"}
        if hasattr(api, "del_struc_member"):
            ok = api.del_struc_member(st, int(offset))
        elif hasattr(idaapi, "del_struc_member"):
            ok = idaapi.del_struc_member(st, int(offset))
        else:
            return {"ok": False, "error": "del_struc_member API not available"}
        return {"ok": bool(ok), "struct_name": struct_name, "offset": int(offset)}

    return sync_exec(_inner, write=True)


def cmd_list_structs(params):
    """List structs and local types matching a filter."""
    pattern = params.get("pattern", "")
    max_results = min(int(params.get("max_results", 100)), 200)

    def _inner():
        api = ida_struct if ida_struct is not None else idaapi
        results = []
        qty = api.get_struc_qty() if hasattr(api, "get_struc_qty") else idaapi.get_struc_qty()
        for i in range(qty):
            st = api.get_struc_by_idx(i) if hasattr(api, "get_struc_by_idx") else idaapi.get_struc_by_idx(i)
            if not st:
                continue
            name = api.get_struc_name(st) if hasattr(api, "get_struc_name") else idaapi.get_struc_name(st)
            if pattern and pattern.lower() not in name.lower():
                continue
            member_count = 0
            if hasattr(api, "get_member_qty"):
                try:
                    member_count = api.get_member_qty(st)
                except Exception:
                    member_count = 0
            results.append({
                "name": name,
                "id": st.id if hasattr(st, "id") else i,
                "members": member_count,
            })
            if len(results) >= max_results:
                break
        return {"results": results, "count": len(results), "pattern": pattern}

    return sync_exec(_inner)


def cmd_get_types(params):
    """List local types using the struct inventory fallback."""
    return cmd_list_structs(params)


def cmd_apply_plan(params):
    """Apply a bounded edit plan: declarations, structs, renames, types, comments."""
    max_operations = min(int(params.get("max_operations", 128)), 256)
    stop_on_error = bool(params.get("stop_on_error", False))
    results = []
    failed = 0
    operations = 0

    def append_result(section, result):
        nonlocal failed, operations
        operations += 1
        ok = not _batch_result_failed(result)
        if not ok:
            failed += 1
        results.append({"section": section, "ok": ok, "result": result})
        return ok

    def should_stop(ok):
        return (not ok and stop_on_error) or operations >= max_operations

    declarations = params.get("declarations")
    if declarations:
        ok = append_result("declarations", cmd_import_c_declarations({"declarations": declarations}))
        if should_stop(ok):
            return {"ok": failed == 0, "count": operations, "failed": failed, "stopped": True, "results": results}

    for struct in (params.get("structs") or [])[:max_operations]:
        ok = append_result("structs", cmd_create_struct(struct if isinstance(struct, dict) else {}))
        if should_stop(ok):
            return {"ok": failed == 0, "count": operations, "failed": failed, "stopped": True, "results": results}

    if params.get("renames"):
        ok = append_result("renames", cmd_rename_many({
            "items": params.get("renames"),
            "stop_on_error": stop_on_error,
            "max_items": max_operations - operations,
            "force": params.get("force", False),
        }))
        if should_stop(ok):
            return {"ok": failed == 0, "count": operations, "failed": failed, "stopped": True, "results": results}

    if params.get("local_renames"):
        for item in params.get("local_renames")[:max_operations - operations]:
            ok = append_result("local_renames", cmd_rename_local(item if isinstance(item, dict) else {}))
            if should_stop(ok):
                return {"ok": failed == 0, "count": operations, "failed": failed, "stopped": True, "results": results}

    if params.get("types"):
        ok = append_result("types", cmd_apply_types({
            "items": params.get("types"),
            "stop_on_error": stop_on_error,
            "max_items": max_operations - operations,
        }))
        if should_stop(ok):
            return {"ok": failed == 0, "count": operations, "failed": failed, "stopped": True, "results": results}

    for comment in (params.get("comments") or [])[:max_operations - operations]:
        ok = append_result("comments", cmd_set_comment(comment if isinstance(comment, dict) else {}))
        if should_stop(ok):
            return {"ok": failed == 0, "count": operations, "failed": failed, "stopped": True, "results": results}

    return {
        "ok": failed == 0,
        "count": operations,
        "failed": failed,
        "stopped": False,
        "truncated": operations >= max_operations,
        "results": results,
    }


MUTATING_COMMANDS = {
    "rename",
    "rename_symbol",
    "rename_function",
    "rename_global",
    "rename_many",
    "rename_local",
    "set_comment",
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


def _normalize_batch_command(name):
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
        "rename_function": "rename_function",
        "rename_global": "rename_global",
        "rename_many": "rename_many",
        "bulk_rename": "rename_many",
        "apply_types": "apply_types",
        "set_member_type": "set_struct_member_type",
        "rename_member": "rename_struct_member",
        "delete_member": "delete_struct_member",
        "apply_plan": "apply_plan",
    }
    return aliases.get(clean, clean)


def _batch_result_failed(result):
    return isinstance(result, dict) and ("error" in result or result.get("ok") is False)


def cmd_batch(params):
    """Execute several bounded IDA commands in one HTTP request."""
    requests = params.get("requests") or params.get("commands") or []
    if not isinstance(requests, list):
        return {"ok": False, "error": "'requests' must be a list"}

    max_requests = min(int(params.get("max_requests", 32)), 32)
    stop_on_error = bool(params.get("stop_on_error", True))
    allow_mutations = bool(params.get("allow_mutations", False))
    results = []
    failed = 0
    stopped = False

    for index, item in enumerate(requests[:max_requests]):
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

        handler = COMMANDS.get(command)
        if handler is None:
            failed += 1
            results.append({"index": index, "id": request_id, "command": command, "ok": False, "error": "unknown command"})
            if stop_on_error:
                stopped = True
                break
            continue

        mutates = command in MUTATING_COMMANDS
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

        try:
            result = handler(item.get("params") or item.get("payload") or {})
            ok = not _batch_result_failed(result)
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
        except Exception as e:
            failed += 1
            results.append({
                "index": index,
                "id": request_id,
                "command": command,
                "ok": False,
                "mutates": mutates,
                "error": str(e),
            })
            if stop_on_error:
                stopped = True
                break

    return {
        "ok": failed == 0,
        "count": len(results),
        "failed": failed,
        "stopped": stopped,
        "truncated": len(requests) > max_requests,
        "results": results,
    }



# ── Command Dispatch Table ─────────────────────────────────────────

COMMANDS = {
    "get_info":        cmd_get_info,
    "list_instances":  cmd_list_instances,
    "list_functions":  cmd_list_functions,
    "decompile":       cmd_decompile,
    "get_pseudocode":  cmd_decompile,   # alias
    "get_disasm":      cmd_get_disasm,
    "rename":          cmd_rename_symbol,
    "rename_symbol":   cmd_rename_symbol,
    "rename_function": lambda params: cmd_rename_symbol({**params, "scope": "function"}),
    "rename_global":   lambda params: cmd_rename_symbol({**params, "scope": "address"}),
    "rename_many":     cmd_rename_many,
    "set_comment":     cmd_set_comment,
    "read_bytes":      cmd_read_bytes,
    "get_xrefs":         cmd_get_xrefs,
    "xrefs":             cmd_get_xrefs,   # alias
    "get_strings":       cmd_get_strings,
    "search_string":     cmd_search_string,
    "search_bytes":      cmd_search_bytes,
    "get_segments":      cmd_get_segments,
    "search_functions":  cmd_search_functions,
    "rename_local":      cmd_rename_local,
    "apply_type":        cmd_apply_type,
    "apply_types":       cmd_apply_types,
    "set_function_type": cmd_set_function_type,
    "import_c_declarations": cmd_import_c_declarations,
    "create_struct":     cmd_create_struct,
    "add_struct_member": cmd_add_struct_member,
    "set_struct_member_type": cmd_set_struct_member_type,
    "rename_struct_member": cmd_rename_struct_member,
    "delete_struct_member": cmd_delete_struct_member,
    "list_structs":      cmd_list_structs,
    "get_types":         cmd_get_types,
    "apply_plan":        cmd_apply_plan,
    "batch":             cmd_batch,
}


# ── HTTP Request Handler ──────────────────────────────────────────
# Using stdlib http.server — NO external dependencies needed.

class HsaBridgeHandler(BaseHTTPRequestHandler):
    """Handle incoming JSON commands from the MCP bridge."""

    def log_message(self, format, *args):
        """Redirect http.server logs to IDA Output window."""
        ida_kernwin.execute_sync(
            lambda: ida_kernwin.msg(f"[HSA] {format % args}\n"),
            ida_kernwin.MFF_NOWAIT,
        )

    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        info = {
            "status": "ok",
            "plugin": PLUGIN_NAME,
            "version": PLUGIN_VERSION,
            "port": ACTIVE_HTTP_PORT,
            "commands": list(COMMANDS.keys()),
        }
        try:
            info.update(cmd_get_info({}))
            info["port"] = ACTIVE_HTTP_PORT
        except Exception as e:
            info["info_error"] = str(e)
        self.wfile.write(json.dumps(info).encode())

    def do_POST(self):
        """Execute a command."""
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len)
            req = json.loads(body.decode("utf-8"))

            cmd_name = req.get("command") or req.get("cmd")
            params = req.get("params", {})

            if not cmd_name:
                self._send_error(400, "Missing 'command' field")
                return

            handler = COMMANDS.get(cmd_name)
            if not handler:
                self._send_error(404, f"Unknown command: {cmd_name}. Available: {list(COMMANDS.keys())}")
                return

            result = handler(params)
            self._send_json(200, {"ok": True, "data": result})

        except Exception as e:
            self._send_error(500, f"{str(e)}\n{traceback.format_exc()}")

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode())

    def _send_error(self, code, msg):
        self._send_json(code, {"ok": False, "error": msg})


# ── Plugin Class ───────────────────────────────────────────────────

class HsaMcpBridgePlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP  # Stay loaded for entire session
    wanted_name = PLUGIN_NAME
    wanted_hotkey = PLUGIN_HOTKEY
    comment = "HSA MCP Bridge — HTTP server for AI agent control"
    help = "Starts HTTP server on port 28472 for MCP bridge communication"

    _server = None
    _thread = None

    def init(self):
        """Called when IDA loads the plugin. Auto-starts HTTP server."""
        ida_kernwin.msg(f"[HSA] {PLUGIN_NAME} v{PLUGIN_VERSION} loaded.\n")
        # Auto-start HTTP server (no need for manual hotkey activation)
        self._start_server()
        return idaapi.PLUGIN_KEEP

    def _start_server(self):
        """Start the HTTP server in a background thread."""
        if self._server is not None:
            return  # Already running
        try:
            global ACTIVE_HTTP_PORT
            last_error = None
            for port in range(HTTP_PORT, HTTP_PORT + max(1, HTTP_PORT_RANGE)):
                try:
                    self._server = HTTPServer((HTTP_HOST, port), HsaBridgeHandler)
                    ACTIVE_HTTP_PORT = port
                    break
                except OSError as e:
                    last_error = e
                    self._server = None
            if self._server is None:
                raise last_error if last_error is not None else OSError("Unable to bind HTTP server")
            self._thread = threading.Thread(
                target=self._server.serve_forever,
                daemon=True,
                name="hsa-mcp-bridge",
            )
            self._thread.start()
            ida_kernwin.msg(f"[HSA] ✅ HTTP server auto-started on http://{HTTP_HOST}:{ACTIVE_HTTP_PORT}\n")
            ida_kernwin.msg(f"[HSA] Available commands: {', '.join(COMMANDS.keys())}\n")
        except OSError as e:
            ida_kernwin.msg(f"[HSA] ❌ Failed to start server: {e}\n")
            if "already in use" in str(e).lower() or "10048" in str(e):
                ida_kernwin.msg(f"[HSA] Port {HTTP_PORT} is already in use. Another instance running?\n")

    def run(self, _arg):
        """Called when user activates the plugin (hotkey or menu)."""
        if self._server is not None:
            ida_kernwin.msg(f"[HSA] Server already running on http://{HTTP_HOST}:{ACTIVE_HTTP_PORT}\n")
            return
        self._start_server()

    def term(self):
        """Called when IDA is shutting down."""
        if self._server:
            ida_kernwin.msg(f"[HSA] Shutting down HTTP server...\n")
            self._server.shutdown()
            self._server = None
            self._thread = None


def PLUGIN_ENTRY():
    """IDA plugin entry point — MUST return a plugin_t instance."""
    return HsaMcpBridgePlugin()
